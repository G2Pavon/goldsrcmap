from dataclasses import dataclass
from typing import Union, Tuple

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

    def is_parallel(self, other: 'Edge') -> bool:
        """Check if this edge is parallel to another edge, vector or plane"""
        return self.direction1.is_perpendicular(other.direction1)

    def is_perpendicular(self, other: 'Edge') -> bool:
        """Check if this edge is perpendicular to another edge, vector or plane"""
        return self.direction1.is_perpendicular(other.direction1)

    def similar_to(self, other: 'Edge') -> bool:
        """Check if this edge is similar to another edge"""
        return self.start.is_near(other.start) and self.end.is_near(other.end)

    def distance_to_edge(self: 'Edge', other: 'Edge', clampAll=True, clamp_self_start=False, clamp_self_end=False, clamp_other_start=False, clamp_other_end=False):
        """Return the closest points on each line segment, their distance, and delta distances (dx, dy, dz)
        https://stackoverflow.com/a/18994296

        clampAll = True: Closest points can not go beyond the actual edges segments
        clamAll = False: Closest points is outside the edge segment
        TODO: test in all scenarios
        """
        epsilon = 1e-6
        if clampAll:
            clamp_self_start = True
            clamp_self_end = True
            clamp_other_start = True
            clamp_other_end = True

        # Direction vectors A and B between the endpoints of the two edges
        A = self.end - self.start
        B = other.end - other.start
        # Edges length
        lengthA = A.length()
        lengthB = B.length()

        A_normalized = A / lengthA
        B_normalized = B / lengthB

        cross = A_normalized.cross(B_normalized)
        denom = (cross.length())**2

        # If lines are parallel (denom=0) test if lines overlap
        # If they don't overlap then there is a closest point solution
        # If they do overlap, there are infinite closest positions, but there is a closest distance
        if denom < epsilon:
            # Project the vector that joins both beginnings of the edges in the direction of self
            d0 = A_normalized.dot(other.start - self.start)

            # Overlap only possible with clamping
            if clamp_self_start or clamp_self_end or clamp_other_start or clamp_other_end:
                # Project the vector that joins self start and other end in the direction of self
                d1 = A_normalized.dot(other.end - self.start)

                # Is segment B before A?
                if d0 <= epsilon and 0 >= d1:
                    if clamp_self_start and clamp_other_end:
                        if abs(d0) < abs(d1):
                            # Closest points are self.start and other.start
                            distance = (self.start - other.start)
                            return self.start, other.start, distance.length(), distance.components()
                        # Closest points are self.start and other.end
                        distance = (self.start - other.end)
                        return self.start, other.end, distance.length(), distance.components()

                # Is segment B after A?
                elif d0 >= lengthA - epsilon and 0 <= d1:
                    if clamp_self_end and clamp_other_start:
                        if abs(d0) < abs(d1):
                            # Closest points are self.end and other.start
                            distance = (self.end - other.start)
                            return self.end, other.start, distance.length(), distance.components()
                        # Closest points are self.end and other.end
                        distance = (self.end - other.end)
                        return self.end, other.end, distance.length(), distance.components()

            # Segments overlap, return distance between parallel segments
            distance =  ((self.start + (d0 * A_normalized)) - other.start)
            return None, None, distance.length(), distance.components()

        # Skew lines: Calculate the projected closest points
        t = (other.start - self.start) # Vector between the starting points of the two edges

        detA = Matrix3x3(t.components(), B_normalized.components(), cross.components()).det()
        detB = Matrix3x3(t.components(), A_normalized.components(), cross.components()).det()

        t0 = detA / denom
        t1 = detB / denom

        point_on_self = self.start + (A_normalized * t0)  # Projected closest point on self
        point_on_other = other.start + (B_normalized * t1)  # Projected closest point on other

        # Clamp projections
        if clamp_self_start or clamp_self_end or clamp_other_start or clamp_other_end:
            # Clamp projection self
            if clamp_self_start and t0 < epsilon:
                point_on_self = self.start
            elif clamp_self_end and t0 > lengthA - epsilon:
                point_on_self = self.end

            # Clamp projection other
            if clamp_other_start and t1 < epsilon:
                point_on_other = other.start
            elif clamp_other_end and t1 > lengthB - epsilon:
                point_on_other = other.end

            # Clamp projection self
            if (clamp_self_start and t0 < epsilon) or (clamp_self_end and t0 > lengthA - epsilon):
                dot = B_normalized.dot(point_on_self - other.start)
                if clamp_other_start and dot < epsilon:
                    dot = epsilon
                elif clamp_other_end and dot > lengthB - epsilon:
                    dot = lengthB - epsilon
                point_on_other = other.start + (B_normalized * dot)

            # Clamp projection other
            if (clamp_other_start and t1 < epsilon) or (clamp_other_end and t1 > lengthB - epsilon):
                dot = A_normalized.dot(point_on_other - self.start)
                if clamp_self_start and dot < epsilon:
                    dot = epsilon
                elif clamp_self_end and dot > lengthA - epsilon:
                    dot = lengthA - epsilon
                point_on_self = self.start + (A_normalized * dot)

        distance = (point_on_self - point_on_other)
        return point_on_self, point_on_other, distance.length(), distance.components()

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