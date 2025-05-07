import math

class BaseObject:
    def __init__(self, type, x, y):
        self.of_type = type
        self.x = x
        self.y = y
        
    def occupies(self, *args):
        raise RuntimeError('Object has no occupies function inbuilt')

class Rectangle(BaseObject):
    def __init__(self, x, y, width, height):
        super().__init__('Rectangle', x, y)
        # X coordinate of the top-left corner
        # Y coordinate of the top-left corner
        self.width = width  # Width of the object
        self.height = height  # Height of the object
    
    def occupies(self, i, j):
        """ Check if the object occupies the given grid position (i, j) """
        return self.x <= j < self.x + self.width and self.y <= i < self.y + self.height
    
class Circle(BaseObject):
    def __init__(self, x, y, radian):
        super().__init__('Circle', x, y)
        self.radian = radian
        
    def occupies(self, i, j):
        """ Check if the object occupies the given grid position (i, j) """
        return math.sqrt((i-self.y)**2 + (j-self.x)**2) < self.radian
