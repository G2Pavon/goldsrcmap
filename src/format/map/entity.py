from format.map.brush import Brush
from format.map.face import Face
from utils.math.point import Point


class Entity:
    """
    Represents an entity in a .map file with properties and associated brushes.

    Attributes:
        properties (dict): Dictionary of entity properties.
        brushes (List[Brush]): List of brushes associated with the entity.
        id (int): Unique identifier for the entity.
        brush_counter (int): Counter for assigning unique IDs to brushes.
    """
    def __init__(self, classname: str|None=None, origin_or_brushes: Point|list[float]|Brush|list[Brush]|None=None, properties: dict|None=None):
        self._id: int = 0
        self.properties: dict = {}
        self.brushes: list[Brush] = []
        self.brush_counter: int = 1
        
        # TODO: Remove default values for 'classname' and 'origin_or_brushes' parameters to make them required during entity initialization. 
        # Requirements: Refactor load_map()
        if classname:
            self['classname'] = classname
        
        if isinstance(origin_or_brushes, Point):
            self['origin'] = f'{origin_or_brushes.x} {origin_or_brushes.y} {origin_or_brushes.z}'
        elif isinstance(origin_or_brushes, list) and len(origin_or_brushes)==3 and all(isinstance(i, (int, float)) for i in origin_or_brushes):
            self['origin'] = f'{origin_or_brushes[0]} {origin_or_brushes[1]} {origin_or_brushes[2]}'
        elif isinstance(origin_or_brushes, Brush):
            self.add_brush(origin_or_brushes)
        elif isinstance(origin_or_brushes, list) and all(isinstance(brush, Brush) for brush in origin_or_brushes):
            self.add_brush(*origin_or_brushes)
        if properties is not None:
            for k, v in properties.items():
                self.properties[k] = v

        self.in_map_instance = False


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    @property
    def id(self) -> int | None:
        if not self.in_map_instance:
            return None
        return self._id
    
    @property
    def classname(self) -> str:
        """Get the classname value of the entity."""
        classname_value = self['classname']
        if classname_value:
            return classname_value
        else:
            raise ValueError(f"Entity N°{self._id}: 'classname' value not found")

    @property
    def origin(self) -> Point|None:
        """Get the origin of the entity"""
        if self.is_point_entity:
            origin_value = self['origin']
            try:
                x, y, z = map(float, str(origin_value).split())
                return Point(x, y, z)
            except SyntaxError:
                raise SyntaxError(f'Entity N°{self._id}: Invalid origin format "{origin_value}"')

        elif self.is_brush_entity:
            brush_origins = [brush.centroid() for brush in self.brushes]
            return Point(sum(p.x for p in brush_origins) / len(brush_origins),
                         sum(p.y for p in brush_origins) / len(brush_origins),
                         sum(p.z for p in brush_origins) / len(brush_origins))

    @property
    def is_point_entity(self) -> bool:
        """Check if the entity is a point entity"""
        if 'classname' not in self.properties:
            raise KeyError(f"Entity N°{self._id}: key 'classname' not found")
        return self['classname'] == 'worldspawn' or not self.brushes

    @property
    def is_brush_entity(self) -> bool:
        """Check if the entity is a brush entity"""
        if 'classname' not in self.properties:
            raise KeyError(f"Entity N°{self._id}: 'classname' not found")
        return bool(self['classname'] != 'worldspawn' and self.brushes)

    @property
    def faces(self) -> list[Face]:
        """Get a list of faces associated with the entity"""
        if self.is_brush_entity or self['classname'] == 'worldspawn':
            return [face for brush in self.brushes for face in brush.faces]

    @property
    def vertices(self) -> list[Point]:
        """Get a list of vertices associated with the entity."""
        if self.is_brush_entity or self['classname'] == 'worldspawn':
            return [vertex for brush in self.brushes for vertex in brush.vertices]


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def add_brush(self, *args: Brush|list[Brush]) -> None:
        """Add brush(es) to entity"""
        for arg in args:
            brush_list = arg if isinstance(arg, list) else [arg]
            for brush in brush_list:
                if isinstance(brush, Brush):
                    brush._id = self.brush_counter
                    self.brush_counter += 1
                    self.brushes.append(brush)
                else:
                    raise TypeError(f"Expected <class {Brush.__name__}> but got {type(brush).__name__}")

    def move_by(self, x: float, y: float, z: float):
        """Moves the entity by a specified offsets"""
        if self.is_brush_entity:
            for brush in self:
                brush.move_by(x, y, z)
        elif self.is_point_entity:
            current = self.origin
            x += current.x
            y += current.y
            z += current.z
            self['origin'] = f'{x} {y} {z}'
    
    def move_to(self, x: float, y: float, z: float, centroid: bool=True, bbox: bool=False):
        """Move the entity to a specific coordinate"""
        if self.is_brush_entity:
            for brush in self:
                brush.move_to(x, y, z, centroid, bbox)
        elif self.is_point_entity:
            self['origin'] = f'{x} {y} {z}'


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __repr__(self) -> str:
        return f"{self.properties} {self.brushes} \n"

    def __iter__(self):
        """Return an iterator over the entity's brushes"""
        return iter(self.brushes)
        
    def __setitem__(self, key: str, value: str) -> None:
        """Set an item in the entity's property dictionary"""
        self.properties[key] = value
        
    def __getitem__(self, key: str) -> str:
        """Get the value of a key property"""
        try:
            return self.properties[key]
        except KeyError:
            raise KeyError(f"Entity N°{self._id}: Property '{key}' not found in entity properties")

    def __contains__(self, key: str) -> bool:
        """Check if a key is present in the entity's property dictionary"""
        return key in self.properties

    def __eq__(self, other):
        """Compare the entity with another object (or string for checking classname)"""
        if isinstance(other, str):
            return self.classname == other
        elif isinstance(other, Entity):
            return self.properties == other.properties and self.brushes == other.brushes
        return False