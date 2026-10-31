# Claude audio integration handoff

Continue the existing Dave's & Enemies project in:

`D:\GameMakerProject\Dave's & Enemies`

You are the lead GameMaker engineer and own audio resource import, playback, looping, mixing, event triggers and integration testing. Integrate the already-generated audio into the existing game. Preserve working systems and the established division of labour. This is an implementation request; carry out the integration and verification, rather than returning only a plan.

## Read the project and delivery specifications

Read applicable project instructions and these files before making changes:

1. `docs/PROJECT_CONTRACT.md`
2. `docs/audio/AUDIO_MANIFEST.json`
3. `docs/audio/AUDIO_CUE_SHEET.csv`
4. `docs/audio/AUDIO_PRODUCTION_PLAN.md`
5. `audio/music/AUDIO_DELIVERY.md` and `audio/music/MUSIC_DELIVERY.json`
6. `audio/SFX_DELIVERY.md` and `audio/SFX_DELIVERY.json`
7. `docs/NARRATIVE_SCRIPT.md` and the implemented storyboard/dialogue data

Use `docs/audio/AUDIO_PROMPTS.md` for additional intent when needed. The audio files already exist; regeneration is not part of this task. Delivery measurements establish technical file validation; human listening review and in-game validation remain outstanding.

The contract governs engine compatibility, naming and delivery formats. The manifest and per-asset JSON sidecars identify actual production files, hashes and measured durations. The cue sheet supplies each event's purpose, variants, trigger, stop, fades, proposed gain, cooldown, priority and voice limits. Reconcile narrative scene timing with these audio cues using the current implementation. Preserve established gameplay timing; document material discrepancies and the smallest integration correction.

## Import the complete production set

The delivery contains **213 production WAVs across 98 stable IDs**:

- `audio/music/`: 6 stereo music WAVs.
- `audio/sfx/`: 195 mono SFX WAVs, including variations and wind.
- `audio/voice/`: 12 mono blips: four Dave, four Pharaoh and four narrator.

Use each manifest record's `existing_delivered_files` as the production allowlist. Verify that every listed file exists and matches its delivery-sidecar SHA-256. Check WAV headers and expected durations; durations rounded to the nearest sample are valid. Count all 213 files exactly once in the import audit.

`audio/previews/` contains review montages. Exclude those reels, duplicate archive contents, score JSON, source scripts and existing template WAVs from the 213-production-file count. Import from the loose production directories; the ZIPs are convenience bundles and do not need extraction into the project.

Every production WAV is signed PCM 16-bit little-endian at 44,100 Hz. Music is stereo around -16 LUFS integrated; SFX/blips are mono, with peaks below -1 dBFS. Preserve the original WAVs under `audio/`. Choose GameMaker resource loading/compression settings appropriate to this LTS build, with seamless music and responsive short SFX. Do not globally normalize or change the source sample rate, channel layout, pitch or duration during import.

Keep existing template asset names unchanged. Resolve resource-name collisions through the existing project conventions: reuse a suitable resource after validation or use an unambiguous imported resource name and explicit mapping. Preserve useful placeholders until replacements pass validation, and remove obsolete playback routes once replacements are wired so both sounds do not fire together.

A stable event ID may represent several files. For example, `snd_sword_hit` maps to the delivered `snd_sword_hit_1.wav` through `_3.wav`; the stable ID is not necessarily a native resource name. Dialogue take IDs such as `snd_voice_dave_1` are already individual IDs. Map every take explicitly, choose variants without immediate repetition and retain a trace from event ID to resource and source file.

## Implement playback using the existing architecture

Inspect the current audio and state systems first. Extend a shared audio service/manager using supported GameMaker LTS APIs and the project's current architecture. Keep trigger calls small and centralize variant selection, gains, fades, priorities, cooldowns, loop ownership and cleanup.

The manifest under `docs/` is design handoff data, not a prescribed runtime schema. Derive a compact runtime catalog using project conventions; keep production prompts and review metadata out of the runtime bundle. Runtime data belongs under `datafiles/data/` when Included Files are used.

Apply per-ID gain, cooldown, per-emitter limit and global limit from the cue sheet, together with the shared budgets below. Limits for an ID include all its variants. Drop requests rejected by a cooldown or cap; do not queue them to play late. Loop starts must be idempotent and return/store an owned playback handle, rather than creating another instance every game step.

Keep separate music, SFX and dialogue volume controls, using the existing settings/menu UI. Honor existing master volume and mute behaviour. Proposed dB offsets become linear amplitude using `10^(dB/20)` and are applied once, alongside user volume, state ducking and any positional attenuation. They are not baked into the source files. Use them as initial balances and adjust through listening while keeping warnings intelligible and the combined mix free of clipping.

Shared starting budgets:

| Group | Limit |
|---|---:|
| Music | 1 steady-state voice; 2 only during a crossfade |
| All SFX including weather | 24 |
| Attack warnings within SFX | 6 |
| Movement/footsteps within SFX | 6 |
| Projectile travel within SFX | 4 |
| Weather within SFX | 1 |
| Dialogue/narrator across all speakers and takes | 1 |

Protect committed warnings, Dave damage/death and important confirmations ahead of distant movement or idle accents. Give world SFX suitable positional attenuation; keep score, UI and text sounds unspatialized. Coordinate pause/inventory states, room unload, scene skips, death, load and encounter reset so owned loops and callbacks cannot accumulate or resume with a backlog.

Follow the production plan's proposed ducking: text lowers music 4 dB and wind 8 dB with roughly 100/350 ms attack/release; attack warnings lower music 3 dB and weather 6 dB with roughly 30/250 ms envelopes. Use the stronger applicable reduction rather than summing competing ducks. Audition and tune these starting values in context.

## Configure loops and story music

These seven assets loop their entire file, start inclusive and end exclusive:

| ID | Loop interval in seconds |
|---|---|
| `mus_desert` | 0-96 |
| `mus_pharaoh` | 0-90 |
| `snd_wind_loop` | 0-12 |
| `snd_magic_travel` | 0-1.5 |
| `snd_worm_rumble` | 0-3 |
| `snd_laser_charge` | 0-1 |
| `snd_laser_fire` | 0-0.8 |

Use the documented loop API behaviour and verified sidecar points. Add entry/exit fades at playback boundaries, not on every repeat. Keep one owner for each persistent loop. Wind is mono per PROJECT_CONTRACT, resolving the older stereo request.

The four other music assets are non-looping one-shots with endings already inside their exports:

- `mus_intro`: 54 s; align to the opening storyboard, with the vow motif at 27 s, broader resolve at 35 s, walking pulse at 43 s and fade at 52-54 s. Wind and text sounds remain separate. Handle reading holds through the current cinematic state model. On skip, cancel pending text/shot cues and fade abandoned intro audio over 300 ms before the exploration handoff.
- `mus_boss_defeat`: 6 s; start about 250 ms after confirmed Pharaoh death. It ends at sequence t=6.25 s, before the proposed exploration return at t=6.5 s.
- `mus_ending`: 10 s; start at threshold-sequence t=0, leave room for Dave's line at 2-5 s, support To Be Continued at t=6 s, then end in silence at t=10 s.
- `mus_gameover`: 4.5 s; play once on Game Over entry, around 250 ms after Dave's death cue. Fade it out on retry/load/menu selection as specified.

Keep `mus_desert` running across connected desert rooms instead of restarting it at every transition. Fade it for the pre-boss exchange; start `mus_pharaoh` once at the combat handoff after the final line is acknowledged. Do not restart the boss theme at health-phase thresholds. Follow the cue sheet's per-track gains and transition-specific fade overrides.

On Pharaoh death, stop attack scheduling and all owned warning, projectile and attack loops immediately. Play `snd_boss_death` and `snd_disintegrate` once, preserving their scene-owned tails through boss-instance destruction and whiteout. Clean up living summons silently; do not emit a mass death-sound burst. Restore low wind and exploration at the established cleared-arena beats. Loading a completed boss state must not replay defeat, gate or reward cues.

## Wire gameplay and UI feedback

Wire every stable ID to its intended event or documented optional variant/material route. Use the enemy coverage matrix in the production plan; do not invent new melee or ranged attacks to create sound triggers.

- Dave's swing fires once on entry to active attack frame 2, not on each click or each active frame. Successful impact fires only after accepted damage, once per swing-target pair. Choose at most one optional material accent per hit and respect clustered-hit limits.
- Nonfatal Dave hurt fires only for accepted HP loss after invulnerability checks. A fatal hit uses the death cue instead. Contact without damage stays silent. Enemy deaths fire once; preserve death tails after entity removal, with explicit cleanup on scene abort/reset.
- Footsteps follow actual movement contact events and surface selection. Dave's walk contacts use frames 2 and 7. Enemy movement sounds follow their own animation events; idle enemies and distant swarms should not produce constant movement chatter.
- Archer/caster windups cancel when interrupted. Their releases fire at frame 5 only when the projectile actually spawns. Stop projectile travel handles on hit, expiry, destruction or reset. Body/world arrow impacts are alternatives.
- Wire undead rise, bat dive/summon, python coil/lunge, worm rumble/emergence/bite/burrow, Pharaoh summon/teleport, laser charge/fire/hit and thunder warn/strike to their respective state events. Charge-loop length follows the telegraph state, not the one-second source length. Thunder warnings play per committed wave/cluster rather than per marked tile; strikes consolidate simultaneous tiles. Warnings must arrive before damage and remain audible in crowds.
- Potion drinking requires accepted consumption; healing requires actual HP gain. Pickup requires a successful inventory transaction, with one sound per batch. Level-up requires an actual level increase. Restoring persistent state must not replay these effects.
- Checkpoint interaction plays when its save UI opens. `snd_save` plays only after a successful save commit; failure uses the error route. Specialist confirmation sounds replace generic UI confirmation for the same action. Retain the existing three independent save slots and their overwrite behaviour.
- Wire chest opening/locked feedback, coin pickup, menu navigation, confirm/cancel, inventory open/close and gate transitions. Avoid held-input or unchanged-hover repeats and prevent menu clicks from triggering world combat.

Observe the rendered sync offsets: thunder warning taps are at 0 and 0.120 s; the main gate slam occurs about 0.495 s into `snd_gate_slam`; the chest lid-stop gesture is about 0.468 s into `snd_chest_open`. Align visual contact using scheduling or the smallest documented integration adaptation, keeping established gameplay timing intact.

## Integrate nonverbal text sounds

Use the delivered four-take profiles for `dave`, `pharaoh` and `narrator`. Dave has warm human-like murmurs, Pharaoh low dry resonant murmurs, and narrator soft text-appearance ticks. All are original synthesized sounds with no words or sentences; Undertale is only the behavioural reference.

Play approximately every second newly revealed letter or digit, excluding spaces and punctuation. Select takes without immediate repetition; apply pitch ratios within 0.94-1.06. Use at least 75 ms between onsets and one active blip globally. If the voice is occupied, drop that reveal sound rather than queueing it. Use 120 ms comma pauses and 240 ms sentence/ellipsis pauses, consistent with the narrative timing.

On instant reveal, skip, speaker change, line close or scene exit, cancel pending blips and stop the active blip with a click-free 5 ms fade. Text revealed instantly produces no backlog. Respect `silent` profiles for objectives, ordinary interface text and the ending title.

## Validate and deliver the integrated project

Perform feasible static/resource validation, listening checks and in-game testing. The contract records that command-line compilation is unavailable without a signed-in GameMaker licence; Igor can load/link, while compilation and play-testing require the IDE. Inspect current availability, complete all feasible work, and distinguish executed checks from the remaining IDE checklist. Do not claim compilation, listening or gameplay tests that were not performed.

Required checks:

1. All 213 source WAVs accounted for across 98 IDs, with valid imported resources and mappings; no preview reels imported and no missing or duplicate takes.
2. Five-repeat loop audition for all seven loops, checking runtime seams and room/state transitions. Four story cues end naturally once and never loop.
3. Frame/event alignment, accepted damage only, interrupted casts, projectile cleanup, each enemy family and all feedback routes.
4. Text reveal at normal and rapid speeds, punctuation, +/-6% pitch, instant reveal and skip; no overlapping speakers or queued sounds.
5. Checkpoint, successful/failed saving, inventory, full inventory, batch loot, repeated input and persistent-state restoration without duplicate feedback.
6. Crowded Pharaoh summons and thunder with bounded voice counts, audible warnings and master headroom; no abandoned laser/travel/weather loops.
7. Intro skip, pre-boss skip, Dave death/retry/load, boss whiteout, completed-boss load and ending/menu exit without stale audio or duplicate music.
8. Independent music/SFX/dialogue sliders and mute, plus pause/resume and room unloading.

Write `docs/audio/AUDIO_INTEGRATION_REPORT.md` with the source-to-resource mapping or its generated audit-file path, import count, implemented routes, resource/loading choices, gain/limit changes, executed checks and remaining work. Keep production provenance and technically-validated status accurate; record integration/listening status separately rather than relabelling all files final automatically.

Finish with a concise report of what was integrated, the 213-file audit result, tests actually performed, any remaining IDE/listening checks and the smallest steps needed to resolve material mismatches. Begin by inspecting the existing implementation, then perform the integration.
