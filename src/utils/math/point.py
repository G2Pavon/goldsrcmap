from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Iterator
from copy import deepcopy

from math import hypot

from .vector import Vector3
from .matrix import Matrix3x3

@dataclass
class Point:
    """
    3-D point implementation
    """
    __slots__ = ('x', 'y', 'z') # disable dynamic attribute

    x: float
    y: float
    z: float

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        METHODS                                   ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def components(self) -> Tuple[float, float, float]:
        """Returns the components of the point as a tuple"""
        return self.x, self.y, self.z

    def as_vector(self) -> Vector3:
        return Vector3(self.x, self.y, self.z)

    def distance_to_point(self, other: Point) -> float:
        """Calculates the Euclidean distance between two points"""
        return hypot(other.x - self.x, other.y - self.y, other.z - self.z)

    def square_distance(self, other: Point) -> float:
        """Calculates the squared Euclidean distance between two points"""
        return (other.x - self.x)**2 + (other.y - self.y)**2 + (other.z - self.z)**2
    
    def move_by(self, x: float, y:float, z:float) -> Point:
        """Moves the point by the specified offsets"""
        self.x += x
        self.y += y
        self.z += z
        return self

    def is_zero(self, threshold: float = 1e-6) -> bool:
        """Checks if the point is close to the origin"""
        return abs(self.x) < threshold and abs(self.y) < threshold and abs(self.z) < threshold
    
    def is_close(self, other: Point, threshold: float = 1e-12) -> bool:
        """Checks if the point is near another point within a specified threshold"""
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        dz = abs(self.z - other.z)
        return dx < threshold and dy < threshold and dz < threshold

    def rotate_x(self, angle: float, center: Point|list=[0,0,0]):
        """Rotates the point around the X-axis using Matrix3x3 rotation"""
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

    def rotate_y(self, angle: float, center: Point|list=[0,0,0]):
        """Rotates the point around the Y-axis"""
        if center:
            self.x -= center[0]
            self.y -= center[1]
            self.z -= center[2]
        new_coords = Matrix3x3.rotation_y(angle) @ self.as_vector()
        self.x, self.y, self.z = new_coords.components()
        if center:
            self.x += center[0]
            self.y += center[1]
            self.z += center[2]
        return self

    def rotate_z(self, angle: float, center: Point|list=[0,0,0]):
        """Rotates the point around the Y-axis"""
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

    def rotate_xyz(self, phi: float, theta: float, psi: float, center: Point|list=[0,0,0]):
        """Rotates the point around the X, Y, and Z axes"""
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
    
    def rotate_around_axis(self, angle: float, axis: Vector3):
        """Rotates the point around an arbitrary axis """
        new_coords = Matrix3x3.rotate_around_axis(angle, axis) @ self.as_vector()
        self.x, self.y, self.z = new_coords.components()

    def copy(self) -> Point:
        """Creates a deep copy of the point"""
        return deepcopy(self)
    

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def __str__(self) -> str: 
        """Returns a string representation of the point in a format supported by Map files"""
        return f"( {self.x} {self.y} {self.z} )"
    
    def __iter__(self) -> Iterator[float]: 
        """Returns an iterator over the point components"""
        return iter((self.x, self.y, self.z))

    def __getitem__(self, index: int) -> float:
        """Returns the component of the point at the specifie index"""
        return [self.x, self.y, self.z][index]
    
    def __setitem__(self, index: int, value: float):
        """Sets the component of the point at the specified index"""
        self[index] = float(value)

    def __add__(self, other: Point|Vector3) -> Point: 
        """Adds another Point or Vector3 to this point"""
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Vector3):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"Unsupported type for addition (+): {type(other)}")
        
    def __sub__(self, other: Point) -> Vector3:
        """Subtracts another Point from this point"""
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type for subtraction (-): {type(other)}")
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other: float) -> Point:
        """Multiplies the point by a scalar"""
        if not isinstance(other, (int, float)):
            raise TypeError(f"Unsupported type for multiplication (*): {type(other)}")
        return Point(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float) -> Point:
        """Divides the point by a scalar"""
        if other == 0:
            raise ZeroDivisionError
        if not isinstance(other, (int, float)):
            raise TypeError(f"Unsupported type for division (/): {type(other)}")
        return Point(self.x / other, self.y / other, self.z / other)
    
    def __iadd__(self, other: float|Point) -> Point:
        """In-place addition"""
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            self.z += other.z 
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
            self.z += other
        else:
            raise TypeError(f"Unsupported type for in-place addition (+=): {type(other)}")
        return self
    
    def __isub__(self, other: float|Point) -> Point:
        """In-place subtraction"""
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z 
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
            self.z -= other
        else:
            raise TypeError(f"Unsupported type for in-place substraction (-=): {type(other)}")
        return self
    
    def __imul__(self, other: float) -> Point:
        """In-place multiplication by a scalar"""
        if not isinstance(other, (int, float)):
            raise TypeError(f"Unsupported type for in-place multiplication (*=): {type(other)}")
        self.x *= other
        self.y *= other
        self.z *= other
        return self
    
    def __itruediv__(self, other: float) -> Point:
        """In-place division by a scalar"""
        if other == 0:
            raise ZeroDivisionError
        if not isinstance(other, (int, float)):
            raise TypeError(f"Unsupported type for in-place division (/=): {type(other)}")
        self.x /= other
        self.y /= other
        self.z /= other
        return self

    def __rmul__(self, other: float) -> Point:
        """Right multiplication with a scalar"""
        if not isinstance(other, (int, float)):
            raise TypeError(f"Unsupported type for right multiplication (*): {type(other)}")
        return self.__mul__(other)

    def __eq__(self, other: Point) -> bool:
        """Checks if two points are equal"""
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type for equality comparison (==): {type(other)}")
        return self.x, self.y, self.z == other.x, other.y, other.z

    def __ne__(self, other: Point) -> bool:
        """Checks if two points are not equal"""
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type for inequality comparison (!=): {type(other)}")
        return not self.__eq__(other)

    def __neg__(self) -> Point:
        """Negates the point"""
        return Point(-self.x, -self.y, -self.z)