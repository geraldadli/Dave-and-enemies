"""
write_audio_report.py - writes docs/audio/AUDIO_INTEGRATION_REPORT.md from the import audit
(docs/audio/audio_import_audit.json), the runtime catalog and the route table below.
Run from the project root after import_deliveries.py.
"""
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")

# stable ID -> where it is triggered in the runtime (script function / state)
ROUTES = {
    "mus_desert": "scene_manager_create (idempotent across scene passes); boss_defeat_step at 6.5 s; boss_defeat_complete on skip",
    "mus_pharaoh": "boss_intro_complete only (after the last boss line or skip); never restarted on phase changes",
    "mus_intro": "obj_intro storyboard cue at t=0; skip fades it over 300 ms (intro_finish)",
    "mus_boss_defeat": "boss_defeat_step at t=250 ms after confirmed zero HP",
    "mus_ending": "boss_begin_ending at t=0 (doorway crossing)",
    "mus_gameover": "player_step death branch, 250 ms after snd_player_defeated; fades on retry/load/menu",
    "snd_wind_loop": "owner 'weather': scene_manager_step with hysteresis and suppress rects; intro storyboard cues; resumed at defeat 4.5 s",
    "snd_intro_grit": "intro storyboard shot 3 (+1 s)",
    "snd_intro_banner": "intro storyboard shot 1 (+1.5 s)",
    "snd_sword_swing": "player_step on entering attack frame 2",
    "snd_sword_hit": "player_sword_hits after enemy_take_hit accepts damage (once per swing-target pair)",
    "snd_sword_hit_bone": "player_sword_hits accent for material 'bone' (undead, skeletons)",
    "snd_sword_hit_armor": "player_sword_hits accent for material 'armor' (bandit, Pharaoh)",
    "snd_hurt": "damage_player on accepted nonfatal HP loss",
    "snd_player_defeated": "damage_player when HP reaches zero (replaces snd_hurt)",
    "snd_potion_drink": "inv_use after an accepted heal",
    "snd_heal": "inv_use; spring_interact (only when HP was missing)",
    "snd_step_sand": "player_walk_anim on moving contacts f2/f7 (sand); intro walk",
    "snd_step_stone": "player_walk_anim contacts on paving/stairs",
    "snd_step_wood": "player_walk_anim contacts on bridges",
    "snd_undead_attack": "enemy_ai_melee windup entry (undead)",
    "snd_undead_move": "enemy_footstep while chasing/returning (undead)",
    "snd_undead_death": "enemy_die (undead); silent for whiteout cleanup",
    "snd_undead_rise": "obj_hazard crack completes and an undead summon rises",
    "snd_skeleton_warrior_attack": "enemy_ai_melee windup entry",
    "snd_skeleton_warrior_move": "enemy_footstep",
    "snd_skeleton_warrior_death": "enemy_die",
    "snd_skeleton_archer_move": "enemy_footstep",
    "snd_skeleton_archer_death": "enemy_die",
    "snd_bow_draw": "enemy_ai_ranged windup entry (archer)",
    "snd_bow_release": "enemy_ai_ranged release, only when the arrow actually spawns",
    "snd_arrow_travel": "projectile_setup (arrow), dropped when out of audible range",
    "snd_arrow_hit": "projectile_step body impact",
    "snd_arrow_hit_world": "projectile_step scenery impact (alternative to body hit)",
    "snd_bandit_attack": "enemy_ai_melee windup entry",
    "snd_bandit_move": "enemy_footstep",
    "snd_bandit_death": "enemy_die",
    "snd_bandit_caster_move": "enemy_footstep",
    "snd_bandit_caster_death": "enemy_die",
    "snd_cast_charge": "enemy_ai_ranged windup entry (caster); interrupted casts never release",
    "snd_magic_launch": "enemy_ai_ranged release, only when the orb spawns",
    "snd_magic_travel": "owned loop per orb (w:proj:<id>), stopped on hit/expiry/destroy",
    "snd_magic_hit": "projectile_step body or world impact (orb)",
    "snd_bat_fly": "enemy_ai_bat every 30 ticks when Dave is within 600 px",
    "snd_bat_screech": "enemy_ai_bat dive windup",
    "snd_bat_dive": "enemy_ai_bat dive start",
    "snd_bat_defeat": "enemy_die (bat)",
    "snd_python_move": "enemy_footstep (python, 34-tick body cycle)",
    "snd_snake_hiss": "enemy_ai_python coil (windup)",
    "snd_snake_lunge": "enemy_ai_python lunge start",
    "snd_python_death": "enemy_die",
    "snd_worm_rumble": "owned loop per worm while hidden/warning (w:<id>)",
    "snd_worm_emerge": "enemy_ai_worm surface break",
    "snd_worm_bite": "enemy_ai_worm attack active frame",
    "snd_worm_burrow": "enemy_ai_worm burrow start",
    "snd_sandworm_death": "enemy_die (rumble stopped first)",
    "snd_enemy_melee_hit": "damage_player for accepted melee damage",
    "snd_boss_summon": "pharaoh_do_summon, once per action",
    "snd_boss_bat_spawn": "pharaoh_do_summon per bat (cooldown/limit bounded)",
    "snd_summon_crack": "obj_hazard crack, first marker of a cluster only",
    "snd_laser_charge": "owned loop 'boss:laser' for the whole charge state",
    "snd_laser_fire": "owned loop 'boss:laser' for the beam state",
    "snd_laser_hit": "damage_player kind 'laser' (accepted damage only)",
    "snd_thunder_warn": "pharaoh_thunder_wave once per committed wave",
    "snd_thunder_strike": "obj_hazard thunder, one tile per wave carries the cue (consolidated)",
    "snd_boss_float": "NOT WIRED: optional glide cue; the Pharaoh has no glide state (teleports only)",
    "snd_boss_teleport_out": "pharaoh_choose teleport start",
    "snd_boss_teleport_in": "pharaoh_step teleport arrival",
    "snd_boss_hurt": "boss_on_hit for nonfatal accepted damage",
    "snd_boss_death": "boss_begin_defeat (scene-owned, not tied to the boss instance)",
    "snd_disintegrate": "boss_begin_defeat (scene-owned)",
    "snd_chest_open": "chest_interact on the closed-to-open change only",
    "snd_chest_locked": "player_interact at a closed barrier (sealed route); no locked chests exist in the design",
    "snd_pickup": "loot_transaction once per accepted batch",
    "snd_coin": "loot_transaction when the batch includes gold (replaces pickup)",
    "snd_levelup": "grant_xp once per award that raises the level",
    "snd_checkpoint": "checkpoint_interact / pause Save Game when the save UI opens",
    "snd_save": "saveload_do_save after save_write succeeds",
    "snd_gate_open": "boss_defeat_step at 4.5 s (barriers reopened under the whiteout)",
    "snd_gate_slam": "gate_close_animated; the 30-tick close puts the slam at ~0.495 s",
    "snd_ui_error": "failed save/load, rejected item action, inventory full with nothing taken",
    "snd_inventory_open": "inventory_open",
    "snd_inventory_close": "ui_close_inventory (replaces cancel)",
    "snd_ui_move": "focus/selection changes in menus, inventory, hotbar",
    "snd_ui_confirm": "accepted menu commands (replaced by specialist cues where specified)",
    "snd_ui_cancel": "back/cancel commands",
}


def main():
    audit = json.load(open(os.path.join(ROOT, "docs", "audio", "audio_import_audit.json"), encoding="utf-8"))
    cat = json.load(open(os.path.join(ROOT, "datafiles", "data", "audio_catalog.json"), encoding="utf-8"))
    summ = audit["summary"]
    by_id = {}
    for r in audit["files"]:
        by_id.setdefault(r["id"], []).append(r)
    lines = []
    w = lines.append
    w("# Audio integration report — Dave's & Enemies, Chapter I")
    w("")
    w("Engineering report, 31 October 2026. Generated by `tools/write_audio_report.py` from "
      "`docs/audio/audio_import_audit.json` and `datafiles/data/audio_catalog.json`.")
    w("")
    w("## Status at a glance")
    w("")
    w("| Check | Result |")
    w("|---|---|")
    w("| Production files accounted for | **%d of 213** passed (music %d, SFX %d, voice %d) |"
      % (summ["passed"], summ["music"], summ["sfx"], summ["voice"]))
    w("| Stable IDs | **%d of 98** in the runtime catalog |" % len(cat["ids"]))
    w("| SHA-256 against delivery sidecars | all match |")
    w("| WAV headers | all PCM 16-bit LE, 44.1 kHz; music stereo, SFX and blips mono |")
    w("| Frame counts against sidecars | all within one sample |")
    w("| Seven loop lengths equal file length (`loop_end`) | all match |")
    w("| Excluded | `audio/previews/*.wav` (2 review reels), the two ZIP bundles, `*.score.json`, template `sounds/*` |")
    w("| Resource load/link (Igor) | passed: \"GMSC serialisation: SUCCESSFUL LOAD AND LINK\" |")
    w("| Compilation | **blocked**: no signed-in licence (Igor \"Unable to obtain permission to execute\") |")
    w("| Listening review / in-game playback | **not performed** (needs the IDE) |")
    w("")
    w("Originals stay in `audio/music`, `audio/sfx`, `audio/voice`. Each take was copied unchanged into "
      "`sounds/<resource>/<resource>.wav`: no normalisation, resampling, pitch, length or channel change.")
    w("")
    w("## Resource naming and the one collision")
    w("")
    w("Every delivered take becomes one sound resource named after its file (`snd_sword_hit_1.wav` → `snd_sword_hit_1`). "
      "The stable event ID (`snd_sword_hit`) is the catalog key and the only name gameplay code uses. "
      "Voice takes (`snd_voice_dave_1` …) are individual IDs. The template already owns a resource called "
      "`snd_player_defeated`; it keeps its name and the delivered take is imported as **`snd_player_defeated_1`** "
      "(explicit mapping in the catalog). No other name collides with the 26 template sounds.")
    w("")
    w("## Loading settings")
    w("")
    w("| Group | GameMaker compression | Why |")
    w("|---|---|---|")
    w("| Looping music (`mus_desert`, `mus_pharaoh`) and all looping SFX | 0, uncompressed | sample-accurate whole-file seams |")
    w("| One-shot music (`mus_intro`, `mus_boss_defeat`, `mus_ending`, `mus_gameover`) | 1, compressed (not streamed) | smaller package; never loops |")
    w("| SFX and dialogue blips | 0, uncompressed | instant start |")
    w("")
    w("All resources use `audiogroup_default`, 16-bit, the delivered sample rate and channel layout. "
      "The seven loops repeat their whole file (`audio_play_sound(..., loop=true)`); the sidecar points are "
      "0 to file end, so no `audio_sound_loop_start/end` override is needed. Fades happen only when a loop "
      "starts or stops (owned-loop envelopes), never on each repeat.")
    w("")
    w("## Runtime service (scripts/scr_audio)")
    w("")
    w("- Catalog: `datafiles/data/audio_catalog.json`, derived from `AUDIO_CUE_SHEET.csv` (gain dB, bus, per-emitter "
      "and global limits, minimum retrigger, priority, loop, fade in/out) and `AUDIO_MANIFEST.json` (files). "
      "Prompts and review metadata are not shipped.")
    w("- Gain: `10^(dB/20)` × user bus volume (music / SFX / dialogue blips) × duck × distance attenuation, applied once at "
      "playback; sources are untouched. Cue-sheet values are used as delivered; **no gain changes were made** "
      "because no listening pass was possible.")
    w("- Budgets: SFX 24 (weather included); within it warnings 6, movement 6, projectile travel 4, weather 1; "
      "dialogue 1 across all speakers; music 1, or 2 during a crossfade. Requests over a limit or inside a cooldown are "
      "**dropped, never queued**. When a budget is full, the lowest-priority un-owned voice below the new priority is "
      "stopped; otherwise the request is dropped.")
    w("- Variants: random pick that never repeats the previous take of the same ID.")
    w("- Loops: started by owner key (`weather`, `boss:laser`, `w:<instance>`, `w:proj:<instance>`); starting an owned "
      "loop again returns the existing handle. Owners stop their loops on hit, expiry, destroy, Clean Up, death, load, "
      "scene unload, skip and menu return.")
    w("- Ducking: text lowers music 4 dB and wind 8 dB (≈100 ms attack, 350 ms release); attack warnings lower music "
      "3 dB and weather 6 dB (≈30/250 ms). The stronger reduction wins; ducks are not summed.")
    w("- Positional: world SFX are attenuated by distance from the camera centre (full within 360 px, silent beyond "
      "≈1260 px). **No stereo panning** is applied (deliberate: listener orientation could not be verified without a "
      "runtime). Music, UI, text and Dave's own cues are unspatialised.")
    w("- Pause: world-owned voices pause while inventory, pause, dialogue or an in-scene cinematic stops the world, and "
      "resume afterwards; music, UI, blips and the wind bed keep playing. Nothing builds a backlog.")
    w("- Blips: one global voice, a blip every second newly revealed letter or digit, takes never repeat back-to-back, "
      "pitch 0.94–1.06, at least 75 ms between onsets, occupied voice = dropped. Comma/semicolon pause 120 ms, "
      "sentence/ellipsis 240 ms. Instant reveal, page/line change, skip and scene exit cancel the active blip with a "
      "5 ms fade. Objective toasts, UI text and the ending title are silent.")
    w("")
    w("## Music transitions")
    w("")
    w("| Moment | Behaviour |")
    w("|---|---|")
    w("| Intro | `mus_intro` at t=0 (54 s, motif beats at 27/35/43 s live in the file). An advance to the next shot seeks the music to the new shot time; skip fades it over 300 ms. |")
    w("| Exploration | `mus_desert` starts on the first scene and keeps playing across both scene passes (start is idempotent). |")
    w("| Pre-boss exchange | `mus_desert` fades over **1200 ms** (cue sheet), not the storyboard's 0.8 s. |")
    w("| Combat | `mus_pharaoh` once at combat handoff, after the second line is acknowledged or skipped. |")
    w("| Pharaoh defeat | `mus_pharaoh` fades over **250 ms** (cue sheet; the storyboard suggests 1.5 s); `mus_boss_defeat` at +250 ms; wind resumes at 4.5 s; `mus_desert` fades in over 1 s at 6.5 s. Control returns at 7.5 s, never at 6.5 s. |")
    w("| Ending | `mus_ending` at t=0, desert fades 1 s, wind fades 2 s; title at 6 s; menu enabled at 10 s. |")
    w("| Game Over | current music fades 250 ms at death; `mus_gameover` 250 ms after the death cue; fades on retry/load/menu. |")
    w("| Completed-boss load | no defeat, gate or reward cue is replayed. |")
    w("")
    w("## Event routes")
    w("")
    w("| Stable ID | Takes | Bus / group | dB | Limits (emitter/global) | Retrigger ms | Priority | Route |")
    w("|---|---:|---|---:|---|---:|---:|---|")
    for aid, e in cat["ids"].items():
        lim = "%d/%d" % (e["pe"], e["gl"])
        w("| `%s` | %d | %s / %s | %g | %s | %d | %d | %s |" % (aid, len(e["res"]), e["bus"], e["grp"], e["db"], lim,
                                                              e["rt"], e["pr"], ROUTES.get(aid, "")))
    w("")
    w("## Source-to-resource mapping (all 213 files)")
    w("")
    w("| Stable ID | Resource | Source file | Duration s |")
    w("|---|---|---|---:|")
    for aid in cat["ids"]:
        for r in by_id.get(aid, []):
            w("| `%s` | `%s` | `%s` | %.3f |" % (aid, r["resource"], r["file"], r["duration"]))
    w("")
    w("## Discrepancies and the smallest integration choice")
    w("")
    w("- Storyboard fade lengths differ from the cue sheet for the pre-boss desert fade (0.8 s vs 1200 ms) and the "
      "Pharaoh death fade (1.5 s vs 250 ms). The cue sheet is used for audio parameters; scene durations follow the "
      "narrative timing.")
    w("- The audio handoff's exploration-return beat near 6.5 s is kept for `mus_desert` only; player control still "
      "returns at the 7.5 s defeat completion.")
    w("- `snd_boss_float` is not wired: the Pharaoh teleports and has no glide state, and no attack was invented to use it.")
    w("- `snd_chest_locked` has no locked chest in the design; it plays for an explicit interaction at a closed barrier.")
    w("- Dialogue reveal speed follows the narrative manifest (24 characters/s, 240 ms sentence pause) rather than "
      "UI_SPEC's 30 characters/s and 220 ms.")
    w("- Positional audio is attenuation only (no panning), noted above.")
    w("")
    w("## Checks actually executed")
    w("")
    w("1. `python tools/import_deliveries.py audio` — existence, SHA-256, WAV header, channels, frame count and loop "
      "length for every allowlisted file: **213/213 passed**, 98 IDs.")
    w("2. Igor load/link of the project with all 239 sound resources: **passed**.")
    w("3. `python tools/gml_lint.py` — every audio call resolves to a script/built-in function with a valid "
      "argument count: **passed** (two findings are in an unregistered template file).")
    w("")
    w("## Not yet verified (IDE checklist)")
    w("")
    w("- [ ] Five-repeat audition of each loop: `mus_desert`, `mus_pharaoh`, `snd_wind_loop`, `snd_magic_travel`, "
      "`snd_worm_rumble`, `snd_laser_charge`, `snd_laser_fire`; confirm the four story cues end once and never loop.")
    w("- [ ] Swing on frame 2 only; hit only on accepted damage; footsteps on f2/f7 while moving; no idle chatter.")
    w("- [ ] Interrupted archer/caster windups stay silent; orb travel loops stop on hit, expiry and scene change.")
    w("- [ ] Blips at normal and rapid reveal, punctuation pauses, ±6% pitch, instant reveal and skip with no backlog.")
    w("- [ ] Checkpoint open cue, save success vs failure, full inventory, batch loot, restored state with no duplicate cues.")
    w("- [ ] Crowded Pharaoh fight (two bats, two undead, thunder): voice counts bounded, warnings audible, no clipping.")
    w("- [ ] Intro skip, boss-intro skip, death/retry/load, defeat whiteout, completed-boss load, ending and menu exit "
      "without stale loops or doubled music.")
    w("- [ ] Music, SFX and dialogue sliders independent; pause/resume; scene unload.")
    w("- [ ] Listening pass on the cue-sheet gains; adjust catalog dB values, never the WAVs.")
    path = os.path.join(ROOT, "docs", "audio", "AUDIO_INTEGRATION_REPORT.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", path)


if __name__ == "__main__":
    main()
