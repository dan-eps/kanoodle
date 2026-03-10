##
# @mainpage     Kanoodle Solver
# @author       Daniel Epstein
# @date         August 20, 2023
# @purpose      The game Kanoodle consists of placing colored pieces 
#               on a rectangular board. This takes the starting position
#               and finds all viable solutions (if one exists).               

# Imports
from board import Board
from piece import Piece
from menu import Menu
from exact_cover_converter import ExactCoverConverter

##
# @function     startPiece
# @purpose      Starts a piece on the board
# @param        board - the board to put the pieces on
# @param        p - the piece to start
# @param        coords - the starting coordinate of the piece p
def startPiece(board: Board, p: Piece, coords: list[list[int, int]]) -> None:

    # Move to starting position
    p.shape = coords.copy()
    board.placePiece(p)

    # Remove the pieces spaces from the open list
    for c in p.shape:
        board.opens.remove(c)
    

##
# @function     tryPlace
# @purpose      Recursively places all the pieces on the board in every avaliable viable position
# @param        pieces - the list of pieces that still need to be added
# @param        opens - the list of open spots remaining on the board
def tryPlace(pieces: list[Piece], opens: list[list]):

    # Next piece to place is the first piece in pieces
    p = pieces[0]

    # For each orientation
    for j in range(p.flips):
        for i in range(p.rots):

            # Copy the opens to a local copy for the current piece
            pc = opens.copy()
            for c in pc:

                # For each open spot, 
                # 1 - move to the open spot,
                # 2 - if that is a valid placement, place the piece, then tryPlace next piece
                # 3 - remove the piece and try next spot

                # Move to open and check placement
                p.moveToOpen(c)
                if(board.isValidPlacement(p)):
                    board.placePiece(p)
                    #If there are more pieces to place, place the next piece
                    if(len(pieces) > 1):
                        # Copy the open spaces minus the spaces being taken up by the current piece
                        temp = opens.copy()
                        for t in p.shape:
                            temp.remove(t)
                        # Place the next piece
                        tryPlace(pieces[1:], temp)
                    else:
                        # Placed the last piece! Print the board
                        print(board)

                    # There aren't anymore solutions with this current placement, remove piece and try next                
                    board.removePiece(p)

            # Rotate the piece to try that solution
            p.rotate90()
        # Flip the piece to try that solution
        p.flip()

##
# @function     Main
if __name__ == "__main__":

    # Initialize each piece, starting at [-1, -1]
    # Pieces must start off the board, so that they can be moved to any position on the board 
    PURPLE = Piece(id=0, color='P', shape=[[-1, -1], [0, -1], [1, -1], [2, -1]], rots=2, flips=1)
    RED = Piece(id=1, color='R', shape=[[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0]], rots=4, flips=2)
    LIGHTPINK = Piece(id=2, color='p', shape=[[-1, -1], [-1, 0], [-1, 1], [0, 1], [-1, 2]], rots=4, flips=2)
    WHITE = Piece(id=3, color='W', shape=[[-1, -1], [-1, 0], [0, -1]], rots=4, flips=1)
    LIGHTGREEN = Piece(id=4, color='g', shape=[[-1, -1], [0, -1], [-1, 0], [0, 0]], rots=1, flips=1)
    LIGHTBLUE = Piece(id=5, color='b', shape=[[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1]], rots=4, flips=1)
    BLUE = Piece(id=6, color='B', shape=[[-1, -1], [0, -1], [0, 0], [0, 1], [0, 2]], rots=4, flips=2)
    SILVER = Piece(id=7, color='+', shape=[[-1, -1], [-2, -1], [-1, -2], [-1, 0], [0, -1]], rots=1, flips=1)
    YELLOW = Piece(id=8, color='Y', shape=[[-1, -1], [0, -1], [1, -1], [1, 0], [-1, 0]], rots=4, flips=1)
    GREEN = Piece(id=9, color='G', shape=[[-1, -1], [-1, 0], [-1, 1], [0, 1], [0, 2]], rots=4, flips=2)
    PINK = Piece(id=10, color='M', shape=[[-1, -1], [0, -1], [0, 0], [1, 0], [1, 1]], rots=4, flips=1)
    ORANGE = Piece(id=11, color='O', shape=[[-1, -1], [0, -1], [0, 0], [0, 1]], rots=4, flips=2)

    # The game board
    board = Board() 

    # Pieces arranged in order of size to place the larger pieces first
    pieces = [SILVER, YELLOW, PINK, GREEN, LIGHTPINK, LIGHTBLUE, RED, BLUE, LIGHTGREEN, ORANGE, PURPLE, WHITE]
    # silver, yellow, pink, green, lightpink, lightblue, red, blue, lightgreen, orange, purple, white

    # Start the Menu
    menu = Menu(pieces)
    starters = menu.run()
    menu.clear_screen()

    # Start all the pieces returned and then remove them from the pieces list
    fixed_pieces = []
    for s in starters:
         startPiece(board, pieces[s.index], s.piece.shape)
         fixed_pieces += [pieces[s.index]]

    # Convert problem to exact-cover and solve!
    converter = ExactCoverConverter(pieces)
    solutions = converter.get_exact_cover(pieces_to_remove=fixed_pieces)
    for solution in solutions:
        print(converter.turn_solution_into_board(solution))