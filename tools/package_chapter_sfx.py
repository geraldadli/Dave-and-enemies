"""Validate SFX deliveries, create listening reels, and package the handoff.

Run after render_chapter_sfx.py. Run build_audio_handoff.py before --zip-only.
Preview reels are review composites, never runtime assets or dialogue sentences.
"""
import argparse
import hashlib
import json
import wave
import zipfile
from pathlib import Path

import numpy as np
from scipy import signal

from render_chapter_sfx import ROOT, SR, read_pcm, seed_for, write_pcm


def load_deliveries():
    spec = json.loads((ROOT / "docs/audio/AUDIO_MANIFEST.json").read_text(encoding="utf-8"))
    assets = [a for a in spec["assets"] if a["id"].startswith("snd_")]
    results = []
    for a in assets:
        folder = ROOT / "audio" / ("voice" if a["group"] == "Text" else "sfx")
        path = folder / f"{a['id']}.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        assert report["status"] == "GENERATED_TECHNICALLY_VALIDATED"
        assert {f["file"] for f in report["files"]} == set(a["planned_filenames"])
        assert (report["channels"], report["bits_per_sample"], report["sample_rate_hz"]) == (1, 16, SR)
        for f in report["files"]:
            wav = folder / f["file"]
            assert hashlib.sha256(wav.read_bytes()).hexdigest() == f["sha256"]
            y = read_pcm(wav)
            assert len(y) == round(a["duration_seconds_per_file"] * SR)
        results.append((a, report, path))
    assert len(results) == 92
    assert sum(len(r["files"]) for _, r, _ in results) == 207
    return results


def reels(deliveries):
    out = ROOT / "audio/previews"
    out.mkdir(parents=True, exist_ok=True)
    mapping = {a["id"]: r for a, r, _ in deliveries}
    voice_entries = []
    at = .25
    for speaker in ["dave", "pharaoh", "narrator"]:
        for n in range(1, 5):
            voice_entries.append((f"snd_voice_{speaker}_{n}", at, None, 1))
            at += .26
        at += .2
        for n, pitch in zip([1, 2, 3, 4, 2, 1, 4, 3], [1, .94, 1.06, 1, .94, 1.06, 1, 1]):
            voice_entries.append((f"snd_voice_{speaker}_{n}", at, None, pitch))
            at += .16
        at += .65
    make_reel(out / "dialogue_blips_preview.wav", voice_entries, mapping)
    ids = ["snd_step_sand", "snd_sword_swing", "snd_sword_hit", "snd_hurt", "snd_heal",
           "snd_chest_open", "snd_pickup", "snd_save", "snd_bow_release", "snd_arrow_hit",
           "snd_cast_charge", "snd_magic_launch", "snd_magic_hit", "snd_undead_rise",
           "snd_skeleton_warrior_death", "snd_bat_screech", "snd_snake_hiss", "snd_worm_emerge",
           "snd_thunder_warn", "snd_thunder_strike", "snd_laser_charge", "snd_laser_fire",
           "snd_boss_death", "snd_disintegrate", "snd_gate_slam", "snd_wind_loop"]
    entries, at = [], .25
    for name in ids:
        duration = 3 if name == "snd_wind_loop" else 2 if name == "snd_laser_charge" else 1.6 if name == "snd_laser_fire" else None
        length = duration or mapping[name]["files"][0]["duration_seconds"]
        entries.append((name, at, duration, 1))
        at += length + .32
    make_reel(out / "sfx_preview.wav", entries, mapping)


def make_reel(path, entries, mapping):
    clips, index = [], []
    for name, at, duration, pitch in entries:
        file = mapping[name]["files"][0]
        y = read_pcm(ROOT / file["path"])
        if pitch == .94:
            y = signal.resample_poly(y, 50, 47)
        elif pitch == 1.06:
            y = signal.resample_poly(y, 50, 53)
        if duration:
            y = np.tile(y, int(np.ceil(duration * SR / len(y))))[:round(duration*SR)]
            edge = round(.012*SR)
            y[:edge] *= np.linspace(0,1,edge)
            y[-edge:] *= np.linspace(1,0,edge)
        start = round(at*SR)
        clips.append((start, y))
        index.append({"asset_id": name, "source_file": file["path"], "start_seconds": start/SR,
                      "duration_seconds": len(y)/SR, "pitch_factor": pitch})
    n = max(start+len(y) for start,y in clips)+round(.3*SR)
    mix = np.zeros(n)
    for start,y in clips:
        mix[start:start+len(y)] += y
    assert np.max(np.abs(mix)) < .89
    write_pcm(path, mix, seed_for(path.name))
    path.with_suffix(".json").write_text(json.dumps({"type":"LISTENING_REEL_ONLY", "runtime_asset":False,
         "source_levels": "Original source levels, no cue-sheet playback gains applied.",
         "notes": "Sequential examples; gaps intentionally inserted. Repeated loop excerpts have preview-only edge fades. Voice block order: Dave, Pharaoh, narrator. Each block has four isolated takes followed by cadence examples with +/-6% pitch.",
         "entries":index}, indent=2)+"\n", encoding="utf-8")


def delivery_notes(deliveries):
    manifest = json.loads((ROOT / "docs/audio/AUDIO_MANIFEST.json").read_text(encoding="utf-8"))
    remaining_music = [a["id"] for a in manifest["assets"] if a["id"].startswith("mus_") and not a["generated"]]
    music_status = ("Music cues still pending: " + ", ".join(f"`{name}`" for name in remaining_music) + ".") if remaining_music else "All six music cues are also delivered; see the [music delivery notes](music/AUDIO_DELIVERY.md)."
    files = [f for _,r,_ in deliveries for f in r["files"]]
    voices = [(a,r) for a,r,_ in deliveries if a["group"] == "Text"]
    assert len(voices) == 12
    hashes = [f["sha256"] for f in files]
    assert len(set(hashes)) == 207
    loops = [{"id":a["id"],"loop_start":r["loop_start"],"loop_end":r["loop_end"],
              "frames":r["loop_end_frame_exclusive"]} for a,r,_ in deliveries if a["loop"]["enabled"]]
    summary = {
        "status":"GENERATED_TECHNICALLY_VALIDATED", "stable_ids":92, "production_wav_count":207,
        "sfx_wav_count":195, "dialogue_blip_wav_count":12, "support_preview_wavs":2,
        "format":"WAV, PCM signed 16-bit little-endian, 44100 Hz, mono",
        "maximum_sample_peak_dbfs":max(f["measurements"]["sample_peak_dbfs"] for f in files),
        "maximum_oversampled_peak_dbfs_4x":max(f["measurements"]["oversampled_peak_dbfs_4x"] for f in files),
        "maximum_onset_ms":max(f["measurements"]["onset_ms_at_minus60_relative"] for f in files),
        "maximum_trailing_ms":max(f["measurements"]["trailing_ms_below_minus60_relative"] for f in files),
        "unique_wav_hashes":len(set(hashes)), "loop_count":len(loops), "loops":loops,
        "duration_tolerance":"Nearest sample to nominal cue-sheet duration, at most 0.5 sample difference",
        "native_blip_duration_range_seconds":[min(r["actual_duration_seconds"] for a,r in voices), max(r["actual_duration_seconds"] for a,r in voices)],
        "voices":"Original formant synthesis for Dave and Pharaoh; soft noise/modal paper ticks for narrator. No words or full sentences.",
        "recipe_source":"tools/render_chapter_sfx.py", "packaging_source":"tools/package_chapter_sfx.py",
        "remaining_music_pending":remaining_music,
        "human_listening_review":"Pending", "game_integration":"Not performed; Claude owns all playback, mixing and triggers.",
        "files":files,
    }
    (ROOT / "audio/SFX_DELIVERY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    rows = "\n".join(f"| `{r['id']}` | 0 | {r['loop_end']:g} | {r['frames']:,} |" for r in loops)
    text = f"""# Dave's & Enemies sound effects and dialogue blips

**207 actual production WAVs across 92 stable IDs are generated and technically validated:** 195 SFX takes and 12 dialogue/narrator blips. All files follow the cue sheet's filenames, durations and variation counts. Human listening review remains pending. This is original procedural Python audio, including synthesized material/creature approximations and human-like formant murmurs; no sounds are claimed to be live recordings.

Download the [SFX and blips ZIP](daves_enemies_sfx_and_blips.zip). Individual production files are in `audio/sfx/` and `audio/voice/`; the [updated cue sheet](../docs/audio/AUDIO_CUE_SHEET.csv) lists every actual path. Each stable ID has a JSON sidecar containing its files, hashes, precise frame counts, validation results, original prompt and provenance. See [SFX_DELIVERY.json](SFX_DELIVERY.json) for the aggregate file ledger.

## Listening previews

- [SFX listening reel](previews/sfx_preview.wav): sequential examples from combat, interactions, enemies, boss attacks, gates and weather.
- [Dialogue blips listening reel](previews/dialogue_blips_preview.wav): Dave, Pharaoh, narrator, in that order. Each group presents four isolated takes, then a short text-like cadence with normal and +/-6% pitch examples. There are no words.

The two reels are review composites with deliberate gaps, not runtime assets or additional production IDs. Their JSON companions identify every example and time offset. Preview-only loop fades and pitch changes do not alter the production files. Reels use source levels without the cue sheet's proposed playback gains.

## Format and validation

All 207 production WAVs are mono, signed PCM 16-bit little-endian, 44,100 Hz. Native blips range from 50 to 110 ms, including edge envelopes, with four distinct takes for each of Dave, Pharaoh and narrator. Dave uses warm, firm closed-mouth formant pulses; Pharaoh uses low, dry resonance with audible upper harmonics; narration uses soft paper/felt-like ticks. These timbres are synthesized, without speech synthesis, cloned voices, recognizable game recordings or spoken sentences.

The final PCM files passed header, exact frame count, nonzero signal, sample peak, 4x oversampled peak, DC offset, leading/trailing silence and unique-file checks. Variants within each SFX ID are RMS-matched; their spectral character and gestures vary. All 207 hashes are distinct. The highest measured sample peak is **{summary['maximum_sample_peak_dbfs']:.2f} dBFS**; the highest 4x oversampled peak is **{summary['maximum_oversampled_peak_dbfs_4x']:.2f} dBFS**, below the contract's -1 dBFS ceiling. Short SFX are not assigned an integrated LUFS target.

Durations are rounded to the nearest 44,100 Hz sample, at most half a sample from the nominal cue-sheet duration. One-shots use 2.5 ms outer edge envelopes and contain their designed decay without long silent padding. The largest measured leading interval below -60 dB relative to a file's peak is {summary['maximum_onset_ms']:.2f} ms; the largest trailing interval is {summary['maximum_trailing_ms']:.2f} ms. These numerical checks do not replace listening review or in-game testing.

## Whole-file SFX loops

| Stable ID | Start in seconds | End in seconds | Sample frames |
|---|---:|---:|---:|
{rows}

Loop starts are inclusive; ends are exclusive. Periodic oscillators/modulation and circular filtered noise create continuous loop beds without baked fades. Boundary sample steps pass the same numerical continuity check used for the two full music themes. Claude still applies the cue sheet's entry/exit fades and owns one runtime handle per emitter, as appropriate. Sandstorm wind is mono in accordance with PROJECT_CONTRACT, despite the older stereo request.

## Integration details for Claude

The cue sheet's trigger, stop, fade, relative gain and concurrency specifications still apply. Proposed runtime gains are not baked into these source files. Keep music, SFX and dialogue controls separate, rate-limit warning clusters, cancel text blips on instant reveal/skip and stop owned projectile/charge loops on destruction or reset. No playback logic has been implemented in this delivery.

`snd_thunder_warn` has taps at 0 and 0.120 seconds. `snd_gate_slam` includes a short slide followed by the main slam at about 0.495 seconds; align that contact to the visible closed-gate frame rather than starting the whole file at contact. `snd_chest_open` begins with a latch and places its lid-stop gesture at about 0.468 seconds. All attack/collision timing remains Claude's integration work. Do not change gameplay timing to match a clip.

No GameMaker project, resource, GML, room or runtime-data file was changed. The two previously delivered full music themes are preserved. {music_status} This pack contains the sound effects and blips; it excludes the separate music WAVs.

## Reproduction

Use [render_chapter_sfx.py](../tools/render_chapter_sfx.py) with Python, NumPy and SciPy:

```powershell
python tools/render_chapter_sfx.py
python tools/package_chapter_sfx.py
python tools/build_audio_handoff.py
python tools/package_chapter_sfx.py --zip-only
```

Use `python tools/render_chapter_sfx.py --id snd_sword_hit` to regenerate one family. Rendering replaces the generated files for the selected IDs. Seeds come from stable filenames, and the source and seed are recorded in each sidecar. The generation environment is Python 3.12.6, NumPy 1.26.4 and SciPy 1.14.1. A different numerical toolchain may cause small differences.

The archive contains the 207 production WAVs, their sidecars, two review reels and their indexes, source scripts, updated documentation and this delivery ledger. It excludes the separately delivered music WAVs.
"""
    (ROOT / "audio/SFX_DELIVERY.md").write_text(text,encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!='files'},indent=2))


def archive(deliveries):
    destination = ROOT / "audio/daves_enemies_sfx_and_blips.zip"
    paths = []
    for a,r,sidecar in deliveries:
        paths += [sidecar] + [ROOT/f["path"] for f in r["files"]]
    paths += list((ROOT/"audio/previews").glob("*.wav")) + list((ROOT/"audio/previews").glob("*.json"))
    paths += [ROOT/name for name in ["audio/SFX_DELIVERY.md","audio/SFX_DELIVERY.json",
              "tools/render_chapter_sfx.py","tools/package_chapter_sfx.py","tools/build_audio_handoff.py",
              "docs/audio/AUDIO_CUE_SHEET.csv","docs/audio/AUDIO_MANIFEST.json","docs/audio/AUDIO_PROMPTS.md",
              "docs/audio/AUDIO_PRODUCTION_PLAN.md","docs/PROJECT_CONTRACT.md"]]
    with zipfile.ZipFile(destination,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in sorted(set(paths)):
            z.write(path,path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(destination) as z:
        assert z.testzip() is None
        production_wavs=[n for n in z.namelist() if n.startswith(('audio/sfx/','audio/voice/')) and n.endswith('.wav')]
        assert len(production_wavs)==207
        assert len([n for n in z.namelist() if n.endswith('.wav')])==209
    print(json.dumps({"archive":str(destination),"bytes":destination.stat().st_size,"production_wavs":207,"review_reels":2}))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--zip-only",action="store_true")
    args=parser.parse_args()
    deliveries=load_deliveries()
    if args.zip_only:
        archive(deliveries)
    else:
        reels(deliveries)
        delivery_notes(deliveries)
