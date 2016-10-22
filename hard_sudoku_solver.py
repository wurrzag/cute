#****************************************************************
#
#               CUT'N'PASTE FROM NET --- START
#
#
#from __future__ import generators
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

# another source...
def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc
#ucomb = []
#for uc in xuniqueCombinations([1, 2, 3, 4], 2): ucomb += [uc]
#for uc in xuniqueCombinations(['l','o','v','e'], 2): ucomb += [''.join(uc)]
#
#
#               CUT'N'PASTE FROM NET --- FINISH
#
#******************************************************************

def neg(s):
  key = '123456789'
  for g in s: key = key.replace(str(g), '')
  return key

def to_str(gr, ch = ''):
  for g in gr: ch += str(g)
  return ch

def nineXnine(a = 0):
  return [[a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9]


trigger_finished = False

def solve(board):
  global trigger_finished       # triggers to True once analysis finds a valid solution
  MAX = 9**4
  
  SW_DEPTH = '11000'            # five characters for five algorithms which may or may not
                                # be included in basic analysis:
                                # [naked_pairs, intersection_removal, naked_triples, hidden_elements(2), hidden_elements(3)]
                                # (defaults are '10000' and '11000')
                                # basic analysis is used only for sorting future-paths by best result
                                # full analysis, applied on (sorted) list of future-paths 
                                # is allways using all five methods (SW_DEPTH='11111')

  SW_SAFEMODE = [0, 0, 0, 0]    # pause and showboard() each step; levels: 
                                # [detailed, after main loop, brute force information, result only]

  SW_SAFEMODE_BOARD = 2         # showboard() includes main board
                                # >1 value for horizontal spaces between slots
  SW_SAFEMODE_SHADOW = 2        # showboard() includes candidate-list board
                                # >2 for mixed board (main + shadow in one)
  
                                # program-essential variables
  shadow = nineXnine(neg(''))   # list of candidates for each slot
    
  def validity_check():
    if is_todo():
      if count_shadows(): return 1
      else: return 0
    else:
      if count_shadows(): return 0
      else:
        return MAX if is_solved_board() else 0
  
  def is_todo():                        #Are we complete? check
    for i in board:
      for j in i:
        if not j: return True
    return False
  
  def is_solved_board():
    for key in range(1, 10):
      for i in range(9):
        if not(is_in_row(i, [key]) and is_in_column(i, [key]) and is_in_area(i, [key])): return 0
    return 1

  def count_shadows(q = 0):              #sum of candidates for all slots
    for i in shadow:
      for j in i:
        q += len(j)
    return q
  
  def showboard():
    if SW_SAFEMODE_BOARD:
      for i in board:
        ch = ''
        for j in i:
          if j: ch += str(j)
          else: ch += '.'
          ch += (SW_SAFEMODE_BOARD -1) * ' '
        print(ch)
      print(' __________n= ' + str(count_shadows()))
    if SW_SAFEMODE_SHADOW:
      for i in range(9):
        ch = ''
        for j in range(9):
          if len(shadow[i][j]): ch += '%8s' % shadow[i][j]
          else:
            if SW_SAFEMODE_SHADOW > 2: ch += '    ' + str(board[i][j]) + '.  '
            else: ch += 8* ' '
        print (ch)
        if SW_SAFEMODE_SHADOW > 1 and (i == 2 or i == 5): print(70* '.')
        
    
  def initial_reduce():
    for i in range(9):
      for j in range(9):
        if board[i][j]:
          write(i, j, board[i][j])
          
# *** removes given type of candidate in given scale
  def lighten(typ, a, b, whattt, exceptions = [], debugging = False):
    for what in whattt:
      if typ == 'slot':
        if not [a, b] in exceptions: shadow[a][b] = shadow[a][b].replace(what, '')
      if typ == 'column':
        for i in range(9):
          if not [i, b] in exceptions: shadow[i][b] = shadow[i][b].replace(what, '')
      if typ == 'row':
        for i in range(9):
          if not [a, i] in exceptions: shadow[a][i] = shadow[a][i].replace(what, '')
      if typ == 'area':
        for i in range(3):
          for j in range(3):
            aa = 3* (a//3) +i; bb = 3* (b//3) +j
            if not [aa, bb] in exceptions: shadow[aa][bb] = shadow[aa][bb].replace(what, '')
            if debugging: shadow[aa][bb] += 'X'
            
  
# *** writes sure-candidates on board (also in intersection_removal())
  def write_singles(again = True):                     # writes all sure candidates to board
    while(again):
      again = False
      for i in range(9):
        for j in range(9):
          if len(shadow[i][j]) == 1:
            again = True; write(i, j, int(shadow[i][j]))
        
  def write(a, b, what):
    board[a][b] = what; shadow[a][b] = ''
    lighten('column', a, b, str(what))
    lighten('row', a, b, str(what))
    lighten('area', a, b, str(what))

# ********************* ANALYSIS METHODS ***********************
# *** naked pairs
  def naked_pairs():
    pairs = []                  #list of all size=2 candidates
    for i in range(9):
      for j in range(9):
        if len(shadow[i][j]) == 2:
          is_new = True
          for k in pairs:
            if shadow[i][j] == k[0]: is_new = False; k += [[i, j]]
          if is_new: pairs += [[shadow[i][j], [i, j]]]    
#    print(pairs); getch()
    
    for k in pairs:
      if len(k) >= 3:
        ucomb = []
        for uc in xuniqueCombinations(k[1:], 2): ucomb += [uc]
#        print(k[0], ucomb);
        for i in ucomb:
          if is_same_area(i[0], i[1]): lighten('area', i[0][0], i[0][1], k[0], k[1:])
          if is_same_row(i[0], i[1]): lighten('row', i[0][0], i[0][1], k[0], k[1:])
          if is_same_column(i[0], i[1]): lighten('column', i[0][0], i[0][1], k[0], k[1:])
   
  def is_same_row(a, b):
    return True if a[0] == b[0] else False
  def is_same_column(a, b):
    return True if a[1] == b[1] else False
  def is_same_area(a, b):
    return True if a[0]//3 == b[0]//3 and a[1]//3 == b[1]//3 else False
    
  def is_in_row(a, what, debugging = False):
    for w in what:
      for i in range(9):
        if debugging: print(board[a][i], w, type(board[a][i]), type(w)); getch()
        if board[a][i] == w: return True
    return False
  def is_in_column(a, what):
    for w in what:
      for i in range(9):
        if board[i][a] == w: return True
    return False
  def is_in_area(a, what):
    for w in what:
      for i in range(3):
        for j in range(3):
          if board[3* (a//3) +i][3* (a%3) +j] == w: return True
    return False
  
  def is_this_group_only(x, y, group):
    sign = False;
    for g in group:
      if str(g) in shadow[x][y]:
        sign = True; break
    if not sign: return False
    for ag in neg(to_str((group))):
      if ag in shadow[x][y]: 
        return False
    return True
    
# *** hidden couples, triples, quads
  def hidden_elements(how_many):
    ucomb = []
    for uc in xuniqueCombinations([1, 2, 3, 4, 5, 6, 7, 8, 9], how_many): ucomb += [uc]
    for group in ucomb:
      for i in range(9):
        if not is_in_row(i, group):
          match = []
          for j in range(9):
            for g in group:
              if str(g) in shadow[i][j]: match += [j]; break
          if len(match) == how_many:
            for m in match: lighten('slot', i, m, neg(to_str(group)));
#            print('row', i, 'group ', group, 'match', match, 'n= ', count_shadows()); getch()
 
        if not is_in_column(i, group):
          match = []
          for j in range(9):
            for g in group:
              if str(g) in shadow[j][i]: match += [j]; break
          if len(match) == how_many:
            for m in match: lighten('slot', m, i, neg(to_str(group)));

        if not is_in_area(i, group):
          match = []
          for j in range(9):
            a = 3* (i//3) + j//3; b = 3* (i%3) + j%3
            for g in group:
              if str(g) in shadow[a][b]: match += [[a, b]]; break
          if len(match) == how_many:
            for m in match: lighten('slot', m[0], m[1], neg(to_str(group)));

# *** naked triples
  def naked_triples():
    ucomb = []
    for uc in xuniqueCombinations([1, 2, 3, 4, 5, 6, 7, 8, 9], 3): ucomb += [uc]
    for group in ucomb:
      for i in range(9):
        if not is_in_row(i, group):
          match = []
          for j in range(9):
            if is_this_group_only(i, j, group): match += [[i, j]]
          if len(match) == 3:
            lighten('row', i, 0, to_str(group), match)
            
        if not is_in_column(i, group):
          match = []
          for j in range(9):
            if is_this_group_only(j, i, group): match += [[j, i]]
          if len(match) == 3:
            lighten('column', 0, i, to_str(group), match)
            
        if not is_in_area(i, group):
          match = []
          for j in range(9):
            a = 3* (i//3) + j//3; b = 3* (i%3) + j%3
            if is_this_group_only(a, b, group): match += [[a, b]]
          if len(match) == 3:
            lighten('area', a, b, to_str(group), match)

# *** pointing pairs &triples + box line reduction            
  def intersection_removal():
    for key in range(1, 10):
      for i in range(9):
                
        match = []; check = [0, 0, 0]
        for j in range(9):
          if str(key) in shadow[i][j]: match += [[i, j]]; check[j // 3] = 1
# *** writes sure-candidate on board (4x)
        if len(match) == 1: write(match[0][0], match[0][1], key)
        elif len(match) == 2 or len(match) == 3:
          ch = 100* check[0] + 10* check[1] + check[2]
          if ch == 1 or ch == 10 or ch == 100: lighten('area', match[0][0], match[0][1], str(key), match)


        match = []; check = [0, 0, 0]
        for j in range(9):
          if str(key) in shadow[j][i]: match += [[j, i]]; check[j // 3] = 1
        if len(match) == 1: write(match[0][0], match[0][1], key)
        elif len(match) == 2 or len(match) == 3:
          ch = 4* check[0] + 2* check[1] + check[2]
          if ch == 1 or ch == 2 or ch == 4:
            lighten('area', match[0][0], match[0][1], str(key), match)

        match = []; check = [0, 0, 0]
        for j in range(9):
          a = 3* (i//3) + j//3; b = 3* (i%3) + j%3
          if str(key) in shadow[a][b]: match += [[a, b]]; check[j // 3] = 1
        if len(match) == 1: write(match[0][0], match[0][1], key)
        elif len(match) == 2 or len(match) == 3:
          ch = 4* check[0] + 2* check[1] + check[2]
          if ch == 1 or ch == 2 or ch == 4:
            lighten('row', match[0][0], match[0][1], str(key), match)

        match = []; check = [0, 0, 0]
        for j in range(9):
          a = 3* (i//3) + j%3; b = 3* (i%3) + j//3
          if str(key) in shadow[a][b]: match += [[a, b]]; check[j // 3] = 1
        if len(match) == 1: write(match[0][0], match[0][1], key)
        elif len(match) == 2 or len(match) == 3:
          ch = 4* check[0] + 2* check[1] + check[2]
          if ch == 1 or ch == 2 or ch == 4:
            lighten('column', match[0][0], match[0][1], str(key), match)
            

# *************** basic &full ANALYSIS ****************
  def main_loop(mask = '11111'):
    safe_mode = SW_SAFEMODE[0]
    mn = count_shadows(); m = mn; n = m - 1
    
    if mask[0] == '1':
      while(m > n): m = count_shadows(); naked_pairs(); write_singles(); n = count_shadows();
      if safe_mode: 
        print("naked pairs:", mn-m); showboard();
        if getch().lower() == 'q': return 'escape'

    if mask[1] == '1':
      mn = count_shadows(); m = mn; n = m - 1
      while(m > n):
        m = count_shadows(); intersection_removal(); write_singles(); n = count_shadows()
      if safe_mode:
        print("intersection removal:", mn-m); showboard();
        if getch().lower() == 'q': return 'escape'
  
    if mask[2] == '1':
      mn = count_shadows(); m = mn; n = m - 1
      while(m > n): m = count_shadows(); naked_triples(); write_singles(); n = count_shadows()
      if safe_mode:
        print("naked triples:", mn-m); showboard();
        if getch().lower() == 'q': return 'escape'
  
    if mask[3] == '1':
      mn = count_shadows(); m = mn; n = m - 1
      while(m > n): m = count_shadows(); hidden_elements(2); write_singles(); n = count_shadows()
      if safe_mode:
        print("hidden doubles:", mn-m); showboard();
        if getch().lower() == 'q': return 'escape'
  
    if mask[4] == '1':
      mn = count_shadows(); m = mn; n = m - 1
      while(m > n): m = count_shadows(); hidden_elements(3); write_singles(); n = count_shadows()
      if safe_mode:
        print("hidden triples:", mn-m); showboard();
        if getch().lower() == 'q': return 'escape'
    
    return 'breach'


  def basic_analysis():
    cs0 = 1; cs1 = 0
    while cs0 > cs1:
      cs0 = count_shadows(); main_loop(SW_DEPTH); cs1 = count_shadows()
    return cs0
        
  def full_analysis():
    safe_mode = SW_SAFEMODE[1]; n = 1; cs_start = count_shadows(); 
    while(n):
      cs0 = 1; cs1 = 0      
      while cs0 > cs1:
        cs0 = count_shadows(); exit_sign = main_loop(); cs1 = count_shadows()
        if exit_sign == 'escape': return 'escape'

      hq0 = count_shadows(); hq_start = hq0; hq1 = hq0 - 1
      while hq0 > hq1:
        hq0 = count_shadows(); hidden_elements(4); write_singles(); hq1 = count_shadows()
      n = hq_start - hq0
    
    if safe_mode:
      print("full_analysis:", cs_start - count_shadows()); showboard();
      if getch().lower() == 'q': return 'escape'
    return 'breach'
    
# ************************ BRUTE FORCE methods starts here ******************************
  #list of all coordinates with: number-of-candidates == gypsies
  def create_adept_list(gypsies, list = []):
    for i in range(9):
      for j in range(9):
        if len(shadow[i][j]) == gypsies:
          list += [[i, j, shadow[i][j]]]
    return list
  
  def nullboard():
    for i in range(9):
      for j in range(9):
        board[i][j] = 0; shadow[i][j] = '1234567890'
  
  # brute force method in case single full_analysis() did not finish the job
  def try_branches(thisboard):
    global trigger_finished
    if trigger_finished: return MAX
    safemode = SW_SAFEMODE[2]
    bossfight = nineXnine(0)
    for i in range(9):
      for j in range(9):
        bossfight[i][j] = thisboard[i][j]
    # saving board for later purposes
    for i in range (2, 8):
      adepts = create_adept_list(i)
      if len(adepts): break;
    adlist = []
    for coord in adepts:
      xy = [[coord[0], coord[1]]]
      for key in coord[2]:
        nullboard();
        for i in range(9):
          for j in range(9):
            board[i][j] = bossfight[i][j]
        initial_reduce();
        # loading the original board
        write(coord[0], coord[1], int(key))  # trying one future possibility for basic analysis
        xy += [[int(key), basic_analysis()]] # result of analysis as a part of new list
      adlist += [xy]                         # list of all possible future-paths
    
    for ele in adlist:
      k = 0
      while True:
        calm = True
        for x in range(1, len(ele) -1):
          if ele[x][1] > ele[x+1][1]:
            calm = False
            y = ele[x]; ele[x] = ele[x+1]; ele[x+1] = y        
        if calm: break
      for e in ele[1:]: k += e[1]
      ele += [k]
      # every coordinate have future paths sorted by result of basic_analysis()
    while True:
      calm = True
      for x in range(len(adlist[:-1])):
        if adlist[x][-1] > adlist[x+1][-1]:
          calm = False
          y = adlist[x]; adlist[x] = adlist[x+1]; adlist[x+1] = y
      if calm: break
    # coordinates in list are sorted by sum of basic_analysis() results of their elements 
    if safemode:
      print('\n')
      for a in adlist: print(a);
      if getch().lower() == 'q':
        trigger_finished = True
        return 'escape'
      
    for fpath in adlist:
      x = fpath[0][0]; y = fpath[0][1]
      if trigger_finished: return MAX
      for oneof in fpath[1:-1]:
        key = oneof[0]
        nullboard();
        for i in range(9):
          for j in range(9):
            board[i][j] = bossfight[i][j]
        initial_reduce();
        # loading the original board
        write(x, y, key)  # trying this one possibility...
        full_analysis();
        nowwhat = validity_check()
        if nowwhat == MAX:
          trigger_finished = True
          return MAX
        elif nowwhat == 1: try_branches(board)
    
    
# *************************** MAIN PROGRAM *******************************
# *************************** MAIN PROGRAM *******************************
#  SW_SAFEMODE = [1, 0, 0, 1]   # every method will show result
#  SW_SAFEMODE = [0, 1, 0, 1]   # every analysis will show result
#  SW_SAFEMODE = [0, 0, 1, 1]   # every branch of future will show partial result
#  SW_SAFEMODE = [0, 0, 0, 1]   # pause between repeated callings of function
  if 1 in SW_SAFEMODE[:-1]: print('\nYou are in safe mode! Escape by presing "Q"\n'); showboard(); getch()

  initial_reduce()
  full_analysis()
  
  if not validity_check() == MAX:
    try_branches(board)  
 
#  showboard();
  if SW_SAFEMODE[3]: getch()
  return board



# ******************* BUNCH OF SUDOKU'S for testing ***********************

#very easy
sud_0_a = '''
...2.6.3.
73...8...
..5...689
....8.29.
.634.981.
.59.1....
382...1..
...8...26
.9.5.4...X'''

sud_0_b = '''
..42....5
6.79..4.2
.318.5...
.7..5...9
.83...14.
4...6..7.
...5.493.
9.5..72.1
3....27..X'''

sud_0_c = '''
3.85.....
.4.....52
52.361...
..3.5.86.
.1.627.4.
.54.1.7..
...174.36
76.....8.
.....61.5X'''

sud_0_d = '''
26.4.....
....6.8.9
19.8....5
5.1.93.6.
.27.1.98.
.3.68.5.7
8....5.32
3.4.7....
.....6.58X'''


#easy
sud_1_a = '''
4.61..27.
...6.9.4.
7.38..16.
......617
....9....
538......
.75..64.2
.8.4.3...
.41..73.6X'''

sud_1_b = '''
.1.26....
...9.5.21
..9...57.
2...71..4
3...8...5
6..52...3
.65...8..
98.6.2...
....14.5.X'''

sud_1_c = '''
7.2.35.1.
...14..5.
15.....7.
2.59.1...
..6...9..
...3.47.5
.6.....38
.2..73...
.9.62.5.7X'''

sud_1_d = '''
54.......
239..4..5
.....5.23
..374.8.1
..2.1.5..
4.1.862..
81.6.....
9..8..362
.......58X'''


#medium
sud_2_a = '''
.7....296
..16....7
..9.2....
...1.3.2.
35..7..81
.8.5.6...
....9.3..
7....54..
436....5.X'''

sud_2_b = '''
...13...4
.24......
.7..9..16
...3.61.2
..2.7.3..
4.72.9...
39..8..6.
......89.
2...63...X'''

sud_2_c = '''
..85...94
3.5......
...81.53.
...3..648
....7....
984..2...
.93.67...
......1.6
67...59..X'''

sud_2_d = '''
..8...92.
...169.3.
.39....1.
5....7..9
...8.1...
4..3....1
.7....49.
.4.925...
.13...5..X'''


#hard
sud_a = '''
.98..2...
.....5..4
..3.7...6
....3.64.
.26...98.
.49.2....
1...6.4..
5..9.....
...7..23.X'''

sud_b = '''
..1...7.6
9.5..1...
..65.2...
57..9....
2.......9
....4..85
...3.54..
...8..5.7
1.9...2..X'''

sud_c = '''
5.1....3.
...4.9...
..68...5.
6...3...7
..9.2.8..
3...9...6
.3...12..
...9.7...
.1....4.8X'''

sud_d = '''
.3.295...
95.7.....
......45.
...4..9..
6.1...3.2
..2..1...
.28......
.....4.25
...312.7.X'''

sud_e = '''
1..2.....
.2.5.4..8
.8......1
....4.892
..2...7..
843.2....
7......5.
5..4.9.7.
.....5..6X'''

sud_f = '''
...24...7
4.5.....3
...9..2.4
.7.....2.
...391...
.3.....9.
2.7..5...
3.....4.6
9...16...X'''

sud_g = '''
...38....
..2....6.
..6...874
..763...8
9.......5
6...912..
385...7..
.7....4..
....29...X'''

sud_h = '''
.5.....46
6..7...8.
.79.1....
..437....
..1...4..
....415..
....3.69.
.3...6..5
74.....3.X'''

sud_i = '''
....19...
9.....28.
37.....4.
..73.1...
5.1...7.9
...9.21..
.3.....95
.62.....7
...68....X'''

sud_j = '''
.54.3....
.9..46...
.......18
...3.46..
7.6...1.9
..89.1...
13.......
...21..7.
....5.26.X'''

sud_hidden_pairs_a = '''
.........
9.46.7...
.768.41..
3.97.1.8.
7.8...3.1
.513.87.2
..75.261.
..54.32.8
.........X'''

sud_hidden_pairs_b = '''
72.4.8.3.
.8.....47
4.1.768.2
81.739...
...851...
...264.8.
2.968.413
34......8
168943275X'''

sud_hidden_triples = '''
.....1.3.
231.9....
.65..31..
6789243..
1.3.5...6
...1367..
..936.57.
..6.19843
3........X'''

sud_pointing_pair = '''
.179.36..
....8....
9.....5.7
.72.1.43.
...4.2.7.
.6437.25.
7.1....65
....3....
.56.1.72.X'''

sud_pointing_triple = '''
93..5....
2..63..95
856..2...
..318.57.
..5.2.98.
.8...5...
...8..159
5.821...4
...56...8X'''

sud_naked_triple = '''
.7.4.8.29
..2.....4
854.2...7
..83742..
.2.......
..32617..
....93612
2.....4.3
12.642.7.X'''

sud_naked_triple2 = '''
294513..6
6..842319
3..697254
....56...
.4..8..6.
...47....
73.164..5
9..735..1
4..928637X'''

#possibly wrong sudoku, '2' added at [0][5] for box line test being possible
sud_box_line_a = '''
.16..78.3
.9.8.....
87...1.6.
.48...3..
65...9.82
239...65.
.6.9...2.
.8...2936
9246..51.X'''

sud_box_line_b = '''
.2.943715
9.4...6..
75.....4.
5..48....
2.....453
4..352...
.42....81
..5..426.
.9.2.85.4X'''

def make_one(s):
  i = 0; j = 0
  t = nineXnine(0)
  for y in s.replace('.', '0'):
    x = ord(y)
    if x >= 48 and x <= 57:
      t[i][j] = x - 48; j += 1
      if j == 9: j = 0; i += 1
  return t
#print(make_one(sud_0_d))


problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
 [0, 0, 0, 4, 0, 6, 0, 0, 0],
 [0, 0, 5, 0, 7, 0, 3, 0, 0],
 [0, 6, 0, 0, 0, 0, 0, 4, 0],
 [4, 0, 1, 0, 6, 0, 5, 0, 8],
 [0, 9, 0, 0, 0, 0, 0, 2, 0],
 [0, 0, 7, 0, 3, 0, 2, 0, 0],
 [0, 0, 0, 7, 0, 5, 0, 0, 0],
 [1, 0, 0, 0, 4, 0, 0, 0, 7]]

solution = [[9, 2, 6, 5, 8, 3, 4, 7, 1], [7, 1, 3, 4, 2, 6, 9, 8, 5], [8, 4, 5, 9, 7, 1, 3, 6, 2], [3, 6, 2, 8, 5, 7, 1, 4, 9], [4, 7, 1, 2, 6, 9, 5, 3, 8], [5, 9, 8, 3, 1, 4, 7, 2, 6], [6, 5, 7, 1, 3, 8, 2, 9, 4], [2, 8, 4, 7, 9, 5, 6, 1, 3], [1, 3, 9, 6, 4, 2, 8, 5, 7]]



'''
print('\n\n\n\n\n\n', 30* ' ', 'START')

#for these simple reduce was enough
solve(make_one(sud_0_a))
solve(make_one(sud_0_b))
solve(make_one(sud_0_c))
solve(make_one(sud_0_d))
solve(make_one(sud_1_a))
solve(make_one(sud_1_b))
solve(make_one(sud_1_c))
solve(make_one(sud_1_d))
solve(make_one(sud_2_c))
solve(make_one(sud_2_d))

#naked pairs solved those
solve(make_one(sud_2_a))
solve(make_one(sud_2_b))
solve(make_one(sud_b))
solve(make_one(sud_e))
solve(make_one(sud_h))

#solve(make_one(sud_pointing_triple))
#solve(make_one(sud_naked_triple))
#solve(problem)


#stubborn ones
solve(make_one(sud_a))
solve(make_one(sud_c))
solve(make_one(sud_d))
solve(make_one(sud_f))
solve(make_one(sud_g))
solve(make_one(sud_i))
solve(make_one(sud_j))
solve(make_one(sud_a))
print('\n\n\n\n\n\n', 10* ' ', 'APPROX 20 SUDOKU SOLVED SO FAR ...')

getch()
print('\n\n\n\n\n\n', 30* ' ', 'LAST SUDOKU START')

solve(problem)
print('\n\n\n\n\n\n', 30* ' ', 'LAST SUDOKU FINISH')

'''
