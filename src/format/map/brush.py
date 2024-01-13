from copy import deepcopy
from typing import Optional, Union

from format.map.face import Face
from format.map.texture import Texture

from utils.math.vector import Vector3
from utils.math.point import Point
from utils.math.plane import Plane, get_intersection

class Brush:
    """
    Represents a brush defined by a list of faces

    Attributes:
    - id (int): The unique identifier for the brush.
    - faces (list[Face]): The faces that compose the brush.
    - face_counter (int): Counter for assigning unique IDs to faces.
    - _vertices (list[Point]): Cached list of vertices for the brush.
    - _origin (Optional[Point]): Cached centroid of the brush.
    """

    def __init__(self):
        self.id: int = 0
        self.faces: list[Face] = []
        self.face_counter: int = 0
        self._vertices: list[Point] = []
        self._origin: Optional[Point] = None


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    @property
    def vertices(self):
        """Get a list of vertices associated with the brush"""
        if not self._vertices:
            self._vertices = self._get_vertices()
        return self._vertices
    
    @property
    def origin(self):
        """Get the origin (centroid) of the brush"""
        if self._origin is None:
            self._origin = self.centroid()
        return self._origin


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def add_face(self, *args: Union[Face, list[Face]]) -> None:
        """Add face(es) to the brush"""
        for arg in args:
            face_list = arg if isinstance(arg, list) else [arg]
            for face in face_list:
                if isinstance(face, Face):
                    face.id = self.face_counter
                    self.face_counter += 1
                    self.faces.append(face)
                else:
                    raise TypeError(f"Expected <class {Face.__name__}> but got {type(face).__name__}")

    def bounding_box_origin(self) -> Point:
        """Return the origin of the bounding box enclosing the brush"""
        vertices = self.vertices
        return Point(
            (min(vertex.x for vertex in vertices) + max(vertex.x for vertex in vertices)) / 2,
            (min(vertex.y for vertex in vertices) + max(vertex.y for vertex in vertices)) / 2,
            (min(vertex.z for vertex in vertices) + max(vertex.z for vertex in vertices)) / 2,
        )

    def centroid(self) -> Point:
        """Return the origin (centroid) of the brush"""
        total_vertices = len(self.vertices)
        if total_vertices == 0:
            return Point(0, 0, 0)

        centroid_x = sum(vertex.x for vertex in self.vertices) / total_vertices
        centroid_y = sum(vertex.y for vertex in self.vertices) / total_vertices
        centroid_z = sum(vertex.z for vertex in self.vertices) / total_vertices

        return Point(centroid_x, centroid_y, centroid_z)
    
    def collide_with(self, other: 'Brush') -> bool:
        """Check if the current brush collides with another brush"""
        # lazy implementation, not tested 
        for vertex in self.vertices:
            if other.is_point_inside(vertex):
                return True
        for vertex in other.vertices:
            if self.is_point_inside(vertex):
                return True
        return False
    
    def copy(self) -> 'Brush':
        """Create a deep copy of the brush"""
        return deepcopy(self)

    def has_texture(self, name: str, exact: bool = True) -> bool:
        """Check if any brush face has a specific texture"""
        return any(face.has_texture(name, exact) for face in self)
    
    def is_point_inside(self, point: Point) -> bool:
        """Check if a given point is inside the brush"""
        for face in self.faces:
            if face.plane.normal.dot(point.as_vector()) + face.plane.d > 0:
                return False
        return True

    def move_by(self, x: float, y: float, z: float):
        """Moves the brush by a specified offsets"""
        for face in self:
            face.move_by(x, y, z)

    def move_to(self, x: float, y: float, z: float, centroid=True, bbox=False):
        """Move the brush to a specific coordinate"""
        if centroid and not bbox:
            reference = self.centroid()
        elif bbox:
            reference = self.bounding_box_origin()
        x -= reference.x
        y -= reference.y
        z -= reference.z

        for face in self:
            face.move_by(x, y, z)

    def replace_texture(self, old: str, new: str):
        """Replaces only on those the faces that have the texture"""
        for face in self:
            if face.has_texture(old):
                face.set_texture(new)

    def rotate_x(self, angle: float, center: Point = Point(0,0,0)):
        """Rotate the brush around X-axis"""
        #TODO: add brush origin as default reference point
        #FIXME: texture offset update does not work when the reference point != (0,0,0)
        for face in self.faces:
            face.rotate_x(angle, center)

    def rotate_y(self, angle: float, center: Point = Point(0,0,0)):
        """Rotate the brush around Y-axis"""
        for face in self.faces:
            face.rotate_y(angle, center)

    def rotate_z(self, angle: float, center: Point = Point(0,0,0)):
        """Rotate the brush around Z-axis"""
        for face in self.faces:
            face.rotate_z(angle, center)

    def rotate_xyz(self, phi, theta, psi):
        """Rotate the brush around the XYZ axes"""
        for face in self.faces:
            face.rotate_xyz(phi, theta, psi)

    def rotate_around_axis(self, angle: float, axis: Vector3):
        """Rotate the brush around a specified axis"""
        for face in self.faces:
            face.rotate_around_axis(angle, axis)

    def set_texture(self, new_texture: str):
        """Set a new texture for all faces in the brush"""
        for face in self:
            face.set_texture(new_texture)

    def _get_vertices(self) -> list[Point]:
        """Return the vertices of the brush"""
        #https://github.com/stefanha/map-files/blob/master/MAPFiles.pdf
        
        brush_vertices = []

        for i in range(len(self.faces) - 2):
            plane_i = self.faces[i].plane

            for j in range(i, len(self.faces) - 1):
                plane_j = self.faces[j].plane

                for k in range(j, len(self.faces)):
                    plane_k = self.faces[k].plane

                    vertex = get_intersection(plane_i, plane_j, plane_k)
                    if vertex:
                        legal = True
                        as_vector = Vector3(vertex.x, vertex.y, vertex.z)

                        for m in range(len(self.faces)):
                            if m != i and m != j and m != k:
                                if plane_m := self.faces[m].plane:
                                    if plane_m.normal.dot(as_vector) + plane_m.d > 0:
                                        legal = False  # vertex is out of brush
                                        break
                        if legal:
                            self.faces[i]._add_vertex(vertex)
                            self.faces[j]._add_vertex(vertex)
                            self.faces[k]._add_vertex(vertex)
                            brush_vertices.append(vertex)

        for face in self.faces:
            vertices = face._vertices
            center = face.centroid()

            for n in range(len(vertices) - 2):
                a = (face._vertices[n] - center).normalized()
                p = Plane(face._vertices[n], center, center + face.normal)
                smallest_angle = -1
                smallest = -1

                for m in range(n + 1, len(vertices)):
                    if not p.point_behind(face._vertices[m]):
                        b = (face._vertices[m] - center).normalized()
                        angle = a.dot(b)

                        if angle > smallest_angle:
                            smallest_angle = angle
                            smallest = m

                face._vertices[n + 1], face._vertices[smallest] = face._vertices[smallest], face._vertices[n + 1]

        return brush_vertices


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __repr__(self): 
        """Return a string representation of the brush"""
        return f'{self.faces}'
    
    def __iter__(self): 
        """Return an iterator over the faces of the brush"""
        return iter(self.faces)
