# Dave's & Enemies Chapter I audio production plan

The score follows Dave from the ruined Holy City through desert exploration to the Pharaoh and the dungeon threshold. Effects make attacks, successful actions and danger readable without crowding the text voices. Claude owns resource import, playback, loop handles, mixing, state transitions and event triggers. The values below are proposed audio integration targets, not changes to gameplay or engineering's contract.

**Delivery status: 213 actual Python-synthesized WAVs generated and technically validated; 0 planned WAVs remain pending.** This handoff supplies original composition instructions, recording/generation prompts and an auditable cue sheet. Delivered music: 6 actual WAVs, with file links, timing and measured results in the [music delivery notes](../../audio/music/AUDIO_DELIVERY.md). All 207 SFX/blip WAVs are also delivered: see the [SFX delivery notes](../../audio/SFX_DELIVERY.md) and [ZIP pack](../../audio/daves_enemies_sfx_and_blips.zip). Human listening review and Claude integration remain pending. Only entries marked generated have actual files; pending entries remain prompts. Template WAVs already under `sounds/` are existing placeholders, not new productions and not certified against this plan. No project resource, sound, runtime data or GML file is changed.

## Sources and contract decisions

- Original user brief in the chat “Create Dave’s action game prompt”, thread `01a19086-ad27-7ba2-b483-5f550e9c8e07`, original user message `01a19086-b65a-75a3-9fbe-ad191a1daa8e`: siege aftermath, vow, eastward desert journey, enemy roster, Pharaoh encounter, whiteout, dungeon cliffhanger and sound requirements.
- [PROJECT_CONTRACT](../PROJECT_CONTRACT.md), especially sections 5, 8, 9 and 11: naming, attack events, exports, text blips and readable warnings.
- [ASSET_REQUESTS](../ASSET_REQUESTS.md): milestone ordering, requested sound IDs and placeholder inventory.
- [NARRATIVE_SCRIPT](../NARRATIVE_SCRIPT.md) and [NARRATIVE_ASSET_REQUESTS](../NARRATIVE_ASSET_REQUESTS.md): the now-authored 54-second intro, 10-second ending, optional banner/grit IDs, defeat sequence and text timing. The audio plan adopts those timings; the contract's exports take precedence over the narrative request's stereo wind.
- This chat's instructions govern the creative direction. Claude's contract governs exports where the asset request list disagrees. `snd_wind_loop` is **mono**, because the contract says SFX mono even though request E9 says stereo. Narration has **four** takes, including `snd_voice_narrator_4`, following the contract's four variants per speaker rather than request E7's three. These are reported discrepancies; the source documents are unchanged.

The delivered audio is produced locally with original deterministic Python synthesis, without a generation service, sampled game audio or cloned voices. The [theme renderer](../../tools/render_chapter_music.py) writes the two full loops; the [story-cue renderer](../../tools/render_chapter_cues.py) writes intro, boss defeat, ending and Game Over; the [SFX/blip renderer](../../tools/render_chapter_sfx.py) writes sound effects and nonverbal formant blips. Actual file paths, hashes and measurements are recorded in the manifest and delivery sidecars.

## Deliverables and how to use them

- [AUDIO_CUE_SHEET.csv](AUDIO_CUE_SHEET.csv): compact production and integration index, one row per stable ID.
- [AUDIO_PROMPTS.md](AUDIO_PROMPTS.md): complete standalone prompt for every ID, with duration, variant count, loop, trigger, stop, fades, loudness, limits and export rules repeated for that asset.
- [AUDIO_MANIFEST.json](AUDIO_MANIFEST.json): the same detailed records in structured form. This is design handoff data under `docs/`, not a new runtime schema. Claude decides whether and how to translate it into game data.

Grouped SFX IDs with several takes use `<id>_1.wav`, `<id>_2.wav`, etc.; the group ID remains the stable event name. Single-take IDs use `<id>.wav`. Dialogue takes are individually stable IDs, e.g. `snd_voice_dave_1.wav`, each with one file. Claude maps groups to resources without renaming existing template assets. Do not use missing-file placeholders or synthetic empty WAVs to suggest completion.

## Desert musical interpretation

“Arabian-major” is treated here as a project-specific tonal colour. The provisional collection is fixed at **C, Db, E, F, G, Ab, B**, with C as tonal centre, twelve-tone equal temperament and A4=440 Hz. Its scale degrees are **1, b2, 3, 4, 5, b6, 7**, and its successive semitone steps are **1, 3, 1, 2, 1, 3, 1**. This matches the pitch-class set indexed as Double Harmonic in [Ian Ring's scale analysis](https://ianring.com/musictheory/scales/2483). The interpretation is a fantasy game composition choice; the pitch list alone is not a specification for a traditional maqam performance.

E natural against C carries the major character. Db-C and B-C provide close tension and release; the Db-E and Ab-B gaps give the phrases their distinctive shape. Use those gaps sparingly within singable lines. Do not silently replace B with Bb, use D/A natural, or substitute an unrelated minor-loop preset. Emphasize open C-G, C major, F minor and Db major colours, and G-B dyads instead of a conventional G major chord containing D natural. Pitched percussion stays on C or G; unpitched percussion need not imply another key.

`mus_desert` is **80 BPM, 4/4, 32 bars, 96 seconds**. It uses restrained plucked strings, a breathy flute-like lead, frame/hand drums and light shaker, with rests and gentle variation over four eight-bar sections. A4=440 Hz; C4 means middle C. The original four-bar melody is:

```text
q = quarter note, e = eighth note; every bar totals four beats
1 | C4 q  Db4 e  E4 e  G4 q  F4 q
2 | E4 q  Db4 e  C4 e  B3 q  C4 q
3 | G4 q  Ab4 e  B4 e  C5 q  G4 q
4 | F4 q  E4 q   Db4 q C4 q
```

Let the motif breathe rather than repeating it continuously. Bars 1-8 establish it, 9-16 shift the answer to strings, 17-24 open the flute register, and 25-32 return to the opening texture. The final two bars hand back to bar 1 without an ending. The full 96-second file loops: **4,233,600 sample frames**, `loop_start=0`, `loop_end=96` seconds. No separate music files are needed for each room.

## The Pharaoh musical identity

`mus_pharaoh` has an independent hook, a darker register, stronger frame-drum/hand-percussion attacks and a C-G bass ostinato. It is **128 BPM, 4/4, 48 bars, 90 seconds**, retaining the desert collection but using sharper 3+3+2 eighth-note accents and more active counterpoint. Intensity comes from arrangement; both music files share the same mastering target.

```text
dq = dotted quarter, q = quarter, e = eighth; every bar totals four beats
1 | C3 dq  Db3 e  G3 q   E3 q
2 | B2 e   C3 e   Ab3 q  G3 q  rest q
```

The long-short opening, Db-G tritone leap, B-C pickup and final rest make the hook identifiable. State it on dark bowed strings and a breath-reed-like colour, answer in octaves with short plucked doubles, and keep the rhythmic identity intact during variation. Develop it across three 16-bar blocks. Do not time gameplay phase changes to the music or require adaptive stems. A single stereo loop covers a long fight without restarting at health thresholds. The full file is **3,969,000 sample frames**, `loop_start=0`, `loop_end=90` seconds.

## Story and music transitions

| Event | Audio proposal for Claude |
|---|---|
| Opening ruined city | Play `mus_intro` once; quiet wind beneath it, sparse optional rubble and cape cues. Narrator uses text appearances; Dave's vow uses his murmurs. No spoken narration or dialogue recording. |
| Intro skip or natural completion | Cancel text scheduling and fade intro assets over 300 ms on skip; start desert loop with a 1200 ms fade. Never play skipped sounds in a burst. |
| Exploration and normal combat | Continue one `mus_desert` instance across connected rooms. Combat uses SFX without restarting music. |
| Arena entry | Gate closes after Dave is inside. Fade exploration over 1200 ms; fade wind to silence over 600 ms. Dialogue is deliberately sparse. |
| Dialogue complete | Start `mus_pharaoh` on beat 1 with the combat-enabled/boss-bar event. Instant text reveal does not start combat until the line is dismissed. |
| Pharaoh fatal hit at t=0 | Cancel scheduling and all laser, warning, projectile and summon loops; start `snd_boss_death`. Fade boss score over 250 ms. Preserve only the intentional sequence-level death tails. |
| Disintegration at t=0 | Play `snd_disintegrate` once alongside the blast, initially soft so the impact reads. Proposed additional `mus_boss_defeat` starts at t=0.25 s and ends at t=6.25 s, leaving room for the authored exploration return at t=6.5 s. |
| Slow whiteout and cleared arena | Continue intentional death/defeat tails across object removal. Silently delete summons and hazards; do not trigger a death sound for every cleanup deletion. Wind returns quietly at t=4.5 s; exploration fades back at t=6.5 s per the narrative. Do not replay defeat sounds on loading a completed boss state. |
| Dungeon threshold | Fade exploration over 1200 ms and start `mus_ending` at sequence t=0; leave space under Dave's 2-5 s final line. To Be Continued appears at t=6 s; let the score end at t=10 s and hold silence. This is not a Grail-recovery fanfare. |
| Dave dies | Stop attack/travel/weather ownership, fade current score over 250 ms, play his death once and `mus_gameover` on Game Over entry about 250 ms later. Suppress the nonfatal hurt cue for the fatal event. Retry clears all old handles before starting the restored area's score. |

The intro follows the narrative's 0-13/13-20/20-27/27-35/35-43/43-52/52-54 s score beats. If shot timing changes, edit/recompose the music; do not force dialogue reveal speed to fit the export. `mus_boss_defeat` is an audio-design addition, explicitly proposed for Claude to bind into the existing defeat sequence; it does not change the whiteout length or delay control return.

## Enemy coverage and intentional absences

These mappings cover every existing family without adding attacks to the game. Successful contact uses the shared `snd_enemy_melee_hit` plus Dave's accepted damage reaction. Sword damage to enemies uses `snd_sword_hit`; do not play damage sounds on overlap alone.

| Contract entity | Melee | Ranged or summoning | Movement | Death |
|---|---|---|---|---|
| `undead` | `snd_undead_attack` | None specified; emergence is `snd_undead_rise` | `snd_undead_move` | `snd_undead_death` |
| `skeleton_warrior` | `snd_skeleton_warrior_attack` | None specified | `snd_skeleton_warrior_move` | `snd_skeleton_warrior_death` |
| `skeleton_archer` | None specified | `snd_bow_draw`, `snd_bow_release`, `snd_arrow_travel`, body/world impacts | `snd_skeleton_archer_move` | `snd_skeleton_archer_death` |
| `bandit` | `snd_bandit_attack` | None specified | `snd_bandit_move` | `snd_bandit_death` |
| `bandit_caster` | None specified | `snd_cast_charge`, `snd_magic_launch`, travel loop, `snd_magic_hit` | `snd_bandit_caster_move` | `snd_bandit_caster_death` |
| `bat` | Dive telegraph `snd_bat_screech`, active `snd_bat_dive` | None specified; same kit for summoned bats | `snd_bat_fly` | `snd_bat_defeat` |
| `python` | Coil `snd_snake_hiss`, active `snd_snake_lunge` | None specified | `snd_python_move` | `snd_python_death` |
| `sandworm` | `snd_worm_bite` | None specified | Rumble warning loop, emergence, burrow | `snd_sandworm_death` |
| `pharaoh` | None specified; do not add contact attack audio | Summon gesture, bat spawn, summon crack and undead rise; rod charge/fire/hit; thunder warn/strike | Float accents, teleport out/in | Fatal blast plus disintegration and musical defeat cue |

Caster/archer windups cancel on interruption; releases sound only when the projectile spawns at animation frame 5. Warrior windup starts at frames 0-2, bandit at 0-1, undead at 0-3. Dave's swing starts at active frame 2, around 0.10 seconds into the contracted 0.45-second animation, not on each click. No enemy frame timing is inferred from the WAV duration. Surface-break, foot-contact and teleport audio events remain Claude's animation integration work.

## Text sound behaviour

Undertale is a **behavioural reference**: a small character-associated sound accompanies progressive text. All timbres, source recordings and synthesized waveforms must be original. No extracted samples, identifiable character voice imitation, full words or spoken sentences.

- Dave: four warm, firm human nonverbal murmurs, 75/80/90/95 ms.
- Pharaoh: four low, dry, resonant nonverbal murmurs with audible upper harmonics, 90/95/100/110 ms.
- Narrator: four soft paper/felt/air text appearances, 50/60/70/75 ms. These are not a third speaking voice.

Use approximately every second newly revealed letter or digit, excluding spaces and punctuation; select a take without immediate repeat. Runtime pitch variation is restrained to **+/-6%**, as contracted; do not bake four widely separated pitches. Match the narrative's minimum 75 ms between onsets, 120 ms comma pauses and 240 ms sentence-punctuation pauses (use the same sentence pause for ellipsis; semicolon may use 120 ms). One active text sound globally across all speakers and variants; all IDs share that cap. Never queue a backlog: if occupied, drop that reveal sound. Stop and clear scheduling on instant reveal, skip, speaker change, line close and scene exit, with a 5 ms click-free stop. No additional sound for every letter in text that is revealed instantly.

## Relative loudness and simultaneous playback

The manifest gives **proposed runtime gain offsets** in dB relative to the audition reference `snd_sword_hit` at 0 dB. These are starting balances, not measured output levels or extra export normalization. Music is first mastered to -16 LUFS integrated; its listed gain is then applied at playback. Short SFX and blips have no integrated LUFS target. Set source levels by listening and preserve peaks at or below -1 dBFS; do not normalize quiet paper ticks and rumbles to sound as loud as a sword hit.

Priority 100 is most protected. Warnings, Dave damage/death and save success must remain understandable. Footsteps, swarm movement and idle accents yield first. Per-ID global caps include all variants; per-emitter caps prevent one object retriggering itself. The per-ID numbers do not override these proposed shared budgets:

| Shared group | Maximum active voices | Arbitration |
|---|---:|---|
| Music | 1 steady state, 2 only during a crossfade | Explicit transition ownership; no room-stack accumulation |
| All SFX including weather | 24 | Drop/steal lowest-priority distant movement first; reserve headroom for danger/death cues |
| Attack warnings within SFX | 6 | Thunder one per wave/cluster, laser one per rod, nearby committed threats first; never queue warning until after damage |
| All movement/footstep cues | 6 | Prefer Dave and nearest enemies; drop distant excess |
| Projectile travel within SFX | 4 | Magic loops plus nearby arrow flybys share this cap; keep nearest, stop on projectile destruction |
| Weather | 1 | One zone-owned wind loop; fade rather than layering a new one |
| Dialogue/narration | 1 total | Drop busy reveal ticks; cancel on skip; never overlap speakers |

Maintain music, SFX and dialogue volume controls from the brief. Proposed sidechain starting points for Claude: text active reduces music 4 dB and wind 8 dB with ~100 ms attack/350 ms release; committed attack warnings reduce music 3 dB and weather 6 dB with 30/250 ms envelopes. Do not add both ducks arithmetically; use the stronger applicable reduction. Boss battle normally suppresses storms. A 30-50 ms fade on stolen ambience prevents clicks; do not steal an active critical warning to admit a footstep. Test final gain structure with worst-case cues for master headroom rather than assuming file peak ceilings prevent mixed clipping.

Single events use the per-asset cooldown. A cooldown drops the new request; it never delays it. Variant selection avoids immediate repeat, with no additional automatic pitch shifts proposed for SFX. Death and special confirmation cues replace generic hurt/confirm where specified. Only one pickup sound plays per transaction/batch, and restore/load never replays persistent rewards or gate interactions.

## Export and loop delivery

Every production file is **WAV, signed PCM 16-bit little-endian, 44,100 Hz**. Music is stereo at **-16 LUFS integrated +/-1 LU**; SFX, wind and all blips are mono. Keep every peak at or below **-1 dBFS**; targeting -1 dBTP for music is an additional production preference. Use 2-5 ms edge envelopes on one-shots to prevent clicks, trim leading dead air, and keep the designed decay inside the stated duration. Blip durations include both edge envelopes. Do not put a fade or silent padding at a whole-file loop seam.

| Loop ID | Seconds | Sample frames at 44,100 Hz | Channels |
|---|---:|---:|---:|
| `mus_desert` | 96 | 4,233,600 | 2 |
| `mus_pharaoh` | 90 | 3,969,000 | 2 |
| `snd_wind_loop` | 12 | 529,200 | 1 |
| `snd_magic_travel` | 1.5 | 66,150 | 1 |
| `snd_worm_rumble` | 3 | 132,300 | 1 |
| `snd_laser_charge` | 1 | 44,100 | 1 |
| `snd_laser_fire` | 0.8 | 35,280 | 1 |

All planned loops use the whole file: start 0 seconds, end equal to its duration. The start frame is inclusive and the end frame exclusive. Seamlessly wrap instrument releases, reverb and noise movement; align DC offset, waveform continuity and musical pulse across the boundary. No pickup intro is assumed. For charge/fire loops, fade at playback boundaries; the warning begins immediately and the runtime state determines how long it persists.

The contract permits whole-file looping without a sidecar, but production should include a factual `<asset>.json` once the **actual** WAV is finalized, for example `{"loop_start":0,"loop_end":96}` for `mus_desert.json`. Do not ship these example values as verified metadata for a file that does not exist. If a generator cannot produce the exact length, edit/recompose in a DAW and validate the resulting frame count, or deliver accurate nonzero points for Claude's review; never label an arbitrary crop seamless. File-loop QA must be passed before placeholders are replaced.

## Production order

1. **Milestone A vertical slice:** sword swing/hit, Dave hurt, sand steps, undead attack/movement/death, chest, potion/heal, pickup, checkpoint/save and UI move/confirm/cancel. Establish the loudness reference with actual combat audition.
2. **Milestone B enemy families:** remaining melee and ranged identities, projectile cleanup, family movement/deaths, worm warning/emergence, inventory and leveling. Material impact accents are optional polish.
3. **Milestone C world:** wind, stone/wood player steps and weather transition audition.
4. **Milestone D saving:** error/denied actions and success-vs-request distinction; three slots reuse one success cue.
5. **Milestone E opening and score:** record/synthesize the 12 text sounds, compose intro/desert/gameover, then optional rubble/cloth details. Lock motif and loop accuracy in a DAW.
6. **Milestone F encounter and ending:** Pharaoh score, summons, laser, thunder, gates, defeat and chapter ending. Telegraphs and death cleanup take priority over optional hover accents.

For each ID, generate or record several candidates from its complete prompt, select the requested matched variations, edit/compose to the required duration, export and validate, then change status only for real reviewed files. Keep source sessions and provenance outside the runtime bundle. Use a progress status such as pending, generated-unreviewed, edited, audio-validated and integrated; 213 delivered WAVs have passed objective audio checks; 0 planned WAVs remain pending.

## Acceptance checks for production and Claude

- Inspect real WAV headers, channels, bit depth, sample rate, peak, duration, DC offset, leading silence and file integrity. Music needs an actual integrated LUFS measurement. Record hashes, source/provenance, measured loudness and exact loop points when files exist; delivered files include measured headers, duration, peak and hashes in their sidecars; every delivered music file also includes integrated loudness.
- Audition at least five repeats of every loop on headphones and speakers, checking the seam for clicks, rhythm jumps, reverb pumping and obvious gust repetition. Verify music note choices and original motif by ear or MIDI, not prompt text alone.
- Check voice takes at normal and +/-6% pitch, with 50-110 ms native durations, one-voice reveal playback, punctuation pauses and rapid skip/reveal input. Confirm no intelligible words and no recognizable borrowed recordings.
- In the IDE, validate active-frame swings, release-frame projectiles, immediate telegraphs, accepted damage only, batch pickup, successful save only and silent persistent-state restoration. No GameMaker compile or play-test is claimed here.
- Stress a boss barrage with summons, travel loops and music. Verify readable warnings, bounded simultaneous playback, safe master headroom, no orphaned sounds after death/reset, no mass enemy-death burst during whiteout and no weather under critical dialogue.
- Listen through intro skip, pre-boss skip, Dave death/retry, boss defeat/load and ending/menu exit. Confirm smooth stop/fades and one owner for each loop. Claude validates all playback and integration behaviour.
