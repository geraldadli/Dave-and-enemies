> SUPERSEDED: reference only. Use [the expanding scene design](DESERT_CHAPTER.md). These are no longer separate loaded areas.

# Desert design - batch 06

[Chapter graph, conventions and import rules](DESERT_CHAPTER.md). Grid = 64 px tiles, zero-based [x,y]. Rectangles and spans inclusive. Terrain JSON is authoritative; diagram letters overlay objects. Legend: . sand, , path, ; grass, ~ blocked water, # blocked cliff, M blocked masonry, _ paving, ^ stairs, C blocked chasm, = E/W bridge, | N/S bridge, x blocked broken span; e enemy, c chest, S star, p solid prop, t trigger, i initial spawn, g gate. Decorative placement has no collision and is listed separately.

## Pharaoh's Gate

Stable ID: `rm_d16_pharaohs_gate`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: An entirely safe final save star sits directly on the route to the arena vestibule. Intensity: **quiet**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
02  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
03  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
04  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
05  #...............MMM................#
06  #...............MMM................#
07  #...............MMM................#
08  #...............MMM................#
09  #...............MMM................#
10  __________________________.........#
11  __________________________.........#
12  __________________________.........#
13  #...............MMM....___.........#
14  #...............MMM....___.........#
15  #......................___..._____.#
16  #......................_____________
17  #......................________S____
18  #......................_____________
19  #............................_____.#
20  #..................................#
21  #..................................#
22  #..................................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d15_tomb_approach` / east | [33, 11] | always |
| east | E rows [16, 18] | [33, 17]; 4 | `rm_d17_pharaohs_courtyard` / west | [2, 17] | always |

Authored main walking line: [2, 11] -> [24, 11] -> [24, 17] -> [33, 17]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- The star is four tile columns from the east border opening, with no intervening room, reward detour or encounter.
- No water, chasm, stairs or bridge. Gate closure occurs inside D17 only after Dave clears the gate plane. Checkpoint remains usable after victory.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- None; preserve the quiet room.

Treasure:

- No chests.

Checkpoint / script data:

- `rm_d16_pharaohs_gate:checkpoint` at [31, 17]; respawn [31, 17]; clear pad [30, 16, 32, 18]. E interaction; three save slots; heal on successful save; no automatic overwrite.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d16_pharaohs_gate:deco1`: `spr_pharaoh_statue` at [25, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Still royal sentinel; no creature or ambush occupies the save room.
- `rm_d16_pharaohs_gate:deco2`: `spr_obelisk` at [11, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Inscription faces the last star and the arena entrance.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_checkpoint`, `snd_save`, `spr_checkpoint_star`, `spr_fx_sparkle`, `spr_obelisk`, `spr_pharaoh_statue`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d16_pharaohs_gate.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Pharaoh's Courtyard

Stable ID: `rm_d17_pharaohs_courtyard`. Dimensions: **40 x 24 tiles** (2560 x 1536 px). Purpose: A distinct paved royal arena with a bent entry vestibule supports the Pharaoh's complete encounter. Intensity: **boss**.

```text
    0         1         2         3         
    0123456789012345678901234567890123456789
00  ########################################
01  #______________________________________#
02  #______________________________________#
03  #______________________________________#
04  #___________________...........________#
05  #___________________...........________#
06  #________________e__...........________#
07  #___________________..........._________
08  #___________________..........._________
09  #___________________..........._________
10  #___________________...........________#
11  #______________________________________#
12  #MMMtttMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
13  #MMM___MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
14  #MMMgggMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
15  #MMM___MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
16  _________MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
17  _________MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
18  _________MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
19  #________MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
20  #________MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
21  #________MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
22  #________MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
23  ########################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [16, 18] | [2, 17]; 0 | `rm_d16_pharaohs_gate` / east | [33, 17] | always |
| east | E rows [7, 9] | [37, 8]; 4 | `rm_d18_dungeon_threshold` / west | [2, 8] | boss_pharaoh_defeated |

Authored main walking line: [2, 17] -> [5, 17] -> [5, 11] -> [5, 9] -> [16, 9] -> [16, 7] -> [37, 7] -> [37, 8]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- The west vestibule enters at y16..18 and turns north through a real horizontal gate. A solid masonry band y12..15 leaves only the x4..6 throat, so the row12 intro trigger cannot be bypassed.
- The fight floor is flat: central sand is ordinary floor, not a raised dais. No pits, water, stairs, bridges, pillars or permanent arena hazards.
- Seal the east border cells plus transition while idle/dialogue/combat/defeat. On victory remove the seal. No ordinary encounter-clear flag can unlock it.
- entrance_gate [4, 14, 6, 14]: Horizontal three-cell gate at the bend, matching the 192-pixel gate asset. Closes only when Dave is fully north of y13.
- sealed_exit [39, 7, 39, 9]: East transition and boundary collision remain sealed until boss_pharaoh_defeated. Use vertical masonry seal/energy effect, not a stretched horizontal gate.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d17_pharaohs_courtyard:boss`: pad/leash [9, 1, 32, 10]; max 1 active. Large uncluttered arena; pursuit, laser sidesteps, marked thunder and capped summons share no solid props. Only boss_entry dialogue completion; ordinary rectangle activation is disabled.
  - `rm_d17_pharaohs_courtyard:boss:e1`: `pharaoh` at [17, 6].

Treasure:

- No chests.
- Unique boss reward `rm_d17_pharaohs_courtyard:u1`, `pharaoh_ankh` x1 at [25,7], pending until inventory space exists; no Holy Grail.

Checkpoint / script data:

- `boss_entry`, event `boss_intro`, trigger [4, 12, 6, 12], persistent flag `boss_intro_seen`: Unavoidable throat trigger: test continuous occupancy while idle, not one-shot on_enter. If boss not defeated and full mask clears north of pixel y832 (top of row13): pause damage, walk one cell to safe mark [5,11], close gate [4,14..6,14], frame both actors at intro camera target, play narrative-owned boss_intro. Set intro-seen only when sequence starts. Skip initializes combat identically. Intro-seen flag must never suppress gate/combat restart after a failed attempt.
- `pharaoh_defeat`, event `boss_hp_zero`, trigger None, persistent flag `boss_pharaoh_defeated`: Stop attacks and disable all damage immediately; disintegration, slow whiteout, remove boss/summons/projectiles/hazards during white, fade back, reopen entrance and east route, commit defeated flag and pending reward together. No Grail reward.
- Boss state table, teleport/summon cells, caps, safe-strip rules and pending reward semantics: see this room's `boss` in gameplay_specs.json and chapter handoff. The east boundary is physically sealed before victory, not just a disabled portal.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d17_pharaohs_courtyard:deco1`: `spr_pharaoh_statue` at [10, 15], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Statues sit on blocked masonry beneath the fight floor, never inside dodge lanes.
- `rm_d17_pharaohs_courtyard:deco2`: `spr_pharaoh_statue` at [28, 15], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Paired sentinels make this space read as a courtyard rather than another desert room.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`mus_ending`, `mus_pharaoh`, `snd_bat_screech`, `snd_boss_death`, `snd_boss_hurt`, `snd_boss_summon`, `snd_disintegrate`, `snd_gate_slam`, `snd_laser_charge`, `snd_laser_fire`, `snd_thunder_strike`, `snd_thunder_warn`, `snd_undead_rise`, `spr_bat_defeat`, `spr_bat_dive`, `spr_bat_fly`, `spr_door_sealed`, `spr_fx_laser_charge`, `spr_fx_sand_burst`, `spr_fx_thunder_impact`, `spr_gate_arena`, `spr_icon_pharaoh_ankh`, `spr_laser_aim`, `spr_laser_beam`, `spr_lightning_bolt`, `spr_mask_bat`, `spr_mask_medium`, `spr_mask_pharaoh`, `spr_pharaoh_death`, `spr_pharaoh_hurt`, `spr_pharaoh_idle`, `spr_pharaoh_laser_charge`, `spr_pharaoh_laser_fire`, `spr_pharaoh_statue`, `spr_pharaoh_summon`, `spr_pharaoh_teleport_in`, `spr_pharaoh_teleport_out`, `spr_pharaoh_thunder_cast`, `spr_portrait_dave`, `spr_portrait_pharaoh`, `spr_summon_crack`, `spr_thunder_exclaim`, `spr_thunder_marker`, `spr_undead_attack_down`, `spr_undead_attack_side`, `spr_undead_attack_up`, `spr_undead_defeat`, `spr_undead_hurt_down`, `spr_undead_idle_down`, `spr_undead_rise`, `spr_undead_walk_down`, `spr_undead_walk_side`, `spr_undead_walk_up`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d17_pharaohs_courtyard.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Dungeon Threshold

Stable ID: `rm_d18_dungeon_threshold`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: A quiet victory walk reaches the dungeon mouth and ends Chapter I without entering an interior. Intensity: **quiet**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #.......................MMMMMMMMMMM#
02  #.......................MMMMMMMMMMM#
03  #.......................MMMMMM__MMM#
04  #.............................tt...#
05  #............................___...#
06  #............................___...#
07  ____________________.........___...#
08  ____________________.........___...#
09  ____________________.........___...#
10  #................___.........___...#
11  #................_______________...#
12  #................_______________...#
13  #................_______________...#
14  #..................................#
15  #..................................#
16  #..................................#
17  #..................................#
18  #..................................#
19  #..................................#
20  #..................................#
21  #..................................#
22  #..................................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [7, 9] | [2, 8]; 0 | `rm_d17_pharaohs_courtyard` / east | [37, 8] | boss_pharaoh_defeated |

Authored main walking line: [2, 8] -> [18, 8] -> [18, 12] -> [30, 12] -> [30, 4]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- A three-cell paved approach leads to an internal two-cell art doorway; the contract's three-cell rule still holds for every border exit.
- No enemies, chests, water, stairs, bridges, moving hazards or Grail. West backtracking is allowed before entering the threshold.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- None; preserve the quiet room.

Treasure:

- No chests.

Checkpoint / script data:

- `dungeon_threshold`, event `chapter_ending`, trigger [30, 4, 31, 4], persistent flag `chapter_desert_complete`: Require boss_pharaoh_defeated; stop movement/damage, transition to rm_ending showing exactly To Be Continued. No dungeon interior. On a loaded completed save, re-entering this trigger may show the ending again; never trap the player behind a once-only empty trigger.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d18_dungeon_threshold:deco1`: `spr_dungeon_entrance` at [30, 4], pixel offset [32, 0], layer `Instances` (sort_by_ground_point_no_collision). Dungeon facade drawn so its existing 128-pixel doorway is aligned with x30..31; art origin needs an integration offset, never infer collision from alpha.
- `rm_d18_dungeon_threshold:deco2`: `spr_ruin_block` at [26, 2], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Sparse dressing; keep readable floor and telegraphs.
- `rm_d18_dungeon_threshold:deco3`: `spr_bush_dead` at [9, 18], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`mus_ending`, `spr_bush_dead`, `spr_dungeon_entrance`, `spr_ending_bg`, `spr_ruin_block`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d18_dungeon_threshold.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Memorial Vault

Stable ID: `rm_o6_memorial_vault`. Dimensions: **32 x 22 tiles** (2048 x 1408 px). Purpose: A final optional terrace duel leads to premium armor, then a quiet return to the star. Intensity: **medium**.

```text
    0         1         2         3 
    01234567890123456789012345678901
00  ################################
01  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
02  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
03  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
04  #..__________________________..#
05  #..______________________c___..#
06  #..__________________________..#
07  #..__________________________..#
08  #..__________________________..#
09  #..__________________________..#
10  #MMMMMMMMMMMMM^^^^^MMMMMMMMMMMM#
11  #MMMMMMMMMMMMM^^^^^MMMMMMMMMMMM#
12  #..............___.............#
13  #..............___.............#
14  #..............___.............#
15  #.........________.............#
16  #......e..________.............#
17  #.........________.............#
18  #.........___..................#
19  #.........___..................#
20  #.........___..................#
21  ##########___###################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| south | S cols [10, 12] | [11, 19]; 2 | `rm_d15_tomb_approach` / north | [11, 2] | always |

Authored main walking line: [11, 19] -> [11, 16] -> [16, 16] -> [16, 8] -> [25, 8] -> [25, 7]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Only ^ cells cross the masonry band. No one-way drop, water, bridge, locked chest or shortcut past the boss.
- stairs [14, 10, 18, 11]: Five-cell-wide memorial stair, z0 south to z1 north, clear two-cell landings.
- Visual level 0, lower rectangle [1, 12, 30, 20]; only authored connectors cross a solid level boundary.
- Visual level 1, memorial rectangle [1, 4, 30, 9]; only authored connectors cross a solid level boundary.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_o6_memorial_vault:g1`: pad/leash [3, 13, 9, 19]; max 1 active. One optional guardian on a broad lower terrace; no enemy occupies the stair or reward landing. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_o6_memorial_vault:g1:e1`: `skeleton_warrior` at [7, 16].

Treasure:

- `rm_o6_memorial_vault:c1` at [25, 5]: 1 x `paladin_mail`, 1 x `potion_greater`. Premium optional armor, earned by taking the memorial detour; never a key or required boss defense tier. Approach [25, 7]; interact from [25, 6]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_o6_memorial_vault:deco1`: `spr_obelisk` at [7, 2], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Memorial stones echo the city's lost comrades without claiming the Grail is recovered.
- `rm_o6_memorial_vault:deco2`: `spr_pharaoh_statue` at [27, 2], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Sparse dressing; keep readable floor and telegraphs.
- `rm_o6_memorial_vault:deco3`: `spr_pebbles` at [25, 18], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `spr_chest_desert`, `spr_icon_paladin_mail`, `spr_icon_potion_greater`, `spr_mask_medium`, `spr_obelisk`, `spr_pebbles`, `spr_pharaoh_statue`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `ts_stairs`.

Implementation sources: `design/desert/rooms/rm_o6_memorial_vault.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.
