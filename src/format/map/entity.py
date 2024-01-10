from dataclasses import (dataclass,
                        field
                        )
from typing import Union, List

from format.map.brush import Brush
from format.map.face import Face
from utils.math.point import Point

@dataclass
class Entity:

    properties: dict = field(default_factory=dict)
    brushes: List[Brush] = field(default_factory=list)
    id: int = 0
    brush_counter: int = 0

    def __repr__(self) -> str:
        return f"{self.properties} {self.brushes} \n"

    def __iter__(self):
        """Return an iterator over the entity's brushes.
        
        Raises:
            - TypeError: If the entity is a point entity

        Example:
        >>> # Traditional syntax
        >>> for brush in entity.brushes:
                # Your logic...
        >>>
        >>> # New alternative syntax
        >>> for brush in entity:
                # Your logic...
        """
        if self.is_brush_entity:
            yield from (self.brushes)
        elif self.classname == 'worldspawn':
            yield from (self.brushes)
        #raise NotImplementedError(f"Iterate over point entity is not possible")
        
    def __setitem__(self, __key: str, __value: str) -> None:
        """
        Set an item in the entity's property dictionary.

        Args:
            - key (str): The name of the property.
            - value (str): The value to set.

        Example:
        >>> # Traditional syntax
        >>> entity.properties['classname'] = 'light'
        >>>
        >>> # New alternative syntax
        >>> entity['classname'] = 'light'
        """
        self.properties[__key] = __value
    
    def __getitem__(self, __key: str) -> str:
        """
        Get the value of a key property.

        Args:
            - key (str): The name of the property.

        Returns:
            - str: The value of the property.

        Example:
        >>> entity = Entity(properties={'classname': 'func_plat'})
        
        >>> # Traditional syntax
        >>> old_way = entity.properties['classname']
        >>> print(old_way)
        func_plat

        >>> # New alternative syntax
        >>> new_way = entity['classname']
        >>> print(new_way)
        func_plat
        """
        return self.properties[__key]
    
    def __contains__(self, __key: str) -> bool:
        """
        Check if a key is present in the entity's property dictionary.

        Args:
            - key (str): The name of the property.

        Returns:
            - bool: True if the property is present, False otherwise.

        Example:
        >>> entity = Entity(properties={'classname': 'func_plat', 'speed': '50'})
        >>> # Traditional syntax
        >>> 'speed' in entity.properties:
        True
        >>> 
        >>> # New alternative syntax
        >>> 'speed' in entity:
        True
        """
        if __key in self.properties:
            return True
        return False

    def __eq__(self, other):
        """
        Compare the entity with another object (or string for checking classname).

        Args:
            - other (str or Entity): The object to compare with.

        Returns:
            - bool: True if the classnames match, False otherwise.

        Example:
        >>> entity1 = Entity(properties={'classname': 'func_plat'})

        >>> # Traditional syntax
        >>> entity1.properties['classname'] == 'func_plat'
        True

        >>> # Using `classname` @property
        >>> entity1.classname == 'func_plat'
        True

        >>> # New alternative syntax
        >>> entity1 == 'func_plat'
        True
        """
        if isinstance(other, str):
            return self.classname == other
        elif isinstance(other, Entity):
            return self.properties == other.properties and self.brushes == other.brushes
        return False

    @property
    def classname(self) -> str:
        """Get the classname value of the entity

        Raises:
            - KeyError: If the 'classname' key is not found in the entity properties
            - ValueError: If the 'classname' value is not found in the entity properties
        """
        try:
            classname_value = self.properties.get('classname')
            if classname_value:
                return classname_value
            else:
                raise ValueError(f"Entity N°{self.id}: 'classname' value not found")
        except KeyError:
            raise KeyError(f"Entity N°{self.id}: key 'classname' not found")

    @property
    def origin(self) -> Union[Point, None]:
        """Get the 'origin' property of the entity

        Raises:
            - ValueError: If the origin is not found or has an invalid format.
        """
        if self.is_point_entity:
            origin_value = self.properties.get('origin')
            if origin_value is not None:
                values = str(origin_value).split()
                try:
                    x, y, z = map(float, values)
                    return Point(x, y, z)
                except ValueError:
                    raise ValueError(f'Entity N°{self.id}: Invalid origin format "{origin_value}"')
            else:
                raise ValueError(f"Entity N°{self.id}: Origin not found")
            
        elif self.is_brush_entity:
            brush_origins = [brush.centroid() for brush in self.brushes]
            return Point(sum(p.x for p in brush_origins) / len(brush_origins),
                         sum(p.y for p in brush_origins) / len(brush_origins),
                         sum(p.z for p in brush_origins) / len(brush_origins))

    @property
    def is_point_entity(self) -> bool:
        """Check if the entity is a point entity

        Raises:
            - KeyError: If the key 'classname' is not found in the entity properties
        """
        if self.classname:
            return bool(self.classname == 'worldspawn' or not self.brushes)
        else:
            raise KeyError(f"Entity N°{self.id}: key 'classname' not found")

    @property
    def is_brush_entity(self) -> bool:
        """Check if the entity is a brush entity

        Raises:
            - KeyError: If the 'classname' property is not found in the entity
        """
        if self.classname:
            return bool(self.classname != 'worldspawn' and self.brushes)
        else:
            raise KeyError(f"Entity N°{self.id}: 'classname' not found")

    @property
    def faces(self) -> list[Face]:
        """Get a list of faces associated with the entity

        Raises:
            - TypeError: If the entity is a point entity
        """
        if self.is_brush_entity or self.classname == 'worldspawn':
            return [face for brush in self.brushes for face in brush.faces]
        else:
            raise TypeError(f"Entity N°{self.id}: Point entities do not have faces")

    @property
    def vertices(self) -> list[Point]:
        """Get a list of vertices associated with the entity

        Raises:
            - TypeError: If the entity is a point entity.
        """
        verts = []
        if self.is_brush_entity or self.classname == 'worldspawn':
            for brush in self.brushes:
                verts.extend(brush.vertices)
            return verts
        else:
            raise TypeError(f"Entity N°{self.id}: Point entities do not have vertices")

    def add_brush(self, *args: Union[Brush, List[Brush]]) -> None:
        """Add brushes to the entity

        Args:
            - *args (Brush or list[Brush]): Brush(es) to add

        Raises:
            - TypeError: If the input is not a Brush or a list of Brushes
        """
        for arg in args:
            brush_list = arg if isinstance(arg, list) else [arg]
            for brush in brush_list:
                if isinstance(brush, Brush):
                    brush.id = self.brush_counter
                    self.brush_counter += 1
                    self.brushes.append(brush)
                else:
                    raise TypeError(f"Expected <class {Brush.__name__}> but got {type(brush).__name__}")
