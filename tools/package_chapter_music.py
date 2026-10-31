"""Verify six music deliveries, document them and package the four story cues.

Run after render_chapter_cues.py and build_audio_handoff.py. Does not render or
modify any production WAV. Requires only the Python standard library.
"""
import hashlib
import json
import wave
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"audio/music"
IDS=["mus_desert","mus_pharaoh","mus_intro","mus_boss_defeat","mus_ending","mus_gameover"]
LABELS={"mus_desert":"Desert exploration", "mus_pharaoh":"The Pharaoh",
        "mus_intro":"Opening cutscene", "mus_boss_defeat":"Boss defeat and whiteout",
        "mus_ending":"To Be Continued", "mus_gameover":"Game Over"}


def verify():
    reports=[]
    for name in IDS:
        r=json.loads((OUT/f"{name}.json").read_text(encoding="utf-8"))
        wav=OUT/r["file"]
        assert hashlib.sha256(wav.read_bytes()).hexdigest()==r["sha256"]
        with wave.open(str(wav),"rb") as f:
            assert (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes(),f.getcomptype())==(2,2,44100,r["frames"],"NONE")
        assert r["status"]=="GENERATED_TECHNICALLY_VALIDATED"
        assert -17<=r["measurements"]["integrated_lufs"]<=-15
        assert r["measurements"]["true_peak_dbtp"]<=-1
        assert r["measurements"]["sample_peak_dbfs"]<=-1
        score=json.loads((OUT/r["score_file"]).read_text(encoding="utf-8"))
        assert len(score["events"])==r["event_count"]
        assert all(e["note"] is None or e["note"]%12 in {0,1,4,5,7,8,11} for e in score["events"])
        if name in IDS[2:]:
            assert r["loop"] is False and r["loop_start"] is None and r["loop_end"] is None
            assert r["source_sha256"]==hashlib.sha256((ROOT/r["source"]).read_bytes()).hexdigest()
            assert r["measurements"]["terminal_quantized_silence_ms"]<45
        reports.append(r)
    return reports


def documentation(reports):
    rows=[]
    for r in reports:
        form=f"{r['bpm']} BPM, {r['bars']} bars, loop" if "bpm" in r else "Non-looping storyboard cue"
        rows.append(f"| [{r['file']}]({r['file']}) | {r['duration_seconds']:g} s | {form} | {r['measurements']['integrated_lufs']:.2f} LUFS | {r['measurements']['true_peak_dbtp']:.2f} dBTP |")
    table="\n".join(rows)
    summary={"status":"ALL_SIX_MUSIC_WAVS_GENERATED_TECHNICALLY_VALIDATED", "music_file_count":6,
             "new_story_cue_count":4,"format":"Stereo signed PCM16 WAV, 44100 Hz",
             "target_integrated_lufs":-16,"peak_ceiling_dbfs":-1,
             "files":[{"id":r["asset_id"],"file":r["file"],"duration_seconds":r["duration_seconds"],
                       "frames":r["frames"],"sha256":r["sha256"],"measurements":r["measurements"]} for r in reports],
             "human_listening_review":"Pending", "game_integration":"Not performed; Claude owns playback, mixing, fades and triggers."}
    (OUT/"MUSIC_DELIVERY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    document=f"""# Dave's & Enemies generated Chapter I music

**All six music WAVs are generated and technically validated**, including the four story cues: intro, boss defeat, ending and Game Over. The two existing full themes are preserved. These are original Python compositions with plucked-string, breath-flute, reed, bowed-string and hand-percussion synthesis. They contain no sampled game audio, vocals, spoken dialogue, weather or battle SFX. Human listening review remains pending.

[Download the four story cues](../daves_enemies_remaining_music.zip). Individual files and measurements are listed below. The archive includes the four WAVs, sidecars, editable scores, source scripts, contract and current cue sheet; the separate exploration and boss loops are not duplicated in it.

| File | Duration | Form | Measured integrated loudness | Measured true peak |
|---|---:|---|---:|---:|
{table}

Every file is stereo, signed PCM 16-bit little-endian WAV, 44,100 Hz, mastered around -16 LUFS integrated. Measurements come from FFmpeg's loudnorm input analysis of the final PCM WAVs. SHA-256 hashes, exact sample-frame counts and full measurements appear in each `<asset>.json` sidecar and the [aggregate music ledger](MUSIC_DELIVERY.json). Proposed playback gains from the cue sheet are not baked into the files.

## Four story cues

`mus_intro` follows the **54-second opening**. A C-G bed and isolated plucked notes support the breached wall and fallen comrades at 0-13 s. The melody thins at 13-20 s beneath the stolen-Grail text; a breath-flute lament enters at 20-27 s. Dave's vow introduces the original C-Db-E-G adventure motif at 27 s, then broadens with restrained E-natural colour at 35 s. At 43 s the eastward walk gains a soft measured pulse. Open C-G resonance fades during 52-54 s. Wind, cloth, grit and text sounds remain separate assets.

`mus_boss_defeat` is **6 seconds**, with a muted low C-G onset and a dissolving C3-Db3-G3-E3 fragment. Soft C-E-G gives way to an airy open fifth; the final two seconds fade as resonance. It leaves room for the separately delivered fatal blast and disintegration. The audio plan proposes starting this cue 0.25 s after confirmed boss death; it ends at sequence t=6.25 s, before exploration music returns at t=6.5 s. It signals survival and the route opening, with the Grail quest unresolved.

`mus_ending` is **10 seconds**. The exploration motif opens at 0-2 s; sparse C-G support leaves room for Dave's final line at 2-5 s. The F-E-Db-C answer supports To Be Continued at t=6 s. The open-fifth tail fades during 8-10 s, after which the title can hold in silence.

`mus_gameover` is **4.5 seconds**. The first 100 ms is sparse, with low C beneath Dave's separate death sound. Soft G4-E4-Db4 plucks descend, then a short breathy C-G resonance fades inside the file. The cue suggests regret and a hopeful retry without a grand impact or spoken voice.

These four cues are **one-shots**. Disable looping; their sidecars set `loop=false`, with `loop_start` and `loop_end` null. Notes, filtering, delay and room reverb are rendered linearly, so ending tails cannot wrap into their beginnings. Final fades are part of the composed one-shots; Claude still applies the cue sheet's runtime fades when a scene is skipped or interrupted. Actual storyboard timestamps, marker names and note events are recorded in the `.score.json` files.

## Existing exploration and Pharaoh loops

The desert uses 80 BPM, 4/4, 32 bars and the original four-bar exploration melody; the Pharaoh uses 128 BPM, 4/4, 48 bars and its separate two-bar hook. Both retain C, Db, E, F, G, Ab, B and the original synthesis/arrangements already delivered. Their WAV hashes have not changed.

| Stable ID | Whole-file start in seconds | End in seconds | Exact sample frames |
|---|---:|---:|---:|
| `mus_desert` | 0 | 96 | 4,233,600 |
| `mus_pharaoh` | 0 | 90 | 3,969,000 |

Loop starts are inclusive; ends are exclusive. These two loop renders use circular notes, echo, room tails and filtering, with no baked fade or silent padding. They retain their previous objective continuity checks. This circular rendering method is used only for those two themes.

## Validation and integration

All six final WAVs passed header, stereo channel count, bit depth, sample rate, exact duration, file hash, nonzero signal, integrated loudness and sample/true-peak checks. The four story cues additionally passed checks for a quiet final 100 ms, an endpoint within one PCM16 count of zero, less than 45 ms of terminal quantized silence, and no fully silent one-second block before the intended ending fade. Their note events use only the requested pitch collection. These are objective checks; no human listening review or GameMaker play-test is claimed.

All **213 production WAVs across 98 stable IDs** now exist and are marked generated in the [manifest](../../docs/audio/AUDIO_MANIFEST.json) and [cue sheet](../../docs/audio/AUDIO_CUE_SHEET.csv). Audio generation has no pending entries. Human listening review and Claude's resource import, playback, mixing, fades, loop ownership, event timing and in-game validation remain pending. No GameMaker project, sound resource, GML, room or runtime data was changed. The [SFX/blip pack](../SFX_DELIVERY.md) retains its existing production audio unchanged.

## Source and reproduction

The four story cues are composed and rendered by [render_chapter_cues.py](../../tools/render_chapter_cues.py), using the instrument palette and mastering functions from [render_chapter_music.py](../../tools/render_chapter_music.py). [package_chapter_music.py](../../tools/package_chapter_music.py) verifies and packages the files. Each cue's `.score.json` stores absolute timestamps, note gates, instrument, velocity, pan and seeded variation. Rerunning the renderer replaces only the selected story cue outputs.

```powershell
python tools/render_chapter_cues.py
python tools/build_audio_handoff.py
python tools/package_chapter_music.py
```

Use `--cue intro`, `--cue boss_defeat`, `--cue ending` or `--cue gameover` to render one cue. To reproduce the two older loops, run `python tools/render_chapter_music.py` instead. The rendering toolchain is Python 3.12.6, NumPy 1.26.4, SciPy 1.14.1, SoundFile 0.14.0, imageio-ffmpeg 0.6.0 and bundled FFmpeg 7.1. A different toolchain can introduce small numerical changes.
"""
    (OUT/"AUDIO_DELIVERY.md").write_text(document,encoding="utf-8")


def archive():
    paths=[]
    for name in IDS[2:]:
        paths += [OUT/f"{name}{suffix}" for suffix in [".wav",".json",".score.json"]]
    paths += [ROOT/name for name in ["tools/render_chapter_cues.py","tools/render_chapter_music.py",
              "tools/package_chapter_music.py","tools/build_audio_handoff.py","docs/PROJECT_CONTRACT.md",
              "docs/audio/AUDIO_MANIFEST.json","docs/audio/AUDIO_CUE_SHEET.csv","docs/audio/AUDIO_PRODUCTION_PLAN.md",
              "audio/music/AUDIO_DELIVERY.md","audio/music/MUSIC_DELIVERY.json"]]
    path=ROOT/"audio/daves_enemies_remaining_music.zip"
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(paths):
            z.write(p,p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert len([n for n in z.namelist() if n.endswith('.wav')])==4
    print(json.dumps({"archive":str(path),"bytes":path.stat().st_size,"story_cue_wavs":4},indent=2))


if __name__=="__main__":
    manifest=json.loads((ROOT/"docs/audio/AUDIO_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["status"]=="ALL_AUDIO_GENERATED" and manifest["generated_audio_file_count"]==213
    reports=verify()
    documentation(reports)
    archive()
