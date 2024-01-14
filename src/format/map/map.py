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
    
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        PROPERTY                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    @property
    def brushes(self) -> list[Brush]:
        """Get a list of all brushes"""
        return [brush for entity in self.entities for brush in entity.brushes]
    
    @property
    def brush_entities(self) -> list[Entity]:
        """Get a list of all brush entities"""
        return [entity for entity in self.entities if entity.is_brush_entity]

    @property
    def faces(self)  -> list[Face]:
        """Get a list of all brush faces"""
        return [face for entity in self.entities for brush in entity.brushes for face in brush.faces]
    
    @property
    def point_entities(self) -> list[Entity]: 
        """Get a list of all point entities"""
        return [entity for entity in self.entities if entity.is_point_entity]
        
    @property
    def worldspawn(self) -> Union[Entity, None]:
        """Get the worldspawn entity"""
        if self.entities:
            if self.entities[0].classname == 'worldspawn':
                return self.entities[0]
            raise ValueError(f"Worldspawn entity not found. There is something wrong with the map")
        return None

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  
    def add_brush(self, *args: Union[Brush, List[Brush]]) -> None:
        """Add brushes to worldspawn entity"""
        for arg in args:
            brush_list = arg if isinstance(arg, list) else [arg]
            for brush in brush_list:
                if isinstance(brush, Brush):
                    self.worldspawn.add_brush(brush)
                else:
                    raise TypeError(f"Expected <class {Brush.__name__}> but got {type(brush).__name__}")
                
    def add_entity(self, *args: Union[Entity, List[Entity]]) -> None:
        """Add entities to map"""
        for arg in args:
            ent_list = arg if isinstance(arg, list) else [arg]
            for entity in ent_list:
                if isinstance(entity, Entity):
                    entity.id = self.entity_counter
                    self.entity_counter += 1
                    self.entities.append(entity)
                else:
                    raise TypeError(f"Expected <class {Entity.__name__}> but got {type(entity).__name__}")

    def copy(self):
        """Return a deepcopy of the current map instance, useful for backup"""
        return deepcopy(self)
    
    def get_entity_by_brush(self, target_brush: Brush) -> Union[Entity, None]:
        """Return the parent entity of the brush"""
        for entity in self.entities:
            if target_brush in entity.brushes:
                return entity
        return None


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                        DUNDER METHODS                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    def __str__(self) -> str:
        """Return a string representation of the map."""
        return f"{self.entities}"
    
    def __iter__(self): 
        """Return an iterator over the Map entities"""
        return iter(self.entities)