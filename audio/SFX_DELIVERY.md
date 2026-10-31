# Dave's & Enemies sound effects and dialogue blips

**207 actual production WAVs across 92 stable IDs are generated and technically validated:** 195 SFX takes and 12 dialogue/narrator blips. All files follow the cue sheet's filenames, durations and variation counts. Human listening review remains pending. This is original procedural Python audio, including synthesized material/creature approximations and human-like formant murmurs; no sounds are claimed to be live recordings.

Download the [SFX and blips ZIP](daves_enemies_sfx_and_blips.zip). Individual production files are in `audio/sfx/` and `audio/voice/`; the [updated cue sheet](../docs/audio/AUDIO_CUE_SHEET.csv) lists every actual path. Each stable ID has a JSON sidecar containing its files, hashes, precise frame counts, validation results, original prompt and provenance. See [SFX_DELIVERY.json](SFX_DELIVERY.json) for the aggregate file ledger.

## Listening previews

- [SFX listening reel](previews/sfx_preview.wav): sequential examples from combat, interactions, enemies, boss attacks, gates and weather.
- [Dialogue blips listening reel](previews/dialogue_blips_preview.wav): Dave, Pharaoh, narrator, in that order. Each group presents four isolated takes, then a short text-like cadence with normal and +/-6% pitch examples. There are no words.

The two reels are review composites with deliberate gaps, not runtime assets or additional production IDs. Their JSON companions identify every example and time offset. Preview-only loop fades and pitch changes do not alter the production files. Reels use source levels without the cue sheet's proposed playback gains.

## Format and validation

All 207 production WAVs are mono, signed PCM 16-bit little-endian, 44,100 Hz. Native blips range from 50 to 110 ms, including edge envelopes, with four distinct takes for each of Dave, Pharaoh and narrator. Dave uses warm, firm closed-mouth formant pulses; Pharaoh uses low, dry resonance with audible upper harmonics; narration uses soft paper/felt-like ticks. These timbres are synthesized, without speech synthesis, cloned voices, recognizable game recordings or spoken sentences.

The final PCM files passed header, exact frame count, nonzero signal, sample peak, 4x oversampled peak, DC offset, leading/trailing silence and unique-file checks. Variants within each SFX ID are RMS-matched; their spectral character and gestures vary. All 207 hashes are distinct. The highest measured sample peak is **-3.00 dBFS**; the highest 4x oversampled peak is **-2.95 dBFS**, below the contract's -1 dBFS ceiling. Short SFX are not assigned an integrated LUFS target.

Durations are rounded to the nearest 44,100 Hz sample, at most half a sample from the nominal cue-sheet duration. One-shots use 2.5 ms outer edge envelopes and contain their designed decay without long silent padding. The largest measured leading interval below -60 dB relative to a file's peak is 0.66 ms; the largest trailing interval is 3.24 ms. These numerical checks do not replace listening review or in-game testing.

## Whole-file SFX loops

| Stable ID | Start in seconds | End in seconds | Sample frames |
|---|---:|---:|---:|
| `snd_wind_loop` | 0 | 12 | 529,200 |
| `snd_magic_travel` | 0 | 1.5 | 66,150 |
| `snd_worm_rumble` | 0 | 3 | 132,300 |
| `snd_laser_charge` | 0 | 1 | 44,100 |
| `snd_laser_fire` | 0 | 0.8 | 35,280 |

Loop starts are inclusive; ends are exclusive. Periodic oscillators/modulation and circular filtered noise create continuous loop beds without baked fades. Boundary sample steps pass the same numerical continuity check used for the two full music themes. Claude still applies the cue sheet's entry/exit fades and owns one runtime handle per emitter, as appropriate. Sandstorm wind is mono in accordance with PROJECT_CONTRACT, despite the older stereo request.

## Integration details for Claude

The cue sheet's trigger, stop, fade, relative gain and concurrency specifications still apply. Proposed runtime gains are not baked into these source files. Keep music, SFX and dialogue controls separate, rate-limit warning clusters, cancel text blips on instant reveal/skip and stop owned projectile/charge loops on destruction or reset. No playback logic has been implemented in this delivery.

`snd_thunder_warn` has taps at 0 and 0.120 seconds. `snd_gate_slam` includes a short slide followed by the main slam at about 0.495 seconds; align that contact to the visible closed-gate frame rather than starting the whole file at contact. `snd_chest_open` begins with a latch and places its lid-stop gesture at about 0.468 seconds. All attack/collision timing remains Claude's integration work. Do not change gameplay timing to match a clip.

No GameMaker project, resource, GML, room or runtime-data file was changed. The two previously delivered full music themes are preserved. All six music cues are also delivered; see the [music delivery notes](music/AUDIO_DELIVERY.md). This pack contains the sound effects and blips; it excludes the separate music WAVs.

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
