from format.map.map import Map
from format.map.entity import Entity
from format.map.face import Face

from typing import TextIO

def save_map(input: Map, output: str):
    MapWriter(input, output)

class MapWriter:

    def __init__(self, input: Map, output: str = 'output.map'):
        self.map_instance = input
        self.output = output
        self.write_map()

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                         METHODS                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  
    def write_map(self):
        with open(self.output, 'w') as f:
            f.write('// Game: Half-Life\n')
            f.write('// Format: Valve\n')
            for entity in self.map_instance:
                if entity.properties:
                    f.write(f'// entity {entity._id}\n')
                    f.write('{\n')
                    self.write_properties(f, entity)
                    
                    for brush in entity.brushes:
                        if brush.faces:
                            f.write(f'// brush {brush.id}\n')
                            f.write('{\n')
                            for face in brush.faces:
                                self.write_face(f, face)
                            f.write('}\n')
                    f.write('}\n')
        print('Saved')

    def write_properties(self, f: TextIO, entity: Entity):
        for key, value in entity.properties.items():
            f.write(f'"{key}" "{value}"\n')


    def write_face(self, f: TextIO, face: Face):
        for point in face.plane:
            f.write(f'{point} ')
        f.write(f'{face.texture.name} ')
        f.write('[ ')
        f.write(f'{face.texture.u_axis} ')
        f.write(f'{face.texture.u_offset} ')
        f.write('] ')
        f.write('[ ')
        f.write(f'{face.texture.v_axis} ')
        f.write(f'{face.texture.v_offset} ')
        f.write('] ')
        f.write(f'{face.texture.rotation} ')
        f.write(f'{face.texture.u_scale} ')
        f.write(f'{face.texture.v_scale} ')
        f.write('\n')
