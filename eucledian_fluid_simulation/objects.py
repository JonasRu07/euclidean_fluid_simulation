import math

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x  # X coordinate of the top-left corner
        self.y = y  # Y coordinate of the top-left corner
        self.width = width  # Width of the object
        self.height = height  # Height of the object
    
    def occupies(self, i, j):
        """ Check if the object occupies the given grid position (i, j) """
        return self.x <= j < self.x + self.width and self.y <= i < self.y + self.height
    
class Circle:
    def __init__(self, x, y, radian):
        self.x = x
        self.y = y
        self.radian = radian
        
    def occupies(self, i, j):
        return math.sqrt((i-self.y)**2 + (j-self.x)**2) < self.radian
