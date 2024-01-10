from dataclasses import dataclass
from typing import Union

from utils.math.vector import Vector3
from utils.math.point import Point

@dataclass
class Plane:
    """
    Represents a 3D plane defined by three points.
    The plane's normal is oriented toward the cross product of (P1-P2) and (P3-P2)
    """
    __slots__ = ('p1', 'p2', 'p3')  # disable dynamic attribute

    p1: Point
    p2: Point
    p3: Point

    def __repr__(self):
        return f"{self.p1} {self.p2} {self.p3}"

    def __getitem__(self, index: int) -> Point:
        """
        Gets the point at the specified index.

        Args:
        - `index` (int): Index of the point (0, 1, or 2)
        """
        return (self.p1, self.p2, self.p3)[index]

    def __iter__(self):
        """
        Returns an iterator over the points of the plane
        """
        yield from (self.p1, self.p2, self.p3)

    def __setitem__(self, index: int, value: Point):
        """
        Sets the point at the specified index

        Args:
        - `index` (int): Index of the point (0, 1, or 2)
        - `value` (Point): The new value of the point
        """
        if 0 <= index <=2:
            setattr(self, ['p1', 'p2', 'p3'][index], value)
        else:
            raise IndexError("Index out of range")

    @property
    def normal(self) -> Vector3:
        """
        Calculates and returns the normal vector of the plane
        """
        return (self.p1 - self.p2).cross(self.p3 - self.p2)

    @property
    def d(self) -> float:
        """
        Calculates and returns the distance of the plane from the origin
        """
        return -self.normal.dot(self.p1.as_vector())

    def collinear_points(self) -> bool:
        """
        Checks if the plane points are collinear
        """
        ab = self.p2 - self.p1
        ac = self.p3 - self.p1
        return ab.cross(ac).is_null()

    def distance_to_point(self, point: Point) -> float:
        """
        Calculates the distance from the plane to a point

        Args:
        - `point` (Point): The point to calculate the distance to
        """
        return abs(self.normal.dot(point.as_vector()) + self.d) / self.normal.length()

    def point_in_front(self, point: Point, threshold=1e-4) -> bool:
        """
        Checks if a point is in front of the plane

        Args:
        - `point` (Point): The point to check
        - `threshold` (float): Tolerance for considering the point in front
        """
        return self.normal.dot(point - self.p1) > threshold

    def point_behind(self, point: Point, threshold=-1e-4) -> bool:
        """
        Checks if a point is behind the plane

        Args:
        - `point` (Point): The point to check
        - `threshold` (float): Tolerance for considering the point behind
        """
        return self.normal.dot(point - self.p1) < threshold

    def point_on_plane(self, point: Point, threshold: float = 1e-4) -> bool:
        """
        Checks if a point is on the plane.

        Args:
        - `point` (Point): The point to check.
        - `threshold` (float): Tolerance for considering the point on the plane.
        """
        distance_to_plane = abs(self.normal.dot(point.as_vector()) + self.d)
        return distance_to_plane < threshold

def get_intersection(plane1: Plane, plane2: Plane, plane3: Plane) -> Union[Point, None]:
    """
    Calculates the intersection point of three planes

    Args:
    - `plane1` (Plane): The first plane
    - `plane2` (Plane): The second plane
    - `plane3` (Plane): The third plane
    """
    n1, d1 = plane1.normal, plane1.d
    n2, d2 = plane2.normal, plane2.d
    n3, d3 = plane3.normal, plane3.d
    denom = n1.dot(n2.cross(n3))

    if denom == 0:
        return None

    p = (-d1 * n2.cross(n3) - d2 * n3.cross(n1) - d3 * n1.cross(n2)) / denom
    return Point(p.x, p.y, p.z)