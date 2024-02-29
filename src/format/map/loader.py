
from .map import Map
from .entity import Entity
from .brush import Brush
from .face import Face
from .texture import Texture
from utils.math.plane import Plane
from utils.math.point import Point
from utils.math.vector import Vector3

import os

def load_map(filepath: str) -> Map:
    map_path, name = os.path.split(filepath)
    map_obj = Map(name)
    map_obj.path = map_path
    map_obj.entity_counter = -1

    with open(filepath, 'r') as file:
        entities = []
        current_entity = None
        current_brush = None
        brace_count = 0

        for line in file:
            tokens = line.strip().split()
            if not tokens or line.startswith('//'):
                continue

            if tokens[0] == '{':
                brace_count += 1
                if brace_count == 1:
                    current_entity = Entity()
                else:
                    current_brush = Brush()

            elif tokens[0] == '}':
                brace_count -= 1
                if brace_count == 0:
                    map_obj.entity_counter += 1
                    current_entity._id = map_obj.entity_counter
                    current_entity.in_map_instance = True
                    entities.append(current_entity)
                else:
                    current_brush._id = current_entity.brush_counter
                    current_entity.brushes.append(current_brush)
                    current_entity.brush_counter += 1

            elif tokens[0] == '(':
                if len(tokens) <= 31:
                    plane = Plane(
                        Point(float(tokens[1]), float(tokens[2]), float(tokens[3])),
                        Point(float(tokens[6]), float(tokens[7]), float(tokens[8])),
                        Point(float(tokens[11]), float(tokens[12]), float(tokens[13]))
                    )
                    texture_name = tokens[15].upper()
                    u_axis = Vector3(float(tokens[17]), float(tokens[18]), float(tokens[19]))
                    u_offset = float(tokens[20])
                    v_axis = Vector3(float(tokens[23]), float(tokens[24]), float(tokens[25]))
                    v_offset = float(tokens[26])
                    rotation = float(tokens[28])
                    u_scale = float(tokens[29])
                    v_scale = float(tokens[30])

                    texture = Texture(texture_name, u_axis, u_offset, v_axis, v_offset, rotation, u_scale, v_scale)
                    current_face = Face(plane, texture)

                    current_brush.face_counter += 1
                    current_face.id = current_brush.face_counter
                    current_brush.faces.append(current_face)

            else:
                k, v = line.strip().split('" "', 1)
                key, value = k.replace('"', ''), v.replace('"', '')
                current_entity.properties[key] = value

    map_obj.entities = entities
    return map_obj
