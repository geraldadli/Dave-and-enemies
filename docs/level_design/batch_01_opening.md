> SUPERSEDED: reference only. Use [the expanding scene design](DESERT_CHAPTER.md). These are no longer separate loaded areas.

# Desert design - batch 01

[Chapter graph, conventions and import rules](DESERT_CHAPTER.md). Grid = 64 px tiles, zero-based [x,y]. Rectangles and spans inclusive. Terrain JSON is authoritative; diagram letters overlay objects. Legend: . sand, , path, ; grass, ~ blocked water, # blocked cliff, M blocked masonry, _ paving, ^ stairs, C blocked chasm, = E/W bridge, | N/S bridge, x blocked broken span; e enemy, c chest, S star, p solid prop, t trigger, i initial spawn, g gate. Decorative placement has no collision and is listed separately.

## Desert Arrival

Stable ID: `rm_d01_arrival`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: Orient east after the vow; teach path and chest interaction without combat. Intensity: **quiet**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  ########...................#########
02  ########...................#########
03  ########...................#########
04  ########...................#########
05  ########...........................#
06  #............._____................#
07  #.............__c__................#
08  #.........,,,,_____,,,,,...........#
09  #.tttttt..,,,,_____,,,,,...........#
10  #,tttttt,,,,,,,,,,,,,,,,,,,,,,,_____
11  #,titttt,,,,,........,,,,,,,,,,_____
12  #,tttttt,,,,,........,,,,,,,,,,_____
13  #.tttttt...........................#
14  #..................................#
15  #..................................#
16  #..................................#
17  #..................................#
18  ##########...................p.....#
19  ##########.........................#
20  ##########.........................#
21  ##########.........................#
22  ##########.........................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d02_dune_trail` / west | [2, 11] | always |

Intro / initial restart arrives at [3, 11], facing E, reserved rectangle [2, 10, 4, 12]. No west border exit.

Authored main walking line: [3, 11] -> [11, 11] -> [11, 9] -> [22, 9] -> [22, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Northwest rubble and southern cliff shape a broad funnel; all interior sand is walkable.
- No water, stairs, bridge, chasm or live hazard. First-death fallback is the initial snapshot at [3,11].

Solid props (separate from art-only decoration):

- `cactus_small` at [29, 18], centred base footprint [16, 12] px; conservative blocked cells rectangle [29, 18, 29, 18].

Encounters:

- None; preserve the quiet room.

Treasure:

- `rm_d01_arrival:c1` at [16, 7]: 1 x `potion_health`. A visible, unguarded first potion; learn interaction before danger. Approach [16, 9]; interact from [16, 8]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- `desert_arrival`, event `chapter_start`, trigger [2, 9, 7, 13], persistent flag `desert_arrival_seen`: Intro hands control to Dave facing E at [3,11]. Use narrative-owned text; do not add new dialogue IDs to runtime here.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d01_arrival:deco1`: `spr_ruin_block` at [5, 4], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Breached-city rubble on blocked cliff; west is the past.
- `rm_d01_arrival:deco2`: `spr_tree_dead` at [29, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Bare silhouette on blocked ground points toward the east gap.
- `rm_d01_arrival:deco3`: `spr_pebbles` at [22, 16], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_d01_arrival:deco4`: `spr_bush_dead` at [8, 16], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_wind_loop`, `spr_bush_dead`, `spr_cactus_small`, `spr_chest_desert`, `spr_icon_potion_health`, `spr_pebbles`, `spr_ruin_block`, `spr_tree_dead`, `spr_tumbleweed`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d01_arrival.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Dune Trail

Stable ID: `rm_d02_dune_trail`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: One slow attacker in an open bowl, then a visible side chest on a loop. Intensity: **low**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #..................................#
02  #..................................#
03  #.........####.....................#
04  #.........####.....................#
05  #.........####...........,,,,c,,...#
06  #.........####...........,,,,,,,...#
07  #.........####...........,,,,,,,...#
08  #........................,,,.......#
09  #........................,,,.......#
10  _____,,,,,,,,,,,,,,,,,,,,,,,,,,_____
11  _____,,,,,,,,,,,,,,,e,,,,,,,,,,_____
12  _____,,,,,,,,,,,,,,,,,,,,,,,,,,_____
13  #..................................#
14  #..................................#
15  #..................................#
16  #..................................#
17  #.....########..............########
18  #.....########..............########
19  #.....########..............########
20  #.....########..............########
21  #.....########..............########
22  #...........................########
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d01_arrival` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d03_canyon_approach` / west | [2, 11] | always |

Authored main walking line: [2, 11] -> [20, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Cliff islands only block their # cells. The treasure loop has three-cell lanes.
- No water, elevation transition, bridges or encounter lock.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d02_dune_trail:g1`: pad/leash [16, 7, 24, 15]; max 1 active. Learn windup, sidestep and one swing of recovery. Entire 9 by 9 bowl is clear. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d02_dune_trail:g1:e1`: `undead` at [20, 11].

Treasure:

- `rm_d02_dune_trail:c1` at [29, 5]: 2 x `potion_health`. Supplies after first combat; visible from the eastward path, reached around the dune. Approach [29, 7]; interact from [29, 6]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d02_dune_trail:deco1`: `spr_cactus_tall` at [11, 5], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). A forked cactus on solid dune top marks the chest loop.
- `rm_d02_dune_trail:deco2`: `spr_pebbles` at [6, 5], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_d02_dune_trail:deco3`: `spr_bush_dead` at [30, 20], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_wind_loop`, `spr_bush_dead`, `spr_cactus_tall`, `spr_chest_desert`, `spr_icon_potion_health`, `spr_mask_medium`, `spr_pebbles`, `spr_tumbleweed`, `spr_undead_attack_down`, `spr_undead_attack_side`, `spr_undead_attack_up`, `spr_undead_defeat`, `spr_undead_hurt_down`, `spr_undead_idle_down`, `spr_undead_rise`, `spr_undead_walk_down`, `spr_undead_walk_side`, `spr_undead_walk_up`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d02_dune_trail.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Canyon Approach

Stable ID: `rm_d03_canyon_approach`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: Reveal a north detour at a canyon marker; two separated fights on the east route. Intensity: **medium**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ##########___#######################
01  #######...___..#######.............#
02  #######...___..#######.............#
03  #######...___..#######.............#
04  #######...___..#######.............#
05  #######.p.,,,......................#
06  #######...,,,......................#
07  #.........,,,....,,,,,,,,,,,.......#
08  #.........,,,....,e,,,,,,,,,.......#
09  #.........,,,....,,,,,,,,,,,.......#
10  _____,,,,,,,,,,,,,,,.....,e,,,,_____
11  _____,,,,,,,,,,,,,,,.....,,,,,,_____
12  _____,,,,,,,,,,,,,,,.....,,,,,,_____
13  #..................................#
14  #..................................#
15  #..................................#
16  #..................................#
17  #############................#######
18  #############..............c.#######
19  #############................#######
20  #############................#######
21  #############................#######
22  #############................#######
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d02_dune_trail` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d04_split_cliffs` / west | [2, 11] | always |
| north | N cols [10, 12] | [11, 2]; 6 | `rm_o1_sunken_lookout` / south | [11, 19] | always |

Authored main walking line: [2, 11] -> [11, 11] -> [18, 11] -> [18, 8] -> [26, 8] -> [26, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- North opening is optional O1; the main exit remains east. Obelisk has a base-only blocker at [8,5].
- No water, bridge or stairs here; the first optional climb happens in O1.

Solid props (separate from art-only decoration):

- `obelisk` at [8, 5], centred base footprint [40, 28] px; conservative blocked cells rectangle [8, 5, 8, 5].

Encounters:

- `rm_d03_canyon_approach:g1`: pad/leash [15, 5, 21, 11]; max 1 active. An isolated familiar enemy keeps the optional turn legible. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d03_canyon_approach:g1:e1`: `undead` at [18, 8].
- `rm_d03_canyon_approach:g2`: pad/leash [23, 7, 29, 13]; max 1 active. Second windup practice after a short walk; groups activate separately. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d03_canyon_approach:g2:e1`: `undead` at [26, 10].

Treasure:

- `rm_d03_canyon_approach:c1` at [27, 18]: 20 x `gold_coins`. A small southern pocket pays for looking away from the dark path. Approach [27, 20]; interact from [27, 19]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d03_canyon_approach:deco1`: `spr_skull` at [24, 20], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_d03_canyon_approach:deco2`: `spr_ruin_block` at [5, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Two incised blocks repeat the notch motif seen in the optional room.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_wind_loop`, `spr_chest_desert`, `spr_icon_gold_coins`, `spr_mask_medium`, `spr_obelisk`, `spr_ruin_block`, `spr_skull`, `spr_tumbleweed`, `spr_undead_attack_down`, `spr_undead_attack_side`, `spr_undead_attack_up`, `spr_undead_defeat`, `spr_undead_hurt_down`, `spr_undead_idle_down`, `spr_undead_rise`, `spr_undead_walk_down`, `spr_undead_walk_side`, `spr_undead_walk_up`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d03_canyon_approach.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Sunken Lookout

Stable ID: `rm_o1_sunken_lookout`. Dimensions: **32 x 22 tiles** (2048 x 1408 px). Purpose: Preview a high chest, turn west to climb, then cross the shelf for the first optional armor. Intensity: **low**.

```text
    0         1         2         3 
    01234567890123456789012345678901
00  ################################
01  ################################
02  ###..........................###
03  ###..........................###
04  ###...,,,,,,,,,,,,,..........###
05  ###...,,,,,,,,e,,,,..........###
06  ###...,,,,,,,,,,,,,..........###
07  ###...,,,.......,,,..........###
08  ###...,,,.......,,,..........###
09  ###...,,,........c...........###
10  ###...,,,....................###
11  ######^^^#######################
12  ######^^^#######################
13  #.....,,,......................#
14  #.....,,,,,,,..................#
15  #.....,,,,,,,..................#
16  #.....,,,,,,,...............####
17  #.........___...............####
18  #.........___...............####
19  #.........___..................#
20  #.........___..................#
21  ##########___###################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| south | S cols [10, 12] | [11, 19]; 2 | `rm_d03_canyon_approach` / north | [11, 2] | always |

Authored main walking line: [11, 19] -> [11, 13] -> [11, 15] -> [7, 15] -> [7, 10] -> [7, 5] -> [17, 5] -> [17, 7]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Only stairs connect basin to shelf; # faces are solid and do not support walking on their art.
- No water, bridges, jumping, secret wall, key or return lock. Return uses the same stairs and south exit.
- stairs [6, 11, 8, 12]: Three wide, two deep, bidirectional climb from lower basin z0 to shelf z1; no drop edges.
- Visual level 0, basin rectangle [1, 13, 30, 20]; only authored connectors cross a solid level boundary.
- Visual level 1, shelf rectangle [3, 2, 28, 10]; only authored connectors cross a solid level boundary.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_o1_sunken_lookout:g1`: pad/leash [11, 2, 17, 8]; max 1 active. Optional shelf duel; a clear south edge allows repositioning and retreat to stairs. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_o1_sunken_lookout:g1:e1`: `undead` at [14, 5].

Treasure:

- `rm_o1_sunken_lookout:c1` at [17, 9]: 1 x `wanderer_tunic`, 1 x `potion_health`. First optional armor and a potion. From the lower basin near [11,13], the chest is six cells east and four north, within the 1280 by 720 view; the west stairs provide access. Interact from its north side. Approach [17, 7]; interact from [17, 8]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_o1_sunken_lookout:deco1`: `spr_obelisk` at [27, 11], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Half-buried lookout marker on the cliff band; never blocks the stair landing.
- `rm_o1_sunken_lookout:deco2`: `spr_tree_dead` at [29, 17], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Silhouette on the far basin rim.
- `rm_o1_sunken_lookout:deco3`: `spr_pebbles` at [17, 17], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_wind_loop`, `spr_chest_desert`, `spr_icon_potion_health`, `spr_icon_wanderer_tunic`, `spr_mask_medium`, `spr_obelisk`, `spr_pebbles`, `spr_tree_dead`, `spr_tumbleweed`, `spr_undead_attack_down`, `spr_undead_attack_side`, `spr_undead_attack_up`, `spr_undead_defeat`, `spr_undead_hurt_down`, `spr_undead_idle_down`, `spr_undead_rise`, `spr_undead_walk_down`, `spr_undead_walk_side`, `spr_undead_walk_up`, `tex_paving`, `ts_stairs`.

Implementation sources: `design/desert/rooms/rm_o1_sunken_lookout.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.
