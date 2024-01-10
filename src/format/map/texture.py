from utils.math.point import Point
from utils.math.vector import Vector3
from utils.math.matrix import Matrix3x3

class Texture:

    def __init__(self, name, u_axis, u_offset, v_axis, v_offset, rotation, u_scale, v_scale) -> None:
        self.name: str = str(name).upper()
        self.u_axis: Vector3 = u_axis
        self.u_offset: float = u_offset
        self.v_axis: Vector3 = v_axis
        self.v_offset: float = v_offset
        self.rotation: float = rotation
        self.u_scale: float = u_scale
        self.v_scale: float = v_scale
        #TODO:self.width and self.heigth (need WAD parsing)

    @property
    def normal(self) -> Vector3:
        return self.u_axis.cross(self.v_axis)
    
    def _update_offset(self, displacement: Vector3):
        # lazy implementation
        # doesn't works when displacemente isn't referenced to the origin (0,0,0)
        self.u_offset -= displacement.dot(self.u_axis)/self.u_scale
        self.v_offset -= displacement.dot(self.v_axis)/self.v_scale

    def _rotate_uv_x(self, angle: float) -> None:
        self._rotate_uv(Matrix3x3.rotation_x(angle))

    def _rotate_uv_y(self, angle: float) -> None:
        self._rotate_uv(Matrix3x3.rotation_y(angle))

    def _rotate_uv_z(self, angle: float) -> None:
        self._rotate_uv(Matrix3x3.rotation_z(angle))

    def _rotate_uv_around_axis(self, angle: float, axis: Vector3) -> None:
        self._rotate_uv(Matrix3x3.rotate_around_axis(angle, axis))

    def _rotate_uv(self, transformation: Matrix3x3):
        self.u_axis = transformation @ self.u_axis
        self.v_axis = transformation @ self.v_axis

    def __str__(self):
        return f"{self.name} [ {self.u_axis} {self.u_offset} ] [ {self.v_axis} {self.u_offset} ] {self.rotation} {self.u_scale} {self.v_scale}"