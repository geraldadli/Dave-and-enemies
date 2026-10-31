"""
build_world.py - converts desert_scenes_v2 into GameMaker resources and registers the runtime.

  1. Scene adapter: design/desert/scenes/*.json + scene_gameplay_specs.json + scene_decorations.json
     -> datafiles/data/scenes/<room>.json (compact runtime schema, stable IDs preserved).
  2. Placeholder terrain tilesets (ts_d_*): procedural seamless textures with noise-edged blends,
     generated only for neighbour configurations that occur. Replaced when tex_* deliveries arrive.
  3. Rooms rm_sc_desert_frontier / rm_sc_caravan_basin / rm_sc_royal_expanse (tile layers +
     obj_manager), rm_intro (1920x1080 stage), rm_ending, and a rebuilt rm_menu.
  4. Object/script .yy registration, Included Files and room order.

Run from the project root after import_deliveries.py and build_placeholders.py.
"""
import glob
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
import gmyy  # noqa: E402
from art_common import periodic_noise  # noqa: E402

P = gmyy.PROJ
DESIGN = os.path.join(P, "design", "desert")
SCENE_ROOMS = ["rm_sc_desert_frontier", "rm_sc_caravan_basin", "rm_sc_royal_expanse"]
FACING = {0: "side", 2: "up", 4: "left", 6: "down"}
T = 64


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ====================================================================== 1. scene adapter
def place_of(places, cell):
    for p in places:
        r = p["rect"]
        if r[0] <= cell[0] <= r[2] and r[1] <= cell[1] <= r[3]:
            return p["name"]
    return None


def build_scene_data():
    manifest = load(os.path.join(DESIGN, "scene_manifest.json"))
    specs = load(os.path.join(DESIGN, "scene_gameplay_specs.json"))
    decor = load(os.path.join(DESIGN, "scene_decorations.json"))
    out = {}
    for sid in manifest["scene_order"]:
        sc = load(os.path.join(DESIGN, manifest["scene_files"][sid]))
        sp = specs[sid]
        room = sc["room_id"]
        w, h = sc["size_cells"]
        assert len(sc["terrain"]) == h and all(len(r) == w for r in sc["terrain"]), room
        places = [{"id": p["place_id"], "name": p["name"], "rect": p["rect"]} for p in sp["places"]]
        enemies = []
        for enc in sp["encounters"]:
            for e in enc["enemies"]:
                enemies.append({"id": e["id"], "family": e["enemy"], "cell": e["cell"], "leash": enc["leash_rect"],
                                "enc": enc["id"]})
        # cross-check against the core scene JSON
        core_enemies = sorted((o["enemy"], tuple(o["cell"])) for o in sc["objects"] if o["type"] == "enemy" and o["enemy"] != "pharaoh")
        spec_enemies = sorted((e["family"], tuple(e["cell"])) for e in enemies if e["family"] != "pharaoh")
        assert core_enemies == spec_enemies, (room, core_enemies, spec_enemies)
        chests = [{"id": c["id"], "cell": c["cell"], "loot": c["loot"], "interact": c["interaction_cell"],
                   "approach": c["approach_cell"]} for c in sp["chests"]]
        props = []
        for p in sp["solid_props"]:
            contract = "spr_palm_01" if p["prop"] == "palm" else "spr_" + p["prop"]
            props.append({"prop": p["prop"], "sprite": contract, "sprite_ph": "spr_ph_" + p["prop"],
                          "cell": p["cell"], "fp": p["footprint_px"]})
        decs = []
        for d in decor.get(sid, []):
            decs.append({"id": d["id"], "sprite": d["asset_id"], "sprite_ph": "spr_ph_" + d["asset_id"][4:],
                         "cell": d["cell"], "off": d.get("offset_px", [0, 0]),
                         "flat": d.get("layer") == "Visual_Assets"})
        cps = []
        for c in sp["checkpoints"]:
            pl = place_of(sp["places"], c["cell"]) or sc["display_name"]
            cps.append({"id": c["id"], "cell": c["cell"], "respawn": c["respawn_cell"], "safe": c["safe_rect"],
                        "quiet": c["quiet_rect"], "location": "%s — %s" % (pl, sc["display_name"])})
        exits = []
        for ex in sc["exits"]:
            tr = next(t for t in sp["transitions"] if t["exit_id"] == ex["id"])
            dest_sid = tr["to_scene_id"]
            dest_arr = next(a for a in specs[dest_sid]["arrivals"] if a["exit_id"] == tr["to_exit"])
            r1, r2 = ex["rows"]
            corridor = [w - 5, r1, w - 1, r2] if ex["side"] == "E" else [0, r1, 4, r2]
            exits.append({"id": ex["id"], "side": ex["side"], "rows": ex["rows"], "to_room": tr["to_room_id"],
                          "to_cell": tr["destination_arrival_cell"], "to_facing": FACING[dest_arr["facing"]],
                          "corridor": corridor})
        scripts = [{"id": s["id"], "rect": s["trigger_rect"], "event": s["event"], "once_flag": s["once_flag"]}
                   for s in sp["scripts"]]
        boss = None
        if sp.get("boss"):
            boss = dict(sp["boss"])
            enc = next(e for e in sp["encounters"] if e["id"].endswith(":boss"))
            boss["arena_rect"] = enc["combat_rect"]
        weather = {"sandstorm": sc["weather"].get("sandstorm", False),
                   "tumbleweeds": sc["weather"].get("tumbleweeds", False),
                   "suppress": sp["weather"]["suppress_rects"]}
        data = {"room": room, "scene_id": sid, "name": sc["display_name"], "w": w, "h": h,
                "terrain": sc["terrain"], "music": sc["music"], "weather": weather, "places": places,
                "props": props, "decor": decs, "chests": chests, "enemies": enemies, "checkpoints": cps,
                "exits": exits, "scripts": scripts, "boss": boss,
                "discoveries": [{"id": d["id"], "name": d["name"], "rect": d["rect"],
                                 "chest_id": d["chest_id"]} for d in sp.get("discoveries", [])],
                "initial": ({"cell": sp["initial_spawn"], "facing": "side"} if sp.get("initial_spawn") else None),
                "source": {"core": "design/desert/" + manifest["scene_files"][sid],
                           "gameplay": "design/desert/scene_gameplay_specs.json#" + sid,
                           "decor": "design/desert/scene_decorations.json#" + sid,
                           "design_version": manifest["design_version"]}}
        os.makedirs(os.path.join(P, "datafiles", "data", "scenes"), exist_ok=True)
        with open(os.path.join(P, "datafiles", "data", "scenes", room + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        out[room] = data
    return out


# ====================================================================== 2. tilesets
def tex(seed, base, var=0.08, scale=24, period=128, extra=None):
    n = periodic_noise(period, scale, seed, octaves=3)
    img = np.zeros((period, period, 3), np.float32)
    for c in range(3):
        img[..., c] = base[c] * (1 - var + 2 * var * n)
    if extra:
        img = extra(img, period)
    return np.clip(img, 0, 255)


def ripples(img, period):
    y, x = np.mgrid[0:period, 0:period]
    warp = periodic_noise(period, 48, 99, 2) * 6
    r = np.sin((x + y * 0.5 + warp * 8) / period * 2 * math.pi * 6)
    img *= (1 + 0.035 * r)[..., None]
    return img


def pebbly(img, period):
    rng = np.random.default_rng(5)
    for _ in range(period // 6):
        cx, cy = rng.integers(0, period, 2)
        rr = rng.uniform(1.5, 3.5)
        y, x = np.ogrid[0:period, 0:period]
        dx = np.minimum(abs(x - cx), period - abs(x - cx))
        dy = np.minimum(abs(y - cy), period - abs(y - cy))
        m = (dx * dx + dy * dy) <= rr * rr
        img[m] *= 0.82
    return img


def slabs(img, period):
    y, x = np.mgrid[0:period, 0:period]
    grout = ((x % 64) < 2) | ((y % 64) < 2) | (((x + 32 * ((y // 64) % 2)) % 64) < 2) & ((y % 32) < 2)
    img[grout] *= 0.72
    return img


def bricks(img, period):
    y, x = np.mgrid[0:period, 0:period]
    row = y // 16
    gx = (x + 16 * (row % 2)) % 32
    m = (gx < 2) | ((y % 16) < 2)
    img[m] *= 0.75
    return img


def crags(img, period):
    n = periodic_noise(period, 12, 31, 2)
    img *= (0.88 + 0.24 * n)[..., None]
    return img


TEX = {}


def textures():
    TEX["sand"] = tex(1, (214, 182, 132), 0.06, 40, 256, ripples)
    TEX["path"] = tex(2, (180, 146, 104), 0.08, 18, 128, pebbly)
    TEX["grass"] = tex(3, (116, 146, 74), 0.14, 10, 128)
    TEX["water"] = tex(4, (72, 142, 176), 0.10, 30, 128, ripples)
    TEX["shore"] = tex(5, (176, 146, 104), 0.05, 20, 128)
    TEX["paving"] = tex(6, (196, 178, 146), 0.06, 20, 128, slabs)
    TEX["chasm"] = tex(7, (40, 30, 36), 0.10, 20, 128)
    TEX["rock"] = tex(8, (168, 120, 82), 0.10, 16, 128, crags)
    TEX["rockface"] = tex(9, (128, 84, 58), 0.10, 10, 128)
    TEX["masonry"] = tex(10, (190, 168, 128), 0.05, 20, 128, bricks)
    TEX["masonryface"] = tex(11, (146, 122, 90), 0.05, 20, 128, bricks)
    TEX["plank"] = tex(12, (150, 104, 64), 0.08, 12, 128)
    TEX["stairs"] = tex(13, (190, 170, 136), 0.05, 20, 128)
    TEX["edgenoise"] = periodic_noise(128, 14, 77, 3)


def sample(name, vx, vy, period=128):
    t = TEX[name]
    p = t.shape[0]
    ox = (vx * T) % p
    oy = (vy * T) % p
    return t[oy:oy + T, ox:ox + T]


def field(occ3):
    """bilinear field of a 3x3 occupancy grid sampled over the centre cell (64x64)."""
    u = (np.arange(T) + 0.5) / T - 0.5
    yy, xx = np.meshgrid(1 + u, 1 + u, indexing="ij")
    return ndimage.map_coordinates(occ3.astype(np.float32), [yy, xx], order=1, mode="nearest")


def edge_alpha(occ3, vx, vy, amp=0.22, soft=0.06):
    f = field(occ3)
    nz = TEX["edgenoise"][(vy * T) % 128:(vy * T) % 128 + T, (vx * T) % 128:(vx * T) % 128 + T]
    f = f + (nz - 0.5) * amp * (1 - np.abs(f - 0.5) * 1.5).clip(0, 1)
    return np.clip((f - 0.5) / soft + 0.5, 0, 1), f


class Layer:
    def __init__(self, name):
        self.name = name
        self.keys = {}
        self.tiles = [np.zeros((T, T, 4), np.uint8)]

    def index(self, key, maker):
        if key not in self.keys:
            self.keys[key] = len(self.tiles)
            self.tiles.append(maker())
        return self.keys[key]


def rgba(rgb, a):
    out = np.zeros((T, T, 4), np.float32)
    out[..., :3] = rgb
    out[..., 3] = a * 255
    return np.clip(out, 0, 255).astype(np.uint8)


WALK = set(".,;_^=|")
BRIDGE = set("=|x")


def occ_of(terrain, x, y, members, w, h):
    o = np.zeros((3, 3), np.uint8)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            xx, yy = x + dx, y + dy
            xx = min(max(xx, 0), w - 1)
            yy = min(max(yy, 0), h - 1)
            o[dy + 1, dx + 1] = 1 if terrain[yy][xx] in members else 0
    return o


def bridge_under(terrain, x, y, w, h):
    water = chasm = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            xx, yy = min(max(x + dx, 0), w - 1), min(max(y + dy, 0), h - 1)
            c = terrain[yy][xx]
            water += c == "~"
            chasm += c in "Cx"
    return "~" if water > chasm else "C"


def make_blob(texname, occ, vx, vy, amp=0.22, soft=0.06, rim=None):
    a, f = edge_alpha(occ, vx, vy, amp, soft)
    rgb = sample(texname, vx, vy).copy()
    if rim is not None:
        edge = np.clip(1 - np.abs(f - 0.5) / 0.12, 0, 1)
        rgb = rgb * (1 - edge[..., None] * 0.35) + np.array(rim) * edge[..., None] * 0.35
    return rgba(rgb, a)


def make_water(occ, vx, vy):
    a_shore, f = edge_alpha(occ * 1.0, vx, vy, 0.18, 0.08)
    # shore band sits just outside the water edge
    fs = field(occ)
    shore_a = np.clip((fs - 0.36) / 0.06 + 0.5, 0, 1)
    water_a = np.clip((fs - 0.5) / 0.05 + 0.5, 0, 1)
    rgb = sample("shore", vx, vy) * (1 - water_a[..., None]) + sample("water", vx, vy) * water_a[..., None]
    hl = np.clip(1 - np.abs(fs - 0.52) / 0.03, 0, 1)
    rgb = rgb * (1 - hl[..., None] * 0.5) + np.array([210, 236, 240]) * hl[..., None] * 0.5
    return rgba(rgb, shore_a)


def make_chasm(occ, vx, vy):
    a, f = edge_alpha(occ, vx, vy, 0.18, 0.05)
    rgb = sample("chasm", vx, vy).copy()
    if occ[0, 1] == 0:
        y = np.arange(T)[:, None].repeat(T, 1)
        band = (y < 26)
        k = (y / 26.0)
        face = np.array([120, 92, 72]) * (1 - k[..., None] * 0.6)
        rgb[band] = face[band]
    rim = np.clip(1 - np.abs(f - 0.5) / 0.08, 0, 1)
    rgb = rgb * (1 - rim[..., None] * 0.5) + np.array([150, 122, 96]) * rim[..., None] * 0.5
    return rgba(rgb, a)


def make_wall(occ, own, vx, vy):
    masonry = own == "M"
    a, f = edge_alpha(occ, vx, vy, 0.06 if masonry else 0.24, 0.05)
    top = sample("masonry" if masonry else "rock", vx, vy).copy()
    face = sample("masonryface" if masonry else "rockface", vx, vy).copy()
    rgb = top
    if occ[2, 1] == 0:
        y = np.arange(T)[:, None].repeat(T, 1)
        fh = 30 if masonry else 34
        band = y >= (T - fh)
        k = (y - (T - fh)) / float(fh)
        shade = (0.95 - 0.35 * k)[..., None]
        if not masonry:
            xs = np.arange(T)[None, :].repeat(T, 0)
            stri = 0.92 + 0.08 * np.sin(xs / 3.0 + (vx * 7) % 13)
            shade = shade * stri[..., None]
        rgb = np.where(band[..., None], face * shade, rgb)
        lip = (y >= T - fh - 3) & (y < T - fh)
        rgb = np.where(lip[..., None], rgb * 0.6 + np.array([250, 230, 190]) * 0.4, rgb)
    rim = np.clip(1 - np.abs(f - 0.5) / 0.07, 0, 1)
    rgb = rgb * (1 - rim[..., None] * 0.55) + np.array([70, 46, 36]) * rim[..., None] * 0.55
    return rgba(rgb, a)


def make_stairs(variant, vx, vy):
    rgb = sample("stairs", vx, vy).copy()
    y = np.arange(T)[:, None].repeat(T, 1)
    step = (y % 16)
    rgb = rgb * (1.0 - 0.25 * (step >= 12))[..., None]
    rgb = rgb * (1.0 + 0.10 * (step < 2))[..., None]
    left, right = variant
    x = np.arange(T)[None, :].repeat(T, 0)
    if left:
        rgb[x < 6] *= 0.6
    if right:
        rgb[x >= T - 6] *= 0.6
    return rgba(rgb, np.ones((T, T)))


def make_bridge(kind, rails, vx, vy):
    rgb = sample("plank", vx, vy).copy()
    a = np.ones((T, T))
    y = np.arange(T)[:, None].repeat(T, 1)
    x = np.arange(T)[None, :].repeat(T, 0)
    if kind == "=":
        rgb = rgb * (1 - 0.3 * ((x % 16) < 2))[..., None]
        if rails[0]:
            rgb[y < 6] = [110, 82, 54]
        if rails[1]:
            rgb[y >= T - 6] = [110, 82, 54]
    elif kind == "|":
        rgb = rgb * (1 - 0.3 * ((y % 16) < 2))[..., None]
        if rails[0]:
            rgb[x < 6] = [110, 82, 54]
        if rails[1]:
            rgb[x >= T - 6] = [110, 82, 54]
    else:  # broken span: missing planks
        rgb = rgb * (1 - 0.3 * ((x % 16) < 2))[..., None]
        holes = ((x // 16 + vx) % 3 == 0) | ((x // 16 + vx + vy) % 4 == 1)
        a = np.where(holes, 0.0, 1.0)
        a = np.where((y < 6) | (y >= T - 6), 1.0, a)
        rgb[(y < 6) | (y >= T - 6)] = [96, 70, 48]
    return rgba(rgb, a)


def build_tilesets(scenes):
    textures()
    layers = {n: Layer(n) for n in ["sand", "path", "grass", "water", "paving", "chasm", "bridge", "walls"]}
    grids = {}
    for room, sc in scenes.items():
        ter = sc["terrain"]
        w, h = sc["w"], sc["h"]
        g = {n: [0] * (w * h) for n in layers}
        for y in range(h):
            for x in range(w):
                c = ter[y][x]
                vx, vy = x % 2, y % 2
                i = y * w + x
                g["sand"][i] = layers["sand"].index(("s", x % 4, y % 4),
                                                    lambda x=x, y=y: rgba(TEX["sand"][(y % 4) * T:(y % 4 + 1) * T,
                                                                                      (x % 4) * T:(x % 4 + 1) * T], np.ones((T, T))))
                if c == ",":
                    o = occ_of(ter, x, y, ",", w, h)
                    g["path"][i] = layers["path"].index(("p", o.tobytes(), vx, vy), lambda o=o, vx=vx, vy=vy: make_blob("path", o, vx, vy, 0.26, 0.07))
                elif c == ";":
                    o = occ_of(ter, x, y, ";", w, h)
                    g["grass"][i] = layers["grass"].index(("g", o.tobytes(), vx, vy), lambda o=o, vx=vx, vy=vy: make_blob("grass", o, vx, vy, 0.3, 0.06, rim=(80, 110, 50)))
                if c in "_^":
                    o = occ_of(ter, x, y, "_^", w, h)
                    g["paving"][i] = layers["paving"].index(("v", o.tobytes(), vx, vy), lambda o=o, vx=vx, vy=vy: make_blob("paving", o, vx, vy, 0.05, 0.04, rim=(120, 100, 80)))
                under = c
                if c in BRIDGE:
                    under = bridge_under(ter, x, y, w, h)
                if under == "~" or c == "~":
                    members = set("~") | {b for b in BRIDGE}
                    o = occ_of(ter, x, y, members, w, h)
                    g["water"][i] = layers["water"].index(("w", o.tobytes(), vx, vy), lambda o=o, vx=vx, vy=vy: make_water(o, vx, vy))
                elif under in "Cx" or c in "Cx":
                    members = set("Cx") | {b for b in BRIDGE}
                    o = occ_of(ter, x, y, members, w, h)
                    g["chasm"][i] = layers["chasm"].index(("c", o.tobytes(), vx, vy), lambda o=o, vx=vx, vy=vy: make_chasm(o, vx, vy))
                if c in BRIDGE:
                    if c == "=":
                        rails = (ter[max(y - 1, 0)][x] not in BRIDGE, ter[min(y + 1, h - 1)][x] not in BRIDGE)
                    elif c == "|":
                        rails = (ter[y][max(x - 1, 0)] not in BRIDGE, ter[y][min(x + 1, w - 1)] not in BRIDGE)
                    else:
                        rails = (True, True)
                    g["bridge"][i] = layers["bridge"].index(("b", c, rails, vx, vy), lambda c=c, r=rails, vx=vx, vy=vy: make_bridge(c, r, vx, vy))
                if c in "#M":
                    o = occ_of(ter, x, y, "#M", w, h)
                    g["walls"][i] = layers["walls"].index(("m", c, o.tobytes(), vx, vy), lambda o=o, c=c, vx=vx, vy=vy: make_wall(o, c, vx, vy))
                elif c == "^":
                    v = (ter[y][max(x - 1, 0)] != "^", ter[y][min(x + 1, w - 1)] != "^")
                    g["walls"][i] = layers["walls"].index(("st", v, vx, vy), lambda v=v, vx=vx, vy=vy: make_stairs(v, vx, vy))
        grids[room] = g
    proj = gmyy.Project()
    counts = {}
    for name, lay in layers.items():
        n = len(lay.tiles)
        # Keep the source and compiler-ready output atlas on the same grid.
        cols = int(math.ceil(math.sqrt(n)))
        rows = cols
        sheet = np.zeros((rows * T, cols * T, 4), np.uint8)
        for k, tile in enumerate(lay.tiles):
            r, c = divmod(k, cols)
            sheet[r * T:(r + 1) * T, c * T:(c + 1) * T] = tile
        spr = "spr_ts_d_" + name
        gmyy.write_sprite(proj, spr, [Image.fromarray(sheet, "RGBA")], (0, 0), "Sprites/Tilesets", fps=0.0,
                          bbox=(0, 0, cols * T - 1, rows * T - 1))
        # Count the complete source grid, including transparent padding cells.
        gmyy.write_tileset(proj, "ts_d_" + name, spr, rows * cols, cols, folder="Tile Sets/Desert")
        counts[name] = n
    proj.save()
    print("tilesets:", counts)
    return grids


# ====================================================================== 3. rooms
LAYERS = [  # name, depth, tileset key (contract section 7)
    ("Tiles_Floor", 700, "sand"), ("Tiles_Path", 650, "path"), ("Tiles_Grass", 600, "grass"),
    ("Tiles_Water", 550, "water"), ("Tiles_Paving", 500, "paving"), ("Tiles_Chasm", 450, "chasm"),
    ("Tiles_Bridge", 425, "bridge"), ("Tiles_Walls_Below", 300, "walls"),
]


def build_rooms(scenes, grids):
    proj = gmyy.Project()
    for room, sc in scenes.items():
        w, h = sc["w"], sc["h"]
        rw = gmyy.RoomWriter(proj, room, w * T, h * T, folder="Rooms/Desert", views=True)
        inst = [rw.instance("obj_manager", 64, 64)]
        rw.layers.append(gmyy.instance_layer("Instances", 0, inst))
        for name, depth, key in LAYERS:
            rw.layers.append(gmyy.tile_layer(name, depth, "ts_d_" + key, w, h, grids[room][key]))
        rw.layers.append(gmyy.background_layer("Background", 800, 0xFF84B6D6))
        rw.save()
    # opening stage
    rw = gmyy.RoomWriter(proj, "rm_intro", 1920, 1080, folder="Rooms/Story", views=True)
    rw.layers.append(gmyy.instance_layer("Instances", 0, [rw.instance("obj_intro", 0, 0)]))
    rw.layers.append(gmyy.background_layer("Background", 800, 0xFF84B6D6))
    rw.save()
    rw = gmyy.RoomWriter(proj, "rm_ending", 1280, 720, folder="Rooms/Story", views=False)
    rw.layers.append(gmyy.instance_layer("Instances", 0, []))
    rw.layers.append(gmyy.background_layer("Background", 800, 0xFF000000))
    rw.save()
    rw = gmyy.RoomWriter(proj, "rm_menu", 1280, 720, folder="Rooms", views=False)
    rw.layers.append(gmyy.instance_layer("Instances", 100, [rw.instance("obj_menu_manager", 0, 0)]))
    rw.layers.append(gmyy.background_layer("Background", 200, 0xFFFFFFFF, "spr_menu_background"))
    rw.save()
    proj.room_order = ["rm_menu", "rm_intro"] + SCENE_ROOMS + ["rm_ending", "rm_level_1", "rm_level_2"]
    proj.save()


# ====================================================================== 4. registration
OBJECTS = [
    # name, folder, parent, sprite, mask, persistent, visible
    ("obj_game", "Objects/Game", None, None, None, True, True),
    ("obj_manager", "Objects/Game", None, None, None, False, True),
    ("obj_menu_manager", "Objects/Menu", None, None, None, False, True),
    ("obj_player", "Objects/Game", None, "spr_dave_idle_down", "spr_mask_dave", False, True),
    ("obj_enemy", "Objects/Game/Enemies", "obj_enemy_parent", "spr_baddie_idle", "spr_mask_medium", False, True),
    ("obj_pharaoh", "Objects/Game/Enemies", "obj_enemy_parent", "spr_ph_pharaoh_idle", "spr_mask_pharaoh", False, True),
    ("obj_boss_ctrl", "Objects/Game/Encounters", None, None, None, False, True),
    ("obj_chest", "Objects/Level", "obj_collision_parent", "spr_chest", "spr_mask_unit", False, True),
    ("obj_checkpoint", "Objects/Level", None, "spr_ph_checkpoint_star", None, False, True),
    ("obj_spring", "Objects/Level", None, None, None, False, True),
    ("obj_pickup", "Objects/Level", None, None, None, False, True),
    ("obj_prop", "Objects/Level", "obj_collision_parent", "spr_ph_prop", "spr_mask_unit", False, True),
    ("obj_deco", "Objects/Level", None, None, None, False, True),
    ("obj_exit", "Objects/Level", None, None, None, False, False),
    ("obj_gate", "Objects/Level", None, None, None, False, True),
    ("obj_projectile", "Objects/Game/Combat", None, None, None, False, True),
    ("obj_hazard", "Objects/Game/Combat", None, None, None, False, True),
    ("obj_fx", "Objects/Game/Combat", None, None, None, False, True),
    ("obj_tumbleweed", "Objects/Level", None, None, None, False, True),
    ("obj_intro", "Objects/Story", None, None, None, False, True),
]


def register_code():
    proj = gmyy.Project()
    for name, folder, parent, spr, mask, pers, vis in OBJECTS:
        gmyy.write_object(proj, name, folder, parent=parent, sprite=spr, mask=mask, persistent=pers, visible=vis)
    for d in sorted(glob.glob(os.path.join(P, "scripts", "*"))):
        name = os.path.basename(d)
        if os.path.exists(os.path.join(d, name + ".gml")):
            gmyy.write_script_yy(proj, name, "Scripts")
    proj.save()
    # included files (datafiles/)
    with open(gmyy.YYP, encoding="utf-8") as f:
        yyp = gmyy.gm_loads(f.read())
    inc = []
    for path in sorted(glob.glob(os.path.join(P, "datafiles", "**", "*"), recursive=True)):
        if os.path.isdir(path):
            continue
        rel = os.path.relpath(os.path.dirname(path), P).replace("\\", "/")
        n = os.path.basename(path)
        inc.append({"$GMIncludedFile": "", "%Name": n, "CopyToMask": -1, "filePath": rel, "name": n,
                    "resourceType": "GMIncludedFile", "resourceVersion": "2.0"})
    yyp["IncludedFiles"] = inc
    gmyy.write_text(gmyy.YYP, gmyy.gm_dumps(yyp))
    print("registered %d objects, %d included files" % (len(OBJECTS), len(inc)))


def main():
    steps = set(sys.argv[1:]) or {"data", "tiles", "rooms", "code"}
    scenes = build_scene_data() if steps & {"data", "tiles", "rooms"} else None
    if "tiles" in steps or "rooms" in steps:
        grids = build_tilesets(scenes)
        build_rooms(scenes, grids)
    if "code" in steps:
        register_code()


if __name__ == "__main__":
    main()
