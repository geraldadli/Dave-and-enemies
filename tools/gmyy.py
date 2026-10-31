"""
gmyy.py - writers for GameMaker (LTS 2026 / IDE 2026.0.0.16) resource files.

Every generated resource is registered in the .yyp so the project opens
directly in the IDE. Schema tags were copied from resources saved by the
same IDE version inside this project (see notes in tools/README.md).
"""
import json
import os
import re
import shutil
import struct
import uuid
import wave

PROJ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
YYP = os.path.join(PROJ, "Dave's & Enemies.yyp")
ORDER = os.path.join(PROJ, "Dave's & Enemies.resource_order")


def guid():
    return str(uuid.uuid4())


def short_id():
    return uuid.uuid4().hex[:8].upper()


# ---------------------------------------------------------------- JSON style
def _scalar(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15:
            return "%.1f" % v
        return repr(v)
    if isinstance(v, int):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def _inline(v):
    if isinstance(v, dict):
        return "{" + "".join(json.dumps(k) + ":" + _inline(x) + "," for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + "".join(_inline(x) + "," for x in v) + "]"
    return _scalar(v)


def gm_dumps(obj):
    """Top-level object pretty printed one key per line, nested values inline,
    lists of dicts one item per line - the layout the GameMaker IDE writes."""
    out = ["{"]
    for k, v in obj.items():
        key = json.dumps(k)
        if isinstance(v, list) and v and all(isinstance(x, (dict, list)) for x in v):
            out.append("  %s:[" % key)
            for x in v:
                out.append("    " + _inline(x) + ",")
            out.append("  ],")
        elif isinstance(v, dict) and len(json.dumps(v)) > 90:
            out.append("  %s:{" % key)
            for k2, v2 in v.items():
                out.append("    %s:%s," % (json.dumps(k2), _inline(v2)))
            out.append("  },")
        else:
            out.append("  %s:%s," % (key, _inline(v)))
    out.append("}")
    return "\n".join(out)


def gm_loads(text):
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return json.loads(text)


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ---------------------------------------------------------------- registry
class Project:
    """Collects resources and folders, then merges them into the .yyp."""

    def __init__(self):
        with open(YYP, encoding="utf-8") as f:
            self.yyp = gm_loads(f.read())
        self.added = {}
        self.removed = set()
        self.folders = set()
        self.room_order = None

    def folder(self, path):
        """path like 'Sprites/Dave/Walk' -> registers each level."""
        parts = path.split("/")
        for i in range(1, len(parts) + 1):
            self.folders.add("/".join(parts[:i]))
        name = parts[-1]
        return {"name": name, "path": "folders/%s.yy" % path}

    def add(self, kind, name):
        self.added[name] = "%s/%s/%s.yy" % (kind, name, name)

    def remove(self, kind, name):
        self.removed.add(name)
        d = os.path.join(PROJ, kind, name)
        if os.path.isdir(d):
            shutil.rmtree(d)

    def save(self):
        res = {r["id"]["name"]: r["id"]["path"] for r in self.yyp["resources"]}
        for n in self.removed:
            res.pop(n, None)
        res.update(self.added)
        self.yyp["resources"] = [
            {"id": {"name": n, "path": p}} for n, p in sorted(res.items(), key=lambda kv: kv[0].lower())
        ]
        existing = {f["folderPath"]: f for f in self.yyp["Folders"]}
        for fp in sorted(self.folders):
            key = "folders/%s.yy" % fp
            if key not in existing:
                name = fp.split("/")[-1]
                existing[key] = {"$GMFolder": "", "%Name": name, "folderPath": key, "name": name,
                                 "resourceType": "GMFolder", "resourceVersion": "2.0"}
        self.yyp["Folders"] = sorted(existing.values(), key=lambda f: f["folderPath"].lower())
        if self.room_order is not None:
            self.yyp["RoomOrderNodes"] = [
                {"roomId": {"name": r, "path": "rooms/%s/%s.yy" % (r, r)}} for r in self.room_order
            ]
        write_text(YYP, gm_dumps(self.yyp))
        # resource_order is optional; drop entries for removed resources
        if os.path.exists(ORDER):
            with open(ORDER, encoding="utf-8") as f:
                ro = gm_loads(f.read())
            ro["ResourceOrderSettings"] = [r for r in ro["ResourceOrderSettings"] if r["name"] in res]
            write_text(ORDER, gm_dumps(ro))


# ---------------------------------------------------------------- sprites
def _bbox_of(frames):
    l, t, r, b = 10 ** 9, 10 ** 9, -1, -1
    for im in frames:
        bb = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if bb:
            l, t = min(l, bb[0]), min(t, bb[1])
            r, b = max(r, bb[2] - 1), max(b, bb[3] - 1)
    if r < 0:
        return 0, 0, frames[0].width - 1, frames[0].height - 1
    return l, t, r, b


def write_sprite(proj, name, frames, origin, folder, fps=10.0, bbox=None, collision_kind=1,
                 events=None, nine_slice=None, htile=False, vtile=False):
    """frames: list of RGBA PIL images (same size). origin: (x, y) custom origin.
    bbox: None -> automatic, else (l, t, r, b) manual collision box in sprite pixels.
    events: {frame_index: "message"} broadcast messages (footsteps etc)."""
    d = os.path.join(PROJ, "sprites", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(os.path.join(d, "layers"))
    w, h = frames[0].size
    layer = guid()
    fids = []
    for im in frames:
        assert im.size == (w, h), name
        fid = guid()
        fids.append(fid)
        im.save(os.path.join(d, fid + ".png"))
        os.makedirs(os.path.join(d, "layers", fid))
        im.save(os.path.join(d, "layers", fid, layer + ".png"))
    if bbox is None:
        mode = 0
        l, t, r, b = _bbox_of(frames)
    else:
        mode = 2
        l, t, r, b = bbox
    path = "sprites/%s/%s.yy" % (name, name)
    keyframes = []
    for i, fid in enumerate(fids):
        keyframes.append({"$Keyframe<SpriteFrameKeyframe>": "", "Channels": {"0": {
            "$SpriteFrameKeyframe": "", "Id": {"name": fid, "path": path},
            "resourceType": "SpriteFrameKeyframe", "resourceVersion": "2.0"}},
            "Disabled": False, "id": guid(), "IsCreationKey": False, "Key": float(i), "Length": 1.0,
            "resourceType": "Keyframe<SpriteFrameKeyframe>", "resourceVersion": "2.0", "Stretch": False})
    ev_keys = []
    for fi, msg in sorted((events or {}).items()):
        ev_keys.append({"$Keyframe<MessageEventKeyframe>": "", "Channels": {"0": {
            "$MessageEventKeyframe": "", "Events": [msg], "resourceType": "MessageEventKeyframe",
            "resourceVersion": "2.0"}}, "Disabled": False, "id": guid(), "IsCreationKey": False,
            "Key": float(fi), "Length": 1.0, "resourceType": "Keyframe<MessageEventKeyframe>",
            "resourceVersion": "2.0", "Stretch": False})
    seq = {
        "$GMSequence": "v1", "%Name": name, "autoRecord": True, "backdropHeight": 768,
        "backdropImageOpacity": 0.5, "backdropImagePath": "", "backdropWidth": 1366,
        "backdropXOffset": 0.0, "backdropYOffset": 0.0,
        "events": {"$KeyframeStore<MessageEventKeyframe>": "", "Keyframes": ev_keys,
                   "resourceType": "KeyframeStore<MessageEventKeyframe>", "resourceVersion": "2.0"},
        "eventStubScript": None, "eventToFunction": {}, "length": float(len(frames)), "lockOrigin": False,
        "moments": {"$KeyframeStore<MomentsEventKeyframe>": "", "Keyframes": [],
                    "resourceType": "KeyframeStore<MomentsEventKeyframe>", "resourceVersion": "2.0"},
        "name": name, "playback": 1, "playbackSpeed": float(fps), "playbackSpeedType": 0,
        "resourceType": "GMSequence", "resourceVersion": "2.0", "showBackdrop": True,
        "showBackdropImage": False, "timeUnits": 1,
        "tracks": [{"$GMSpriteFramesTrack": "", "builtinName": 0, "events": [], "inheritsTrackColour": True,
                    "interpolation": 1, "isCreationTrack": False,
                    "keyframes": {"$KeyframeStore<SpriteFrameKeyframe>": "", "Keyframes": keyframes,
                                  "resourceType": "KeyframeStore<SpriteFrameKeyframe>", "resourceVersion": "2.0"},
                    "modifiers": [], "name": "frames", "resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0", "spriteId": None, "trackColour": 0, "tracks": [], "traits": 0}],
        "visibleRange": None, "volume": 1.0, "xorigin": int(origin[0]), "yorigin": int(origin[1]),
    }
    yy = {
        "$GMSprite": "v2", "%Name": name, "bboxMode": mode, "bbox_bottom": int(b), "bbox_left": int(l),
        "bbox_right": int(r), "bbox_top": int(t), "collisionKind": collision_kind, "collisionTolerance": 0,
        "DynamicTexturePage": False, "edgeFiltering": False, "For3D": False,
        "frames": [{"$GMSpriteFrame": "v1", "%Name": fid, "name": fid, "resourceType": "GMSpriteFrame",
                    "resourceVersion": "2.0"} for fid in fids],
        "gridX": 0, "gridY": 0, "height": h, "HTile": htile,
        "layers": [{"$GMImageLayer": "", "%Name": layer, "blendMode": 0, "displayName": "default",
                    "isLocked": False, "name": layer, "opacity": 100.0, "resourceType": "GMImageLayer",
                    "resourceVersion": "2.0", "visible": True}],
        "name": name, "nineSlice": nine_slice, "origin": 9, "parent": proj.folder(folder),
        "preMultiplyAlpha": False, "resourceType": "GMSprite", "resourceVersion": "2.0", "sequence": seq,
        "swatchColours": None, "swfPrecision": 2.525,
        "textureGroupId": {"name": "Default", "path": "texturegroups/Default"},
        "type": 0, "VTile": vtile, "width": w,
    }
    write_text(os.path.join(d, name + ".yy"), gm_dumps(yy))
    proj.add("sprites", name)
    return name


# ---------------------------------------------------------------- objects
EVENT_TYPES = {"Create": 0, "Destroy": 1, "Alarm": 2, "Step": 3, "Collision": 4, "Keyboard": 5,
               "Mouse": 6, "Other": 7, "Draw": 8, "KeyPress": 9, "KeyRelease": 10, "CleanUp": 12}


def write_object(proj, name, folder, parent=None, sprite=None, mask=None, persistent=False,
                 visible=True, solid=False):
    """Scans objects/<name>/*.gml for events (Create_0.gml, Step_2.gml, Draw_64.gml ...)."""
    d = os.path.join(PROJ, "objects", name)
    os.makedirs(d, exist_ok=True)
    events = []
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".dnd") or (fn.endswith(".yy")):
            if fn != name + ".yy":
                os.remove(os.path.join(d, fn))
            continue
        if not fn.endswith(".gml"):
            continue
        base = fn[:-4]
        etype, _, rest = base.partition("_")
        coll = None
        if etype == "Collision":
            num = 0
            coll = {"name": rest, "path": "objects/%s/%s.yy" % (rest, rest)}
        else:
            num = int(rest)
        events.append({"$GMEvent": "v1", "%Name": "", "collisionObjectId": coll, "eventNum": num,
                       "eventType": EVENT_TYPES[etype], "isDnD": False, "name": "",
                       "resourceType": "GMEvent", "resourceVersion": "2.0"})
    ref = lambda kind, n: None if n is None else {"name": n, "path": "%s/%s/%s.yy" % (kind, n, n)}
    yy = {
        "$GMObject": "", "%Name": name, "eventList": events, "managed": True, "name": name,
        "overriddenProperties": [], "parent": proj.folder(folder), "parentObjectId": ref("objects", parent),
        "persistent": persistent, "physicsAngularDamping": 0.1, "physicsDensity": 0.5,
        "physicsFriction": 0.2, "physicsGroup": 1, "physicsKinematic": False, "physicsLinearDamping": 0.1,
        "physicsObject": False, "physicsRestitution": 0.1, "physicsSensor": False, "physicsShape": 1,
        "physicsShapePoints": [], "physicsStartAwake": True, "properties": [], "resourceType": "GMObject",
        "resourceVersion": "2.0", "solid": solid, "spriteId": ref("sprites", sprite),
        "spriteMaskId": ref("sprites", mask), "visible": visible,
    }
    write_text(os.path.join(d, name + ".yy"), gm_dumps(yy))
    proj.add("objects", name)


# ---------------------------------------------------------------- scripts
def write_script_yy(proj, name, folder="Scripts"):
    d = os.path.join(PROJ, "scripts", name)
    os.makedirs(d, exist_ok=True)
    assert os.path.exists(os.path.join(d, name + ".gml")), name
    yy = {"$GMScript": "v1", "%Name": name, "isCompatibility": False, "isDnD": False, "name": name,
          "parent": proj.folder(folder), "resourceType": "GMScript", "resourceVersion": "2.0"}
    write_text(os.path.join(d, name + ".yy"), gm_dumps(yy))
    proj.add("scripts", name)


# ---------------------------------------------------------------- sounds
def write_sound(proj, name, wav_src, folder, compression=0, volume=1.0, preload=False):
    """compression: 0 uncompressed, 1 compressed, 2 uncompress on load, 3 compressed streamed."""
    d = os.path.join(PROJ, "sounds", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    dst = os.path.join(d, name + ".wav")
    shutil.copyfile(wav_src, dst)
    with wave.open(dst) as w:
        ch, rate, frames = w.getnchannels(), w.getframerate(), w.getnframes()
    yy = {"$GMSound": "v2", "%Name": name,
          "audioGroupId": {"name": "audiogroup_default", "path": "audiogroups/audiogroup_default"},
          "bitDepth": 1, "channelFormat": 1 if ch == 2 else 0, "compression": compression,
          "compressionQuality": 4, "conversionMode": 0, "duration": round(frames / rate, 6),
          "exportDir": "", "name": name, "parent": proj.folder(folder), "preload": preload,
          "resourceType": "GMSound", "resourceVersion": "2.0", "sampleRate": rate,
          "soundFile": name + ".wav", "volume": float(volume)}
    write_text(os.path.join(d, name + ".yy"), gm_dumps(yy))
    proj.add("sounds", name)


# ---------------------------------------------------------------- tilesets
def write_tileset(proj, name, sprite, count, columns, folder="Tile Sets", tile=64):
    d = os.path.join(PROJ, "tilesets", name)
    os.makedirs(d, exist_ok=True)
    # The compiler consumes this prepared image, not the source sprite PNG.
    # Keep it in sync with the indices/stride in the .yy on every rebuild.
    # Otherwise an IDE-generated image from an older layout can survive and
    # draw unrelated texture-page regions as terrain.
    import numpy as np
    from PIL import Image
    sprite_dir = os.path.join(PROJ, "sprites", sprite)
    with open(os.path.join(sprite_dir, sprite + ".yy"), encoding="utf-8") as f:
        source_meta = gm_loads(f.read())
    source = np.array(Image.open(os.path.join(sprite_dir, source_meta["frames"][0]["name"] + ".png")).convert("RGBA"))
    source_columns = source.shape[1] // tile
    assert count <= source_columns * (source.shape[0] // tile), name
    stride = tile + 4
    rows = (count + columns - 1) // columns
    packed = np.zeros((rows * stride, columns * stride, 4), dtype=np.uint8)
    for index in range(count):
        sy, sx = divmod(index, source_columns)
        cell = source[sy*tile:(sy+1)*tile, sx*tile:(sx+1)*tile]
        py, px = divmod(index, columns)
        packed[py*stride:(py+1)*stride, px*stride:(px+1)*stride] = np.pad(cell, ((2, 2), (2, 2), (0, 0)), mode="edge")
    Image.fromarray(packed, "RGBA").save(os.path.join(d, "output_tileset.png"))
    yy = {"$GMTileSet": "v1", "%Name": name, "autoTileSets": [],
          "macroPageTiles": {"SerialiseHeight": 0, "SerialiseWidth": 0, "TileSerialiseData": []},
          "name": name, "out_columns": columns, "out_tilehborder": 2, "out_tilevborder": 2,
          "parent": proj.folder(folder), "resourceType": "GMTileSet", "resourceVersion": "2.0",
          "spriteId": {"name": sprite, "path": "sprites/%s/%s.yy" % (sprite, sprite)},
          "spriteNoExport": True, "textureGroupId": {"name": "Default", "path": "texturegroups/Default"},
          "tileAnimationFrames": [], "tileAnimationSpeed": 15.0, "tileHeight": tile, "tilehsep": 0,
          "tilevsep": 0, "tileWidth": tile, "tilexoff": 0, "tileyoff": 0, "tile_count": count}
    write_text(os.path.join(d, name + ".yy"), gm_dumps(yy))
    proj.add("tilesets", name)


# ---------------------------------------------------------------- fonts
def write_font(proj, name, glyphs, atlas_img, font_name, size, style="Regular", bold=False,
               ranges=((32, 127),), folder="Fonts", line_height=0):
    d = os.path.join(PROJ, "fonts", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    atlas_img.save(os.path.join(d, name + ".png"))
    yy = {"$GMFont": "", "%Name": name, "AntiAlias": 1, "applyKerning": 0, "ascender": 0,
          "ascenderOffset": 0, "bold": bold, "canGenerateBitmap": True, "charset": 0, "first": 0,
          "fontName": font_name, "glyphOperations": 0,
          "glyphs": {str(c): g for c, g in sorted(glyphs.items())}, "hinting": 0, "includeTTF": False,
          "interpreter": 0, "italic": False, "kerningPairs": [], "last": 0, "lineHeight": line_height,
          "maintainGms1Font": False, "name": name, "parent": proj.folder(folder), "pointRounding": 0,
          "ranges": [{"lower": a, "upper": b} for a, b in ranges], "regenerateBitmap": False,
          "resourceType": "GMFont", "resourceVersion": "2.0",
          "sampleText": "abcdef ABCDEF\n0123456789 .,<>\"'&!?\nthe quick brown fox jumps over the lazy dog\nTHE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
          "sdfSpread": 8, "size": float(size), "styleName": style,
          "textureGroupId": {"name": "Default", "path": "texturegroups/Default"}, "TTFName": "",
          "usesSDF": False}
    text = gm_dumps(yy)
    # glyph table is written one glyph per line like the IDE does
    write_text(os.path.join(d, name + ".yy"), text)
    proj.add("fonts", name)


# ---------------------------------------------------------------- rooms
def tile_compress(cells):
    """GameMaker TileDataFormat 1: negative n -> run of next value n times,
    positive n -> n literal values follow."""
    out = []
    i, n = 0, len(cells)
    while i < n:
        j = i
        while j < n and cells[j] == cells[i]:
            j += 1
        run = j - i
        if run >= 2:
            out += [-run, cells[i]]
            i = j
        else:
            lit = [cells[i]]
            i += 1
            while i < n and (i + 1 >= n or cells[i] != cells[i + 1]):
                lit.append(cells[i])
                i += 1
            out += [len(lit)] + lit
    return out


def layer_common(name, depth, extra):
    base = {"%Name": name, "depth": depth, "effectEnabled": True, "effectType": None, "gridX": 64,
            "gridY": 64, "hierarchyFrozen": False, "inheritLayerDepth": False, "inheritLayerSettings": False,
            "inheritSubLayers": True, "inheritVisibility": True, "layers": [], "name": name,
            "properties": [], "userdefinedDepth": True, "visible": True}
    base.update(extra)
    return base


def tile_layer(name, depth, tileset, w, h, cells, visible=True):
    d = {"$GMRTileLayer": ""}
    d.update(layer_common(name, depth, {
        "resourceType": "GMRTileLayer", "resourceVersion": "2.0",
        "tiles": {"SerialiseHeight": h, "SerialiseWidth": w, "TileCompressedData": tile_compress(cells),
                  "TileDataFormat": 1},
        "tilesetId": {"name": tileset, "path": "tilesets/%s/%s.yy" % (tileset, tileset)},
        "visible": visible, "x": 0, "y": 0}))
    return d


def instance_layer(name, depth, instances, visible=True):
    d = {"$GMRInstanceLayer": ""}
    d.update(layer_common(name, depth, {"instances": instances, "resourceType": "GMRInstanceLayer",
                                        "resourceVersion": "2.0", "visible": visible}))
    return d


def asset_layer(name, depth, assets):
    d = {"$GMRAssetLayer": ""}
    d.update(layer_common(name, depth, {"assets": assets, "resourceType": "GMRAssetLayer",
                                        "resourceVersion": "2.0"}))
    return d


def background_layer(name, depth, colour, sprite=None):
    d = {"$GMRBackgroundLayer": ""}
    d.update(layer_common(name, depth, {
        "animationFPS": 30.0, "animationSpeedType": 0, "colour": colour, "hspeed": 0.0, "htiled": False,
        "resourceType": "GMRBackgroundLayer", "resourceVersion": "2.0",
        "spriteId": None if sprite is None else {"name": sprite, "path": "sprites/%s/%s.yy" % (sprite, sprite)},
        "stretch": False, "userdefinedAnimFPS": False, "visible": True, "vspeed": 0.0, "vtiled": False,
        "x": 0, "y": 0}))
    return d


def sprite_graphic(sprite, x, y, colour=0xFFFFFFFF, sx=1.0, sy=1.0, rot=0.0):
    n = "graphic_" + short_id()
    return {"$GMRSpriteGraphic": "v1", "%Name": n, "animationSpeed": 1.0, "colour": colour, "frozen": False,
            "headPosition": 0.0, "ignore": False, "inheritedItemId": None, "inheritItemSettings": False,
            "name": n, "resourceType": "GMRSpriteGraphic", "resourceVersion": "2.0", "rotation": float(rot),
            "scaleX": float(sx), "scaleY": float(sy),
            "spriteId": {"name": sprite, "path": "sprites/%s/%s.yy" % (sprite, sprite)},
            "x": float(x), "y": float(y)}


class RoomWriter:
    def __init__(self, proj, name, width, height, folder="Rooms/Desert", views=True):
        self.proj, self.name, self.w, self.h = proj, name, width, height
        self.folder, self.views = folder, views
        self.layers = []
        self.order = []
        self.creation = {}

    def instance(self, obj, x, y, code=None, sx=1.0, sy=1.0, colour=0xFFFFFFFF, rot=0.0):
        n = "inst_" + short_id()
        self.order.append(n)
        if code:
            self.creation[n] = code
        return {"$GMRInstance": "v4", "%Name": n, "colour": colour, "frozen": False,
                "hasCreationCode": bool(code), "ignore": False, "imageIndex": 0, "imageSpeed": 1.0,
                "inheritCode": False, "inheritedItemId": None, "inheritItemSettings": False, "isDnd": False,
                "name": n, "objectId": {"name": obj, "path": "objects/%s/%s.yy" % (obj, obj)},
                "properties": [], "resourceType": "GMRInstance", "resourceVersion": "2.0",
                "rotation": float(rot), "scaleX": float(sx), "scaleY": float(sy), "x": float(x), "y": float(y)}

    def save(self, room_creation_code=""):
        d = os.path.join(PROJ, "rooms", self.name)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        path = "rooms/%s/%s.yy" % (self.name, self.name)
        for n, code in self.creation.items():
            write_text(os.path.join(d, "InstanceCreationCode_%s.gml" % n), code)
        if room_creation_code:
            write_text(os.path.join(d, "RoomCreationCode.gml"), room_creation_code)
        view_on = {"hborder": 32, "hport": 720, "hspeed": -1, "hview": 720, "inherit": False, "objectId": None,
                   "vborder": 32, "visible": True, "vspeed": -1, "wport": 1280, "wview": 1280, "xport": 0,
                   "xview": 0, "yport": 0, "yview": 0}
        view_off = dict(view_on, visible=False)
        yy = {
            "$GMRoom": "v1", "%Name": self.name,
            "creationCodeFile": ("${project_dir}/rooms/%s/RoomCreationCode.gml" % self.name) if room_creation_code else "",
            "inheritCode": False, "inheritCreationOrder": False, "inheritLayers": False,
            "instanceCreationOrder": [{"name": n, "path": path} for n in self.order],
            "isDnd": False, "layers": self.layers, "name": self.name, "parent": self.proj.folder(self.folder),
            "parentRoom": None,
            "physicsSettings": {"inheritPhysicsSettings": False, "PhysicsWorld": False,
                                "PhysicsWorldGravityX": 0.0, "PhysicsWorldGravityY": 10.0,
                                "PhysicsWorldPixToMetres": 0.1},
            "resourceType": "GMRoom", "resourceVersion": "2.0",
            "roomSettings": {"Height": self.h, "inheritRoomSettings": False, "persistent": False,
                             "Width": self.w},
            "sequenceId": None,
            "views": [view_on if (self.views and i == 0) else view_off for i in range(8)],
            "viewSettings": {"clearDisplayBuffer": True, "clearViewBackground": False,
                             "enableViews": bool(self.views), "inheritViewSettings": False},
            "volume": 1.0,
        }
        write_text(os.path.join(d, self.name + ".yy"), gm_dumps(yy))
        self.proj.add("rooms", self.name)


# ---------------------------------------------------------------- audio io
def write_wav(path, samples, rate=44100):
    """samples: numpy float array, mono (n,) or stereo (n, 2), range -1..1"""
    import numpy as np
    a = np.asarray(samples, dtype=np.float64)
    a = np.clip(a, -1.0, 1.0)
    ch = 1 if a.ndim == 1 else a.shape[1]
    data = (a * 32767.0).astype("<i2").tobytes()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data)
