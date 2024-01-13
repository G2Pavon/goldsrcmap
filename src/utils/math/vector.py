from dataclasses import dataclass
from typing import Tuple, Iterator
from math import hypot

@dataclass
class Vector3:
    """
    3-D vector implementation
    """

    __slots__ = ('x', 'y', 'z') # disable dynamic attribute

    x: float
    y: float
    z: float

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def components(self) -> Tuple[float, float, float]:
        """Returns a tuple of the vector components"""
        return self.x, self.y, self.z

    def length(self) -> float:
        """Returns the length (magnitude) of the vector"""
        return hypot(self.x, self.y, self.z)

    def square_length(self) -> float:
        """Returns the square of the length (magnitude) of the vector"""
        return self.x**2+ self.y**2 + self.z**2

    def normalize(self) -> 'Vector3':
        """Normalizes the vector"""
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector.")
        inv_length = 1.0 / length
        self.x *= inv_length
        self.y *= inv_length
        self.z *= inv_length

    def normalized(self) -> 'Vector3':
        """Returns a normalized version of the vector"""
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector.")
        return Vector3(self.x / length, self.y / length, self.z / length)

    def dot(self, other: 'Vector3') -> float:
        """Computes the dot product of this vector with another vector"""
        if isinstance(other, Vector3):
            result = self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise TypeError(f"Unsupported type for dot product: {type(other)}")
        return result

    def cross(self, other: 'Vector3') -> 'Vector3':
        """Computes the cross product of this vector with another vector"""
        if isinstance(other, Vector3):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.z
            z = self.x * other.y - self.y * other.x
        else:
            raise TypeError(f"Unsupported type for cross product: {type(other)}")
        return Vector3(x, y, z)

    def is_null(self, threshold: float = 1e-4) -> bool:
        """Checks if the vector is close to the zero vector"""
        return abs(self.x) < threshold and abs(self.y) < threshold and abs(self.z) < threshold

    def is_parallel(self, other: 'Vector3', threshold: float = 1e-4) -> bool:
        """Checks if the vector is parallel to another vector"""
        if isinstance(other, Vector3):
            return abs(abs(self.dot(other)) - 1) < threshold
        else:
            raise TypeError(f"Unsupported type for parallel check: {type(other)}")

    def is_perpendicular(self, other: 'Vector3', threshold: float = 1e-4) -> bool:
        """Checks if the vector is perpendicular to another vector"""
        if isinstance(other, Vector3):
            return abs(self.dot(other)) < threshold
        else:
            raise TypeError(f"Unsupported type for perpendicular check: {type(other)}")
    

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def __str__(self) -> str:
        """Returns a formatted string of the vector"""
        return f"{self.x} {self.y} {self.z}"

    def __iter__(self) -> Iterator[float]:
        """Returns an iterator over the vector components (x, y, z)"""
        return iter((self.x, self.y, self.z))

    def __getitem__(self, index: int) -> float:
        """Returns the component of the vector at the specified index"""
        return [self.x, self.y, self.z][index]

    def __setitem__(self, index: int, value: float) -> None:
        """Sets the value of the component at the specified index"""
        self[index] = value

    def __add__(self, other: 'Vector3') -> 'Vector3':
        """Adds another vector to this vector"""
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"Unsupported type for addition (+): {type(other)}")

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        """Subtracts another vector from this vector"""
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError(f"Unsupported type for subtraction (-): {type(other)}")

    def __mul__(self, other: float) -> 'Vector3':
        """Multiplies the vector by a scalar"""
        if isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"Unsupported type for multiplication (*): {type(other)}")
        
    def __imul__(self, other: float) -> 'Vector3':
        """In-place multiplication with a scalar"""
        if isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise TypeError(f"Unsupported type for in-place division (*=): {type(other)}")
        return self

    def __rmul__(self, other: float) -> 'Vector3':
        """Right multiplication with a scalar"""
        if isinstance(other, (int, float)):
            return Vector3(other * self.x, other * self.y, other * self.z)
        else:
            raise TypeError(f"Unsupported type for right multiplication (*): {type(other)}")

    def __truediv__(self, other: float) -> 'Vector3':
        """Divides the vector by a scalar"""
        if isinstance(other, (int, float)):
            return Vector3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(f"Unsupported type for division (/): {type(other)}")

    def __itruediv__(self, other: float) -> 'Vector3':
        """In-place division with a scalar"""
        if other == 0:
            raise ZeroDivisionError
        if isinstance(other, (int, float)):
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise TypeError(f"Unsupported type for in-place division (/=): {type(other)}")
        return self

    def __eq__(self, other: 'Vector3') -> bool:
        """Checks if two vectors are equal"""
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) == (other.x, other.y, other.z)
        else:
            raise TypeError(f"Unsupported type for equality comparison: {type(other)}")

    def __ne__(self, other: 'Vector3') -> bool:
        """Checks if two vectors are not equal"""
        if isinstance(other, Vector3):
            return not self.__eq__(other)
        else:
            raise TypeError(f"Unsupported type for inequality comparison: {type(other)}")

    def __neg__(self) -> 'Vector3':
        """Negates the vector"""
        return Vector3(-self.x, -self.y, -self.z)