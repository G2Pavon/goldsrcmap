from utils.math.point import Point
from utils.math.vector import Vector3
from utils.math.matrix import Matrix3x3

class Texture:
    """
    Represents a texture with properties like name, axes, offsets, rotation, and scales.

    Attributes:
      name: The name of the texture.
      u_axis: The U-axis vector of the texture.
      u_offset: The U-axis offset of the texture.
      v_axis: The V-axis vector of the texture.
      v_offset: The V-axis offset of the texture.
      rotation: The rotation angle of the texture.
      u_scale: The U-axis scale of the texture.
      v_scale: The V-axis scale of the texture.
    """

    def __init__(self, name, u_axis, u_offset, v_axis, v_offset, rotation, u_scale, v_scale) -> None:
        self.name: str = str(name).upper()
        self.u_axis: Vector3 = u_axis
        self.u_offset: float = u_offset
        self.v_axis: Vector3 = v_axis
        self.v_offset: float = v_offset
        self.rotation: float = rotation #TODO: update rotation value from uv axis rotations
        self.u_scale: float = u_scale
        self.v_scale: float = v_scale
        # TODO: self.width and self.height (need WAD parsing)


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    @property
    def normal(self) -> Vector3:
        """Return the normal vector of the texture"""
        return self.u_axis.cross(self.v_axis)


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def _rotate_uv_x(self, angle: float) -> None:
        """Rotate (in degrees) the texture around the X-axis"""
        self._rotate_uv(Matrix3x3.rotation_x(angle))

    def _rotate_uv_y(self, angle: float) -> None:
        """Rotate (in degrees) the texture around the Y-axis"""
        self._rotate_uv(Matrix3x3.rotation_y(angle))

    def _rotate_uv_z(self, angle: float) -> None:
        """Rotate (in degrees) the texture around the Z-axis"""
        self._rotate_uv(Matrix3x3.rotation_z(angle))

    def _rotate_uv_around_axis(self, angle: float, axis: Vector3) -> None:
        """Rotate (in degrees) the texture around a specified axis"""
        self._rotate_uv(Matrix3x3.rotate_around_axis(angle, axis))

    def _rotate_uv(self, transformation: Matrix3x3):
        """Apply a 3x3 matrix transformation to the texture axes"""
        self.u_axis = transformation @ self.u_axis
        self.v_axis = transformation @ self.v_axis

    def _update_offset(self, displacement: Vector3):
        """Update the texture offset based on a displacement vector"""
        # lazy implementation
        # doesn't work when displacement isn't referenced to the origin (0,0,0)
        self.u_offset -= displacement.dot(self.u_axis) / self.u_scale
        self.v_offset -= displacement.dot(self.v_axis) / self.v_scale


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __str__(self):
        """Return a string representation of the texture"""
        return f"{self.name} [ {self.u_axis} {self.u_offset} ] [ {self.v_axis} {self.u_offset} ] {self.rotation} {self.u_scale} {self.v_scale}"
