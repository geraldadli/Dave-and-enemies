# Desert chapter - expanding scene world

**Current design: desert_scenes_v2.** The chapter is organized around a few large, continuously explorable scenes. The earlier 24-small-map design and six room batches are superseded. Scene count is not a design target or a claimed FFV count. Build exploration depth, connected landscapes and recognizable places; expand the extents when playtests show a useful destination or route.

Use **scene** for a landscape that loads as one continuous world area, and **place** for a landmark or district within it. A place boundary never causes a fade, load, teleport or enemy reset. GameMaker still calls its technical resource a room: the `room_id`/`rm_` keys below retain Claude's format, while design and player language use scene. This revision changes the geography and connections, rather than renaming the old small maps.

## World structure

```mermaid
flowchart LR
  F[Desert Frontier] <--> B[Caravan Basin]
  B <--> R[Royal Expanse]
  R --> END[Dungeon doorway - To Be Continued]
```

Only the two landscape passes change scenes. All earlier optional branches become explorable pockets or returning circuits inside these landscapes. The Pharaoh courtyard and dungeon exterior are distinct places within Royal Expanse; the fight, whiteout and victory walk do not load another landscape.

| Scene | Starting extent | Main landmarks in preferred eastward order | Exploration expansion |
|---|---|---|---|
| [Desert Frontier](scene_desert_frontier.md) | 128 x 80 tiles | Desert Arrival, Dune Trail, Canyon Approach, Split Cliffs, Dry Wash, Oasis Refuge | Two-stair lookout loop, southern canyon/wash bypass, both oasis banks and Hidden Spring |
| [Caravan Basin](scene_caravan_basin.md) | 144 x 88 tiles | Ruined Caravan, Cactus Flats, Bonefield, Broken Bridge, Forgotten Ruins, Great Desert Stairs | Northern bandit camp circuit, two intact crossings of the chasm, exposed cistern with rim/catwalk loop, upper-shelf treasure |
| [Royal Expanse](scene_royal_expanse.md) | 160 x 96 tiles | Windblown Plateau, Royal Causeway, Tomb Approach, Pharaoh's Gate, Pharaoh's Courtyard, Dungeon Threshold | Open grotto circuit, elective worm basin, two-stair memorial terrace, new Sundial Court circuit, quiet forecourt and physically gated boss arena |

The original route order remains the recommended journey and landmark sequence. It is not an invisible checklist forcing every district to be visited. Players can wander north or south, choose a longer approach, spot treasure from another elevation, return along another path and backtrack across scene passes. The boss remains the only progression lock to the dungeon exterior. Saves at oasis, ruins and the final star remain player initiated.

## Exploration rhythm and scene expansion

Start with the opening basin and its first visible distant destination. Add the lookout as a connected elevated loop, then extend the canyon/wash routes into the oasis. A new place should offer a recognizable silhouette, a view toward another destination, a route choice and either a reward or a useful return. Avoid long empty strips added merely to enlarge the tile dimensions.

Caravan Basin develops that vocabulary: the broken span is a landmark, the main bridge is a clear route, and the southern bridge/cistern circuit rewards exploring the wider landscape. Royal Expanse gives more open ground before the causeway, an elective grotto and worm basin, then a calmer royal forecourt before the final gate. Quiet travel surrounds the dense combat pockets; do not scatter enemies evenly across every open tile.

Implementation batches are expansions of a shared scene: establish the travel floor and landmark relationships, add one complete returning loop, then extend toward the next anchor. Batch edges must never become player-facing doors, temporary shipping walls or extra scene transitions. Each scene document supplies the implementation batches, full world grid data, reduced overview, detailed place crops, exact placements and local route circuits.

## Coordinate, collision and transition rules

64-pixel tiles; cells `[x,y]` start at zero in each scene, X east and Y south. Ground points are `[64*x+32,64*y+32]` pixels. Rectangles include both endpoints. Every scene JSON contains the full exact tile grid. Overview diagrams reduce 4 x 4 tiles to one character, while place crops show one character per tile and state their global origin.

Legend: `.` sand, `,` dark path, `;` grass, `~` blocked water, `#` blocked cliff/rock, `M` blocked masonry, `_` paving, `^` stairs, `C` blocked chasm, `=` E/W bridge, `|` N/S bridge, `x` blocked broken span. Diagram overlays: `e` enemy, `c` chest, `S` star, `p` solid prop base, `a` scene arrival, `i` initial spawn, `g` boss gate, `t` scripted trigger. Decoration is separate and never determines collision.

Primary paths and exploration circuits support a three-tile-wide route. Most painted paths are five wide; stair and bridge widths are explicit. All ordinary combat pockets have at least 7 x 7 unobstructed tiles, usually larger in this revision. Characters use the contract's foot masks, props collide only at their listed bases, and chests have reachable interaction cells plus a clear three-wide approach. No jump, swim, movement upgrade, optional equipment or grinding is required.

Scene passes are five tiles wide. Safe arrival is two indices inside the matching exit, with a clear 3 x 3 reserve and five-deep corridor. Transitions require deliberate outward crossing; pause damage during load, clear incoming projectiles and debounce until Dave leaves the destination corridor and releases outward intent. Combat leashes, projectiles, summons and scenery never occupy these reserves or structure landings.

## Boss, final checkpoint and ending

The final star is at Royal Expanse `[122,38]`, seven tiles south of the entrance gate `[121..123,31]`. Dave walks straight toward it within the same scene. The narrow throat's row28 trigger is unavoidable; test continuously while idle until his full mask is north of pixel y1856, pause damage, walk to `[122,26]`, close the entrance and play `boss_intro`. Skipping dialogue initializes the same encounter. Start `mus_pharaoh` only when dialogue completes.

The paved courtyard has no solid props in its combat floor. The Pharaoh begins at `[132,20]`, with authored teleport and summon points in the sidecar. Keep all attacks and committed warnings visible at 1280 x 720. Capped summons and committed thunder targets preserve a connected safe strip at least three tiles wide; actual movement speed and warning timing require Claude's playtest. Optional premium equipment cannot be assumed for boss balance.

The eastern seal at `[148,17..149,21]` physically isolates the dungeon exterior until victory. There is no route around the courtyard through the wider landscape. On defeat, stop all damage, disintegrate, fade slowly to white, remove the boss/summons/projectiles/hazards, fade back and reopen both barriers. Atomically persist `boss_pharaoh_defeated` plus pending unique reward `rm_sc_royal_expanse:u1`. Then walk into the dungeon exterior, still within the same scene. Doorway `[153..154,12]` triggers **To Be Continued**. No interior or Grail recovery is specified.

## Current handoff files and persistence

- `design/desert/scenes/*.json`: current full-scene terrain and object data using Claude's contract keys; no north/south exit schema extension is needed.
- `scene_manifest.json`: authoritative scene graph, conventions and world rules.
- `scene_gameplay_specs.json`: places, broad route polylines, returning circuits, combat pockets, arrivals, checkpoints, exact triggers/barriers and per-scene required asset IDs.
- `scene_decorations.json`: noncolliding art only; solid prop bases remain in gameplay data.
- `scene_asset_manifest.json`: per-scene required IDs and source availability; IDs remain requirements rather than a claim that all art is imported.
- `scene_migration.json`: maps old draft chest IDs, checkpoint locations, places and unique reward to the current scenes. Stable enemy spawn IDs are retained. Claude must migrate save identity and checkpoint positions together, or explicitly version old saves as incompatible; never load old local coordinates into a new landscape.
- `scene_validation_report.json`: current static topology results. The old v1 report applies only to the superseded layouts.

The earlier `rooms/*.json`, old gameplay/decor manifests, old atlas and `batch_01` through `batch_06` documents are reference material, not the current import list. The user's scene-world directive replaces the provisional 18+6 resource naming/count in PROJECT_CONTRACT section 8 and the x24 layouts request in ASSET_REQUESTS C5; it retains their tile size, core data keys, masks, art formats and layers. No GameMaker resources, code or Claude-owned contract have been edited by this design handoff.

Fixed geometry, landmarks, chest/reward claims, enemy defeats, bridges, checkpoints and boss flags persist across revisits. Crossing a place or a renderer/AI chunk never resets content. Only cosmetic material/decal variation and bounded E-to-W wind may be procedural; never generate solid obstacles or rearrange routes. Preserve a cosmetic seed. Suppress weather around save refuges, final gate, arena, threshold and important silhouettes.

Save the whole snapshot together: scene/checkpoint, stats/XP, inventory, defeated spawn IDs, remaining chest contents, pending reward and flags. Death rolls it back together. An undefeated boss snapshot recreates an idle encounter; a defeated one recreates the cleared courtyard. If inventory is full, leave unclaimed chest contents and the unique reward available. Completed saves may replay the ending doorway.

## Preview and validation

[Full scene atlas](../../design/desert/previews/scene_world_atlas.png). Regenerate design with `python tools/design_desert_scenes.py`; check exported files with `python tools/validate_desert_scenes.py`.

The static validator checks exact tile sizes, connected travel floor, three-wide primary/circuit paths, reachable treasure, safe passes, clear combat pockets/structure landings, checkpoint peace, matching destinations, unavoidable boss trigger and sealed/cleared dungeon access. This guarantees the authored static topology under the conservative collision model. Claude still needs GameMaker tests for AI, melee arcs, camera/telegraph visibility, real movement speed, gate timing, save migration/rollback, whiteout cleanup and ending replay. Large scene data does not imply the engine already supports streaming or that runtime performance has been tested.

## Content-focused layout revision

The scene extents stay large, but unused sand is folded into irregular rock shoulders. Routes widen into distinct destinations rather than crossing a uniformly open basin. Authored scenery beats use caravan cargo, cactus shelters, bone trails, green banks and ceremonial ruins. Static placement is rebuilt by `focus_desert_layouts.py`, never randomized during play. Existing spawn identities, loot, stars, circuits and gates remain authoritative.

Travel views target four persistent details and two landmark silhouettes; combat approaches use a lighter two-detail frame, with the full fighting pads and warning floor clear. Quiet refuges receive scenery outside the actual save interaction reserve. Coverage ignores defeated enemies and follows the camera's border clamping. The central Pharaoh arena deliberately keeps its readable sand/paving floor.

Rebuild imported rooms with `python tools/build_world.py rooms`. Run `python tools/validate_layout_focus.py` after the topology validator. Generate [the actual tile/sprite atlas](../../design/desert/previews/focused_world_rendered.png) and [nine player-view compositions](../../design/desert/previews/focused_camera_review.png) with `python tools/preview_desert_layouts.py`. These are static render reviews; representative native-game checks are documented below.

## Runtime tile export and visibility correction

Terrain rebuilds must regenerate `output_tileset.png`, including two-pixel edge extrusion, with the exact declared output stride. Stale prepared images caused the skull/enemy fragments and checkerboard terrain seen in the original runtime screenshot. Previews now read the same prepared images as the compiler; `validate_compiled_tilesets.py` verifies the packed atlases inside a GameMaker 2026 `.win` file.

Local repeat limits keep obelisks, wagons and identical tree silhouettes from forming rows. Routine ground dressing uses rocks and shrubs; only two authored skull decals remain. Tall scenery becomes 25% opaque when it would cover Dave or an enemy. Prop base collision and clear routes remain intact.

Runtime verification on 2026-10-31 covered eleven views across all scenes and movement past a palm, over the basin bridge and cistern catwalk, and up the Great Desert Stairs. Palm and obelisk transparency were visually inspected. See `design/desert/runtime_layout_report.json`, `runtime_tile_validation_report.json`, and the captured images under `design/desert/previews/runtime/`. One audio-service warning occurred during scripted scene warps; no fatal runtime errors. The chapter now compiles from the command line with explicit project/user/runtime/cache paths.

## Discovery routes and close scenery

Narrow worn trails now bend gently and change width, with sand shoulders and broken stone stretches along the royal procession route. Small returning trails lead to twelve new, optional supply caches. Each has a named camp, garden, overlook or ruin composition; entering it shows a brief discovery caption once per saved run. Cache contents and the discovery flag use existing snapshot persistence. Rewards add consumables and collectibles, with no progression keys or mandatory equipment.

Five scenery variants reuse the template's barrel and column pixels with ground-contact origins and complete opaque silhouette bounds. Build them with `python tools/build_scenery_library.py` before generating the design. Contextual ground materials distinguish planted gardens, survey aprons, shrines and worn cargo areas. Low shrubs and stones can dress route shoulders; the centre line, full fighting pads, treasure approaches, save reserves and structure landings stay readable.

Travel views also require nearby details within the middle 11 by 7 tiles, so a tiny prop at a distant screen edge cannot satisfy the layout review. A green planting can anchor a junction while keeping the view low. Bridge/stair compositions, shores and the deliberately clear Pharaoh court have explicit framing rules. Static inspection compares actual opaque sprite bounds, including camera clamping.

| Scene | New discovery | Persistent cache | Reward |
|---|---|---|---|
| Desert Frontier | Lost Porters' Camp | `rm_sc_desert_frontier:c9` | 1 x potion_health |
| Desert Frontier | Wash Survey Camp | `rm_sc_desert_frontier:c10` | 6 x gold_coins |
| Desert Frontier | Spring Keeper's Niche | `rm_sc_desert_frontier:c11` | 1 x desert_rose |
| Desert Frontier | Buried Palm Garden | `rm_sc_desert_frontier:c12` | 1 x ancient_coin |
| Caravan Basin | Stranded Supply Wagon | `rm_sc_caravan_basin:c9` | 1 x potion_health |
| Caravan Basin | Cactus Shelter | `rm_sc_caravan_basin:c10` | 8 x gold_coins |
| Caravan Basin | Broken Span Overlook | `rm_sc_caravan_basin:c11` | 1 x desert_rose |
| Caravan Basin | Well Keeper's Yard | `rm_sc_caravan_basin:c12` | 1 x potion_health, 3 x gold_coins |
| Royal Expanse | Forgotten Pilgrims' Rest | `rm_sc_royal_expanse:c7` | 1 x potion_greater |
| Royal Expanse | Procession Waystation | `rm_sc_royal_expanse:c8` | 2 x ancient_coin |
| Royal Expanse | Sunken Offering Garden | `rm_sc_royal_expanse:c9` | 1 x desert_rose |
| Royal Expanse | Fallen Archive | `rm_sc_royal_expanse:c10` | 1 x golden_scarab |

[Discovery compositions](../../design/desert/previews/exploration_discoveries_review.png). Rebuild with `python tools/design_desert_scenes.py`, `python tools/build_world.py rooms`, then run both design/layout validators and the compiled-atlas validator.

The final compiled-game discovery run triggered all twelve captions, claimed every new cache, verified that repeated interaction grants no duplicate loot, and crossed the palm lane, bridge, cistern catwalk and stairs. It used the current scene exports and produced no runtime errors or audio warnings. User saves were not written. See [the native verification report](../../design/desert/discovery_runtime_report.json) and [captured discovery views](../../design/desert/previews/exploration_runtime/). These checks cover representative movement and interactions; combat balance and long-session performance remain separate work.
