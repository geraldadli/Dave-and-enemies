# Royal Expanse - expanding scene design

[Current chapter structure](DESERT_CHAPTER.md). Stable scene ID `sc_royal_expanse`; technical GameMaker resource `rm_sc_royal_expanse`. Starting extent **160 x 96 tiles** (10240 x 6144 px). A high, wind-scoured landscape opens into a royal approach: optional grotto and memorial loops precede the final save, an in-scene boss courtyard and the dungeon exterior.

No place below is a separate loaded scene. All place boundaries and batch edges are metadata only.

## Landscape overview

Reduced grid: one character summarizes 4 x 4 tiles; row labels are global tile rows. Full exact grid: `design/desert/scenes/rm_sc_royal_expanse.json`. Legend and coordinate rules are in the chapter document.

```text
00 ##############C#########################
04 ##############C#########################
08 ######.p.c####C#######MMMMMM#MMMMMMMMMM#
12 ######pee..###C#######___pp_MM_______Mt#
16 _,###.,.ep.,p#C#######_e__c_MM__...__.p#
20 a...#....__#p#C##pp###_.p___MM__.e...,_p
24 #p.....,,p._p#C,,,,,.#M^^M^^MM,,..___p_#
28 #p.pp,,...,,.#C,pcppp,..##.,#MgMMMMMMM##
32 ##.pp,p###p..===pe..p.p..#p,pM,MMMMMM###
36 ##.pc,####.e,===,,,,,,,,,,,,ppSp.#######
40 ##...,####.,p===..epp.....p,ppp..#######
44 ####p,.p.#p,.pCp_.##.,,,.p.,..._p#######
48 ####p....p.p.#C#p#c#..#pcpp.c##p########
52 ####.,.e.pp,##C###..._p,,..,,..,,,p#####
56 #####....c.,##C#####..pMpMM_.MMMp_,,####
60 #####,p.p..,##C######.M_p_p_____.,pp####
64 #####....p..##C######,p..p_p_c.,p,cp####
68 ##############C######.._p_pp_p_p..,.####
72 ##############C#######Mp.,,,,,__########
76 ##############C########MMMM_MMMM########
80 ##############C#########################
84 ##############C#########################
88 ##############C#########################
92 ##############C#########################
```

Scene transitions:

| Border | Opening rows | Arrival here | Destination scene / arrival |
|---|---|---|---|
| W | [18, 22] | [2, 20], pixels [160, 1312] | `sc_caravan_basin` / [141, 20] |

Preferred walking route: [2, 20] -> [12, 20] -> [12, 28] -> [25, 28] -> [47, 28] -> [47, 37] -> [66, 37] -> [96, 37] -> [110, 37] -> [110, 39] -> [122, 39] -> [122, 38] -> [122, 26] -> [132, 26] -> [132, 20] -> [145, 20] -> [154, 20] -> [154, 14]. This is a route suggestion, not a compulsory chain of place triggers.

Exploration circuits:

- **Grotto circuit**: Enter from the south, search the rock recess and return through the east opening to the plateau. Waypoints: [12, 28] -> [24, 28] -> [24, 22] -> [24, 16] -> [40, 16] -> [47, 16] -> [47, 28].
- **Southern worm basin circuit**: Take a broad southern sweep; the worm remains elective and cannot emerge on the causeway approach. Waypoints: [25, 28] -> [21, 28] -> [21, 63] -> [45, 63] -> [45, 45] -> [47, 45] -> [47, 37].
- **Memorial terrace circuit**: Climb one stair and descend the other, then return to the tomb approach before the final star. Waypoints: [82, 37] -> [84, 37] -> [84, 30] -> [94, 30] -> [94, 24] -> [94, 22] -> [107, 22] -> [107, 30] -> [110, 30] -> [110, 37].
- **Sundial court circuit**: Explore the quiet southern court, pass its sundial and valuable cache, then return from another side toward the final star. Its north opening gives a shorter direct approach as well. Waypoints: [96, 37] -> [84, 37] -> [84, 54] -> [84, 67] -> [97, 67] -> [97, 73] -> [122, 73] -> [122, 67] -> [134, 67] -> [134, 54] -> [110, 54] -> [110, 39].
- **Forgotten Pilgrims' Rest trail**: Find forgotten pilgrims' rest and its supplies; return by another approach. Waypoints: [12, 28] -> [12, 39] -> [21, 39] -> [21, 28].
- **Procession Waystation trail**: Find procession waystation and its supplies; return by another approach. Waypoints: [66, 37] -> [62, 37] -> [62, 26] -> [79, 26] -> [79, 37] -> [82, 37].
- **Sunken Offering Garden trail**: Find sunken offering garden and its supplies; return by another approach. Waypoints: [84, 45] -> [94, 45] -> [94, 53] -> [110, 53].
- **Fallen Archive trail**: Find fallen archive and its supplies; return by another approach. Waypoints: [134, 58] -> [142, 58] -> [142, 69] -> [134, 69] -> [134, 67].

Elevation and structures:

- Incoming plateau, causeway and royal forecourt are continuous base level z1 after the previous scene's stairs. Memorial terrace z2 is bounded by masonry and connects through its two stairs. Courtyard floor is flat at z1; sand inset is not a raised dais.
- `bridge_ew` [55, 34, 60, 40]: Seven-wide Royal Causeway, with clear banks; the visible bridge is a geographical passage, not a scene transition.
- `stairs` [92, 26, 96, 27]: West memorial ascent, five wide; all landings clear.
- `stairs` [105, 26, 109, 27]: East memorial descent completes a pre-boss exploration loop.

## Build this scene by expansion

1. **Plateau expansion**: Create the broad plateau, two elective loops, causeway and separated combat pockets. Places: `place_windblown_plateau`, `place_echo_grotto`, `place_royal_causeway`.
2. **Royal forecourt expansion**: Add the quiet forecourt, two-stair memorial circuit, new southern Sundial Court loop and final star immediately south of the gate. Places: `place_tomb_approach`, `place_memorial_vault`, `place_sundial_court`, `place_pharaohs_gate`.
3. **Courtyard and ending**: Build the in-scene arena enclosure, unavoidable entry trigger, two stateful barriers and ending exterior. Places: `place_pharaohs_courtyard`, `place_dungeon_threshold`.

## Places and readable local grids

Each crop below uses global `[x,y]` coordinates, one character per tile. It is an inspection window into the shared scene, not an enclosed map or scene boundary. The crop's x origin is stated; row labels remain global. Objects outside a crop are still present in the same scene.

### Fallen Archive

`place_archive_cache`; anchor [138, 68]; inspection extent [135, 64, 142, 70]; x origin **135**. A close, recognizable little destination with an optional persistent supply cache.

```text
64 ......._
65 .p____._
66 .__c_p.,
67 _p_____,
68 __.__._,
69 ,,,,,,,,
70 ,,,,,,..
```

### Sunken Offering Garden

`place_sunken_garden`; anchor [99, 52]; inspection extent [96, 48, 103, 54]; x origin **96**. A close, recognizable little destination with an optional persistent supply cache.

```text
48 ,...p..#
49 ,;;;;;##
50 ;;;c;;;.
51 ;;;;;;p;
52 ;;;;;;;,
53 ,,,,,,,,
54 ,,,.....
```

### Procession Waystation

`place_procession_cache`; anchor [71, 30]; inspection extent [68, 26, 75, 32]; x origin **68**. A close, recognizable little destination with an optional persistent supply cache.

```text
26 _,,,,,,,
27 ._____..
28 __.c_._.
29 ______p_
30 _.__.__.
31 ._____..
32 ........
```

### Forgotten Pilgrims' Rest

`place_pilgrim_camp`; anchor [16, 38]; inspection extent [13, 34, 20, 40]; x origin **13**. A close, recognizable little destination with an optional persistent supply cache.

```text
34 ,......,
35 ,p____p_
36 __.c_.__
37 _p____p_
38 _.__,__,
39 __,,,,,,
40 ,,,,,,,,
```

### Windblown Plateau

`place_windblown_plateau`; anchor [25, 28]; inspection extent [5, 25, 51, 62]; x origin **5**. Wide horizon on the same high level as the incoming pass; an elective worm basin lies south.

```text
25 ......._,.........,,..................__.____.p
26 .......,,........,__....,,,,,,,,..p....____,__.
27 .p.....,,...,,,,___,,,,,,,,,,,,___,,...._.___..
28 ......,,,,,,,,___,,,,,,,,,,,,___,,,,,,,,,,,....
29 ......,,,,,,___,,,,,,,,...........,,,,,,,.__..#
30 #.p...,,.......,,,........................_,...
31 ###...,,,p..p..,,,,.......................,,...
32 ####..._,......,,,,......###########......,,...
33 ####...,,...p..,,,,....#############......,,...
34 ####...,,......,,_,.p.##############p.....,,...
35 ####...,,p____p___....##############......,....
36 ####...,__.c_.__,,...###############......e,,,,
37 ####...,_p____p_,,..################.....,,,,,,
38 ####..,,_.__,__,,,..################.....,,....
39 ####..,___,,,,,,,,..################.....,,....
40 ####...,,,,,,,,,,,..################.....,,...p
41 ####............,,,.################.....,,....
42 #####...........__,.################.....,,....
43 ######.........._,,..################....,,,...
44 ##########......,,,..###############....,,_,...
45 ##########.p....,,,......p.......###.p.,___,...
46 ##########......,,...............###...,_,,....
47 ##########......,,...............###...,,,.....
48 ###########.....,,...............###...,,,.....
49 ############..p.,_...............###....,,.....
50 ############....__...............###....,,.....
51 ############...,,,..............p###....,,p...#
52 ############...,,,.......e.......###....,_,.###
53 ############...,,...............p###p...__,.###
54 #############..,,................###....,,,.###
55 #############..,,................###....,,,.###
56 #############..,,.......................,,,.###
57 #############..,_.......................,,..###
58 #############..__.................c....,,,..###
59 #############..,,......................,,,..###
60 #############..,,......................,_,..###
61 ##############.,,...p........p.........,_,..###
62 ##############.,,,,,,__...........,,,,,,,,..###
```

### Royal Causeway

`place_royal_causeway`; anchor [57, 37]; inspection extent [41, 29, 79, 53]; x origin **41**. A royal bridge, a guard before it and a caster pocket after it; no combat on the span.

```text
29 ,,,,,.__..####CCCCCC,_.p..p______p_..__
30 ......_,...###CCCCCC__....._.__.__.p___
31 ......,,...###CCCCCC,,......_____..__._
32 ......,,...###CCCCCC,,..............___
33 ......,,......CCCCCC,,.p............._,
34 p.....,,......======,,........e.......,
35 ......,.....,,======,,,p..............,
36 ......e,,,,,,,======,,__,,,,,,,......,_
37 .....,,,,,,,,,======___,,,,,,,,,,,,,,_,
38 .....,,.......======,,,,,,,,,,,,,,,,,,,
39 .....,,.......======...................
40 .....,,...p...======.............e.....
41 .....,,.......CCCCCC##................p
42 .....,,....###CCCCCC..................#
43 #....,,,...###CCCCCC.._.___...........#
44 ....,,_,....##CCCCCCp.____._..........#
45 .p.,___,.....#CCCCCC____.____..########
46 ...,_,,......#CCCCCC._.____...#########
47 ...,,,.....p..CCCCCC..___._...#########
48 ...,,,.......#CCCCCC.........##########
49 ....,,.......#CCCCCC##..p..###.....####
50 ....,,......##CCCCCC##########.........
51 ....,,p...####CCCCCC##########..c......
52 ....,_,.######CCCCCC##########.........
53 p...__,.######CCCCCC##########.........
```

### Tomb Approach

`place_tomb_approach`; anchor [96, 37]; inspection extent [81, 31, 114, 53]; x origin **81**. Quiet ceremonial ground with a northern memorial circuit and guaranteed consumables.

```text
31 __,_......,,.....#######..,,,,,..#
32 .__,............########...,,,....
33 __,_............#########p.,,,....
34 ..__.......................,,,..p.
35 p.,,....p..................,,_....
36 ,,,,,,,,,,,,___,,,,,......,,__,.p.
37 ,,,,,,,,,,___,,,,,,,,,,,,___,,,...
38 ,..,,,,,___,,,.,,,,,,,,___,,,,,,,,
39 ...,,...............,,,,,,..,,,,,,
40 .p.,_.......................,,,...
41 ...__..########.........p...,,,...
42 ...,,......###..............,,_...
43 ...,,..................p.....__p..
44 ...,,,,,,,..,,...............,,...
45 ...,,,,,,___,,,..............,,...
46 ...,,..,,_,,,,,..............,,...
47 ..,,,........,,,......p.#....,,...
48 ..,_....###p.,,,...p..###....,,..c
49 ..__...####..,,,;;;;;##......,,...
50 ..,,...###...,_;;;c;;;.......__...
51 ..,,.....#..,__;;;;;;p;p,.p.._,...
52 ..___._.....,,,;;;;;;;,,,___,,....
53 .__,____....,,,,,,,,,,,,,_,,,,,,,,
```

### Pharaoh's Gate

`place_pharaohs_gate`; anchor [122, 38]; inspection extent [115, 35, 133, 47]; x origin **115**. Final yellow star, seven tiles south of the boss gate with no fight or transition between them.

```text
35 ......,,...........
36 ......,,...........
37 .,,p..__...p.......
38 ,,,,___S...........
39 ,,,,_,,,...........
40 ...................
41 ...................
42 .....p...__.__.....
43 .p......_.____.....
44 ........____.___...
45 ........__.____p...
46 ..####...____....##
47 ..#####.........###
```

### Pharaoh's Courtyard

`place_pharaohs_courtyard`; anchor [132, 20]; inspection extent [116, 8, 149, 34]; x origin **116**. A visibly distinct paved courtyard inside this scene, physically gated for combat.

```text
08 MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
09 MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
10 MM______________________________MM
11 MM______________________________MM
12 MM______________________________MM
13 MM______________________________MM
14 MM__________............._______MM
15 MM__________............._______MM
16 MM__________............._______MM
17 MM__________............._________
18 MM__________......................
19 MM__________....,,,,,,,,,,,,_,,,..
20 MM__________...,e,,,,....,,,,,,,,,
21 MM__________...,,...............,,
22 MM__________...,,...............MM
23 MM__________..,,,........_______MM
24 MM__..........,,,.._____________MM
25 MM__..,,,,,,,,___.._____________MM
26 MM__.,,,,,,,___,,.._____________MM
27 MM__.,,,,.........._____________MM
28 MMMMMtttMMMMMMMMMMMMMMMMMMMMMMMMMM
29 MMMMM,_.MMMMMMMMMMMMMMMMMMMMMMMMMM
30 MMMMM__.MMMMMMMMMMMMMMMMMMMMMMMMMM
31 MMMMMgggMMMMMMMMMMMMMMMMMMMMMMMMMM
32 MMMMM,,.MMMMMMMMMMMMMMMMMMMMMMMMMM
33 MMMMM,,.MMMMMMMMMMMMMMMMMMMMMMMMMM
34 MMMMM,,.MMMMMMMMMMMMMMMMMMMMMMMMMM
```

### Dungeon Threshold

`place_dungeon_threshold`; anchor [154, 19]; inspection extent [150, 9, 157, 27]; x origin **150**. A quiet dungeon exterior physically reachable only through the cleared courtyard; the doorway ends Chapter I.

```text
09 #MMMMMMM
10 #MMMMMMM
11 #MM__MMM
12 __.tt.._
13 __....._
14 __.._,._
15 __.,,,._
16 __..,,._
17 __p.,,._
18 ....,,._
19 ...,,,._
20 ,,,,,,._
21 ,,,_,..p
22 ...___._
23 ________
24 _p______
25 ________
26 ________
27 ________
```

### Echo Grotto

`place_echo_grotto`; anchor [32, 16]; inspection extent [17, 5, 45, 24]; x origin **17**. Echo Grotto is an open rock recess with south and east access; no interior load or opaque roof.

```text
05 #############################
06 #############################
07 #############################
08 #######.......p..........####
09 #######..................####
10 #######...............c..####
11 #######..................####
12 #######....e......e......####
13 #####.....................###
14 #####..p........,,,,,....,###
15 ####......,,,,,,,,,,,,,,,,,,_
16 ####...,,,,,,,,,,,,,,,,,,,___
17 ####...,,,,,,.........,,,..,,
18 ####..._,......e.............
19 ####..._,............p.......
20 ####..,,,............__.__###
21 ####..,,,..........._.____###
22 ####..,,,...........____._###
23 ####..,,....######..__.___###
24 ###...,,....######...____..__
```

### Memorial Vault

`place_memorial_vault`; anchor [101, 20]; inspection extent [87, 10, 114, 28]; x origin **87**. Memorial Vault is a roofless upper terrace with two stairs, a guardian and premium optional armor.

```text
10 MMMMMMMMMMMMMMMMMMMMMMMMMMMM
11 MMMMMMMMMMMMMMMMMMMMMMMMMMMM
12 MM______________p___p_____MM
13 MM________________________MM
14 MM________________________MM
15 MM________________________MM
16 MM________________________MM
17 MM______e_________c_______MM
18 MM________________________MM
19 MM________________________MM
20 MM___.......p..........___MM
21 MM___..__,,...__.__,,..___MM
22 MM___._,,,,,,_,______,.___MM
23 MM___.,,....,________,.___MM
24 MM___.,,.....__.____,,.___MM
25 MM___.,,..________..,,.___MM
26 MMMMM^^^^^MMMMMMMM^^^^^MMMMM
27 MMMMM^^^^^MMMMMMMM^^^^^MMMMM
28 .......__..#######.,,,,....#
```

### Sundial Court

`place_sundial_court`; anchor [110, 68]; inspection extent [83, 53, 136, 80]; x origin **83**. A new quiet southern destination: an obelisk sundial, four broad openings, visible valuable treasure and different approaches back to the royal forecourt. No key, puzzle lock or new scene.

```text
53 _,____....,,,,,,,,,,,,,_,,,,,,,,,,,,___,,,,,,,,,,,,,,.
54 ____._p...,,,,,,...........,,,,,,,_...,,,,,,,,,,,___,p
55 __,___.....................................,,,,_____,.
56 _____...#.......p..............................___,___
57 _,...p.###......................#######.......p_.____,
58 ,,...##MMMMMMMMMMMMMMMMMM_____MMMMMMMMMMMMMMMM.____,__
59 ,,...##MMMMMMMMMMMMMMMMMM_____MMMMMMMMMMMMMMMM.._.___,
60 ,,...##MM___________________________________MM....,,_.
61 ,,...##MM______p_____p______________________MM#...,__.
62 ,,,..##MM___________________________________MM#...,,,.
63 ,_,..##MM___________________________________MM....,,,.
64 ,_,....MM___________________________c_______MM.p..,,..
65 ,,,....p........._p__________________.............,,.p
66 ,,,,,.......,,...____________________..,,,..,,,,,,,,._
67 ,,,,,,,,___,,,,..__________p_________.,__,,,,,,,,,,,_p
68 ,,,,,,___,_,___.._______p_________p__.,,,,,,,,,,...___
69 ..........____,_.______________________,,,........,_,,
70 .......MM___.___p________p___________.___,__MM.....,,,
71 #####..MM______..................__.____,p__MM........
72 #######MM_______,,,,,,,,,,,.......____,__.__MM##......
73 #######MMp__._,,,,,,,,,,,,___,,,,,,_,___,.__MM########
74 #######MM___.............,_,,,,,,,,,,,,,..__MM########
75 #######MM___..............................__MM########
76 #######MM___________________________________MM########
77 #######MMMMMMMMMMMMMMMMMM_____MMMMMMMMMMMMMMMM########
78 #######MMMMMMMMMMMMMMMMMM_____MMMMMMMMMMMMMMMM########
79 ########################.......#######################
80 #########################.....########################
```

## Gameplay placement

Encounters (IDs retained across the redesign):

- `rm_d13_windblown_plateau:g1`: pad/leash [24, 46, 36, 58], max 1 active. Elective worm emergence basin, with a broad escape ring and a reward beyond it. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d13_windblown_plateau:g1:e1`: `sandworm` at [30, 52].
- `rm_d14_royal_causeway:g1`: pad/leash [42, 31, 50, 41], max 1 active. One known melee guard, kept away from bridge landings. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d14_royal_causeway:g1:e1`: `skeleton_warrior` at [47, 36].
- `rm_d14_royal_causeway:g2`: pad/leash [65, 31, 77, 43], max 2 active. Caster and bandit combine on a broad far-bank pad; never fire onto the bridge. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_d14_royal_causeway:g2:e1`: `bandit_caster` at [71, 34].
  - `rm_d14_royal_causeway:g2:e2`: `bandit` at [74, 40].
- `rm_o5_echo_grotto:g1`: pad/leash [25, 9, 37, 21], max 3 active. Optional bat pair plus telegraphed lunge; both grotto exits remain open. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_o5_echo_grotto:g1:e1`: `bat` at [28, 12].
  - `rm_o5_echo_grotto:g1:e2`: `bat` at [35, 12].
  - `rm_o5_echo_grotto:g1:e3`: `python` at [32, 18].
- `rm_o6_memorial_vault:g1`: pad/leash [90, 12, 98, 20], max 1 active. One memorial guardian, separated from stairs and the armor's approach. Activation: Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones.
  - `rm_o6_memorial_vault:g1:e1`: `skeleton_warrior` at [95, 17].
- `rm_d17_pharaohs_courtyard:boss`: pad/leash [123, 12, 143, 24], max 1 active. Uncluttered arena for laser movement, committed thunder warnings and capped summons. Activation: boss_intro_complete
  - `rm_d17_pharaohs_courtyard:boss:e1`: `pharaoh` at [132, 20].

Chests (all unlocked, no ordinary kill lock; overflow stays pending):

- `rm_sc_royal_expanse:c1` at [39, 58]: 1 x `desert_rose`, 1 x `potion_greater`. Approach [39, 60], interaction [39, 59]. A visible reward beyond the elective basin; no worm kill flag gates it. Legacy ID `rm_d13_windblown_plateau:c1` is mapped explicitly.
- `rm_sc_royal_expanse:c2` at [73, 51]: 2 x `potion_greater`. Approach [73, 53], interaction [73, 52]. Restock after the last dense required-route group. Legacy ID `rm_d14_royal_causeway:c1` is mapped explicitly.
- `rm_sc_royal_expanse:c3` at [114, 48]: 2 x `potion_greater`. Approach [114, 50], interaction [114, 49]. Guaranteed pre-boss consumables on a short, enemy-free side pocket. Legacy ID `rm_d15_tomb_approach:c1` is mapped explicitly.
- `rm_sc_royal_expanse:c4` at [39, 10]: 1 x `sunsteel_blade`. Approach [39, 12], interaction [39, 11]. A strong optional weapon, never assumed by Pharaoh health tuning. Legacy ID `rm_o5_echo_grotto:c1` is mapped explicitly.
- `rm_sc_royal_expanse:c5` at [105, 17]: 1 x `paladin_mail`, 1 x `potion_greater`. Approach [105, 19], interaction [105, 18]. Premium optional armor, earned by taking the memorial detour; never a key or required boss defense tier. Legacy ID `rm_o6_memorial_vault:c1` is mapped explicitly.
- `rm_sc_royal_expanse:c6` at [119, 64]: 2 x `ancient_coin`, 1 x `golden_scarab`. Approach [119, 66], interaction [119, 65]. Reward the wider southern landscape with collectibles; no power or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_royal_expanse:c7` at [16, 36]: 1 x `potion_greater`. Approach [16, 38], interaction [16, 37]. Optional discovery at Forgotten Pilgrims' Rest; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_royal_expanse:c8` at [71, 28]: 2 x `ancient_coin`. Approach [71, 30], interaction [71, 29]. Optional discovery at Procession Waystation; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_royal_expanse:c9` at [99, 50]: 1 x `desert_rose`. Approach [99, 52], interaction [99, 51]. Optional discovery at Sunken Offering Garden; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.
- `rm_sc_royal_expanse:c10` at [138, 66]: 1 x `golden_scarab`. Approach [138, 68], interaction [138, 67]. Optional discovery at Fallen Archive; no equipment or progression requirement. New scene-world reward; no legacy claim to migrate.

Checkpoint and scripts:

- `sc_royal_expanse:checkpoint` at/respawn [122, 38]; clear 3 x 3 [121, 37, 123, 39]; peaceful district [115, 35, 133, 45]. E opens exactly 3 save slots; heal on successful save; snapshot all state together.
- `boss_entry` at [121, 28, 123, 28], event `boss_intro`, flag `boss_intro_seen`: Continuously test occupied throat while idle; after full mask clears north of row29 top (pixel y1856), pause damage, walk to [122,26], close gate, frame dialogue. Intro-seen never suppresses encounter initialization after failure.
- `pharaoh_defeat` at None, event `boss_hp_zero`, flag `boss_pharaoh_defeated`: Disable all damage immediately. Disintegrate; slow whiteout; remove every summon, projectile and hazard; fade back; open both barriers and atomically commit defeated flag plus pending unique reward. No scene load; no Grail reward.
- `dungeon_threshold` at [153, 12, 154, 12], event `chapter_ending`, flag `chapter_desert_complete`: Require boss_pharaoh_defeated. Enter the doorway to show To Be Continued in rm_ending; no dungeon interior. Completed saves may replay the ending.
- Boss state/camera/music/caps: this scene's `boss` in `scene_gameplay_specs.json`. Gate [121, 31, 123, 31], east seal [148, 17, 149, 21]; unique reward `rm_sc_royal_expanse:u1` at [134, 19]. Both barriers are within this scene, not loading exits.

Solid props (terrain/chests handled separately):

- `pharaoh_statue` at [118, 37]; centred base [48, 28] px, conservative blocked cells [118, 37, 118, 37].
- `pharaoh_statue` at [126, 37]; centred base [48, 28] px, conservative blocked cells [126, 37, 126, 37].
- `obelisk` at [110, 67]; centred base [40, 28] px, conservative blocked cells [110, 67, 110, 67].
- `column_whole` at [14, 35]; centred base [28, 18] px, conservative blocked cells [14, 35, 14, 35].
- `column_broken` at [19, 35]; centred base [28, 18] px, conservative blocked cells [19, 35, 19, 35].
- `water_barrel` at [14, 37]; centred base [38, 20] px, conservative blocked cells [14, 37, 14, 37].
- `column_fallen` at [19, 37]; centred base [36, 20] px, conservative blocked cells [19, 37, 19, 37].
- `column_whole` at [67, 29]; centred base [28, 18] px, conservative blocked cells [67, 29, 67, 29].
- `column_broken` at [74, 29]; centred base [28, 18] px, conservative blocked cells [74, 29, 74, 29].
- `column_fallen` at [76, 30]; centred base [36, 20] px, conservative blocked cells [76, 30, 76, 30].
- `palm` at [102, 51]; centred base [24, 14] px, conservative blocked cells [102, 51, 102, 51].
- `column_broken` at [103, 47]; centred base [28, 18] px, conservative blocked cells [103, 47, 103, 47].
- `column_broken` at [136, 65]; centred base [28, 18] px, conservative blocked cells [136, 65, 136, 65].
- `column_fallen` at [140, 66]; centred base [36, 20] px, conservative blocked cells [140, 66, 140, 66].
- `tree_dead` at [6, 27]; centred base [24, 16] px, conservative blocked cells [6, 27, 6, 27].
- `supply_barrel` at [7, 30]; centred base [28, 16] px, conservative blocked cells [7, 30, 7, 30].
- `tree_dead` at [17, 33]; centred base [24, 16] px, conservative blocked cells [17, 33, 17, 33].
- `column_fallen` at [25, 34]; centred base [36, 20] px, conservative blocked cells [25, 34, 25, 34].
- `ruin_block` at [39, 26]; centred base [48, 24] px, conservative blocked cells [39, 26, 39, 26].
- `column_whole` at [51, 25]; centred base [28, 18] px, conservative blocked cells [51, 25, 51, 25].
- `column_broken` at [50, 22]; centred base [28, 18] px, conservative blocked cells [50, 22, 50, 22].
- `tree_dead` at [16, 45]; centred base [24, 16] px, conservative blocked cells [16, 45, 16, 45].
- `column_fallen` at [19, 49]; centred base [36, 20] px, conservative blocked cells [19, 49, 19, 49].
- `tree_dead` at [34, 61]; centred base [24, 16] px, conservative blocked cells [34, 61, 34, 61].
- `column_fallen` at [37, 66]; centred base [36, 20] px, conservative blocked cells [37, 66, 37, 66].
- `tree_dead` at [52, 47]; centred base [24, 16] px, conservative blocked cells [52, 47, 52, 47].
- `supply_barrel` at [47, 51]; centred base [28, 16] px, conservative blocked cells [47, 51, 47, 51].
- `column_whole` at [65, 49]; centred base [28, 18] px, conservative blocked cells [65, 49, 65, 49].
- `column_broken` at [61, 44]; centred base [28, 18] px, conservative blocked cells [61, 44, 61, 44].
- `column_whole` at [81, 35]; centred base [28, 18] px, conservative blocked cells [81, 35, 81, 35].
- `column_broken` at [83, 28]; centred base [28, 18] px, conservative blocked cells [83, 28, 83, 28].
- `tree_dead` at [100, 48]; centred base [24, 16] px, conservative blocked cells [100, 48, 100, 48].
- `supply_barrel` at [104, 43]; centred base [28, 16] px, conservative blocked cells [104, 43, 104, 43].
- `column_broken` at [89, 54]; centred base [28, 18] px, conservative blocked cells [89, 54, 89, 54].
- `ruin_block` at [88, 57]; centred base [48, 24] px, conservative blocked cells [88, 57, 88, 57].
- `column_whole` at [99, 70]; centred base [28, 18] px, conservative blocked cells [99, 70, 99, 70].
- `column_broken` at [92, 73]; centred base [28, 18] px, conservative blocked cells [92, 73, 92, 73].
- `column_whole` at [124, 71]; centred base [28, 18] px, conservative blocked cells [124, 71, 124, 71].
- `column_broken` at [117, 68]; centred base [28, 18] px, conservative blocked cells [117, 68, 117, 68].
- `column_whole` at [129, 57]; centred base [28, 18] px, conservative blocked cells [129, 57, 129, 57].
- `column_broken` at [136, 54]; centred base [28, 18] px, conservative blocked cells [136, 54, 136, 54].
- `column_whole` at [126, 48]; centred base [28, 18] px, conservative blocked cells [126, 48, 126, 48].
- `column_broken` at [130, 45]; centred base [28, 18] px, conservative blocked cells [130, 45, 130, 45].
- `column_whole` at [151, 24]; centred base [28, 18] px, conservative blocked cells [151, 24, 151, 24].
- `column_broken` at [157, 21]; centred base [28, 18] px, conservative blocked cells [157, 21, 157, 21].
- `column_broken` at [37, 53]; centred base [28, 18] px, conservative blocked cells [37, 53, 37, 53].
- `ruin_block` at [41, 53]; centred base [48, 24] px, conservative blocked cells [41, 53, 41, 53].
- `column_broken` at [112, 43]; centred base [28, 18] px, conservative blocked cells [112, 43, 112, 43].
- `ruin_block` at [116, 43]; centred base [48, 24] px, conservative blocked cells [116, 43, 116, 43].
- `column_broken` at [103, 12]; centred base [28, 18] px, conservative blocked cells [103, 12, 103, 12].
- `ruin_block` at [107, 12]; centred base [48, 24] px, conservative blocked cells [107, 12, 107, 12].
- `column_broken` at [14, 31]; centred base [28, 18] px, conservative blocked cells [14, 31, 14, 31].
- `ruin_block` at [17, 31]; centred base [48, 24] px, conservative blocked cells [17, 31, 17, 31].
- `column_broken` at [69, 23]; centred base [28, 18] px, conservative blocked cells [69, 23, 69, 23].
- `ruin_block` at [73, 23]; centred base [48, 24] px, conservative blocked cells [73, 23, 73, 23].
- `column_broken` at [104, 51]; centred base [28, 18] px, conservative blocked cells [104, 51, 104, 51].
- `ruin_block` at [99, 56]; centred base [48, 24] px, conservative blocked cells [99, 56, 99, 56].
- `column_broken` at [140, 61]; centred base [28, 18] px, conservative blocked cells [140, 61, 140, 61].
- `ruin_block` at [137, 61]; centred base [48, 24] px, conservative blocked cells [137, 61, 137, 61].
- `tree_dead` at [30, 45]; centred base [24, 16] px, conservative blocked cells [30, 45, 30, 45].
- `column_fallen` at [37, 51]; centred base [36, 20] px, conservative blocked cells [37, 51, 37, 51].
- `column_fallen` at [41, 34]; centred base [36, 20] px, conservative blocked cells [41, 34, 41, 34].
- `tree_dead` at [79, 41]; centred base [24, 16] px, conservative blocked cells [79, 41, 79, 41].
- `column_fallen` at [64, 35]; centred base [36, 20] px, conservative blocked cells [64, 35, 64, 35].
- `tree_dead` at [31, 8]; centred base [24, 16] px, conservative blocked cells [31, 8, 31, 8].
- `column_fallen` at [24, 14]; centred base [36, 20] px, conservative blocked cells [24, 14, 24, 14].
- `column_whole` at [104, 61]; centred base [28, 18] px, conservative blocked cells [104, 61, 104, 61].
- `tree_dead` at [89, 35]; centred base [24, 16] px, conservative blocked cells [89, 35, 89, 35].
- `tree_dead` at [113, 36]; centred base [24, 16] px, conservative blocked cells [113, 36, 113, 36].
- `tree_dead` at [105, 41]; centred base [24, 16] px, conservative blocked cells [105, 41, 105, 41].
- `tree_dead` at [7, 24]; centred base [24, 16] px, conservative blocked cells [7, 24, 7, 24].
- `column_whole` at [107, 68]; centred base [28, 18] px, conservative blocked cells [107, 68, 107, 68].
- `tree_dead` at [113, 34]; centred base [24, 16] px, conservative blocked cells [113, 34, 113, 34].
- `column_whole` at [90, 65]; centred base [28, 18] px, conservative blocked cells [90, 65, 90, 65].
- `tree_dead` at [25, 61]; centred base [24, 16] px, conservative blocked cells [25, 61, 25, 61].
- `column_whole` at [108, 70]; centred base [28, 18] px, conservative blocked cells [108, 70, 108, 70].
- `column_broken` at [98, 61]; centred base [28, 18] px, conservative blocked cells [98, 61, 98, 61].
- `column_whole` at [64, 29]; centred base [28, 18] px, conservative blocked cells [64, 29, 64, 29].
- `column_broken` at [101, 65]; centred base [28, 18] px, conservative blocked cells [101, 65, 101, 65].
- `column_broken` at [38, 19]; centred base [28, 18] px, conservative blocked cells [38, 19, 38, 19].
- `column_whole` at [152, 17]; centred base [28, 18] px, conservative blocked cells [152, 17, 152, 17].
- `column_whole` at [120, 42]; centred base [28, 18] px, conservative blocked cells [120, 42, 120, 42].
- `tree_dead` at [107, 51]; centred base [24, 16] px, conservative blocked cells [107, 51, 107, 51].
- `column_broken` at [49, 16]; centred base [28, 18] px, conservative blocked cells [49, 16, 49, 16].
- `column_whole` at [99, 20]; centred base [28, 18] px, conservative blocked cells [99, 20, 99, 20].
- `supply_barrel` at [106, 33]; centred base [28, 16] px, conservative blocked cells [106, 33, 106, 33].
- `supply_barrel` at [51, 40]; centred base [28, 16] px, conservative blocked cells [51, 40, 51, 40].
- `column_broken` at [64, 33]; centred base [28, 18] px, conservative blocked cells [64, 33, 64, 33].
- `column_whole` at [82, 40]; centred base [28, 18] px, conservative blocked cells [82, 40, 82, 40].
- `supply_barrel` at [42, 45]; centred base [28, 16] px, conservative blocked cells [42, 45, 42, 45].
- `column_broken` at [92, 48]; centred base [28, 18] px, conservative blocked cells [92, 48, 92, 48].
- `column_whole` at [130, 64]; centred base [28, 18] px, conservative blocked cells [130, 64, 130, 64].
- `column_whole` at [136, 67]; centred base [28, 18] px, conservative blocked cells [136, 67, 136, 67].

## Decoration and required assets

Decoration is separate, noncolliding art. Tall landmarks sit on existing blocked terrain unless their real base is listed as a solid prop above.

- `spr_tree_dead` at [11, 50], offset [0, 0], layer `Instances`. Wind-scoured tree on the western rock island.
- `spr_ruin_block` at [18, 10], offset [0, 0], layer `Instances`. Grotto rock-rim shrine; the floor and exits stay fully visible.
- `spr_obelisk` at [101, 11], offset [0, 0], layer `Instances`. Memorial inscription on its solid north rim.
- `spr_pharaoh_statue` at [117, 15], offset [0, 0], layer `Instances`. Arena statues occupy masonry only, leaving all dodge lanes free.
- `spr_pharaoh_statue` at [148, 25], offset [0, 0], layer `Instances`. Matching statue remains outside the fight floor.
- `spr_dungeon_entrance` at [153, 12], offset [32, 0], layer `Instances`. Align the existing two-cell doorway with x153..154; ground base offset places its centre between tile centres.
- `spr_bush_dead` at [104, 49], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_pebbles` at [41, 64], offset [0, 0], layer `Visual_Assets`. Sparse, readable dressing.
- `spr_ruin_block` at [98, 58], offset [0, 0], layer `Instances`. Broken sundial-court wall on existing masonry.
- `spr_pharaoh_statue` at [123, 78], offset [0, 0], layer `Instances`. Weathered southern landmark, planted on the blocked foundation edge.
- `spr_loose_rocks` at [14, 40], offset [0, 0], layer `Visual_Assets`. Forgotten Pilgrims' Rest — composed discovery
- `spr_bush_dead` at [20, 37], offset [0, 0], layer `Visual_Assets`. Forgotten Pilgrims' Rest — composed discovery
- `spr_loose_rocks` at [69, 30], offset [0, 0], layer `Visual_Assets`. Procession Waystation — composed discovery
- `spr_bush_dead` at [75, 29], offset [0, 0], layer `Visual_Assets`. Procession Waystation — composed discovery
- `spr_water_barrel` at [102, 49], offset [0, 0], layer `Instances`. Sunken Offering Garden — composed discovery
- `spr_bush` at [97, 52], offset [0, 0], layer `Visual_Assets`. Sunken Offering Garden — composed discovery
- `spr_bush` at [102, 52], offset [0, 0], layer `Visual_Assets`. Sunken Offering Garden — composed discovery
- `spr_loose_rocks` at [96, 54], offset [0, 0], layer `Visual_Assets`. Sunken Offering Garden — composed discovery
- `spr_loose_rocks` at [136, 70], offset [0, 0], layer `Visual_Assets`. Fallen Archive — composed discovery
- `spr_pebbles` at [141, 64], offset [0, 0], layer `Visual_Assets`. Fallen Archive — composed discovery
- `spr_pebbles` at [13, 29], offset [0, 0], layer `Visual_Assets`. Plateau windbreak
- `spr_bush_dead` at [13, 26], offset [0, 0], layer `Visual_Assets`. Plateau windbreak
- `spr_pebbles` at [19, 30], offset [0, 0], layer `Visual_Assets`. Grotto approach bones
- `spr_loose_rocks` at [22, 36], offset [0, 0], layer `Visual_Assets`. Grotto approach bones
- `spr_column_broken` at [44, 22], offset [0, 0], layer `Instances`. Echo shrine offerings
- `spr_loose_rocks` at [42, 19], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings
- `spr_bush_dead` at [43, 21], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings
- `spr_pebbles` at [49, 28], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns
- `spr_bush_dead` at [44, 26], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns
- `spr_pebbles` at [23, 43], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge
- `spr_loose_rocks` at [17, 44], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge
- `spr_pebbles` at [35, 64], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains
- `spr_loose_rocks` at [39, 65], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains
- `spr_pebbles` at [50, 44], offset [0, 0], layer `Visual_Assets`. Southern return marker
- `spr_bush_dead` at [51, 48], offset [0, 0], layer `Visual_Assets`. Southern return marker
- `spr_pebbles` at [67, 48], offset [0, 0], layer `Visual_Assets`. Broken royal procession
- `spr_bush_dead` at [64, 42], offset [0, 0], layer `Visual_Assets`. Broken royal procession
- `spr_pebbles` at [83, 29], offset [0, 0], layer `Visual_Assets`. Memorial stair approach
- `spr_bush_dead` at [83, 32], offset [0, 0], layer `Visual_Assets`. Memorial stair approach
- `spr_column_whole` at [103, 27], offset [0, 0], layer `Instances`. Memorial offerings
- `spr_column_broken` at [100, 26], offset [0, 0], layer `Instances`. Memorial offerings
- `spr_pebbles` at [101, 20], offset [0, 0], layer `Visual_Assets`. Memorial offerings
- `spr_bush_dead` at [102, 20], offset [0, 0], layer `Visual_Assets`. Memorial offerings
- `spr_pebbles` at [103, 46], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains
- `spr_bush_dead` at [101, 47], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains
- `spr_loose_rocks` at [82, 56], offset [0, 0], layer `Visual_Assets`. Sunken court approach
- `spr_bush_dead` at [82, 53], offset [0, 0], layer `Visual_Assets`. Sunken court approach
- `spr_pebbles` at [98, 68], offset [0, 0], layer `Visual_Assets`. Sundial west cloister
- `spr_bush_dead` at [94, 73], offset [0, 0], layer `Visual_Assets`. Sundial west cloister
- `spr_pebbles` at [118, 74], offset [0, 0], layer `Visual_Assets`. Sundial east cloister
- `spr_bush_dead` at [117, 70], offset [0, 0], layer `Visual_Assets`. Sundial east cloister
- `spr_pebbles` at [135, 60], offset [0, 0], layer `Visual_Assets`. Processional road return
- `spr_bush_dead` at [132, 60], offset [0, 0], layer `Visual_Assets`. Processional road return
- `spr_pebbles` at [124, 41], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones
- `spr_bush_dead` at [127, 47], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones
- `spr_column_whole` at [145, 30], offset [0, 0], layer `Instances`. Courtyard wall sentinels
- `spr_column_broken` at [149, 27], offset [0, 0], layer `Instances`. Courtyard wall sentinels
- `spr_pebbles` at [149, 24], offset [0, 0], layer `Visual_Assets`. Courtyard wall sentinels
- `spr_bush_dead` at [148, 27], offset [0, 0], layer `Visual_Assets`. Courtyard wall sentinels
- `spr_pebbles` at [151, 22], offset [0, 0], layer `Visual_Assets`. Sealed threshold rubble
- `spr_bush_dead` at [152, 28], offset [0, 0], layer `Visual_Assets`. Sealed threshold rubble
- `spr_loose_rocks` at [44, 56], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [71, 46], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [75, 46], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [68, 49], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [109, 46], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [37, 5], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [41, 5], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [34, 8], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [100, 15], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_column_broken` at [117, 59], offset [0, 0], layer `Instances`. Treasure approach
- `spr_ruin_block` at [121, 59], offset [0, 0], layer `Instances`. Treasure approach
- `spr_loose_rocks` at [114, 62], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [18, 31], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [66, 30], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [97, 45], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_loose_rocks` at [136, 61], offset [0, 0], layer `Visual_Assets`. Treasure approach
- `spr_pebbles` at [23, 52], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_tree_dead` at [40, 36], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_pebbles` at [51, 34], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [71, 44], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_pebbles` at [24, 15], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_tree_dead` at [92, 11], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_column_fallen` at [96, 11], offset [0, 0], layer `Instances`. Encounter perimeter
- `spr_pebbles` at [89, 14], offset [0, 0], layer `Visual_Assets`. Encounter perimeter
- `spr_column_whole` at [79, 68], offset [0, 0], layer `Instances`. Sundial west cloister — trail-edge continuation
- `spr_column_whole` at [82, 71], offset [0, 0], layer `Instances`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [81, 65], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_column_whole` at [105, 80], offset [0, 0], layer `Instances`. Sundial east cloister — trail-edge continuation
- `spr_column_whole` at [108, 83], offset [0, 0], layer `Instances`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [107, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_tree_dead` at [10, 13], offset [0, 0], layer `Instances`. Plateau windbreak — trail-edge continuation
- `spr_tree_dead` at [7, 16], offset [0, 0], layer `Instances`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [13, 16], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_tree_dead` at [101, 31], offset [0, 0], layer `Instances`. Forecourt garden remains — trail-edge continuation
- `spr_tree_dead` at [99, 31], offset [0, 0], layer `Instances`. Forecourt garden remains — trail-edge continuation
- `spr_tree_dead` at [16, 65], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_column_whole` at [91, 41], offset [0, 0], layer `Instances`. Memorial stair approach — trail-edge continuation
- `spr_column_whole` at [149, 9], offset [0, 0], layer `Instances`. Sealed threshold rubble — trail-edge continuation
- `spr_pebbles` at [149, 15], offset [0, 0], layer `Visual_Assets`. Sealed threshold rubble — trail-edge continuation
- `spr_pebbles` at [148, 9], offset [0, 0], layer `Visual_Assets`. Sealed threshold rubble — trail-edge continuation
- `spr_pebbles` at [90, 41], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_tree_dead` at [19, 68], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [18, 62], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_tree_dead` at [32, 34], offset [0, 0], layer `Instances`. Grotto approach bones — trail-edge continuation
- `spr_column_whole` at [133, 32], offset [0, 0], layer `Instances`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [136, 35], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_column_whole` at [105, 77], offset [0, 0], layer `Instances`. Sundial west cloister — trail-edge continuation
- `spr_column_whole` at [120, 49], offset [0, 0], layer `Instances`. Last refuge votive stones — trail-edge continuation
- `spr_column_broken` at [89, 48], offset [0, 0], layer `Instances`. Sunken court approach — trail-edge continuation
- `spr_column_whole` at [117, 50], offset [0, 0], layer `Instances`. Last refuge votive stones — trail-edge continuation
- `spr_tree_dead` at [51, 61], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [18, 66], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [105, 66], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_tree_dead` at [18, 21], offset [0, 0], layer `Instances`. Plateau windbreak — trail-edge continuation
- `spr_supply_barrel` at [97, 33], offset [0, 0], layer `Instances`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [137, 48], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [51, 62], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_column_whole` at [89, 63], offset [0, 0], layer `Instances`. Sundial west cloister — trail-edge continuation
- `spr_tree_dead` at [30, 24], offset [0, 0], layer `Instances`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [90, 62], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [31, 32], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [124, 59], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_column_whole` at [61, 19], offset [0, 0], layer `Instances`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [62, 19], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [140, 51], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_column_broken` at [77, 57], offset [0, 0], layer `Instances`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [128, 72], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_column_broken` at [46, 10], offset [0, 0], layer `Instances`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [43, 13], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [48, 10], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_pebbles` at [115, 18], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_tree_dead` at [16, 21], offset [0, 0], layer `Instances`. Plateau windbreak — trail-edge continuation
- `spr_tree_dead` at [14, 53], offset [0, 0], layer `Instances`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [113, 58], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_column_whole` at [127, 63], offset [0, 0], layer `Instances`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [127, 64], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [85, 71], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [115, 34], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_column_whole` at [136, 39], offset [0, 0], layer `Instances`. Last refuge votive stones — trail-edge continuation
- `spr_tree_dead` at [28, 69], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_column_whole` at [115, 20], offset [0, 0], layer `Instances`. Memorial offerings — trail-edge continuation
- `spr_column_whole` at [115, 79], offset [0, 0], layer `Instances`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [103, 35], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_tree_dead` at [115, 58], offset [0, 0], layer `Instances`. Forecourt garden remains — trail-edge continuation
- `spr_column_whole` at [145, 53], offset [0, 0], layer `Instances`. Processional road return — trail-edge continuation
- `spr_pebbles` at [148, 56], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_column_whole` at [149, 13], offset [0, 0], layer `Instances`. Sealed threshold rubble — trail-edge continuation
- `spr_pebbles` at [119, 31], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_loose_rocks` at [77, 49], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_tree_dead` at [15, 56], offset [0, 0], layer `Instances`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [145, 55], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [15, 59], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [114, 78], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_tree_dead` at [95, 41], offset [0, 0], layer `Instances`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [136, 41], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [79, 42], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_column_broken` at [79, 47], offset [0, 0], layer `Instances`. Sunken court approach — trail-edge continuation
- `spr_column_whole` at [129, 49], offset [0, 0], layer `Instances`. Processional road return — trail-edge continuation
- `spr_column_whole` at [95, 59], offset [0, 0], layer `Instances`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [27, 69], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_column_whole` at [145, 67], offset [0, 0], layer `Instances`. Processional road return — trail-edge continuation
- `spr_pebbles` at [111, 9], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_tree_dead` at [32, 24], offset [0, 0], layer `Instances`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [29, 24], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [103, 36], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_column_whole` at [68, 55], offset [0, 0], layer `Instances`. Broken royal procession — trail-edge continuation
- `spr_loose_rocks` at [78, 60], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [27, 68], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [127, 71], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_column_whole` at [134, 75], offset [0, 0], layer `Instances`. Sundial east cloister — trail-edge continuation
- `spr_column_whole` at [90, 76], offset [0, 0], layer `Instances`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [98, 79], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [84, 23], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [97, 32], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_column_whole` at [54, 31], offset [0, 0], layer `Instances`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [126, 32], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [89, 41], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_tree_dead` at [38, 46], offset [0, 0], layer `Instances`. Southern return marker — trail-edge continuation
- `spr_loose_rocks` at [90, 48], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_loose_rocks` at [88, 50], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [117, 49], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [128, 50], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [138, 51], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [103, 58], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [40, 55], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [128, 63], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [136, 75], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_column_whole` at [145, 72], offset [0, 0], layer `Instances`. Processional road return — trail-edge continuation
- `spr_column_whole` at [50, 12], offset [0, 0], layer `Instances`. Causeway warning cairns — trail-edge continuation
- `spr_column_whole` at [52, 14], offset [0, 0], layer `Instances`. Causeway warning cairns — trail-edge continuation
- `spr_column_whole` at [62, 21], offset [0, 0], layer `Instances`. Causeway warning cairns — trail-edge continuation
- `spr_column_fallen` at [20, 22], offset [0, 0], layer `Instances`. Grotto approach bones — trail-edge continuation
- `spr_tree_dead` at [40, 46], offset [0, 0], layer `Instances`. Southern return marker — trail-edge continuation
- `spr_pebbles` at [128, 58], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_column_broken` at [79, 62], offset [0, 0], layer `Instances`. Sunken court approach — trail-edge continuation
- `spr_column_broken` at [91, 60], offset [0, 0], layer `Instances`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [106, 77], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [50, 13], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [51, 16], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [115, 21], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [77, 20], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [76, 20], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_column_fallen` at [19, 24], offset [0, 0], layer `Instances`. Grotto approach bones — trail-edge continuation
- `spr_loose_rocks` at [34, 24], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_tree_dead` at [28, 33], offset [0, 0], layer `Instances`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [89, 31], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_tree_dead` at [7, 41], offset [0, 0], layer `Instances`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [40, 45], offset [0, 0], layer `Visual_Assets`. Southern return marker — trail-edge continuation
- `spr_pebbles` at [115, 57], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_tree_dead` at [51, 55], offset [0, 0], layer `Instances`. Southern return marker — trail-edge continuation
- `spr_pebbles` at [27, 67], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_tree_dead` at [48, 66], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [91, 71], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [100, 77], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [110, 9], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_column_broken` at [42, 11], offset [0, 0], layer `Instances`. Echo shrine offerings — trail-edge continuation
- `spr_pebbles` at [113, 17], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [113, 16], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [10, 17], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [11, 17], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_column_whole` at [113, 21], offset [0, 0], layer `Instances`. Memorial offerings — trail-edge continuation
- `spr_column_whole` at [80, 20], offset [0, 0], layer `Instances`. Memorial stair approach — trail-edge continuation
- `spr_loose_rocks` at [43, 23], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [38, 32], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_column_whole` at [118, 29], offset [0, 0], layer `Instances`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [90, 29], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [87, 34], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_tree_dead` at [52, 32], offset [0, 0], layer `Instances`. Southern return marker — trail-edge continuation
- `spr_pebbles` at [99, 33], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [129, 34], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [128, 34], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [79, 43], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [134, 40], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [94, 41], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [99, 40], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [111, 38], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_tree_dead` at [26, 42], offset [0, 0], layer `Instances`. Burrowed trail edge — trail-edge continuation
- `spr_loose_rocks` at [79, 48], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_loose_rocks` at [75, 56], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [103, 49], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [116, 57], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [127, 50], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_tree_dead` at [106, 59], offset [0, 0], layer `Instances`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [147, 60], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [18, 61], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [18, 65], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [25, 59], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [28, 62], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [117, 66], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [146, 71], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [106, 69], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [146, 72], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [98, 77], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [115, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [116, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [115, 70], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [128, 76], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [53, 20], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [113, 22], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [113, 23], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [68, 20], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [61, 21], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [20, 23], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [30, 32], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [31, 24], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [18, 24], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [32, 32], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [23, 30], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_loose_rocks` at [37, 32], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_pebbles` at [88, 41], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [78, 38], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_loose_rocks` at [88, 49], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_column_whole` at [121, 57], offset [0, 0], layer `Instances`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [41, 57], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [91, 64], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_column_whole` at [134, 73], offset [0, 0], layer `Instances`. Processional road return — trail-edge continuation
- `spr_pebbles` at [100, 69], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_loose_rocks` at [40, 6], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_pebbles` at [107, 10], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [22, 11], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_loose_rocks` at [43, 14], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_pebbles` at [21, 12], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [101, 13], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [103, 16], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [103, 17], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_column_whole` at [87, 17], offset [0, 0], layer `Instances`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [148, 14], offset [0, 0], layer `Visual_Assets`. Courtyard wall sentinels — trail-edge continuation
- `spr_pebbles` at [148, 15], offset [0, 0], layer `Visual_Assets`. Courtyard wall sentinels — trail-edge continuation
- `spr_pebbles` at [20, 17], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [51, 17], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [5, 24], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [16, 23], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [4, 25], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [17, 23], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [3, 25], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [7, 23], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [102, 21], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [113, 24], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [104, 23], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_column_whole` at [86, 23], offset [0, 0], layer `Instances`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [53, 24], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [67, 21], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [77, 22], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [75, 27], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [54, 26], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [54, 27], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [64, 25], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_loose_rocks` at [34, 23], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [33, 24], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [44, 23], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [45, 23], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [33, 23], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [40, 30], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_pebbles` at [86, 25], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [22, 30], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [33, 32], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [31, 26], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_pebbles` at [32, 26], offset [0, 0], layer `Visual_Assets`. Grotto approach bones — trail-edge continuation
- `spr_loose_rocks` at [39, 32], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_loose_rocks` at [31, 30], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_bush_dead` at [36, 32], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_bush_dead` at [40, 32], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_bush_dead` at [35, 32], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_bush_dead` at [34, 32], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_bush_dead` at [38, 25], offset [0, 0], layer `Visual_Assets`. Echo shrine offerings — trail-edge continuation
- `spr_pebbles` at [116, 28], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [114, 31], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [125, 28], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_column_whole` at [127, 29], offset [0, 0], layer `Instances`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [104, 28], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [103, 29], offset [0, 0], layer `Visual_Assets`. Memorial offerings — trail-edge continuation
- `spr_column_whole` at [104, 31], offset [0, 0], layer `Instances`. Memorial offerings — trail-edge continuation
- `spr_pebbles` at [54, 32], offset [0, 0], layer `Visual_Assets`. Causeway warning cairns — trail-edge continuation
- `spr_pebbles` at [80, 31], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_pebbles` at [7, 35], offset [0, 0], layer `Visual_Assets`. Plateau windbreak — trail-edge continuation
- `spr_pebbles` at [87, 35], offset [0, 0], layer `Visual_Assets`. Memorial stair approach — trail-edge continuation
- `spr_supply_barrel` at [101, 33], offset [0, 0], layer `Instances`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [61, 33], offset [0, 0], layer `Visual_Assets`. Broken royal procession — trail-edge continuation
- `spr_bush_dead` at [98, 33], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_bush_dead` at [100, 33], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_bush_dead` at [93, 41], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_bush_dead` at [102, 33], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_bush_dead` at [92, 41], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_bush_dead` at [103, 33], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_bush_dead` at [97, 40], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [114, 38], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [134, 41], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [134, 42], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [135, 34], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [125, 38], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [62, 41], offset [0, 0], layer `Visual_Assets`. Broken royal procession — trail-edge continuation
- `spr_pebbles` at [105, 42], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [10, 44], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [26, 41], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [117, 46], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [118, 46], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [113, 40], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [125, 40], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [13, 44], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [41, 43], offset [0, 0], layer `Visual_Assets`. Southern return marker — trail-edge continuation
- `spr_tree_dead` at [52, 43], offset [0, 0], layer `Instances`. Southern return marker — trail-edge continuation
- `spr_tree_dead` at [40, 40], offset [0, 0], layer `Instances`. Southern return marker — trail-edge continuation
- `spr_supply_barrel` at [39, 43], offset [0, 0], layer `Instances`. Southern return marker — trail-edge continuation
- `spr_loose_rocks` at [79, 45], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_loose_rocks` at [79, 44], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_loose_rocks` at [92, 42], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_loose_rocks` at [85, 42], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [16, 49], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [61, 51], offset [0, 0], layer `Visual_Assets`. Broken royal procession — trail-edge continuation
- `spr_pebbles` at [40, 50], offset [0, 0], layer `Visual_Assets`. Southern return marker — trail-edge continuation
- `spr_pebbles` at [105, 48], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [117, 48], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [104, 48], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [106, 52], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [50, 52], offset [0, 0], layer `Visual_Assets`. Southern return marker — trail-edge continuation
- `spr_loose_rocks` at [76, 55], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_loose_rocks` at [85, 55], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [106, 55], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [115, 55], offset [0, 0], layer `Visual_Assets`. Forecourt garden remains — trail-edge continuation
- `spr_pebbles` at [16, 50], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge — trail-edge continuation
- `spr_column_fallen` at [17, 54], offset [0, 0], layer `Instances`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [126, 50], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [16, 53], offset [0, 0], layer `Visual_Assets`. Burrowed trail edge — trail-edge continuation
- `spr_pebbles` at [125, 58], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_pebbles` at [125, 56], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_bush_dead` at [120, 57], offset [0, 0], layer `Visual_Assets`. Last refuge votive stones — trail-edge continuation
- `spr_bush_dead` at [127, 58], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_bush_dead` at [126, 58], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_bush_dead` at [125, 50], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_bush_dead` at [124, 50], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_bush_dead` at [123, 50], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_bush_dead` at [123, 58], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_bush_dead` at [132, 52], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [138, 54], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_pebbles` at [136, 57], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_tree_dead` at [49, 55], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_tree_dead` at [38, 55], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_column_fallen` at [49, 59], offset [0, 0], layer `Instances`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [37, 61], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [49, 60], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [49, 58], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [50, 60], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [50, 64], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [40, 56], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [40, 64], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_loose_rocks` at [49, 61], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_loose_rocks` at [49, 62], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_loose_rocks` at [49, 57], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_loose_rocks` at [49, 63], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_loose_rocks` at [49, 56], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_loose_rocks` at [49, 64], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_loose_rocks` at [40, 62], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [146, 61], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_loose_rocks` at [79, 61], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [18, 67], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [27, 61], offset [0, 0], layer `Visual_Assets`. Worm hunter's remains — trail-edge continuation
- `spr_pebbles` at [97, 59], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [94, 59], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [103, 59], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [91, 65], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_bush_dead` at [96, 59], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_bush_dead` at [98, 59], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_bush_dead` at [99, 59], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_bush_dead` at [100, 59], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_bush_dead` at [91, 63], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_bush_dead` at [90, 63], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_bush_dead` at [97, 66], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [114, 63], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [117, 64], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [138, 63], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_loose_rocks` at [79, 66], offset [0, 0], layer `Visual_Assets`. Sunken court approach — trail-edge continuation
- `spr_pebbles` at [127, 70], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_column_broken` at [130, 72], offset [0, 0], layer `Instances`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [85, 72], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [89, 72], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [140, 74], offset [0, 0], layer `Visual_Assets`. Processional road return — trail-edge continuation
- `spr_bush_dead` at [103, 72], offset [0, 0], layer `Visual_Assets`. Sundial west cloister — trail-edge continuation
- `spr_pebbles` at [115, 71], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_bush_dead` at [109, 69], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_bush_dead` at [113, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_bush_dead` at [104, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_bush_dead` at [114, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_bush_dead` at [103, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_bush_dead` at [109, 70], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation
- `spr_pebbles` at [125, 77], offset [0, 0], layer `Visual_Assets`. Sundial east cloister — trail-edge continuation

Every required asset ID (including shared character/combat families) is enumerated for this scene in `scene_gameplay_specs.json` and `scene_asset_manifest.json`. These are incoming requirements; exact prop aliases and animation suffixes still need Claude's asset mapping. Weather suppression rectangles are explicit in this scene's sidecar entry.

`mus_desert`, `mus_ending`, `mus_pharaoh`, `snd_bat_screech`, `snd_boss_death`, `snd_boss_hurt`, `snd_boss_summon`, `snd_cast_charge`, `snd_checkpoint`, `snd_chest_open`, `snd_disintegrate`, `snd_gate_slam`, `snd_laser_charge`, `snd_laser_fire`, `snd_magic_hit`, `snd_magic_travel`, `snd_pickup`, `snd_save`, `snd_snake_hiss`, `snd_snake_lunge`, `snd_step_sand`, `snd_sword_hit`, `snd_sword_swing`, `snd_thunder_strike`, `snd_thunder_warn`, `snd_undead_rise`, `snd_wind_loop`, `snd_worm_bite`, `snd_worm_emerge`, `snd_worm_rumble`, `spr_bandit_attack_down`, `spr_bandit_attack_side`, `spr_bandit_attack_up`, `spr_bandit_caster_attack_down`, `spr_bandit_caster_attack_side`, `spr_bandit_caster_attack_up`, `spr_bandit_caster_defeat`, `spr_bandit_caster_hurt_down`, `spr_bandit_caster_idle_down`, `spr_bandit_caster_walk_down`, `spr_bandit_caster_walk_side`, `spr_bandit_caster_walk_up`, `spr_bandit_defeat`, `spr_bandit_hurt_down`, `spr_bandit_idle_down`, `spr_bandit_walk_down`, `spr_bandit_walk_side`, `spr_bandit_walk_up`, `spr_bat_defeat`, `spr_bat_dive`, `spr_bat_fly`, `spr_bush`, `spr_bush_dead`, `spr_checkpoint_star`, `spr_chest_desert`, `spr_column_broken`, `spr_column_fallen`, `spr_column_whole`, `spr_dave_attack_down`, `spr_dave_attack_down_side`, `spr_dave_attack_side`, `spr_dave_attack_up`, `spr_dave_attack_up_side`, `spr_dave_idle_down`, `spr_dave_idle_down_side`, `spr_dave_idle_side`, `spr_dave_idle_up`, `spr_dave_idle_up_side`, `spr_dave_walk_down`, `spr_dave_walk_down_side`, `spr_dave_walk_side`, `spr_dave_walk_up`, `spr_dave_walk_up_side`, `spr_door_sealed`, `spr_dungeon_entrance`, `spr_ending_bg`, `spr_fx_hit`, `spr_fx_laser_charge`, `spr_fx_magic_hit`, `spr_fx_magic_launch`, `spr_fx_sand_burst`, `spr_fx_slash`, `spr_fx_sparkle`, `spr_fx_thunder_impact`, `spr_gate_arena`, `spr_icon_ancient_coin`, `spr_icon_desert_rose`, `spr_icon_golden_scarab`, `spr_icon_paladin_mail`, `spr_icon_pharaoh_ankh`, `spr_icon_potion_greater`, `spr_icon_sunsteel_blade`, `spr_laser_aim`, `spr_laser_beam`, `spr_lightning_bolt`, `spr_loose_rocks`, `spr_magic_orb`, `spr_mask_bat`, `spr_mask_dave`, `spr_mask_medium`, `spr_mask_pharaoh`, `spr_mask_python`, `spr_mask_sandworm`, `spr_obelisk`, `spr_palm`, `spr_pebbles`, `spr_pharaoh_death`, `spr_pharaoh_hurt`, `spr_pharaoh_idle`, `spr_pharaoh_laser_charge`, `spr_pharaoh_laser_fire`, `spr_pharaoh_statue`, `spr_pharaoh_summon`, `spr_pharaoh_teleport_in`, `spr_pharaoh_teleport_out`, `spr_pharaoh_thunder_cast`, `spr_portrait_dave`, `spr_portrait_pharaoh`, `spr_python_coil`, `spr_python_defeat`, `spr_python_hurt`, `spr_python_lunge_down`, `spr_python_lunge_side`, `spr_python_lunge_up`, `spr_python_slither_down`, `spr_python_slither_side`, `spr_python_slither_up`, `spr_rock_small`, `spr_ruin_block`, `spr_sandworm_attack`, `spr_sandworm_burrow`, `spr_sandworm_defeat`, `spr_sandworm_emerge`, `spr_sandworm_hurt`, `spr_sandworm_idle_up`, `spr_sandworm_mound`, `spr_skeleton_warrior_attack_down`, `spr_skeleton_warrior_attack_side`, `spr_skeleton_warrior_attack_up`, `spr_skeleton_warrior_defeat`, `spr_skeleton_warrior_hurt_down`, `spr_skeleton_warrior_idle_down`, `spr_skeleton_warrior_walk_down`, `spr_skeleton_warrior_walk_side`, `spr_skeleton_warrior_walk_up`, `spr_skull`, `spr_summon_crack`, `spr_supply_barrel`, `spr_thunder_exclaim`, `spr_thunder_marker`, `spr_tree_dead`, `spr_tumbleweed`, `spr_undead_attack_down`, `spr_undead_attack_side`, `spr_undead_attack_up`, `spr_undead_defeat`, `spr_undead_hurt_down`, `spr_undead_idle_down`, `spr_undead_rise`, `spr_undead_walk_down`, `spr_undead_walk_side`, `spr_undead_walk_up`, `spr_water_barrel`, `tex_chasm_void`, `tex_chasm_wall`, `tex_cliff_face`, `tex_grass`, `tex_masonry_face`, `tex_masonry_top`, `tex_paving`, `tex_rock_top`, `tex_sand_dark`, `tex_sand_light`, `ts_bridge`, `ts_stairs`.
