# goldsrcmap
---------
Python module to manipulate goldsrc engine .map files

work in progress...

# Installation

~~pip install goldsrcmap~~ *not implemented*

Add `src` content to your working directory
e.g. `/Mapping/Scripting/`

Now create your scripts inside `/Scripting/`

# Usage

~~Documentation~~ *not implemented*

Load map:
```Python
#../Mapping/Scripting/example1.py
import goldsrcmap as gsm

# Load .map file
m = gsm.load_map('Mapping/maps/file.map')

for entity in m.entities:
  if entity.classname == 'func_door': # classname @property
    for brush in entity.brushes:
      brush.rotate_z(45)
  if entity.properties['classname'] == 'func_wall': # using properties attribute
    for brush in entity: # alternative syntax without using brushes @property
      brush.move_by(256, 256, 64)
  if entity['classname'] == 'func_plat': # without using properties attribute
    brush.move_to(32,32,256, centroid=True)
            
  # more logic here

# Save the edited map in /Scripting/ folder
gsm.save_map(m, 'edited.map')

```

Create from scratch:
```Python
#../Mapping/Scripting/example2.py
import goldsrcmap as gsm

m = gsm.new_map()

# Edit worldspawn properties
m.worldspawn.properties['wad'] = 'path/to/zhlt.wad; path/to/other.wad' # get worldspawn entity directly with @property
m.worldspawn['skyname'] = 'nebula' # alternative way to add entity property without using properties attribute

# Create brushes
skybox_room = gsm.BrushGenerator.room(2048, 2048, 2048, 16, [0,0,0], center=True)
floor = gsm.BrushGenerator.cuboid(512, 512, 32, [0,0,-128], texture="grass")

# Create entities
player = gsm.EntityGenerator.info_player_start([0,0,0])
light = gsm.EntityGenerator.light_environment([0,0,1024], angle=180, pitch=-70)

# append brush and entities in map
m.add_brush(skybox_room, floor) # adding individually or as a list also works add_brush([skybox_room, floor])
m.add_entity(player, light) # same here

button = Entity()
button.add_brush(gsm.BrushGenerator.cuboid(16, 16, 48, [82,82,0], texture="black"))
button.properties = {
                    "classname":"func_button",
                    "spawnflags":"1",
                    "speed":"5",
                    "lip":"0",
                    "wait":"2",
                    "delay":"0",
                    "target":"counter_off",
                    "master":"stopsource",
                    "targetname":"counter_stop_button"
                    }
m.add_entity(button)

# Save the new map in cstrike
gsm.save_map(m, 'cstrike/maps/generated.map')
```
---------

Documentation


---------
# References:

https://developer.valvesoftware.com/wiki/MAP_(file_format)

https://github.com/stefanha/map-files/blob/master/MAPFiles.pdf

