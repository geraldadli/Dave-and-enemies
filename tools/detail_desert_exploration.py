"""Authored local discoveries, returning paths and close scenery compositions."""
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

# Every small route leaves and rejoins an existing route at different points.
# New rewards append to the original chest list, preserving all existing IDs.
DISCOVERIES = {
    "sc_desert_frontier": [
        ("lost_porters", "Lost Porters' Camp", [21,45], "supplies", [["potion_health",1]],
         [[19,40],[19,48],[24,48],[24,40]]),
        ("survey_cache", "Wash Survey Camp", [78,50], "survey", [["gold_coins",6]],
         [[75,46],[75,53],[82,53],[82,46]]),
        ("spring_keeper", "Spring Keeper's Niche", [105,22], "garden", [["desert_rose",1]],
         [[101,20],[101,24],[109,24],[109,20]]),
        ("palm_garden", "Buried Palm Garden", [109,50], "garden", [["ancient_coin",1]],
         [[96,46],[104,46],[104,53],[115,53],[115,42]]),
    ],
    "sc_caravan_basin": [
        ("spilled_supplies", "Stranded Supply Wagon", [16,49], "supplies", [["potion_health",1]],
         [[10,40],[10,52],[22,52],[22,43]]),
        ("grove_cache", "Cactus Shelter", [47,51], "shelter", [["gold_coins",8]],
         [[42,49],[42,54],[52,54],[52,49]]),
        ("bridge_watch", "Broken Span Overlook", [74,29], "survey", [["desert_rose",1]],
         [[62,30],[62,27],[80,27],[80,41],[78,41]]),
        ("well_keeper", "Well Keeper's Yard", [115,59], "supplies", [["potion_health",1],["gold_coins",3]],
         [[109,54],[118,54],[118,62],[109,62]]),
    ],
    "sc_royal_expanse": [
        ("pilgrim_camp", "Forgotten Pilgrims' Rest", [16,36], "shrine", [["potion_greater",1]],
         [[12,28],[12,39],[21,39],[21,28]]),
        ("procession_cache", "Procession Waystation", [71,28], "shrine", [["ancient_coin",2]],
         [[66,37],[62,37],[62,26],[79,26],[79,37],[82,37]]),
        ("sunken_garden", "Sunken Offering Garden", [99,50], "garden", [["desert_rose",1]],
         [[84,45],[94,45],[94,53],[110,53]]),
        ("archive_cache", "Fallen Archive", [138,66], "archive", [["golden_scarab",1]],
         [[134,58],[142,58],[142,69],[134,69],[134,67]]),
    ],
}

STAMPS = {
    "supplies": [("wagon_wreck",-4,-2),("water_barrel",-3,1),("supply_barrel",3,0),
                 ("supply_barrel",3,2),("loose_rocks",-2,3),("bush_dead",4,3)],
    "survey": [("column_broken",-3,-1),("column_fallen",3,0),("supply_barrel",-3,2),
               ("ruin_block",3,3),("loose_rocks",-2,4),("pebbles",4,-2),
               ("water_barrel",-4,5),("loose_rocks",3,5)],
    "garden": [("palm",3,1),("water_barrel",3,0),("bush",-2,2),
               ("bush",3,3),("loose_rocks",-3,4),("column_broken",4,-2)],
    "shelter": [("cactus_tall",-3,-1),("cactus_small",3,0),("supply_barrel",-3,2),
                ("bush_dead",3,3),("pebbles",-2,4),("loose_rocks",4,-2)],
    "shrine": [("column_whole",-3,-1),("column_broken",3,-1),("water_barrel",-3,2),
               ("column_fallen",3,3),("loose_rocks",-2,4),("bush_dead",4,1)],
    "archive": [("column_broken",-3,-1),("column_fallen",3,0),("ruin_block",-3,2),
                ("supply_barrel",3,3),("loose_rocks",-2,4),("pebbles",4,-2)],
}


def prepare_discoveries(scenes):
    for scene in scenes:
        scene.s["discoveries"] = []
        for slug, name, cell, theme, loot, route in DISCOVERIES[scene.id]:
            scene.loop(name+" trail", route, "Find "+name.lower()+" and its supplies; return by another approach.")
            scene.new_chest(cell, loot, "Optional discovery at "+name+"; no equipment or progression requirement.")
            chest = scene.s["chests"][-1]
            x, y = cell
            rect = [x-3,y-2,x+4,y+4]
            scene.new_place("place_"+slug, name, rect, chest["approach_cell"],
                            "A close, recognizable little destination with an optional persistent supply cache.")
            # Small discoveries win the name lookup inside their broader district.
            scene.s["places"].insert(0, scene.s["places"].pop())
            scene.s["discoveries"].append(dict(id=scene.id+":"+slug, name=name,
                cell=cell, theme=theme, chest_id=chest["id"], rect=rect, route=route,
                approach=chest["approach_cell"], reward=loot))


def paint_trails(grid, paths, scene_id, combat_rects):
    """A narrow, winding worn ribbon; collision/clearance is a separate layer."""
    h, w = grid.shape
    scale = 4
    spine = Image.new("1", (w*scale,h*scale))
    draw = ImageDraw.Draw(spine)
    for route_index, points in enumerate(paths):
        for (x1,y1),(x2,y2) in zip(points, points[1:]):
            length = abs(x2-x1)+abs(y2-y1)
            samples = []
            for i in range(max(2,length*4+1)):
                t = i/max(1,length*4)
                x, y = x1+(x2-x1)*t, y1+(y2-y1)*t
                bend = .95*math.sin(math.pi*t)*math.sin((x+y)/5.3+route_index*.9)
                if y1 == y2:
                    y += bend
                else:
                    x += bend
                samples.append(((x+.5)*scale,(y+.5)*scale))
            draw.line(samples, fill=1, width=1)
    distance = ndimage.distance_transform_edt(~np.array(spine,dtype=bool))/scale
    distance = distance[2::scale,2::scale]
    yy, xx = np.indices(grid.shape)
    width = 1.15+.3*np.sin(xx/6.7+yy/8.1)
    # Long brown rectangles become two-to-three-cell ribbons with sand shoulders.
    grid[grid == ","] = "."
    paint = (distance <= width) & (grid == ".")
    grid[paint] = ","
    if scene_id == "sc_royal_expanse":
        # Remnants of an old stone procession road interrupt the dirt rhythm.
        fragments = paint & (distance < .9) & (((xx+2*yy)//3) % 5 == 0)
        for x1,y1,x2,y2 in combat_rects:
            fragments[y1:y2+1,x1:x2+1] = False
        grid[fragments] = "_"


def dress_discoveries(scene, add_art, footprints):
    placed = {}
    for discovery in scene.s["discoveries"]:
        x, y = discovery["cell"]
        made = 0
        for asset, dx, dy in STAMPS[discovery["theme"]]:
            target = (x+dx,y+dy)
            candidates = [(target[0]+a,target[1]+b) for b in range(-2,3) for a in range(-2,3)]
            candidates.sort(key=lambda p: (p[0]-target[0])**2+(p[1]-target[1])**2)
            if asset == "palm":
                # Canopies fit beside the reward in deep gardens; the shallow
                # spring-bank niche uses its outer bank instead of the path.
                candidates = [(x+3,y+1),(x+7,y+3),(x-7,y+3)] + candidates
            for a,b in candidates:
                if add_art(asset,a,b,discovery["name"]+" — composed discovery",solid=asset in footprints):
                    made += 1; break
        placed[discovery["id"]] = made
    scene.s["discovery_dressing"] = placed
