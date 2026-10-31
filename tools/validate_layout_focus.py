"""Audit exported layout using actual sprite bounds and generated room tiles.

Enemy silhouettes are omitted: scenery must survive a cleared fight. Complements
validate_desert_scenes.py's topology, interaction and persistence checks.
"""
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from preview_room import load_yy, decompress

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "design/desert"
WALK = set(".,;_^=|")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(None)
def art_bounds(names):
    for name in names:
        path = ROOT / "sprites" / name / (name+".yy")
        if path.exists():
            meta = load_yy(str(path))
            ox, oy = meta["sequence"]["xorigin"], meta["sequence"]["yorigin"]
            return (meta["bbox_left"]-ox, meta["bbox_top"]-oy,
                    meta["bbox_right"]-ox, meta["bbox_bottom"]-oy)
    raise ValueError(f"No installed sprite/fallback for {names}")


def intersects(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def pixels(rect, pad=0):
    x1, y1, x2, y2 = rect
    return [(x1-pad)*64, (y1-pad)*64, (x2+pad+1)*64, (y2+pad+1)*64]


def run():
    specs = load(BASE / "scene_gameplay_specs.json")
    decorations = load(BASE / "scene_decorations.json")
    baseline = load(BASE / "layout_focus_baseline.json")
    report = {}; errors = []; checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(message)

    for sid, sp in specs.items():
        room = sp["room_id"]
        core = load(BASE / "scenes" / (room+".json"))
        data = load(ROOT / "datafiles/data/scenes" / (room+".json"))
        w, h = core["size_cells"]
        check(data["terrain"] == core["terrain"], sid+": runtime terrain is stale")
        check(len(data["decor"]) == len(decorations[sid]), sid+": runtime scenery is stale")
        check(len(data["props"]) == len(sp["solid_props"]), sid+": runtime props are stale")
        yy = load_yy(str(ROOT / "rooms" / room / (room+".yy")))
        check(yy["roomSettings"]["Width"] == w*64 and yy["roomSettings"]["Height"] == h*64, sid+": room dimensions differ")
        for layer in yy["layers"]:
            if "tiles" not in layer:
                continue
            name = layer["tilesetId"]["name"]
            directory = ROOT / "tilesets" / name
            meta = load_yy(str(directory / (name+".yy")))
            sprite = meta["spriteId"]["name"]
            source_meta = load_yy(str(ROOT / "sprites" / sprite / (sprite+".yy")))
            source = np.array(Image.open(ROOT / "sprites" / sprite / (source_meta["frames"][0]["name"]+".png")).convert("RGBA"))
            packed = np.array(Image.open(directory / "output_tileset.png").convert("RGBA"))
            cols = meta["out_columns"]; count = meta["tile_count"]
            check(packed.shape[:2] == (((count+cols-1)//cols)*68, cols*68), name+": prepared image stride/count differs from metadata")
            matching = True
            for tile_id in range(count):
                sy, sx = divmod(tile_id, source.shape[1]//64)
                py, px = divmod(tile_id, cols)
                body = packed[py*68+2:py*68+66, px*68+2:px*68+66]
                expected = source[sy*64:sy*64+64, sx*64:sx*64+64]
                matching &= np.array_equal(body, expected)
            check(matching, name+": compiler-ready image is stale relative to source tiles")
            ids = decompress(layer["tiles"]["TileCompressedData"], w*h)
            check(max(v & 0x7ffff for v in ids) < count, name+": room references a tile outside the prepared image")
        wall = next(l for l in yy["layers"] if l["name"] == "Tiles_Walls_Below")
        cells = decompress(wall["tiles"]["TileCompressedData"], w*h)
        check(len(cells) == w*h, sid+": truncated wall layer")
        check(all(bool(cells[y*w+x]) == (ch in "#M^") for y, row in enumerate(core["terrain"]) for x, ch in enumerate(row)), sid+": visual walls and collision terrain differ")
        reserves = [pixels(g["combat_rect"]) for g in sp["encounters"]]
        reserves += [pixels(c["safe_rect"], 1) for c in sp["checkpoints"]]
        reserves += [pixels(a["safe_rect"], 1) for a in sp["arrivals"]]
        route_reserves = []; flat_route_reserves = []
        for path in [sp["primary_route"]]+[p["waypoints"] for p in sp["exploration_loops"]]:
            for (x1, y1), (x2, y2) in zip(path, path[1:]):
                line = [min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)]
                route_reserves.append(pixels(line,1))
                flat_route_reserves.append(pixels(line))
        for script in sp["scripts"]:
            if script["trigger_rect"] and script["event"] != "chapter_start":
                reserves.append(pixels(script["trigger_rect"], 1))
        for chest in sp["chests"]:
            x, y = chest["cell"]; ax, ay = chest["approach_cell"]
            reserves.extend([pixels([x-1, y-1, x+1, y+1]), pixels([ax-1, ay-1, ax+1, ay+1])])
        for st in sp["structures"]:
            x1, y1, x2, y2 = st["rect"]
            if st["kind"] in ("stairs", "bridge_ns"):
                reserves.append(pixels([x1, y1-2, x2, y2+2]))
            elif st["kind"] == "bridge_ew":
                reserves.append(pixels([x1-3, y1, x2+3, y2]))

        features = []
        for category, old_count in (("props", baseline[sid]["solid_props"]), ("decor", baseline[sid]["decorations"])):
            for i, obj in enumerate(data[category]):
                bounds = art_bounds((obj["sprite"], obj["sprite_ph"]))
                offset = obj.get("off", [0, 0])
                x, y = [v*64+32+off for v, off in zip(obj["cell"], offset)]
                bounds = [bounds[0]+x, bounds[1]+y, bounds[2]+x+1, bounds[3]+y+1]
                features.append((bounds, not obj.get("flat", False), not obj.get("flat",False) or obj["sprite"] in ("spr_bush", "spr_bush_dead")))
                if i >= old_count:
                    routes = flat_route_reserves if obj.get("flat",False) else route_reserves
                    check(not any(intersects(bounds, r) for r in reserves+routes), f"{sid}: new {category} covers protected floor {obj['cell']}")
        for obj in data["chests"]+data["checkpoints"]:
            x, y = [v*64+32 for v in obj["cell"]]
            features.append(([x-24, y-56, x+24, y+8], True, True))
        bounds = np.array([f[0] for f in features])
        significant = np.array([f[1] for f in features])
        local_anchors = np.array([f[2] for f in features])
        terrain = np.array([list(row) for row in core["terrain"]])
        floor = np.isin(terrain, list(WALK))
        for prop in sp["solid_props"]:
            x1, y1, x2, y2 = prop["blocked_rect"]; floor[y1:y2+1, x1:x2+1] = False
        for chest in sp["chests"]:
            x, y = chest["cell"]; floor[y, x] = False
        failures = []; details = []; landmarks = []; deliberate_arena = 0
        close_failures = []; close_details = []
        shore = ndimage.distance_transform_edt(~np.isin(terrain,list("~C"))) <= 3
        for y, x in zip(*np.where(floor)):
            cx = max(640, min(w*64-640, x*64+32))
            cy = max(360, min(h*64-360, y*64+32))
            widths = np.minimum(bounds[:, 2], cx+640)-np.maximum(bounds[:, 0], cx-640)
            heights = np.minimum(bounds[:, 3], cy+360)-np.maximum(bounds[:, 1], cy-360)
            visible = (widths >= 16) & (heights >= 16)
            count = int(visible.sum()); major = int((visible & significant).sum())
            centre_x = int(np.clip(x, 10, w-11)); centre_y = int(np.clip(y, 6, h-7))
            def inside(group, pad=0):
                r = group["combat_rect"]
                return r[0]-pad <= centre_x <= r[2]+pad and r[1]-pad <= centre_y <= r[3]+pad
            if sp.get("boss") and 118 <= centre_x <= 147 and 10 <= centre_y <= 27:
                deliberate_arena += 1; continue
            combat_view = any(inside(g, 2) for g in sp["encounters"] if not g["id"].endswith(":boss"))
            details.append(count); landmarks.append(major)
            if not (count >= (2 if combat_view else 4) and (combat_view or major >= 2)):
                failures.append([int(x), int(y), count, major])
            structure_view = any(s["rect"][0]-3 <= centre_x <= s["rect"][2]+3 and s["rect"][1]-3 <= centre_y <= s["rect"][3]+3 for s in sp["structures"])
            if not combat_view and not structure_view:
                near_width = np.minimum(bounds[:,2],cx+352)-np.maximum(bounds[:,0],cx-352)
                near_height = np.minimum(bounds[:,3],cy+224)-np.maximum(bounds[:,1],cy-224)
                near = (near_width >= 16) & (near_height >= 16)
                close_count = int(near.sum()); close_major = int((near & local_anchors).sum())
                close_details.append(close_count)
                bank = shore[centre_y,centre_x]
                if close_count < (2 if bank else 3) or (not bank and close_major < 1):
                    close_failures.append([int(x),int(y),close_count,close_major])
        check(not failures, f"{sid}: {len(failures)} under-dressed camera positions; examples {failures[:6]}")
        check(not close_failures, f"{sid}: {len(close_failures)} empty close-focus views; examples {close_failures[:6]}")
        chest_ids = {c["id"] for c in sp["chests"]}
        check(len(data.get("discoveries",[])) == len(sp.get("discoveries",[])), sid+": runtime discoveries are stale")
        for discovery in sp.get("discoveries",[]):
            check(discovery["chest_id"] in chest_ids, sid+": discovery reward missing")
            check(sp["discovery_dressing"].get(discovery["id"],0) >= 4, sid+": discovery composition incomplete "+discovery["name"])
        original = baseline[sid]["walkable_cells"]
        current = int(np.isin(terrain, list(WALK)).sum())
        report[sid] = dict(original_terrain_floor=original, focused_terrain_floor=current,
            unused_floor_reclaimed_percent=round((1-current/original)*100, 1),
            solid_props=len(data["props"]), decorations=len(data["decor"]),
            scenic_beats=len(sp["layout_focus"]["beats"]),
            unique_scenery_sprites=len({d["sprite"] for d in data["props"]+data["decor"]}),
            inspected_walkable_positions=int(floor.sum()), deliberate_boss_floor_positions=deliberate_arena,
            under_dressed_positions=len(failures), minimum_visible_details=min(details),
            median_visible_details=float(np.median(details)), minimum_visible_landmarks=min(landmarks),
            discoveries=len(sp.get("discoveries",[])), empty_close_focus_positions=len(close_failures),
            median_close_focus_details=float(np.median(close_details)),
            enemies_counted_as_scenery=False)
    output = dict(status="pass" if not errors else "fail", checks=checks, errors=errors, scenes=report,
        limits="Static bounds/composition audit; central boss floor remains deliberately clear. Does not test GameMaker movement, combat, camera interpolation or rendering performance.")
    (BASE / "layout_focus_report.json").write_text(json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(f"{output['status'].upper()}: {checks} export/art/camera checks; {len(errors)} errors.")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(run())
