def nineXnine(a = 0): return [[a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9, [a]*9]

# *** sum of candidates (shadows) for all slots
def count_shadows(shadow, count = 0):              
  for row in shadow:
    for string in row: count += len(string)
  return count

# *** validity test returns <0, 1, 2> for board being <not correct, not finished, finished properly>
def validity_test(board, shadow, validity):
  l = 1 if count_shadows(shadow) else 0
  if not(is_unfinished(board) + l -1): return 0 # if (non)existence of fields to fill and (non)existece of shadows are not corresponding, the board is not valid
  else: return 1 if l else validity # if there are shadows left, return 'unfinished board'. either case return result of methods.is_board_solved_properly() (0 or 2)

# *** Are we complete? check
def is_unfinished(board):
  for row in board:
    for cell in row:
      if not cell: return 1
  return 0
  
# *** prints main and/or shadow board on monitor
def showboard(board, shadow, main_board_mode, shadow_board_mode):
  # main board print
  if main_board_mode:
    for row in board:
      line = ''
      for col in row:
        if col: line += str(col)
        else: line += '.'
        line += (main_board_mode -1) * ' '
      print(line)
    print(' _____________________n= ' + str(count_shadows(shadow)))
  #shadow board print
  if shadow_board_mode:
    for row in range(9):
      line = ''
      for col in range(9):
        if len(shadow[row][col]): line += '%8s' % shadow[row][col]
        else:
          # possibility of printing what is on the board into solved fields (with shadow == '')
          if shadow_board_mode > 2: line += '    ' + str(board[row][col]) + '.  '
          else: line += 8* ' '
      print(line)
      # dividing line between rows from 1/2/3th third of board      
      if shadow_board_mode > 1 and (row == 2 or row == 5): print(60* '.')
  return True



# *** ******************** CUT'N'PASTE FROM NET ****************************
# ***                                                                    ***
# *** works as a pause after message                                     ***
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
