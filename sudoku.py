from sudoku import basic
from sudoku import methods
from sudoku import data
#from copy import deepcopy


# ********************************************************************
#                      basic & full analysis                         *
# ********************************************************************

# ********************************************************************
# **********************************
# *** basic analysis
def basic_analysis(board, shadow):
  global SW_DEPTH; shadows_start = 1; shadows_finish = 0
  while shadows_start > shadows_finish: # run the test for as long as it is >0 efficient
    shadows_start = basic.count_shadows(shadow)
    a = main_loop(board, shadow, SW_DEPTH); board = a[0]; shadow = a[1]
    shadows_finish = basic.count_shadows(shadow)
  return [board, shadow, shadows_finish]

# ********************************************************************
# **********************************
# *** full analysis
def full_analysis(board, shadow):
  global SW_SAFEMODE; global SW_SAFEMODE_BOARD; global SW_SAFEMODE_SHADOW; global SW_HIDDEN_QUADS
  switch = 1; cs_start = basic.count_shadows(shadow); 
  while(switch):
    before = 1; after = 0      
    while before > after: # run the test for as long as it is >0 efficient
      before = basic.count_shadows(shadow)
      a = main_loop(board, shadow, '11111'); board = a[0]; shadow = a[1];
      after = basic.count_shadows(shadow)
      if a[2] == 'escape': return [board, shadow, 'escape']

      # run hidden quads method if switch says so
      if SW_HIDDEN_QUADS:
        hid_quad_start = basic.count_shadows(); hid_quad_start = 1; hid_quad_finish = 0
        while hid_quad_start > hid_quad_finish:
          hid_quad_start = basic.count_shadows(shadow); a = methods.hidden_elements(board, shadow, 4); board = a[0]; shadow = a[1]; hid_quad_finish = basic.count_shadows(shadow)
        switch = hid_quad_start - hid_quad_finish   # repeat ALL methods (naked pairs, ...) if hidden quads finds and removes whatever on the board and then hidden quads again
      else: switch = 0
      
  # second bit of safemode mask will make board print and pause here if set
  if SW_SAFEMODE[1]:
    print("full_analysis:", cs_start - basic.count_shadows(shadow));
    basic.showboard(board, shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW);
    if basic.getch().lower() == 'q': return [board, shadow, 'escape']
  return [board, shadow, 'breach']

# ********************************************************************
# **********************************
# *** main loop
def main_loop(board, shadow, mask):
  global SW_SAFEMODE; global SW_SAFEMODE_BOARD; global SW_SAFEMODE_SHADOW
  # first bit of safemode mask is making pauses after every method if set
  safe_mode = SW_SAFEMODE[0]
  
  # naked pairs  
  if mask[0] == '1':
    size_very_start = basic.count_shadows(shadow); size_start = 1; size_finish = 0
    while(size_start > size_finish):
      size_start = basic.count_shadows(shadow); a = methods.naked_pairs(board, shadow); board = a[0]; shadow = a[1]; size_finish = basic.count_shadows(shadow);
    if safe_mode: 
      print("naked pairs:", size_very_start - size_finish); basic.showboard(board, shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW)
      if basic.getch().lower() == 'q': return [board, shadow, 'escape']
    
  # intersection removal aka pointing pairs &triples + box line reduction
  if mask[1] == '1':
    size_very_start = basic.count_shadows(shadow); size_start = 1; size_finish = 0
    while(size_start > size_finish):
      size_start = basic.count_shadows(shadow); a = methods.intersection_removal(board, shadow); board = a[0]; shadow = a[1]; size_finish = basic.count_shadows(shadow)
    if safe_mode:
      print("intersection removal:", size_very_start - size_finish); basic.showboard(board, shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW)
      if basic.getch().lower() == 'q': return [board, shadow, 'escape']
  # naked triples
  if mask[2] == '1':
    size_very_start = basic.count_shadows(shadow); size_start = 1; size_finish = 0
    while(size_start > size_finish):
      size_start = basic.count_shadows(shadow); a = methods.naked_triples(board, shadow); board = a[0]; shadow = a[1]; size_finish = basic.count_shadows(shadow)
    if safe_mode:
      print("naked triples:", size_very_start - size_finish); basic.showboard(board, shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW)
      if basic.getch().lower() == 'q': return [board, shadow, 'escape']
    
  # hidden doubles
  if mask[3] == '1':
    size_very_start = basic.count_shadows(shadow); size_start = 1; size_finish = 0
    while(size_start > size_finish):
      size_start = basic.count_shadows(shadow); a = methods.hidden_elements(board, shadow, 2); board = a[0]; shadow = a[1]; size_finish = basic.count_shadows(shadow)
    if safe_mode:
      print("hidden doubles:", size_very_start - size_finish); basic.showboard(board, shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW)
      if basic.getch().lower() == 'q': return [board, shadow, 'escape']
    
  # hidden triples
  if mask[4] == '1':
    size_very_start = basic.count_shadows(shadow); size_start = 1; size_finish = 0
    while(size_start > size_finish):
      size_start = basic.count_shadows(shadow); a = methods.hidden_elements(board, shadow, 3); board = a[0]; shadow = a[1]; size_finish = basic.count_shadows(shadow)
    if safe_mode:
      print("hidden triples:", size_very_start - size_finish); basic.showboard(board, shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW)
      if basic.getch().lower() == 'q': return [board, shadow, 'escape']
      
  return [board, shadow, 'breach']


# ********************************************************************
#                   sub methods of try_branches()                    *
# ********************************************************************

# *** list of all coordinates with: number-of-candidates == gypsies
def create_adept_list(shadow, gypsies, list = []):
  for row in range(9):
    for col in range(9):
      if len(shadow[row][col]) == gypsies:
        list += [[row, col, shadow[row][col]]]
  return list
  
# *** setting board fields to 0 and shadow to '123456789'
# *** in case of loading new board
def nullboard(board, shadow):
  for row in range(9):
    for col in range(9):
      board[row][col] = 0; shadow[row][col] = methods.neg('')
  return [board, shadow]

# *** solve() will read the answer from here if this function will run once
def write_the_answer(whatboard):
  global resulting_board; global resulting_shadow
  for move in range(81):
    x = move //9; y = move %9
    resulting_board[x][y] = whatboard[x][y]
  return True

# ********************************************************************
# **********************************
# *** future paths
def future_paths(bossfight, board, shadow):
  global SW_SAFEMODE
  # create list of future paths, for every field with short (usually 2) shadow
  for step in range(81): x = step//9; y = step%9; bossfight[x][y] = board[x][y]
  for doubles in range (2, 8):  # create list of all fields with 2-letter shadow, if it fails, try 3-letters and so on
    adepts = create_adept_list(shadow, doubles);
    if len(adepts): break;
  if SW_SAFEMODE[2]: # printing the list in case switch is set
    for ff in adepts: print(ff)
    
  adlist = []
  for field in adepts: # for every one of coordinations in list
    coordinate = [[field[0], field[1]]]
    for number in field[2]: # for (usualy 2) options of what to fill here
      a = nullboard(board, shadow); board = a[0]; shadow = a[1]
      for i in range(81): x = i//9; y = i%9; board[x][y] = bossfight[x][y]   # loading original board
      a = methods.initial_reduce(board, shadow); board = a[0]; shadow = a[1] # creating proper shadow mask there
      a = methods.write(board, shadow, field[0], field[1], int(number)); board = a[0]; shadow = a[1]  # trying one future possibility for basic analysis
      coordinate += [[int(number), basic_analysis(board, shadow)[2]]] # result of analysis as a part of new list
    adlist += [coordinate]                         # list of all possible future-paths
    
  return adlist
 
# ********************************************************************
# **********************************
# *** bubble sort
def sort_list(adlist):
  # sorting future paths by best results given by basic_analysis()
  # [[col, row], [candidate_to_write, his_analysis_result], [other_candidate, his_analysis_result]]
  for fpath in adlist: # for every single path
    while True: # for as long as there will be changes into list after one sort
      calm = True
      for bub in range(1, len(fpath) -1): # first goes coordinate, sort the rest
        if fpath[bub][1] > fpath[bub+1][1]: # if analysis less succesful than next bubble's one
          calm = False                  # switch the bubbles
          ab = fpath[bub]; fpath[bub] = fpath[bub+1]; fpath[bub+1] = ab
      if calm: break
    # every coordinate have candidates sorted by result of basic_analysis()
    mixed_analysis_result = 0
    for option in fpath[1:]: mixed_analysis_result += option[1]
    fpath += [mixed_analysis_result]
    # sum of basic_analysis() results added to the end of line
      
  while True: # for as long as there will be changes into list after one sort
    calm = True
    for bub in range(len(adlist[:-1])): # for all single paths in list
      if adlist[bub][-1] > adlist[bub+1][-1]: # if their result is higher (means worse)
        calm = False
        ab= adlist[bub]; adlist[bub] = adlist[bub+1]; adlist[bub+1] = ab # move it to back
    if calm: break
  # path list is sorted by sum of basic_analysis() results of its elements
  return adlist


# ********************************************************************
#                           try_branches()                           *
# ********************************************************************
#
# brute force method in case single full_analysis() did not finish the job
def try_branches(board, shadow):
  global SW_SAFEMODE; global SW_SAFEMODE_BOARD; global SW_SAFEMODE_SHADOW
  global trigger_finished
  
  # if (answer didn't been written yet and) board is solved properly,
  # save it into global.resulting_board and stop the function
  val = basic.validity_test(board, shadow, methods.is_board_solved_properly(board))
  if trigger_finished == False and val == 2: write_the_answer(board); trigger_finished = True
  elif val == 0: return False # if board is wrong, stop the function
  if trigger_finished: return True
  # next lines continues only if val == 1 (not 0 or 2) ie board is unfinished

  bossfight = basic.nineXnine(0) # save position for future use

  # list of future paths, sorted by best mixed result of all (usually 2) alternatives
  path_list = sort_list(future_paths(bossfight, board, shadow))

  # if third bit in safemode mask is set, print adept list
  if SW_SAFEMODE[2]:
    print('new ones:')
    for ad in path_list: print(ad)
    if basic.getch().lower() == 'q':
      trigger_finished = True
      return [board, shadow]
      
  # if thou cometh this far, explore the future now
  for fpath in path_list: # for every single future path
    row = fpath[0][0]; col = fpath[0][1]
    if trigger_finished: return True
    for oneof in fpath[1:-1]: # for every (usualy 2) possibility there:
      if trigger_finished: return True
      number = oneof[0]
      a = nullboard(board, shadow); board = a[0]; shadow = a[1]
      for step in range(81): x = step//9; y = step%9; board[x][y] = bossfight[x][y] # loading an original board
      a = methods.initial_reduce(board, shadow); board = a[0]; shadow = a[1] # setting proper initial shadows
      a = methods.write(board, shadow, row, col, number); board = a[0]; shadow = a[1] # trying this one possibility...
      a = full_analysis(board, shadow); board = a[0]; shadow = a[1]  # full_analysis() of this one possibility
      try_branches(board, shadow) # method have the ability to switch trigger_finished as a first thing
  return True
        

# ********************************************************************
#                           MAIN PROGRAM                             *
# ********************************************************************
        
SW_SAFEMODE = [0, 0, 0, 0]      # pause and showboard() each step; levels: 
                                # [detailed, after main loop, brute force information, result only]

SW_SAFEMODE_BOARD = 2           # showboard() includes main board
                                # >1 value for horizontal spaces between slots

SW_SAFEMODE_SHADOW = 2          # showboard() includes candidate-list board
                                # >2 for mixed board (main + shadow in one)  


# five characters for five algorithms which may or may not
# be included in basic analysis (default is '11000')
# basic analysis is used only for sorting future-paths by best result
# full analysis, applied on (sorted) list of future-paths 
# is allways using all five methods (SW_DEPTH='11111')

SW_DEPTH = '11000'              
#       [ naked_pairs(), intersection_removal(), naked_triples(),
#         hidden_elements(2), hidden_elements(3) ]

SW_HIDDEN_QUADS = False         # optional: include hidden quads into reducing methods

# try_branches() save the result here if full_analysis() will not be enough to solve the problem                             
resulting_board  = basic.nineXnine(0)
resulting_shadow = basic.nineXnine(methods.neg(''))


# ********************************************************************
#                           main function                            *
# ********************************************************************

trigger_finished = False # triggers to True once analysis finds a valid solution
def solve(board):
  global trigger_finished
  global resulting_board; global resulting_shadow
  global SW_SAFEMODE; global SW_SAFEMODE_BOARD; global SW_SAFEMODE_SHADOW
  
                                              # program-essential variable
  shadow = basic.nineXnine(methods.neg(''))   # list of candidates for each slot
  
  #SW_SAFEMODE = [1, 0, 0, 1]   # every method will show result
  #SW_SAFEMODE = [0, 1, 0, 1]   # every analysis will show result
  #SW_SAFEMODE = [0, 0, 1, 1]   # every branch of future will show partial result
  #SW_SAFEMODE = [0, 0, 0, 1]   # pause between repeated callings of function    

  # initial print and simple reduce of board
  a = methods.initial_reduce(board, shadow, 'is not'); board = a[0]; shadow = a[1] # initial setting of shadows
  print('start:'); basic.showboard(board, shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW) # printing the sudoku
  a = methods.write_singles(board, shadow); board = a[0]; shadow = a[1] # initial simple reduce method, normally included in initial_reduce()

  # if user will have possibility of ending program with 'Q' key, program will tell that to him
  if 1 in SW_SAFEMODE[:-2]:
    print('\nYou are in safe mode! Escape anytime by presing "Q"\n')
    if basic.getch().lower() == 'q': return False
  
  # solving sequence
  a = full_analysis(board, shadow); board = a[0]; shadow = a[1] # first run of all reducing methods
  if a[2] == 'escape': return False # 'Q' was pressed during main analysis, end the program
  val = basic.validity_test(board, shadow, methods.is_board_solved_properly(board)) # testing the board
  if val == 1: try_branches(board, shadow) # if board is unfinished, examine its future paths
  
  # printing the board and ensuring the result is in proper variable
  if not trigger_finished: # if future was succesfully seen, the result is already in global variable.
    for step in range(81): x = step//9; y = step%9; resulting_board[x][y] = board[x][y] # otherwise copy it there
  resulting_shadow = methods.initial_reduce(resulting_board, resulting_shadow)[1] # reducing resulting shadow to (supposable) 0
  finishing_showboard(resulting_board, resulting_shadow, SW_SAFEMODE_BOARD, SW_SAFEMODE_SHADOW) # showing the result

  # last bit in safemode mask triggers this pause
  if SW_SAFEMODE[3]: basic.getch()
  
  return resulting_board

# ********************************************************************
#                        end of main function                        *
# ********************************************************************

  
# *** even if safemode is [0, 0, 0, 0], program will print the result
def finishing_showboard(board, shadow, mode1, mode2):
  vtest = basic.validity_test(board, shadow, methods.is_board_solved_properly(board))
  if   vtest == 0: print('Incorrect board')
  elif vtest == 1: print('Unfinished board')
  elif vtest == 2: print('Passed')
  basic.showboard(board, shadow, mode1, mode2)
  print('end of the program')
  return True


# *** testing all valid sudokus from data.py
def the_test():
  # safemode mask in solve() needs to be untouched ([0, 0, 0, 0]) for speed test to make any sense
  print(30* '\n', 30* ' ', 'START...')
  basic.getch()

  for i in range(10): solve(data.get_sudoku('easy', i))
  for i in range( 5): solve(data.get_sudoku('medium', i))
  for i in range( 7): solve(data.get_sudoku('hard', i))
  
  print('\n\n\n\n\n\n', 10* ' ', 'APPROX 20 SUDOKU SOLVED SO FAR ...')
  print('\n\n\n', 30* ' ', 'MAIN SUDOKU START...')
  basic.getch()
  
  solve(data.problem)
  print('\n\n\n\n\n\n', 20* ' ', 'MAIN SUDOKU FINISH')
  print('\n\n\n\n\n\n', 20* ' ', 'OTHER TEST SUDOKU START...')
  basic.getch()
  
  solve(data.problem2)
  print('\n\n\n\n\n\n', 20* ' ', 'OTHER TEST SUDOKU FINISH')
  return True


#solve(data.problem)
the_test();