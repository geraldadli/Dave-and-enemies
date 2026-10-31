# Dave's & Enemies Chapter I narrative art and audio requests

Produce the following content for the final script in [NARRATIVE_SCRIPT.md](NARRATIVE_SCRIPT.md). Follow [PROJECT_CONTRACT.md](PROJECT_CONTRACT.md) and the existing milestone E/F IDs in [ASSET_REQUESTS.md](ASSET_REQUESTS.md). These are production requests; no image, animation or audio file is delivered in this narrative pack.

## Art requirements

Match the smooth cartoon style, dark outlines, soft cel shading, top-left lighting and established chibi proportions. Dave has long golden-brown hair, shining but battle-worn armor, a red cape and his sword in the right hand. Keep his equipment and silhouette consistent across portraits, cinematic poses and gameplay. Use the existing top-down three-quarter view. Wind travels east to west.

All images are 8-bit RGBA PNG, sRGB, straight alpha. Deliver exact, untrimmed canvases with a reference sheet. Do not bake ground shadows; engineering draws them. Portraits must read at 208×208 in the 1280×720 GUI.

| Priority | Asset IDs | Exact deliverable | Acting and use |
|---|---|---|---|
| P0 | `spr_intro_wall` | 1920×640, one frame; stage top-left origin (0,0), noncolliding cinematic backdrop | Breached Holy City fortifications, roughly 400 px gap at local x=760-1160, broken masonry and a ruined banner attachment. No visible Grail or living person. Reuse consistent masonry colors from the desert ruins. |
| P1 | `spr_intro_sky` | 1280×720, one opaque backdrop, origin (0,0) | Restrained dusty atmosphere behind the wall; compatible with the established perspective. Optional parallax at a slower pan rate; no new landmark with story significance. Base renderer can use a flat muted backdrop. |
| P0 | `spr_intro_rubble_01` through `04` | Canvases 64×64, 96×96, 128×96, 160×128; base-centre origins (32,56), (48,88), (64,88), (80,120); cinematic decoration without collision | Four readable broken stone clusters. Keep the foreground spacious enough to frame the fallen comrades without concealing them. |
| P0 | `spr_intro_fallen_01` through `03` | 128×64 each, origin (64,56), one frame per comrade; decorative, no collision | Three distinct motionless fallen city defenders, modest armor and cloth, respectful silhouettes without gore. No breathing, glow, twitching, ghosts, names or individual backstories. |
| P0 | `spr_intro_banner` | 128×192, origin (64,176); 6 frames at 8 fps looping; decorative | Torn city banner, attached at the right, pulling left. Optional still-frame fallback if wind motion is supplied by engineering. No readable heraldic text. |
| P0 | `spr_intro_spear` | 128×64, origin (64,56), one frame; decorative | Broken spear among the rubble; rotate/duplicate only as needed. No additional weapon quest. |
| P0 | `spr_dave_wind_idle_down` | 96×96, origin (48,88), 12 frames at 12 fps looping | Sole standing survivor, sword lowered, head slightly bowed; golden-brown hair and red cape pull left. Feet remain fixed. |
| P1 | `spr_dave_grief_down`, `spr_dave_vow_down` | 96×96, origin (48,88), one still pose each | Grief: bowed head and closed free hand. Vow: raised head, free hand resting at breastplate. P0 fallback uses wind idle plus the portrait expression; never stretch the sprite for acting. |
| P0 | `spr_dave_turn` | 96×96, origin (48,88), 4 frames at 8 fps, once | Down to down_side to side, facing right by final frame. Plays over 0.5 s at the start of shot 7; fixed feet and consistent sword hand. Reuse gameplay side walk after the turn. |
| P0 | `spr_portrait_dave` | 512×512 bust, facing right, one base portrait | Warm, firm, battle-worn paladin. Neutral resolve suitable for "Step aside." Clear anatomy and restrained surface detail; preserve hair, armor, cape and lighting. |
| P1 | `spr_portrait_dave_solemn`, `spr_portrait_dave_determined` | 512×512 each, same crop, scale, pose family and lighting as base | Solemn eyes lowered for regret; determined steady gaze for the vow and ending. These resolve through the sidecar expression map; fallback is the base portrait. |
| P0 | `spr_portrait_pharaoh` | 512×512 bust, facing right, one base portrait | Ancient undead ruler, regal headdress and weathered remains, controlled menace. Visually match the 192×192 boss sprite and rod. He must not hold or display the Grail. A rage portrait is unnecessary for this script. |
| P0 reuse | `spr_pharaoh_idle`, `spr_pharaoh_death` | Follow F1: 192×192, origin (96,176); idle 8-frame loop; death 16 frames at 12 fps for the cinematic | Float facing down during the exchange. No rod charge while talking. Death is a single disintegration/blast, followed by a slow screen fade drawn in code. |
| P0 reuse | `spr_gate_arena`, `spr_door_sealed`, `spr_dungeon_entrance` | Follow F5: 192×192, 192×224, 384×320 | Gate closes behind a fully entered Dave; dungeon route opens only after victory. Entrance remains dark; no playable interior is requested. |
| P2 | `spr_ending_bg` | 1280×720, one frame, origin (0,0) | Restrained silhouette of the threshold or plain dark background. Render "To Be Continued" and the menu button as live text, never baked into the background. |

Reuse existing light/dark sand, masonry, sand particles, footstep dust and Dave's side-walk animation. Cinematic rubble/fallen/spear origins are staging proposals for Claude's importer; they do not alter gameplay collision conventions.

The intro stage is 1920×1080. Place Dave at ground (1040,790) with the wall behind him; arrange three fallen defenders in the foreground and to his sides. Keep the eastward route clear through ground (1536,790). The camera pans at native scale, without zooming above 1.0. Use low-density drifting sand so every pose and text remains readable. Repeated ambient loops may move cloth and sand, never the fallen comrades.

## Vocal blip requests

All voices are original, short nonverbal murmurs, without words or full spoken dialogue. Deliver WAV PCM 16-bit, 44.1 kHz, mono, silence trimmed, peak at or below -1 dBFS. Each file is independent and non-looping. Match perceptual loudness across a speaker's four variants; let the game apply mix gain.

| Profile | Exact asset IDs | Length per variant | Direction |
|---|---|---|---|
| `voice_narrator` | `snd_voice_narrator_1` through `4` | 50-75 ms | Soft breath-like text tone; low presence, neutral, solemn. |
| `voice_dave` | `snd_voice_dave_1` through `4` | 70-95 ms | Warm and firm, human-sounding, closed-mouth vowel texture. Grief stays restrained; resolve never becomes a shout. |
| `voice_pharaoh` | `snd_voice_pharaoh_1` through `4` | 90-110 ms | Low, dry and resonant, with a controlled ancient rasp. Short tail that does not muddy repeated playback. |
| `silent` | none | — | Objective, checkpoint, title and interface text never mutter. |

The existing E7 row lists three narrator variants; contract section 9 requires four per speaker. Request narrator variant 4 to satisfy that rule. If delivery initially contains only three, use the available set without fabricating a missing resource; silence is the fallback when none exist.

The manifest specifies one blip for roughly every second eligible character, ±6% pitch, at least 75 ms between onsets, punctuation pauses, and one simultaneous blip. Reveal, advance and skip stop blips immediately. No recognizable sound from Undertale or another game is requested.

## Music and environmental sound

Music is stereo WAV PCM 16-bit, 44.1 kHz, around -16 LUFS integrated, without clipping; request peak at or below -1 dBFS. Supply key, tempo, duration and loop points in sidecar JSON. SFX are mono except the explicitly requested stereo wind ambience in existing E9. Separate blips, SFX and music in the game's mix.

| Priority | Asset ID | Length and loop | Required timing and direction |
|---|---|---|---|
| P0 | `mus_intro` | 54 s, non-looping, with a clean fade/tail by 54 s | 0-13 s: spare sustained texture and loss; 13-20 s: thin the melody under the stolen-Grail line; 20-27 s: quiet regret; 27-43 s: introduce and broaden a restrained resolve motif; 43-52 s: measured forward pulse; 52-54 s: fade. Space for vocal blips, no choir words or triumphant quest-completion cadence. |
| P0 reuse | `mus_desert` | 60-120 s seamless loop or supplied loop points | Exploration and cleared-arena continuation. Follow the existing C, Db, E, F, G, Ab, B pitch palette, transposable. Fade in at arrival; duck/fade before the Pharaoh speaks. |
| P0 reuse | `mus_pharaoh` | 60-120 s loop, 120-140 bpm per F7 | Start at the combat handoff, after the exact exchange. Stop/fade on boss death. Intro dialogue has wind and intentional musical space. |
| P0 | `mus_ending` | 10 s, non-looping | Begin at the threshold; leave room at 2-5 s for Dave's final line. A restrained chapter-resolution phrase supports the title at 6 s; leave the harmony open and end its tail at 10 s. Title then holds in silence. |
| P0 | `snd_wind_loop` | 8-15 s seamless stereo ambience, per E9 | Gentle right-to-left sand presence; fade in over 1.5 s at opening. Transfer/fade smoothly on arrival, duck during text and the boss exchange, fade out over the first 2 s of ending. Do not layer duplicate wind loops. |
| P1 | `snd_intro_banner` | 0.3-0.8 s, mono, one shot; one or two variants | A restrained cloth flutter at 1.5 s of opening; no startling crack. Optional production detail. |
| P1 | `snd_intro_grit` | 0.2-0.6 s, mono, one shot | A few pebbles settle at 14 s of opening. Optional and quiet; no sound implying a surviving comrade moves. |
| P0 reuse | `snd_step_sand` | Four short mono footstep variants from A11 | Use the existing animation step events during the eastward walk; variant naming resolves through engineering's SFX mapping. Stop immediately on skip. |
| P0 reuse | `snd_gate_slam` | Mono, trimmed one shot, per F6 | One gate close as Dave is fully inside; skipped presentation must not produce repeated slams. |
| P0 reuse | `snd_boss_death`, `snd_disintegrate` | Mono one shots, per F6 | One controlled impact and dissolving texture at zero HP; no repeated blasts or strobing. Stop abandoned tails when leaving the scene. |
| P0 reuse | `snd_checkpoint`, `snd_save`, UI move/confirm/cancel | Follow A11 | Save success sound only after a successful save. Never combine these with narrator blips. |

The storyboard's `score_direction` cues describe what is baked into the music, rather than extra audio events the runtime must trigger. The `animation_step_events` action delegates to the walk animation's contacts. Cue names and IDs are content bindings for Claude to map to the audio system.

## Production checks

Check native size, alpha, origins, feet alignment, right-facing portraits and consistent lighting before replacing placeholders. Audition voice sets at the scripted cadence with the ±6% pitch range. Confirm seamless wind/music loops and supplied loop metadata, and listen to the 54-second intro against its seven text windows. Preview the slow whiteout and reduced-flash alternative in GameMaker.

Keep placeholder art and sound until each replacement passes validation. This request adds no major character, Grail recovery image, dungeon interior or extra spoken dialogue.

