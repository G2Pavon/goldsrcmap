from dataclasses import dataclass
from typing import Union

from utils.math.point import Point
from utils.math.vector import Vector3
from utils.math.matrix import Matrix3x3


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
            self._direction = (self.end - self.start)
        return self._direction

    @property
    def direction2(self) -> Vector3:
        """Get the direction vector from end to start"""
        if not self._invdirection:
            self._invdirection = (self.start - self.end)
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

    def is_parallel(self, other: 'Edge') -> bool:
        """Check if this edge is parallel to another edge, vector or plane"""
        return self.direction1.is_perpendicular(other.direction1)

    def is_perpendicular(self, other: 'Edge') -> bool:
        """Check if this edge is perpendicular to another edge, vector or plane"""
        return self.direction1.is_perpendicular(other.direction1)

    def similar_to(self, other: 'Edge') -> bool:
        """Check if this edge is similar to another edge"""
        return self.start.is_near(other.start) and self.end.is_near(other.end)
    
    def distance_to_point(self, point: Point):
        """Return the shortest distance and closest points between edge and point"""
        t = (point - self.start).dot(self.direction1) / (self.direction1).dot(self.direction1)
        t = min(max(t, 0), 1)
        closest_edge_point = self.start + t * self.direction1
        return (point - closest_edge_point).length(), closest_edge_point

    def distance_to_edge(self, other: 'Edge'):
        """Return the shortest distance and closest points between two edges"""
        epsilon = 1e-6

        length_self_squared = self.direction1.square_length()
        length_other_squared = other.direction1.square_length()

        if length_self_squared < epsilon and length_other_squared < epsilon:
            return ((other.start - self.start).length(), self.start, other.start)

        relative_start = self.start - other.start
        dot_product = other.direction1.dot(relative_start)

        if length_self_squared < epsilon:
            s = 0
            t = min(max(dot_product / length_other_squared, 0), 1)
        else:
            dot_relative_start = self.direction1.dot(relative_start)

            if length_other_squared <= epsilon:
                t = 0
                s = min(max(-dot_relative_start / length_self_squared, 0), 1)
            else:
                dot_directions = self.direction1.dot(other.direction1)
                denom = length_self_squared * length_other_squared - dot_directions ** 2

                if denom != 0:
                    s = min(max((dot_directions * dot_product - dot_relative_start * length_other_squared) / denom, 0), 1)
                else:
                    s = 0

                t = (dot_directions * s + dot_product) / length_other_squared
                if t < 0:
                    t = 0
                    s = min(max(-dot_relative_start / length_self_squared, 0), 1)
                elif t > 1:
                    t = 1
                    s = min(max((dot_directions - dot_relative_start) / length_self_squared, 0), 1)

        closest_point_self = self.start + s * self.direction1
        closest_point_other = other.start + t * other.direction1

        return (closest_point_other - closest_point_self).length(), closest_point_self, closest_point_other
    

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __repr__(self) -> str:
        """Get a string representation of the edge"""
        return f"Edge: {self.start}<---{self.length}---> {self.end}"

    def __str__(self) -> str:
        """Get a string representation of the edge"""
        return f"[{self.start}, {self.end}]"

    def __eq__(self, other: 'Edge') -> bool:
        """Check if this edge is equal to another edge"""
        return self.start == other.start and self.end == other.end