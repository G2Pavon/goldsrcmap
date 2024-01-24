from __future__ import annotations

from utils.math.vector import Vector3
from math import radians, cos, sin

class Matrix3x3:
    
    """
    3x3 Matrix

    Used for transformations
    """

    def __init__(self, row1: list[float], row2: list[float], row3: list[float]) -> None:
        if len(row1)  != 3 or len(row1)  != 3 or len(row1) != 3:
            raise ValueError("Matrix must be 3x3")

        self.a11, self.a12, self.a13 = row1[0], row1[1], row1[2]
        self.a21, self.a22, self.a23 = row2[0], row2[1], row2[2]
        self.a31, self.a32, self.a33 = row3[0], row3[1], row3[2]

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        CLASSMETHOD                               ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
        
    @classmethod
    def rotation_x(cls, angle: float) -> Matrix3x3:
        if not isinstance(angle, (int, float)):
            raise TypeError(f"Unsupported type for angle: {type(angle)}")
        theta = radians(angle)

        return cls([1,     0     ,           0],
                   [0, cos(theta), -sin(theta)],
                   [0, sin(theta), cos(theta)])
    
    @classmethod
    def rotation_y(cls, angle: float) -> Matrix3x3:
        if not isinstance(angle, (int, float)):
            raise TypeError(f"Unsupported type for angle: {type(angle)}")
        theta = radians(angle)

        return cls([cos(theta),  0, sin(theta)],
                   [    0     ,  1,     0     ],
                   [-sin(theta), 0, cos(theta)])
        
    @classmethod
    def rotation_z(cls, angle: float) -> Matrix3x3:
        if not isinstance(angle, (int, float)):
            raise TypeError(f"Unsupported type for angle: {type(angle)}")
        theta = radians(angle)

        return cls([cos(theta), -sin(theta), 0],
                   [sin(theta), cos(theta) , 0],
                   [0         ,     0      , 1])

    @classmethod
    def rotation_xyz(cls, phi: float, theta: float, psi: float) -> Matrix3x3:
        if not isinstance(phi, (int, float)):
            raise TypeError(f"Unsupported type for phi angle: {type(phi)}")
        if not isinstance(theta, (int, float)):
            raise TypeError(f"Unsupported type for theta angle: {type(theta)}")
        if not isinstance(psi, (int, float)):
            raise TypeError(f"Unsupported type for psi angle: {type(psi)}")
        
        return Matrix3x3.rotation_z(psi) @ Matrix3x3.rotation_y(theta) @ Matrix3x3.rotation_x(phi)

    @classmethod
    def rotate_around_axis(cls, angle: float, axis: Vector3) -> Matrix3x3:
        if not isinstance(angle, (int, float)):
            raise TypeError(f"Unsupported type for angle: {type(angle)}")
        angle = radians(angle)
        c = cos(angle)
        s = sin(angle)
        C = 1 - c
        axis_x, axis_y, axis_z = axis.normalized().components()

        return cls([c+axis_x**2*C           , axis_x*axis_y*C-axis_z*s, axis_x*axis_z*C+axis_y*s],
                   [axis_y*axis_x*C+axis_z*s, c+axis_y**2*C           , axis_y*axis_z*C-axis_x*s], 
                   [axis_z*axis_x*C-axis_y*s, axis_z*axis_y*C+axis_x*s, c+axis_z**2*C           ])

    @classmethod
    def reflection_xy(cls) -> Matrix3x3:
        return cls([1, 0, 0],
                   [0, 1, 0],
                   [0, 0, -1])
    
    @classmethod
    def reflection_xz(cls) -> Matrix3x3:
        return cls([1,  0, 0],
                   [0, -1, 0],
                   [0,  0, 1])
    
    @classmethod
    def reflection_yz(cls) -> Matrix3x3:
        return cls([-1, 0, 0],
                   [ 0, 1, 0],
                   [ 0, 0, 1])
    
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def inv(self) -> Matrix3x3:
        det = self.det()

        if det == 0:
            raise ValueError("Matrix is singular")

        adjugate = Matrix3x3(
            [self.a22 * self.a33 - self.a23 * self.a32,
            self.a13 * self.a32 - self.a12 * self.a33,
            self.a12 * self.a23 - self.a13 * self.a22,
            ],
            [
            self.a23 * self.a31 - self.a21 * self.a33,
            self.a11 * self.a33 - self.a13 * self.a31,
            self.a13 * self.a21 - self.a11 * self.a23,
            ],
            [
            self.a21 * self.a32 - self.a22 * self.a31,
            self.a12 * self.a31 - self.a11 * self.a32,
            self.a11 * self.a22 - self.a12 * self.a21
            ]
        )

        return (1 / det) * adjugate

    def det(self) -> float:
        return (
            self.a11 * (self.a22 * self.a33 - self.a23 * self.a32) +
            self.a12 * (self.a21 * self.a33 - self.a23 * self.a31) +
            self.a13 * (self.a21 * self.a32 - self.a22 * self.a31)
        )
    
    def trace(self) -> float:
        return self.a11 + self.a22 + self.a33
    

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    def __mul__(self, scalar: float) -> Matrix3x3:
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Unsupported type for multiplication by a scalar: {type(scalar)}")
    
        a11, a12, a13 = self.a11 * scalar, self.a12 * scalar, self.a13 * scalar
        a21, a22, a23 = self.a21 * scalar, self.a22 * scalar, self.a23 * scalar
        a31, a32, a33 = self.a31 * scalar, self.a32 * scalar, self.a33 * scalar

        return Matrix3x3([a11, a12, a13],
                         [a21, a22, a23],
                         [a31, a32, a33])
    
    __rmul__ = __mul__
    
    def __matmul__(self, other: Vector3 | Matrix3x3) -> Vector3 | Matrix3x3:
        if not isinstance(other, (Vector3, Matrix3x3)):
            raise TypeError(f"Unsupported type for matrix multiplication: {type(other)}")
        elif isinstance(other, Vector3):
            x = self.a11 * other.x + self.a12 * other.y + self.a13 * other.z
            y = self.a21 * other.x + self.a22 * other.y + self.a23 * other.z
            z = self.a31 * other.x + self.a32 * other.y + self.a33 * other.z
            result = Vector3(x, y, z)
        
        elif isinstance(other, Matrix3x3):
            a11 = self.a11 * other.a11 + self.a12 * other.a21 + self.a13 * other.a31
            a12 = self.a11 * other.a12 + self.a12 * other.a22 + self.a13 * other.a32
            a13 = self.a11 * other.a13 + self.a12 * other.a23 + self.a13 * other.a33

            a21 = self.a21 * other.a11 + self.a22 * other.a21 + self.a23 * other.a31
            a22 = self.a21 * other.a12 + self.a22 * other.a22 + self.a23 * other.a32
            a23 = self.a21 * other.a13 + self.a22 * other.a23 + self.a23 * other.a33

            a31 = self.a31 * other.a11 + self.a32 * other.a21 + self.a33 * other.a31
            a32 = self.a31 * other.a12 + self.a32 * other.a22 + self.a33 * other.a32
            a33 = self.a31 * other.a13 + self.a32 * other.a23 + self.a33 * other.a33

            result = Matrix3x3([a11, a12, a13], [a21, a22, a23], [a31, a32, a33])
        return result