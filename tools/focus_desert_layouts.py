"""Static content pass for the continuous scenes. Called by design_desert_scenes.

Keep authored routes and gameplay reserves, fold unused sand into landforms, and
compose contextual scenery at the edges of travel. No runtime random placement.
"""
from collections import deque
from functools import lru_cache
from pathlib import Path
import math

import numpy as np
from scipy import ndimage
import gmyy

ROOT = Path(__file__).resolve().parents[1]
WALK = set(".,;_^=|")

# A visual story and palette for each stretch, rather than one scene-wide scatter.
# Centres are inspection anchors; scenery is composed around their clear floor.
BEATS = {
    "sc_desert_frontier": [
        (12, 37, "Breached city baggage", "rubble"),
        (25, 27, "Lookout foothill cairns", "rubble"),
        (46, 18, "Watchman's abandoned perch", "rubble"),
        (29, 49, "Sheltered cactus bend", "cactus"),
        (45, 42, "Canyon windbreak", "dry"),
        (58, 28, "Split-cliff trail marker", "rubble"),
        (61, 56, "Washed-out stone bed", "dry"),
        (77, 45, "First green in the wash", "oasis"),
        (91, 58, "Shed snake bones", "bones"),
        (95, 23, "Spring-bank palms", "oasis"),
        (114, 39, "Lakeside resting place", "oasis"),
        (119, 21, "Hidden spring cairns", "oasis"),
    ],
    "sc_caravan_basin": [
        (11, 46, "Spilled caravan cargo", "caravan"),
        (26, 29, "Broken axle pull-off", "caravan"),
        (29, 20, "Camp approach windbreak", "cactus"),
        (48, 29, "Bandit lookout remains", "caravan"),
        (43, 51, "Cactus grove fork", "cactus"),
        (49, 69, "Snake-skin hollow", "bones"),
        (58, 45, "Bonefield waystones", "bones"),
        (77, 29, "Last warning before the broken span", "bones"),
        (78, 54, "Bridge builder's abandoned yard", "caravan"),
        (57, 73, "Cistern waterline", "oasis"),
        (75, 72, "Cistern keeper's niche", "rubble"),
        (99, 52, "Far-bank stone cairns", "rubble"),
        (109, 62, "Southern bridge watch", "rubble"),
        (123, 39, "Ruined arcade", "royal"),
        (123, 25, "Stair-foot votive stones", "royal"),
        (138, 14, "Upper-terrace lookout", "royal"),
    ],
    "sc_royal_expanse": [
        (10, 27, "Plateau windbreak", "dry"),
        (21, 33, "Grotto approach bones", "bones"),
        (40, 22, "Echo shrine offerings", "rubble"),
        (47, 25, "Causeway warning cairns", "royal"),
        (20, 45, "Burrowed trail edge", "bones"),
        (38, 62, "Worm hunter's remains", "bones"),
        (48, 47, "Southern return marker", "dry"),
        (65, 45, "Broken royal procession", "royal"),
        (80, 31, "Memorial stair approach", "royal"),
        (103, 23, "Memorial offerings", "royal"),
        (100, 44, "Forecourt garden remains", "dry"),
        (85, 54, "Sunken court approach", "rubble"),
        (95, 70, "Sundial west cloister", "royal"),
        (120, 71, "Sundial east cloister", "royal"),
        (133, 57, "Processional road return", "royal"),
        (126, 44, "Last refuge votive stones", "royal"),
        (145, 26, "Courtyard wall sentinels", "royal"),
        (155, 24, "Sealed threshold rubble", "royal"),
    ],
}

PALETTES = {
    "rubble": ("column_broken", "ruin_block", "loose_rocks", "bush_dead"),
    "dry": ("tree_dead", "supply_barrel", "pebbles", "bush_dead"),
    "cactus": ("cactus_tall", "cactus_small", "bush_dead", "pebbles"),
    "oasis": ("palm", "water_barrel", "bush", "pebbles"),
    "bones": ("tree_dead", "column_fallen", "pebbles", "loose_rocks"),
    "caravan": ("wagon_wreck", "supply_barrel", "loose_rocks", "bush_dead"),
    "royal": ("column_whole", "column_broken", "pebbles", "bush_dead"),
}
FOOTPRINTS = {"palm": [24, 14], "cactus_small": [16, 12],
              "cactus_tall": [24, 16], "tree_dead": [24, 16],
              "obelisk": [40, 28], "ruin_block": [48, 24],
              "wagon_wreck": [160, 40], "supply_barrel": [28, 16],
              "water_barrel": [38, 20], "column_fallen": [36, 20],
              "column_broken": [28, 18], "column_whole": [28, 18]}
FLAT = {"pebbles", "loose_rocks", "bush", "bush_dead", "skull"}
COMPANIONS = {
    "rubble": ("column_fallen","supply_barrel","column_whole"),
    "dry": ("cactus_small","column_fallen","water_barrel"),
    "cactus": ("supply_barrel","tree_dead","column_fallen"),
    "oasis": ("supply_barrel","column_broken","ruin_block"),
    "bones": ("cactus_small","column_broken","supply_barrel"),
    "caravan": ("water_barrel","column_fallen","ruin_block"),
    "royal": ("column_fallen","water_barrel","ruin_block","supply_barrel"),
}


def rect_mask(shape, rect, pad=0):
    mask = np.zeros(shape, dtype=bool)
    x1, y1, x2, y2 = rect
    mask[max(0, y1-pad):min(shape[0], y2+pad+1),
         max(0, x1-pad):min(shape[1], x2+pad+1)] = True
    return mask


def route_mask(shape, points, radius=0):
    mask = np.zeros(shape, dtype=bool)
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        mask |= rect_mask(shape, [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)], radius)
    return mask


def connected_path(floor, start, targets):
    """Shortest old-floor spur; never tunnels through a wall, water or elevation."""
    start = tuple(start)
    if targets[start[1], start[0]]:
        return [start]
    queue = deque([start]); previous = {start: None}
    end = None
    while queue:
        x, y = queue.popleft()
        if targets[y, x]:
            end = (x, y); break
        for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            xx, yy = p
            if 0 <= yy < floor.shape[0] and 0 <= xx < floor.shape[1] and floor[yy, xx] and p not in previous:
                previous[p] = (x, y); queue.append(p)
    if end is None:
        raise ValueError(f"No existing-floor connection for {start}")
    path = []
    while end is not None:
        path.append(end); end = previous[end]
    return path


@lru_cache(None)
def sprite_bounds(name):
    for asset in ("spr_"+name, "spr_ph_"+name):
        path = ROOT / "sprites" / asset / (asset+".yy")
        if path.exists():
            data = gmyy.gm_loads(path.read_text(encoding="utf-8"))
            ox, oy = data["sequence"]["xorigin"], data["sequence"]["yorigin"]
            return (data["bbox_left"]-ox, data["bbox_top"]-oy,
                    data["bbox_right"]-ox, data["bbox_bottom"]-oy)
    raise ValueError(f"Scenery has no imported sprite or fallback: {name}")


def apply_focus(scene):
    sp = scene.s
    grid = np.array(scene.grid)
    shape = grid.shape
    original = np.isin(grid, list(WALK))
    before = int(original.sum())
    paths = [sp["primary_route"]] + [p["waypoints"] for p in sp["exploration_loops"]]
    centre = np.zeros(shape, dtype=bool)
    lanes = np.zeros(shape, dtype=bool)
    for path in paths:
        centre |= route_mask(shape, path)
        lanes |= route_mask(shape, path, 1)

    # Existing combat, structures, reserves and interactions remain authoritative.
    hard = lanes.copy()
    art_clear = np.zeros(shape, dtype=bool)
    for group in sp["encounters"]:
        hard |= rect_mask(shape, group["combat_rect"], 1)
        art_clear |= rect_mask(shape, group["combat_rect"])
    for cp in sp["checkpoints"]:
        hard |= rect_mask(shape, cp["quiet_rect"])
        art_clear |= rect_mask(shape, cp["safe_rect"], 1)
    for ar in sp["arrivals"]:
        hard |= rect_mask(shape, ar["safe_rect"], 1)
        art_clear |= rect_mask(shape, ar["safe_rect"], 1)
    if sp["initial_spawn"]:
        x, y = sp["initial_spawn"]
        hard |= rect_mask(shape, [x, y, x, y], 2)
        art_clear |= rect_mask(shape, [x, y, x, y], 2)
    for ex in scene.exits:
        edge = [0, ex["rows"][0], 4, ex["rows"][1]] if ex["side"] == "W" else [scene.w-5, ex["rows"][0], scene.w-1, ex["rows"][1]]
        hard |= rect_mask(shape, edge)
        art_clear |= rect_mask(shape, edge, 1)
    for script in sp["scripts"]:
        if script["trigger_rect"]:
            hard |= rect_mask(shape, script["trigger_rect"], 1)
            if script["event"] != "chapter_start":
                art_clear |= rect_mask(shape, script["trigger_rect"], 1)
    for st in sp["structures"]:
        x1, y1, x2, y2 = st["rect"]
        if st["kind"] == "broken_bridge":
            continue
        landing = [x1, y1-2, x2, y2+2] if st["kind"] in ("stairs", "bridge_ns") else [x1-3, y1, x2+3, y2]
        hard |= rect_mask(shape, landing)
        art_clear |= rect_mask(shape, landing)
    for chest in sp["chests"]:
        x, y = chest["cell"]
        reserve = rect_mask(shape, [x-1, y-1, x+1, y+1])
        ax, ay = chest["approach_cell"]
        reserve |= rect_mask(shape, [ax-1, ay-1, ax+1, ay+1])
        hard |= reserve; art_clear |= reserve
    for prop in sp["solid_props"]:
        hard |= rect_mask(shape, prop["blocked_rect"], 1)
    if sp.get("boss"):
        # Preserve the entire enclosing court and narrow mandatory entrance/seal.
        hard |= rect_mask(shape, [116, 8, 157, 34])
        art_clear |= rect_mask(shape, [118, 10, 147, 27])
        art_clear |= rect_mask(shape, [120, 28, 124, 34])
        art_clear |= rect_mask(shape, [148, 17, 149, 21])

    # Connect every persistent object/landmark and every authored scenic beat to
    # the route network before reclaiming floor. Spokes are at least 3 cells wide.
    # Quiet districts retain broad floor but may contain scenery away from the
    # star's actual interaction reserve; peaceful does not mean featureless.
    no_solids = art_clear | lanes
    targets = centre & original
    anchors = [p["anchor"] for p in sp["places"]]
    anchors += [o["cell"] for o in scene.objects]
    anchors += [c["approach_cell"] for c in sp["chests"]]
    beats = []
    for x, y, name, theme in BEATS[scene.id]:
        if not original[y, x]:
            candidates = [(xx, yy) for yy in range(max(1, y-3), min(scene.h-1, y+4))
                          for xx in range(max(1, x-3), min(scene.w-1, x+4)) if original[yy, xx]]
            x, y = min(candidates, key=lambda p: (p[0]-x)**2 + (p[1]-y)**2)
        beats.append(dict(name=name, theme=theme, cell=[x, y]))
        anchors.append([x, y])
    for anchor in anchors:
        path = connected_path(original, anchor, targets)
        for x, y in path:
            hard |= rect_mask(shape, [x, y, x, y], 1)
            no_solids |= rect_mask(shape, [x, y, x, y], 1)
        x, y = anchor
        hard |= rect_mask(shape, [x, y, x, y], 2)
        no_solids |= rect_mask(shape, [x, y, x, y], 1)

    # Chest spurs must reach a wide centre without passing through the chest's
    # own blocked cell (ordinary floor BFS alone would accept that shortcut).
    navigation = original.copy()
    for chest in sp["chests"]:
        x, y = chest["cell"]; navigation[y, x] = False
    for prop in sp["solid_props"]:
        navigation[rect_mask(shape, prop["blocked_rect"])] = False
    wide = ndimage.binary_erosion(navigation, structure=np.ones((3, 3)))
    for chest in sp["chests"]:
        for x, y in connected_path(wide, chest["approach_cell"], centre & wide):
            hard |= rect_mask(shape, [x, y, x, y], 1)
            no_solids |= rect_mask(shape, [x, y, x, y], 1)

    # Irregular connected landforms enclose routes and small destinations. The
    # low-frequency contour varies shoulder width without isolated rock noise.
    yy, xx = np.indices(shape)
    shoulders = 3.8 + .65*np.sin(xx/5.1 + yy/8.3) + .4*np.cos(yy/3.7-xx/10.1)
    network_distance = ndimage.distance_transform_edt(~centre)
    retain = hard | (network_distance <= shoulders)
    retain |= np.isin(grid, list(";_^=|"))
    # Preserve both banks of every pool and the rims of foundations.
    special = np.isin(grid, list("~;_"))
    retain |= ndimage.binary_dilation(special, iterations=2)
    # Pocket shoulders, rather than whole rectangular districts.
    for beat in beats:
        x, y = beat["cell"]
        retain |= ((xx-x)**2/6.0**2 + (yy-y)**2/4.5**2 <= 1)
    grid[original & ~retain] = "#"
    from detail_desert_exploration import paint_trails, dress_discoveries
    paint_trails(grid, paths, scene.id, [g["combat_rect"] for g in sp["encounters"]])
    # Remove any fringe cell separated when open sand was folded into the rim.
    floor = np.isin(grid, list(WALK))
    labels, _ = ndimage.label(floor)
    sx, sy = sp["initial_spawn"] or sp["arrivals"][0]["cell"]
    grid[floor & (labels != labels[sy, sx])] = "#"
    scene.grid = grid.tolist()
    floor = np.isin(grid, list(WALK))

    # Contextual material islands: scrub at palms; fragmented paving at remnants.
    for beat in beats:
        x, y = beat["cell"]
        region = ((xx-x)**2/4.1**2 + (yy-y)**2/2.8**2 < 1)
        region &= (grid == ".") | (grid == ",")
        if beat["theme"] == "oasis":
            grid[region] = ";"
        elif beat["theme"] in ("rubble", "royal", "caravan"):
            # Cracked apron with open sand seams, not a filled rectangle.
            grid[region & (((xx+2*yy) % 5) != 0)] = "_"
    for discovery in sp["discoveries"]:
        x,y = discovery["cell"]
        region = ((xx-x)**2/4.1**2+(yy-y-1)**2/2.9**2 < 1)
        region &= np.isin(grid,list(".,")) & ~centre
        if discovery["theme"] == "garden":
            grid[region] = ";"
        elif discovery["theme"] in ("shrine","archive","survey"):
            grid[region & (((2*xx+yy) % 6) != 0)] = "_"
        elif discovery["theme"] == "supplies":
            worn = ((xx-x)**2/2.6**2+(yy-y)**2/1.6**2 < 1)
            grid[region & worn] = ","
    scene.grid = grid.tolist()

    if scene.id == "sc_desert_frontier":
        # Natural water and vegetation have rounded shoulders; the cistern and
        # royal masonry elsewhere retain their deliberately architectural edges.
        for material, radius, replacement in (("~", 2, ";"), (";", 3, ".")):
            material_mask = grid == material
            disk = np.indices((2*radius+1, 2*radius+1))-radius
            kernel = (disk[0]**2+disk[1]**2) <= radius**2
            rounded = ndimage.binary_opening(material_mask, structure=kernel)
            grid[material_mask & ~rounded] = replacement
        floor = np.isin(grid, list(WALK))
        scene.grid = grid.tolist()

    # Preserve deliberately planted small gardens after rounding the large
    # natural lake banks: a three-cell opening would erase these little beds.
    for discovery in sp["discoveries"]:
        if discovery["theme"] == "garden":
            x,y = discovery["cell"]
            bed = ((xx-x)**2/4.1**2+(yy-y-1)**2/2.9**2 < 1)
            bed &= np.isin(grid,list(".,")) & ~centre
            grid[bed] = ";"
    scene.grid = grid.tolist()

    occupied = {tuple(o["cell"]) for o in scene.objects}
    occupied |= {tuple(d["cell"]) for d in scene.decor}
    # Ground routes also exclude intrusive art. Small ground decals stay outside
    # fight pads, interactions and structure landings to preserve telegraph value.
    flat_clear = art_clear | centre
    art_clear |= lanes
    all_positions = [tuple(d["cell"]) for d in scene.decor]
    placements = [(o["prop"], *o["cell"]) for o in scene.objects if o["type"] == "prop"]
    placements += [(d["asset_id"][4:], *d["cell"]) for d in scene.decor]
    def art_allowed(name, x, y):
        if not (2 <= x < scene.w-2 and 3 <= y < scene.h-2) or (x, y) in occupied:
            return False
        if grid[y, x] in "~Cx=|^":
            return False
        spacing = .95 if name in FLAT else 1.65
        if any((x-a)**2+(y-b)**2 < spacing**2 for a, b in all_positions):
            return False
        # Avoid repeated obelisks, wagons or identical trees forming rows. Low
        # companion details may repeat, but a local view gets varied silhouettes.
        repeat_limit = 1 if name in ("obelisk", "wagon_wreck") else 2 if name in FOOTPRINTS else 4
        if sum(asset == name and abs(x-a) <= 8 and abs(y-b) <= 5 for asset, a, b in placements) >= repeat_limit:
            return False
        l, t, r, b = sprite_bounds(name)
        l += x*64+32; r += x*64+32; t += y*64+32; b += y*64+32
        ax1, ay1 = max(0, l//64), max(0, t//64)
        ax2, ay2 = min(scene.w-1, r//64), min(scene.h-1, b//64)
        reserve = flat_clear if name in FLAT else art_clear
        if reserve[ay1:ay2+1, ax1:ax2+1].any():
            return False
        return True

    def add_art(name, x, y, note, solid=False):
        if not art_allowed(name, x, y):
            return False
        if solid and floor[y, x]:
            if no_solids[y, x] or grid[y, x] in "^=|":
                return False
            fp = FOOTPRINTS[name]
            if fp[0] > 64:
                if x < 1 or x+1 >= scene.w or not floor[y, x-1:x+2].all() or no_solids[y, x-1:x+2].any():
                    return False
                blocked = [x-1, y, x+1, y]
            else:
                blocked = [x, y, x, y]
            # Conservative blocker must not cut a three-wide route or a pocket.
            proposal = floor.copy()
            proposal[blocked[1]:blocked[3]+1, blocked[0]:blocked[2]+1] = False
            _, count = ndimage.label(proposal)
            if count != 1:
                return False
            scene.prop(name, [x, y], fp, blocked)
            floor[:] = proposal
            for bx in range(blocked[0], blocked[2]+1):
                occupied.add((bx, y))
        else:
            # Tall decor goes on already blocked terrain; its base cannot be
            # walked through. Walkable dressing is small, flat ground detail.
            if name in FOOTPRINTS and grid[y, x] in WALK:
                return False
            scene.deco(name, [x, y], note)
        occupied.add((x, y)); all_positions.append((x, y))
        placements.append((name, x, y))
        return True

    # Authored camps, gardens and ruins get the best nearby positions before
    # background dressing. Each is a reachable reward, rather than a prop count.
    dress_discoveries(scene, add_art, FOOTPRINTS)

    # Compose asymmetrical little scenes: silhouette, companion, two ground
    # details. Search an annulus, so landmarks frame movement rather than sit on it.
    for index, beat in enumerate(beats):
        x, y = beat["cell"]
        palette = PALETTES[beat["theme"]]
        cells = [(a, b) for b in range(max(3, y-6), min(scene.h-2, y+7))
                 for a in range(max(2, x-7), min(scene.w-2, x+8))
                 if 2.5**2 <= (a-x)**2+(b-y)**2 <= 7**2]
        cells.sort(key=lambda p: (abs(math.hypot(p[0]-x, p[1]-y)-4.0),
                                 math.sin(p[0]*1.7+p[1]*.8+index)))
        for n, asset in enumerate(palette):
            shifted = cells[n*11:] + cells[:n*11]
            for a, b in shifted:
                if add_art(asset, a, b, beat["name"], solid=asset in FOOTPRINTS):
                    break

    # Frame encounters/rewards with scenery outside the complete visible art
    # footprint reserves, retaining the contrast needed for attacks and loot.
    focus_points = [(p["cell"], "Treasure approach", "rubble") for p in sp["chests"]]
    focus_points += [([sum(g["combat_rect"][::2])//2, sum(g["combat_rect"][1::2])//2],
                      "Encounter perimeter", "bones") for g in sp["encounters"] if not g["id"].endswith(":boss")]
    for (x, y), note, theme in focus_points:
        for asset in PALETTES[theme][:3]:
            candidates = [(a, b) for b in range(max(3, y-9), min(scene.h-2, y+10))
                          for a in range(max(2, x-10), min(scene.w-2, x+11))]
            candidates.sort(key=lambda p: abs(math.hypot(p[0]-x, p[1]-y)-5.5))
            for a, b in candidates:
                if add_art(asset, a, b, note, solid=asset in FOOTPRINTS):
                    break

    # Fill visual gaps with contextual edge groups, measured at player-camera
    # scale. Four persistent details, including a landmark silhouette, must be
    # visible together. An isolated pebble at the screen edge is not enough.
    def coverage():
        counts = np.zeros((scene.h+1, scene.w+1), dtype=int)
        major = np.zeros_like(counts)
        nearby = np.zeros_like(counts)
        nearby_major = np.zeros_like(counts)

        def visible(a, b, top, significant, planted=False):
            x1, x2 = max(0, a-9), min(scene.w-1, a+9)
            y1, y2 = max(0, math.ceil(top-5.875)), min(scene.h-1, b+5)
            for array in (counts, major) if significant else (counts,):
                array[y1, x1] += 1; array[y2+1, x1] -= 1
                array[y1, x2+1] -= 1; array[y2+1, x2+1] += 1
            x1, x2 = max(0,a-5), min(scene.w-1,a+5)
            y1, y2 = max(0,math.ceil(top-3.75)), min(scene.h-1,b+3)
            for array in (nearby, nearby_major) if significant or planted else (nearby,):
                array[y1,x1] += 1; array[y2+1,x1] -= 1
                array[y1,x2+1] -= 1; array[y2+1,x2+1] += 1

        for obj in scene.objects:
            if obj["type"] == "enemy":
                continue
            a, b = obj["cell"]
            if obj["type"] == "prop":
                bounds = sprite_bounds(obj["prop"])
                top = max(0, (b*64+32+bounds[1])/64)
            else:
                top = b
            visible(a, b, top, True)
        for d in scene.decor:
            a, b = d["cell"]
            bounds = sprite_bounds(d["asset_id"][4:])
            top = max(0, (b*64+32+bounds[1])/64)
            visible(a, b, top, d["layer"] != "Visual_Assets", d["asset_id"] in ("spr_bush", "spr_bush_dead"))
        counts = counts.cumsum(0).cumsum(1)[:-1, :-1]
        major = major.cumsum(0).cumsum(1)[:-1, :-1]
        nearby = nearby.cumsum(0).cumsum(1)[:-1,:-1]
        nearby_major = nearby_major.cumsum(0).cumsum(1)[:-1,:-1]
        if sp.get("boss"):
            # Central warning floor remains deliberately clear and composed
            # through sand/paving, the boss and its persistent reward point.
            arena = [118,10,147,27]
            counts[rect_mask(shape, arena)] = 4
            major[rect_mask(shape, arena)] = 2
            nearby[rect_mask(shape, arena)] = 3
            nearby_major[rect_mask(shape, arena)] = 1
        covered = (counts >= 4) & (major >= 2) & (nearby >= 3) & (nearby_major >= 1)
        shore = ndimage.distance_transform_edt(~np.isin(grid,list("~C"))) <= 3
        # A lake or chasm already supplies the large local silhouette. Add two
        # close details on its walkable bank instead of crowding the edge.
        covered[shore] = (counts[shore] >= 4) & (major[shore] >= 2) & (nearby[shore] >= 2)
        for structure in sp["structures"]:
            # The bridge/stair composition itself is the close focal point.
            # Its functional landing stays open; frame it from the shoulders.
            area = rect_mask(shape, structure["rect"], 3)
            covered[area] = (counts[area] >= 4) & (major[area] >= 2)
        for group in sp["encounters"]:
            if not group["id"].endswith(":boss"):
                area = rect_mask(shape, group["combat_rect"], 2)
                covered[area] = counts[area] >= 2
        # The follow camera stops at scene edges; an arrival two cells from the
        # border still sees the full viewport looking into the landscape.
        cx = np.clip(xx.astype(float),9.5,scene.w-10.5)
        cy = np.clip(yy.astype(float),5.125,scene.h-6.125)
        xlo,xhi = np.floor(cx).astype(int),np.ceil(cx).astype(int)
        ylo,yhi = np.floor(cy).astype(int),np.ceil(cy).astype(int)
        need_major = np.where(nearby_major < 1, 0, major)
        # The camera stops between tile centres at room edges. Cover both
        # neighbouring samples so a half-tile clamp cannot lose its landmark.
        safe = covered[ylo,xlo] & covered[ylo,xhi] & covered[yhi,xlo] & covered[yhi,xhi]
        priority = np.minimum.reduce([need_major[ylo,xlo],need_major[ylo,xhi],need_major[yhi,xlo],need_major[yhi,xhi]])
        return safe, priority

    for _ in range(1200):
        covered, major = coverage()
        missing = floor & ~covered
        if not missing.any():
            break
        # Address the largest empty patch first, deterministic tie-breaking.
        distance = ndimage.distance_transform_edt(~covered)
        y, x = np.unravel_index(np.argmax(distance * missing), shape)
        x = int(np.clip(x, 10, scene.w-11)); y = int(np.clip(y, 6, scene.h-7))
        beat = min(beats, key=lambda p: (p["cell"][0]-x)**2+(p["cell"][1]-y)**2)
        palette = PALETTES[beat["theme"]]
        candidates = [(a, b) for b in range(max(3, y-4), min(scene.h-2, y+5))
                      for a in range(max(2, x-7), min(scene.w-2, x+8))]
        candidates.sort(key=lambda p: (grid[p[1], p[0]] in WALK,
                                       abs(math.hypot(p[0]-x, p[1]-y)-3)))
        placed = False
        silhouettes = (palette[0],palette[1])+COMPANIONS[beat["theme"]]
        plant = "bush" if beat["theme"] == "oasis" else "bush_dead"
        details = (palette[2],palette[3],"loose_rocks",plant)
        assets = silhouettes+(plant,)+details if major[y,x] < 2 else details+silhouettes
        for asset in assets:
            for a, b in candidates:
                if add_art(asset, a, b, beat["name"]+" — trail-edge continuation", solid=asset in FOOTPRINTS):
                    placed = True; break
            if placed:
                break
        if not placed:
            raise ValueError(f"No safe scenery for empty camera at {scene.id} {[int(x), int(y)]}")
    if (floor & ~coverage()[0]).any():
        raise ValueError(f"Unresolved empty views in {scene.id}")

    sp["layout_focus"] = dict(
        revision="discovery_routes_v2", original_walkable_cells=before,
        walkable_cells=int(np.isin(grid, list(WALK)).sum()),
        principle="Continuous landscapes with framed routes, short scenic pockets and distinct material/prop stories. Traversable cameras see persistent scenery; the central boss arena keeps deliberate open warning floor.",
        camera_coverage_cells=[19, 11], camera_minimum_details=4,
        camera_minimum_landmarks=2, camera_combat_minimum_details=2, beats=beats,
        nearby_coverage_cells=[11,7], nearby_minimum_details=3, nearby_minimum_landmarks=1,
        protected="Three-wide routes, full combat pads, chest approaches, save/arrival reserves, bridge/stair landings, boss gates and warning floor.",
    )


def focus_scenes(scenes):
    for scene in scenes:
        apply_focus(scene)
