> SUPERSEDED: reference only. Use [the expanding scene design](DESERT_CHAPTER.md). These are no longer separate loaded areas.

# Desert design - batch 05

[Chapter graph, conventions and import rules](DESERT_CHAPTER.md). Grid = 64 px tiles, zero-based [x,y]. Rectangles and spans inclusive. Terrain JSON is authoritative; diagram letters overlay objects. Legend: . sand, , path, ; grass, ~ blocked water, # blocked cliff, M blocked masonry, _ paving, ^ stairs, C blocked chasm, = E/W bridge, | N/S bridge, x blocked broken span; e enemy, c chest, S star, p solid prop, t trigger, i initial spawn, g gate. Decorative placement has no collision and is listed separately.

## Windblown Plateau

Stable ID: `rm_d13_windblown_plateau`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: A wide horizon and quiet upper route reveal an elective sandworm basin and a grotto detour. Intensity: **low**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ##########___#######################
01  #.........___......................#
02  #.........___......................#
03  #.........___...####...............#
04  _____,,,,,___,,,,,,,,,,,...........#
05  _____,,,,,,,,,,,,,,,,,,,...........#
06  _____,,,,,,,,,,,,,,,,,,,...........#
07  #...............####.,,,...........#
08  #....................,,,...........#
09  #....................,,,...........#
10  #....................,,,,,,,,,,_____
11  #....................,,,,,,,,,,_____
12  #....................,,,,,,,,,,_____
13  #..########........................#
14  #..########........................#
15  #..########........................#
16  #..########........................#
17  #..########................e.......#
18  #..########........................#
19  #..########.....................c..#
20  #..................................#
21  #..................................#
22  #..................................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [4, 6] | [2, 5]; 0 | `rm_d12_great_desert_stairs` / east | [33, 5] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d14_royal_causeway` / west | [2, 11] | always |
| north | N cols [10, 12] | [11, 2]; 6 | `rm_o5_echo_grotto` / south | [11, 19] | always |

Authored main walking line: [2, 5] -> [11, 5] -> [22, 5] -> [22, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- No forced storm hazard or current. All sand is ordinary speed. No bridge, water, stairs or drop.
- Sandworm emergence is confined to its authored combat pad; never retarget under arrival reserves or chest interaction cells. North exit leads to O5.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d13_windblown_plateau:g1`: pad/leash [23, 14, 31, 20]; max 1 active. Optional first emergence with a wide lateral escape pad; disturbed sand warns before activation. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d13_windblown_plateau:g1:e1`: `sandworm` at [27, 17].

Treasure:

- `rm_d13_windblown_plateau:c1` at [32, 19]: 1 x `desert_rose`, 1 x `potion_greater`. A visible reward beyond the elective basin; no worm kill flag gates it. Approach [32, 21]; interact from [32, 20]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d13_windblown_plateau:deco1`: `spr_tree_dead` at [7, 17], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Wind-scoured tree on a blocked island points west with its branches.
- `rm_d13_windblown_plateau:deco2`: `spr_rock_small` at [18, 5], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Sparse dressing; keep readable floor and telegraphs.
- `rm_d13_windblown_plateau:deco3`: `spr_pebbles` at [28, 3], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_wind_loop`, `snd_worm_bite`, `snd_worm_emerge`, `snd_worm_rumble`, `spr_chest_desert`, `spr_icon_desert_rose`, `spr_icon_potion_greater`, `spr_mask_sandworm`, `spr_pebbles`, `spr_rock_small`, `spr_sandworm_attack`, `spr_sandworm_burrow`, `spr_sandworm_defeat`, `spr_sandworm_emerge`, `spr_sandworm_hurt`, `spr_sandworm_idle_up`, `spr_sandworm_mound`, `spr_tree_dead`, `spr_tumbleweed`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d13_windblown_plateau.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Royal Causeway

Stable ID: `rm_d14_royal_causeway`. Dimensions: **40 x 24 tiles** (2560 x 1536 px). Purpose: One melee guard, an empty crossing, then a caster-and-bandit combination on a broad landing. Intensity: **high**.

```text
    0         1         2         3         
    0123456789012345678901234567890123456789
00  ########################################
01  #................CCCCC.................#
02  #................CCCCC.................#
03  #.............MMMCCCCCMMM..............#
04  #.............MMMCCCCCMMM..............#
05  #.............MMMCCCCCMMM..............#
06  #................CCCCC.................#
07  #................CCCCC.................#
08  #................CCCCC.................#
09  #................=====.......e.........#
10  _________________=====__________________
11  __________e______=====__________________
12  _________________=====__________________
13  #................CCCCC.................#
14  #................CCCCC........e........#
15  #................CCCCC.................#
16  #................CCCCC.................#
17  #................CCCCC.................#
18  #................CCCCC.................#
19  #................CCCCC.......c.........#
20  #................CCCCC.................#
21  #................CCCCC.................#
22  #................CCCCC.................#
23  ########################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d13_windblown_plateau` / east | [33, 11] | always |
| east | E rows [10, 12] | [37, 11]; 4 | `rm_d15_tomb_approach` / west | [2, 11] | always |

Authored main walking line: [2, 11] -> [15, 11] -> [23, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- C is blocked; = deck is walkable. Rails remain outside deck and landings. No combat on the bridge, water, stairs or scripted gate.
- bridge_ew [17, 9, 21, 12]: Four-row deck, five long. West landing x14..16 and east landing x22..24 have no combat, props or projectiles.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d14_royal_causeway:g1`: pad/leash [5, 7, 13, 15]; max 1 active. A known melee guard before the bridge; it cannot pursue onto the deck. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d14_royal_causeway:g1:e1`: `skeleton_warrior` at [10, 11].
- `rm_d14_royal_causeway:g2`: pad/leash [25, 7, 33, 15]; max 2 active. First required-route caster mix, isolated from the crossing so the player can enter a nine-cell-square landing. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d14_royal_causeway:g2:e1`: `bandit_caster` at [29, 9].
  - `rm_d14_royal_causeway:g2:e2`: `bandit` at [30, 14].

Treasure:

- `rm_d14_royal_causeway:c1` at [29, 19]: 2 x `potion_greater`. Restock after the last dense required-route group. Approach [29, 21]; interact from [29, 20]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d14_royal_causeway:deco1`: `spr_pharaoh_statue` at [15, 4], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Royal marker on a blocked pedestal.
- `rm_d14_royal_causeway:deco2`: `spr_pharaoh_statue` at [23, 4], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Matching far-bank statue frames the causeway.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_cast_charge`, `snd_chest_open`, `snd_magic_hit`, `snd_magic_travel`, `snd_wind_loop`, `spr_bandit_attack_down`, `spr_bandit_attack_side`, `spr_bandit_attack_up`, `spr_bandit_caster_attack_down`, `spr_bandit_caster_attack_side`, `spr_bandit_caster_attack_up`, `spr_bandit_caster_defeat`, `spr_bandit_caster_hurt_down`, `spr_bandit_caster_idle_down`, `spr_bandit_caster_walk_down`, `spr_bandit_caster_walk_side`, `spr_bandit_caster_walk_up`, `spr_bandit_defeat`, `spr_bandit_hurt_down`, `spr_bandit_idle_down`, `spr_bandit_walk_down`, `spr_bandit_walk_side`, `spr_bandit_walk_up`, `spr_chest_desert`, `spr_fx_magic_hit`, `spr_fx_magic_launch`, `spr_icon_potion_greater`, `spr_magic_orb`, `spr_mask_medium`, `spr_pharaoh_statue`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `spr_tumbleweed`, `tex_chasm_void`, `tex_chasm_wall`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `ts_bridge`.

Implementation sources: `design/desert/rooms/rm_d14_royal_causeway.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Tomb Approach

Stable ID: `rm_d15_tomb_approach`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: A quiet ceremonial approach foreshadows the boss and offers the final optional equipment branch. Intensity: **quiet**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ##########___#######################
01  #MMMMMM...___....MMMMMMMM..........#
02  #MMMMMM...___....MMMMMMMM..........#
03  #MMMMMM...___....MMMMMMMM..........#
04  #MMMMMM...___......................#
05  #MMMMMM...___..............c.......#
06  #.........___......................#
07  #.........___......................#
08  #.........___......................#
09  #........__________________________#
10  ____________________________________
11  ____________________________________
12  ____________________________________
13  #........__________________________#
14  #..................................#
15  #..................................#
16  #..................................#
17  #..................................#
18  #.......##########.................#
19  #.......##########.................#
20  #.......##########.................#
21  #.......##########.................#
22  #.......##########.................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d14_royal_causeway` / east | [37, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d16_pharaohs_gate` / west | [2, 11] | always |
| north | N cols [10, 12] | [11, 2]; 6 | `rm_o6_memorial_vault` / south | [11, 19] | always |

Authored main walking line: [2, 11] -> [11, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Five-cell ceremonial paving is flat. No enemies, water, bridge, stairs or gate. O6 branches north before the save room; no branch beyond the star.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- None; preserve the quiet room.

Treasure:

- `rm_d15_tomb_approach:c1` at [27, 5]: 2 x `potion_greater`. Guaranteed pre-boss consumables on a short, enemy-free side pocket. Approach [27, 7]; interact from [27, 6]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d15_tomb_approach:deco1`: `spr_pharaoh_statue` at [4, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). First intact royal statue; the second has lost its head.
- `rm_d15_tomb_approach:deco2`: `spr_ruin_block` at [20, 2], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Broken companion statue base on solid masonry.
- `rm_d15_tomb_approach:deco3`: `spr_bush_dead` at [29, 19], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `spr_bush_dead`, `spr_chest_desert`, `spr_icon_potion_greater`, `spr_pharaoh_statue`, `spr_ruin_block`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d15_tomb_approach.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Echo Grotto

Stable ID: `rm_o5_echo_grotto`. Dimensions: **32 x 22 tiles** (2048 x 1408 px). Purpose: A clearly optional cave encounter grants the chapter's premium sword. Intensity: **high**.

```text
    0         1         2         3 
    01234567890123456789012345678901
00  ################################
01  ################################
02  ################################
03  ####........................####
04  ####......................c.####
05  ####........................####
06  ######.........................#
07  ######...........,,,,,,,,,.....#
08  ######..........e,,,,,e,,,.....#
09  ######...........,,,,,,,,,.....#
10  ######...........,,,...........#
11  ######...........,,,...........#
12  ######...........,,,e..........#
13  #................,,,...........#
14  #.........,,,,,,,,,,.......#####
15  #.........,,,,,,,,,,.......#####
16  #.........,,,,,,,,,,.......#####
17  #.........___..............#####
18  #.........___..............#####
19  #.........___..............#####
20  #.........___..............#####
21  ##########___###################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| south | S cols [10, 12] | [11, 19]; 2 | `rm_d13_windblown_plateau` / north | [11, 2] | always |

Authored main walking line: [11, 19] -> [11, 15] -> [18, 15] -> [18, 8] -> [25, 8] -> [25, 5]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Cave walls are #; all sand pockets connect. No combat lock, water, stairs or bridge; bats respect walls and cannot attack through the roof.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_o5_echo_grotto:g1`: pad/leash [14, 6, 24, 14]; max 3 active. Optional three-enemy mastery check: visible bat circles over a telegraphed ground lunge, with an eleven by nine floor. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_o5_echo_grotto:g1:e1`: `bat` at [16, 8].
  - `rm_o5_echo_grotto:g1:e2`: `bat` at [22, 8].
  - `rm_o5_echo_grotto:g1:e3`: `python` at [20, 12].

Treasure:

- `rm_o5_echo_grotto:c1` at [26, 4]: 1 x `sunsteel_blade`. A strong optional weapon, never assumed by Pharaoh health tuning. Approach [26, 6]; interact from [26, 5]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_o5_echo_grotto:deco1`: `spr_ruin_block` at [7, 2], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Ancient blade shrine embedded in the cave roof; no hidden breakable wall.
- `rm_o5_echo_grotto:deco2`: `spr_pebbles` at [6, 17], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_o5_echo_grotto:deco3`: `spr_skull` at [29, 16], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_bat_screech`, `snd_chest_open`, `snd_snake_hiss`, `snd_snake_lunge`, `spr_bat_defeat`, `spr_bat_dive`, `spr_bat_fly`, `spr_chest_desert`, `spr_icon_sunsteel_blade`, `spr_mask_bat`, `spr_mask_python`, `spr_pebbles`, `spr_python_coil`, `spr_python_defeat`, `spr_python_hurt`, `spr_python_lunge_down`, `spr_python_lunge_side`, `spr_python_lunge_up`, `spr_python_slither_down`, `spr_python_slither_side`, `spr_python_slither_up`, `spr_ruin_block`, `spr_skull`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_o5_echo_grotto.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.
