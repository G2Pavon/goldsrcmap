from copy import deepcopy
from typing import Optional, Union

from format.map.face import Face

from utils.math.vector import Vector3
from utils.math.point import Point
from utils.math.plane import get_intersection

class Brush:

    def __init__(self):
        self.id: int = 0
        self.faces: list[Face] = []
        self.face_counter: int = 0
        self._vertices: list[Point] = []
        self._origin: Optional[Point] = None

    def __repr__(self): 
        return f'{self.faces}'
    def __iter__(self): 
        return iter(self.faces)

    @property
    def vertices(self):
        if not self._vertices:
            self._vertices = self._get_vertices()
        return self._vertices
    
    @property
    def origin(self):
        if self._origin is None:
            self._origin = self.centroid()
        return self._origin
    
    def copy(self) -> 'Brush':
        return deepcopy(self)

    def add_face(self, *args: Union[Face, list[Face]]) -> None:
        """Add face(es) to the brush

        Args:
            *args (Face or list[Face] ): Face(es) to add

        Raises:
            TypeError: If the input is not a Face or a list of Faces
        """
        for arg in args:
            face_list = arg if isinstance(arg, list) else [arg]
            for face in face_list:
                if isinstance(face, Face):
                    face.id = self.face_counter
                    self.face_counter += 1
                    self.faces.append(face)
                else:
                    raise TypeError(f"Expected <class {Face.__name__}> but got {type(face).__name__}")


    def has_texture(self, name: str, exact: bool = True) -> bool:
        return any(face.has_texture(name, exact) for face in self)

    
    def set_texture(self, new_texture: str):
        for face in self:
            face.set_texture(new_texture)

    def replace_texture(self, old: str, new: str):
        for face in self:
            if face.has_texture(old):
                face.set_texture(new)
    
    def move_by(self, x: float, y: float, z: float):
        for face in self:
            face.move_by(x, y, z)

    def move_to(self, x: float, y: float, z: float, centroid=True, bbox=False):
        if centroid and not bbox:
            reference = self.centroid()
        elif bbox:
            reference = self.bounding_box_origin()
        x -= reference.x
        y -= reference.y
        z -= reference.z

        for face in self:
            face.move_by(x, y, z)


    def rotate_x(self, angle: float, center: Point = Point(0,0,0)):
        #TODO: add brush origin as default reference point
        #FIXME: texture offset update does not work when the reference point != (0,0,0)
        for face in self.faces:
            face.rotate_x(angle, center)

    def rotate_y(self, angle: float, center: Point = Point(0,0,0)):
        for face in self.faces:
            face.rotate_y(angle, center)

    def rotate_z(self, angle: float, center: Point = Point(0,0,0)):
        for face in self.faces:
            face.rotate_z(angle, center)

    def rotate_xyz(self, phi, theta, psi):
        for face in self.faces:
            face.rotate_xyz(phi, theta, psi)

    def rotate_around_axis(self, angle: float, axis: Vector3):
        for face in self.faces:
            face.rotate_around_axis(angle, axis)

    def bounding_box_origin(self) -> Point:
        vertices = self.vertices
        return Point(
            (min(vertex.x for vertex in vertices) + max(vertex.x for vertex in vertices)) / 2,
            (min(vertex.y for vertex in vertices) + max(vertex.y for vertex in vertices)) / 2,
            (min(vertex.z for vertex in vertices) + max(vertex.z for vertex in vertices)) / 2,
        )
    
    def centroid(self) -> Point:
        """
        Calculates the centroid of the brush based on its vertices.

        Returns:
        - Point: The centroid of the brush.
        """
        total_vertices = len(self.vertices)
        if total_vertices == 0:
            return Point(0, 0, 0)

        centroid_x = sum(vertex.x for vertex in self.vertices) / total_vertices
        centroid_y = sum(vertex.y for vertex in self.vertices) / total_vertices
        centroid_z = sum(vertex.z for vertex in self.vertices) / total_vertices

        return Point(centroid_x, centroid_y, centroid_z)


    def _get_vertices(self) -> list[Point]:
        #TODO: Order vertices in clockwise direction
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
        return brush_vertices

    def collide_with(self, other: 'Brush') -> bool:
        """
        Check if the current brush collides with another brush.

        Args:
        - other ('Brush'): The other brush to check for collision
        """
        # lazy implementation, not tested 
        for vertex in self.vertices:
            if other.is_point_inside(vertex):
                return True
        for vertex in other.vertices:
            if self.is_point_inside(vertex):
                return True
        return False

    def is_point_inside(self, point: Point) -> bool:
        """
        Check if a given point is inside the brush.

        Args:
        - point (Point): The point to check.
        """
        for face in self.faces:
            if face.plane.normal.dot(point.as_vector()) + face.plane.d > 0:
                return False
        return True


    #TODO: return new brush from vertices; calc volume; flip h/v; check if 2 brushes share face planes