# Desert Frontier - expanding scene design

[Current chapter structure](DESERT_CHAPTER.md). Stable scene ID `sc_desert_frontier`; technical GameMaker resource `rm_sc_desert_frontier`. Starting extent **128 x 80 tiles** (8192 x 5120 px). A broad first landscape: orient east, choose dune and canyon routes, climb a lookout loop, then recognize the oasis from multiple approaches.

No place below is a separate loaded scene. All place boundaries and batch edges are metadata only.

## Landscape overview

Reduced grid: one character summarizes 4 x 4 tiles; row labels are global tile rows. Full exact grid: `design/desert/scenes/rm_sc_desert_frontier.json`. Legend and coordinate rules are in the chapter document.

```text
00 ################################
04 ################################
08 #########pp##############..#####
12 ########.e,p...##########.~~pp##
16 ########,.._p..########..ptt.c##
20 ######p#^p#c#^^#######p..,ct...#
24 #####._,,c.##.,,c######.p.~.p,.#
28 #####..p#..p#p_.p.#####..~~~.p.#
32 ##pc#,.p.pe..,p,e.p.###p.~~~p,.#
36 #tt_,p,e....#.......###..p.p;.p_
40 #it.p,,,,,p.######.p###ppp,S,,.a
44 ###ppcp..##p#####...p,,,,,.ppcp#
48 ####ppp.p.pp#####.,cpp..#,;cpp.#
52 ######..p.e.##.pp.,..pp.#.,..###
56 ######.,,,,,,,,,..pp...p###p####
60 ##########c.########pe.c########
64 ####################....########
68 ################################
72 ################################
76 ################################
```

Scene transitions:

| Border | Opening rows | Arrival here | Destination scene / arrival |
|---|---|---|---|
| E | [38, 42] | [125, 40], pixels [8032, 2592] | `sc_caravan_basin` / [2, 40] |

Intro/first-death fallback: [7, 40], facing east. West scene border stays closed.

Preferred walking route: [7, 40] -> [28, 40] -> [43, 40] -> [43, 35] -> [61, 35] -> [75, 35] -> [75, 46] -> [96, 46] -> [96, 42] -> [108, 42] -> [118, 42] -> [118, 40] -> [125, 40]. This is a route suggestion, not a compulsory chain of place triggers.

Exploration circuits:

- **Lookout ridge circuit**: Leave the dune trail, climb west, claim shelf treasure, descend east and rejoin beyond the canyon approach. Waypoints: [28, 40] -> [24, 40] -> [24, 25] -> [34, 25] -> [34, 20] -> [34, 16] -> [56, 16] -> [56, 25] -> [61, 25] -> [61, 35].
- **Southern wash circuit**: A longer open-ground route passes the canyon's south end and reveals a coin pocket and python detour. Waypoints: [28, 40] -> [28, 57] -> [43, 57] -> [43, 53] -> [43, 57] -> [72, 57] -> [72, 46] -> [96, 46].
- **Oasis banks circuit**: Approach the oasis from either bank, discover the spring and return to a recognizable save landmark. Waypoints: [96, 42] -> [95, 42] -> [95, 20] -> [117, 20] -> [117, 42] -> [108, 42].
- **Lost Porters' Camp trail**: Find lost porters' camp and its supplies; return by another approach. Waypoints: [19, 40] -> [19, 48] -> [24, 48] -> [24, 40].
- **Wash Survey Camp trail**: Find wash survey camp and its supplies; return by another approach. Waypoints: [75, 46] -> [75, 53] -> [82, 53] -> [82, 46].
- **Spring Keeper's Niche trail**: Find spring keeper's niche and its supplies; return by another approach. Waypoints: [101, 20] -> [101, 24] -> [109, 24] -> [109, 20].
- **Buried Palm Garden trail**: Find buried palm garden and its supplies; return by another approach. Waypoints: [96, 46] -> [104, 46] -> [104, 53] -> [115, 53] -> [115, 42].

Elevation and structures:

- Lookout shelf z1: [29,10..60,21], fully bounded by solid rock except two five-wide stairs. Basin z0. No free cliff crossing, jumping or one-way drops.
- `stairs` [32, 22, 36, 23]: Five-wide west ascent to lookout shelf; north/south landings stay empty.
- `stairs` [54, 22, 58, 23]: Five-wide east descent returns to the canyon's far approach; forms a continuous exploration loop.

## Build this scene by expansion

1. **Opening expanse**: Block the broad basin, first combat and the full two-stair lookout circuit together. Do not make separate scenes for these places. Places: `place_arrival`, `place_dune_trail`, `place_canyon_approach`, `place_sunken_lookout`.
2. **Canyon and wash expansion**: Add the canyon notch, southern bypass, cliff islands and elective python pocket. Places: `place_split_cliffs`, `place_dry_wash`.
3. **Oasis expansion**: Extend into both lake banks, the northern spring circuit, checkpoint and east scene transition. Places: `place_oasis_refuge`, `place_hidden_spring`.

## Places and readable local grids

Each crop below uses global `[x,y]` coordinates, one character per tile. It is an inspection window into the shared scene, not an enclosed map or scene boundary. The crop's x origin is stated; row labels remain global. Objects outside a crop are still present in the same scene.

### Buried Palm Garden

`place_palm_garden`; anchor [109, 52]; inspection extent [106, 48, 113, 54]; x origin **106**. A close, recognizable little destination with an optional persistent supply cache.

```text
48 ........
49 .;;;;;p.
50 ;;;c;;;.
51 ;;;;;;p;
52 ;;;;;;;,
53 ,,,,,,,,
54 ........
```

### Spring Keeper's Niche

`place_spring_keeper`; anchor [105, 24]; inspection extent [102, 20, 109, 26]; x origin **102**. A close, recognizable little destination with an optional persistent supply cache.

```text
20 ,,,ttttt
21 ,;;;;;,,
22 ;;;c;;;,
23 ;;;;;;;,
24 ,,,,,,,,
25 .;;;;;.,
26 ........
```

### Wash Survey Camp

`place_survey_cache`; anchor [78, 52]; inspection extent [75, 48, 82, 54]; x origin **75**. A close, recognizable little destination with an optional persistent supply cache.

```text
48 ,,....,,
49 ,_____,,
50 ,_.c_p_,
51 ,______,
52 ,,__,__,
53 ,,,,,,,,
54 .......,
```

### Lost Porters' Camp

`place_lost_porters`; anchor [21, 47]; inspection extent [18, 43, 25, 49]; x origin **18**. A close, recognizable little destination with an optional persistent supply cache.

```text
43 ,,,.,,,.
44 ,,,,,,,.
45 ,,,c,,,.
46 ,,,,,,,.
47 ,,,,,,,.
48 ,,,,,,,,
49 .,....,.
```

### Desert Arrival

`place_arrival`; anchor [9, 40]; inspection extent [3, 29, 20, 53]; x origin **3**. Breached-city stone gives way to open sand; no enemies around the first chest.

```text
29 #################.
30 #################.
31 #################.
32 #########.....###.
33 #######.......###.
34 #####.p....c..###.
35 ####....____...##.
36 ####..____.__.....
37 #....p__.____.....
38 #.ttttttt__,_,,,,,
39 #.ttttttt,__,,,,,,
40 #.ttitttt,,,,,,,,,
41 #.ttttttt,.....,,,
42 #.ttttttt......,,,
43 #............p.,,,
44 ####...........,,,
45 ############p..,,,
46 ############..p,,,
47 ############...,,,
48 ############...,,,
49 ############..p.,.
50 ############......
51 ############......
52 ##################
53 ##################
```

### Dune Trail

`place_dune_trail`; anchor [28, 40]; inspection extent [21, 25, 36, 47]; x origin **21**. A first slow enemy on the main trail; dunes and the northern shelf invite a wider scan.

```text
25 ..__,__,,,,,,,,.
26 ._,____.....,,..
27 .____.___.......
28 .__,____........
29 .,____....######
30 .,,,...p.#######
31 .,,,....########
32 .,,,....########
33 .,,,...p......##
34 .,,,..........##
35 .,,,..........##
36 ..,,,.........##
37 ..,,,...........
38 ,p,,,...........
39 ,,,,,,,e,,......
40 ,,,,,,,,,,,,,,,,
41 ..,,,,,,,,,,,,,,
42 ..,,,.,,,.......
43 .,,,..,,,.......
44 ,,,,..,,,.....##
45 c,,,..,,,.....##
46 ,,,,.p,,.....###
47 ,,,,..,,......##
```

### Canyon Approach

`place_canyon_approach`; anchor [45, 35]; inspection extent [37, 28, 54, 43]; x origin **37**. Read a broad canyon notch, the upper lookout return and a southern bypass.

```text
28 ........p..######.
29 ...........######.
30 ...........######.
31 ...........######.
32 p.................
33 .................,
34 .....e......,,,,,,
35 ......,,,,,,,,,,,,
36 ......,,..........
37 ......,,..........
38 ......,,...######.
39 ......,....######.
40 ,,,,,,,....#######
41 ,,,,.......#######
42 ...........#######
43 ....p......#######
```

### Split Cliffs

`place_split_cliffs`; anchor [63, 35]; inspection extent [55, 26, 74, 42]; x origin **55**. Two separated cliff islands frame crossing paths without enclosing another small area.

```text
26 .__.__,.....c.######
27 _.____,.......######
28 ____.___......######
29 __.____.......######
30 .____,,..p.......###
31 p....,,..........###
32 ...p.,,.............
33 ,....,,,..........p.
34 ,,,,,,,,,,,,,,....,,
35 ,,,,,,,,,,e,,,,,,,,,
36 .....,,,,,,,,,,,,,,,
37 ....................
38 ....................
39 .###................
40 ####...............,
41 #################..,
42 #################..,
```

### Dry Wash

`place_dry_wash`; anchor [79, 46]; inspection extent [69, 43, 96, 68]; x origin **69**. A quiet dry riverbed winds toward green; an elective python pocket lies farther south.

```text
43 #....,...............###..,,
44 ............p..............,
45 ...,.........,,,,,,,,..,,,,,
46 ..,,,.......,,,,,,,,,,,,,,,,
47 ..,,.......,,,,,,,,,,,,,,,,,
48 ..,,..,,....,,..............
49 ..,,..,_____,,..............
50 ..,,..,_.c_p_,.p.####.....##
51 ..,,._,______,...####.....##
52 ...,.,,,__,__,...####.....##
53 ...,.,,,,,,,,,,..####.....##
54 ...,,........,...###......##
55 ...,,............p.p.......#
56 ...,.p...p..................
57 ,,,,...####.................
58 .......####...............p.
59 .......####.................
60 ......#####.................
61 ###########p.....e.........#
62 ###########.............c..#
63 ###########................#
64 ###########................#
65 ###########................#
66 ###########................#
67 ###########.............####
68 ############################
```

### Oasis Refuge

`place_oasis_refuge`; anchor [108, 42]; inspection extent [94, 23, 122, 51]; x origin **94**. A visible lake, palms, connected banks and safe star anchor the whole eastern basin.

```text
23 ......,,;;;;;;;,......,......
24 .....p,,,,,,,,,,,....,,,.....
25 .........;;;;;.,..p..,,,.....
26 .,,..................,,,.....
27 .,,....~~~~~~~~~~....,,,.....
28 .,,...~~~~~~~~~~~~...,,,.....
29 .,,..~~~~~~~~~~~~~~..,,,.....
30 .,,.~~~~~~~~~~~~~~~..,,,.p...
31 .,,.~~~~~~~~~~~~~~~..,,,.....
32 .,,..~~~~~~~~~~~~~~..,,,.....
33 .,,...~~~~~~~~~~~~....,,.....
34 .,,....~~~~~~~~~~;;...,,.....
35 .,,............;;;;;p.,,,....
36 .,,............;;;;;;.,,,....
37 .,,...........;;;;;;;;.,,....
38 ,,,............;p;;;;...,.p..
39 ,,,....p.......;;;;;;....,,,,
40 ,,,p.p...p.......;;.....,,,.,
41 ,,,,,.....,,,,,,,,.....,,....
42 ,,,,,,,,,,,,,,S,,,,,,,,,,....
43 .,,,,,,,,,,,,,,,,,,,,,,......
44 ..,,,,,,,,..........,,.c.....
45 ,,,,,..,,,,......p..,,.......
46 ,,,,,,,,,,,,........,,......p
47 ,,,,,,,,,,,,.......p,,.......
48 .........,,.........,,.......
49 ........,,,..;;;;;p.,,...p...
50 .######.,,,.;;;c;;;.,,......#
51 .######.,,,;;;;;;;p;,,...####
```

### Sunken Lookout

`place_sunken_lookout`; anchor [45, 19]; inspection extent [26, 8, 63, 23]; x origin **26**. Sunken Lookout becomes a two-stair shelf loop, with armor seen near the ledge and a separate way down.

```text
08 ######################################
09 ######################################
10 ########...p...p...###################
11 ########...........###################
12 ######.............###################
13 #####............................#####
14 ####........,,,,,,..p.............####
15 ####....,,,,,e,,,,,,,,,............###
16 ####...,,,,,,,,,,,____,,,,,,,,,....###
17 ####..,,,,,......___,___,,,,,.,,...###
18 ####..,,,.......__.____._.....,,...###
19 ####..,,,,.......____.__p.....,,...###
20 ####...,,,........_c___.......,,...###
21 #####.,,,,.p####.........#....,,...###
22 ######^^^^^#################^^^^^#####
23 ######^^^^^#################^^^^^#####
```

### Hidden Spring

`place_hidden_spring`; anchor [108, 19]; inspection extent [99, 10, 119, 22]; x origin **99**. Hidden Spring sits on the northern oasis-bank circuit; no loading door or dead-end branch.

```text
10 ................;;...
11 ..............;;;;;;.
12 ......~~~~~~..;p;;;p.
13 .....~~~~~~~~;;;;;;;;
14 ....~~~~~~~~~~;;;;;;;
15 ....~~~~~~~~~~;;;;;;.
16 .....~~~~~~~~..;;;;;.
17 ....p.~~~~~~.....c...
18 ..p...ttttt.p........
19 ,.....ttttt...,,,,...
20 ,,,,,,ttttt,,,,,,....
21 .,,,;;;;;,,,,,,,.....
22 .,,;;;c;;;,..........
```

## Gameplay placement

Encounters (IDs retained across the redesign):

- `rm_d02_dune_trail:g1`: pad/leash [23, 34, 33, 44], max 1 active. First undead windup lesson; wide sand around every side. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d02_dune_trail:g1:e1`: `undead` at [28, 39].
- `rm_d03_canyon_approach:g1`: pad/leash [38, 30, 46, 38], max 1 active. A familiar attacker near the canyon's west approach. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d03_canyon_approach:g1:e1`: `undead` at [42, 34].
- `rm_d03_canyon_approach:g2`: pad/leash [38, 49, 46, 57], max 1 active. Elective duel on the southern return route; does not seal a passage. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d03_canyon_approach:g2:e1`: `undead` at [42, 53].
- `rm_d04_split_cliffs:g1`: pad/leash [60, 31, 70, 39], max 1 active. First skeleton warrior in a broad, uncluttered crossing. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d04_split_cliffs:g1:e1`: `skeleton_warrior` at [65, 35].
- `rm_d05_dry_wash:g1`: pad/leash [81, 56, 91, 66], max 1 active. Python telegraph in a southern wash pocket; main oasis approach remains quiet. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d05_dry_wash:g1:e1`: `python` at [86, 61].
- `rm_o1_sunken_lookout:g1`: pad/leash [35, 11, 43, 19], max 1 active. Optional shelf duel before the armor; two stairs allow a different return. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_o1_sunken_lookout:g1:e1`: `undead` at [39, 15].

Chests (all unlocked, no ordinary kill lock; overflow stays pending):

- `rm_sc_desert_frontier:c1` at [14, 34]: 1 x `potion_health`. Approach [14, 36], interaction [14, 35]. A visible, unguarded first potion; learn interaction before danger. Legacy ID `rm_d01_arrival:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c2` at [39, 26]: 2 x `potion_health`. Approach [39, 28], interaction [39, 27]. Supplies after first combat; visible from the eastward path, reached around the dune. Legacy ID `rm_d02_dune_trail:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c3` at [43, 61]: 20 x `gold_coins`. Approach [43, 63], interaction [43, 62]. A small southern pocket pays for looking away from the dark path. Legacy ID `rm_d03_canyon_approach:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c4` at [67, 26]: 1 x `ancient_coin`. Approach [67, 28], interaction [67, 27]. Upper-lane souvenir; neither lane is mandatory for the other. Legacy ID `rm_d04_split_cliffs:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c5` at [93, 62]: 2 x `potion_health`. Approach [93, 64], interaction [93, 63]. Tempt a deliberate step into the wash pocket; not required before the healing checkpoint. Legacy ID `rm_d05_dry_wash:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c6` at [117, 44]: 2 x `potion_health`. Approach [117, 46], interaction [117, 45]. An unguarded emergency reserve beside the refuge; never required to activate the star. Legacy ID `rm_d06_oasis_refuge:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c7` at [45, 20]: 1 x `wanderer_tunic`, 1 x `potion_health`. Approach [45, 18], interaction [45, 19]. First optional armor and a potion. From the lower basin near [11,13], the chest is six cells east and four north, within the 1280 by 720 view; the west stairs provide access. Interact from its north side. Legacy ID `rm_o1_sunken_lookout:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c8` at [116, 17]: 1 x `desert_rose`. Approach [116, 19], interaction [116, 18]. A small collectible at the far side of a visible shoreline loop. Legacy ID `rm_o2_hidden_spring:c1` is mapped explicitly.
- `rm_sc_desert_frontier:c9` at [21, 45]: 1 x `potion_health`. Approach [21, 47], interaction [21, 46]. Optional discovery at Lost Porters' Camp; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_desert_frontier:c10` at [78, 50]: 6 x `gold_coins`. Approach [78, 52], interaction [78, 51]. Optional discovery at Wash Survey Camp; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_desert_frontier:c11` at [105, 22]: 1 x `desert_rose`. Approach [105, 24], interaction [105, 23]. Optional discovery at Spring Keeper's Niche; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_desert_frontier:c12` at [109, 50]: 1 x `ancient_coin`. Approach [109, 52], interaction [109, 51]. Optional discovery at Buried Palm Garden; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.

Checkpoint and scripts:

- `sc_desert_frontier:checkpoint` at/respawn [108, 42]; clear 3 x 3 [107, 41, 109, 43]; peaceful district [99, 37, 117, 48]. E opens exactly 3 save slots; heal on successful save; snapshot all state together.
- `desert_arrival` at [5, 38, 11, 42], event `chapter_start`, flag `desert_arrival_seen`: Intro ends at [7,40] facing east; initial death fallback is a complete snapshot here.
- `hidden_spring_heal` at [105, 18, 109, 20], event `interact_heal`, flag `None`: E on the bank heals without loot, XP or saving. At full HP do nothing.

Solid props (terrain/chests handled separately):

- `cactus_small` at [17, 49]; centred base [16, 12] px, conservative blocked cells [17, 49, 17, 49].
- `obelisk` at [45, 28]; centred base [40, 28] px, conservative blocked cells [45, 28, 45, 28].
- `palm` at [93, 33]; centred base [24, 14] px, conservative blocked cells [93, 33, 93, 33].
- `palm` at [119, 30]; centred base [24, 14] px, conservative blocked cells [119, 30, 119, 30].
- `wagon_wreck` at [16, 43]; centred base [160, 40] px, conservative blocked cells [15, 43, 17, 43].
- `water_barrel` at [17, 46]; centred base [38, 20] px, conservative blocked cells [17, 46, 17, 46].
- `supply_barrel` at [26, 46]; centred base [28, 16] px, conservative blocked cells [26, 46, 26, 46].
- `supply_barrel` at [26, 48]; centred base [28, 16] px, conservative blocked cells [26, 48, 26, 48].
- `column_fallen` at [80, 50]; centred base [36, 20] px, conservative blocked cells [80, 50, 80, 50].
- `water_barrel` at [74, 56]; centred base [38, 20] px, conservative blocked cells [74, 56, 74, 56].
- `palm` at [112, 25]; centred base [24, 14] px, conservative blocked cells [112, 25, 112, 25].
- `column_broken` at [111, 18]; centred base [28, 18] px, conservative blocked cells [111, 18, 111, 18].
- `palm` at [112, 51]; centred base [24, 14] px, conservative blocked cells [112, 51, 112, 51].
- `water_barrel` at [112, 49]; centred base [38, 20] px, conservative blocked cells [112, 49, 112, 49].
- `column_broken` at [113, 47]; centred base [28, 18] px, conservative blocked cells [113, 47, 113, 47].
- `column_broken` at [8, 37]; centred base [28, 18] px, conservative blocked cells [8, 37, 8, 37].
- `ruin_block` at [9, 34]; centred base [48, 24] px, conservative blocked cells [9, 34, 9, 34].
- `column_broken` at [25, 23]; centred base [28, 18] px, conservative blocked cells [25, 23, 25, 23].
- `ruin_block` at [28, 30]; centred base [48, 24] px, conservative blocked cells [28, 30, 28, 30].
- `column_broken` at [46, 14]; centred base [28, 18] px, conservative blocked cells [46, 14, 46, 14].
- `ruin_block` at [50, 19]; centred base [48, 24] px, conservative blocked cells [50, 19, 50, 19].
- `cactus_tall` at [33, 49]; centred base [24, 16] px, conservative blocked cells [33, 49, 33, 49].
- `cactus_small` at [32, 52]; centred base [16, 12] px, conservative blocked cells [32, 52, 32, 52].
- `tree_dead` at [45, 46]; centred base [24, 16] px, conservative blocked cells [45, 46, 45, 46].
- `supply_barrel` at [41, 43]; centred base [28, 16] px, conservative blocked cells [41, 43, 41, 43].
- `column_broken` at [58, 32]; centred base [28, 18] px, conservative blocked cells [58, 32, 58, 32].
- `ruin_block` at [55, 31]; centred base [48, 24] px, conservative blocked cells [55, 31, 55, 31].
- `tree_dead` at [61, 52]; centred base [24, 16] px, conservative blocked cells [61, 52, 61, 52].
- `supply_barrel` at [64, 53]; centred base [28, 16] px, conservative blocked cells [64, 53, 64, 53].
- `palm` at [81, 44]; centred base [24, 14] px, conservative blocked cells [81, 44, 81, 44].
- `water_barrel` at [78, 41]; centred base [38, 20] px, conservative blocked cells [78, 41, 78, 41].
- `tree_dead` at [95, 58]; centred base [24, 16] px, conservative blocked cells [95, 58, 95, 58].
- `column_fallen` at [88, 55]; centred base [36, 20] px, conservative blocked cells [88, 55, 88, 55].
- `palm` at [91, 23]; centred base [24, 14] px, conservative blocked cells [91, 23, 91, 23].
- `water_barrel` at [99, 24]; centred base [38, 20] px, conservative blocked cells [99, 24, 99, 24].
- `palm` at [114, 35]; centred base [24, 14] px, conservative blocked cells [114, 35, 114, 35].
- `water_barrel` at [110, 38]; centred base [38, 20] px, conservative blocked cells [110, 38, 110, 38].
- `column_broken` at [37, 21]; centred base [28, 18] px, conservative blocked cells [37, 21, 37, 21].
- `column_broken` at [122, 46]; centred base [28, 18] px, conservative blocked cells [122, 46, 122, 46].
- `ruin_block` at [119, 49]; centred base [48, 24] px, conservative blocked cells [119, 49, 119, 49].
- `column_broken` at [114, 12]; centred base [28, 18] px, conservative blocked cells [114, 12, 114, 12].
- `ruin_block` at [118, 12]; centred base [48, 24] px, conservative blocked cells [118, 12, 118, 12].
- `column_broken` at [15, 45]; centred base [28, 18] px, conservative blocked cells [15, 45, 15, 45].
- `ruin_block` at [21, 51]; centred base [48, 24] px, conservative blocked cells [21, 51, 21, 51].
- `column_broken` at [84, 50]; centred base [28, 18] px, conservative blocked cells [84, 50, 84, 50].
- `ruin_block` at [78, 56]; centred base [48, 24] px, conservative blocked cells [78, 56, 78, 56].
- `column_broken` at [103, 17]; centred base [28, 18] px, conservative blocked cells [103, 17, 103, 17].
- `ruin_block` at [101, 18]; centred base [48, 24] px, conservative blocked cells [101, 18, 101, 18].
- `column_broken` at [111, 45]; centred base [28, 18] px, conservative blocked cells [111, 45, 111, 45].
- `ruin_block` at [109, 56]; centred base [48, 24] px, conservative blocked cells [109, 56, 109, 56].
- `tree_dead` at [28, 33]; centred base [24, 16] px, conservative blocked cells [28, 33, 28, 33].
- `column_fallen` at [22, 38]; centred base [36, 20] px, conservative blocked cells [22, 38, 22, 38].
- `column_fallen` at [37, 32]; centred base [36, 20] px, conservative blocked cells [37, 32, 37, 32].
- `tree_dead` at [40, 48]; centred base [24, 16] px, conservative blocked cells [40, 48, 40, 48].
- `column_fallen` at [44, 48]; centred base [36, 20] px, conservative blocked cells [44, 48, 44, 48].
- `tree_dead` at [64, 30]; centred base [24, 16] px, conservative blocked cells [64, 30, 64, 30].
- `tree_dead` at [86, 55]; centred base [24, 16] px, conservative blocked cells [86, 55, 86, 55].
- `column_fallen` at [80, 61]; centred base [36, 20] px, conservative blocked cells [80, 61, 80, 61].
- `tree_dead` at [37, 10]; centred base [24, 16] px, conservative blocked cells [37, 10, 37, 10].
- `column_fallen` at [41, 10]; centred base [36, 20] px, conservative blocked cells [41, 10, 41, 10].
- `palm` at [101, 39]; centred base [24, 14] px, conservative blocked cells [101, 39, 101, 39].
- `palm` at [120, 38]; centred base [24, 14] px, conservative blocked cells [120, 38, 120, 38].
- `palm` at [103, 40]; centred base [24, 14] px, conservative blocked cells [103, 40, 103, 40].
- `water_barrel` at [99, 40]; centred base [38, 20] px, conservative blocked cells [99, 40, 99, 40].
- `column_fallen` at [97, 40]; centred base [36, 20] px, conservative blocked cells [97, 40, 97, 40].
- `palm` at [73, 33]; centred base [24, 14] px, conservative blocked cells [73, 33, 73, 33].
- `column_fallen` at [93, 40]; centred base [36, 20] px, conservative blocked cells [93, 40, 93, 40].

## Decoration and required assets

Decoration is separate, noncolliding art. Tall landmarks sit on existing blocked terrain unless their real base is listed as a solid prop above.

- `spr_ruin_block` at [18, 21], offset [0, 0], layer `Instances`. City rubble on the blocked dune: westward visual anchor.
- `spr_obelisk` at [61, 20], offset [0, 0], layer `Instances`. Lookout marker on the shelf's solid east rim.
- `spr_tree_dead` at [64, 46], offset [0, 0], layer `Instances`. Wind-shaped silhouette on the central blocked island.
- `spr_healing_spring` at [108, 15], offset [0, 0], layer `Instances`. Noncolliding art on blocked water; healing interaction is on the dry bank.
- `spr_bush` at [97, 37], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_pebbles` at [73, 58], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_skull` at [40, 60], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_loose_rocks` at [18, 48], offset [0, 0], layer `Visual_Assets`. Lost Porters' Camp — composed discovery
- `spr_bush_dead` at [25, 48], offset [0, 0], layer `Visual_Assets`. Lost Porters' Camp — composed discovery
- `spr_loose_rocks` at [76, 54], offset [0, 0], layer `Visual_Assets`. Wash Survey Camp — composed discovery
- `spr_pebbles` at [81, 48], offset [0, 0], layer `Visual_Assets`. Wash Survey Camp — composed discovery
- `spr_loose_rocks` at [81, 55], offset [0, 0], layer `Visual_Assets`. Wash Survey Camp — composed discovery
- `spr_bush` at [103, 23], offset [0, 0], layer `Visual_Assets`. Spring Keeper's Niche — composed discovery
- `spr_bush` at [108, 25], offset [0, 0], layer `Visual_Assets`. Spring Keeper's Niche — composed discovery
- `spr_loose_rocks` at [102, 26], offset [0, 0], layer `Visual_Assets`. Spring Keeper's Niche — composed discovery
- `spr_bush` at [107, 52], offset [0, 0], layer `Visual_Assets`. Buried Palm Garden — composed discovery
- `spr_bush` at [112, 52], offset [0, 0], layer `Visual_Assets`. Buried Palm Garden — composed discovery
- `spr_loose_rocks` at [106, 54], offset [0, 0], layer `Visual_Assets`. Buried Palm Garden — composed discovery
- `spr_loose_rocks` at [16, 35], offset [0, 0], layer `Visual_Assets`. Breached city baggage
- `spr_bush_dead` at [15, 38], offset [0, 0], layer `Visual_Assets`. Breached city baggage
- `spr_loose_rocks` at [22, 25], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns
- `spr_bush_dead` at [22, 28], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns
- `spr_loose_rocks` at [44, 15], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch
- `spr_bush_dead` at [47, 21], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch
- `spr_bush_dead` at [27, 52], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend
- `spr_pebbles` at [26, 50], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend
- `spr_pebbles` at [48, 44], offset [0, 0], layer `Visual_Assets`. Canyon windbreak
- `spr_bush_dead` at [48, 41], offset [0, 0], layer `Visual_Assets`. Canyon windbreak
- `spr_loose_rocks` at [54, 26], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker
- `spr_bush_dead` at [59, 31], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker
- `spr_pebbles` at [59, 59], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed
- `spr_bush_dead` at [58, 55], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed
- `spr_bush` at [74, 47], offset [0, 0], layer `Visual_Assets`. First green in the wash
- `spr_pebbles` at [76, 48], offset [0, 0], layer `Visual_Assets`. First green in the wash
- `spr_pebbles` at [95, 60], offset [0, 0], layer `Visual_Assets`. Shed snake bones
- `spr_loose_rocks` at [94, 57], offset [0, 0], layer `Visual_Assets`. Shed snake bones
- `spr_bush` at [93, 20], offset [0, 0], layer `Visual_Assets`. Spring-bank palms
- `spr_pebbles` at [96, 26], offset [0, 0], layer `Visual_Assets`. Spring-bank palms
- `spr_bush` at [110, 37], offset [0, 0], layer `Visual_Assets`. Lakeside resting place
- `spr_pebbles` at [111, 40], offset [0, 0], layer `Visual_Assets`. Lakeside resting place
- `spr_palm` at [123, 21], offset [0, 0], layer `Instances`. Hidden spring cairns
- `spr_water_barrel` at [120, 17], offset [0, 0], layer `Instances`. Hidden spring cairns
- `spr_bush` at [116, 23], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns
- `spr_pebbles` at [116, 22], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns
- `spr_column_broken` at [12, 29], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [16, 29], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [9, 32], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_ruin_block` at [41, 21], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [44, 24], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [38, 63], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [48, 63], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [38, 59], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [65, 21], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [69, 21], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [62, 24], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [98, 60], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [98, 64], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [95, 57], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [115, 39], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [50, 22], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [47, 25], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [47, 15], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [121, 15], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [16, 47], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [76, 45], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [100, 24], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [107, 45], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_pebbles` at [22, 39], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_tree_dead` at [36, 34], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_pebbles` at [44, 29], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [37, 51], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_column_fallen` at [65, 41], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_pebbles` at [63, 30], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [86, 67], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [34, 13], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_palm` at [91, 39], offset [0, 0], layer `Instances`. Spring-bank palms — trail-edge continuation
- `spr_palm` at [91, 41], offset [0, 0], layer `Instances`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [124, 33], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [124, 32], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [124, 34], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [124, 31], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [114, 33], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_tree_dead` at [96, 50], offset [0, 0], layer `Instances`. Shed snake bones — trail-edge continuation
- `spr_pebbles` at [97, 50], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_pebbles` at [92, 43], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_palm` at [79, 31], offset [0, 0], layer `Instances`. First green in the wash — trail-edge continuation
- `spr_palm` at [82, 34], offset [0, 0], layer `Instances`. First green in the wash — trail-edge continuation
- `spr_bush` at [78, 31], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_cactus_tall` at [23, 60], offset [0, 0], layer `Instances`. Sheltered cactus bend — trail-edge continuation
- `spr_tree_dead` at [54, 63], offset [0, 0], layer `Instances`. Washed-out stone bed — trail-edge continuation
- `spr_column_broken` at [57, 10], offset [0, 0], layer `Instances`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [60, 13], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [56, 10], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [10, 46], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [9, 46], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [8, 45], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [7, 45], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [3, 40], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [3, 39], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [10, 39], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [12, 39], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_cactus_tall` at [25, 61], offset [0, 0], layer `Instances`. Sheltered cactus bend — trail-edge continuation
- `spr_bush_dead` at [28, 64], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_tree_dead` at [69, 61], offset [0, 0], layer `Instances`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [100, 50], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush_dead` at [26, 63], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_palm` at [105, 5], offset [0, 0], layer `Instances`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [102, 8], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [108, 8], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [77, 29], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_tree_dead` at [60, 61], offset [0, 0], layer `Instances`. Washed-out stone bed — trail-edge continuation
- `spr_bush` at [88, 29], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_pebbles` at [65, 51], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush` at [99, 7], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [96, 10], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_tree_dead` at [54, 41], offset [0, 0], layer `Instances`. Canyon windbreak — trail-edge continuation
- `spr_bush` at [80, 38], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_tree_dead` at [90, 43], offset [0, 0], layer `Instances`. Shed snake bones — trail-edge continuation
- `spr_palm` at [93, 13], offset [0, 0], layer `Instances`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [90, 16], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_pebbles` at [52, 40], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_bush` at [100, 38], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_tree_dead` at [51, 52], offset [0, 0], layer `Instances`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [52, 52], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_cactus_tall` at [24, 55], offset [0, 0], layer `Instances`. Sheltered cactus bend — trail-edge continuation
- `spr_cactus_tall` at [32, 62], offset [0, 0], layer `Instances`. Sheltered cactus bend — trail-edge continuation
- `spr_pebbles` at [51, 63], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_column_broken` at [30, 11], offset [0, 0], layer `Instances`. Lookout foothill cairns — trail-edge continuation
- `spr_column_broken` at [30, 13], offset [0, 0], layer `Instances`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [55, 12], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_column_broken` at [27, 17], offset [0, 0], layer `Instances`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [51, 29], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker — trail-edge continuation
- `spr_tree_dead` at [51, 31], offset [0, 0], layer `Instances`. Canyon windbreak — trail-edge continuation
- `spr_loose_rocks` at [13, 39], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_bush_dead` at [11, 46], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_loose_rocks` at [55, 40], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker — trail-edge continuation
- `spr_tree_dead` at [51, 54], offset [0, 0], layer `Instances`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [70, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush` at [90, 31], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [75, 31], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [68, 43], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_tree_dead` at [87, 50], offset [0, 0], layer `Instances`. Shed snake bones — trail-edge continuation
- `spr_bush` at [119, 55], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_cactus_tall` at [34, 52], offset [0, 0], layer `Instances`. Sheltered cactus bend — trail-edge continuation
- `spr_pebbles` at [100, 57], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush` at [115, 7], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [92, 13], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_loose_rocks` at [51, 21], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [61, 17], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [27, 18], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_bush` at [90, 18], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_loose_rocks` at [25, 19], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_palm` at [89, 20], offset [0, 0], layer `Instances`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [124, 27], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [124, 26], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [124, 25], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [114, 27], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_loose_rocks` at [29, 31], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_bush` at [114, 29], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_loose_rocks` at [18, 30], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_bush` at [90, 30], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [90, 29], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [90, 35], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [99, 33], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_pebbles` at [50, 31], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_palm` at [80, 40], offset [0, 0], layer `Instances`. First green in the wash — trail-edge continuation
- `spr_pebbles` at [37, 45], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_pebbles` at [92, 42], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_pebbles` at [102, 45], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_pebbles` at [102, 44], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_pebbles` at [88, 51], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush` at [67, 50], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush_dead` at [32, 53], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_bush_dead` at [27, 61], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_bush_dead` at [26, 61], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_bush_dead` at [33, 54], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_pebbles` at [52, 54], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [50, 53], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [110, 57], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_pebbles` at [50, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [61, 63], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [38, 65], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_pebbles` at [98, 65], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush` at [93, 10], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [106, 8], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [101, 15], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_loose_rocks` at [47, 12], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [46, 12], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [53, 19], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_pebbles` at [67, 52], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [62, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_palm` at [103, 6], offset [0, 0], layer `Instances`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [93, 7], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [101, 14], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [114, 8], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [115, 9], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_column_broken` at [57, 12], offset [0, 0], layer `Instances`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [56, 11], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [60, 18], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_bush_dead` at [53, 12], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_bush_dead` at [52, 12], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_bush_dead` at [54, 12], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_bush_dead` at [51, 12], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_bush_dead` at [60, 14], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_bush_dead` at [52, 19], offset [0, 0], layer `Visual_Assets`. Watchman's abandoned perch — trail-edge continuation
- `spr_loose_rocks` at [28, 17], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_bush` at [120, 16], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [120, 15], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [121, 18], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [121, 17], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [111, 17], offset [0, 0], layer `Visual_Assets`. Hidden spring cairns — trail-edge continuation
- `spr_bush` at [90, 19], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [99, 21], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_loose_rocks` at [21, 23], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [30, 23], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [31, 23], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_bush` at [87, 23], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [84, 23], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_pebbles` at [87, 24], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [99, 23], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [99, 26], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_bush` at [99, 27], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_pebbles` at [90, 26], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_loose_rocks` at [68, 22], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker — trail-edge continuation
- `spr_loose_rocks` at [68, 23], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker — trail-edge continuation
- `spr_loose_rocks` at [31, 29], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [30, 30], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [36, 30], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [37, 23], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [39, 23], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [40, 23], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [41, 29], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_loose_rocks` at [19, 29], offset [0, 0], layer `Visual_Assets`. Lookout foothill cairns — trail-edge continuation
- `spr_palm` at [88, 27], offset [0, 0], layer `Instances`. Spring-bank palms — trail-edge continuation
- `spr_column_broken` at [17, 33], offset [0, 0], layer `Instances`. Lookout foothill cairns — trail-edge continuation
- `spr_pebbles` at [49, 30], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_bush` at [99, 36], offset [0, 0], layer `Visual_Assets`. Spring-bank palms — trail-edge continuation
- `spr_pebbles` at [49, 31], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_tree_dead` at [49, 39], offset [0, 0], layer `Instances`. Canyon windbreak — trail-edge continuation
- `spr_pebbles` at [49, 38], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_pebbles` at [48, 38], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_loose_rocks` at [53, 38], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker — trail-edge continuation
- `spr_loose_rocks` at [56, 39], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker — trail-edge continuation
- `spr_loose_rocks` at [52, 38], offset [0, 0], layer `Visual_Assets`. Split-cliff trail marker — trail-edge continuation
- `spr_bush` at [73, 31], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [80, 37], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [80, 39], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [71, 37], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [71, 38], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [114, 39], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_loose_rocks` at [3, 38], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_bush_dead` at [10, 45], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_bush_dead` at [9, 45], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_bush_dead` at [11, 45], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_bush_dead` at [3, 37], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_bush_dead` at [10, 38], offset [0, 0], layer `Visual_Assets`. Breached city baggage — trail-edge continuation
- `spr_pebbles` at [36, 44], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_pebbles` at [35, 44], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_pebbles` at [39, 44], offset [0, 0], layer `Visual_Assets`. Canyon windbreak — trail-edge continuation
- `spr_bush` at [71, 41], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [87, 42], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [89, 42], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush_dead` at [91, 43], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush_dead` at [91, 42], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush_dead` at [91, 40], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush_dead` at [90, 42], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush_dead` at [100, 44], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_bush` at [67, 44], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_bush` at [86, 50], offset [0, 0], layer `Visual_Assets`. First green in the wash — trail-edge continuation
- `spr_pebbles` at [89, 50], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_tree_dead` at [99, 52], offset [0, 0], layer `Instances`. Shed snake bones — trail-edge continuation
- `spr_bush` at [100, 51], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [99, 50], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [99, 51], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [106, 46], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [109, 48], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush` at [120, 51], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_bush_dead` at [12, 51], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_bush` at [120, 52], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_pebbles` at [55, 53], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [66, 52], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [35, 52], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_bush_dead` at [36, 52], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_bush_dead` at [24, 54], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_bush_dead` at [35, 58], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_pebbles` at [65, 52], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [70, 58], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush` at [112, 59], offset [0, 0], layer `Visual_Assets`. Lakeside resting place — trail-edge continuation
- `spr_pebbles` at [49, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [48, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [42, 59], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [49, 53], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [48, 53], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [51, 53], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [47, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [51, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [46, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [52, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [55, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [56, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [49, 54], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [61, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [71, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [72, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [73, 61], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [66, 54], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_bush_dead` at [41, 68], offset [0, 0], layer `Visual_Assets`. Sheltered cactus bend — trail-edge continuation
- `spr_pebbles` at [44, 68], offset [0, 0], layer `Visual_Assets`. Washed-out stone bed — trail-edge continuation
- `spr_pebbles` at [97, 66], offset [0, 0], layer `Visual_Assets`. Shed snake bones — trail-edge continuation
- `spr_tree_dead` at [77, 67], offset [0, 0], layer `Instances`. Shed snake bones — trail-edge continuation

Every required asset ID (including shared character/combat families) is enumerated for this scene in `scene_gameplay_specs.json` and `scene_asset_manifest.json`. These are incoming requirements; exact prop aliases and animation suffixes still need Claude's asset mapping. Weather suppression rectangles are explicit in this scene's sidecar entry.

`mus_desert`, `snd_checkpoint`, `snd_chest_open`, `snd_pickup`, `snd_save`, `snd_snake_hiss`, `snd_snake_lunge`, `snd_step_sand`, `snd_sword_hit`, `snd_sword_swing`, `snd_wind_loop`, `spr_boulder`, `spr_bush`, `spr_bush_dead`, `spr_cactus_small`, `spr_cactus_tall`, `spr_checkpoint_star`, `spr_chest_desert`, `spr_column_broken`, `spr_column_fallen`, `spr_dave_attack_down`, `spr_dave_attack_down_side`, `spr_dave_attack_side`, `spr_dave_attack_up`, `spr_dave_attack_up_side`, `spr_dave_idle_down`, `spr_dave_idle_down_side`, `spr_dave_idle_side`, `spr_dave_idle_up`, `spr_dave_idle_up_side`, `spr_dave_walk_down`, `spr_dave_walk_down_side`, `spr_dave_walk_side`, `spr_dave_walk_up`, `spr_dave_walk_up_side`, `spr_fx_hit`, `spr_fx_slash`, `spr_fx_sparkle`, `spr_healing_spring`, `spr_icon_ancient_coin`, `spr_icon_desert_rose`, `spr_icon_gold_coins`, `spr_icon_potion_health`, `spr_icon_wanderer_tunic`, `spr_loose_rocks`, `spr_mask_dave`, `spr_mask_medium`, `spr_mask_python`, `spr_obelisk`, `spr_palm`, `spr_pebbles`, `spr_python_coil`, `spr_python_defeat`, `spr_python_hurt`, `spr_python_lunge_down`, `spr_python_lunge_side`, `spr_python_lunge_up`, `spr_python_slither_down`, `spr_python_slither_side`, `spr_python_slither_up`, `spr_ruin_block`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `spr_skull`, `spr_supply_barrel`, `spr_tree_dead`, `spr_tree_desert`, `spr_tumbleweed`, `spr_undead_attack_down`, `spr_undead_attack_side`, `spr_undead_attack_up`, `spr_undead_defeat`, `spr_undead_hurt_down`, `spr_undead_idle_down`, `spr_undead_rise`, `spr_undead_walk_down`, `spr_undead_walk_side`, `spr_undead_walk_up`, `spr_wagon_wreck`, `spr_water_barrel`, `tex_cliff_face`, `tex_grass`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `tex_rock_top`, `tex_sand_dark`, `tex_sand_light`, `tex_water`, `tex_wet_sand`, `ts_stairs`.
