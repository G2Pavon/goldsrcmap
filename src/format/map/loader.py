
from .map import Map
from .entity import Entity
from .brush import Brush
from .face import Face
from .texture import Texture
from utils.math.plane import Plane
from utils.math.point import Point
from utils.math.vector import Vector3

import os
# Lazy implementation
#TODO: Class Reader

def extract_pathname(filepath: str):
    path, filename = os.path.split(filepath)
    mapname, extension = os.path.splitext(filename)
    if extension == '.map':
        return path, mapname


def load_map(filepath:str) -> Map:
    map_path, name = extract_pathname(filepath)
    map_obj = Map(name)
    map_obj.path = map_path

    brace_count = 0
    current_entity = None
    current_brush = None
    
    with open(filepath, 'r') as file:
        for line in file.readlines():

            #skip comments
            if line.startswith('//'):
                continue

            elif line.startswith('{'):
                brace_count += 1
                if brace_count == 1:
                    #start of the entity
                    current_entity = Entity()
                else:
                    #start of the brush
                    current_brush = Brush()
                    
            elif line.startswith('}'):
                brace_count -= 1
                if brace_count == 0:
                    #end of the entity
                    map_obj.add_entity(current_entity)

                else: # brace_count == 1
                    #end of the brush
                    current_entity.add_brush(current_brush)

            #entity property, brace_count == 1
            elif line.startswith('"'):
                k, v = line.strip().split('" "', 1)
                key, value = k.replace('"', ''), v.replace('"', '')
                current_entity.properties[key] = value
            
            #brush face, brace_count == 2
            elif line.startswith('('):
                face_info = line.strip().split()
                if len(face_info) <= 31:
                    plane = Plane(
                        Point(float(face_info[1]), float(face_info[2]), float(face_info[3])),
                        Point(float(face_info[6]), float(face_info[7]), float(face_info[8])),
                        Point(float(face_info[11]), float(face_info[12]), float(face_info[13]))
                    )
                    texture_name = str(face_info[15]).upper()
                    u_axis =  Vector3(float(face_info[17]), float(face_info[18]), float(face_info[19]))
                    u_offset = float(face_info[20])
                    v_axis = Vector3(float(face_info[23]), float(face_info[24]), float(face_info[25]))
                    v_offset = float(face_info[26])
                    rotation = float(face_info[28])
                    u_scale = float(face_info[29])
                    v_scale = float(face_info[30])

                    texture = Texture(texture_name, u_axis, u_offset, v_axis, v_offset, rotation, u_scale, v_scale)
                    current_face = Face(plane, texture)

                    current_brush.add_face(current_face)
    return map_obj

