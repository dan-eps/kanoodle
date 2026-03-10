##
# @file         Piece.py
# @author       Daniel Epstein
# @date         August 20, 2023
# @purpose      A class that represents a kanoodle piece   

class Piece():
    ##
    # @function     init
    # @purpose      Piece constructor. Creates an instance of a Piece
    # @param        self - the Piece instance
    # @param        color - the character to display, generally is the first letter of the color
    # @param        shape - the coordinates of the spaces taken up by the piece
    # @param        rots - the number of different rotations that a piece has
    def __init__(self, id, color, shape, rots, flips):
        self.id = id
        self.color = color
        self.shape = shape 
        self.rots = rots
        self.flips = flips
    
    ##
    # @function     moveToOpen
    # @purpose      moves the piece to a given open spot 
    # @param        self - the Piece instance
    # @param        open - the open space to move the first shape spot to
    def moveToOpen(self, open):
        # Find the change from the old first spot to the open space
        deltaX = open[1] - self.shape[0][1]
        deltaY = open[0] - self.shape[0][0]

        # Apply that change to each subsequent spot in shape
        for i in range(len(self.shape)):
            self.shape[i][1] = self.shape[i][1]+deltaX
            self.shape[i][0] = self.shape[i][0]+deltaY
    
    ##
    # @function     rotate90
    # @purpose      Rotates the piece by 90 degrees to the right
    # @param        self - the Piece instance
    def rotate90(self):
        for i in range(len(self.shape)):
            temp = self.shape[i][0]
            self.shape[i][0] = self.shape[i][1]
            self.shape[i][1] = -1 * temp
    

    ##
    # @function     flip
    # @purpose      Flips any non-symmetrical piece
    # @param        self - the Piece instance
    def flip(self):
        for i in range(len(self.shape)):
            self.shape[i][1] = self.shape[i][1] * -1