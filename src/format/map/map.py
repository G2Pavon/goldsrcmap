from typing import Union, List
from copy import deepcopy

from format.map.entity import Entity
from format.map.brush import Brush
from format.map.face import Face

class Map:
    """
    Represents the .map file with its entities stored in a list.

    Attributes:
        name (str): The filename of the map.
        path (str): The path to the map file.
        entities (List[Entity]): List of entities in the map.
        entity_counter (int): Counter for assigning unique IDs to entities.
    """

    def __init__(self, filename=None):
        self.name = filename
        self.path = '' # currently unused
        self.entities: list[Entity] = []
        self.entity_counter: int = 0

        #Create from scratch
        if not self.name:
            world = Entity()
            world.properties = {
                "classname": "worldspawn",
                "mapversion": "220",           # Valve220 texture projection
                "wad": "",                     # Wad path
                "message": "",                 # Map Description/Title
                "skyname": "",                 # Environment Map
                "light": 0,                    # Default light level
                "WaveHeight": "",              # Default Wave Height
                "MaxRange": "4096",            # Max viewable distance
                "origin": "0 0 0",
            }
            self.add_entity(world)
    
    def __str__(self) -> str:
        """Return a string representation of the map."""
        return f"{self.entities}"
    
    def __iter__(self): 
        """Return an iterator over the Map entities

        Example:
        >>> # Traditional syntax
        >>> for entity in self.entities:
                # Your logic...
        >>>
        >>> # New alternative syntax
        >>> for entity in self:
                # Your logic...
        """
        return iter(self.entities)
    
    @property
    def brushes(self) -> Union[List[Brush], None]:
        """Get a list of all brushes"""
        brush_list = [brush for entity in self.entities for brush in entity.brushes]
        return brush_list or None
    
    @property
    def brush_entities(self) -> Union[list[Entity],None]: 
        """Get a list of all brush entities"""
        if self.entities:
            return [entity for entity in self.entities if entity.is_brush_entity]
        return None

    @property
    def faces(self)  -> Union[list[Face],None]:
        """Get a list of all brush faces"""
        face_list = [face for entity in self.entities for brush in entity.brushes for face in brush.faces]
        return face_list or None
    
    @property
    def point_entities(self) -> Union[list[Entity],None]: 
        """Get a list of all point entities"""
        if self.entities:
            return [entity for entity in self.entities if entity.is_point_entity]
        return None
    
    @property
    def wad(self) -> str:
        """Return the used wads"""
        return self.worldspawn.properties.get('wad', '')
    
    @wad.setter
    def wad(self, wads: str) -> None:
        """Set the WAD path in the worldspawn entity

        Args:
            wads (str): The WAD path.
        Example:
        >>> # One wad
        >>> self.wad = 'path/to/file1.wad'
        >>> # Multi wads
        >>> self.wad = 'path/to/file2.wad; path/to/file'
        """
        self.worldspawn.properties['wad'] = wads
        
    @property
    def worldspawn(self) -> Union[Entity, None]:
        """Get the worldspawn entity.

        Raises:
            ValueError: If the worldspawn entity is not at index 0 in the map entity list.
        """
        if self.entities:
            if self.entities[0].classname == 'worldspawn':
                return self.entities[0]
            raise ValueError(f"Worldspawn entity not found. There is something wrong with the map")
        return None
        

    def add_entity(self, *args: Union[Entity, List[Entity]]) -> None:
        """Add entities to map

        Args:
            *args (Entity or list[Entity]): Entities to add

        Raises:
            TypeError: If the input is not an Entity
        """
        for arg in args:
            ent_list = arg if isinstance(arg, list) else [arg]
            for entity in ent_list:
                if isinstance(entity, Entity):
                    entity.id = self.entity_counter
                    self.entity_counter += 1
                    self.entities.append(entity)
                else:
                    raise TypeError(f"Expected <class {Entity.__name__}> but got {type(entity).__name__}")
    
    def add_brush(self, *args: Union[Brush, List[Brush]]) -> None:
        """Add brushes to worldspawn entity

        Args:
            *args (Brush or list[Brush] ): Brushes to add

        Raises:
            TypeError: If the input is not a Brush
        """
        for arg in args:
            brush_list = arg if isinstance(arg, list) else [arg]
            for brush in brush_list:
                if isinstance(brush, Brush):
                    self.worldspawn.add_brush(brush)
                else:
                    raise TypeError(f"Expected <class {Brush.__name__}> but got {type(brush).__name__}")
                
    def copy(self):
        """Return a deepcopy of the current map instance, useful for backup"""
        return deepcopy(self)