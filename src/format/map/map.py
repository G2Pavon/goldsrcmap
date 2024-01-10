from typing import Union, List
from copy import deepcopy

from format.map.entity import Entity
from format.map.brush import Brush
from format.map.face import Face

class Map:
    """
    Represents the .map file with its entities stored in a list
    """

    def __init__(self, filename=None):
        self.name = filename
        self.path = ''
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
    def brushes(self) -> Union[list[Brush],None]:
        """Get a list of all brushes in the map

        Raises:
            ValueError: If there are no brushes
        """
        brush_lst = [brush for entity in self for brush in entity]
        if not brush_lst:
            return None
        return brush_lst
    
    @property
    def brush_entities(self) -> Union[list[Entity],None]: 
        """Get a list of brush entities

        Raises:
            ValueError: If there are no entities
        """
        if self.entities:
            ent_lst = [entity for entity in self if entity.is_brush_entity]
            if not ent_lst:
                return None
            return ent_lst
        else:
            raise ValueError("No entities on the map")

    @property
    def faces(self)  -> Union[list[Face],None]:
        """Get a list of all faces in the map

        Raises:
            ValueError: If there are no brush faces
        """
        face_lst = [face for entity in self for brush in entity for face in brush]
        if not face_lst:
            return None
        return face_lst
    
    @property
    def point_entities(self) -> Union[list[Entity],None]: 
        """Get a list of point entities

        Raises:
            ValueError: If there are no entities
        """
        if self.entities:
            ent_lst = [entity for entity in self if entity.is_point_entity]
            if not ent_lst:
                return None
            return ent_lst
        else:
            raise ValueError("There are no entities on the map")
    
    @property
    def wad(self):
        return self.worldspawn['wad']
    
    @wad.setter
    def wad(self, wads: str):
        self.worldspawn['wad'] = wads
        
    @property
    def worldspawn(self) -> Entity:
        """Get the worldspawn entity.

        Raises:
            ValueError: If there are no entities or the worldspawn entity is not at index 0 in the map entity list.
        """
        if self.entities:
            if self.entities[0].classname == 'worldspawn':
                return self.entities[0]
        raise ValueError(f"Worldspawn entity not found. There is something wrong with the map file, should be at the beginning.")

    def add_entity(self, *args: Union[Entity, List[Entity]]) -> None:
        """Add entities to the map

        Args:
            *args (Entity or list[Entity] ): Entities to add

        Raises:
            TypeError: If the input is not an Entity or a list of Entities.
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
        """Add brushes to the worldspawn entity

        Args:
            *args (Brush or list[Brush] ): Brushes to add

        Raises:
            TypeError: If the input is not a Brush or a list of Brushes
        """
        for arg in args:
            brush_list = arg if isinstance(arg, list) else [arg]
            for brush in brush_list:
                if isinstance(brush, Brush):
                    self.worldspawn.add_brush(brush)
                else:
                    raise TypeError(f"Expected <class {Brush.__name__}> but got {type(brush).__name__}")