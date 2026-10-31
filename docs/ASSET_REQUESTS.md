# ASSET_REQUESTS — ordered by playable milestone

Conventions, canvases and formats: see `PROJECT_CONTRACT.md`. Directions `5dir` = down, down_side, side, up_side, up (side faces right). `3dir` = down, side, up.
"Temp" = what the engine uses until the deliverable passes validation.

## Integration status (updated 2026-10-31, engineering)

Scope change recorded: the desert is now three large scenes (`rm_sc_desert_frontier`, `rm_sc_caravan_basin`, `rm_sc_royal_expanse`; design `desert_scenes_v2`). The 24-room layout request (C5) is superseded. Dave's west facing is authored, not mirrored: `spr_dave_walk_left` and `spr_dave_attack_left` are contract IDs.

| Delivery | Status in the project | Still requested |
|---|---|---|
| Dave down v001 (`spr_dave_idle_down`, `spr_dave_walk_down`, `spr_dave_attack_down`) + base | Imported; frame/size/alpha/strip checks passed (`docs/integration/import_validation.json`). Engine preview pending (IDE). | — |
| Dave cardinal v001 (`spr_dave_walk_side/left/up`, `spr_dave_attack_side/left/up`) + bases | Imported, west bound to `*_left` with `image_xscale = 1`. Engine preview pending. | Idle side/left/up (bases used as stand-in), all diagonals (`*_down_side`, `*_up_side` and left-handed counterparts), hurt, death, potion (A1–A3 remainder, B1) |
| UI prototype frame kit (`spr_ui_*`) | Imported as prototype frames (not production-final). | Production polish optional |
| Noto Sans Regular/Bold + OFL | Pre-rendered `fnt_ui_meta/body/heading/dialogue/title` at 18/23/28/28/46 px; `OFL.txt` shipped in `datafiles/licenses/`. | — |
| Narrative (`dialogue.json`, `narrative_manifest.json`, `intro_storyboard.json`) | Included Files; bound by scene ID/line index/stable line ID. | Portraits E5, intro art E2–E4 |
| Production audio, 213 WAVs / 98 IDs | Imported and wired (`docs/audio/AUDIO_INTEGRATION_REPORT.md`). Listening review pending. | — |
| Scenes `desert_scenes_v2` | Converted to rooms + `datafiles/data/scenes/*.json`. | Terrain textures (A5, C1), stairs/bridge sheets (C2, C3), props (C4) |
| Everything else in the tables below | Not delivered; labelled placeholders (`spr_ph_*`, template sprites, code-drawn FX) are in use. | As listed |

Name collision to resolve when B6 arrives: the template already has a 200×200 `spr_bat_fly`. Smallest correction: deliver the 64×64 bat as `spr_bat_fly` and engineering replaces the unused template resource (the runtime currently looks for `spr_bat_fly_64` first, then scales the template bat by 0.5).

## Milestone A — vertical slice (movement, combat, one enemy, chest, checkpoint, two rooms)
| # | Asset ID | Purpose | Size / footprint | States, directions, frames | Pri | Temp exists? |
|---|---|---|---|---|---|---|
| A1 | `spr_dave_idle_<5dir>` | Dave idle | 96×96, origin (48,88) | 8 f, 10 fps loop; cape and hair sway | P0 | **Down delivered.** Side/left/up use the delivered reference bases; diagonals not delivered |
| A2 | `spr_dave_walk_<5dir>` + `spr_dave_walk_left` | Dave run | 96×96, (48,88) | 10 f, 20 fps loop; feet contact f2, f7 | P0 | **Down, side, left, up delivered.** Diagonals fall back to side/left |
| A3 | `spr_dave_attack_<5dir>` + `spr_dave_attack_left` | Sword slash | 128×128, (64,112) | 8 f: 0–1 anticipation, 2–4 active, 5–7 recovery; ticks [3,3,3,3,3,4,4,4] | P0 | **Down, side, left, up delivered.** Diagonals fall back to side/left |
| A4 | `spr_fx_slash` | Slash arc drawn during active frames | 128×96, origin (16,48), arc points +x (east) | 4 f, 20 fps once; white-gold arc. Engine rotates it toward the mouse | P0 | Yes: template `spr_sword_attack` |
| A5 | Textures `tex_sand_light`, `tex_sand_dark`, `tex_rock_top`, `tex_cliff_face` | Ground, paths, canyon walls | 256×256 seamless (cliff face: 256×64 repeating horizontally) | 1 each; light sand needs 3 detail variants (ripples, pebbles, cracks) | P0 | No: procedural placeholder to be generated |
| A6 | `spr_undead_*` | First enemy (slow melee) | 128×128, (64,112) | idle_down 6 f · walk_<3dir> 8 f · attack_<3dir> 8 f (windup f0–3, active f4–5, recovery f6–7) · hurt_down 2 f · defeat 8 f · rise 10 f | P0 | Yes: template skull "baddie" set |
| A7 | `spr_chest_desert` | Treasure chest | 64×64, origin (32,56); footprint 48×20 | closed 1 f, opening 4 f, open 1 f | P0 | Yes: template `spr_chest`, `spr_chest_open` |
| A8 | `spr_checkpoint_star` + `spr_fx_sparkle` | Glowing yellow save star | 64×64, origin (32,48); 16×16 sparkle | star 8 f 10 fps loop (gentle pulse); sparkle 6 f once | P0 | No: procedural placeholder planned |
| A9 | `spr_icon_potion_health` | Potion item icon | 64×64 | 1 f | P0 | No |
| A10 | HUD kit (**prototype delivered**): `spr_ui_hp_frame`, `spr_ui_hp_fill`, `spr_ui_slot`, `spr_ui_slot_selected`, `spr_ui_panel` (9-slice) | Health bar, hotbar, panels | bar 320×32; slot 72×72; panel 96×96 source with 24 px borders | 1 f each | P0 | Partial: template hearts and buttons; code-drawn fallback |
| A11 | SFX: `snd_sword_hit`, `snd_checkpoint`, `snd_save`, `snd_potion_drink`, `snd_heal`, `snd_pickup`, `snd_step_sand`, `snd_ui_move`, `snd_ui_confirm`, `snd_ui_cancel` | Core feedback | WAV mono | 1 each (step: 4 variants) | P0 | Partial: template `snd_sword_swing`, `snd_hurt`, `snd_chest_open`, `snd_coin`, `snd_button`, `snd_footstep` |
| A12 | UI font family (OFL TTF + licence) | All text | sizes in contract §9 | Regular and Bold | P0 | **Delivered** (Noto Sans) |

## Milestone B — enemy families, loot, inventory, progression
| # | Asset ID | Purpose | Size | States / frames | Pri | Temp? |
|---|---|---|---|---|---|---|
| B1 | `spr_dave_hurt_<5dir>`, `spr_dave_death`, `spr_dave_potion` (down) | Damage, death, drinking | 96×96; death 128×96 (64,88) | hurt 3 f · death 10 f (holds last) · potion 8 f at 16 fps | P0 | Partial: `spr_player_defeated` |
| B2 | `spr_skeleton_warrior_*` | Sword or spear melee | 128×128 | same set as A6 without rise; attack: windup f0–2, active f3–4 | P0 | No (baddie recolour) |
| B3 | `spr_skeleton_archer_*` + `spr_arrow`, `spr_fx_arrow_hit` | Ranged | 128×128; arrow 32×8 (16,4) pointing east; hit 48×48 | attack = draw and release, **release f5**; nock offset per direction in JSON; hit 6 f | P0 | Partial: template `spr_bat_projectile` |
| B4 | `spr_bandit_*` | Fast melee | 128×128 | like A6; attack windup f0–1, active f2–4 | P0 | No |
| B5 | `spr_bandit_caster_*` + `spr_magic_orb`, `spr_fx_magic_launch`, `spr_fx_magic_hit` | Ranged magic | 128×128; orb 32×32 centre; FX 64×64 | cast 8 f, **release f5**, staff-tip offset per direction; orb 4 f loop; launch 6 f; hit 8 f | P0 | Partial: template bat projectile and splatter |
| B6 | `spr_bat_fly`, `spr_bat_dive`, `spr_bat_defeat` | Circling and diving flyer | 64×64 centre origin | fly 6 f 15 fps loop · dive 4 f · defeat 6 f | P0 | Yes: template `spr_bat_fly` (200×200) |
| B7 | `spr_python_*` | Coil and lunge | 128×96 (64,72) | slither_<3dir> 8 f 12 fps · coil (telegraph) 6 f · lunge_<3dir> 4 f · hurt 2 f · defeat 8 f | P1 | No |
| B8 | `spr_sandworm_*` | Burrow, emerge, attack | 192×192 (96,176) | mound 6 f loop (also the warning) · emerge 8 f · idle_up 6 f loop · attack 8 f (active f4–5) · burrow 8 f · hurt 2 f · defeat 10 f | P1 | No |
| B9 | Item icons `spr_icon_<id>` | Inventory | 64×64 | weapons: longsword, bandit_scimitar, sunsteel_blade · armour: worn_tabard, iron_tunic, paladin_mail, wanderer_tunic · valuables: gold_coins, desert_rose, golden_scarab, ancient_coin, pharaoh_ankh (boss reward) · potion_greater | P1 | No |
| B10 | FX: `spr_fx_hit`, `spr_fx_dust`, `spr_fx_poof`, `spr_fx_heal_ring`, `spr_fx_heal_particle`, `spr_fx_levelup` | Feedback | hit 64×64; dust 48×32; poof 96×96; heal ring 128×64 (ground ellipse, **red**); particle 16×16 | 6–8 f each | P1 | Partial: template splatter |
| B11 | Enemy SFX: attack per family, `snd_bow_release`, `snd_arrow_hit`, `snd_cast_charge`, `snd_magic_travel` (loop), `snd_magic_hit`, `snd_bat_screech`, `snd_snake_hiss`, `snd_snake_lunge`, `snd_worm_rumble` (loop), `snd_worm_emerge`, `snd_worm_bite`, deaths, `snd_levelup`, `snd_inventory_open` | Combat audio | WAV mono | 1–3 variants each | P1 | Partial: template bat, baddie, coin and powerup sounds |

## Milestone C — connected desert world
| # | Asset ID | Purpose | Size / footprint | Notes | Pri | Temp? |
|---|---|---|---|---|---|---|
| C1 | Textures `tex_grass`, `tex_water` (4 f animated optional), `tex_wet_sand`, `tex_paving`, `tex_masonry_top`, `tex_masonry_face`, `tex_chasm_wall`, `tex_chasm_void` | Remaining terrain | 256×256 seamless (faces 256×64) | engineering builds the blends | P0 | Procedural |
| C2 | `ts_stairs` sheet | Wide desert stairs | 192×128 (3 wide × 2 tall, 64 grid): left / mid / right × top / bottom | mid tile must repeat horizontally | P0 | No |
| C3 | `ts_bridge` sheet | Bridges | 64-grid: E–W planks (rope top, rope bottom, both, none), N–S same, broken E–W ×2, posts 32×64 | clear entrances | P0 | No |
| C4 | Props (origin = base centre) | Landmarks and obstacles | cactus_tall 64×128 (fp 24×16); cactus_small 48×64; rock_small ×3 48×40; boulder ×2 128×112 (fp 96×40); tree_desert 160×160 (trunk fp 24×14); tree_dead 128×160; palm ×2 128×192; bush, bush_dead 64×48 (no collision); pebbles ×3 and skull ×2 flat decals 64×64 / 32×32; ruin_block ×3 64–128; wagon_wreck 192×128 (fp 160×40); obelisk 96×224; pharaoh_statue 128×256; tumbleweed 48×48 (engine rotates) | 1 f each (tumbleweed 1 f) | P0–P1 | Partial: template pillars, bones, rocks |
| C5 | ~~Room layouts ×24~~ **superseded** by `design/desert/scenes/*.json` (three scenes) | Maps and encounters | contract §10 core keys | delivered as desert_scenes_v2 and integrated | — | Done |
| C6 | `spr_healing_spring` | Optional-room landmark | 128×96 | 4 f loop | P2 | No |

## Milestone D — checkpoints and save/load UI
| D1 | (**prototype delivered**) `spr_ui_save_card`, `spr_ui_save_card_empty`, `spr_ui_button` (9-slice) | Three-slot save screen, menus, Game Over | card 760×120; button 64×64 source with 16 px borders | normal / hover / pressed | P1 | Code-drawn fallback |

## Milestone E — opening cutscene, portraits, dialogue, audio
| # | Asset ID | Purpose | Size | Notes | Pri | Temp? |
|---|---|---|---|---|---|---|
| E1 | Storyboard `intro_storyboard.json` (**delivered**, 54 s) | Shot list with timing (45–60 s) | — | shots: start s, duration, camera target and zoom, text lines, sound cues | P0 | Engineering draft |
| E2 | `spr_intro_wall` (+ optional parallax layers) | Breached Holy City wall | 1920×640 (wall), sky 1280×720 | breach gap ~400 px | P0 | No |
| E3 | `spr_intro_rubble_*` ×4, `spr_intro_fallen_*` ×3, broken banner, spears | Aftermath props | rubble 64–160; fallen 128×64 (respectful, no gore) | 1 f each | P0 | No |
| E4 | `spr_dave_wind_idle_down` (12 f 12 fps), `spr_dave_turn` (down → down_side → side, 4 f) | Cutscene acting | 96×96 (48,88) | strong wind toward the west (screen left) | P0 | No |
| E5 | `spr_portrait_dave`, `spr_portrait_pharaoh` | Dialogue | 512×512, facing right | optional extra moods: dave_determined, pharaoh_rage | P0 | No |
| E6 | `dialogue.json` (**delivered**) | Narration, vow, boss lines, item pickup lines | format in contract §10 | use the brief's lines | P0 | Engineering draft |
| E7 | Blips `snd_voice_dave_1–4`, `snd_voice_pharaoh_1–4`, `snd_voice_narrator_1–4` (**delivered**) | Nonverbal text voices | 50–110 ms | Dave warm and firm; Pharaoh low, dry, resonant; narrator soft | P0 | No |
| E8 | Music `mus_intro` (non-loop ~50 s), `mus_desert` (loop 60–120 s, pitch set C Db E F G Ab B transposable), `mus_ending` (8–15 s resolution), `mus_gameover` (3–5 s sting) | Score | stereo WAV | document key and loop points | P0–P1 | Template `snd_music_*` (dungeon mood) |
| E9 | `snd_wind_loop` (**delivered**, mono per contract) | Sandstorm | seamless 12 s | — | P1 | No |

## Milestone F — Pharaoh encounter and ending
| # | Asset ID | Purpose | Size | States / frames | Pri | Temp? |
|---|---|---|---|---|---|---|
| F1 | `spr_pharaoh_*` | Boss | 192×192 (96,176) | idle 8 f loop · summon 10 f · laser_charge 8 f (rod-tip offset per frame in JSON) · laser_fire 4 f loop · thunder_cast 8 f · hurt 2 f · teleport_out / in 6 f each · death 16 f disintegration | P0 | No |
| F2 | `spr_laser_beam` (64×32, repeats horizontally, 4 f), `spr_fx_laser_charge` 64×64 8 f, `spr_laser_aim` 16×16 dash | Laser rod | — | — | P0 | No |
| F3 | `spr_thunder_marker` (ground ring 128×64, 4 f pulse), `spr_thunder_exclaim` 32×48, `spr_lightning_bolt` 96×384 origin (48,376) 6 f, `spr_fx_thunder_impact` 128×96 8 f | Thunder barrage | — | — | P0 | No |
| F4 | `spr_summon_crack` 96×48 6 f, `spr_fx_sand_burst` 96×64 8 f | Undead summon marker | — | — | P0 | No |
| F5 | `spr_gate_arena` 192×192 (spans 3 cells), `spr_door_sealed` 192×224, `spr_dungeon_entrance` 384×320 (doorway 128 wide) | Gates and ending threshold | — | gate open/close 8 f | P0 | Template gate sprites (64 wide), `spr_entrance` + gate particles |
| F6 | Boss SFX: `snd_boss_summon`, `snd_laser_charge`, `snd_laser_fire`, `snd_thunder_warn`, `snd_thunder_strike`, `snd_boss_hurt`, `snd_disintegrate`, `snd_boss_death`, `snd_undead_rise`, `snd_gate_slam` | Boss audio | WAV | — | P0 | Partial: template `snd_gate_iron_open` |
| F7 | `mus_pharaoh` | Boss theme | stereo, loop 60–120 s, 120–140 bpm | strong percussion, memorable motif | P0 | Template `snd_music_rampage` |
| F8 | `spr_title_bg` 1280×720, `spr_title_logo` 640×240, `spr_ending_bg` 1280×720 | Title and "To Be Continued" | — | — | P2 | Template menu background and logo |
