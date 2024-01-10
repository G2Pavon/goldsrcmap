from format.map.entity import Entity

class EntityGenerator:

    @staticmethod
    def info_player_start(origin: list, angle: int = 0) -> Entity:
        e = Entity()
        e.properties = {
                        "classname":"info_player_start",
                        "origin":f"{origin[0]} {origin[1]} {origin[2]}",
                        "angles":f"0 {angle} 0",
                        }
        return e
    
    @staticmethod
    def light_environment(origin: list, angle: int = 0, pitch: int = -90) -> Entity:
        e = Entity()
        e.properties = {
                        "classname":"light_environment",
                        "angle":f"{angle}",
                        "pitch":f"{pitch}",
                        "_light":"255 255 255 200",
                        "origin":f"{origin[0]} {origin[1]} {origin[2]}"
                        }
        return e