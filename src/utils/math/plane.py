from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator

from utils.math.vector import Vector3
from utils.math.point import Point

@dataclass
class Plane:
    """
    3-D plane representation defined by three points.
    The plane's normal is oriented toward the cross product of (P1-P2) and (P3-P2)
    """

    p1: Point
    p2: Point
    p3: Point
    _normal: None|Vector3 = None
    _d: None|float = None

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    @property
    def normal(self) -> Vector3:
        """Calculates and caches the normal vector of the plane"""
        if self._normal is None:
            self._normal = (self.p1 - self.p2).cross(self.p3 - self.p2)
        return self._normal

    @property
    def d(self) -> float:
        """Calculates and caches the distance of the plane from the origin"""
        if self._d is None:
            self._d = -self.normal.dot(self.p1.as_vector())
        return self._d
    
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        METHODS                                   ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    
    def collinear_points(self) -> bool:
        """Checks if the plane points are collinear"""
        ab = self.p2 - self.p1
        ac = self.p3 - self.p1
        return ab.cross(ac).is_null()
    
    def distance_to_plane(self, other: Plane) -> float:
        """Calculates the distance between two planes"""
        if not isinstance(other, Plane):
            raise TypeError(f"Unsupported type for distance between plane to plane: {type(other)}")
        return abs(self.d - other.d) / self.normal.length() if self.is_parallel(other) else 0

    def distance_to_point(self, other: Point) -> float:
        """Calculates the perpendicular(shortest) distance between the plane and a point"""
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type for distance between plane to point: {type(other)}")
        return abs(self.normal.dot(other.as_vector()) + self.d) / self.normal.length()

    def is_overlap(self, other: Plane, epsilon: float = 1e-6) -> bool:
        """Checks if two planes overlap"""
        return self.is_parallel(other) and self.distance_to_plane(other) < epsilon

    def is_point_above(self, other: Point, threshold=1e-6) -> bool:
        """Checks if a point is in front of the plane"""
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type to check position relative to plane: {type(other)}")
        return self._solve_plane_equation(other) > threshold

    def is_point_below(self, other: Point, threshold=1e-6) -> bool:
        """Checks if a point is behind the plane"""
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type to check position relative to plane: {type(other)}")
        return self._solve_plane_equation(other) < -threshold

    def is_point_on_plane(self, other: Point, threshold: float = 1e-6) -> bool:
        """Checks if a point is on the plane"""
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type to check position relative to plane: {type(other)}")
        return abs(self._solve_plane_equation(other)) < threshold
    
    def is_parallel(self, other: Plane) -> bool:
        if not isinstance(other, Plane):
            raise TypeError(f"Unsupported type to check if planes are parallel: {type(other)}")
        return self.normal.is_parallel(other.normal)

    def is_perpendicular(self, other: Plane) -> bool:
        if not isinstance(other, Plane):
            raise TypeError(f"Unsupported type to check if planes are perpendicular: {type(other)}")
        return self.normal.is_perpendicular(other.normal)

    def project_point(self, other: Point) -> Point:
        if not isinstance(other, Point):
            raise TypeError(f"Unsupported type to project in plane: {type(other)}")
        vector = other - self.p1
        distance_from_plane = vector.dot(self.normal.normalized())
        projection_on_normal = distance_from_plane * self.normal.normalized()
        projection_on_plane = other - Point(*projection_on_normal)
        return Point(*projection_on_plane)
    
    def _solve_plane_equation(self, other: (Point, Vector3)) -> float:
        if isinstance(other, Point):
            other = other.as_vector()
        return self.normal.dot(other) + self.d

    
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def __repr__(self) -> str:
        return f"{self.p1} {self.p2} {self.p3}"

    def __getitem__(self, index: int) -> Point:
        """Gets the point at the specified index"""
        return [self.p1, self.p2, self.p3][index]

    def __iter__(self) -> Iterator[Point]:
        """Returns an iterator over the points of the plane"""
        return iter((self.p1, self.p2, self.p3))
    
    def __eq__(self, other: Plane) -> bool:
        return self.is_overlap(other) and self.normal.dot(other.normal) == 1


def get_plane_intersection(plane1: Plane, plane2: Plane, plane3: Plane) -> Point|None:
    """Calculates the intersection point of three planes"""
    n1, d1 = plane1.normal, plane1.d
    n2, d2 = plane2.normal, plane2.d
    n3, d3 = plane3.normal, plane3.d

    cross23 = n2.cross(n3)
    denom = n1.dot(cross23)
    if denom == 0:
        return None
    p = -(d1 * cross23 + d2 * n3.cross(n1) + d3 * n1.cross(n2)) / denom
    return Point(p.x, p.y, p.z)
