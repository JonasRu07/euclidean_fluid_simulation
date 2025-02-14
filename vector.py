import math


class Vector2:
    """
        2 Dimensional Vector class. Supports basic arithmetic 
    """
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        self._length = math.sqrt(self._x**2 + self._y**2)
        
    @property
    def x(self): 
        return self._x
    
    @x.setter
    def x(self, value: float):
        self._x = value
        self.__length_calculation()
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: float):
        self._y = value
        self.__length_calculation()
        
    @property
    def length(self):
        return self._length
    
    def normalize(self):
        self._x = self._x / self.length
        self._y = self._y / self.length
        self._length = 1
        self.__length_calculation()
        
    def dot(self, vec3: 'Vector3'):
        return self.x * vec3.x + self._y * vec3.y

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x,
                           self.y + other.y)
        else:
            raise RuntimeError('Vector2 can only be added/subbed with Vector3')
        
    def __sub__(self, other):
        self.__add__(-other)
        
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3(self.x * other,
                           self.y * other)
            
    def __str__(self):
        return f'Vector2: {self.x}, {self.y}, {self.length}'

    def __length_calculation(self):
        self._length = math.sqrt(self._x**2 + self._y**2)
        
        
class Vector3:
    """
        3 Dimensional Vector class. Support for basic arithmetic
    """
    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z
        self._length = math.sqrt(self._x**2 + self._y**2 + self._z**2)
        
    @property
    def x(self): 
        return self._x
    
    @x.setter
    def x(self, value: float):
        self._x = value
        self.__length_calculation()
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: float):
        self._y = value
        self.__length_calculation()
        
    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value: float):
        self._x = value
        self.__length_calculation()
        
    @property
    def length(self):
        return self._length
    
    def dot(self, vec3: 'Vector3'):
        return self.x * vec3.x + self._y * vec3.y + self.z*vec3.z
    
    def cross(self, vec3: 'Vector3'):
        return Vector3(self.y*vec3.z - self.z*vec3.y,
                       self.z*vec3.x - self.x*vec3.z,
                       self.x*vec3.y - self.y*vec3.x)
        
    def normalize(self):
        self._x /= self._length
        self._y /= self._length
        self._z /= self._length
        self._length = 1
        
    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x,
                           self.y + other.y,
                           self.z + other.z)
        else:
            raise RuntimeError('Vector3 can only be added/subbed with Vector3')
        
    def __sub__(self, other):
        self.__add__(-other)
        
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3(self.x * other,
                           self.y * other,
                           self.z * other)
            
    def __str__(self):
        return f'Vector3: {self.x}, {self.y}, {self.z}, {self.length}'
    
    def __length_calculation(self):
        self._length = math.sqrt(self._x**2 + self._y**2 + self._z**2)
        