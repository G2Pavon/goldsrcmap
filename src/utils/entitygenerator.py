from format.map.entity import Entity

class EntityGenerator:

    @staticmethod
    def info_player_start(origin: list, yaw: int = 0) -> Entity:
        return Entity('info_player_start',origin, {"angles":f"0 {yaw} 0"})
    
    @staticmethod
    def light_environment(origin: list, yaw: int = 0, pitch: int = -90, color: list[int] = [255, 255, 255, 200] ) -> Entity:
        return Entity('light_environment', origin, 
                    {
                        "angles":f"0 {yaw} 0",
                        "pitch":f"{pitch}",
                        "_light":f"{color[0]} {color[1]} {color[2]} {color[3]}"
                    }
        )