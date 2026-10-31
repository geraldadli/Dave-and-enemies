# Caravan Basin - expanding scene design

[Current chapter structure](DESERT_CHAPTER.md). Stable scene ID `sc_caravan_basin`; technical GameMaker resource `rm_sc_caravan_basin`. Starting extent **144 x 88 tiles** (9216 x 5632 px). An expansive travel basin: caravan wreck, cactus routes and bonefield lead to two usable chasm crossings, quiet ruins and a panoramic ascent.

No place below is a separate loaded scene. All place boundaries and batch edges are metadata only.

## Landscape overview

Reduced grid: one character summarizes 4 x 4 tiles; row labels are global tile rows. Full exact grid: `design/desert/scenes/rm_sc_caravan_basin.json`. Legend and coordinate rules are in the chapter document.

```text
00 #####################CC#############
04 #####################CC#############
08 #####################CC##########p##
12 ##########p##########CC#######c.p.__
16 ######.p...ec########CC#######.p.ep_
20 ######,,pe,.#########CC#######.p,..a
24 #####p,cp.,.p##.,ppppxx######p__.###
28 #####p_.##.__.,,.pcp,xx###MM###^^^##
32 ###.p.,####....,pp..,CC###M...p..###
36 _..pe.,####.pp.eppe.pCC###.pp._p.###
40 a.p.,,,.p....,,,,,,,.CC###.pS....###
44 #.__.pp...,pp...#e.,,==,,,,,.p..####
48 ##,pc,..eppc,,pp##pc.==..p.p..e.####
52 ##.p.....p,pp,####._pCCp__c,....####
56 ####p#####...,MMMMMM.CC#pp.,c,p#####
60 ##########.ep,__||,.#CC.e.p_p,p#####
64 ##########...,p~||p,,==p..p,p#######
68 ###########pc.pp||p,.==p....########
72 ###########p.;;,,c_,.CC#c###########
76 #############....pp.#CC#############
80 #####################CC#############
84 #####################CC#############
```

Scene transitions:

| Border | Opening rows | Arrival here | Destination scene / arrival |
|---|---|---|---|
| W | [38, 42] | [2, 40], pixels [160, 2592] | `sc_desert_frontier` / [125, 40] |
| E | [18, 22] | [141, 20], pixels [9056, 1312] | `sc_royal_expanse` / [2, 20] |

Preferred walking route: [2, 40] -> [17, 40] -> [17, 43] -> [42, 43] -> [42, 49] -> [52, 49] -> [52, 41] -> [78, 41] -> [78, 46] -> [96, 46] -> [113, 46] -> [113, 41] -> [128, 41] -> [128, 33] -> [128, 20] -> [141, 20]. This is a route suggestion, not a compulsory chain of place triggers.

Exploration circuits:

- **Northern camp circuit**: Detour past the bandit camp, then return on the bonefield's west approach. Waypoints: [25, 43] -> [25, 22] -> [42, 22] -> [42, 30] -> [62, 30] -> [62, 41].
- **Twin crossing circuit**: Use the southern bridge and eastern bank to return via the main bridge; permanent geography, no switch or loading. Waypoints: [52, 49] -> [54, 49] -> [54, 74] -> [78, 74] -> [78, 67] -> [99, 67] -> [109, 67] -> [109, 46] -> [113, 46].
- **Cistern rim and catwalk**: Cross the water by catwalk or follow the outer paving; reconnect with the southern basin route. Waypoints: [66, 74] -> [67, 74] -> [67, 60] -> [76, 60] -> [76, 67] -> [78, 67].
- **Stranded Supply Wagon trail**: Find stranded supply wagon and its supplies; return by another approach. Waypoints: [10, 40] -> [10, 52] -> [22, 52] -> [22, 43].
- **Cactus Shelter trail**: Find cactus shelter and its supplies; return by another approach. Waypoints: [42, 49] -> [42, 54] -> [52, 54] -> [52, 49].
- **Broken Span Overlook trail**: Find broken span overlook and its supplies; return by another approach. Waypoints: [62, 30] -> [62, 27] -> [80, 27] -> [80, 41] -> [78, 41].
- **Well Keeper's Yard trail**: Find well keeper's yard and its supplies; return by another approach. Waypoints: [109, 54] -> [118, 54] -> [118, 62] -> [109, 62].

Elevation and structures:

- Great Stairs upper shelf z1: [117,11..142,29], bounded on west/north/south; only stairs and east scene pass connect it. Rest of basin z0. Cistern is a flat flooded foundation, not an overlapping lower floor.
- `broken_bridge` [84, 26, 89, 30]: Broken northern span is fully blocked; no repair, jump or key objective.
- `bridge_ew` [84, 44, 89, 48]: Five-wide main crossing; clear three-cell banks at both ends.
- `bridge_ew` [84, 65, 89, 69]: Five-wide southern crossing makes a permanent regional loop, not a transition.
- `bridge_ns` [66, 62, 68, 68]: Three-wide cistern catwalk; both banks and the outer paving form a smaller loop within the basin.
- `stairs` [126, 30, 132, 31]: Seven-wide Great Desert Stairs; upper shelf connects directly to the next scene at the same elevation.

## Build this scene by expansion

1. **Caravan and grove**: Lay out shared travel floor, distinct combat pockets and the northern camp circuit. Places: `place_ruined_caravan`, `place_cactus_flats`, `place_bandit_cache`.
2. **Bridge basin expansion**: Add both intact bridges, broken landmark, southern return and cistern rim/catwalk. Places: `place_bonefield`, `place_broken_bridge`, `place_buried_cistern`.
3. **Ruins and ascent**: Complete quiet ruins, checkpoint, broad climb, upper treasure and east transition. Places: `place_forgotten_ruins`, `place_great_desert_stairs`.

## Places and readable local grids

Each crop below uses global `[x,y]` coordinates, one character per tile. It is an inspection window into the shared scene, not an enclosed map or scene boundary. The crop's x origin is stated; row labels remain global. Objects outside a crop are still present in the same scene.

### Well Keeper's Yard

`place_well_keeper`; anchor [115, 61]; inspection extent [112, 57, 119, 63]; x origin **112**. A close, recognizable little destination with an optional persistent supply cache.

```text
57 p.....,,
58 .,,,,,,,
59 .,,c,,,,
60 p,,,,,,,
61 _....,,,
62 __,,,,,,
63 _,,,,,,.
```

### Broken Span Overlook

`place_bridge_watch`; anchor [74, 31]; inspection extent [71, 27, 78, 33]; x origin **71**. A close, recognizable little destination with an optional persistent supply cache.

```text
27 ,,,,,,,,
28 ._.__,,,
29 ___c___.
30 _.__.__.
31 ______p.
32 .__.__..
33 ........
```

### Cactus Shelter

`place_grove_cache`; anchor [47, 53]; inspection extent [44, 49, 51, 55]; x origin **44**. A close, recognizable little destination with an optional persistent supply cache.

```text
49 ,,,,,,,,
50 .....,,,
51 ...c..,,
52 .p,,,,p,
53 ,,,,,,,,
54 ,,,,,,,,
55 .......,
```

### Stranded Supply Wagon

`place_spilled_supplies`; anchor [16, 51]; inspection extent [13, 47, 20, 53]; x origin **13**. A close, recognizable little destination with an optional persistent supply cache.

```text
47 __.....,
48 p,,,,,.,
49 .,,c,,p,
50 p,,,,,,.
51 ,,,,,,,,
52 ,,,,,,,,
53 ,,......
```

### Ruined Caravan

`place_ruined_caravan`; anchor [17, 43]; inspection extent [6, 27, 33, 50]; x origin **6**. Wreck and scattered cargo can be approached from the trail or northern loop.

```text
27 ###############..,__.__...##
28 ###############.._,____...##
29 ##############...____.___..#
30 ##############...__,____..##
31 ##############..p,____..####
32 ##############...,,,....####
33 ######......p....,,,....####
34 ######...........,,,...#####
35 ######............,,,..#####
36 ######............,,,..#####
37 ..................,,,..#####
38 ......p...........,,,..#####
39 ...,,,,,,,,,e.....,,,..####.
40 ,,,,,,,,,,,,,.....,,,.......
41 ,,,,,,...,,,,.....,,,.......
42 ...,,,...,,,,,,,,,,,,.......
43 ..p.,,...,,,,,,,,,,,,,,,,,,,
44 ...___,_..,,,,,,,,,,,,,,,,,,
45 ..__,____......,,...........
46 ._.____.__....p,,..##.......
47 ..___,___.....,,,..##p......
48 ....___p,,,,,.,,,..##.......
49 ...,,,..,,c,,p,,,...#......e
50 ...,,,.p,,,,,,.,,...#.......
```

### Cactus Flats

`place_cactus_flats`; anchor [42, 49]; inspection extent [30, 39, 54, 71]; x origin **30**. Loose cactus groves frame wide paths; the cache lies north, the python hollow south.

```text
39 ###.....#......#........p
40 .....p..........##....,,,
41 .................#...,,,,
42 ...........,,....#...,,,,
43 ,,,,,,,,,,,,,....#...,,..
44 ,,,,,,,,...,,....#...,,..
45 ...........,,.......,,,..
46 ...........,,..p...p.,,,.
47 ...........,,........,,,.
48 ..........p,,,,,,,,,,,,,,
49 ...e.......,,,,,,,,,,,,,,
50 ...........,,,.....,,,,,,
51 .........p.,,,...c..,,,,,
52 ...........,,..p,,,,p,,,,
53 ...........,,,,,,,,,,,,,,
54 ...........,,,,,,,,,,,,,,
55 .........p..,,.......,,,,
56 #######................,,
57 #######...............,,,
58 #########.............,,,
59 #########.............,,,
60 #########.............,,,
61 #########.............,,,
62 #########......e.....p,,,
63 #########.............,,,
64 #########.............,,,
65 #########..............,,
66 #########..............,,
67 #########..............,,
68 #########..............,,
69 #############........p.,,
70 ##############.p..c....,,
71 ##############..........,
```

### Bonefield

`place_bonefield`; anchor [67, 41]; inspection extent [55, 31, 81, 57]; x origin **55**. Melee and archer groups occupy separate open pockets around a visible eastward route.

```text
31 ......,,,..#####______p..,,
32 ......,,,..##..p.__.__...,,
33 ......,,,.p..............,,
34 ......,,,....p...........,,
35 ......,,,................,,
36 ......,,,................,,
37 .......,,....p...........,,
38 .......,,..........e.....,,
39 ......e,,...p............,.
40 ,,,,,,,,,.........,,,,,,.,.
41 ,,,,,,,,,,,,,,,,,,,,,,,,,,.
42 ,,,,,,,,,,,,,,,,,,,,..,,...
43 .........,,,,.........,,...
44 ...............e......,,...
45 ......................,,,,,
46 .........####.........,,,,,
47 .........##########........
48 ,.....p.###########.p......
49 ,..p..##############.......
50 ,..#################.......
51 ,..################...c....
52 ,.################....____.
53 ,.################..____.__
54 ,.###############..___.____
55 ,.################...____._
56 ..##########.........__.__.
57 ..MMMMMMMMMMMMMMMMMMMMMMM..
```

### Broken Bridge

`place_broken_bridge`; anchor [87, 46]; inspection extent [80, 23, 95, 72]; x origin **80**. The broken span points south toward a usable bridge; farther south another crossing rewards exploration.

```text
23 ####CCCCCC######
24 ...#CCCCCC######
25 p...CCCCCC######
26 ,...xxxxxx######
27 ,,..xxxxxx######
28 ,,..xxxxxx######
29 ,,..xxxxxx######
30 ,,..xxxxxx######
31 ,,..CCCCCC######
32 ,,..CCCCCC######
33 ,,..CCCCCC######
34 ,,..CCCCCC######
35 ,,..CCCCCC######
36 ,,..CCCCCC######
37 ,,..CCCCCC######
38 ,,..CCCCCC######
39 ,..pCCCCCC######
40 ,...CCCCCC######
41 ,...CCCCCC######
42 ....CCCCCC######
43 ....CCCCCC######
44 ....======......
45 ,,,,======..,,,,
46 ,,,,======,,,,,,
47 ....======,,,,,,
48 ....======......
49 ....CCCCCC.##...
50 ..##CCCCCC####..
51 ...#CCCCCC####..
52 _...CCCCCC###.._
53 __p.CCCCCC####.p
54 __..CCCCCC####..
55 ._..CCCCCC#####.
56 _...CCCCCC######
57 ...#CCCCCC######
58 .###CCCCCC###...
59 ..##CCCCCC###...
60 ..##CCCCCC###...
61 ..##CCCCCC###...
62 ..##CCCCCC###...
63 ..##CCCCCC##....
64 ..##CCCCCC...p..
65 ..,,======......
66 ,,,,======,,,...
67 ,,,,======,,,,,,
68 ,...======,,,,,,
69 ....======......
70 ....CCCCCC...p..
71 ..##CCCCCC......
72 ..##CCCCCC#####.
```

### Forgotten Ruins

`place_forgotten_ruins`; anchor [113, 41]; inspection extent [103, 27, 123, 55]; x origin **103**. Quiet open ruins and a save star provide an eastern anchor reached from either bridge.

```text
27 ###############....__
28 ##MMMMMMMMMM####.....
29 ##MMMMMMMMMM######...
30 ##MM#################
31 ##MM#################
32 ##MM############MM###
33 ..MM............MM###
34 ..MM............MM###
35 ..MM............MM..p
36 ..MM............MM...
37 .......p...........__
38 ...........p.....____
39 ...............,___._
40 ..........,,,,,,,,___
41 .........,S,,,,...__,
42 ......p..,,..........
43 ........,,,..........
44 .....,..,,,.....p....
45 ,,,,,,,,,,,..........
46 ,,,,,,,,,,,..........
47 ,,,..,,.,............
48 .....,,,.............
49 .....,,,p...#.....e..
50 .....,,,..###........
51 ......,,.............
52 _.....,,.............
53 ..c...,,,,...........
54 ......,,,,,,,,,,.....
55 ......,,...,,,,,,.###
```

### Great Desert Stairs

`place_great_desert_stairs`; anchor [129, 30]; inspection extent [115, 9, 142, 54]; x origin **115**. Broad ascent to a walkable upper shelf; looking back west rewards treasure hunting.

```text
09 ############################
10 ############################
11 ###################.p.......
12 ####.....#########....____..
13 ####...........p....____.__.
14 ####..c............___.____.
15 ####.................____._.
16 ####.................__.__..
17 ####.................p......
18 ####................,...____
19 #########p...,,,,e,,,,,,____
20 #########...,,,,,,,,,.,,__a_
21 ######...p..,,,,........____
22 ####........,,,.........____
23 ###...___._.,,..............
24 ###..__.____,,........##....
25 ##..p.____.__,........######
26 ###..___.___,,...###########
27 ###....____,,,...###########
28 ####.......,,.....##########
29 ######.....,,,....##########
30 ###########^^^^^^^##########
31 ###########^^^^^^^##########
32 ####MM####..,,....##########
33 ....MM####..,,....##########
34 ....MM####..,,..############
35 ....MM..p...,,..############
36 ....MM.....p,,..############
37 .......____.,,..############
38 .....____.__,,..############
39 ...,___.____.,..############
40 ,,,,,,____,_.,...###########
41 ,,,...__,__,,,...###########
42 .................###########
43 ................############
44 ....p...........############
45 ............################
46 ............################
47 ............################
48 ............################
49 #.....e.....################
50 #...........################
51 ............################
52 ............################
53 ............################
54 ,,,,........################
```

### Bandit Cache

`place_bandit_cache`; anchor [42, 20]; inspection extent [29, 10, 59, 29]; x origin **29**. Bandit Cache is a northern camp reached by a loop, with two routes back into the basin.

```text
10 ###############################
11 ###############################
12 ###############################
13 ###############################
14 ######......p......############
15 ######................#########
16 .p.###................#########
17 .....#..............c.#########
18 ...............e......#########
19 ......................#########
20 ,,,,p,p,..............#########
21 ,,,,,,,,,,e,,,........#########
22 ,,,,,,,,,,,,,,,....############
23 .........,,,,,,....############
24 ............,,,....###########.
25 .....p.......,,....p..########.
26 c..###.......,,.......########.
27 ...########..,,...____########.
28 ...########..,,.____.__........
29 __..#######..,,___.____,,,,,,,,
```

### Buried Cistern

`place_buried_cistern`; anchor [67, 70]; inspection extent [56, 56, 80, 78]; x origin **56**. Buried Cistern is an exposed flooded foundation on the southern bridge circuit, continuously outdoors.

```text
56 .##########.........__.__
57 .MMMMMMMMMMMMMMMMMMMMMMM.
58 .MMMMMMMMMMMMMMMMMMMMMMM.
59 .________.........,,,.._.
60 .________..,,,,,,,,,,,._.
61 .________..,,,,,,,,,,.._.
62 ._____~~~~|||~~~~~.,,.._.
63 ._____~~~~|||~~~~~.,,.._.
64 ._____~~~~|||~~~~~.,,.._.
65 ._p___~~~~|||~~~~~.,,,,..
66 ._____~~~~|||~~~~~p,,,,,,
67 ._____~~~~|||~~~~~.,,,,,,
68 ._____~~~~|||~~~~~p.,,,,,
69 .p_______.,,..__p_..,,,..
70 .___p____.,,..________,..
71 ;________.,,..________,..
72 ;;;;;.....,,..,c____,___.
73 ;;;;;;...,,,,,,,__,____,.
74 ;;;;;,,,,,,,,,,,,____,,,.
75 ;;;;,,,,,,,,,.......,,,..
76 .........................
77 .____________p___p______.
78 .........................
```

## Gameplay placement

Encounters (IDs retained across the redesign):

- `rm_d07_ruined_caravan:g1`: pad/leash [13, 34, 23, 44], max 1 active. First bandit in a clear clearing beside the wreck. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d07_ruined_caravan:g1:e1`: `bandit` at [18, 39].
- `rm_d07_ruined_caravan:g2`: pad/leash [28, 44, 38, 54], max 1 active. A second fast attacker near the cactus trail; groups stay separated. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d07_ruined_caravan:g2:e1`: `bandit` at [33, 49].
- `rm_d08_cactus_flats:g1`: pad/leash [40, 57, 50, 67], max 1 active. Elective python pocket on the south side of the grove. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d08_cactus_flats:g1:e1`: `python` at [45, 62].
- `rm_d09_bonefield:g1`: pad/leash [56, 34, 66, 44], max 1 active. Known warrior before the archer pocket. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d09_bonefield:g1:e1`: `skeleton_warrior` at [61, 39].
- `rm_d09_bonefield:g2`: pad/leash [69, 33, 79, 45], max 2 active. An archer and warrior combine with broad flanking ground; no bridge combat. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d09_bonefield:g2:e1`: `skeleton_archer` at [74, 38].
  - `rm_d09_bonefield:g2:e2`: `skeleton_warrior` at [70, 44].
- `rm_d10_broken_bridge:g1`: pad/leash [94, 59, 104, 69], max 1 active. Optional bat encounter on the far southern bank, outside the crossing landings. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d10_broken_bridge:g1:e1`: `bat` at [98, 63].
- `rm_d12_great_desert_stairs:g1`: pad/leash [117, 45, 125, 53], max 1 active. Elective lower-terrace warrior; the save approach and stairs are calm. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d12_great_desert_stairs:g1:e1`: `skeleton_warrior` at [121, 49].
- `rm_d12_great_desert_stairs:g2`: pad/leash [125, 14, 135, 24], max 1 active. Upper-shelf archer, with a broad landing and routes around its pad. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d12_great_desert_stairs:g2:e1`: `skeleton_archer` at [132, 19].
- `rm_o3_bandit_cache:g1`: pad/leash [36, 15, 46, 25], max 2 active. Optional early caster plus fast melee; open camp, no ambush or exit lock. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_o3_bandit_cache:g1:e1`: `bandit` at [39, 21].
  - `rm_o3_bandit_cache:g1:e2`: `bandit_caster` at [44, 18].

Chests (all unlocked, no ordinary kill lock; overflow stays pending):

- `rm_sc_caravan_basin:c1` at [29, 26]: 1 x `bandit_scimitar`. Approach [29, 28], interaction [29, 27]. A weapon sidegrade in abandoned cargo; no unique movement or key function. Legacy ID `rm_d07_ruined_caravan:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c2` at [48, 70]: 2 x `potion_health`. Approach [48, 72], interaction [48, 71]. Recovery for a careful reader of the cactus gaps. Legacy ID `rm_d08_cactus_flats:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c3` at [77, 51]: 2 x `ancient_coin`, 1 x `potion_health`. Approach [77, 53], interaction [77, 52]. A southern recovery loop after the hardest early group; no mandatory kill lock. Legacy ID `rm_d09_bonefield:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c4` at [98, 72]: 1 x `potion_greater`. Approach [98, 74], interaction [98, 73]. A safe eastern-bank pocket for players who explore after the crossing. Legacy ID `rm_d10_broken_bridge:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c5` at [105, 53]: 2 x `potion_health`. Approach [105, 55], interaction [105, 54]. A safe stock-up before the stairs; tucked behind a broken wall end, never hidden by opaque art. Legacy ID `rm_d11_forgotten_ruins:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c6` at [121, 14]: 2 x `ancient_coin`. Approach [121, 16], interaction [121, 15]. After ascending, the east exit is clear; looking west along the upper shelf finds a worthwhile detour. Legacy ID `rm_d12_great_desert_stairs:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c7` at [49, 17]: 1 x `iron_tunic`, 1 x `potion_greater`. Approach [49, 19], interaction [49, 18]. Clear optional equipment improvement; never part of the chapter's required power budget. Legacy ID `rm_o3_bandit_cache:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c8` at [71, 72]: 1 x `golden_scarab`, 1 x `potion_greater`. Approach [71, 74], interaction [71, 73]. A valuable plus recovery reached by either the outer rim or the central catwalk. Legacy ID `rm_o4_buried_cistern:c1` is mapped explicitly.
- `rm_sc_caravan_basin:c9` at [16, 49]: 1 x `potion_health`. Approach [16, 51], interaction [16, 50]. Optional discovery at Stranded Supply Wagon; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_caravan_basin:c10` at [47, 51]: 8 x `gold_coins`. Approach [47, 53], interaction [47, 52]. Optional discovery at Cactus Shelter; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_caravan_basin:c11` at [74, 29]: 1 x `desert_rose`. Approach [74, 31], interaction [74, 30]. Optional discovery at Broken Span Overlook; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_caravan_basin:c12` at [115, 59]: 1 x `potion_health`, 3 x `gold_coins`. Approach [115, 61], interaction [115, 60]. Optional discovery at Well Keeper's Yard; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.

Checkpoint and scripts:

- `sc_caravan_basin:checkpoint` at/respawn [113, 41]; clear 3 x 3 [112, 40, 114, 42]; peaceful district [103, 33, 119, 44]. E opens exactly 3 save slots; heal on successful save; snapshot all state together.

Solid props (terrain/chests handled separately):

- `wagon_wreck` at [22, 31]; centred base [160, 40] px, conservative blocked cells [21, 31, 23, 31].
- `cactus_tall` at [35, 40]; centred base [24, 16] px, conservative blocked cells [35, 40, 35, 40].
- `cactus_tall` at [48, 37]; centred base [24, 16] px, conservative blocked cells [48, 37, 48, 37].
- `cactus_tall` at [39, 55]; centred base [24, 16] px, conservative blocked cells [39, 55, 39, 55].
- `cactus_tall` at [51, 69]; centred base [24, 16] px, conservative blocked cells [51, 69, 51, 69].
- `cactus_tall` at [16, 56]; centred base [24, 16] px, conservative blocked cells [16, 56, 16, 56].
- `wagon_wreck` at [13, 48]; centred base [160, 40] px, conservative blocked cells [12, 48, 14, 48].
- `water_barrel` at [13, 50]; centred base [38, 20] px, conservative blocked cells [13, 50, 13, 50].
- `supply_barrel` at [19, 49]; centred base [28, 16] px, conservative blocked cells [19, 49, 19, 49].
- `cactus_small` at [50, 52]; centred base [16, 12] px, conservative blocked cells [50, 52, 50, 52].
- `supply_barrel` at [45, 52]; centred base [28, 16] px, conservative blocked cells [45, 52, 45, 52].
- `column_broken` at [70, 30]; centred base [28, 18] px, conservative blocked cells [70, 30, 70, 30].
- `column_fallen` at [77, 31]; centred base [36, 20] px, conservative blocked cells [77, 31, 77, 31].
- `supply_barrel` at [70, 32]; centred base [28, 16] px, conservative blocked cells [70, 32, 70, 32].
- `water_barrel` at [68, 34]; centred base [38, 20] px, conservative blocked cells [68, 34, 68, 34].
- `wagon_wreck` at [112, 57]; centred base [160, 40] px, conservative blocked cells [111, 57, 113, 57].
- `water_barrel` at [112, 60]; centred base [38, 20] px, conservative blocked cells [112, 60, 112, 60].
- `supply_barrel` at [120, 59]; centred base [28, 16] px, conservative blocked cells [120, 59, 120, 59].
- `supply_barrel` at [120, 61]; centred base [28, 16] px, conservative blocked cells [120, 61, 120, 61].
- `supply_barrel` at [8, 43]; centred base [28, 16] px, conservative blocked cells [8, 43, 8, 43].
- `supply_barrel` at [23, 26]; centred base [28, 16] px, conservative blocked cells [23, 26, 23, 26].
- `cactus_tall` at [33, 20]; centred base [24, 16] px, conservative blocked cells [33, 20, 33, 20].
- `cactus_small` at [30, 16]; centred base [16, 12] px, conservative blocked cells [30, 16, 30, 16].
- `wagon_wreck` at [48, 25]; centred base [160, 40] px, conservative blocked cells [47, 25, 49, 25].
- `cactus_tall` at [39, 51]; centred base [24, 16] px, conservative blocked cells [39, 51, 39, 51].
- `cactus_small` at [40, 48]; centred base [16, 12] px, conservative blocked cells [40, 48, 40, 48].
- `tree_dead` at [45, 70]; centred base [24, 16] px, conservative blocked cells [45, 70, 45, 70].
- `column_fallen` at [46, 72]; centred base [36, 20] px, conservative blocked cells [46, 72, 46, 72].
- `tree_dead` at [58, 49]; centred base [24, 16] px, conservative blocked cells [58, 49, 58, 49].
- `column_fallen` at [61, 48]; centred base [36, 20] px, conservative blocked cells [61, 48, 61, 48].
- `tree_dead` at [76, 25]; centred base [24, 16] px, conservative blocked cells [76, 25, 76, 25].
- `column_fallen` at [80, 25]; centred base [36, 20] px, conservative blocked cells [80, 25, 80, 25].
- `supply_barrel` at [82, 53]; centred base [28, 16] px, conservative blocked cells [82, 53, 82, 53].
- `palm` at [57, 69]; centred base [24, 14] px, conservative blocked cells [57, 69, 57, 69].
- `water_barrel` at [60, 70]; centred base [38, 20] px, conservative blocked cells [60, 70, 60, 70].
- `column_broken` at [74, 68]; centred base [28, 18] px, conservative blocked cells [74, 68, 74, 68].
- `ruin_block` at [72, 69]; centred base [48, 24] px, conservative blocked cells [72, 69, 72, 69].
- `column_broken` at [99, 56]; centred base [28, 18] px, conservative blocked cells [99, 56, 99, 56].
- `ruin_block` at [95, 53]; centred base [48, 24] px, conservative blocked cells [95, 53, 95, 53].
- `column_broken` at [105, 62]; centred base [28, 18] px, conservative blocked cells [105, 62, 105, 62].
- `ruin_block` at [106, 65]; centred base [48, 24] px, conservative blocked cells [106, 65, 106, 65].
- `column_whole` at [123, 35]; centred base [28, 18] px, conservative blocked cells [123, 35, 123, 35].
- `column_broken` at [126, 36]; centred base [28, 18] px, conservative blocked cells [126, 36, 126, 36].
- `column_whole` at [119, 25]; centred base [28, 18] px, conservative blocked cells [119, 25, 119, 25].
- `column_broken` at [124, 21]; centred base [28, 18] px, conservative blocked cells [124, 21, 124, 21].
- `column_broken` at [135, 11]; centred base [28, 18] px, conservative blocked cells [135, 11, 135, 11].
- `column_broken` at [93, 70]; centred base [28, 18] px, conservative blocked cells [93, 70, 93, 70].
- `column_broken` at [101, 49]; centred base [28, 18] px, conservative blocked cells [101, 49, 101, 49].
- `ruin_block` at [103, 58]; centred base [48, 24] px, conservative blocked cells [103, 58, 103, 58].
- `column_broken` at [69, 77]; centred base [28, 18] px, conservative blocked cells [69, 77, 69, 77].
- `ruin_block` at [73, 77]; centred base [48, 24] px, conservative blocked cells [73, 77, 73, 77].
- `column_broken` at [20, 46]; centred base [28, 18] px, conservative blocked cells [20, 46, 20, 46].
- `ruin_block` at [14, 55]; centred base [48, 24] px, conservative blocked cells [14, 55, 14, 55].
- `column_broken` at [45, 46]; centred base [28, 18] px, conservative blocked cells [45, 46, 45, 46].
- `ruin_block` at [49, 46]; centred base [48, 24] px, conservative blocked cells [49, 46, 49, 46].
- `column_broken` at [72, 24]; centred base [28, 18] px, conservative blocked cells [72, 24, 72, 24].
- `ruin_block` at [70, 25]; centred base [48, 24] px, conservative blocked cells [70, 25, 70, 25].
- `column_broken` at [120, 57]; centred base [28, 18] px, conservative blocked cells [120, 57, 120, 57].
- `ruin_block` at [115, 65]; centred base [48, 24] px, conservative blocked cells [115, 65, 115, 65].
- `tree_dead` at [18, 33]; centred base [24, 16] px, conservative blocked cells [18, 33, 18, 33].
- `column_fallen` at [12, 38]; centred base [36, 20] px, conservative blocked cells [12, 38, 12, 38].
- `column_fallen` at [27, 47]; centred base [36, 20] px, conservative blocked cells [27, 47, 27, 47].
- `column_fallen` at [51, 62]; centred base [36, 20] px, conservative blocked cells [51, 62, 51, 62].
- `tree_dead` at [54, 39]; centred base [24, 16] px, conservative blocked cells [54, 39, 54, 39].
- `column_fallen` at [67, 39]; centred base [36, 20] px, conservative blocked cells [67, 39, 67, 39].
- `tree_dead` at [83, 39]; centred base [24, 16] px, conservative blocked cells [83, 39, 83, 39].
- `column_fallen` at [68, 37]; centred base [36, 20] px, conservative blocked cells [68, 37, 68, 37].
- `tree_dead` at [99, 58]; centred base [24, 16] px, conservative blocked cells [99, 58, 99, 58].
- `column_fallen` at [93, 64]; centred base [36, 20] px, conservative blocked cells [93, 64, 93, 64].
- `column_fallen` at [119, 44]; centred base [36, 20] px, conservative blocked cells [119, 44, 119, 44].
- `tree_dead` at [130, 13]; centred base [24, 16] px, conservative blocked cells [130, 13, 130, 13].
- `column_fallen` at [124, 19]; centred base [36, 20] px, conservative blocked cells [124, 19, 124, 19].
- `tree_dead` at [41, 14]; centred base [24, 16] px, conservative blocked cells [41, 14, 41, 14].
- `column_fallen` at [35, 20]; centred base [36, 20] px, conservative blocked cells [35, 20, 35, 20].
- `column_broken` at [109, 42]; centred base [28, 18] px, conservative blocked cells [109, 42, 109, 42].
- `palm` at [58, 65]; centred base [24, 14] px, conservative blocked cells [58, 65, 58, 65].
- `column_whole` at [110, 37]; centred base [28, 18] px, conservative blocked cells [110, 37, 110, 37].
- `column_broken` at [74, 66]; centred base [28, 18] px, conservative blocked cells [74, 66, 74, 66].
- `column_whole` at [114, 38]; centred base [28, 18] px, conservative blocked cells [114, 38, 114, 38].
- `column_whole` at [136, 17]; centred base [28, 18] px, conservative blocked cells [136, 17, 136, 17].
- `wagon_wreck` at [34, 25]; centred base [160, 40] px, conservative blocked cells [33, 25, 35, 25].
- `wagon_wreck` at [65, 33]; centred base [160, 40] px, conservative blocked cells [64, 33, 66, 33].
- `wagon_wreck` at [75, 48]; centred base [160, 40] px, conservative blocked cells [74, 48, 76, 48].
- `column_broken` at [111, 49]; centred base [28, 18] px, conservative blocked cells [111, 49, 111, 49].

## Decoration and required assets

Decoration is separate, noncolliding art. Tall landmarks sit on existing blocked terrain unless their real base is listed as a solid prop above.

- `spr_ruin_block` at [32, 34], offset [0, 0], layer `Instances`. Caravan stone cargo rests on blocked rock.
- `spr_obelisk` at [110, 29], offset [0, 0], layer `Instances`. Ruins inscription is on existing masonry, not a new blocker.
- `spr_tree_dead` at [25, 66], offset [0, 0], layer `Instances`. A southern silhouette points toward the cistern circuit.
- `spr_skull` at [63, 49], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_pebbles` at [76, 75], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_bush_dead` at [100, 51], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_loose_rocks` at [14, 51], offset [0, 0], layer `Visual_Assets`. Stranded Supply Wagon — composed discovery
- `spr_bush_dead` at [20, 51], offset [0, 0], layer `Visual_Assets`. Stranded Supply Wagon — composed discovery
- `spr_bush_dead` at [50, 53], offset [0, 0], layer `Visual_Assets`. Cactus Shelter — composed discovery
- `spr_pebbles` at [45, 55], offset [0, 0], layer `Visual_Assets`. Cactus Shelter — composed discovery
- `spr_loose_rocks` at [51, 48], offset [0, 0], layer `Visual_Assets`. Cactus Shelter — composed discovery
- `spr_loose_rocks` at [72, 32], offset [0, 0], layer `Visual_Assets`. Broken Span Overlook — composed discovery
- `spr_pebbles` at [78, 26], offset [0, 0], layer `Visual_Assets`. Broken Span Overlook — composed discovery
- `spr_loose_rocks` at [77, 32], offset [0, 0], layer `Visual_Assets`. Broken Span Overlook — composed discovery
- `spr_loose_rocks` at [113, 61], offset [0, 0], layer `Visual_Assets`. Well Keeper's Yard — composed discovery
- `spr_bush_dead` at [119, 62], offset [0, 0], layer `Visual_Assets`. Well Keeper's Yard — composed discovery
- `spr_wagon_wreck` at [4, 46], offset [0, 0], layer `Instances`. Spilled caravan cargo
- `spr_loose_rocks` at [8, 48], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo
- `spr_bush_dead` at [12, 43], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo
- `spr_wagon_wreck` at [31, 31], offset [0, 0], layer `Instances`. Broken axle pull-off
- `spr_loose_rocks` at [23, 31], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off
- `spr_bush_dead` at [29, 30], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off
- `spr_bush_dead` at [32, 18], offset [0, 0], layer `Visual_Assets`. Camp approach windbreak
- `spr_pebbles` at [28, 23], offset [0, 0], layer `Visual_Assets`. Camp approach windbreak
- `spr_supply_barrel` at [51, 26], offset [0, 0], layer `Instances`. Bandit lookout remains
- `spr_loose_rocks` at [51, 31], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains
- `spr_bush_dead` at [51, 28], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains
- `spr_bush_dead` at [40, 53], offset [0, 0], layer `Visual_Assets`. Cactus grove fork
- `spr_pebbles` at [40, 50], offset [0, 0], layer `Visual_Assets`. Cactus grove fork
- `spr_pebbles` at [52, 67], offset [0, 0], layer `Visual_Assets`. Snake-skin hollow
- `spr_loose_rocks` at [52, 70], offset [0, 0], layer `Visual_Assets`. Snake-skin hollow
- `spr_pebbles` at [60, 48], offset [0, 0], layer `Visual_Assets`. Bonefield waystones
- `spr_loose_rocks` at [55, 46], offset [0, 0], layer `Visual_Assets`. Bonefield waystones
- `spr_pebbles` at [79, 25], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span
- `spr_loose_rocks` at [76, 26], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span
- `spr_wagon_wreck` at [78, 58], offset [0, 0], layer `Instances`. Bridge builder's abandoned yard
- `spr_loose_rocks` at [81, 56], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard
- `spr_bush_dead` at [79, 57], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard
- `spr_bush` at [60, 75], offset [0, 0], layer `Visual_Assets`. Cistern waterline
- `spr_pebbles` at [60, 72], offset [0, 0], layer `Visual_Assets`. Cistern waterline
- `spr_loose_rocks` at [73, 69], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche
- `spr_bush_dead` at [76, 69], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche
- `spr_loose_rocks` at [102, 54], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns
- `spr_bush_dead` at [102, 51], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns
- `spr_loose_rocks` at [111, 65], offset [0, 0], layer `Visual_Assets`. Southern bridge watch
- `spr_bush_dead` at [106, 63], offset [0, 0], layer `Visual_Assets`. Southern bridge watch
- `spr_pebbles` at [125, 42], offset [0, 0], layer `Visual_Assets`. Ruined arcade
- `spr_bush_dead` at [120, 40], offset [0, 0], layer `Visual_Assets`. Ruined arcade
- `spr_pebbles` at [120, 27], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones
- `spr_bush_dead` at [122, 28], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones
- `spr_column_whole` at [138, 10], offset [0, 0], layer `Instances`. Upper-terrace lookout
- `spr_pebbles` at [140, 10], offset [0, 0], layer `Visual_Assets`. Upper-terrace lookout
- `spr_bush_dead` at [141, 13], offset [0, 0], layer `Visual_Assets`. Upper-terrace lookout
- `spr_column_broken` at [34, 28], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [33, 30], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [27, 21], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [43, 72], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [46, 75], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [43, 68], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [72, 49], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [72, 53], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [75, 46], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_ruin_block` at [93, 74], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [103, 70], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [103, 48], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [119, 9], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [123, 9], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [116, 12], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [47, 12], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [51, 12], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [54, 15], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [76, 70], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [11, 47], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [45, 56], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [76, 24], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [110, 57], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_pebbles` at [12, 39], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_tree_dead` at [26, 49], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_pebbles` at [27, 49], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_tree_dead` at [38, 62], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_pebbles` at [39, 62], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [61, 33], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [68, 39], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [105, 64], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_tree_dead` at [127, 49], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_pebbles` at [123, 44], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [136, 19], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [47, 20], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_column_broken` at [103, 31], offset [0, 0], layer `Instances`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [100, 34], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [106, 34], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_column_broken` at [102, 41], offset [0, 0], layer `Instances`. Far-bank stone cairns — trail-edge continuation
- `spr_wagon_wreck` at [61, 20], offset [0, 0], layer `Instances`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [58, 23], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_column_broken` at [91, 43], offset [0, 0], layer `Instances`. Far-bank stone cairns — trail-edge continuation
- `spr_tree_dead` at [60, 56], offset [0, 0], layer `Instances`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [59, 56], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_loose_rocks` at [43, 36], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_column_whole` at [133, 27], offset [0, 0], layer `Instances`. Stair-foot votive stones — trail-edge continuation
- `spr_loose_rocks` at [102, 42], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_palm` at [54, 79], offset [0, 0], layer `Instances`. Cistern waterline — trail-edge continuation
- `spr_loose_rocks` at [62, 20], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_column_whole` at [114, 31], offset [0, 0], layer `Instances`. Ruined arcade — trail-edge continuation
- `spr_tree_dead` at [62, 56], offset [0, 0], layer `Instances`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [106, 36], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [133, 37], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [44, 36], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_column_broken` at [83, 78], offset [0, 0], layer `Instances`. Cistern keeper's niche — trail-edge continuation
- `spr_pebbles` at [110, 40], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_wagon_wreck` at [67, 58], offset [0, 0], layer `Instances`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_palm` at [61, 82], offset [0, 0], layer `Instances`. Cistern waterline — trail-edge continuation
- `spr_column_broken` at [113, 50], offset [0, 0], layer `Instances`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [114, 50], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_cactus_tall` at [23, 16], offset [0, 0], layer `Instances`. Camp approach windbreak — trail-edge continuation
- `spr_wagon_wreck` at [57, 27], offset [0, 0], layer `Instances`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [57, 26], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_pebbles` at [115, 31], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [10, 33], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_loose_rocks` at [115, 49], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [11, 58], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_loose_rocks` at [90, 42], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_wagon_wreck` at [82, 64], offset [0, 0], layer `Instances`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_column_broken` at [103, 76], offset [0, 0], layer `Instances`. Southern bridge watch — trail-edge continuation
- `spr_cactus_tall` at [19, 20], offset [0, 0], layer `Instances`. Camp approach windbreak — trail-edge continuation
- `spr_column_whole` at [131, 39], offset [0, 0], layer `Instances`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [68, 82], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [58, 26], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_wagon_wreck` at [40, 33], offset [0, 0], layer `Instances`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [38, 30], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_column_whole` at [112, 32], offset [0, 0], layer `Instances`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [31, 37], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off — trail-edge continuation
- `spr_wagon_wreck` at [31, 39], offset [0, 0], layer `Instances`. Broken axle pull-off — trail-edge continuation
- `spr_pebbles` at [110, 39], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [90, 43], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_wagon_wreck` at [25, 55], offset [0, 0], layer `Instances`. Spilled caravan cargo — trail-edge continuation
- `spr_palm` at [59, 58], offset [0, 0], layer `Instances`. Cistern waterline — trail-edge continuation
- `spr_palm` at [57, 58], offset [0, 0], layer `Instances`. Cistern waterline — trail-edge continuation
- `spr_loose_rocks` at [70, 53], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_bush` at [50, 77], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_loose_rocks` at [21, 22], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off — trail-edge continuation
- `spr_loose_rocks` at [39, 30], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_pebbles` at [51, 36], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_cactus_tall` at [44, 38], offset [0, 0], layer `Instances`. Cactus grove fork — trail-edge continuation
- `spr_bush_dead` at [45, 39], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_pebbles` at [134, 42], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [26, 55], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_supply_barrel` at [76, 58], offset [0, 0], layer `Instances`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [90, 63], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_column_broken` at [112, 70], offset [0, 0], layer `Instances`. Southern bridge watch — trail-edge continuation
- `spr_bush` at [61, 80], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_loose_rocks` at [93, 76], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_loose_rocks` at [76, 82], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [53, 20], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_pebbles` at [69, 21], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_tree_dead` at [64, 22], offset [0, 0], layer `Instances`. Last warning before the broken span — trail-edge continuation
- `spr_loose_rocks` at [21, 23], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off — trail-edge continuation
- `spr_pebbles` at [65, 22], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_tree_dead` at [66, 31], offset [0, 0], layer `Instances`. Last warning before the broken span — trail-edge continuation
- `spr_column_whole` at [134, 29], offset [0, 0], layer `Instances`. Stair-foot votive stones — trail-edge continuation
- `spr_loose_rocks` at [51, 35], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_pebbles` at [121, 32], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [90, 36], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_column_whole` at [123, 33], offset [0, 0], layer `Instances`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [90, 37], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_pebbles` at [90, 38], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_pebbles` at [90, 35], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_pebbles` at [90, 41], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_pebbles` at [81, 35], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_loose_rocks` at [10, 35], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_loose_rocks` at [30, 39], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off — trail-edge continuation
- `spr_pebbles` at [47, 41], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_loose_rocks` at [97, 40], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [106, 45], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_column_broken` at [93, 50], offset [0, 0], layer `Instances`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [82, 50], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [10, 58], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_loose_rocks` at [21, 56], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_loose_rocks` at [111, 70], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_bush` at [50, 75], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [61, 72], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_loose_rocks` at [103, 75], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_loose_rocks` at [68, 80], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [76, 80], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_pebbles` at [118, 20], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_loose_rocks` at [39, 29], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [38, 37], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_pebbles` at [109, 45], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [91, 49], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [75, 58], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_bush` at [58, 60], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_loose_rocks` at [67, 80], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_pebbles` at [119, 10], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [122, 10], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [119, 11], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [122, 11], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [122, 19], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [121, 19], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [123, 19], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [128, 12], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [128, 11], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_bush_dead` at [124, 12], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_loose_rocks` at [49, 13], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [25, 14], offset [0, 0], layer `Visual_Assets`. Camp approach windbreak — trail-edge continuation
- `spr_cactus_tall` at [19, 22], offset [0, 0], layer `Instances`. Camp approach windbreak — trail-edge continuation
- `spr_cactus_tall` at [32, 16], offset [0, 0], layer `Instances`. Camp approach windbreak — trail-edge continuation
- `spr_cactus_small` at [22, 19], offset [0, 0], layer `Instances`. Camp approach windbreak — trail-edge continuation
- `spr_pebbles` at [117, 26], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_pebbles` at [63, 22], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_loose_rocks` at [18, 26], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off — trail-edge continuation
- `spr_pebbles` at [62, 22], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_pebbles` at [60, 22], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_pebbles` at [64, 29], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_pebbles` at [63, 29], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_supply_barrel` at [37, 28], offset [0, 0], layer `Instances`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [48, 24], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [49, 24], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [39, 28], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [48, 28], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [39, 27], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [51, 27], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [50, 24], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [51, 25], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [39, 31], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [38, 28], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [38, 27], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_bush_dead` at [48, 31], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_pebbles` at [135, 28], offset [0, 0], layer `Visual_Assets`. Stair-foot votive stones — trail-edge continuation
- `spr_loose_rocks` at [57, 33], offset [0, 0], layer `Visual_Assets`. Bandit lookout remains — trail-edge continuation
- `spr_pebbles` at [77, 30], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_wagon_wreck` at [54, 35], offset [0, 0], layer `Instances`. Bandit lookout remains — trail-edge continuation
- `spr_loose_rocks` at [29, 35], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off — trail-edge continuation
- `spr_column_broken` at [101, 32], offset [0, 0], layer `Instances`. Far-bank stone cairns — trail-edge continuation
- `spr_column_broken` at [100, 38], offset [0, 0], layer `Instances`. Far-bank stone cairns — trail-edge continuation
- `spr_pebbles` at [119, 36], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [119, 35], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [10, 36], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_bush_dead` at [37, 36], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_pebbles` at [82, 42], offset [0, 0], layer `Visual_Assets`. Last warning before the broken span — trail-edge continuation
- `spr_bush_dead` at [37, 37], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_pebbles` at [53, 36], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [52, 36], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [47, 42], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [47, 43], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [47, 44], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_loose_rocks` at [54, 36], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_loose_rocks` at [53, 37], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [131, 38], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [131, 36], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [131, 44], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [132, 36], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [132, 44], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [122, 38], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [29, 39], offset [0, 0], layer `Visual_Assets`. Broken axle pull-off — trail-edge continuation
- `spr_bush_dead` at [36, 38], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_bush_dead` at [34, 42], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_pebbles` at [56, 45], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [57, 45], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_pebbles` at [58, 45], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_loose_rocks` at [53, 44], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_loose_rocks` at [50, 42], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_bush_dead` at [46, 40], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_loose_rocks` at [5, 44], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_bush_dead` at [47, 40], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_bush_dead` at [41, 46], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_loose_rocks` at [93, 43], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_column_whole` at [128, 46], offset [0, 0], layer `Instances`. Ruined arcade — trail-edge continuation
- `spr_loose_rocks` at [102, 40], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [94, 48], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_loose_rocks` at [102, 48], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_bush_dead` at [96, 41], offset [0, 0], layer `Visual_Assets`. Far-bank stone cairns — trail-edge continuation
- `spr_pebbles` at [115, 45], offset [0, 0], layer `Visual_Assets`. Ruined arcade — trail-edge continuation
- `spr_pebbles` at [59, 52], offset [0, 0], layer `Visual_Assets`. Bonefield waystones — trail-edge continuation
- `spr_loose_rocks` at [10, 57], offset [0, 0], layer `Visual_Assets`. Spilled caravan cargo — trail-edge continuation
- `spr_loose_rocks` at [115, 50], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_loose_rocks` at [112, 51], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_loose_rocks` at [111, 58], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_bush_dead` at [57, 56], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_bush_dead` at [34, 57], offset [0, 0], layer `Visual_Assets`. Cactus grove fork — trail-edge continuation
- `spr_pebbles` at [58, 58], offset [0, 0], layer `Visual_Assets`. Snake-skin hollow — trail-edge continuation
- `spr_pebbles` at [60, 58], offset [0, 0], layer `Visual_Assets`. Snake-skin hollow — trail-edge continuation
- `spr_pebbles` at [61, 58], offset [0, 0], layer `Visual_Assets`. Snake-skin hollow — trail-edge continuation
- `spr_pebbles` at [57, 65], offset [0, 0], layer `Visual_Assets`. Snake-skin hollow — trail-edge continuation
- `spr_loose_rocks` at [74, 58], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [72, 58], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [81, 58], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [74, 65], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [83, 62], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [83, 64], offset [0, 0], layer `Visual_Assets`. Bridge builder's abandoned yard — trail-edge continuation
- `spr_loose_rocks` at [124, 63], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_loose_rocks` at [115, 66], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_loose_rocks` at [82, 71], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [112, 69], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation
- `spr_loose_rocks` at [63, 72], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_bush` at [50, 76], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_column_broken` at [83, 73], offset [0, 0], layer `Instances`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [81, 78], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_bush` at [59, 80], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [60, 80], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [50, 78], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [59, 73], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [60, 73], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [69, 80], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [70, 80], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [71, 80], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [72, 80], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [68, 73], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_bush` at [69, 73], offset [0, 0], layer `Visual_Assets`. Cistern waterline — trail-edge continuation
- `spr_loose_rocks` at [77, 80], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [82, 73], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [82, 72], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [73, 73], offset [0, 0], layer `Visual_Assets`. Cistern keeper's niche — trail-edge continuation
- `spr_loose_rocks` at [96, 79], offset [0, 0], layer `Visual_Assets`. Southern bridge watch — trail-edge continuation

Every required asset ID (including shared character/combat families) is enumerated for this scene in `scene_gameplay_specs.json` and `scene_asset_manifest.json`. These are incoming requirements; exact prop aliases and animation suffixes still need Claude's asset mapping. Weather suppression rectangles are explicit in this scene's sidecar entry.

`mus_desert`, `snd_arrow_hit`, `snd_bat_screech`, `snd_bow_release`, `snd_cast_charge`, `snd_checkpoint`, `snd_chest_open`, `snd_magic_hit`, `snd_magic_travel`, `snd_pickup`, `snd_save`, `snd_snake_hiss`, `snd_snake_lunge`, `snd_step_sand`, `snd_sword_hit`, `snd_sword_swing`, `snd_wind_loop`, `spr_arrow`, `spr_bandit_attack_down`, `spr_bandit_attack_side`, `spr_bandit_attack_up`, `spr_bandit_caster_attack_down`, `spr_bandit_caster_attack_side`, `spr_bandit_caster_attack_up`, `spr_bandit_caster_defeat`, `spr_bandit_caster_hurt_down`, `spr_bandit_caster_idle_down`, `spr_bandit_caster_walk_down`, `spr_bandit_caster_walk_side`, `spr_bandit_caster_walk_up`, `spr_bandit_defeat`, `spr_bandit_hurt_down`, `spr_bandit_idle_down`, `spr_bandit_walk_down`, `spr_bandit_walk_side`, `spr_bandit_walk_up`, `spr_bat_defeat`, `spr_bat_dive`, `spr_bat_fly`, `spr_bush`, `spr_bush_dead`, `spr_cactus_small`, `spr_cactus_tall`, `spr_checkpoint_star`, `spr_chest_desert`, `spr_column_broken`, `spr_column_fallen`, `spr_column_whole`, `spr_dave_attack_down`, `spr_dave_attack_down_side`, `spr_dave_attack_side`, `spr_dave_attack_up`, `spr_dave_attack_up_side`, `spr_dave_idle_down`, `spr_dave_idle_down_side`, `spr_dave_idle_side`, `spr_dave_idle_up`, `spr_dave_idle_up_side`, `spr_dave_walk_down`, `spr_dave_walk_down_side`, `spr_dave_walk_side`, `spr_dave_walk_up`, `spr_dave_walk_up_side`, `spr_fx_arrow_hit`, `spr_fx_hit`, `spr_fx_magic_hit`, `spr_fx_magic_launch`, `spr_fx_slash`, `spr_fx_sparkle`, `spr_icon_ancient_coin`, `spr_icon_bandit_scimitar`, `spr_icon_desert_rose`, `spr_icon_gold_coins`, `spr_icon_golden_scarab`, `spr_icon_iron_tunic`, `spr_icon_potion_greater`, `spr_icon_potion_health`, `spr_loose_rocks`, `spr_magic_orb`, `spr_mask_bat`, `spr_mask_dave`, `spr_mask_medium`, `spr_mask_python`, `spr_obelisk`, `spr_palm`, `spr_pebbles`, `spr_pharaoh_statue`, `spr_python_coil`, `spr_python_defeat`, `spr_python_hurt`, `spr_python_lunge_down`, `spr_python_lunge_side`, `spr_python_lunge_up`, `spr_python_slither_down`, `spr_python_slither_side`, `spr_python_slither_up`, `spr_rock_small`, `spr_ruin_block`, `spr_skeleton_archer_attack_down`, `spr_skeleton_archer_attack_side`, `spr_skeleton_archer_attack_up`, `spr_skeleton_archer_defeat`, `spr_skeleton_archer_hurt_down`, `spr_skeleton_archer_idle_down`, `spr_skeleton_archer_walk_down`, `spr_skeleton_archer_walk_side`, `spr_skeleton_archer_walk_up`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `spr_skull`, `spr_supply_barrel`, `spr_tree_dead`, `spr_tumbleweed`, `spr_wagon_wreck`, `spr_water_barrel`, `tex_chasm_void`, `tex_chasm_wall`, `tex_cliff_face`, `tex_grass`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `tex_rock_top`, `tex_sand_dark`, `tex_sand_light`, `tex_water`, `tex_wet_sand`, `ts_bridge`, `ts_stairs`.
