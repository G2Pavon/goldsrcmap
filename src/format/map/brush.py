from __future__ import annotations
from copy import deepcopy

from format.map.face import Face

from utils.math.vector import Vector3
from utils.math.point import Point
from utils.math.edge import Edge
from utils.math.plane import get_plane_intersection

class Brush:
    """
    Represents a brush defined by a list of faces.
    A brush is convex polyhedron defined by the intersection of half-spaces.

    Attributes:
    - id (int): The unique identifier for the brush.
    - faces (list[Face]): The faces that compose the brush.
    - face_counter (int): Counter for assigning unique IDs to faces.
    - _vertices (list[Point]): Cached list of vertices for the brush.
    - _origin (Optional[Point]): Cached centroid of the brush.
    """

    def __init__(self, faces: list[Face]|None=None):
        self._id: int = 0
        self.faces: list[Face] = []
        self.face_counter: int = 0
        self._origin: Point|None = None
        if faces is None: # when load map
            self._vertices: list[Point] = []

        elif isinstance(faces, list): # when use BrushGenerator
            if not len(faces) >= 4:
                raise ValueError(f'Invalid number of faces, expected 4 or more but found {len(faces)}')
            for face in faces:
                if not isinstance(face, Face):
                    raise TypeError(f'Excepted a list of Face instances but found {type(face)}: {face}')
            self.add_face(faces)
            self._vertices: list[Point] = self._vertex_enumeration()


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    @property
    def vertices(self) -> list[Point]:
        """Get a list of vertices of the brush"""
        if not self._vertices:
            self._vertices = self._vertex_enumeration()
        return self._vertices
    
    @property
    def origin(self) -> Point:
        """Get the origin (centroid) of the brush"""
        if self._origin is None:
            self._origin = self.centroid()
        return self._origin

    @property
    def edges(self) -> list[Edge]:
        """Get a list of edges of the brush"""
        edges =[]
        self.vertices
        for face in self:
            face.vertices
            edges.extend(face.edges)
        return edges


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def add_face(self, *args: Face | list[Face]) -> None:
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
    
    def copy(self) -> Brush:
        """Create a deep copy of the brush"""
        return deepcopy(self)

    def has_texture(self, name: str, exact: bool = True) -> bool:
        """Check if any brush face has a specific texture"""
        return any(face.has_texture(name, exact) for face in self)

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
                
    def _vertex_enumeration(self) -> list[Point]:
        """Return the vertices of the brush"""
        brush_vertices = []
        num_faces = len(self.faces)
        all_faces = self.faces

        for i in range(num_faces - 2):
            face_i = all_faces[i]

            for j in range(i + 1, num_faces - 1):
                face_j = all_faces[j]

                for k in range(j + 1, num_faces):
                    face_k = all_faces[k]

                    # Point of intersection
                    vertex = get_plane_intersection(face_i.plane, face_j.plane, face_k.plane)
                    if vertex:
                        as_vector = Vector3(vertex.x, vertex.y, vertex.z)

                        # Check if the point is outside
                        outside_brush = False
                        for m in range(num_faces):
                            if m != i and m != j and m != k:
                                plane_m = all_faces[m].plane
                                if plane_m.normal.dot(as_vector) + plane_m.d > 0:
                                    outside_brush = True
                                    break

                        if not outside_brush and not any(vertex.is_close(v) for v in brush_vertices):
                            brush_vertices.append(vertex)
                            face_i._add_vertex(vertex)
                            face_i.sort_vertices_clockwise()

                            face_j._add_vertex(vertex)
                            face_j.sort_vertices_clockwise()

                            face_k._add_vertex(vertex)
                            face_k.sort_vertices_clockwise()
        return brush_vertices


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __repr__(self) -> str: 
        """Return a string representation of the brush"""
        return f'{self.faces}'
    
    def __iter__(self): 
        """Return an iterator over the faces of the brush"""
        return iter(self.faces)