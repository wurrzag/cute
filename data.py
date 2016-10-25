# *** creates 9x9 board (valid input for _main_file.solve()) from some of data below (below the getch() method)
def create_sudoku(inp):
  row = 0; col = 0; outp = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
  for letter in inp.replace('.', '0'):
    a = ord(letter)
    if a >= 48 and a <= 57:             # if letter is in between '0' and '9'
      outp[row][col] = a - 48; col += 1 # save int(letter) here and continue to next field
      if col == 9: col = 0; row += 1    # next line
  return outp

# *** more optimalised version of previous
def get_sudoku(whichgroup, number):
  # for these simple reduce was enough
  if whichgroup == 'easy':
    if number == 0: return create_sudoku(sud_0_a)
    if number == 1: return create_sudoku(sud_0_b)
    if number == 2: return create_sudoku(sud_0_c)
    if number == 3: return create_sudoku(sud_0_d)
    if number == 4: return create_sudoku(sud_1_a)
    if number == 5: return create_sudoku(sud_1_b)
    if number == 6: return create_sudoku(sud_1_c)
    if number == 7: return create_sudoku(sud_1_d)
    if number == 8: return create_sudoku(sud_2_c)
    if number == 9: return create_sudoku(sud_2_d)
  # naked pairs solved those
  if whichgroup == 'medium':
    if number == 0: return create_sudoku(sud_2_a)
    if number == 1: return create_sudoku(sud_2_b)
    if number == 2: return create_sudoku(sud_b)
    if number == 3: return create_sudoku(sud_e)
    if number == 4: return create_sudoku(sud_h)
  # stubborn ones
  if whichgroup == 'hard':
    if number == 0: return create_sudoku(sud_a)
    if number == 1: return create_sudoku(sud_c)
    if number == 2: return create_sudoku(sud_d)
    if number == 3: return create_sudoku(sud_f)
    if number == 4: return create_sudoku(sud_g)
    if number == 5: return create_sudoku(sud_i)
    if number == 6: return create_sudoku(sud_j)
  # methods examples - not valid sudoku
  if whichgroup == 'methods':
    if number == 0: return create_sudoku(sud_hidden_pairs_a)
    if number == 1: return create_sudoku(sud_hidden_pairs_b)
    if number == 2: return create_sudoku(sud_hidden_triples)
    if number == 3: return create_sudoku(sud_pointing_pair)
    if number == 4: return create_sudoku(sud_pointing_triple)
    if number == 5: return create_sudoku(sud_naked_triple)
    if number == 6: return create_sudoku(sud_naked_triple2)
  if whichgroup == 'crazy':
    if number == 0: return create_sudoku(sud_crazy1)
    if number == 1: return create_sudoku(sud_crazy2)
    if number == 2: return create_sudoku(sud_crazy3b)
    if number == 3: return create_sudoku(sud_crazy3)
    if number == 4: return create_sudoku(sud_crazy4)
    if number == 5: return create_sudoku(sud_crazy5)
    if number == 6: return create_sudoku(sud_crazy6)
    if number == 7: return create_sudoku(sud_crazy0)
  if whichgroup == 'problem': return problem
  if whichgroup == 'problem2': return problem2
  if whichgroup == 'solution': return solution
  if whichgroup == 'solution2': return solution2    
  return True


# ******************* BUNCH OF SUDOKU'S for testing ***********************
# ***                (official problem from codewars)                   ***
problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1], [0, 0, 0, 4, 0, 6, 0, 0, 0], [0, 0, 5, 0, 7, 0, 3, 0, 0], [0, 6, 0, 0, 0, 0, 0, 4, 0], [4, 0, 1, 0, 6, 0, 5, 0, 8], [0, 9, 0, 0, 0, 0, 0, 2, 0], [0, 0, 7, 0, 3, 0, 2, 0, 0], [0, 0, 0, 7, 0, 5, 0, 0, 0], [1, 0, 0, 0, 4, 0, 0, 0, 7]]
solution = [[9, 2, 6, 5, 8, 3, 4, 7, 1], [7, 1, 3, 4, 2, 6, 9, 8, 5], [8, 4, 5, 9, 7, 1, 3, 6, 2], [3, 6, 2, 8, 5, 7, 1, 4, 9], [4, 7, 1, 2, 6, 9, 5, 3, 8], [5, 9, 8, 3, 1, 4, 7, 2, 6], [6, 5, 7, 1, 3, 8, 2, 9, 4], [2, 8, 4, 7, 9, 5, 6, 1, 3], [1, 3, 9, 6, 4, 2, 8, 5, 7]]

problem2 = [[7, 0, 5, 6, 2, 0, 8, 0, 0], [0, 2, 0, 8, 0, 9, 0, 7, 5], [3, 0, 8, 7, 4, 5, 0, 2, 1], [5, 3, 0, 2, 0, 6, 0, 1, 0], [0, 0, 2, 0, 0, 0, 5, 0, 0], [0, 7, 0, 5, 0, 4, 0, 6, 2], [2, 5, 0, 0, 6, 7, 0, 8, 4], [0, 8, 0, 4, 5, 2, 0, 9, 0], [0, 0, 7, 0, 0, 0, 2, 5, 0]]
solution2 = [[7, 1, 5, 6, 2, 3, 8, 4, 9], [6, 2, 4, 8, 1, 9, 3, 7, 5], [3, 9, 8, 7, 4, 5, 6, 2, 1], [5, 3, 9, 2, 7, 6, 4, 1, 8], [4, 6, 2, 1, 9, 8, 5, 3, 7], [8, 7, 1, 5, 3, 4, 9, 6, 2], [2, 5, 3, 9, 6, 7, 1, 8, 4], [1, 8, 6, 4, 5, 2, 7, 9, 3], [9, 4, 7, 3, 8, 1, 2, 5, 6]]

# ***            (cut'n'paste from sudoku book-to-solve)                ***
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


# ***                 cut'n'paste from sudokuwiki.org                   ***
# *** they are good for testing (debugging) specific elimination method ***
# *** all of (or maybe nearly all of) them are not valid                ***
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


# almost unfilled sudokus
sud_crazy0 = '''
.........
.........
.........
.........
.........
.........
.........
.........
.........X'''

sud_crazy1 = '''
1........
.2.......
..3......
...4.....
....5....
.....6...
......7..
......28.
........9X'''

sud_crazy2 = '''
1........
.2.......
..3......
...4.....
....5....
.....6...
......7..
.......8.
........9X'''

sud_crazy3 = '''
12.......
..34.....
.........
.........
.........
.........
.........
.........
.........X'''

sud_crazy3b = '''
12..56...
..34..78.
.........
.........
.........
.........
.........
.........
.........X'''

sud_crazy4 = '''
.........
.........
.....3...
.........
.........
.........
..5..7...
.........
.........X'''

sud_crazy5 = '''
.........
.6.......
.........
.........
.........
.........
........9
.........
.........X'''

sud_crazy6 = '''
.........
.........
.........
.........
....5....
.........
.........
.........
.........X'''

