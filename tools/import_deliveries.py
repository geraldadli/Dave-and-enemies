"""
import_deliveries.py - imports validated creative deliveries into GameMaker resources.

  * Dave v002 cardinal animations (art/exports/dave/*)  -> spr_dave_*
  * UI prototype frame kit (docs/ui/assets)             -> spr_ui_*
  * Noto Sans Regular/Bold (docs/ui/fonts)              -> fnt_ui_* (pre-rendered at exact pixel ems)
  * Production audio (audio/music|sfx|voice allowlist)   -> snd_* / mus_* + runtime catalog + audit

Every import is validated against its delivery sidecar first. Failures are reported and the
asset is skipped, never silently changed. Run from the project root:  python tools/import_deliveries.py
"""
import csv
import hashlib
import json
import os
import re
import sys
import wave

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import gmyy  # noqa: E402

P = gmyy.PROJ
REPORT = {"dave": [], "ui": [], "fonts": [], "audio": {}}


def rel(*a):
    return os.path.join(P, *a)


# ======================================================================= Dave
DAVE = [
    ("down_v001", "spr_dave_idle_down"),
    ("down_v001", "spr_dave_walk_down"),
    ("down_v001", "spr_dave_attack_down"),
    ("cardinal_v001", "spr_dave_walk_side"),
    ("cardinal_v001", "spr_dave_attack_side"),
    ("cardinal_v001", "spr_dave_walk_left"),
    ("cardinal_v001", "spr_dave_attack_left"),
    ("cardinal_v001", "spr_dave_walk_up"),
    ("cardinal_v001", "spr_dave_attack_up"),
]
DAVE_BASES = [
    ("down_v001", "dave_base_down_reference", "spr_dave_base_down"),
    ("cardinal_v001", "dave_base_side_reference", "spr_dave_base_side"),
    ("cardinal_v001", "dave_base_left_reference", "spr_dave_base_left"),
    ("cardinal_v001", "dave_base_up_reference", "spr_dave_base_up"),
]


def load_frames(folder, asset, count):
    frames = []
    for i in range(count):
        f = os.path.join(folder, "%s_%02d.png" % (asset, i))
        im = Image.open(f)
        frames.append(im)
    return frames


def check_frames(asset, frames, canvas, strip_path):
    errs = []
    for i, im in enumerate(frames):
        if im.mode != "RGBA":
            errs.append("%s f%d mode %s" % (asset, i, im.mode))
        if list(im.size) != list(canvas):
            errs.append("%s f%d size %s != %s" % (asset, i, im.size, canvas))
        a = im.convert("RGBA").getchannel("A")
        w, h = im.size
        border = [a.getpixel((x, 0)) for x in range(w)] + [a.getpixel((x, h - 1)) for x in range(w)]
        border += [a.getpixel((0, y)) for y in range(h)] + [a.getpixel((w - 1, y)) for y in range(h)]
        if max(border) != 0:
            errs.append("%s f%d border alpha %d" % (asset, i, max(border)))
    if strip_path and os.path.exists(strip_path):
        strip = Image.open(strip_path).convert("RGBA")
        w, h = canvas
        if strip.size != (w * len(frames), h):
            errs.append("%s strip size %s" % (asset, strip.size))
        else:
            for i, im in enumerate(frames):
                if strip.crop((i * w, 0, (i + 1) * w, h)).tobytes() != im.convert("RGBA").tobytes():
                    errs.append("%s strip/frame %d differ" % (asset, i))
    return errs


def import_dave(proj):
    for batch, asset in DAVE:
        folder = rel("art", "exports", "dave", batch, asset)
        meta = json.load(open(os.path.join(folder, asset + ".json"), encoding="utf-8"))
        canvas = meta["canvas_px"]
        origin = meta["origin_px"]
        n = meta.get("frame_count") or len(meta.get("source_frames", []))
        frames = load_frames(folder, asset, n)
        strip = os.path.join(folder, "%s_strip%d.png" % (asset, n))
        errs = check_frames(asset, frames, canvas, strip)
        ticks = meta.get("game_ticks_per_frame")
        step = meta.get("step_frames") or meta.get("contact_frames")
        rec = {"asset": asset, "source": os.path.relpath(folder, P).replace("\\", "/"), "frames": n,
               "canvas": canvas, "origin": origin, "fps": meta.get("fps"), "ticks": ticks,
               "step_frames": step, "errors": errs,
               "delivery_status": meta.get("status"),
               "verified_engine_ready_in_delivery": meta.get("verified_engine_ready")}
        REPORT["dave"].append(rec)
        if errs:
            print("DAVE REJECT", asset, errs)
            continue
        fps = meta.get("fps") or 20
        gmyy.write_sprite(proj, asset, [f.convert("RGBA") for f in frames], origin, "Sprites/Dave",
                          fps=float(fps))
    for batch, src, name in DAVE_BASES:
        folder = rel("art", "exports", "dave", batch, src)
        meta = json.load(open(os.path.join(folder, src + ".json"), encoding="utf-8"))
        im = Image.open(os.path.join(folder, src + "_00.png"))
        canvas = meta.get("canvas_px", [96, 96])
        origin = meta.get("origin_px", [48, 88])
        errs = check_frames(src, [im], canvas, None)
        REPORT["dave"].append({"asset": name, "source": os.path.relpath(folder, P).replace("\\", "/"),
                               "frames": 1, "canvas": canvas, "origin": origin,
                               "use": "idle fallback for this facing (reference base, not an animation)",
                               "errors": errs})
        if not errs:
            gmyy.write_sprite(proj, name, [im.convert("RGBA")], origin, "Sprites/Dave", fps=1.0)


# ======================================================================= UI kit
UI_KIT = [
    ("spr_ui_panel", ["spr_ui_panel.png"]),
    ("spr_ui_hp_frame", ["spr_ui_hp_frame.png"]),
    ("spr_ui_hp_fill", ["spr_ui_hp_fill.png"]),
    ("spr_ui_slot", ["spr_ui_slot.png"]),
    ("spr_ui_slot_selected", ["spr_ui_slot_selected.png"]),
    ("spr_ui_button", ["spr_ui_button_00.png", "spr_ui_button_01.png", "spr_ui_button_02.png"]),
    ("spr_ui_save_card", ["spr_ui_save_card_00.png", "spr_ui_save_card_01.png", "spr_ui_save_card_02.png"]),
    ("spr_ui_save_card_empty", ["spr_ui_save_card_empty_00.png", "spr_ui_save_card_empty_01.png",
                                "spr_ui_save_card_empty_02.png"]),
]


def import_ui(proj):
    sizes = {}
    with open(rel("docs", "ui", "UI_ASSETS.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            m = re.fullmatch(r"(\d+)x(\d+)", r["source_size"].strip())
            if m:
                sizes[r["asset_id"]] = (int(m.group(1)), int(m.group(2)))
    for name, files in UI_KIT:
        frames = [Image.open(rel("docs", "ui", "assets", fn)) for fn in files]
        errs = []
        for fn, im in zip(files, frames):
            if im.mode != "RGBA":
                errs.append("%s mode %s" % (fn, im.mode))
            if name in sizes and im.size != sizes[name]:
                errs.append("%s size %s != %s" % (fn, im.size, sizes[name]))
        REPORT["ui"].append({"asset": name, "frames": len(files), "size": list(frames[0].size), "errors": errs,
                             "status": "supplied prototype frame kit (not production-final)"})
        if errs:
            print("UI REJECT", name, errs)
            continue
        gmyy.write_sprite(proj, name, [im.convert("RGBA") for im in frames], (0, 0), "Sprites/UI", fps=0.0,
                          bbox=(0, 0, frames[0].width - 1, frames[0].height - 1))


# ======================================================================= fonts
FONTS = [
    # resource, file, pixel em, line box, bold
    ("fnt_ui_meta", "NotoSans-Regular.ttf", 18, 24, False),
    ("fnt_ui_body", "NotoSans-Regular.ttf", 23, 30, False),
    ("fnt_ui_heading", "NotoSans-Bold.ttf", 28, 36, True),
    ("fnt_ui_dialogue", "NotoSans-Regular.ttf", 28, 36, False),
    ("fnt_ui_title", "NotoSans-Bold.ttf", 46, 58, True),
]
EXTRA_GLYPHS = [215, 8212, 8217, 8220, 8221, 8230, 8226]  # x  —  ’  “  ”  …  •


def build_font(proj, name, ttf, px, line_box, bold):
    font = ImageFont.truetype(rel("docs", "ui", "fonts", ttf), px)
    ascent, descent = font.getmetrics()
    cell_h = ascent + descent
    chars = list(range(32, 127)) + EXTRA_GLYPHS
    glyphs, imgs = {}, []
    for c in chars:
        ch = chr(c)
        adv = font.getlength(ch)
        l, t, r, b = font.getbbox(ch, anchor="ls")
        l = min(0, l) if c == 32 else l
        w = max(1, int(round(r - l)) + 2) if c != 32 else max(1, int(round(adv)))
        im = Image.new("L", (w, cell_h), 0)
        if c != 32:
            ImageDraw.Draw(im).text((1 - l, ascent), ch, font=font, fill=255, anchor="ls")
        imgs.append((c, im, int(round(adv)), int(round(l)) - 1 if c != 32 else 0))
    # pack rows into a power-of-two-ish atlas
    width = 512 if px < 40 else 1024
    x = y = 2
    for c, im, adv, off in imgs:
        if x + im.width + 2 > width:
            x = 2
            y += cell_h + 2
        glyphs[c] = {"character": c, "h": cell_h, "offset": off, "shift": adv, "w": im.width, "x": x, "y": y}
        x += im.width + 2
    height = y + cell_h + 2
    atlas = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    for c, im, adv, off in imgs:
        g = glyphs[c]
        white = Image.new("RGBA", im.size, (255, 255, 255, 255))
        white.putalpha(im)
        atlas.paste(white, (g["x"], g["y"]))
    ranges = [(32, 126)] + [(c, c) for c in EXTRA_GLYPHS]
    gmyy.write_font(proj, name, glyphs, atlas, "Noto Sans", round(px * 0.75, 2),
                    style="Bold" if bold else "Regular", bold=bold, ranges=ranges, folder="Fonts/UI")
    REPORT["fonts"].append({"resource": name, "file": "docs/ui/fonts/" + ttf, "pixel_em": px,
                            "line_box": line_box, "cell_height": cell_h, "ascent": ascent,
                            "glyph_count": len(glyphs),
                            "method": "pre-rendered from supplied static TTF with FreeType at exact pixel em"})


def import_fonts(proj):
    for args in FONTS:
        build_font(proj, *args)
    # ship the licence with the distributed font glyphs
    os.makedirs(rel("datafiles", "licenses"), exist_ok=True)
    with open(rel("docs", "ui", "fonts", "OFL.txt"), "rb") as s, open(rel("datafiles", "licenses", "OFL.txt"), "wb") as d:
        d.write(s.read())


# ======================================================================= audio
WARNING_IDS = {"snd_undead_attack", "snd_skeleton_warrior_attack", "snd_bandit_attack", "snd_bow_draw",
               "snd_cast_charge", "snd_bat_screech", "snd_snake_hiss", "snd_worm_rumble", "snd_laser_charge",
               "snd_thunder_warn", "snd_summon_crack"}
PROJECTILE_IDS = {"snd_arrow_travel", "snd_magic_travel"}
NONSPATIAL_GROUPS = {"Music", "UI", "Text"}
NONSPATIAL_IDS = {"snd_wind_loop", "snd_intro_grit", "snd_intro_banner", "snd_hurt", "snd_player_defeated",
                  "snd_potion_drink", "snd_heal", "snd_levelup", "snd_checkpoint", "snd_save", "snd_pickup",
                  "snd_coin", "snd_sword_swing", "snd_step_sand", "snd_step_stone", "snd_step_wood",
                  "snd_boss_death", "snd_disintegrate", "snd_gate_slam", "snd_gate_open"}
COLLISION_RENAME = {"snd_player_defeated": "snd_player_defeated_1"}  # template resource keeps its name


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def budget_group(aid, group):
    if group == "Music":
        return "music"
    if group == "Text":
        return "text"
    if group == "UI":
        return "ui"
    if aid == "snd_wind_loop":
        return "weather"
    if aid in WARNING_IDS:
        return "warning"
    if aid in PROJECTILE_IDS:
        return "projectile"
    if aid.endswith("_move") or aid.startswith("snd_step_") or aid in ("snd_bat_fly", "snd_boss_float"):
        return "movement"
    return "sfx"


def import_audio(proj, do_write=True):
    manifest = json.load(open(rel("docs", "audio", "AUDIO_MANIFEST.json"), encoding="utf-8"))
    with open(rel("docs", "audio", "AUDIO_CUE_SHEET.csv"), encoding="utf-8-sig") as f:
        cues = {r["id"]: r for r in csv.DictReader(f)}
    template_sounds = set(os.listdir(rel("sounds")))
    audit, catalog, errors = [], {}, []
    seen = set()
    for a in manifest["assets"]:
        aid = a["id"]
        files = a["existing_delivered_files"]
        cue = cues.get(aid)
        if cue is None:
            errors.append("no cue sheet row for " + aid)
            continue
        sidecar_path = rel(os.path.dirname(files[0]), aid + ".json")
        sidecar = json.load(open(sidecar_path, encoding="utf-8")) if os.path.exists(sidecar_path) else {}
        side_files = {os.path.basename(x["path"]): x for x in sidecar.get("files", [])}
        res_names = []
        for fpath in files:
            src = rel(fpath)
            base = os.path.splitext(os.path.basename(fpath))[0]
            res = COLLISION_RENAME.get(base, base)
            row = {"id": aid, "file": fpath, "resource": res, "errors": []}
            if fpath in seen:
                row["errors"].append("duplicate allowlist entry")
            seen.add(fpath)
            if not os.path.exists(src):
                row["errors"].append("missing")
                audit.append(row)
                continue
            if res in template_sounds and res not in COLLISION_RENAME.values():
                row["errors"].append("collides with template resource")
            sf = side_files.get(os.path.basename(fpath))
            digest = sha256(src)
            row["sha256"] = digest
            if sf is None:
                # single-file music sidecars keep the hash at top level
                exp = sidecar.get("sha256")
                exp_frames = sidecar.get("frames")
            else:
                exp = sf.get("sha256")
                exp_frames = sf.get("frames")
            row["sha256_expected"] = exp
            if exp is None:
                row["errors"].append("no sidecar hash")
            elif exp != digest:
                row["errors"].append("sha256 mismatch")
            with wave.open(src) as w:
                ch, rate, sw, frames = w.getnchannels(), w.getframerate(), w.getsampwidth(), w.getnframes()
                comp = w.getcomptype()
            row.update({"channels": ch, "rate": rate, "bits": sw * 8, "frames": frames,
                        "duration": round(frames / rate, 6), "frames_expected": exp_frames})
            want_ch = 2 if a["group"] == "Music" else 1
            if comp != "NONE" or sw != 2 or rate != 44100:
                row["errors"].append("format %s %d-bit %d Hz" % (comp, sw * 8, rate))
            if ch != want_ch:
                row["errors"].append("channels %d != %d" % (ch, want_ch))
            if exp_frames is not None and abs(int(exp_frames) - frames) > 1:
                row["errors"].append("frames %d != sidecar %s" % (frames, exp_frames))
            dur = float(a.get("duration_seconds_per_file") or 0)
            if dur and abs(frames / rate - dur) > 0.002:
                # nominal manifest duration; the per-file sidecar frame count above is authoritative
                row["warning"] = "duration %.6f differs from nominal %.3f" % (frames / rate, dur)
            loop = a.get("loop") or {}
            if loop.get("enabled"):
                le = float(loop.get("loop_end"))
                if abs(le * 44100 - frames) > 1:
                    row["errors"].append("loop_end %.3f does not match file length" % le)
            audit.append(row)
            if row["errors"]:
                errors.append("%s: %s" % (fpath, row["errors"]))
                continue
            looped = bool(loop.get("enabled"))
            # loops and SFX stay uncompressed for sample-accurate seams and instant starts;
            # long non-looping music is compressed (not streamed) to keep the package small.
            compression = 1 if (a["group"] == "Music" and not looped) else 0
            folder = "Sounds/Production/" + {"Music": "Music", "Text": "Voice"}.get(a["group"], a["group"])
            if do_write:
                gmyy.write_sound(proj, res, src, folder, compression=compression)
            row["compression"] = compression
            res_names.append(res)
        g = budget_group(aid, a["group"])
        catalog[aid] = {
            "res": res_names,
            "db": float(cue["relative_gain_db"] or 0),
            "bus": cue["bus"],
            "grp": g,
            "pe": int(cue["simultaneous_limit_per_emitter"] or 1),
            "gl": int(cue["simultaneous_limit_global_for_id"] or 1),
            "rt": int(cue["minimum_retrigger_ms"] or 0),
            "pr": int(cue["priority_0_to_100"] or 50),
            "loop": cue["loop"] == "True",
            "fi": int(cue["fade_in_ms"] or 0),
            "fo": int(cue["fade_out_ms_on_stop"] or 0),
            "sp": not (a["group"] in NONSPATIAL_GROUPS or aid in NONSPATIAL_IDS),
        }
    total = len(audit)
    ok = sum(1 for r in audit if not r["errors"])
    summary = {"production_files": total, "passed": ok, "stable_ids": len(manifest["assets"]),
               "music": sum(1 for r in audit if r["file"].startswith("audio/music/")),
               "sfx": sum(1 for r in audit if r["file"].startswith("audio/sfx/")),
               "voice": sum(1 for r in audit if r["file"].startswith("audio/voice/")),
               "excluded": ["audio/previews/*.wav (review reels)", "audio/*.zip (convenience bundles)",
                            "audio/music/*.score.json", "template sounds/*"],
               "collision_renames": COLLISION_RENAME, "errors": errors}
    REPORT["audio"] = summary
    os.makedirs(rel("docs", "audio"), exist_ok=True)
    with open(rel("docs", "audio", "audio_import_audit.json"), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "files": audit}, f, indent=1)
    with open(rel("datafiles", "data", "audio_catalog.json"), "w", encoding="utf-8") as f:
        json.dump({"schema": 1, "source": "docs/audio/AUDIO_CUE_SHEET.csv + AUDIO_MANIFEST.json",
                   "budgets": {"sfx": 24, "warning": 6, "movement": 6, "projectile": 4, "weather": 1,
                               "text": 1, "music": 1, "music_crossfade": 2},
                   "ids": catalog}, f, indent=0, separators=(",", ":"))
    print("audio: %d/%d files passed, %d ids" % (ok, total, len(catalog)))
    return summary


def main():
    proj = gmyy.Project()
    only = set(sys.argv[1:])
    if not only or "dave" in only:
        import_dave(proj)
    if not only or "ui" in only:
        import_ui(proj)
    if not only or "fonts" in only:
        import_fonts(proj)
    if not only or "audio" in only:
        import_audio(proj)
    proj.save()
    os.makedirs(rel("docs", "integration"), exist_ok=True)
    with open(rel("docs", "integration", "import_validation.json"), "w", encoding="utf-8") as f:
        json.dump(REPORT, f, indent=1)
    bad = [r for r in REPORT["dave"] + REPORT["ui"] if r.get("errors")]
    print("dave/ui rejects:", len(bad))


if __name__ == "__main__":
    main()
