from dataclasses import dataclass
from typing import Optional, Union, Tuple, Iterator

from math import sqrt
from copy import deepcopy

from .vector import Vector3
from .matrix import Matrix3x3

@dataclass
class Point:
    __slots__ = ('x', 'y', 'z') # disable dynamic attribute

    x: float
    y: float
    z: float

    def components(self) -> Tuple[Union[int,float], Union[int,float], Union[int,float]]:
        """
        Returns the components of the point as a tuple (x, y, z)

        Example:
        >>> p = Point(1, 2, 3)
        >>> p.components()
        (1, 2, 3)
        """
        return self.x, self.y, self.z

    def as_vector(self) -> Vector3:
        return Vector3(self.x, self.y, self.z)

    def distance(self, other: 'Point') -> float:
        """
        Calculates the Euclidean distance between two points

        Parameters:
        - `other` (Point): The other point

        Example:
        >>> p1 = Point(1, 2, 3)
        >>> p2 = Point(4, 5, 6)
        >>> p1.distance(p2)
        5.656854249
        """
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2 + (other.z - self.z)**2)

    def square_distance(self, other: 'Point') -> float:
        """
        Calculates the squared Euclidean distance between two points

        Parameters:
        - `other` (Point): The other point

        Example:
        >>> p1 = Point(1, 2, 3)
        >>> p2 = Point(4, 5, 6)
        >>> p1.square_distance(p2)
        32
        """
        return (other.x - self.x)**2 + (other.y - self.y)**2 + (other.z - self.z)**2
    
    def move_by(self, x: float, y:float, z:float) -> 'Point':
        """
        Moves the point by the specified offsets

        Parameters:
        - `x` (float): Offset in the X direction
        - `y` (float): Offset in the Y direction
        - `z` (float): Offset in the Z direction

        Example:
        >>> p = Point(1, 2, 3)
        >>> p.move_by(10, 10, 10)
        >>> p
        Point(11, 12, 13)
        """
        self.x += x
        self.y += y
        self.z += z
        return self

    def is_zero(self, threshold: float = 1e-6) -> bool:
        """
        Checks if the point is close to the origin (zero point)

        Parameters:
        - `threshold` (float): Tolerance for considering a point as zero

        Example:
        >>> p = Point(1e-7, 1e-8, 1e-9)
        >>> p.is_zero()
        True
        """
        return self.x < threshold and self.y < threshold and self.z < threshold
    
    def is_near(self, other: 'Point', threshold: float = 1e-12) -> bool:
        """
        Checks if the point is near another point within a specified threshold

        Parameters:
        - `other` (Point): The other point.
        - `threshold` (float): Tolerance for considering two points as near

        Example:
        >>> p1 = Point(1, 2, 3)
        >>> p2 = Point(1.0000001, 1.9999999, 3.0000002)
        >>> p1.is_near(p2)
        True
        """
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        dz = abs(self.z - other.z)
        return dx < threshold and dy < threshold and dz < threshold


    def rotate_x(self, angle: Union[int, float], center: Union['Point',list]=[0,0,0]) -> 'Point':
        """
        Rotates the point around the X-axis using Matrix3x3 rotation

        Parameters:
        - `angle` (float): The rotation angle in degrees
        - `center` (Optional[Point]): The center point for rotation. Defaults to the origin

        Example:
        >>> p = Point(0, 1, 0)
        >>> p.rotate_x(90)
        >>> p
        Point(0, 0, 1)
        """

        # If a center point is provided, translate the point to the origin
        if center:
            self.x -= center[0]
            self.y -= center[1]
            self.z -= center[2]

        new_coords = Matrix3x3.rotation_x(angle) @ self.as_vector()
        self.x, self.y, self.z = new_coords.components()

        # Translate the point back to its original position
        if center:
            self.x += center[0]
            self.y += center[1]
            self.z += center[2]

        return self

    def rotate_y(self, angle: Union[int, float], center: Union['Point',list]=[0,0,0]) -> 'Point':
        """
        Rotates the point around the Y-axis

        Parameters:
        - `angle` (float): The rotation angle in degrees
        - `center` (Optional[Point]): The center point for rotation. Defaults to the origin

        Example:
        >>> p = Point(0, 0, 1)
        >>> p.rotate_y(90)
        >>> p
        Point(1, 0, 0)
        """
        # If a center point is provided, translate the point to the origin
        if center:
            self.x -= center[0]
            self.y -= center[1]
            self.z -= center[2]

        new_coords = Matrix3x3.rotation_y(angle) @ self.as_vector()
        self.x, self.y, self.z = new_coords.components()
        # Translate the point back to its original position
        if center:
            self.x += center[0]
            self.y += center[1]
            self.z += center[2]

        return self

    def rotate_z(self, angle: Union[int, float], center: Union['Point',list]=[0,0,0]) -> 'Point':
        """
        Rotates the point around the Y-axis

        Parameters:
        - `angle` (float): The rotation angle in degrees
        - `center` (Optional[Point]): The center point for rotation. Defaults to the origin

        Example:
        >>> p = Point(1, 0, 0)
        >>> p.rotate_z(90)
        >>> p
        Point(0, 1, 0)
        """
        if center:
            self.x -= center[0]
            self.y -= center[1]
            self.z -= center[2]

        new_coords = Matrix3x3.rotation_z(angle) @ self.as_vector()
        self.x, self.y, self.z = new_coords.components()
        if center:
            self.x += center[0]
            self.y += center[1]
            self.z += center[2]

        return self

    def rotate_xyz(self, phi: Union[int, float], theta: Union[int, float], psi: Union[int, float], center: Union['Point',list]=[0,0,0]) -> 'Point':
        """
        Rotates the point around the X, Y, and Z axes

        Parameters:
        - `phi` (float): Rotation angle around the X-axis in degrees
        - `theta` (float): Rotation angle around the Y-axis in degrees
        - `psi` (float): Rotation angle around the Z-axis in degrees

        Example:
        >>> p = Point(1, 2, 3)
        >>> p.rotate_xyz(90, 180, 270)
        >>> p
        Point(-3, 1, -2)
        """
        if center:
            self.x -= center[0]
            self.y -= center[1]
            self.z -= center[2]

        self.rotate_x(phi, center)
        self.rotate_y(theta, center)
        self.rotate_z(psi, center)

        if center:
            self.x += center[0]
            self.y += center[1]
            self.z += center[2]

        return self
    
    def rotate_around_axis(self, angle: Union[int, float], axis: Vector3) -> 'Point':
        """
        Rotates the point around an arbitrary axis

        Parameters:
        - `angle` (float): The rotation angle in degrees
        - `axis` (Vector3): The rotation axis

        Example:
        >>> p = Point(1, 2, 3)
        >>> axis = Vector3(1, 1, 1)
        >>> p.rotate_around_axis(45, axis)
        >>> p
        Point( 1.7011415092773154 1.183503419072274 3.11535507165041 )
        """
        new_coords = Matrix3x3.rotate_around_axis(angle, axis) @ self.as_vector()
        self.x, self.y, self.z = new_coords.components()

    def copy(self) -> 'Point':
        """
        Creates a deep copy of the point

        Example:
        >>> p = Point(1, 2, 3)
        >>> q = p.copy()
        >>> p is q
        False
        """
        return deepcopy(self)
    
    def __str__(self) -> str: 
        """
        Returns a string representation of the point in a format supported by Map files.

        Example:
        >>> p = Point(1, 2, 3)
        >>> str(p)
        '( 1 2 3 )'
        """
        return f"( {self.x} {self.y} {self.z} )"
    
    def __iter__(self) -> Iterator[float]: 
        """
        Returns an iterator over the point components (x, y, z)

        Example:
        >>> p = Point(1, 2, 3)
        >>> for component in p:
        ...     print(component)
        1
        2
        3
        """
        return iter((self.x, self.y, self.z))

    def __getitem__(self, index: int) -> float:
        """
        Returns the component of the point at the specified index

        Parameters:
        - `index` (int): Index of the component (0 for x, 1 for y, 2 for z)

        Example:
        >>> p = Point(1, 2, 3)
        >>> p[1]
        2
        """
        components = [self.x, self.y, self.z]
        
        if 0 <= index < len(components):
            return components[index]
        else:
            raise IndexError(f"Index out of range. Expected index to be 0, 1, or 2, but got {index}.")

    
    def __add__(self, other: Union['Point', Vector3]) -> 'Point': 
        """
        Adds another Point or Vector3 to this point

        Parameters:
        - `other` (Union[Point, Vector3]): The other point or vector

        Example:
        >>> p1 = Point(1, 2, 3)
        >>> p2 = Point(4, 5, 6)
        >>> p1 + p2
        Point(5, 7, 9)
        """
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Vector3):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")
        
    def __sub__(self, other: 'Point') -> Vector3:
        """
        Subtracts another Point from this point

        Parameters:
        - `other` (Point): The other point

        Example:
        >>> p1 = Point(4, 5, 6)
        >>> p2 = Point(1, 2, 3)
        >>> p1 - p2
        Vector3(3, 3, 3)
        """
        if isinstance(other, Point):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError(f"Unsupported type for subtraction: {type(other)}")
    
    def __mul__(self, other: Union[int, float]) -> 'Point':
        """
        Multiplies the point by a scalar

        Parameters:
        - `other` (float): The scalar multiplier

        Example:
        >>> p = Point(1, 2, 3)
        >>> p * 2
        Point(2, 4, 6)
        """
        if isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

    def __truediv__(self, other: Union[int, float]) -> 'Point':
        """
        Divides the point by a scalar

        Parameters:
        - `other` (float): The divisor

        Example:
        >>> p = Point(2, 4, 6)
        >>> p / 2
        Point(1.0, 2.0, 3.0)
        """
        if other == 0:
            raise ZeroDivisionError
        if isinstance(other, (int, float)):
            return Point(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(f"Unsupported type for division: {type(other)}")
    
    def __iadd__(self, other: Union[int, float,'Point']) -> 'Point':
        """
        In-place addition with another point

        Parameters:
        - `other` (Point): The other point

        Example:
        >>> p1 = Point(1, 2, 3)
        >>> p2 = Point(4, 5, 6)
        >>> p1 += p2
        >>> p1
        Point(5, 7, 9)
        """
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            self.z += other.z 
        elif isinstance(other, (int,float)):
            self.x += other
            self.y += other
            self.z += other
        else:
            raise TypeError(f"Unsupported type for in-place addition: {type(other)}")
        return self
    
    def __isub__(self, other: Union[int, float,'Point']) -> 'Point':
        """
        In-place subtraction with another point

        Parameters:
        - `other` (Point): The other point

        Example:
        >>> p1 = Point(4, 5, 6)
        >>> p2 = Point(1, 2, 3)
        >>> p1 -= p2
        >>> p1
        Point(3, 3, 3)
        """
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z 
        elif isinstance(other, (int,float)):
            self.x -= other
            self.y -= other
            self.z -= other
        else:
            raise TypeError(f"Unsupported type for in-place substraction: {type(other)}")
        return self
    
    def __imul__(self, other: Union[int, float]) -> 'Point':
        """
        In-place multiplication by a scalar

        Parameters:
        - `other` (float): The scalar multiplier

        Example:
        >>> p = Point(1, 2, 3)
        >>> p *= 2
        >>> p
        Point(2, 4, 6)
        """
        if isinstance(other, (int,float)):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise TypeError(f"Unsupported type for in-place multiplication: {type(other)}")
        return self
    
    def __itruediv__(self, other: Union[int, float]) -> 'Point':
        """
        In-place division by a scalar

        Parameters:
        - `other` (float): The divisor

        Example:
        >>> p = Point(2, 4, 6)
        >>> p /= 2
        >>> p
        Point(1.0, 2.0, 3.0)
        """
        if other == 0:
            raise ZeroDivisionError
        if isinstance(other, (int,float)):
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise TypeError(f"Unsupported type for in-place division: {type(other)}")
        return self

    def __rmul__(self, other: Union[int, float]) -> 'Point':
        """ 
        Right multiplication with a scalar

        Parameters:
        - `other` (float): The scalar multiplier

        Example:
        >>> p = Point(1, 2, 3)
        >>> 2 * p
        Point(2, 4, 6)
        """
        if isinstance(other, (int,float)):
            return Point(other * self.x, other * self.y, other * self.z)
        else:
            raise TypeError(f"Unsupported type for right multiplication: {type(other)}")

    def __eq__(self, other: 'Point') -> bool:
        """
        Checks if two points are equal

        Parameters:
        - `other` (Point): The other point

        Example:
        >>> p1 = Point(1, 2, 3)
        >>> p2 = Point(1, 2, 3)
        >>> p1 == p2
        True
        """
        if isinstance(other, Point):
            return (self.x, self.y, self.z) == (other.x, other.y, other.z)
        else:
            raise TypeError(f"Unsupported type for equality comparison: {type(other)}")


    def __ne__(self, other: 'Point') -> bool:
        """
        Checks if two points are not equal

        Parameters:
        - `other` (Point): The other point

        Example:
        >>> p1 = Point(1, 2, 3)
        >>> p2 = Point(4, 5, 6)
        >>> p1 != p2
        True
        """
        if isinstance(other, Point):
            return not self.__eq__(other)
        else:
            raise TypeError(f"Unsupported type for inequality comparison: {type(other)}")

    def __neg__(self) -> 'Point':
        """
        Negates the point

        Example:
        >>> p = Point(1, 2, 3)
        >>> -p
        Point(-1, -2, -3)
        """
        return Point(-self.x, -self.y, -self.z)