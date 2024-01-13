from copy import deepcopy
from typing import Union

from format.map.texture import Texture

from utils.math.plane import Plane
from utils.math.vector import Vector3
from utils.math.point import Point
from utils.math.edge import Edge


class Face:
    """
    Plane: ( x1 y1 z1 ) ( x2 y2 z2 ) ( x3 y3 z3 ) 
    Texture definition: NAME [ Ux Uy Uz Uoffset ] [ Vx Vy Vz Voffset ] rotation Uscale Vscale
                
    Three non-coplanar points define a plane
    Plane normal is oriented toward the cross product of (P1-P2) and (P3-P2)

    Attributes:
      id (int): The unique identifier for the face.
      plane (Plane): The Plane that compose the face.
      texture (Texture): The texture definition
      vertices (list[Point]): List of vertices
    """

    def __init__(self, plane: Plane, texture: Texture):
        self.id: int = 0
        self.plane: Plane = plane
        self.texture: Texture = texture
        self.vertices: list[Point] = []
        self.edges: list[Edge] = []
        #      self.width and self.heigth useful for justify texture? Need wad parser

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    @property
    def normal(self) -> Vector3:
        """Returns the normal vector of the face's plane"""
        return self.plane.normal

    @property
    def texture_normal(self) -> Vector3:
        """Returns the normal vector of the face's texture"""
        return self.texture.u_axis.cross(self.texture.v_axis).normalize()
    

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def centroid(self) -> Union[Point, None]:
        """Calculates the centroid of the face"""
        if not self.plane.collinear_points():
            centroid_x = sum(point.x for point in self.plane) / 3
            centroid_y = sum(point.y for point in self.plane) / 3
            centroid_z = sum(point.z for point in self.plane) / 3

            return Point(centroid_x, centroid_y, centroid_z)
        return None
    
    def copy(self) -> 'Face':
        """Creates a deep copy of the face"""
        return deepcopy(self)

    def has_texture(self, text_name: str, exact: bool = True):
        """Checks if the face has a specific texture"""
        if exact:
            return self.texture.name == text_name.upper()
        return text_name.upper() in self.texture.name

    def is_valid(self, threshold: float = 1e-3):
        """Checks if the face is valid based on its geometry or the texture axis alignement"""
        if (self.plane.collinear_points()
            or abs(abs(self.normal.dot(self.texture.u_axis)) - 1) < threshold
            or abs(abs(self.normal.dot(self.texture.v_axis)) - 1) < threshold
        ):
            return False
        return True

    def move_by(self, x: float, y: float, z: float):
        """Moves the face by a specified offsets"""
        for point in self.plane:
            point.move_by(x, y, z)
        self.texture._update_offset(Vector3(x, y, z))

    def rotate_x(self, angle: float, center: Point):
        """Rotates the face around the X-axis"""
        for point in self.plane:
            point.rotate_x(angle, center)
        self.texture._rotate_uv_x(angle)
        self.texture._update_offset(Vector3(0, 0, 0))

    def rotate_y(self, angle: float, center: Point):
        """Rotates the face around the Y-axis"""
        for point in self.plane:
            point.rotate_y(angle, center)
        self.texture._rotate_uv_x(angle)
        self.texture._update_offset(Vector3(0, 0, 0))

    def rotate_z(self, angle: float, center: Point):
        """Rotates the face around the Z-axis"""
        for point in self.plane:
            point.rotate_z(angle, center)
        self.texture._rotate_uv_x(angle)
        self.texture._update_offset(Vector3(0, 0, 0))

    def rotate_xyz(self, phi, theta, psi):
        """Rotates the face around the XYZ axes"""
        for point in self.plane:
            point.rotate_xyz(phi, theta, psi)
        self.texture._rotate_uv_x(phi)
        self.texture._rotate_uv_y(theta)
        self.texture._rotate_uv_z(psi)
        self.texture._update_offset(Vector3(0,0,0))

    def rotate_around_axis(self, angle: float, axis: Vector3):
        """Rotate the face around the given axis"""
        for point in self.plane:
            point.rotate_around_axis(angle, axis)
        self.texture._rotate_uv_around_axis(angle, axis)

    def set_texture(self, text_name: str):
        """Sets the texture name of the face"""
        self.texture.name = text_name

    def _add_vertex(self, vertex: Point):
        """Add a vertex to the face"""
        self.vertices.append(vertex)


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __repr__(self) -> str:
        """Returns a string representation of the face."""
        return f"{self.plane} {self.texture} \n"

    def __iter__(self):
        """Return an iterator over the face plane points"""
        return iter((self.plane))

    def __contains__(self, other: Union[str, Point]) -> bool:
        """Checks if a texture or a point is present in the face plane"""
        if isinstance(other, str):
            return other in self.texture.name
        elif isinstance(other, Point):
            return other in self.plane