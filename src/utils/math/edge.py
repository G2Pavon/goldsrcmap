from dataclasses import dataclass
from typing import Union

from utils.math.point import Point
from utils.math.vector import Vector3
from utils.math.geometry_utils import is_parallel, is_perpendicular


@dataclass
class Edge:
    """
    A class representing a line segment between two points
    
    TODO: Use in Brush/Face edges
    """
    start: Point
    end: Point
    _length: Union[None, float] = None
    _direction: Union[None, Vector3] = None
    _invdirection: Union[None, Vector3] = None

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        CLASSMETHOD                               ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    @classmethod
    def from_points(cls, a: Point, b: Point) -> 'Edge':
        """Create an edge using two points"""
        return cls(a, b)
    
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    @property
    def direction1(self) -> Vector3:
        """Get the direction vector from start to end"""
        if not self._direction:
            self._direction = (self.end - self.start).normalize()
        return self._direction

    @property
    def direction2(self) -> Vector3:
        """Get the direction vector from end to start"""
        if not self._invdirection:
            self._invdirection = (self.start - self.end).normalize()
        return self._invdirection

    @property
    def length(self) -> float:
        """Get the length of the edge"""
        if not self._length:
            self._length = (self.end - self.start).length()
        return self._length
    
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        METHODS                                   ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def midpoint(self) -> Point:
        """Get the midpoint of the edge"""
        mid = (self.start + self.end) / 2
        return mid

    def is_parallel(self, other) -> bool:
        """Check if this edge is parallel to another edge, vector or plane"""
        return is_parallel(self, other)

    def is_perpendicular(self, other) -> bool:
        """Check if this edge is perpendicular to another edge, vector or plane"""
        return is_perpendicular(self, other)

    def similar_to(self, other: 'Edge') -> bool:
        """Check if this edge is similar to another edge"""
        return self.start.is_near(other.start) and self.end.is_near(other.end)
    

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def __repr__(self) -> str:
        """Get a string representation of the edge"""
        return f"Edge: ({self.start}; {self.end}), Length: {self.length}, Half-edges: [{self.direction1}; {self.direction2}]"

    def __str__(self) -> str:
        """Get a string representation of the edge"""
        return f"[{self.start}, {self.end}]"

    def __eq__(self, other: 'Edge') -> bool:
        """Check if this edge is equal to another edge"""
        return self.start == other.start and self.end == other.end