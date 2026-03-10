##
# @file         Exact_cover_converter.py
# @author       Daniel Epstein
# @date         March 10, 2026
# @purpose      A class that converts Kanoodle into an exact cover problem

from board import Board
from piece import Piece
import numpy as np
import exact_cover as ec
from collections import OrderedDict


## 
# In order to try out exact-cover, a library that uses Knuth's Algorithm X and Dancing Links,
# We need to convert each placement into a row of 1s and 0s. Each row will have 67 columns,
# to represent the 55 spaces on the board and the 12 piece types.

class ExactCoverConverter:

    __slots__ = ["pieces", "all_placements"]

    def __init__(self, pieces: list[Piece]):
        self.pieces = OrderedDict({piece.id: piece for piece in pieces})
        self.all_placements = self.load_all_valid_placements()

    ##
    # @function     load_all_valid_placements
    # @purpose      Loads the valid placement file or creates it if it does not exist
    def load_all_valid_placements(self):
        try:
            all_placements = np.genfromtxt('all_placements.csv', delimiter=',')
        except FileNotFoundError:
            print("File Not Found! Generating new file...")
            with open("all_placements.csv", 'w+') as config_file:
                all_placements = []
                for piece in self.pieces:
                    piece_rows = self.get_all_valid_placements_per_piece(piece)
                    all_placements += piece_rows
                    config_file.writelines("\n".join([",".join(row) for row in piece_rows]))
            all_placements = np.array(all_placements)
        finally:
            return all_placements
        
    ##
    # @function     get_exact_cover
    # @purpose      Turns a piece's current config into an exact-cover row
    def get_exact_cover(self, pieces_to_remove=[]) -> np.ndarray:
        for piece in pieces_to_remove:
            different_piece = self.all_placements[:, 55 + piece.id] != 1
            starting_orientation = np.all(self.all_placements == np.array(self.turn_placement_into_row(piece), dtype=int), axis=1)
            
            self.all_placements = self.all_placements[different_piece | starting_orientation]

        return ec.get_all_solutions(self.all_placements)
        
    ##
    # @function     turn_placement_into_row
    # @purpose      Turns a piece's current config into an exact-cover row
    # @param        piece - the piece whose placement needs to be turned into a row
    def turn_placement_into_row(self, piece: Piece) -> list[str]:
        config_row = ['0'] * 55
        for (row, col) in piece.shape:
            config_row[row * 11 + col] = '1'
        config_row += ['1' if i == piece.id else '0' for i in range(12)]
        return config_row

    ##
    # @function     get_all_valid_placements_per_piece
    # @purpose      Gets all the possible valid placements for the piece
    def get_all_valid_placements_per_piece(self, piece: Piece) -> list[list]:
        board = Board()
        config_rows = []

        for j in range(piece.flips):
            for i in range(piece.rots):
                for loc in board.opens:

                    # Move to open and check placement
                    piece.moveToOpen(loc)
                    if(board.isValidPlacement(piece)):
                        config_rows += self.turn_placement_into_row(piece)


                # Rotate the piece to try that config
                piece.rotate90()

            # Flip the piece to try that config
            piece.flip()
        
        return config_rows

    ##
    # @function     turn_solution_into_board
    # @purpose      turns exact-cover solutions back to kanoodle boards
    # @param        solution - a list of row indicies that form a solution
    def turn_solution_into_board(self, solution) -> Board:
        board = Board()
        for row_index in solution:
            solution_row = self.all_placements[row_index]
            piece = self.pieces[list(solution_row[-12:]).index(1)]
            for idx in range(55):
                r = idx // 11
                c = idx % 11
                if(solution_row[idx] == 1):
                    board.board[r][c] = piece.color
        return board