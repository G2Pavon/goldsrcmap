from typing import Union

from .point import Point
from .vector import Vector3
from .plane import Plane

class Edge:

    """
    A class representing a line segment between two points
    
    TODO: Use in Brush/Face edges
    """

    __slots__ = ('start', 'end', '_length', '_direction', '_invdirection')

    def __init__(self, start: Point, end: Point):
        self.start: Point = start
        self.end: Point = end
        self._length = None
        self._direction = None  # half-edge
        self._invdirection = None  # half-edge


    def __repr__(self) -> str:
        """
        Get a string representation of the edge
        """
        return f"Edge: ({self.start}; {self.end}), Length: {self.length}, Half-edges: [{self.direction1}; {self.direction2}]"

    def __str__(self) -> str:
        """
        Get a string representation of the edge
        """
        return f"[{self.start}, {self.end}]"

    def __eq__(self, other: 'Edge') -> bool:
        """
        Check if this edge is equal to another edge

        Args:
        - `other` (Edge): The other edge
        """
        return self.start == other.start and self.end == other.end


    @classmethod
    def from_points(cls, a: Point, b: Point) -> 'Edge':
        """
        Create an edge using two points

        Args:
        - `a` (Point): The starting point
        - `b` (Point): The ending point
        """
        return cls(a, b)

    @property
    def direction1(self) -> Vector3:
        """
        Get the direction vector from start to end
        """
        if not self._direction:
            self._direction = (self.end - self.start).normalize()
        return self._direction

    @property
    def direction2(self) -> Vector3:
        """
        Get the direction vector from end to start
        """
        if not self._invdirection:
            self._invdirection = (self.start - self.end).normalize()
        return self._invdirection

    @property
    def length(self) -> float:
        """
        Get the length of the edge
        """
        if not self._length:
            self._length = (self.end - self.start).length()
        return self._length

    def midpoint(self) -> Point:
        """
        Get the midpoint of the edge
        """
        mid = (self.start + self.end) / 2
        return mid

    def is_parallel(self, other: Union['Edge',Vector3,Plane]) -> bool:
        """
        Check if this edge is parallel to another edge, vector or plane

        Args:
        - `other` (Edge, Vector3, Plane): The other edge
        """
        if isinstance(other, Edge):
            return self.direction1.is_parallel(other.direction1)
        elif isinstance(other, Vector3):
            return self.direction1.is_parallel(other)
        elif isinstance(other, Plane):
            return self.direction1.is_perpendicular(other.normal)
        else:
            raise TypeError(f"Unsupported type for parallel check: {type(other)}")

    def is_perpendicular(self, other: Union['Edge',Vector3,Plane]) -> bool:
        """
        Check if this edge is perpendicular to another edge, vector or plane

        Args:
        - `other` (Edge, Vector3, Plane): The other edge, vector or plane
        """
        if isinstance(other, Edge):
            return self.direction1.is_perpendicular(other.direction1)
        elif isinstance(other, Vector3):
            return self.direction1.is_perpendicular(other)
        elif isinstance(other, Plane):
            return self.direction1.is_parallel(other.normal)
        else:
            raise TypeError(f"Unsupported type for parallel check: {type(other)}")

    def similar_to(self, other: 'Edge') -> bool:
        """
        Check if this edge is similar to another edge

        Args:
        - `other` (Edge): The other edge
        """
        return self.start.is_near(other.start) and self.end.is_near(other.end)