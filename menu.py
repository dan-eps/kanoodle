##
# @file         Menu.py
# @author       Daniel Epstein
# @date         September 1, 2023
# @purpose      A class that represents the UI for the Kanoodle Solver

# Imports
from board import Board
from piece import Piece
import os, keyboard
import copy

# Keyboard Options for selecting a piece
pieceOptions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']

# Class that holds the return information for the pieces that the user is starting with
class Starter:
    def __init__(self, piece, index):
        self.piece = piece
        self.index = index
    
class Menu:
    def __init__(self, pieces):
        self.board = Board()
        self.pieces = pieces
        self.starters = []

    ##
    # @function     clear_screen
    # @purpose      Clears the console
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    ##
    # @function     print
    # @purpose      prints the menu
    def print(self):
        self.clear_screen()
        print(self.board)
        print("Options:")
        print("[P] - New Piece")
        print("[F] - Flip Piece")
        print("[R] - Rotate Piece")
        print("[D] - Delete Piece")
        print()
        print("[UP] - Move Piece Up")
        print("[LEFT] - Move Piece Left")
        print("[DOWN] - Move Piece Down")
        print("[RIGHT] - Move Piece Right")
        print()
        print("[Q] - Solve")
        print()

    # @function     printPieces
    # @purpose      prints the pieces menu
    # @param        pieces - the list of pieces to print
    def printPieces(self, pieces):
        c = 0
        for p in pieces:
            option = ""
            s = ""
            match p.color:
                case 'P':   
                    s="\033[0;35m"
                    option="Purple"
                case 'R':
                    s="\033[0;31m"
                    option="Red"
                case '+':
                    s="\033[0;37m"
                    option="Silver"
                case 'W':
                    s="\033[1;37m"
                    option="White"
                case 'p':
                    s="\033[1m"
                    option="Light Pink"
                case 'b':
                    s="\033[1;34m"
                    option="Light Blue"
                case 'B':
                    s="\033[0;34m"
                    option="Blue"
                case 'g':
                    s="\033[1;32m"
                    option="Light Green"
                case 'G':
                    s="\033[0;32m"
                    option="Green"
                case 'Y':
                    s="\033[1;33m"
                    option="Yellow"
                case 'O':
                    s="\033[0;31m"
                    option="Orange"
                case 'M':
                    s="\033[1;35m"
                    option="Magenta"
                case _:
                    s="\033[1;30m"
            print("[", pieceOptions[c], "] - " + s + option + "\033[0m")
            c += 1
    
    # @function     selectPiece
    # @purpose      adds a hotkey for each selectable piece
    def selectPiece(self):
        self.clear_screen()
        self.printPieces(self.pieces)
        for key in pieceOptions:
            keyboard.add_hotkey(key, lambda key=key: self.addPiece(copy.deepcopy(self.pieces[pieceOptions.index(key)]), pieceOptions.index(key)), suppress=True)
    
    # @function     addPiece
    # @purpose      Adds a selected piece to the next open spot on the board
    # @param        p - the piece to add
    # @param        i - the index of the piece in pieces
    def addPiece(self, p, i):
        s = Starter(p, i)
        self.starters = [s] + self.starters
        opens = self.board.opens.copy()
        index = 0
        rots = 0
        flips = 0
        while(True):
            self.starters[0].piece.moveToOpen(opens[index])
            if(self.board.isValidPlacement(self.starters[0].piece)):
                break
            index += 1

            if(index == len(opens)):
                if(rots != self.starters[0].piece.rots):
                    self.starters[0].piece.rotate90()
                    rots+=1
                elif(flips != self.starters[0].piece.flips):
                    rots = 0
                    self.starters[0].piece.flip()
                    flips+=1
                else:
                    break
                index = 0
                self.starters[0].piece.moveToOpen([-1, -1])
                opens = self.board.opens.copy()

        
        if(self.board.isValidPlacement(self.starters[0].piece)):
            self.board.placePiece(self.starters[0].piece)
            for c in self.starters[0].piece.shape:
                self.board.opens.remove(c)
        else:
            self.starters.pop(0)
            self.board.opens.sort()
        
        for key in pieceOptions:
            keyboard.remove_hotkey(key)

        self.clear_screen()
        self.print()

    # @function     removeLastPiece
    # @purpose      removes the last piece added to the board
    def removeLastPiece(self):
        if(len(self.starters) <= 0): return
        lp = self.starters[0].piece
        self.board.removePiece(lp)
        for c in lp.shape:
            self.board.opens.append(c)
        self.board.opens.sort()
        self.starters.pop(0)
        self.print()

    # @function     moveLeft
    # @purpose      moves the last piece added to the board left
    def moveLeft(self):
        if(len(self.starters) <= 0): return
        p = self.starters[0].piece
        self.board.removePiece(p)
        for c in p.shape:
            if(c not in self.board.opens): self.board.opens.append(c)
        self.board.opens.sort()
        opts = self.board.opens.copy()
        nmi = opts.index(p.shape[0])
        while(True):
            x = copy.deepcopy(p)
            nmi -= 1
            if(nmi < 0): nmi = len(opts) - 1
            x.moveToOpen(opts[nmi])
            if(self.board.isValidPlacement(x)):
                p.shape = x.shape.copy()
                p.moveToOpen(opts[nmi])
                self.board.placePiece(p)
                for c in p.shape:
                    self.board.opens.remove(c)
                break
        self.print()

    # @function     moveRight
    # @purpose      moves the last piece added to the board right
    def moveRight(self):
        if(len(self.starters) <= 0): return
        p = self.starters[0].piece
        self.board.removePiece(p)
        for c in p.shape:
            if(c not in self.board.opens): self.board.opens.append(c)
        self.board.opens.sort()
        opts = self.board.opens.copy()
        nmi = opts.index(p.shape[0])
        while(True):
            x = copy.deepcopy(p)
            nmi += 1
            if(nmi >= len(opts)): nmi = 0
            x.moveToOpen(opts[nmi])
            if(self.board.isValidPlacement(x)):
                p.shape = x.shape.copy()
                p.moveToOpen(opts[nmi])
                self.board.placePiece(p)
                for c in p.shape:
                    self.board.opens.remove(c)
                break
        self.print()

    # @function     moveDown
    # @purpose      moves the last piece added to the board down 
    def moveDown(self):
        if(len(self.starters) <= 0): return
        p = self.starters[0].piece
        self.board.removePiece(p)
        for c in p.shape:
            if(c not in self.board.opens): self.board.opens.append(c)
        self.board.opens.sort()
        x = copy.deepcopy(p)
        while(True):
            nm = [0, x.shape[0][1]] if (x.shape[0][0] + 1 )> 4  else [x.shape[0][0] + 1, x.shape[0][1]]
            x.moveToOpen(nm)
            if(nm == p.shape[0]):
                break
            if(self.board.isValidPlacement(x)):
                p.shape = x.shape.copy()
                p.moveToOpen(nm)
                self.board.placePiece(p)
                for c in p.shape:
                    self.board.opens.remove(c)
                break
        self.print()

    # @function     moveUp
    # @purpose      moves the last piece added to the board left
    def moveUp(self):
        if(len(self.starters) <= 0): return
        p = self.starters[0].piece
        self.board.removePiece(p)
        for c in p.shape:
            if(c not in self.board.opens): self.board.opens.append(c)
        self.board.opens.sort()
        x = copy.deepcopy(p)
        while(True):
            nm = [4, x.shape[0][1]] if (x.shape[0][0] - 1 ) < 0  else [x.shape[0][0] - 1, x.shape[0][1]]
            x.moveToOpen(nm)
            if(nm == p.shape[0]):
                break
            if(self.board.isValidPlacement(x)):
                p.shape = x.shape.copy()
                p.moveToOpen(nm)
                self.board.placePiece(p)
                for c in p.shape:
                    self.board.opens.remove(c)
                break
        self.print()

    # @function     rotateLast
    # @purpose      rotates the last piece added to the board 90 degrees
    def rotateLast(self):
        if(len(self.starters) <= 0): return
        p = self.starters[0].piece
        self.board.removePiece(p)
        for c in p.shape:
            if(c not in self.board.opens): self.board.opens.append(c)
        self.board.opens.sort()
        opts = self.board.opens.copy()
        nmi = 0
        x = copy.deepcopy(p)
        x.rotate90()
        while(True):
            x.moveToOpen(opts[nmi])
            if(self.board.isValidPlacement(x)):
                p.shape = x.shape.copy()
                p.moveToOpen(opts[nmi])
                self.board.placePiece(p)
                for c in p.shape:
                    self.board.opens.remove(c)
                break
            nmi += 1
        self.print()
    
    # @function     flipLast
    # @purpose      flips the last piece added to the board
    def flipLast(self):
        if(len(self.starters) <= 0): return
        p = self.starters[0].piece
        self.board.removePiece(p)
        for c in p.shape:
            if(c not in self.board.opens): self.board.opens.append(c)
        self.board.opens.sort()
        opts = self.board.opens.copy()
        nmi = 0
        x = copy.deepcopy(p)
        x.flip()
        while(True):
            x.moveToOpen(opts[nmi])
            if(self.board.isValidPlacement(x)):
                p.shape = x.shape.copy()
                p.moveToOpen(opts[nmi])
                self.board.placePiece(p)
                for c in p.shape:
                    self.board.opens.remove(c)
                break
            nmi += 1
        self.print()

    # @function     startListeners
    # @purpose      Adds hotkeys for all of the menu options
    def startListeners(self):
        keyboard.add_hotkey('d', self.removeLastPiece, suppress=True)
        keyboard.add_hotkey('p', self.selectPiece, suppress=True)
        keyboard.add_hotkey('r', self.rotateLast, suppress=True)
        keyboard.add_hotkey('f', self.flipLast, suppress=True)
        keyboard.add_hotkey('left', self.moveLeft, suppress=True)
        keyboard.add_hotkey('right', self.moveRight, suppress=True)
        keyboard.add_hotkey('down', self.moveDown, suppress=True)
        keyboard.add_hotkey('up', self.moveUp, suppress=True)

    # @function     run
    # @purpose      Runs the menu until the user hits "q" to solve
    # @return       the pieces to start the solver with
    def run(self):
        self.startListeners()
        self.print()
        keyboard.wait('q', suppress=True)
        return self.starters


