import math


class Vector2:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        self._betrag = math.sqrt(self._x**2 + self._y**2)
        
    @property
    def x(self): return self._x
    
    @x.setter
    def x(self, value: float):
        self._x = value
        self.__betrag_calculation()
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: float):
        self._y = value
        self.__betrag_calculation()
        
    @property
    def betrag(self):
        return self._betrag
    
    def normalise(self):
        self._x = self._x / self.betrag
        self._y = self._y / self.betrag
        self._betrag = 1
        self.__betrag_calculation()

    def __betrag_calculation(self):
        self._betrag = math.sqrt(self._x**2 + self._y**2)
        print(self.betrag)
        
