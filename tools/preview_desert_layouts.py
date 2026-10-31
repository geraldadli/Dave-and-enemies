"""Render generated .yy tile layers plus runtime scenery at camera/map scale.

Static composition review, not a GameMaker screenshot or a playtest.
python tools/preview_desert_layouts.py
"""
from functools import lru_cache
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from preview_room import load_yy, decompress, tileset_image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design/desert/previews"
ROOMS = ["rm_sc_desert_frontier", "rm_sc_caravan_basin", "rm_sc_royal_expanse"]


@lru_cache(None)
def sprite(names):
    for name in names:
        path = ROOT / "sprites" / name / (name+".yy")
        if path.exists():
            meta = load_yy(str(path))
            img = Image.open(path.parent / (meta["frames"][0]["name"]+".png")).convert("RGBA")
            if name == "spr_chest":
                # Match scene_chest_draw's template fallback.
                img = img.resize((round(img.width*1.6), round(img.height*1.6)), Image.Resampling.LANCZOS)
                return img, meta["sequence"]["xorigin"]*1.6, meta["sequence"]["yorigin"]*1.6+10
            return img, meta["sequence"]["xorigin"], meta["sequence"]["yorigin"]
    raise ValueError(f"Missing preview sprite: {names}")


@lru_cache(None)
def room_layers(room):
    meta = load_yy(str(ROOT / "rooms" / room / (room+".yy")))
    layers = []
    for layer in sorted(meta["layers"], key=lambda l: -l["depth"]):
        if "tiles" not in layer:
            continue
        tiles = layer["tiles"]
        w, h = tiles["SerialiseWidth"], tiles["SerialiseHeight"]
        sheet, cols = tileset_image(layer["tilesetId"]["name"])
        cells = decompress(tiles["TileCompressedData"], w*h)
        layers.append((w, h, cells, sheet, cols))
    return layers


def render(room, rect, scale=1, player=None):
    x1, y1, x2, y2 = rect
    tile = round(64*scale)
    scale = tile/64
    img = Image.new("RGBA", ((x2-x1+1)*tile, (y2-y1+1)*tile), "#d6b684")
    for w, h, cells, sheet, cols in room_layers(room):
        cache = {}
        for y in range(max(0, y1), min(h, y2+1)):
            for x in range(max(0, x1), min(w, x2+1)):
                v = cells[y*w+x] & 0x7ffff
                if not v:
                    continue
                if v not in cache:
                    sx, sy = (v % cols)*64, (v//cols)*64
                    cache[v] = sheet.crop((sx, sy, sx+64, sy+64)).resize((tile, tile), Image.Resampling.LANCZOS)
                img.alpha_composite(cache[v], ((x-x1)*tile, (y-y1)*tile))
    data = json.loads((ROOT / "datafiles/data/scenes" / (room+".json")).read_text(encoding="utf-8"))
    actors = []
    for obj in data["decor"]:
        actors.append((150 if obj["flat"] else -(obj["cell"][1]*64+32+obj["off"][1]),
                       obj["cell"], obj["off"], (obj["sprite"], obj["sprite_ph"])))
    for obj in data["props"]:
        actors.append((-(obj["cell"][1]*64+32), obj["cell"], [0, 0], (obj["sprite"], obj["sprite_ph"])))
    for obj in data["chests"]:
        actors.append((-(obj["cell"][1]*64+32), obj["cell"], [0, 0], ("spr_chest_desert", "spr_chest")))
    for obj in data["checkpoints"]:
        actors.append((-(obj["cell"][1]*64+32), obj["cell"], [0, 0], ("spr_checkpoint_star", "spr_ph_checkpoint_star")))
    if player:
        actors.append((-(player[1]*64+32), player, [0, 0], ("spr_dave_idle_down", "spr_player_idle")))
    for _, cell, off, names in sorted(actors, key=lambda a: -a[0]):
        art, ox, oy = sprite(names)
        px = (cell[0]*64+32+off[0]-ox-x1*64)*scale
        py = (cell[1]*64+32+off[1]-oy-y1*64)*scale
        if px+art.width*scale < 0 or py+art.height*scale < 0 or px >= img.width or py >= img.height:
            continue
        art = art.resize((max(1, round(art.width*scale)), max(1, round(art.height*scale))), Image.Resampling.LANCZOS)
        img.alpha_composite(art, (round(px), round(py)))
    return img.convert("RGB")


def main():
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
    heading = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 27)
    maps = []
    for room in ROOMS:
        data = json.loads((ROOT / "datafiles/data/scenes" / (room+".json")).read_text(encoding="utf-8"))
        im = render(room, [0, 0, data["w"]-1, data["h"]-1], .125)
        panel = Image.new("RGB", (im.width+32, im.height+96), "#17212d")
        d = ImageDraw.Draw(panel)
        d.text((16, 9), data["name"], font=heading, fill="#ffedcd")
        d.text((16, 46), "Generated room tiles + persistent scenery; enemies hidden for layout review", font=font, fill="#bccbd6")
        panel.paste(im, (16, 80)); panel.save(OUT / (data["scene_id"]+"_rendered.png")); maps.append(panel)
    atlas = Image.new("RGB", (max(m.width for m in maps), sum(m.height for m in maps)), "#17212d")
    y = 0
    for im in maps:
        atlas.paste(im, (0, y)); y += im.height
    atlas.save(OUT / "focused_world_rendered.png")

    # 20 x 12 tile crops, clipped to the actual 1280 x 720 view. No enemy
    # silhouettes obscure the persistent scenery being reviewed.
    views = [
        (ROOMS[0], [12, 39], "Arrival: breached-city baggage"),
        (ROOMS[0], [60, 35], "Split cliffs: framed crossing"),
        (ROOMS[0], [106, 40], "Oasis: green banks and resting place"),
        (ROOMS[1], [23, 42], "Caravan: cargo and cactus fork"),
        (ROOMS[1], [78, 48], "Bridge approach: bones and abandoned yard"),
        (ROOMS[1], [113, 41], "Ruins: quiet star and arcade"),
        (ROOMS[2], [80, 37], "Royal approach: processional remnants"),
        (ROOMS[2], [110, 68], "Sundial: a destination inside the landscape"),
        (ROOMS[2], [122, 38], "Final refuge: clear gate approach"),
    ]
    board = Image.new("RGB", (1920, len(views)//3*408+48), "#17212d")
    d = ImageDraw.Draw(board)
    d.text((16, 6), "Player-view composition review — generated assets, enemies hidden", font=heading, fill="#ffedcd")
    for i, (room, cell, title) in enumerate(views):
        x, y = cell
        # Player centre matches the continuous follow camera.
        im = render(room, [x-10, y-6, x+10, y+6], 1, player=cell)
        im = im.crop((32, 56, 1312, 776)).resize((640, 360), Image.Resampling.LANCZOS)
        bx, by = i % 3*640, i//3*408+48
        d.text((bx+12, by+6), title, font=font, fill="#ffedcd")
        board.paste(im, (bx, by+40))
    board.save(OUT / "focused_camera_review.png")
    specs = json.loads((ROOT/"design/desert/scene_gameplay_specs.json").read_text(encoding="utf-8"))
    discoveries = [(sp["room_id"],d) for sp in specs.values() for d in sp.get("discoveries",[])]
    discovery_board = Image.new("RGB", (1920, ((len(discoveries)+2)//3)*408+48), "#17212d")
    draw = ImageDraw.Draw(discovery_board)
    draw.text((16,6), "New discoveries — optional caches with returning trails",font=heading,fill="#ffedcd")
    for i,(room,discovery) in enumerate(discoveries):
        x,y = discovery["approach"]
        view = render(room,[x-10,y-6,x+10,y+6],1,player=[x,y])
        view = view.crop((32,56,1312,776)).resize((640,360),Image.Resampling.LANCZOS)
        bx,by = i%3*640,i//3*408+48
        draw.text((bx+12,by+6),discovery["name"],font=font,fill="#ffedcd")
        discovery_board.paste(view,(bx,by+40))
    discovery_board.save(OUT/"exploration_discoveries_review.png")
    print("Rendered three scene maps and nine player-camera compositions in", OUT)


if __name__ == "__main__":
    main()
