> SUPERSEDED: reference only. Use [the expanding scene design](DESERT_CHAPTER.md). These are no longer separate loaded areas.

# Desert design - batch 02

[Chapter graph, conventions and import rules](DESERT_CHAPTER.md). Grid = 64 px tiles, zero-based [x,y]. Rectangles and spans inclusive. Terrain JSON is authoritative; diagram letters overlay objects. Legend: . sand, , path, ; grass, ~ blocked water, # blocked cliff, M blocked masonry, _ paving, ^ stairs, C blocked chasm, = E/W bridge, | N/S bridge, x blocked broken span; e enemy, c chest, S star, p solid prop, t trigger, i initial spawn, g gate. Decorative placement has no collision and is listed separately.

## Split Cliffs

Stable ID: `rm_d04_split_cliffs`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: Two reconverging lanes around a cliff island; the upper lane rewards a short climb. Intensity: **medium**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #.............................######
02  #........,,,,,,,,,,,,,,,,,,,,,,,,###
03  #........,,,,,,,,,,,,,,,,c,,,,,,,..#
04  #........,,,,,,,,,,,,,,,,,,,,,,,,..#
05  #........,,,..................,,,..#
06  #........,,,..................,,,..#
07  ########^^^^##################,,,..#
08  ########^^^^##################,,,..#
09  #........,,,.###########......,,,..#
10  _____,,,,,,,.###########...,,,,_____
11  _____,,,,,,,.###########...,,,,_____
12  _____,,,,,,,.###########...,,,,_____
13  #.....,,,....###########...,,,.....#
14  #.....,,,..................,,,.....#
15  #.....,,,,,,,,,,,,,,,,,,,,,,,,.....#
16  #.....,,,,,,,,,,,,,,,,,,,,,,e,.....#
17  #.....,,,,,,,,,,,,,,,,,,,,,,,,.....#
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
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d03_canyon_approach` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d05_dry_wash` / west | [2, 11] | always |

Authored main walking line: [2, 11] -> [7, 11] -> [7, 16] -> [28, 16] -> [28, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Main lower lane is flat; upper lane contains stairs and an east ramp. No drop, water, chasm or bridge.
- stairs [8, 7, 11, 8]: Four-wide climb to z1 northern ledge. Return by stairs or the broad eastern ramp at x30..33.
- ramp [30, 3, 33, 10]: Bidirectional sand ramp blends z1 down to z0, clear four-cell width.
- Visual level 1, north_ledge rectangle [1, 1, 29, 6]; only authored connectors cross a solid level boundary.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d04_split_cliffs:g1`: pad/leash [24, 13, 32, 21]; max 1 active. Introduce a firmer melee windup on the broad lower approach, away from stairs. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d04_split_cliffs:g1:e1`: `skeleton_warrior` at [28, 16].

Treasure:

- `rm_d04_split_cliffs:c1` at [25, 3]: 1 x `ancient_coin`. Upper-lane souvenir; neither lane is mandatory for the other. Approach [25, 5]; interact from [25, 4]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d04_split_cliffs:deco1`: `spr_boulder` at [18, 11], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Split central island divides the two visible routes; art sits on solid cells.
- `rm_d04_split_cliffs:deco2`: `spr_cactus_tall` at [17, 7], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Sparse dressing; keep readable floor and telegraphs.
- `rm_d04_split_cliffs:deco3`: `spr_pebbles` at [5, 18], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_wind_loop`, `spr_boulder`, `spr_cactus_tall`, `spr_chest_desert`, `spr_icon_ancient_coin`, `spr_mask_medium`, `spr_pebbles`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `spr_tumbleweed`, `tex_paving`, `ts_stairs`.

Implementation sources: `design/desert/rooms/rm_d04_split_cliffs.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Dry Wash

Stable ID: `rm_d05_dry_wash`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: A quiet riverbed read leads toward palms; the first python guards a voluntary southern pocket. Intensity: **low**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ####################################
01  #...........,,,....................#
02  #.......####,,,....................#
03  #.......####,,,..####..............#
04  #.......####,,,..####..............#
05  #.......####,,,..####..............#
06  #.......####,,,..####..............#
07  #.......####,,,....................#
08  #...........,,,,,,,,,,,............#
09  #...........,,,,,,,,,,,............#
10  _____,,,,,,.,,,,,,,,,,,,,,,,,,,_____
11  _____,,,,,,........,,,,,,,,,,,,_____
12  _____,,,,,,,,,,,,,,,,,,,,,,,,,,_____
13  #.......,,,,,,,,,,,,,,,............#
14  #.......,,,,,,,,,,,,,,,............#
15  #...................,,,............#
16  #...................,,,............#
17  #...................,,,...e........#
18  #..##########.......,,,,,,,,,,,,,..#
19  #..##########.......,,,,,,,,,,,,,c.#
20  #..##########.......,,,,,,,,,,,,,..#
21  #..##########......................#
22  #..##########......................#
23  ####################################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d04_split_cliffs` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d06_oasis_refuge` / west | [2, 11] | always |

Authored main walking line: [2, 11] -> [9, 11] -> [9, 13] -> [20, 13] -> [20, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Dark sand is a dry wash, not flowing water or quicksand. All , cells have ordinary movement.
- No bridge or stairs. Python cannot pursue onto checkpoint approach or within arrival reserves.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- `rm_d05_dry_wash:g1`: pad/leash [23, 14, 31, 20]; max 1 active. Optional first coil-and-lunge lesson with room to move sideways; path to oasis remains calm. Player enters combat_rect; no attacks before activation. Respect arrival protection.
  - `rm_d05_dry_wash:g1:e1`: `python` at [26, 17].

Treasure:

- `rm_d05_dry_wash:c1` at [33, 19]: 2 x `potion_health`. Tempt a deliberate step into the wash pocket; not required before the healing checkpoint. Approach [33, 21]; interact from [33, 20]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d05_dry_wash:deco1`: `spr_tree_desert` at [18, 4], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Dry roots above the wash; green palm silhouette appears beyond the east exit.
- `rm_d05_dry_wash:deco2`: `spr_palm` at [32, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Distant oasis cue on solid edge rock; decorative only.
- `rm_d05_dry_wash:deco3`: `spr_pebbles` at [14, 19], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.

Music: `mus_desert`; weather flags: `{"sandstorm": true, "tumbleweeds": true}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `snd_snake_hiss`, `snd_snake_lunge`, `snd_wind_loop`, `spr_chest_desert`, `spr_icon_potion_health`, `spr_mask_python`, `spr_palm`, `spr_pebbles`, `spr_python_coil`, `spr_python_defeat`, `spr_python_hurt`, `spr_python_lunge_down`, `spr_python_lunge_side`, `spr_python_lunge_up`, `spr_python_slither_down`, `spr_python_slither_side`, `spr_python_slither_up`, `spr_tree_desert`, `spr_tumbleweed`, `tex_paving`.

Implementation sources: `design/desert/rooms/rm_d05_dry_wash.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Oasis Refuge

Stable ID: `rm_d06_oasis_refuge`. Dimensions: **36 x 24 tiles** (2304 x 1536 px). Purpose: First full refuge: water, grass, a clear checkpoint and an optional restorative detour. Intensity: **quiet**.

```text
    0         1         2         3     
    012345678901234567890123456789012345
00  ##########___#######################
01  #.........___......................#
02  #.......;;___;;;;;;;;;;;;;.........#
03  #.......;;___;;;;;;;;;;;;;MM.......#
04  #.......;;___;~~~~~~~~;;;;MM.......#
05  #.......;;,,,~~~~~~~~~;;p;MM.......#
06  #.......;;,,,~~~~~~~~~;;;;...c.....#
07  #.......p;,,,~~~~~~~~~;;;;.........#
08  #.......;;,,,;~~~~~~~~;;;;.........#
09  #.......;;,,,;;;;;;;;;;______......#
10  _____,,,,,,,,,,,,,,,,,,______,,_____
11  _____,,,,,,,,,,,,,,,,,,__S___,,_____
12  _____,,,,,,,,,,,,,,,,,,______,,_____
13  #......................______......#
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
| west | W rows [10, 12] | [2, 11]; 0 | `rm_d05_dry_wash` / east | [33, 11] | always |
| east | E rows [10, 12] | [33, 11]; 4 | `rm_d07_ruined_caravan` / west | [2, 11] | always |
| north | N cols [10, 12] | [11, 2]; 6 | `rm_o2_hidden_spring` / south | [11, 19] | always |

Authored main walking line: [2, 11] -> [25, 11] -> [33, 11]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- All ~ cells are shallow-looking but impassable shoreline; no swimming. The southern shore is at least three clear cells deep.
- No enemies, cliffs inside the floor, stairs, bridges or hazards. North exit leads to O2. Save interaction is player initiated.

Solid props (separate from art-only decoration):

- `palm` at [8, 7], centred base footprint [24, 14] px; conservative blocked cells rectangle [8, 7, 8, 7].
- `palm` at [24, 5], centred base footprint [24, 14] px; conservative blocked cells rectangle [24, 5, 24, 5].

Encounters:

- None; preserve the quiet room.

Treasure:

- `rm_d06_oasis_refuge:c1` at [29, 6]: 2 x `potion_health`. An unguarded emergency reserve beside the refuge; never required to activate the star. Approach [29, 8]; interact from [29, 7]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- `rm_d06_oasis_refuge:checkpoint` at [25, 11]; respawn [25, 11]; clear pad [24, 10, 26, 12]. E interaction; three save slots; heal on successful save; no automatic overwrite.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_d06_oasis_refuge:deco1`: `spr_bush` at [9, 3], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_d06_oasis_refuge:deco2`: `spr_bush` at [22, 9], pixel offset [0, 0], layer `Visual_Assets` (fixed_flat_decal). Sparse dressing; keep readable floor and telegraphs.
- `rm_d06_oasis_refuge:deco3`: `spr_ruin_block` at [26, 4], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). A low square of old stone frames the safe star; no new collision.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_checkpoint`, `snd_chest_open`, `snd_save`, `spr_bush`, `spr_checkpoint_star`, `spr_chest_desert`, `spr_fx_sparkle`, `spr_icon_potion_health`, `spr_palm`, `spr_ruin_block`, `tex_grass`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `tex_water`, `tex_wet_sand`.

Implementation sources: `design/desert/rooms/rm_d06_oasis_refuge.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.

## Hidden Spring

Stable ID: `rm_o2_hidden_spring`. Dimensions: **32 x 22 tiles** (2048 x 1408 px). Purpose: A quiet loop around a spring provides healing and a botanical valuable. Intensity: **quiet**.

```text
    0         1         2         3 
    01234567890123456789012345678901
00  ################################
01  #..............................#
02  #.###..........................#
03  #.###.,,,,,,,,,,,,,,,,,,,,,....#
04  #.###.,,,,,,,,,,,,,,,,,,,,c....#
05  #.....,,,,,,,,,,,,,,,,,,,,,....#
06  #.....,,,;;;~~~~~~~~~;;;,,,....#
07  #.....,,,;;;~~~~~~~~~;;;,,,....#
08  #.....,,,;;;~~~~~~~~~;;;,,,....#
09  #.....,,,;;;~~~~~~~~~;;;,,,....#
10  #.....,,,;;;;;~~~~~~;;;;,,,....#
11  #.....,,,;;;;;~~~~~~;;;;,,,....#
12  #.....,,,;;;;;;ttt;;;;;;,,,....#
13  #.....,,,;,,,,,ttt,,,,,,,,,....#
14  #.....,,,,,,,,,,,,,,,,,,,,,....#
15  #.....,,,,,,,,,,,,,,,,,,,,,....#
16  #.....,,,,,,,..................#
17  #.........___..................#
18  #.........___..................#
19  #.........___..................#
20  #.........___..................#
21  ##########___###################
```

Entrances / exits (arrival is inside this room; destination cell is inside the target):

| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |
|---|---|---|---|---|---|
| south | S cols [10, 12] | [11, 19]; 2 | `rm_d06_oasis_refuge` / north | [11, 2] | always |

Authored main walking line: [11, 19] -> [11, 15] -> [7, 15] -> [7, 4] -> [25, 4]. These are guidance waypoints; all legal floor remains walkable.

Terrain and boundaries:

- Water blocks; the entire outer bank is connected. No combat, cliffs in the route, stairs, bridges, save checkpoint or movement upgrade.

Solid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.

Encounters:

- None; preserve the quiet room.

Treasure:

- `rm_o2_hidden_spring:c1` at [26, 4]: 1 x `desert_rose`. A small collectible at the far side of a visible shoreline loop. Approach [26, 6]; interact from [26, 5]. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.

Checkpoint / script data:

- `hidden_spring_heal`, event `interact_heal`, trigger [15, 12, 17, 13], persistent flag `None`: E on dry south bank restores HP; no save UI, item, XP or persistent reward. No effect at full HP.

Landmarks and decoration (art-only, no gameplay or collision):

- `rm_o2_hidden_spring:deco1`: `spr_healing_spring` at [16, 8], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Animated spring sits on blocked water; interact from a separate dry bank trigger.
- `rm_o2_hidden_spring:deco2`: `spr_palm` at [3, 3], pixel offset [0, 0], layer `Instances` (sort_by_ground_point_no_collision). Nonblocking silhouette beyond the trail; base is drawn on perimeter rock.

Music: `mus_desert`; weather flags: `{"sandstorm": false, "tumbleweeds": false}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:

`snd_chest_open`, `spr_chest_desert`, `spr_healing_spring`, `spr_icon_desert_rose`, `spr_palm`, `tex_grass`, `tex_paving`, `tex_water`, `tex_wet_sand`.

Implementation sources: `design/desert/rooms/rm_o2_hidden_spring.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.
