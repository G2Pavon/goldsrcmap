from format.map.loader import load_map
from format.map.writer import save_map
def new_map():
    return Map()

from format.map.map import Map
from format.map.entity import Entity
from format.map.entity import Brush
from format.map.face import Face
from format.map.texture import Texture

from utils.math.point import Point
from utils.math.vector import Vector3
from utils.math.plane import Plane
from utils.math.edge import Edge

from utils.brushgenerator import BrushGenerator
from utils.entitygenerator import EntityGenerator
