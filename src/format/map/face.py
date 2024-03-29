from __future__ import annotations
from copy import deepcopy

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
      _vertices (list[Point]): List of vertices ordered in clockwise
      _edges (list[Edge]): List of edges
    """

    def __init__(self, plane: Plane, texture: Texture):
        self.id: int = 0
        self.plane: Plane = plane
        self.texture: Texture = texture
        self._vertices: list[Point] = []
        self._edges: list[Edge] = []
        #self.width and self.heigth useful for justify texture? Need wad parser


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

    @property
    def vertices(self) -> list[Point]:
        return self._vertices
    
    @property
    def edges(self) -> list[Edge]:
        if not self._edges:
            self._edges = self._get_edges()
        return self._edges
    

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def centroid(self) -> Point|None:
        """Calculates the centroid of the face"""
        if not self.plane.collinear_points():
            if self._vertices:
                centroid_x = sum(vertex.x for vertex in self._vertices) / 3
                centroid_y = sum(vertex.y for vertex in self._vertices) / 3
                centroid_z = sum(vertex.z for vertex in self._vertices) / 3

                return Point(centroid_x, centroid_y, centroid_z)
        return None
    
    def copy(self) -> Face:
        """Creates a deep copy of the face"""
        return deepcopy(self)

    def has_texture(self, text_name: str, exact: bool = True) -> bool:
        """Checks if the face has a specific texture"""
        if exact:
            return self.texture.name == text_name.upper()
        return text_name.upper() in self.texture.name

    def is_valid(self) -> bool:
        """Checks if the face is valid based on its geometry or the texture axis alignement"""
        if (self.plane.collinear_points()
            or self.normal.is_parallel(self.texture.u_axis)
            or self.normal.is_parallel(self.texture.v_axis)):
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
        self.texture._rotate_uv_z(angle)
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
        self._vertices.append(vertex)

    def _get_edges(self) -> list[Edge]:
        """Compute the edges of the face based on its vertices"""
        if not self._vertices:
            raise ValueError("Vertices must be set before calculating edges.")

        num_vertices = len(self._vertices)
        if num_vertices < 3:
            raise ValueError("At least 3 vertices are required to form a face.")

        edges = [Edge(self._vertices[i], self._vertices[(i + 1) % num_vertices]) for i in range(num_vertices)]
        return edges

    def sort_vertices_clockwise(self) -> None:
        """Sort the vertices of the face in clockwise order"""
        center = self.centroid()
        len_vertices = len(self._vertices)
        if center:
            for n in range(len_vertices - 2):
                a = (self._vertices[n] - center).normalized()
                p = Plane(self._vertices[n], center, center + self.normal)
                smallest_angle = -1
                smallest = -1

                for m in range(n + 1, len_vertices):
                    if not p.is_point_below(self._vertices[m]):
                        b = (self._vertices[m] - center).normalized()
                        angle = a.dot(b)

                        if angle > smallest_angle:
                            smallest_angle = angle
                            smallest = m

                self._vertices[n + 1], self._vertices[smallest] = self._vertices[smallest], self._vertices[n + 1]

    def is_point_on_face(self, point: Point) -> bool:
        return NotImplemented


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __repr__(self) -> str:
        """Returns a string representation of the face."""
        return f"{self.plane} {self.texture} \n"

    def __iter__(self):
        """Return an iterator over the face plane points"""
        return iter((self.plane))

    def __contains__(self, other: str|Point) -> bool:
        """Checks if a texture or a point is present in the face plane"""
        if isinstance(other, str):
            return other in self.texture.name
        elif isinstance(other, Point):
            return other in self.plane