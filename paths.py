from . import methods # sudoku candidates reducing methods
from .matrix import Stack_of_boards # list of valid boards as a returning value of program

HIDDEN_QUADS = False # whether to include hidden quads into main analysis or not. hidden quads have extremely low chance of being efficient an it is approximatelly 2x slower than hidden triples so this switch is rated 'experimental'

class Manager():
  def __init__(self, basic_py_instance, basic_analysis_switch, full_analysis_switch):
    self.bs = basic_py_instance
    self.meth = methods.Manager(self.bs)
    self.basic_analysis_switch = basic_analysis_switch
    self.full_analysis_switch = full_analysis_switch
    
  # basic analysis is used for determining the most advantageous field (from all fields in sudoku board) to run the analysis of future from
  def basic_analysis(self, imp): # basic analysis is supposed to run many more times than full analysis (in case of self.try_branches() comes to existence), so it runs just once by default
    exp = imp.__class__(imp.board, imp.shadow)
    return self.meth.all_methods(exp, self.basic_analysis_switch)
  
  # full analysis are used once at start and then possibly couple more times to determine more closely the variants of future from specific (most advantageous) field (in sudoku board)
  def full_analysis(self, imp):
    exp = imp.__class__(imp.board, imp.shadow); start = 9**9
    while(start > exp.count_shadows()): # full analysis runs for as long as is efficient
      start = exp.count_shadows()       # save sum of shadows before analysis to compare it with sum of shadows after analysis at loop-start
      exp = self.meth.all_methods(exp, self.full_analysis_switch) # run five standart candidates-removing methods (if not overrided)
      if HIDDEN_QUADS: self.meth.hidden_elements(exp, 4)    # run sixth one if you wish so
    return exp
    
  # ********************************************************************
  #                           try_branches()                           *
  # ********************************************************************
  #
  # brute force method in case single full_analysis() did not finish the job
  def try_branches(self, imp):
    def try_branches_loop():                    # parent method assures this method is called only with nonzero 'todo_list'
      actual = todo_list.get()                  # take the last item and work with it
      where = self.choose_proper_field(actual)  # the most advantageous field to continue from  #[row, col, shadow]
      for candidate in where[2]:                # for every one number in shadow of chosen field
        path = actual.write(where[0], where[1], int(candidate)) # fill the field with this one number
        path = self.full_analysis(path); value = self.bs.validity_test(path) # make the full analysis and check how well it worked
        if value == 'properly finished board': result.add(path.__class__(path.board, path.shadow)) # valid answer means: remember that for later
        elif value == 'unfinished board': todo_list.add(path.__class__(path.board, path.shadow))   # if there is work to do left, continue working
        elif value == 'wrong board': continue   # wrong answer means do nothing aka don't continue this branch
      
    todo_list = Stack_of_boards(); result = Stack_of_boards()
    todo_list.add(imp.__class__(imp.board, imp.shadow))
    while(todo_list.length()): try_branches_loop()
    return result

  # *** choose proper field - determine the point from where to continue the analysis of future (whatever field needs to be filled with one of now-possible candidates by the end of program so one field is enough to continue)
  def choose_proper_field(self, imp):
    exp = imp.__class__(imp.board, imp.shadow)
    adepts = self.create_adept_list(exp.shadow) # list of reasonable enough sudoku board fields to mess with
    for field in adepts:                        # for every one of field in such list
      summ = 0                                  # sum of basic analysis results will be needed
      for number in field[2]: # for all (most likely 2) options of what to fill into this field  #(field[0:1] are coordinates)
        future_path = exp.write(field[0], field[1], int(number)) # try this one possibility... (write one of candidats into field)
        future_path = self.basic_analysis(future_path)           # ...for basic analysis       (and push it little further)
        summ += future_path.count_shadows()                      # and remember the result
      field += [summ]                                            # and write the result
    # choosing the most advantageous field to continue the progress...  
    best_result = 9**9; the_one = 0; index = 0
    for field in adepts:
      if field[-1] < best_result:                # if this one result is better than up-to-now best result,
        best_result = field[-1]; the_one = index # , remember the index of this one list-member (the field in sudoku board)
      index += 1
    return adepts[the_one][:-1] # ... here it is ([:result_of_basic_analysis] doesn't need to be included)
  
  # *** list of all coordinates with smallest existing shadow (except for 0's, whose are unimportant for future progress and 1's, whose shouldn't exist in this point of code (after main analysis))
  def create_adept_list(self, shadow, adepts = []):
    for doubles in range (2, 8):  # create the list of all fields with 2-letter shadow, if it fails, try 3-letter and so on
      for row in range(9):
        for col in range(9):
          if len(shadow[row][col]) == doubles:
            adepts += [[row, col, shadow[row][col]]]
      if len(adepts): break       # leave the method as soon as there is anything to return
    return adepts
  
      