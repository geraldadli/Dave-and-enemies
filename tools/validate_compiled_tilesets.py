"""Check actual GameMaker 2026 .win tileset stride against compiler images.

python tools/validate_compiled_tilesets.py path/to/game.win
BGND/TPAG field layout: UndertaleModLib Models/UndertaleBackground.cs and
UndertaleTexturePageItem.cs (UnderminersTeam/UndertaleModTool).
"""
import json
from pathlib import Path
import struct
import sys
from PIL import Image
from preview_room import load_yy

ROOT = Path(__file__).resolve().parents[1]


def run(path):
    data = Path(path).read_bytes()
    assert data[:4] == b"FORM", "Not a GameMaker .win file"
    chunks = {}; offset = 8
    while offset+8 <= len(data):
        key, size = struct.unpack_from("<4sI", data, offset)
        chunks[key] = offset+8; offset += 8+size
    bg = chunks[b"BGND"]
    count = struct.unpack_from("<I", data, bg)[0]
    results = {}; errors = []
    for i in range(count):
        offset = struct.unpack_from("<I", data, bg+4+i*4)[0]
        fields = struct.unpack_from("<18I", data, offset)
        name = data[fields[0]:].split(b"\0", 1)[0].decode("utf-8")
        if not name.startswith("ts_d_"):
            continue
        if not fields[4]:
            errors.append(name+": compiled texture missing"); continue
        entry = struct.unpack_from("<11H", data, fields[4])
        directory = ROOT / "tilesets" / name
        meta = load_yy(str(directory / (name+".yy")))
        with Image.open(directory / "output_tileset.png") as image:
            expected_size = image.size
        actual_size = (entry[2], entry[3])
        cols, tiles = fields[12], fields[14]
        ok = (actual_size == expected_size and cols == meta["out_columns"]
              and tiles == meta["tile_count"] and actual_size[0] == cols*68)
        results[name] = dict(status="pass" if ok else "fail", columns=cols, tiles=tiles,
                             compiled_pixels=list(actual_size), expected_pixels=list(expected_size))
        if not ok:
            errors.append(name+": compiled atlas differs from exported stride/count")
    if len(results) != 8:
        errors.append("Expected eight current desert tilesets")
    report = dict(status="pass" if not errors else "fail", errors=errors, tilesets=results)
    (ROOT / "design/desert/runtime_tile_validation_report.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(f"{report['status'].upper()}: {len(results)} compiled atlases; {len(errors)} errors")
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1]))
