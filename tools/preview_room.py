"""
preview_room.py - renders a region of a generated room from its tile layers (static check of the
tile data written into the .yy, not an engine render).

  python tools/preview_room.py rm_sc_desert_frontier x1 y1 x2 y2 out.png
"""
import json
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import gmyy  # noqa: E402

P = gmyy.PROJ


def load_yy(path):
    with open(path, encoding="utf-8") as f:
        return gmyy.gm_loads(f.read())


def decompress(data, n):
    out = []
    i = 0
    while i < len(data) and len(out) < n:
        k = data[i]
        if k < 0:
            out += [data[i + 1]] * (-k)
            i += 2
        else:
            out += data[i + 1:i + 1 + k]
            i += 1 + k
    return out


def tileset_image(ts):
    t = load_yy(os.path.join(P, "tilesets", ts, ts + ".yy"))
    # Review the same prepared image consumed by GameMaker's compiler. Reading
    # only the source sprite hid stale output_tileset.png errors in old previews.
    sheet = Image.open(os.path.join(P, "tilesets", ts, "output_tileset.png")).convert("RGBA")
    cols = t["out_columns"]
    bx, by = t["out_tilehborder"], t["out_tilevborder"]
    tw, th = t["tileWidth"], t["tileHeight"]
    sx, sy = tw+2*bx, th+2*by
    assert sheet.width == cols*sx, (ts, "compiled atlas stride differs")
    rows = sheet.height//sy
    unbordered = Image.new("RGBA", (cols*tw, rows*th))
    for y in range(rows):
        for x in range(cols):
            unbordered.paste(sheet.crop((x*sx+bx, y*sy+by, x*sx+bx+tw, y*sy+by+th)), (x*tw, y*th))
    return unbordered, cols


def main():
    room, x1, y1, x2, y2, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
    r = load_yy(os.path.join(P, "rooms", room, room + ".yy"))
    W, H = (x2 - x1 + 1) * 64, (y2 - y1 + 1) * 64
    img = Image.new("RGBA", (W, H), (214, 182, 132, 255))
    layers = [l for l in r["layers"] if "tiles" in l]
    layers.sort(key=lambda l: -l["depth"])
    for l in layers:
        tw, th = l["tiles"]["SerialiseWidth"], l["tiles"]["SerialiseHeight"]
        cells = decompress(l["tiles"]["TileCompressedData"], tw * th)
        sheet, cols = tileset_image(l["tilesetId"]["name"])
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                v = cells[y * tw + x] & 0x7FFFF
                if v == 0:
                    continue
                sx, sy = (v % cols) * 64, (v // cols) * 64
                img.alpha_composite(sheet.crop((sx, sy, sx + 64, sy + 64)), ((x - x1) * 64, (y - y1) * 64))
    img.convert("RGB").save(out)
    print(out, img.size)


if __name__ == "__main__":
    main()
