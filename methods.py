# *** converts string to '1-9' - string
def neg(st):
  key = '123456789'
  for s in st: key = key.replace(str(s), '')
  return key

# *** converts array of integers to string
def to_str(arr, ch = ''):
  for pirate in arr: ch += str(pirate)
  return ch

# *** is sudoku properly done due the rules?     method returns <2, 0>
# *** in case of <Success, Fail> for purposes of basic.validity_test()
def is_board_solved_properly(board):
  for key in range(1, 10):
    for i in range (9):
      if not(is_in_row(board, i, [key]) and is_in_column(board, i, [key]) and is_in_area(board, i, [key])): return 0
  return 2

# *** initial setting of shadows after loading new desk
def initial_reduce(board, shadow, normal_mode = ''):
  for row in range(9):
    for col in range(9):
      if board[row][col]:
        a = write(board, shadow, row, col, board[row][col]); board = a[0]; shadow = a[1]
  return [board, shadow] if normal_mode == 'is not' else write_singles(board, shadow)
          
# *** writes all sure-candidates (fields with only one shadow) on board
# *** except for special cases which are checked in intersection_removal())
def write_singles(board, shadow, again = True):
  while(again):
    again = False          # if there is nothing to add to desk, end this loop
    for row in range(9):
      for col in range(9):
        if len(shadow[row][col]) == 1: # only one candidate for cell means sure-candidate
          again = True     # if we are filling a cell in sudoku, there is a chance another run will reval new one
          a = write(board, shadow, row, col, int(shadow[row][col])); board = a[0]; shadow = a[1]
  return [board, shadow]        

# *** writes specific number into slot and
# *** removes number's candidates from row, column and area slot it belongs to
def write(board, shadow, row, col, what):
  board[row][col] = what; shadow[row][col] = ''
  shadow = lighten(shadow, 'column', row, col, str(what))
  shadow = lighten(shadow, 'row'   , row, col, str(what))
  shadow = lighten(shadow, 'area'  , row, col, str(what))
  return [board, shadow]

# *** removes given type of candidates (1-9) in given scale (row,column,area)
def lighten(shadow, typ, row, col, mask, exceptions = []):
  for what in mask:
    if typ == 'slot':
      if not [row, col] in exceptions: shadow[row][col] = shadow[row][col].replace(what, '')
    if typ == 'column':
      for x in range(9):
        if not [x, col] in exceptions: shadow[x][col] = shadow[x][col].replace(what, '')
    if typ == 'row':
      for y in range(9):
        if not [row, y] in exceptions: shadow[row][y] = shadow[row][y].replace(what, '')
    if typ == 'area':
      for slot in range(9):
        x = 3* (row//3) + slot//3; y = 3* (col//3) + slot%3
        if not [x, y] in exceptions: shadow[x][y] = shadow[x][y].replace(what, '')
  return shadow       
  

# *** takes list of integers
# *** returns whether ANY of them is within given scale of board
def is_in_row(board, row, what):
  for number in what:
    for slot in range(9):
      if board[row][slot] == number: return True
  return False
def is_in_column(board, col, what):
  for number in what:
    for slot in range(9):
      if board[slot][col] == number: return True
  return False
def is_in_area(board, area, what):
  for number in what:
     for slot in range(9):
       if board[3* (area //3) + slot //3][3* (area %3) + slot %3] == number: return True
  return False
  
  

# ********************************************************************
# *******************      ANALYSIS METHODS      *********************
# ********************************************************************

# ********************************************************************
# **********************************
# *** naked pairs
def naked_pairs(board, shadow):
  pairs = []
  for row in range(9):             # search the board...
    for col in range(9):
      if len(shadow[row][col]) == 2: # if given field have exactly 2 shadows, add it to list of such fields (pairs[])
        is_new = True
        for pair in pairs:
          if shadow[row][col] == pair[0]: is_new = False; pair += [[row, col]] # if this specific 2-letter shadow is already on the list, add new [coordinates] there
        if is_new: pairs += [[shadow[row][col], [row, col]]] # or else add [shadow, coordinates] to list    
    
  for pair in pairs:                            # for every len==2 shadow in board
    if len(pair) >= 3:                          # if it is there at least 2 times (2 fields in board)
      u_comb = make_unique_groups(pair[1:], 2)  # make list of unique couples amongst all coordinates with this combination
      #print (u_comb)
      for com in u_comb:
        # check every unique couple whether it shares row, column or area and act accordingly if so
        if is_same_area  (com[0], com[1]): shadow = lighten(shadow, 'area'  , com[0][0], com[0][1], pair[0], pair[1:])
        if is_same_row   (com[0], com[1]): shadow = lighten(shadow, 'row'   , com[0][0], com[0][1], pair[0], pair[1:])
        if is_same_column(com[0], com[1]): shadow = lighten(shadow, 'column', com[0][0], com[0][1], pair[0], pair[1:])
  return write_singles(board, shadow)

def is_same_row(a, b): return True if a[0] == b[0] else False
def is_same_column(a, b): return True if a[1] == b[1] else False
def is_same_area(a, b): return True if a[0]//3 == b[0]//3 and a[1]//3 == b[1]//3 else False
   

# ********************************************************************
# **********************************
# *** hidden couples, triples, quads
def hidden_elements(board, shadow, how_many):
  u_comb = make_unique_groups([1, 2, 3, 4, 5, 6, 7, 8, 9], how_many)
  for group in u_comb:     # run the test for every possible n-combination of numbers 1-9
    for where in range(9): # and for row, column and area 1-9
      
      if not is_in_row(board, where, group): # run the test only if none of the numbers are presented in given row
        match = []
        for slot in range(9):       # for every single field in given row
          for number in group:      # if any one number from combination is present
            if str(number) in shadow[where][slot]: match += [slot]; break # add that field to the list
        if len(match) == how_many:  # if there is same amount of numbers and fields into which any of them can fit
          for m in match: shadow = lighten(shadow, 'slot', where, m, neg(to_str(group))); # remove all other candidates from those fields
          #print('row', where, 'group ', group, 'match', match, 'n= ',)
 
      if not is_in_column(board, where, group):
        match = []
        for slot in range(9):
          for number in group:
            if str(number) in shadow[slot][where]: match += [slot]; break
        if len(match) == how_many:
          for m in match: shadow = lighten(shadow, 'slot', m, where, neg(to_str(group)));

      if not is_in_area(board, where, group):
        match = []
        for slot in range(9):
          a = 3* (where //3) + slot //3; b = 3* (where %3) + slot %3
          for number in group:
            if str(number) in shadow[a][b]: match += [[a, b]]; break
        if len(match) == how_many:
          for m in match: shadow = lighten(shadow, 'slot', m[0], m[1], neg(to_str(group)));
  return write_singles(board, shadow) if how_many == 1 else [board, shadow]

# *** returns True if given shadow consists from AT LEAST ONE number from 'group'
# *** and at the same time NONE of the other numbers   
def is_this_group_only(one_shadow, group, sign = False):  
  for number in group:
    if str(number) in one_shadow:
      sign = True; break
  if not sign: return False
  for absent_number in neg(to_str((group))):
    if absent_number in one_shadow: 
      return False
  return True    

# ********************************************************************
# **********************************
# *** naked triples
def naked_triples(board, shadow):
  u_comb = make_unique_groups([1, 2, 3, 4, 5, 6, 7, 8, 9], 3) # make every posible unique triple from 1-9
  for group in u_comb:     # and run the rest for each of them
    for scale in range(9): # for rows 1-9, columns 1-9 and areas 1-9
      
      # rows
      if not is_in_row(board, scale, group): # run the test only if none of the numbers are presented in given row (column,area)
        match = []
        for column in range(9):              # for (shadow of) each field in given row
          if is_this_group_only(shadow[scale][column], group): match += [[scale, column]] # if that field fits the proper condition, ad it's coords to the list
        if len(match) == 3:                  # if there are just three such equals                 
          shadow = lighten(shadow, 'row', scale, 0, to_str(group), match) # we can remove given numbers from rest of row (column, area)
          
      # columns    
      if not is_in_column(board, scale, group):
        match = []
        for row in range(9):
          if is_this_group_only(shadow[row][scale], group): match += [[row, scale]]
        if len(match) == 3:
          shadow = lighten(shadow, 'column', 0, scale, to_str(group), match)
          
      # areas    
      if not is_in_area(board, scale, group):
        match = []
        for slot in range(9):
          a = 3* (scale //3) + slot //3; b = 3* (scale %3) + slot %3
          if is_this_group_only(shadow[a][b], group): match += [[a, b]]
        if len(match) == 3:
          shadow = lighten(shadow, 'area', a, b, to_str(group), match)
  return write_singles(board, shadow)


# ********************************************************************
# **********************************
# *** pointing pairs &triples + box line reduction            
def intersection_removal(board, shadow):
  for number in range(1, 10): # for every number between 1-9
    for scale in range(9):    # check that number against 9 rows, 9 columns and 2x9 areas
      
      # row - check          
      match = []; check = [0, 0, 0] # list of proper fields and (3x 0/1 switch of) their allegiance to 1,2,3th third of given row
      for column in range(9):
        if str(number) in shadow[scale][column]: match += [[scale, column]]; check[column // 3] = 1
# *** writes sure-candidate on board (4x)
      if len(match) == 1: a = write(board, shadow, match[0][0], match[0][1], number); board = a[0]; shadow = a[1] # we can write the number directly if it have shadow in only one field of row
      elif len(match) == 2 or len(match) == 3:         # if it have candidates in 2-3 fields
        mask = 100* check[0] + 10* check[1] + check[2] # create a mask of 1/2/3th third of the row
        if mask == 1 or mask == 10 or mask == 100:     # if all fields are in the same third
          shadow = lighten(shadow, 'area', match[0][0], match[0][1], str(number), match) # remove shadow of that number from the rest of given area
          
      # column - check
      match = []; check = [0, 0, 0]
      for j in range(9):
        if str(number) in shadow[j][scale]: match += [[j, scale]]; check[j // 3] = 1
      if len(match) == 1: a = write(board, shadow, match[0][0], match[0][1], number); board = a[0]; shadow = a[1]
      elif len(match) == 2 or len(match) == 3:
        mask = 100* check[0] + 10* check[1] + check[2] # create a mask of 1/2/3th third of the column
        if mask == 1 or mask == 10 or mask == 100:
          shadow = lighten(shadow, 'area', match[0][0], match[0][1], str(number), match)
          
      # area - horizontal - check
      match = []; check = [0, 0, 0]
      for slot in range(9):
        x = 3* (scale//3) + slot//3; y = 3* (scale%3) + slot%3
        if str(number) in shadow[x][y]: match += [[x, y]]; check[slot // 3] = 1
      if len(match) == 1: a = write(board, shadow, match[0][0], match[0][1], number); board = a[0]; shadow = a[1]
      elif len(match) == 2 or len(match) == 3:
        mask = 100* check[0] + 10* check[1] + check[2] # create a mask of 1/2/3th row of the area
        if mask == 1 or mask == 10 or mask == 100:     # and clean the row if there is just one row with occurance
          shadow = lighten(shadow, 'row', match[0][0], match[0][1], str(number), match)
          
      # area - vertical - check
      match = []; check = [0, 0, 0]
      for slot in range(9):
        x = 3* (scale//3) + slot%3; y = 3* (scale%3) + slot//3
        if str(number) in shadow[x][y]: match += [[x, y]]; check[slot // 3] = 1
      if len(match) == 1: a = write(board, shadow, match[0][0], match[0][1], number); board = a[0]; shadow = a[1]
      elif len(match) == 2 or len(match) == 3:
        mask = 100* check[0] + 10* check[1] + check[2] # create a mask of 1/2/3th column of the area
        if mask == 1 or mask == 10 or mask == 100:     # and clean the column if there is just one column with occurance
          shadow = lighten(shadow, 'column', match[0][0], match[0][1], str(number), match)
  return write_singles(board, shadow)


# *** ******************** CUT'N'PASTE FROM NET ****************************
# ***                                                                    ***
# *** finds unique n-combinations (couples, triples, ...) of group       ***
def make_unique_groups(group, n):
  ucomb = []
  for uc in xuniqueCombinations(group, n): ucomb += [uc]
  return ucomb
def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc
