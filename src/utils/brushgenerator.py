from typing import Union, List

from format.map.brush import Brush
from format.map.face import Face
from format.map.texture import Texture
from .math.point import Point
from .math.vector import Vector3
from .math.plane import Plane

class BrushGenerator():
    """
    Class to generate primtive brush.
    """

    @staticmethod
    def cuboid(w: float, l: float, h: float, position: Union[Point, list[float]], center: bool=False, texture: str="null") -> Brush:
        if isinstance(position, Point):
            x, y, z = position.components()

        elif isinstance(position, list):
            x, y, z= position[0], position[1], position[2]

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

        room = [BrushGenerator.cuboid(*params) for params in orientations]

        for brush in room:
            brush.set_texture(texture)

        return room