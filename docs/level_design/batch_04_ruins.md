> SUPERSEDED: reference only. Use [the expanding scene design](DESERT_CHAPTER.md). These are no longer separate loaded areas.

# Desert design - batch 04

[Chapter graph, conventions and import rules](DESERT_CHAPTER.md). Grid = 64 px tiles, zero-based [x,y]. Rectangles and spans inclusive. Terrain JSON is authoritative; diagram letters overlay objects. Legend: . sand, , path, ; grass, ~ blocked water, # blocked cliff, M blocked masonry, _ paving, ^ stairs, C blocked chasm, = E/W bridge, | N/S bridge, x blocked broken span; e enemy, c chest, S star, p solid prop, t trigger, i initial spawn, g gate. Decorative placement has no collision and is listed separately.

## Broken Bridge

Stable ID: `rm_d10_broken_bridge`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: Pause combat pressure: read a broken upper span, then use an intact lower bridge. Intensity: **low**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ##########___#######################
01  #.........___...CCCCC..............#
02  #.........___...CCCCC..............#
03  #.........___...CCCCC..............#
04  #.........___MM.CCCCC..............#
05  #.........,,MMM.xxxxx..............#
06  #.........,,MMM.xxxxx..............#
07  #.........,,,...xxxxx..............#
08  #.........,,,...CCCCC..............#
09  #.........,,,...CCCCC..............#
10  _____,,,,,,,,,..CCCCC...,,,,,,,_____
11  _____,,,,,,,,,..CCCCC...,,,,,,,_____
12  _____,,,,,,,,,..CCCCC...,,,,,,,_____
13  #..........,,,..CCCCC...,,,........#
14  #..........,,,,,=====,,,,,,........#
15  #..........,,,,,=====,,,,,,........#
16  #..........,,,,,=====,,,,,,........#
17  #...............CCCCC..............#
18  #...............CCCCC.......e......#
19  #...............CCCCC...........c..#
20  #...............CCCCC..............#
21  #...............CCCCC..............#
22  #...............CCCCC..............#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d09_bonefield` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d11_forgotten_ruins` / west | [2, 11] | always |
| north | N cols [10, 12] | [11, 2]; 6 | `rm_o4_buried_cistern` / south | [11, 19] | always |

Authored main walking line: [2, 11] -> [12, 11] -> [12, 15] -> [23, 15] -> [25, 15] -> [25, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Chasm and x cells are full blockers; intact = cells replace chasm collision. Add deck-edge rails only along y13/y17, never across landings.
- North exit before the chasm leads to O4. No forced combat, dynamic bridge collapse, water or stairs.
- broken_bridge [16, 5, 20, 7]: All x cells are blocked; broken ropes visually expose the missing centre. Never a jump or repair objective.
- bridge_ew [16, 14, 20, 16]: Intact three-row deck, five cells long, both landings clear at x13..15 and x21..23.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d10_broken_bridge:g1`: pad/leash [25, 15, 31, 21]; max 1 active. One optional bat after crossing; no attacks or aggro on the bridge itself. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d10_broken_bridge:g1:e1`: `bat` at [28, 18].

Treasure:

- `rm_d10_broken_bridge:c1` at [32, 19]: 1 x `potion_greater`. A safe eastern-bank pocket for players who explore after the crossing. Approach [32, 21]; interact from [32, 20]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d10_broken_bridge:deco1`: `spr_ruin_block` at [13, 5], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Broken-span abutment, set away from the intact route.
- `rm_d10_broken_bridge:deco2`: `spr_tree_dead` at [30, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Far-bank tree is visible across the chasm and anchors orientation.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_bat_screech`, `snd_chest_open`, `snd_wind_loop`, `spr_bat_defeat`, `spr_bat_dive`, `spr_bat_fly`, `spr_chest_desert`, `spr_icon_potion_greater`, `spr_mask_bat`, `spr_ruin_block`, `spr_tree_dead`, `spr_tumbleweed`, `tex_chasm_void`, `tex_chasm_wall`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `ts_bridge`.

Implementation sources: `design/desert/rooms/rm_d10_broken_bridge.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Forgotten Ruins

Stable ID: `rm_d11_forgotten_ruins`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: A silent ruined courtyard restores safety and establishes the second checkpoint. Intensity: **quiet**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
02  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
03  #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
04  #..............MM..................#
05  #..............MM..................#
06  #..............MM..................#
07  #..............MM..................#
08  #..............MM..................#
09  #..............MM......______......#
10  ____________________________________
11  _________________________S__________
12  ____________________________________
13  #..............MM......______......#
14  #..............MM..................#
15  #..............MM..................#
16  #..............MM..................#
17  #..............MM..................#
18  #..............MM...........c......#
19  #..............MM..................#
20  #..................................#
21  #..................................#
22  #..................................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d10_broken_bridge` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d12_great_desert_stairs` / west | [2, 11] | always |

Authored main walking line: [2, 11] -> [25, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Masonry divide has a permanent three-cell opening at y10..12. No puzzle or locked door.
- No enemies, water, stairs, bridge or active hazard. Wind and tumbleweeds are suppressed.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- None; preserve the quiet room.

Treasure:

- `rm_d11_forgotten_ruins:c1` at [28, 18]: 2 x `potion_health`. A safe stock-up before the stairs; tucked behind a broken wall end, never hidden by opaque art. Approach [28, 20]; interact from [28, 19]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- `rm_d11_forgotten_ruins:checkpoint` at [25, 11]; respawn [25, 11]; clear pad [24, 10, 26, 12]. E interaction; three save slots; heal on successful save; no automatic overwrite.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d11_forgotten_ruins:deco1`: `spr_obelisk` at [9, 2], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Two intact inscriptions contrast with the broken city rubble from Arrival.
- `rm_d11_forgotten_ruins:deco2`: `spr_ruin_block` at [16, 7], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Sparse dressing; keep readable floor and telegraphs.
- `rm_d11_forgotten_ruins:deco3`: `spr_bush_dead` at [6, 19], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_checkpoint`, `snd_chest_open`, `snd_save`, `spr_bush_dead`, `spr_checkpoint_star`, `spr_chest_desert`, `spr_fx_sparkle`, `spr_icon_potion_health`, `spr_obelisk`, `spr_ruin_block`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d11_forgotten_ruins.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Great Desert Stairs

Stable ID: `rm_d12_great_desert_stairs`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: A wide mandatory ascent changes viewpoint and rewards looking back along the upper shelf. Intensity: **medium**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #..................................#
02  #..................................#
03  #..................................#
04  #.....c...........,,,,,,,,,,,,,_____
05  #.................,,,,,,,,,,e,,_____
06  #.................,,,,,,,,,,,,,_____
07  #.................,,,..............#
08  #.................,,,..............#
09  #################^^^^^##############
10  _____,,,,########^^^^^##############
11  _____,,,,.........,,,..............#
12  _____,,,,.........,,,..............#
13  #.....,,,.........,,,..............#
14  #.....,,,,,,,,,,,,,,,..............#
15  #.....,,,,,e,,,,,,,,,..............#
16  #.....,,,,,,,,,,,,,,,..............#
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
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d11_forgotten_ruins` / east | [33, 11] | always |
| east | E rows [4, 6] | [33, 5]; 4 | `rm_d13_windblown_plateau` / west | [2, 5] | always |

Authored main walking line: [2, 11] -> [7, 11] -> [7, 15] -> [19, 15] -> [19, 5] -> [33, 5]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- North and south terraces connect only through ^ cells. No jumping, one-way drops, water or bridge. East opening is y4..6.
- stairs [17, 9, 21, 10]: Five wide and two deep; z0 south to z1 north. Landings x17..21 y7..8 and y11..12 are reserved clear.
- Visual level 0, lower rectangle [1, 11, 34, 22]; only authored connectors cross a solid level boundary.
- Visual level 1, upper rectangle [1, 1, 34, 8]; only authored connectors cross a solid level boundary.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d12_great_desert_stairs:g1`: pad/leash [8, 12, 14, 18]; max 1 active. One lower-terrace duel; it cannot chase onto the stairs. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d12_great_desert_stairs:g1:e1`: `skeleton_warrior` at [11, 15].
- `rm_d12_great_desert_stairs:g2`: pad/leash [24, 2, 30, 8]; max 1 active. An upper-terrace archer approached after a wide, clear landing; no firing through the cliff face. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d12_great_desert_stairs:g2:e1`: `skeleton_archer` at [28, 5].

Treasure:

- `rm_d12_great_desert_stairs:c1` at [6, 4]: 2 x `ancient_coin`. After ascending, the east exit is clear; looking west along the upper shelf finds a worthwhile detour. Approach [6, 6]; interact from [6, 5]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d12_great_desert_stairs:deco1`: `spr_pharaoh_statue` at [32, 10], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Statue on the cliff face announces the royal plateau.
- `rm_d12_great_desert_stairs:deco2`: `spr_pebbles` at [4, 19], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_arrow_hit`, `snd_bow_release`, `snd_chest_open`, `snd_wind_loop`, `spr_arrow`, `spr_chest_desert`, `spr_fx_arrow_hit`, `spr_icon_ancient_coin`, `spr_mask_medium`, `spr_pebbles`, `spr_pharaoh_statue`, `spr_skeleton_archer_attack_down`, `spr_skeleton_archer_attack_side`, `spr_skeleton_archer_attack_up`, `spr_skeleton_archer_defeat`, `spr_skeleton_archer_hurt_down`, `spr_skeleton_archer_idle_down`, `spr_skeleton_archer_walk_down`, `spr_skeleton_archer_walk_side`, `spr_skeleton_archer_walk_up`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `spr_tumbleweed`, `tex_paving`, `ts_stairs`.

Implementation sources: `design/desert/rooms/rm_d12_great_desert_stairs.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Buried Cistern

Stable ID: `rm_o4_buried_cistern`. Dimensions: **32 x 22 tiles** (2048 x 1408 px). Purpose: A cool, enemy-free cistern loop rewards the bridge-side detour. Intensity: **quiet**.

```text
    0         1         2         3 
    01234567890123456789012345678901
00  ################################
01  #..............................#
02  #..MMMMMMMMMMMMMMMMMMMMMMMMMM..#
03  #..MMMMMMMMMMMMMMMMMMMMMMMMMM..#
04  #..__________________________..#
05  #..______________________c___..#
06  #..______~~~~~~|||~~~~~______..#
07  #..______~~~~~~|||~~~~~______..#
08  #..______~~~~~~|||~~~~~______..#
09  #..______~~~~~~|||~~~~~______..#
10  #..______~~~~~~|||~~~~~______..#
11  #..______~~~~~~|||~~~~~______..#
12  #..______~~~~~~|||~~~~~______..#
13  #..__________________________..#
14  #..__________________________..#
15  #..__________________________..#
16  #..__________________________..#
17  #..__________________________..#
18  #.........___..................#
19  #.........___..................#
20  #.........___..................#
21  ##########___###################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| south | S cols [10, 12] | [11, 19]; 2 | `rm_d10_broken_bridge` / north | [11, 2] | always |

Authored main walking line: [11, 19] -> [11, 15] -> [16, 15] -> [16, 5] -> [25, 7]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Water is impassable. The catwalk and outer paved rim form a permanent loop; neither requires a switch. No combat, stairs or drops.
- bridge_ns [15, 6, 17, 12]: Three-column stone-supported wooden catwalk; replaces water collision. Both landings x15..17 y4..5 and y13..14 stay empty.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- None; preserve the quiet room.

Treasure:

- `rm_o4_buried_cistern:c1` at [25, 5]: 1 x `golden_scarab`, 1 x `potion_greater`. A valuable plus recovery reached by either the outer rim or the central catwalk. Approach [25, 7]; interact from [25, 6]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_o4_buried_cistern:deco1`: `spr_obelisk` at [5, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Water-measure carving on blocked masonry.
- `rm_o4_buried_cistern:deco2`: `spr_bush` at [6, 15], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `spr_bush`, `spr_chest_desert`, `spr_icon_golden_scarab`, `spr_icon_potion_greater`, `spr_obelisk`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `tex_water`, `tex_wet_sand`, `ts_bridge`.

Implementation sources: `design/desert/rooms/rm_o4_buried_cistern.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.
