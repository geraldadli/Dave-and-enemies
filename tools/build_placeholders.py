"""
build_placeholders.py - generates clearly named placeholder sprites (spr_ph_*) and collision masks.

Placeholders stand in for undelivered contract art (ASSET_REQUESTS). They never use contract IDs:
runtime code looks up the contract ID first (asset_get_index) and only falls back to spr_ph_*, so an
imported delivery replaces a placeholder without code changes. Masks (spr_mask_*) are engineering
assets defined by PROJECT_CONTRACT section 6. Run from the project root.
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import gmyy  # noqa: E402
from art_common import Frame, star_points, mix, shade_col, light_col  # noqa: E402

PH = "Sprites/Placeholders"
FONT = os.path.join(gmyy.PROJ, "docs", "ui", "fonts", "NotoSans-Bold.ttf")
random.seed(7)


def save(proj, name, frames, origin, folder=PH, fps=10.0, bbox=None):
    gmyy.write_sprite(proj, name, frames, origin, folder, fps=fps, bbox=bbox)


# ------------------------------------------------------------------ masks
def masks(proj):
    for name, w, h in [("spr_mask_dave", 28, 14), ("spr_mask_medium", 32, 16), ("spr_mask_python", 48, 16),
                       ("spr_mask_sandworm", 64, 28), ("spr_mask_pharaoh", 72, 30), ("spr_mask_bat", 24, 12)]:
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse([0, 0, w - 1, h - 1], fill=(255, 0, 255, 160))
        save(proj, name, [im], (w // 2, h // 2), "Sprites/Masks", bbox=(0, 0, w - 1, h - 1))
    im = Image.new("RGBA", (64, 64), (255, 0, 255, 120))
    save(proj, "spr_mask_unit", [im], (32, 32), "Sprites/Masks", bbox=(0, 0, 63, 63))


# ------------------------------------------------------------------ props
SAND = (214, 182, 132)
OUT = (40, 28, 30)


def cactus(h, arms):
    w = 64 if h > 80 else 48
    f = Frame(w, h)
    cx = w / 2
    green = (96, 150, 78)
    body = f.capsule((cx, h - 8), (cx, 12), w * 0.17)
    f.part(body, green)
    for side, ay, ah in arms:
        x2 = cx + side * w * 0.3
        arm = f.capsule((cx, ay), (x2, ay), w * 0.09)
        arm = np.maximum(arm, f.capsule((x2, ay), (x2, ay - ah), w * 0.09))
        f.part(arm, mix(green, (120, 170, 90), 0.2))
    for i in range(6):
        y = 18 + i * (h - 30) / 6
        f.paint(f.line_mask([(cx - 2, y), (cx + 2, y + 3)], 1), (200, 220, 170), 0.6)
    return f.result()


def obelisk():
    f = Frame(96, 224)
    base = f.poly([(18, 212), (78, 212), (72, 196), (24, 196)])
    f.part(base, (150, 128, 100))
    shaft = f.poly([(34, 198), (62, 198), (56, 40), (40, 40)])
    f.part(shaft, (196, 170, 128))
    tip = f.poly([(40, 42), (56, 42), (48, 18)])
    f.part(tip, (232, 196, 110))
    for i in range(5):
        y = 70 + i * 24
        f.paint(f.line_mask([(44, y), (52, y)], 2), (120, 96, 70), 0.8)
    return f.result()


def palm(seed):
    rnd = random.Random(seed)
    f = Frame(128, 192)
    pts = [(64 + math.sin(t / 8.0) * 8, 184 - t * 1.25) for t in range(0, 120, 6)]
    trunk = f.ribbon(pts, [9 - i * 0.15 for i in range(len(pts))])
    f.part(trunk, (140, 100, 62))
    top = pts[-1]
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.55 + rnd.uniform(-0.1, 0.1)
        leaf = []
        for i in range(10):
            r = i * 6
            leaf.append((top[0] + math.cos(a) * r, top[1] + math.sin(a) * r + (i * i) * 0.35))
        f.part(f.ribbon(leaf, [2 + 4 * math.sin(i / 9 * math.pi) for i in range(10)]), (70, 140, 70))
    return f.result()


def wagon():
    f = Frame(192, 128)
    bed = f.poly([(20, 92), (172, 80), (176, 54), (24, 64)])
    f.part(bed, (132, 92, 56))
    for x in range(40, 170, 22):
        f.paint(f.line_mask([(x, 62), (x + 2, 88)], 2), (90, 60, 36), 0.8)
    for cx in (52, 140):
        wheel = f.ellipse(cx, 98, 20, 20)
        f.part(wheel, (110, 78, 50))
        f.paint(f.ellipse(cx, 98, 7, 7), (70, 50, 34))
    cloth = f.poly([(60, 64), (120, 58), (110, 30), (70, 36)])
    f.part(cloth, (210, 196, 160))
    return f.result()


def statue():
    f = Frame(128, 256)
    f.part(f.poly([(24, 244), (104, 244), (98, 214), (30, 214)]), (150, 128, 96))
    f.part(f.poly([(40, 216), (88, 216), (84, 110), (44, 110)]), (196, 164, 110))
    f.part(f.ellipse(64, 92, 22, 26), (206, 176, 120))
    f.part(f.poly([(34, 96), (94, 96), (82, 50), (46, 50)]), (60, 90, 150))
    f.part(f.poly([(46, 52), (82, 52), (64, 28)]), (230, 190, 90))
    return f.result()


def ruin_block(seed):
    rnd = random.Random(seed)
    f = Frame(96, 80)
    pts = [(10, 70), (86, 70), (82 + rnd.randint(-4, 4), 24), (60, 14 + rnd.randint(0, 8)), (18, 22)]
    f.part(f.poly(pts), (184, 156, 112))
    f.paint(f.line_mask([(20, 46), (76, 44)], 2), (120, 96, 70), 0.7)
    return f.result()


def tree_dead():
    f = Frame(128, 160)
    trunk = f.ribbon([(64, 152), (62, 110), (58, 70), (52, 40)], [9, 7, 5, 3])
    f.part(trunk, (110, 82, 60))
    for a, b, c in [((60, 90), (30, 60), (18, 52)), ((58, 70), (88, 40), (100, 36)), ((54, 52), (40, 26), (34, 18))]:
        f.part(f.ribbon([a, b, c], [4, 2.5, 1.5]), (104, 78, 58))
    return f.result()


def spring():
    f = Frame(128, 96)
    f.part(f.ellipse(64, 60, 56, 24), (150, 136, 110))
    f.part(f.ellipse(64, 58, 46, 18), (70, 150, 190), outline=None)
    f.paint(f.ellipse(52, 52, 14, 4), (210, 240, 250), 0.7)
    return f.result()


def bush(dead):
    f = Frame(64, 48)
    col = (150, 120, 80) if dead else (96, 140, 70)
    for cx, cy, r in [(22, 30, 13), (40, 28, 14), (32, 20, 12)]:
        f.part(f.ellipse(cx, cy, r, r * 0.8), col)
    return f.result()


def pebbles(seed):
    rnd = random.Random(seed)
    f = Frame(64, 64)
    for i in range(7):
        cx, cy = rnd.uniform(10, 54), rnd.uniform(14, 50)
        f.part(f.ellipse(cx, cy, rnd.uniform(3, 7), rnd.uniform(2, 5)), (160, 140, 110), ow=0.8)
    return f.result()


def skull():
    f = Frame(32, 32)
    f.part(f.ellipse(16, 14, 10, 9), (236, 228, 210))
    f.part(f.poly([(10, 18), (22, 18), (20, 26), (12, 26)]), (226, 218, 200))
    f.paint(f.ellipse(12, 14, 2.6, 2.6), (40, 30, 30))
    f.paint(f.ellipse(20, 14, 2.6, 2.6), (40, 30, 30))
    return f.result()


def tumbleweed():
    f = Frame(48, 48)
    m = np.zeros((f.H, f.W), np.float32)
    rnd = random.Random(3)
    for i in range(26):
        a1, a2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
        p1 = (24 + math.cos(a1) * 18, 24 + math.sin(a1) * 18)
        p2 = (24 + math.cos(a2) * 18, 24 + math.sin(a2) * 18)
        m = np.maximum(m, f.line_mask([p1, p2], 1.4))
    f.part(m, (170, 132, 82), ow=0.9, shade=0.2, hl=0.2)
    return f.result()


def entrance():
    f = Frame(384, 320)
    f.part(f.poly([(20, 300), (364, 300), (340, 60), (44, 60)]), (176, 150, 112))
    f.part(f.poly([(60, 64), (324, 64), (300, 20), (84, 20)]), (196, 168, 120))
    door = f.poly([(128, 300), (256, 300), (256, 140), (192, 100), (128, 140)])
    f.part(door, (24, 18, 22), shade=0.0, hl=0.0)
    for x in (80, 304):
        f.part(f.poly([(x - 18, 300), (x + 18, 300), (x + 14, 80), (x - 14, 80)]), (206, 180, 130))
    return f.result()


def star_frames():
    out = []
    for i in range(8):
        f = Frame(64, 64)
        s = 1.0 + 0.06 * math.sin(i / 8 * 6.283)
        pts = star_points(32, 30, 20 * s, 9 * s, rot=-math.pi / 2 + i * 0.05)
        f.glow(f.poly(pts), (255, 230, 120), sigma=4, strength=0.6)
        f.part(f.poly(pts), (255, 214, 72), outline=(150, 100, 30))
        f.paint(f.ellipse(27, 24, 4, 3), (255, 250, 220), 0.8)
        out.append(f.result())
    return out


def props(proj):
    save(proj, "spr_ph_prop", [ruin_block(1).resize((48, 40))], (24, 34))
    save(proj, "spr_ph_cactus_small", [cactus(64, [(1, 34, 10)])], (24, 58))
    save(proj, "spr_ph_cactus_tall", [cactus(128, [(-1, 70, 22), (1, 54, 26)])], (32, 120))
    save(proj, "spr_ph_obelisk", [obelisk()], (48, 212))
    save(proj, "spr_ph_palm", [palm(1)], (64, 184))
    save(proj, "spr_ph_wagon_wreck", [wagon()], (96, 112))
    save(proj, "spr_ph_pharaoh_statue", [statue()], (64, 244))
    save(proj, "spr_ph_ruin_block", [ruin_block(2)], (48, 70))
    save(proj, "spr_ph_tree_dead", [tree_dead()], (64, 150))
    save(proj, "spr_ph_healing_spring", [spring()], (64, 64))
    save(proj, "spr_ph_bush", [bush(False)], (32, 40))
    save(proj, "spr_ph_bush_dead", [bush(True)], (32, 40))
    save(proj, "spr_ph_pebbles", [pebbles(4)], (32, 32))
    save(proj, "spr_ph_skull", [skull()], (16, 20))
    save(proj, "spr_ph_tumbleweed", [tumbleweed()], (24, 24))
    save(proj, "spr_ph_dungeon_entrance", [entrance()], (192, 300))
    save(proj, "spr_ph_checkpoint_star", star_frames(), (32, 60))


# ------------------------------------------------------------------ icons
def icon(kind, col):
    f = Frame(64, 64)
    if kind == "potion":
        f.part(f.ellipse(32, 40, 16, 16), col)
        f.part(f.poly([(27, 26), (37, 26), (36, 12), (28, 12)]), (200, 220, 230))
        f.part(f.poly([(26, 12), (38, 12), (38, 7), (26, 7)]), (140, 100, 60))
        f.paint(f.ellipse(26, 34, 4, 6), (255, 230, 230), 0.7)
    elif kind == "sword":
        f.part(f.poly([(30, 52), (34, 52), (36, 10), (32, 4), (28, 10)]), col)
        f.part(f.poly([(20, 50), (44, 50), (44, 46), (20, 46)]), (200, 160, 70))
        f.part(f.capsule((32, 52), (32, 60), 3), (110, 70, 40))
    elif kind == "armor":
        f.part(f.poly([(14, 16), (50, 16), (54, 26), (46, 30), (46, 56), (18, 56), (18, 30), (10, 26)]), col)
        f.paint(f.line_mask([(32, 18), (32, 54)], 1.5), shade_col(col, 0.5), 0.8)
    elif kind == "coin":
        for cx, cy in [(26, 40), (38, 36), (32, 28)]:
            f.part(f.ellipse(cx, cy, 11, 8), col)
    elif kind == "rose":
        for a in range(6):
            r = math.radians(a * 60)
            f.part(f.ellipse(32 + math.cos(r) * 10, 34 + math.sin(r) * 8, 9, 6, rot=r), col)
    elif kind == "scarab":
        f.part(f.ellipse(32, 36, 14, 18), col)
        f.part(f.ellipse(32, 16, 8, 6), shade_col(col, 0.2))
        f.paint(f.line_mask([(32, 22), (32, 52)], 1.2), shade_col(col, 0.5), 0.8)
    elif kind == "ankh":
        f.part(f.ellipse(32, 18, 10, 12), col)
        f.paint(f.ellipse(32, 18, 5, 7), (0, 0, 0), 1.0)
        f.part(f.poly([(28, 28), (36, 28), (37, 58), (27, 58)]), col)
        f.part(f.poly([(14, 30), (50, 30), (50, 37), (14, 37)]), col)
    return f.result()


ICONS = {
    "potion_health": ("potion", (196, 48, 56)), "potion_greater": ("potion", (150, 24, 60)),
    "longsword": ("sword", (210, 214, 224)), "bandit_scimitar": ("sword", (196, 186, 160)),
    "sunsteel_blade": ("sword", (250, 220, 120)), "worn_tabard": ("armor", (226, 214, 190)),
    "wanderer_tunic": ("armor", (176, 150, 110)), "iron_tunic": ("armor", (150, 156, 166)),
    "paladin_mail": ("armor", (210, 220, 236)), "gold_coins": ("coin", (240, 196, 70)),
    "desert_rose": ("rose", (220, 160, 140)), "golden_scarab": ("scarab", (226, 184, 70)),
    "ancient_coin": ("coin", (190, 160, 110)), "pharaoh_ankh": ("ankh", (232, 196, 90)),
}


def icons(proj):
    for iid, (kind, col) in ICONS.items():
        save(proj, "spr_ph_icon_" + iid, [icon(kind, col)], (0, 0), "Sprites/Placeholders/Icons")


# ------------------------------------------------------------------ portraits
def portrait(name, label):
    im = Image.new("RGBA", (512, 512), (26, 30, 44, 255))
    d = ImageDraw.Draw(im)
    if name == "dave":
        src = Image.open(os.path.join(gmyy.PROJ, "art", "exports", "dave", "cardinal_v001",
                                      "dave_base_side_reference", "dave_base_side_reference_00.png")).convert("RGBA")
        bust = src.crop((20, 6, 76, 62)).resize((448, 448), Image.LANCZOS)
        im.alpha_composite(bust, (40, 70))
    else:
        f = Frame(512, 512, s=2)
        f.part(f.poly([(120, 512), (392, 512), (360, 300), (152, 300)]), (60, 90, 150))
        f.part(f.ellipse(256, 230, 80, 96), (150, 140, 110))
        f.part(f.poly([(150, 250), (362, 250), (330, 110), (182, 110)]), (60, 90, 150))
        f.part(f.poly([(182, 116), (330, 116), (256, 60)]), (230, 190, 90))
        f.paint(f.ellipse(226, 230, 14, 10), (255, 120, 60))
        f.paint(f.ellipse(286, 230, 14, 10), (255, 120, 60))
        im.alpha_composite(f.result())
    font = ImageFont.truetype(FONT, 30)
    d.rectangle([0, 456, 511, 511], fill=(16, 21, 33, 230))
    d.text((256, 484), label, font=font, fill=(234, 196, 119, 255), anchor="mm")
    return im


def portraits(proj):
    save(proj, "spr_ph_portrait_dave", [portrait("dave", "PLACEHOLDER  Dave")], (0, 0), "Sprites/Placeholders/Portraits")
    save(proj, "spr_ph_portrait_pharaoh", [portrait("pharaoh", "PLACEHOLDER  Pharaoh")], (0, 0),
         "Sprites/Placeholders/Portraits")


# ------------------------------------------------------------------ python / sandworm / pharaoh
def python_frames(kind, n):
    out = []
    for i in range(n):
        f = Frame(128, 96)
        ph = i / n * 6.283
        pts = []
        for k in range(14):
            x = 18 + k * 7
            amp = 7 if kind == "slither" else 2
            y = 72 - 6 + math.sin(ph + k * 0.7) * amp
            if kind == "coil":
                a = k * 0.55 + ph * 0.2
                r = 26 - k * 1.4
                x, y = 64 + math.cos(a) * r, 64 + math.sin(a) * r * 0.5
            pts.append((x, y))
        body = f.ribbon(pts, [3 + min(k, 13 - k) * 0.7 for k in range(14)])
        f.part(body, (120, 140, 60))
        hx, hy = pts[-1] if kind != "coil" else (64, 30 - 6 * math.sin(ph))
        f.part(f.ellipse(hx + 4, hy, 9, 6), (130, 150, 64))
        f.paint(f.ellipse(hx + 8, hy - 2, 1.6, 1.6), (20, 20, 20))
        out.append(f.result())
    return out


def worm_frames(kind, n):
    out = []
    for i in range(n):
        f = Frame(192, 192)
        k = i / max(1, n - 1)
        sand = (196, 160, 110)
        if kind == "mound":
            f.part(f.ellipse(96, 172, 46 + 4 * math.sin(i), 14), sand, shade=0.3)
        else:
            h = {"emerge": 40 + 100 * k, "idle": 140 + 6 * math.sin(i), "attack": 140 - 30 * math.sin(k * 3.14)}[kind]
            f.part(f.ellipse(96, 174, 54, 16), sand, shade=0.3)
            body = f.capsule((96, 172), (96 + (16 * math.sin(k * 3.14) if kind == "attack" else 0), 172 - h), 26, 22)
            f.part(body, (170, 110, 120))
            top = 172 - h
            f.part(f.ellipse(96, top, 26, 20), (150, 90, 100))
            if kind == "attack" and 0.3 < k < 0.8:
                f.paint(f.ellipse(96, top, 16, 12), (60, 20, 30))
            f.paint(f.ellipse(86, top - 6, 3, 3), (255, 220, 120))
            f.paint(f.ellipse(106, top - 6, 3, 3), (255, 220, 120))
        out.append(f.result())
    return out


def pharaoh_frames(cast, n):
    out = []
    for i in range(n):
        f = Frame(192, 192)
        ph = i / n * 6.283
        y0 = 150
        robe = f.poly([(64, y0), (128, y0), (116, 70), (76, 70)])
        f.part(robe, (60, 84, 140))
        f.part(f.poly([(80, 72), (112, 72), (108, 60), (84, 60)]), (230, 190, 90))
        f.part(f.ellipse(96, 46, 16, 18), (160, 150, 120))
        f.part(f.poly([(74, 52), (118, 52), (110, 18), (82, 18)]), (60, 84, 140))
        f.part(f.poly([(84, 20), (108, 20), (96, 4)]), (240, 200, 90))
        f.paint(f.ellipse(90, 46, 3, 2), (255, 120, 60))
        f.paint(f.ellipse(102, 46, 3, 2), (255, 120, 60))
        rod_a = -1.2 if cast else -0.5 + 0.1 * math.sin(ph)
        rx, ry = 124, 90
        tip = (rx + math.cos(rod_a) * 60, ry + math.sin(rod_a) * 60)
        f.part(f.capsule((rx, ry + 30), tip, 3), (200, 160, 60))
        f.glow(f.ellipse(tip[0], tip[1], 6, 6), (200, 120, 255), sigma=4, strength=0.8 if cast else 0.4)
        out.append(f.result())
    return out


def creatures(proj):
    save(proj, "spr_ph_python_slither", python_frames("slither", 8), (64, 72), "Sprites/Placeholders/Enemies", fps=12)
    save(proj, "spr_ph_python_coil", python_frames("coil", 6), (64, 72), "Sprites/Placeholders/Enemies", fps=12)
    save(proj, "spr_ph_sandworm_mound", worm_frames("mound", 6), (96, 176), "Sprites/Placeholders/Enemies")
    save(proj, "spr_ph_sandworm_emerge", worm_frames("emerge", 8), (96, 176), "Sprites/Placeholders/Enemies")
    save(proj, "spr_ph_sandworm_idle", worm_frames("idle", 6), (96, 176), "Sprites/Placeholders/Enemies")
    save(proj, "spr_ph_sandworm_attack", worm_frames("attack", 8), (96, 176), "Sprites/Placeholders/Enemies")
    save(proj, "spr_ph_pharaoh_idle", pharaoh_frames(False, 8), (96, 176), "Sprites/Placeholders/Enemies")
    save(proj, "spr_ph_pharaoh_cast", pharaoh_frames(True, 8), (96, 176), "Sprites/Placeholders/Enemies")


# ------------------------------------------------------------------ intro / ending
def intro_wall():
    w, h = 1920, 640
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rnd = random.Random(11)
    top = 300
    for x0 in range(0, w, 8):
        if 760 <= x0 < 1160:
            continue
        jag = 0 if not (700 < x0 < 1220) else rnd.randint(0, 120)
        d.rectangle([x0, top + jag + rnd.randint(-6, 6), x0 + 7, h], fill=(176, 150, 112, 255))
    for y in range(top, h, 32):
        off = 0 if (y // 32) % 2 else 32
        for x in range(-off, w, 64):
            if 760 <= x < 1160:
                continue
            d.rectangle([x, y, x + 62, y + 30], outline=(140, 116, 86, 255))
    for x in range(0, w, 96):
        if 680 <= x < 1220:
            continue
        d.rectangle([x, top - 40, x + 56, top], fill=(186, 160, 120, 255), outline=(140, 116, 86, 255))
    d.rectangle([0, h - 20, w, h], fill=(150, 126, 96, 255))
    return im


def rubble_frames():
    out = []
    for i in range(4):
        rnd = random.Random(20 + i)
        f = Frame(160, 100)
        for k in range(5):
            cx, cy = rnd.uniform(30, 130), rnd.uniform(50, 80)
            pts = [(cx + math.cos(a) * rnd.uniform(10, 24), cy + math.sin(a) * rnd.uniform(6, 14))
                   for a in np.linspace(0, 6.28, 7)[:-1]]
            f.part(f.poly(pts), (176, 150, 112))
        out.append(f.result())
    return out


def fallen_frames():
    out = []
    for i in range(3):
        f = Frame(128, 64)
        col = [(120, 70, 60), (90, 96, 120), (130, 110, 80)][i]
        f.part(f.ellipse(64, 40, 46, 13), col)
        f.part(f.ellipse(24 if i != 1 else 104, 36, 10, 9), (190, 180, 170))
        f.paint(f.line_mask([(30, 30), (100, 46)], 1.5), shade_col(col, 0.4), 0.6)
        out.append(f.result())
    return out


def ending_bg():
    im = Image.new("RGBA", (1280, 720), (10, 10, 14, 255))
    d = ImageDraw.Draw(im)
    for y in range(720):
        c = int(14 + 26 * (y / 720))
        d.line([(0, y), (1280, y)], fill=(c, c - 4, c - 8, 255))
    d.polygon([(470, 720), (810, 720), (790, 380), (640, 300), (490, 380)], fill=(30, 26, 26, 255))
    d.polygon([(540, 720), (740, 720), (740, 470), (640, 420), (540, 470)], fill=(6, 6, 8, 255))
    return im


def scenes_art(proj):
    save(proj, "spr_ph_intro_wall", [intro_wall()], (0, 0), "Sprites/Placeholders/Intro")
    save(proj, "spr_ph_intro_rubble", rubble_frames(), (80, 80), "Sprites/Placeholders/Intro")
    save(proj, "spr_ph_intro_fallen", fallen_frames(), (64, 40), "Sprites/Placeholders/Intro")
    save(proj, "spr_ph_ending_bg", [ending_bg()], (0, 0), "Sprites/Placeholders/Intro")


def main():
    proj = gmyy.Project()
    masks(proj)
    props(proj)
    icons(proj)
    portraits(proj)
    creatures(proj)
    scenes_art(proj)
    proj.save()
    print("placeholders written")


if __name__ == "__main__":
    main()
