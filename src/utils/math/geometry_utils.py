from format.map.face import Face

from .point import Point
from .edge import Edge
from .vector import Vector3
from .plane import Plane

def is_parallel(obj1: Vector3|Edge|Plane|Face, obj2: Vector3|Edge|Plane|Face) -> bool:
    if isinstance(obj1, Vector3):
        if isinstance(obj2, Vector3):
            return obj1.is_parallel(obj2)
        elif isinstance(obj2, Edge):
            return obj1.is_parallel(obj2.direction1)
        elif isinstance(obj2, Plane):
            return obj1.is_perpendicular(obj2.normal)
        elif isinstance(obj2, Face):
            return obj1.is_perpendicular(obj2.normal)

    elif isinstance(obj1, Edge):
        if isinstance(obj2, Vector3):
            return obj1.direction1.is_parallel(obj2)
        elif isinstance(obj2, Edge):
            return obj1.direction1.is_parallel(obj2.direction1)
        elif isinstance(obj2, Plane):
            return obj1.direction1.is_perpendicular(obj2.normal)
        elif isinstance(obj2, Face):
            return obj1.direction1.is_perpendicular(obj2.normal)

    elif isinstance(obj1, Plane):
        if isinstance(obj2, Vector3):
            return obj1.normal.is_perpendicular(obj2)
        elif isinstance(obj2, Edge):
            return obj1.normal.is_perpendicular(obj2.direction1)
        elif isinstance(obj2, Plane):
            return obj1.normal.is_parallel(obj2.normal)
        elif isinstance(obj2, Face):
            return obj1.normal.is_parallel(obj2.normal)
    
    elif isinstance(obj1, Face):
        if isinstance(obj2, Vector3):
            return obj1.normal.is_perpendicular(obj2)
        if isinstance(obj2, Edge):
            return obj1.normal.is_perpendicular(obj2.direction1)
        if isinstance(obj2, Plane):
            return obj1.normal.is_parallel(obj2.normal)
        if isinstance(obj2, Face):
            return obj1.normal.is_parallel(obj2.normal)

    raise TypeError(f"Unsupported types for parallel check: {type(obj1)}, {type(obj2)}")

def is_perpendicular(obj1: Vector3|Edge|Plane|Face, obj2: Vector3|Edge|Plane|Face) -> bool:
    try:
        return not is_parallel(obj1, obj2)
    except TypeError as e:
        raise TypeError(f"Unsupported types for perpendicular check: {type(obj1)}, {type(obj2)}") from e