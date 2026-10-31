> SUPERSEDED: reference only. Use [the expanding scene design](DESERT_CHAPTER.md). These are no longer separate loaded areas.

# Desert design - batch 03

[Chapter graph, conventions and import rules](DESERT_CHAPTER.md). Grid = 64 px tiles, zero-based [x,y]. Rectangles and spans inclusive. Terrain JSON is authoritative; diagram letters overlay objects. Legend: . sand, , path, ; grass, ~ blocked water, # blocked cliff, M blocked masonry, _ paving, ^ stairs, C blocked chasm, = E/W bridge, | N/S bridge, x blocked broken span; e enemy, c chest, S star, p solid prop, t trigger, i initial spawn, g gate. Decorative placement has no collision and is listed separately.

## Ruined Caravan

Stable ID: `rm_d07_ruined_caravan`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: Introduce fast melee around a wreck while leaving broad bypass lanes. Intensity: **medium**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  ########..........########.........#
02  ########..........########.........#
03  ########..........########.........#
04  ########...........................#
05  #............................c.....#
06  #....................p.............#
07  #..................................#
08  #..................................#
09  #............e.....................#
10  _____,,,,,,,,,,.............,,,_____
11  _____,,,,,,,,,,.............,,,_____
12  _____,,,,,,,,,,.............,,,_____
13  #...........,,,.............,,,....#
14  #...........,,,.............,,,....#
15  #...........,,,,,,,,,,,,,,,,e,,....#
16  #...........,,,,,,,,,,,,,,,,,,,....#
17  #...........,,,,,,,,,,,,,,,,,,,....#
18  #..................................#
19  #...........#########..............#
20  #...........#########..............#
21  #...........#########..............#
22  #...........#########..............#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d06_oasis_refuge` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d08_cactus_flats` / west | [2, 11] | always |

Authored main walking line: [2, 11] -> [13, 11] -> [13, 16] -> [29, 16] -> [29, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Wagon blocks only its explicit 160 by 40 pixel base; validator conservatively blocks three cells.
- No water, cliffs across the lane, stairs, bridge or encounter gate.

Solid props (separate from art-only decoration):

- `wagon_wreck` at [21, 6], centred base footprint [160, 40] px; conservative blocked cells rectangle [20, 6, 22, 6].

Encounters:

- `rm_d07_ruined_caravan:g1`: pad/leash [10, 6, 16, 12]; max 1 active. First fast attacker, separated from the wreck footprint and later reinforcement. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d07_ruined_caravan:g1:e1`: `bandit` at [13, 9].
- `rm_d07_ruined_caravan:g2`: pad/leash [24, 12, 30, 18]; max 1 active. Repeat the dash-and-recover read while the player chooses which side of the wagon to pass. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d07_ruined_caravan:g2:e1`: `bandit` at [28, 15].

Treasure:

- `rm_d07_ruined_caravan:c1` at [29, 5]: 1 x `bandit_scimitar`. A weapon sidegrade in abandoned cargo; no unique movement or key function. Approach [29, 7]; interact from [29, 6]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d07_ruined_caravan:deco1`: `spr_ruin_block` at [21, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Caravan stone cargo spilled into the north rim.
- `rm_d07_ruined_caravan:deco2`: `spr_pebbles` at [6, 18], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_wind_loop`, `spr_bandit_attack_down`, `spr_bandit_attack_side`, `spr_bandit_attack_up`, `spr_bandit_defeat`, `spr_bandit_hurt_down`, `spr_bandit_idle_down`, `spr_bandit_walk_down`, `spr_bandit_walk_side`, `spr_bandit_walk_up`, `spr_chest_desert`, `spr_icon_bandit_scimitar`, `spr_mask_medium`, `spr_pebbles`, `spr_ruin_block`, `spr_tumbleweed`, `spr_wagon_wreck`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d07_ruined_caravan.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Cactus Flats

Stable ID: `rm_d08_cactus_flats`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: A low-pressure grove gives landmark navigation and an optional bandit-cache turn. Intensity: **low**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ##########___#######################
01  ######....___......................#
02  ######....___.....######...........#
03  ######....___.....######...........#
04  ######....___.....######...........#
05  ######....,,,...........p..........#
06  #......p..,,,...p..................#
07  #.........,,,......................#
08  #.........,,,.......,,,,,,,,,,,,...#
09  #.........,,,.......,,,,,,,,,,,,...#
10  _____,,,,,,,,,,,,,,,,,,,,,,,,,,_____
11  _____,,,,,,,,,,,,,,,,,,......,,_____
12  _____,,,,,,,,,,,,,,,,,,......,,_____
13  #..................................#
14  #..................................#
15  #..................................#
16  #..................................#
17  #.....p...................e........#
18  #...............p...............p..#
19  #..............................c...#
20  #..................................#
21  #..................................#
22  #..................................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d07_ruined_caravan` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d09_bonefield` / west | [2, 11] | always |
| north | N cols [10, 12] | [11, 2]; 6 | `rm_o3_bandit_cache` / south | [11, 19] | always |

Authored main walking line: [2, 11] -> [11, 11] -> [21, 11] -> [21, 9] -> [30, 9] -> [30, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Cactus collisions use trunks only; no random solid cactus placement. Lanes never narrow below three cells.
- North branch O3 is an optional higher-pressure cache. No water, stairs, bridge or chasm.

Solid props (separate from art-only decoration):

- `cactus_tall` at [7, 6], centred base footprint [24, 16] px; conservative blocked cells rectangle [7, 6, 7, 6].
- `cactus_tall` at [16, 6], centred base footprint [24, 16] px; conservative blocked cells rectangle [16, 6, 16, 6].
- `cactus_tall` at [24, 5], centred base footprint [24, 16] px; conservative blocked cells rectangle [24, 5, 24, 5].
- `cactus_tall` at [6, 17], centred base footprint [24, 16] px; conservative blocked cells rectangle [6, 17, 6, 17].
- `cactus_tall` at [16, 18], centred base footprint [24, 16] px; conservative blocked cells rectangle [16, 18, 16, 18].
- `cactus_tall` at [32, 18], centred base footprint [24, 16] px; conservative blocked cells rectangle [32, 18, 32, 18].

Encounters:

- `rm_d08_cactus_flats:g1`: pad/leash [23, 14, 29, 20]; max 1 active. A voluntary southern coil challenge; the central path and north detour stay quiet. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d08_cactus_flats:g1:e1`: `python` at [26, 17].

Treasure:

- `rm_d08_cactus_flats:c1` at [31, 19]: 2 x `potion_health`. Recovery for a careful reader of the cactus gaps. Approach [31, 21]; interact from [31, 20]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d08_cactus_flats:deco1`: `spr_bush_dead` at [20, 20], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_d08_cactus_flats:deco2`: `spr_rock_small` at [20, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Three dark stones distinguish the north cache trail from the east route.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_snake_hiss`, `snd_snake_lunge`, `snd_wind_loop`, `spr_bush_dead`, `spr_cactus_tall`, `spr_chest_desert`, `spr_icon_potion_health`, `spr_mask_python`, `spr_python_coil`, `spr_python_defeat`, `spr_python_hurt`, `spr_python_lunge_down`, `spr_python_lunge_side`, `spr_python_lunge_up`, `spr_python_slither_down`, `spr_python_slither_side`, `spr_python_slither_up`, `spr_rock_small`, `spr_tumbleweed`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d08_cactus_flats.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Bonefield

Stable ID: `rm_d09_bonefield`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: Introduce an archer with a frontal melee distraction, then a short second duel. Intensity: **high**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #..................................#
02  #...#####........####..............#
03  #...#####........####..............#
04  #...#####........####..............#
05  #..................................#
06  #..................................#
07  #..........,,,,,,,,,,,,,,,,,e......#
08  #..........,,,,,,,,,,,,,,,,,,......#
09  #..........,,,e,,,,,,,,,,,,,,......#
10  _____,,,,,,,,,............,,,,,_____
11  _____,,,,,,,,,...........e,,,,,_____
12  _____,,,,,,,,,............,,,,,_____
13  #..................................#
14  #..................................#
15  #..................................#
16  #..................................#
17  #..................................#
18  #.....########.....................#
19  #.....########..............c......#
20  #.....########.....................#
21  #.....########.....................#
22  #.....########.....................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d08_cactus_flats` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d10_broken_bridge` / west | [2, 11] | always |

Authored main walking line: [2, 11] -> [12, 11] -> [12, 8] -> [27, 8] -> [27, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- All skulls and bones are flat decoration; cliff islands alone block. No water, elevation, stairs, bridge or gate.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d09_bonefield:g1`: pad/leash [10, 5, 18, 13]; max 1 active. Known melee before exposing the archer; a nine-cell square supports flanking. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d09_bonefield:g1:e1`: `skeleton_warrior` at [14, 9].
- `rm_d09_bonefield:g2`: pad/leash [22, 5, 30, 13]; max 2 active. First ranged plus melee mix; approach diagonally on open sand, never along a one-cell funnel. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d09_bonefield:g2:e1`: `skeleton_archer` at [28, 7].
  - `rm_d09_bonefield:g2:e2`: `skeleton_warrior` at [25, 11].

Treasure:

- `rm_d09_bonefield:c1` at [28, 19]: 2 x `ancient_coin`, 1 x `potion_health`. A southern recovery loop after the hardest early group; no mandatory kill lock. Approach [28, 21]; interact from [28, 20]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d09_bonefield:deco1`: `spr_skull` at [7, 3], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). A few skulls, not a carpet; silhouettes contrast with intact ruin columns ahead.
- `rm_d09_bonefield:deco2`: `spr_pebbles` at [18, 19], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_d09_bonefield:deco3`: `spr_tree_dead` at [19, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_arrow_hit`, `snd_bow_release`, `snd_chest_open`, `snd_wind_loop`, `spr_arrow`, `spr_chest_desert`, `spr_fx_arrow_hit`, `spr_icon_ancient_coin`, `spr_icon_potion_health`, `spr_mask_medium`, `spr_pebbles`, `spr_skeleton_archer_attack_down`, `spr_skeleton_archer_attack_side`, `spr_skeleton_archer_attack_up`, `spr_skeleton_archer_defeat`, `spr_skeleton_archer_hurt_down`, `spr_skeleton_archer_idle_down`, `spr_skeleton_archer_walk_down`, `spr_skeleton_archer_walk_side`, `spr_skeleton_archer_walk_up`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `spr_skull`, `spr_tree_dead`, `spr_tumbleweed`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d09_bonefield.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Bandit Cache

Stable ID: `rm_o3_bandit_cache`. Dimensions: **32 x 22 tiles** (2048 x 1408 px). Purpose: A deliberate optional two-enemy challenge rewards armor and a strong restorative. Intensity: **high**.

```text
    0         1         2         3 
    01234567890123456789012345678901
00  ################################
01  #######........................#
02  #######........................#
03  #######........................#
04  #######....................c...#
05  #######........................#
06  #######..............e.........#
07  #######..........,,,,,,,,,,,...#
08  #................,,,,,,,,,,,...#
09  #...............e,,,,,,,,,,,...#
10  #................,,,...........#
11  #................,,,...........#
12  #................,,,...........#
13  #................,,,.....#######
14  #......p..,,,,,,,,,,.....#######
15  #.........,,,,,,,,,,.....#######
16  #.........,,,,,,,,,,.....#######
17  #.........___............#######
18  #.........___............#######
19  #.........___............#######
20  #.........___............#######
21  ##########___###################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| south | S cols [10, 12] | [11, 19]; 2 | `rm_d08_cactus_flats` / north | [11, 2] | always |

Authored main walking line: [11, 19] -> [11, 15] -> [18, 15] -> [18, 8] -> [26, 8] -> [27, 6]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- No ambush spawns, exit lock, water, stairs or bridge. The south approach remains outside the group's leash.

Solid props (separate from art-only decoration):

- `wagon_wreck` at [7, 14], centred base footprint [160, 40] px; conservative blocked cells rectangle [6, 14, 8, 14].

Encounters:

- `rm_o3_bandit_cache:g1`: pad/leash [14, 4, 22, 12]; max 2 active. Optional early spell preview; dodge one visible orb while isolating the fast melee attacker. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_o3_bandit_cache:g1:e1`: `bandit` at [16, 9].
  - `rm_o3_bandit_cache:g1:e2`: `bandit_caster` at [21, 6].

Treasure:

- `rm_o3_bandit_cache:c1` at [27, 4]: 1 x `iron_tunic`, 1 x `potion_greater`. Clear optional equipment improvement; never part of the chapter's required power budget. Approach [27, 6]; interact from [27, 5]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_o3_bandit_cache:deco1`: `spr_ruin_block` at [3, 4], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Canvas shelter is implied by cargo on the rock rim; do not invent a new tent asset.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_cast_charge`, `snd_chest_open`, `snd_magic_hit`, `snd_magic_travel`, `snd_wind_loop`, `spr_bandit_attack_down`, `spr_bandit_attack_side`, `spr_bandit_attack_up`, `spr_bandit_caster_attack_down`, `spr_bandit_caster_attack_side`, `spr_bandit_caster_attack_up`, `spr_bandit_caster_defeat`, `spr_bandit_caster_hurt_down`, `spr_bandit_caster_idle_down`, `spr_bandit_caster_walk_down`, `spr_bandit_caster_walk_side`, `spr_bandit_caster_walk_up`, `spr_bandit_defeat`, `spr_bandit_hurt_down`, `spr_bandit_idle_down`, `spr_bandit_walk_down`, `spr_bandit_walk_side`, `spr_bandit_walk_up`, `spr_chest_desert`, `spr_fx_magic_hit`, `spr_fx_magic_launch`, `spr_icon_iron_tunic`, `spr_icon_potion_greater`, `spr_magic_orb`, `spr_mask_medium`, `spr_ruin_block`, `spr_tumbleweed`, `spr_wagon_wreck`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_o3_bandit_cache.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.
