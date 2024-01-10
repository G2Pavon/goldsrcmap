from dataclasses import dataclass
from typing import Union, Tuple, Iterator

from math import hypot

@dataclass
class Vector3:
    __slots__ = ('x', 'y', 'z') # disable dynamic attribute

    x: float
    y: float
    z: float

    def __str__(self) -> str:
        """
        Returns a formatted string of the vector
        
        Example:
        >>> v = Vector3(1, 2, 3)
        >>> str(v)
        '1.0 2.0 3.0'
        """
        return f"{self.x} {self.y} {self.z}"

    def __iter__(self) -> Iterator[float]:
        """
        Returns an iterator over the vector components (x, y, z)
        """
        return iter((self.x, self.y, self.z))

    def __getitem__(self, index: int) -> float:
        """
        Returns the component of the vector at the specified index

        Parameters:
        - `index` (int): Index of the component (0 for x, 1 for y, 2 for z)

        Example:
        >>> v = Vector3(1, 2, 3)
        >>> v[0]
        1.0
        """
        components = [self.x, self.y, self.z]
        if 0 <= index < 3:
            return components[index]
        else:
            raise IndexError(f"Index out of range. Expected index to be 0, 1, or 2, but got {index}.")

    def __setitem__(self, index: int, value: Union[int, float]) -> None:
        """
        Sets the value of the component at the specified index

        Parameters:
        - `index` (int): Index of the component (0 for x, 1 for y, 2 for z)
        - `value` (Union[int, float]): The new value of the component

        Example:
        >>> v = Vector3(1, 2, 3)
        >>> v[0] = 4
        >>> v.x
        4
        """
        if 0 <= index < 3:
            setattr(self, ['x', 'y', 'z'][index], value)
        else:
            raise IndexError(f"Index out of range. Expected index to be 0, 1, or 2, but got {index}.")

    def __add__(self, other: 'Vector3') -> 'Vector3':
        """
        Adds another vector to this vector

        Parameters:
        - `other` (Vector3): The other vector to add

        Example:
        >>> v1 = Vector3(1, 2, 3)
        >>> v2 = Vector3(4, 5, 6)
        >>> v1 + v2
        Vector3(x=5.0, y=7.0, z=9.0)
        """
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        """
        Subtracts another vector from this vector

        Parameters:
        - `other` (Vector3): The other vector to subtract

        Example:
        >>> v1 = Vector3(4, 5, 6)
        >>> v2 = Vector3(1, 2, 3)
        >>> v1 - v2
        Vector3(x=3.0, y=3.0, z=3.0)
        """
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError(f"Unsupported type for subtraction: {type(other)}")

    def __mul__(self, other: Union[int, float]) -> 'Vector3':
        """
        Multiplies the vector by a scalar

        Parameters:
        - `other` (int or float): The scalar multiplier

        Example:
        >>> v = Vector3(1, 2, 3)
        >>> v * 2
        Vector3(x=2.0, y=4.0, z=6.0)
        """
        if isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

    def __rmul__(self, other: Union[int, float]) -> 'Vector3':
        """
        Right multiplication with a scalar

        Parameters:
        - `other` (int or float): The scalar multiplier

        Example:
        >>> v = Vector3(1, 2, 3)
        >>> 2 * v
        Vector3(x=2.0, y=4.0, z=6.0)
        """
        if isinstance(other, (int, float)):
            return Vector3(other * self.x, other * self.y, other * self.z)
        else:
            raise TypeError(f"Unsupported type for right multiplication: {type(other)}")

    def __truediv__(self, other: float) -> 'Vector3':
        """
        Divides the vector by a scalar

        Parameters:
        - `other` (int or float): The divisor

        Example:
        >>> v = Vector3(2, 4, 6)
        >>> v / 2
        Vector3(x=1.0, y=2.0, z=3.0)
        """
        if isinstance(other, (int, float)):
            return Vector3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(f"Unsupported type for division: {type(other)}")

    def __itruediv__(self, other: Union[int, float]) -> 'Vector3':
        """
        In-place division with a scalar

        Parameters:
        - `other` (int or float): The divisor

        Example:
        >>> v = Vector3(2, 4, 6)
        >>> v /= 2
        >>> v
        Vector3(x=1.0, y=2.0, z=3.0)
        """
        if other == 0:
            raise ZeroDivisionError
        if isinstance(other, (int, float)):
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise TypeError(f"Unsupported type for in-place division: {type(other)}")
        return self

    def __eq__(self, other: 'Vector3') -> bool:
        """
        Checks if two vectors are equal

        Parameters:
        - `other` (Vector3): The other vector

        Example:
        >>> v1 = Vector3(1, 2, 3)
        >>> v2 = Vector3(1, 2, 3)
        >>> v1 == v2
        True
        """
        if isinstance(other, Vector3):
            return (self.x, self.y, self.z) == (other.x, other.y, other.z)
        else:
            raise TypeError(f"Unsupported type for equality comparison: {type(other)}")

    def __ne__(self, other: 'Vector3') -> bool:
        """
        Checks if two vectors are not equal

        Parameters:
        - `other` (Vector3): The other vector

        Example:
        >>> v1 = Vector3(1, 2, 3)
        >>> v2 = Vector3(4, 5, 6)
        >>> v1 != v2
        True
        """
        if isinstance(other, Vector3):
            return not self.__eq__(other)
        else:
            raise TypeError(f"Unsupported type for inequality comparison: {type(other)}")

    def __neg__(self) -> 'Vector3':
        """
        Negates the vector

        Example:
        >>> v = Vector3(1, 2, 3)
        >>> -v
        Vector3(x=-1.0, y=-2.0, z=-3.0)
        """
        return Vector3(-self.x, -self.y, -self.z)

    def components(self) -> Tuple[float, float, float]:
        """
        Returns a tuple of the vector components (x, y, z)

        Example:
        >>> v = Vector3(1, 2, 3)
        >>> v.components()
        (1.0, 2.0, 3.0)
        """
        return self.x, self.y, self.z

    def length(self) -> float:
        """
        Returns the length (magnitude) of the vector

        Example:
        >>> v = Vector3(3, 4, 0)
        >>> v.length()
        5.0
        """
        return hypot(self.x, self.y, self.z)

    def square_length(self) -> float:
        """
        Returns the square of the length (magnitude) of the vector

        Example:
        >>> v = Vector3(3, 4, 0)
        >>> v.square_length()
        25.0
        """
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self) -> 'Vector3':
        """
        Normalizes the vector

        Example:
        >>> v = Vector3(3, 4, 0)
        >>> v.normalize()
        >>> v
        Vector3(x=0.6, y=0.8, z=0.0)
        """
        length = self.length()
        if length == 0:
            return self
        self /= length
        return self

    def normalized(self) -> 'Vector3':
        """
        Returns a normalized version of the vector

        Example:
        >>> v = Vector3(3, 4, 0)
        >>> v.normalized()
        Vector3(x=0.6, y=0.8, z=0.0)
        """
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector.")
        return Vector3(self.x / length, self.y / length, self.z / length)

    def dot(self, other: 'Vector3') -> float:
        """
        Computes the dot product of this vector with another vector

        Parameters:
        - `other` (Vector3): The other vector

        Example:
        >>> v1 = Vector3(1, 2, 3)
        >>> v2 = Vector3(4, 5, 6)
        >>> v1.dot(v2)
        32.0
        """
        if isinstance(other, Vector3):
            result = self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise TypeError(f"Unsupported type for dot product: {type(other)}")
        return result

    def cross(self, other: 'Vector3') -> 'Vector3':
        """
        Computes the cross product of this vector with another vector

        Parameters:
        - `other` (Vector3): The other vector

        Example:
        >>> v1 = Vector3(1, 0, 0)
        >>> v2 = Vector3(0, 1, 0)
        >>> v1.cross(v2)
        Vector3(x=0.0, y=0.0, z=1.0)
        """
        if isinstance(other, Vector3):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.z
            z = self.x * other.y - self.y * other.x
        else:
            raise TypeError(f"Unsupported type for cross product: {type(other)}")
        return Vector3(x, y, z)

    def is_null(self, threshold: float = 1e-4) -> bool:
        """
        Checks if the vector is close to the zero vector

        Parameters:
        - `threshold` (float): Tolerance for considering the vector as null

        Example:
        >>> v = Vector3(1e-5, 1e-5, 1e-5)
        >>> v.is_null()
        True
        """
        return abs(self.x) < threshold and abs(self.y) < threshold and abs(self.z) < threshold

    def is_parallel(self, other: 'Vector3', threshold: float = 1e-4) -> bool:
        """
        Checks if the vector is parallel to another vector

        Parameters:
        - `other` (Vector3): The other vector.
        - `threshold` (float): Tolerance for considering vectors as parallel

        Example:
        >>> v1 = Vector3(1, 2, 3)
        >>> v2 = Vector3(2, 4, 6)
        >>> v1.is_parallel(v2)
        True
        """
        if isinstance(other, Vector3):
            return abs(abs(self.dot(other)) - 1) < threshold
        else:
            raise TypeError(f"Unsupported type for parallel check: {type(other)}")

    def is_perpendicular(self, other: 'Vector3', threshold: float = 1e-4) -> bool:
        """
        Checks if the vector is perpendicular to another vector

        Parameters:
        - `other` (Vector3): The other vector.
        - `threshold` (float): Tolerance for considering vectors as perpendicular

        Example:
        >>> v1 = Vector3(1, 0, 0)
        >>> v2 = Vector3(0, 1, 0)
        >>> v1.is_perpendicular(v2)
        True
        """
        if isinstance(other, Vector3):
            return abs(self.dot(other)) < threshold
        else:
            raise TypeError(f"Unsupported type for perpendicular check: {type(other)}")

    # TODO: Implement vector rotation methods (avoid circular import with Matrix class)