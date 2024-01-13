from typing import Union, List

from format.map.brush import Brush
from format.map.face import Face
from format.map.texture import Texture
from .math.point import Point
from .math.vector import Vector3
from .math.plane import Plane
import math


class BrushGenerator():
    """
    Class to generate primtive brush.
    """

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        STATICMETHOD                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    @staticmethod
    def cuboid(w: float, l: float, h: float, position: Union[Point, list[float]], center: bool=False, texture: str="null") -> Brush:
        x, y, z = position.components() if isinstance(position, Point) else position[:3]

        lst_textures = [
            Texture(name=texture.upper(), u_axis=Vector3(1, 0, 0), u_offset=0.0, v_axis=Vector3(0, -1, 0),
                    v_offset=0.0, rotation=0.0, u_scale=1.0, v_scale=1.0)
            for _ in range(6)
        ]

        top = Face(Plane(Point(x, y, z + h), Point(x, y + l, z + h), Point(x + w, y + l, z + h)), lst_textures[0])
        top.texture.u_axis, top.texture.v_axis = Vector3(1, 0, 0), Vector3(0, -1, 0)

        bottom = Face(Plane(Point(x, y + l, z), Point(x, y, z), Point(x + w, y, z)), lst_textures[1])
        bottom.texture.u_axis, bottom.texture.v_axis = Vector3(1, 0, 0), Vector3(0, -1, 0)

        front = Face(Plane(Point(x + w, y + l, z), Point(x + w, y + l, z + h), Point(x, y + l, z + h)), lst_textures[2])
        front.texture.u_axis, front.texture.v_axis = Vector3(-1, 0, 0), Vector3(0, 0, -1)

        back = Face(Plane(Point(x + w, y, z + h), Point(x + w, y, z), Point(x, y, z)), lst_textures[3])
        back.texture.u_axis, back.texture.v_axis = Vector3(1, 0, 0), Vector3(0, 0, -1)

        left = Face(Plane(Point(x, y, z), Point(x, y + l, z), Point(x, y + l, z + h)), lst_textures[4])
        left.texture.u_axis, left.texture.v_axis = Vector3(0, -1, 0), Vector3(0, 0, -1)

        rigth = Face(Plane(Point(x + w, y + l, z), Point(x + w, y, z), Point(x + w, y, z + h)), lst_textures[5])
        rigth.texture.u_axis, rigth.texture.v_axis = Vector3(0, 1, 0), Vector3(0, 0, -1)

        brush = Brush()
        brush.add_face(top, bottom, front, back, left, rigth)

        for face in brush.faces:
            face.texture._update_offset(Vector3(x, y, z))

        if center:
            new_position = Point(x,y,z)-brush.bounding_box_origin()
            brush.move_by(new_position.x, new_position.y, new_position.z)

        return brush

    @staticmethod
    def room(width: float, height: float, length: float, thickness: float = 1.0, position: Union[Point, List[float]] = Point(0,0,0), center: bool=False, texture: str="SKY") -> List[Brush]:
        if isinstance(position, list):
            position = Point(position[0], position[1], position[2])

        x, y, z = (Vector3(*position) - Vector3(width / 2, height / 2, length / 2)).components() if center else (0, 0, 0)

        orientations = [(width, length, thickness, [x, y, z]), #FLOOR
                        (width, length, thickness, [x, y, z + height - thickness]), #ROOF
                        (width, thickness, height - 2 * thickness, [x, y, z + thickness]), #BACK WALL
                        (width, thickness, height - 2 * thickness, [x, y + length - thickness, z + thickness]), #FRONT WALL
                        (thickness, length - 2 * thickness, height - 2 * thickness, [x, y + thickness, z + thickness]), #LEFT WALL
                        (thickness, length - 2 * thickness, height - 2 * thickness, [x + width - thickness, y + thickness, z + thickness])] #RIGHT WALL

        room = [BrushGenerator.cuboid(*params, texture=texture) for params in orientations]

        return room

    @staticmethod
    def sphere(radius: float, segments: float,position: Union[Point, list[float]], texture: str="null") -> Brush:
        x, y, z = position.components() if isinstance(position, Point) else position[:3]

        lst_textures = [
            Texture(name=texture.upper(), u_axis=Vector3(1, 0, 0), u_offset=0.0, v_axis=Vector3(0, -1, 0),
                    v_offset=0.0, rotation=0.0, u_scale=1.0, v_scale=1.0)
            for _ in range(6)
        ]

        theta_segments = segments
        phi_segments = segments // 2

        faces = []

        for phi in range(phi_segments):
            for theta in range(theta_segments):
                phi0 = math.pi * phi / phi_segments
                phi1 = math.pi * (phi + 1) / phi_segments
                theta0 = 2 * math.pi * theta / theta_segments
                theta1 = 2 * math.pi * (theta + 1) / theta_segments

                # Vertices
                p00 = Point(x + radius * math.sin(phi0) * math.cos(theta0),
                            y + radius * math.sin(phi0) * math.sin(theta0),
                            z + radius * math.cos(phi0))
                p01 = Point(x + radius * math.sin(phi0) * math.cos(theta1),
                            y + radius * math.sin(phi0) * math.sin(theta1),
                            z + radius * math.cos(phi0))
                p10 = Point(x + radius * math.sin(phi1) * math.cos(theta0),
                            y + radius * math.sin(phi1) * math.sin(theta0),
                            z + radius * math.cos(phi1))
                p11 = Point(x + radius * math.sin(phi1) * math.cos(theta1),
                            y + radius * math.sin(phi1) * math.sin(theta1),
                            z + radius * math.cos(phi1))

                u0 = theta / theta_segments
                #u1 = (theta + 1) / theta_segments
                v0 = phi / phi_segments
                #v1 = (phi + 1) / phi_segments
                
                face = Face(Plane(p00, p01, p11), lst_textures[0])
                face.texture.u_axis, face.texture.v_axis = Vector3(1, 0, 0), Vector3(0, -1, 0)
                face.texture.u_offset, face.texture.v_offset = u0, v0
                face.texture.u_scale, face.texture.v_scale = (u1 - u0), (v1 - v0)
                faces.append(face)

                face = Face(Plane(p00, p11, p10), lst_textures[1])
                face.texture.u_axis, face.texture.v_axis = Vector3(1, 0, 0), Vector3(0, -1, 0)
                face.texture.u_offset, face.texture.v_offset = u0, v0
                face.texture.u_scale, face.texture.v_scale = 1, 1 #(u1 - u0), (v1 - v0)
                faces.append(face)

        brush = Brush()
        brush.faces = faces

        return brush

    @staticmethod
    def tetrahedron(edge_length: float, position: Union[Point, list[float]], texture: str="null") -> Brush:
        x, y, z = position.components() if isinstance(position, Point) else position[:3]

        lst_textures = [
            Texture(name=texture.upper(), u_axis=Vector3(1, 0, 0), u_offset=0.0, v_axis=Vector3(0, -1, 0),
                    v_offset=0.0, rotation=0.0, u_scale=1.0, v_scale=1.0)
            for _ in range(4)
        ]

        # Base
        v0 = Point(x, y, z)
        v1 = Point(x + edge_length, y, z)
        v2 = Point(x, y - edge_length, z)
        
        # Centroid of the base
        centroid = Point((v0.x + v1.x + v2.x) / 3, (v0.y + v1.y + v2.y) / 3, (v0.z + v1.z + v2.z) / 3)

        height = -(edge_length)/4
        v3 = Point(centroid.x, centroid.y, centroid.z + (2 / 3) * height)

        faces = [
            Face(Plane(v0, v1, v2), lst_textures[0]),
            Face(Plane(v0, v2, v3), lst_textures[1]),
            Face(Plane(v0, v3, v1), lst_textures[2]),
            Face(Plane(v1, v3, v2), lst_textures[3])
        ]

        brush = Brush()
        brush.faces = faces

        return brush
