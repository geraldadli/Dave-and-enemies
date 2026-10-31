"""Author the desert design handoff; never edits GameMaker resources.

All geometry and placements below are authored. Rectangle helpers only expand
fixed tile coordinates; they are not a runtime procedural map generator.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design" / "desert"
DOC = ROOT / "docs" / "level_design"
ROOMS, SPECS, DECOR = {}, {}, {}


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class Map:
    def __init__(self, room_id, name, size, purpose, intensity, batch, floor=".", wall="#"):
        self.id, self.name = room_id, name
        self.w, self.h = size
        self.grid = [[wall] * self.w for _ in range(self.h)]
        self.rect([1, 1, self.w-2, self.h-2], floor)
        self.objects, self.exits = [], []
        self.spec = dict(purpose=purpose, intensity=intensity, batch=batch,
                         entry_spawn=None, encounters=[], chests=[], checkpoints=[],
                         scripts=[], structures=[], elevations=[], route_waypoints=[],
                         terrain_notes=[], collision_footprints=[], landmarks=[],
                         additional_assets=[], state_notes=[])
        self.decoration = []
        self.music = "mus_desert"
        self.weather = dict(sandstorm=True, tumbleweeds=True)
        ROOMS[self.id], SPECS[self.id], DECOR[self.id] = self, self.spec, self.decoration

    def rect(self, r, char):
        x1, y1, x2, y2 = r
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                self.grid[y][x] = char
        return self

    def line(self, points, char=",", width=3):
        r = width // 2
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            assert x1 == x2 or y1 == y2
            for y in range(max(1, min(y1, y2)-r), min(self.h-2, max(y1, y2)+r)+1):
                for x in range(max(1, min(x1, x2)-r), min(self.w-2, max(x1, x2)+r)+1):
                    self.grid[y][x] = char
        return self

    def enemy_group(self, local_id, pad, placements, purpose):
        ids = []
        for n, (kind, cell) in enumerate(placements, 1):
            eid = f"{self.id}:{local_id}:e{n}"
            # Contract room objects carry only its documented keys.
            self.objects.append(dict(type="enemy", enemy=kind, cell=cell))
            ids.append(dict(id=eid, enemy=kind, cell=cell))
        self.spec["encounters"].append(dict(
            id=f"{self.id}:{local_id}", combat_rect=pad, leash_rect=pad,
            enemies=ids, purpose=purpose,
            activation="Player enters combat_rect; no attacks before activation. Respect arrival protection.",
            max_active=len(placements), clear_required=False))
        return self

    def chest(self, n, cell, loot, intention):
        cid = f"{self.id}:c{n}"
        self.objects.append(dict(type="chest", id=cid, cell=cell, loot=loot))
        self.spec["chests"].append(dict(id=cid, cell=cell, loot=loot,
            interaction_cell=[cell[0], cell[1]+1], approach_cell=[cell[0], cell[1]+2],
            interaction_side="south",
            intention=intention, locked=False, footprint_px=[48, 20],
            conservative_blocked_cells=[cell], persistence="opened_chests; partial claims remain pending by chest ID"))
        return self

    def prop(self, prop, cell, footprint_px, blocked_rect=None):
        self.objects.append(dict(type="prop", prop=prop, cell=cell))
        self.spec["collision_footprints"].append(dict(
            prop=prop, cell=cell, footprint_px=footprint_px,
            footprint_anchor="centred on cell ground point",
            blocked_rect=blocked_rect or [*cell, *cell]))
        return self

    def deco(self, prop, cell, note="", landmark=False):
        flat = prop in {"pebbles", "skull", "bush", "bush_dead"}
        entry = dict(id=f"{self.id}:deco{len(self.decoration)+1}", prop=prop,
                     asset_id=f"spr_{prop}", cell=cell, collision=False,
                     offset_px=[0,0],
                     layer="Visual_Assets" if flat else "Instances",
                     depth_policy="fixed_flat_decal" if flat else "sort_by_ground_point_no_collision",
                     note=note)
        self.decoration.append(entry)
        if landmark:
            self.spec["landmarks"].append(dict(decoration_id=entry["id"], description=note))
        return self

    def structure(self, kind, rect, note):
        char = {"stairs":"^", "bridge_ew":"=", "bridge_ns":"|", "broken_bridge":"x"}.get(kind)
        if char:
            self.rect(rect, char)
        self.spec["structures"].append(dict(kind=kind, rect=rect, note=note))
        return self

    def checkpoint(self, cell):
        cid = f"{self.id}:checkpoint"
        self.objects.append(dict(type="checkpoint", cell=cell))
        self.spec["checkpoints"].append(dict(id=cid, cell=cell, respawn_cell=cell,
            safe_rect=[cell[0]-1, cell[1]-1, cell[0]+1, cell[1]+1],
            activation="E interaction; three save slots; heal on successful save; no automatic overwrite"))
        return self

    def path(self, points):
        self.spec["route_waypoints"] = points
        return self

    def notes(self, *notes):
        self.spec["terrain_notes"].extend(notes)
        return self

    def export(self):
        return dict(room_id=self.id, display_name=self.name, size_cells=[self.w, self.h],
            terrain=["".join(row) for row in self.grid], exits=self.exits,
            objects=self.objects, music=self.music, weather=self.weather,
            notes=f"Authored design v1; batch {self.spec['batch']}. See gameplay_specs.json and decorations.json. {self.spec['purpose']}")


def main(n, slug, name, purpose, intensity, batch, size=(36,24)):
    return Map(f"rm_d{n:02}_{slug}", name, size, purpose, intensity, batch)


def optional(n, slug, name, purpose, intensity, batch, size=(32,22)):
    return Map(f"rm_o{n}_{slug}", name, size, purpose, intensity, batch)


# Batch 1: orient, practice, choose, climb for optional equipment.
d1 = main(1,"arrival","Desert Arrival","Orient east after the vow; teach path and chest interaction without combat.","quiet",1)
d1.rect([1,1,7,5],"#").rect([1,18,9,22],"#").rect([27,1,34,4],"#")
d1.line([[2,11],[11,11],[11,9],[22,9],[22,11],[34,11]])
d1.rect([14,6,18,9],"_").chest(1,[16,7],[["potion_health",1]],"A visible, unguarded first potion; learn interaction before danger.")
d1.deco("ruin_block",[5,4],"Breached-city rubble on blocked cliff; west is the past.",True)
d1.deco("tree_dead",[29,3],"Bare silhouette on blocked ground points toward the east gap.",True)
d1.deco("pebbles",[22,16]).deco("bush_dead",[8,16]).prop("cactus_small",[29,18],[16,12])
d1.spec["entry_spawn"] = [3,11]
d1.spec["scripts"] = [dict(id="desert_arrival",trigger_rect=[2,9,7,13],event="chapter_start",once_flag="desert_arrival_seen",note="Intro hands control to Dave facing E at [3,11]. Use narrative-owned text; do not add new dialogue IDs to runtime here.")]
d1.path([[3,11],[11,11],[11,9],[22,9],[22,11],[33,11]])
d1.notes("Northwest rubble and southern cliff shape a broad funnel; all interior sand is walkable.","No water, stairs, bridge, chasm or live hazard. First-death fallback is the initial snapshot at [3,11].")

d2 = main(2,"dune_trail","Dune Trail","One slow attacker in an open bowl, then a visible side chest on a loop.","low",1)
d2.rect([10,3,13,7],"#").rect([6,17,13,21],"#").rect([28,17,34,22],"#")
d2.line([[1,11],[20,11],[33,11]])
d2.line([[22,11],[26,11],[26,6],[30,6]])
d2.enemy_group("g1",[16,7,24,15],[("undead",[20,11])],"Learn windup, sidestep and one swing of recovery. Entire 9 by 9 bowl is clear.")
d2.chest(1,[29,5],[["potion_health",2]],"Supplies after first combat; visible from the eastward path, reached around the dune.")
d2.deco("cactus_tall",[11,5],"A forked cactus on solid dune top marks the chest loop.",True)
d2.deco("pebbles",[6,5]).deco("bush_dead",[30,20])
d2.path([[2,11],[20,11],[33,11]]).notes("Cliff islands only block their # cells. The treasure loop has three-cell lanes.","No water, elevation transition, bridges or encounter lock.")

d3 = main(3,"canyon_approach","Canyon Approach","Reveal a north detour at a canyon marker; two separated fights on the east route.","medium",1)
d3.rect([1,1,6,6],"#").rect([15,1,21,4],"#").rect([1,17,12,22],"#").rect([29,17,34,22],"#")
d3.line([[1,11],[11,11],[11,5],[11,1]])
d3.line([[11,11],[18,11],[18,8],[26,8],[26,11],[34,11]])
d3.enemy_group("g1",[15,5,21,11],[("undead",[18,8])],"An isolated familiar enemy keeps the optional turn legible.")
d3.enemy_group("g2",[23,7,29,13],[("undead",[26,10])],"Second windup practice after a short walk; groups activate separately.")
d3.chest(1,[27,18],[["gold_coins",20]],"A small southern pocket pays for looking away from the dark path.")
d3.prop("obelisk",[8,5],[40,28]).deco("skull",[24,20])
d3.deco("ruin_block",[5,3],"Two incised blocks repeat the notch motif seen in the optional room.",True)
d3.path([[2,11],[11,11],[18,11],[18,8],[26,8],[26,11],[33,11]])
d3.notes("North opening is optional O1; the main exit remains east. Obelisk has a base-only blocker at [8,5].","No water, bridge or stairs here; the first optional climb happens in O1.")

o1 = optional(1,"sunken_lookout","Sunken Lookout","Preview a high chest, turn west to climb, then cross the shelf for the first optional armor.","low",1)
o1.rect([1,1,30,12],"#").rect([3,2,28,10],".").rect([6,11,8,12],"^")
o1.line([[11,20],[11,15],[7,15],[7,13]])
o1.line([[7,10],[7,5],[17,5],[17,7]])
o1.chest(1,[17,9],[["wanderer_tunic",1],["potion_health",1]],"First optional armor and a potion. From the lower basin near [11,13], the chest is six cells east and four north, within the 1280 by 720 view; the west stairs provide access. Interact from its north side.")
o1.spec["chests"][-1].update(interaction_cell=[17,8],approach_cell=[17,7],interaction_side="north")
o1.enemy_group("g1",[11,2,17,8],[("undead",[14,5])],"Optional shelf duel; a clear south edge allows repositioning and retreat to stairs.")
o1.structure("stairs",[6,11,8,12],"Three wide, two deep, bidirectional climb from lower basin z0 to shelf z1; no drop edges.")
o1.spec["elevations"]=[dict(id="basin",level=0,rect=[1,13,30,20]),dict(id="shelf",level=1,rect=[3,2,28,10])]
o1.deco("obelisk",[27,11],"Half-buried lookout marker on the cliff band; never blocks the stair landing.",True)
o1.deco("tree_dead",[29,17],"Silhouette on the far basin rim.",True).deco("pebbles",[17,17])
o1.rect([28,16,30,18],"#")
o1.path([[11,19],[11,13],[11,15],[7,15],[7,10],[7,5],[17,5],[17,7]])
o1.notes("Only stairs connect basin to shelf; # faces are solid and do not support walking on their art.","No water, bridges, jumping, secret wall, key or return lock. Return uses the same stairs and south exit.")

# Batch 2: an internal route loop, a dry river, then the first safe checkpoint.
d4=main(4,"split_cliffs","Split Cliffs","Two reconverging lanes around a cliff island; the upper lane rewards a short climb.","medium",2)
d4.rect([13,9,23,13],"#").rect([1,7,29,8],"#").rect([8,7,11,8],"^").rect([30,1,34,2],"#")
d4.line([[1,11],[7,11],[7,16],[28,16],[28,11],[34,11]])
d4.line([[7,11],[10,11],[10,9]])
d4.line([[10,6],[10,3],[31,3],[31,11]])
d4.chest(1,[25,3],[["ancient_coin",1]],"Upper-lane souvenir; neither lane is mandatory for the other.")
d4.enemy_group("g1",[24,13,32,21],[("skeleton_warrior",[28,16])],"Introduce a firmer melee windup on the broad lower approach, away from stairs.")
d4.structure("stairs",[8,7,11,8],"Four-wide climb to z1 northern ledge. Return by stairs or the broad eastern ramp at x30..33.")
d4.structure("ramp",[30,3,33,10],"Bidirectional sand ramp blends z1 down to z0, clear four-cell width.")
d4.spec["elevations"]=[dict(id="north_ledge",level=1,rect=[1,1,29,6])]
d4.deco("boulder",[18,11],"Split central island divides the two visible routes; art sits on solid cells.",True)
d4.deco("cactus_tall",[17,7]).deco("pebbles",[5,18])
d4.path([[2,11],[7,11],[7,16],[28,16],[28,11],[33,11]])
d4.notes("Main lower lane is flat; upper lane contains stairs and an east ramp. No drop, water, chasm or bridge.")

d5=main(5,"dry_wash","Dry Wash","A quiet riverbed read leads toward palms; the first python guards a voluntary southern pocket.","low",2)
d5.rect([8,2,11,7],"#").rect([17,3,20,6],"#").rect([3,18,12,22],"#")
d5.line([[1,11],[9,11],[9,13],[20,13],[20,11],[34,11]])
d5.line([[13,1],[13,9],[21,9],[21,19],[31,19]])
d5.enemy_group("g1",[23,14,31,20],[("python",[26,17])],"Optional first coil-and-lunge lesson with room to move sideways; path to oasis remains calm.")
d5.chest(1,[33,19],[["potion_health",2]],"Tempt a deliberate step into the wash pocket; not required before the healing checkpoint.")
d5.deco("tree_desert",[18,4],"Dry roots above the wash; green palm silhouette appears beyond the east exit.",True)
d5.deco("palm",[32,3],"Distant oasis cue on solid edge rock; decorative only.",True).deco("pebbles",[14,19])
d5.path([[2,11],[9,11],[9,13],[20,13],[20,11],[33,11]])
d5.notes("Dark sand is a dry wash, not flowing water or quicksand. All , cells have ordinary movement.","No bridge or stairs. Python cannot pursue onto checkpoint approach or within arrival reserves.")

d6=main(6,"oasis_refuge","Oasis Refuge","First full refuge: water, grass, a clear checkpoint and an optional restorative detour.","quiet",2)
d6.rect([8,2,25,10],";").rect([14,4,21,8],"~").rect([12,5,13,7],"~")
d6.line([[1,11],[11,11],[11,2]])
d6.line([[11,11],[34,11]])
d6.rect([23,9,28,13],"_").checkpoint([25,11])
d6.chest(1,[29,6],[["potion_health",2]],"An unguarded emergency reserve beside the refuge; never required to activate the star.")
d6.prop("palm",[8,7],[24,14]).prop("palm",[24,5],[24,14])
d6.deco("bush",[9,3]).deco("bush",[22,9])
d6.deco("ruin_block",[26,4],"A low square of old stone frames the safe star; no new collision.",True)
d6.rect([26,3,27,5],"M")
d6.path([[2,11],[25,11],[33,11]]).notes("All ~ cells are shallow-looking but impassable shoreline; no swimming. The southern shore is at least three clear cells deep.","No enemies, cliffs inside the floor, stairs, bridges or hazards. North exit leads to O2. Save interaction is player initiated.")
d6.weather=dict(sandstorm=False,tumbleweeds=False)

o2=optional(2,"hidden_spring","Hidden Spring","A quiet loop around a spring provides healing and a botanical valuable.","quiet",2)
o2.rect([7,3,24,13],";").rect([12,5,20,9],"~").rect([14,10,19,11],"~")
o2.line([[11,20],[11,15],[7,15],[7,4],[25,4],[25,14],[11,14]])
o2.chest(1,[26,4],[["desert_rose",1]],"A small collectible at the far side of a visible shoreline loop.")
o2.deco("healing_spring",[16,8],"Animated spring sits on blocked water; interact from a separate dry bank trigger.",True)
o2.deco("palm",[3,3],"Nonblocking silhouette beyond the trail; base is drawn on perimeter rock.",True)
o2.rect([2,2,4,4],"#")
o2.spec["scripts"]=[dict(id="hidden_spring_heal",trigger_rect=[15,12,17,13],event="interact_heal",once_flag=None,note="E on dry south bank restores HP; no save UI, item, XP or persistent reward. No effect at full HP.")]
o2.path([[11,19],[11,15],[7,15],[7,4],[25,4]])
o2.notes("Water blocks; the entire outer bank is connected. No combat, cliffs in the route, stairs, bridges, save checkpoint or movement upgrade.")
o2.weather=dict(sandstorm=False,tumbleweeds=False)

# Batch 3: people, a quiet cactus maze, then ranged skeletal pressure.
d7=main(7,"ruined_caravan","Ruined Caravan","Introduce fast melee around a wreck while leaving broad bypass lanes.","medium",3)
d7.rect([1,1,7,4],"#").rect([18,1,25,3],"#").rect([12,19,20,22],"#")
d7.line([[1,11],[13,11],[13,16],[29,16],[29,11],[34,11]])
d7.prop("wagon_wreck",[21,6],[160,40],[20,6,22,6])
d7.enemy_group("g1",[10,6,16,12],[("bandit",[13,9])],"First fast attacker, separated from the wreck footprint and later reinforcement.")
d7.enemy_group("g2",[24,12,30,18],[("bandit",[28,15])],"Repeat the dash-and-recover read while the player chooses which side of the wagon to pass.")
d7.chest(1,[29,5],[["bandit_scimitar",1]],"A weapon sidegrade in abandoned cargo; no unique movement or key function.")
d7.deco("ruin_block",[21,3],"Caravan stone cargo spilled into the north rim.",True).deco("pebbles",[6,18])
d7.path([[2,11],[13,11],[13,16],[29,16],[29,11],[33,11]])
d7.notes("Wagon blocks only its explicit 160 by 40 pixel base; validator conservatively blocks three cells.","No water, cliffs across the lane, stairs, bridge or encounter gate.")

d8=main(8,"cactus_flats","Cactus Flats","A low-pressure grove gives landmark navigation and an optional bandit-cache turn.","low",3)
d8.rect([1,1,5,5],"#").rect([18,2,23,4],"#")
d8.line([[1,11],[11,11],[11,1]])
d8.line([[11,11],[21,11],[21,9],[30,9],[30,11],[34,11]])
for cell in ([7,6],[16,6],[24,5],[6,17],[16,18],[32,18]):
    d8.prop("cactus_tall",list(cell),[24,16])
d8.enemy_group("g1",[23,14,29,20],[("python",[26,17])],"A voluntary southern coil challenge; the central path and north detour stay quiet.")
d8.chest(1,[31,19],[["potion_health",2]],"Recovery for a careful reader of the cactus gaps.")
d8.deco("bush_dead",[20,20]).deco("rock_small",[20,3],"Three dark stones distinguish the north cache trail from the east route.",True)
d8.path([[2,11],[11,11],[21,11],[21,9],[30,9],[30,11],[33,11]])
d8.notes("Cactus collisions use trunks only; no random solid cactus placement. Lanes never narrow below three cells.","North branch O3 is an optional higher-pressure cache. No water, stairs, bridge or chasm.")

d9=main(9,"bonefield","Bonefield","Introduce an archer with a frontal melee distraction, then a short second duel.","high",3)
d9.rect([4,2,8,4],"#").rect([17,2,20,4],"#").rect([6,18,13,22],"#")
d9.line([[1,11],[12,11],[12,8],[27,8],[27,11],[34,11]])
d9.enemy_group("g1",[10,5,18,13],[("skeleton_warrior",[14,9])],"Known melee before exposing the archer; a nine-cell square supports flanking.")
d9.enemy_group("g2",[22,5,30,13],[("skeleton_archer",[28,7]),("skeleton_warrior",[25,11])],"First ranged plus melee mix; approach diagonally on open sand, never along a one-cell funnel.")
d9.chest(1,[28,19],[["ancient_coin",2],["potion_health",1]],"A southern recovery loop after the hardest early group; no mandatory kill lock.")
d9.deco("skull",[7,3],"A few skulls, not a carpet; silhouettes contrast with intact ruin columns ahead.",True)
d9.deco("pebbles",[18,19]).deco("tree_dead",[19,3])
d9.path([[2,11],[12,11],[12,8],[27,8],[27,11],[33,11]])
d9.notes("All skulls and bones are flat decoration; cliff islands alone block. No water, elevation, stairs, bridge or gate.")

o3=optional(3,"bandit_cache","Bandit Cache","A deliberate optional two-enemy challenge rewards armor and a strong restorative.","high",3)
o3.rect([1,1,6,7],"#").rect([25,13,30,20],"#")
o3.line([[11,20],[11,15],[18,15],[18,8],[26,8]])
o3.enemy_group("g1",[14,4,22,12],[("bandit",[16,9]),("bandit_caster",[21,6])],"Optional early spell preview; dodge one visible orb while isolating the fast melee attacker.")
o3.chest(1,[27,4],[["iron_tunic",1],["potion_greater",1]],"Clear optional equipment improvement; never part of the chapter's required power budget.")
o3.prop("wagon_wreck",[7,14],[160,40],[6,14,8,14])
o3.deco("ruin_block",[3,4],"Canvas shelter is implied by cargo on the rock rim; do not invent a new tent asset.",True)
o3.path([[11,19],[11,15],[18,15],[18,8],[26,8],[27,6]])
o3.notes("No ambush spawns, exit lock, water, stairs or bridge. The south approach remains outside the group's leash.")

# Batch 4: bridge repair is NOT required; show a broken choice beside an intact one.
d10=main(10,"broken_bridge","Broken Bridge","Pause combat pressure: read a broken upper span, then use an intact lower bridge.","low",4)
d10.rect([16,1,20,22],"C").rect([16,5,20,7],"x").rect([16,14,20,16],"=")
d10.line([[1,11],[11,11],[11,1]])
d10.line([[11,11],[12,11],[12,15],[14,15]])
d10.line([[22,15],[25,15],[25,11],[34,11]])
d10.enemy_group("g1",[25,15,31,21],[("bat",[28,18])],"One optional bat after crossing; no attacks or aggro on the bridge itself.")
d10.chest(1,[32,19],[["potion_greater",1]],"A safe eastern-bank pocket for players who explore after the crossing.")
d10.structure("broken_bridge",[16,5,20,7],"All x cells are blocked; broken ropes visually expose the missing centre. Never a jump or repair objective.")
d10.structure("bridge_ew",[16,14,20,16],"Intact three-row deck, five cells long, both landings clear at x13..15 and x21..23.")
d10.deco("ruin_block",[13,5],"Broken-span abutment, set away from the intact route.",True)
d10.rect([12,4,14,6],"M")
d10.deco("tree_dead",[30,3],"Far-bank tree is visible across the chasm and anchors orientation.",True)
d10.path([[2,11],[12,11],[12,15],[23,15],[25,15],[25,11],[33,11]])
d10.notes("Chasm and x cells are full blockers; intact = cells replace chasm collision. Add deck-edge rails only along y13/y17, never across landings.","North exit before the chasm leads to O4. No forced combat, dynamic bridge collapse, water or stairs.")

d11=main(11,"forgotten_ruins","Forgotten Ruins","A silent ruined courtyard restores safety and establishes the second checkpoint.","quiet",4)
d11.rect([1,1,34,3],"M").rect([15,4,16,19],"M").rect([15,10,16,12],"_")
d11.line([[1,11],[14,11]],"_").line([[17,11],[34,11]],"_")
d11.rect([23,9,28,13],"_").checkpoint([25,11])
d11.chest(1,[28,18],[["potion_health",2]],"A safe stock-up before the stairs; tucked behind a broken wall end, never hidden by opaque art.")
d11.deco("obelisk",[9,2],"Two intact inscriptions contrast with the broken city rubble from Arrival.",True)
d11.deco("ruin_block",[16,7]).deco("bush_dead",[6,19])
d11.path([[2,11],[25,11],[33,11]])
d11.notes("Masonry divide has a permanent three-cell opening at y10..12. No puzzle or locked door.","No enemies, water, stairs, bridge or active hazard. Wind and tumbleweeds are suppressed.")
d11.weather=dict(sandstorm=False,tumbleweeds=False)

d12=main(12,"great_desert_stairs","Great Desert Stairs","A wide mandatory ascent changes viewpoint and rewards looking back along the upper shelf.","medium",4)
d12.rect([1,9,34,10],"#").rect([17,9,21,10],"^")
d12.line([[1,11],[7,11],[7,15],[19,15],[19,12]])
d12.line([[19,7],[19,5],[34,5]])
d12.enemy_group("g1",[8,12,14,18],[("skeleton_warrior",[11,15])],"One lower-terrace duel; it cannot chase onto the stairs.")
d12.enemy_group("g2",[24,2,30,8],[("skeleton_archer",[28,5])],"An upper-terrace archer approached after a wide, clear landing; no firing through the cliff face.")
d12.chest(1,[6,4],[["ancient_coin",2]],"After ascending, the east exit is clear; looking west along the upper shelf finds a worthwhile detour.")
d12.structure("stairs",[17,9,21,10],"Five wide and two deep; z0 south to z1 north. Landings x17..21 y7..8 and y11..12 are reserved clear.")
d12.spec["elevations"]=[dict(id="lower",level=0,rect=[1,11,34,22]),dict(id="upper",level=1,rect=[1,1,34,8])]
d12.deco("pharaoh_statue",[32,10],"Statue on the cliff face announces the royal plateau.",True)
d12.deco("pebbles",[4,19])
d12.path([[2,11],[7,11],[7,15],[19,15],[19,5],[33,5]])
d12.notes("North and south terraces connect only through ^ cells. No jumping, one-way drops, water or bridge. East opening is y4..6.")

o4=optional(4,"buried_cistern","Buried Cistern","A cool, enemy-free cistern loop rewards the bridge-side detour.","quiet",4)
o4.rect([3,2,28,17],"_").rect([3,2,28,3],"M").rect([9,6,22,12],"~").rect([15,6,17,12],"|")
o4.line([[11,20],[11,15],[16,15],[16,14]],"_")
o4.chest(1,[25,5],[["golden_scarab",1],["potion_greater",1]],"A valuable plus recovery reached by either the outer rim or the central catwalk.")
o4.structure("bridge_ns",[15,6,17,12],"Three-column stone-supported wooden catwalk; replaces water collision. Both landings x15..17 y4..5 and y13..14 stay empty.")
o4.deco("obelisk",[5,3],"Water-measure carving on blocked masonry.",True).deco("bush",[6,15])
o4.path([[11,19],[11,15],[16,15],[16,5],[25,7]])
o4.notes("Water is impassable. The catwalk and outer paved rim form a permanent loop; neither requires a switch. No combat, stairs or drops.")
o4.weather=dict(sandstorm=False,tumbleweeds=False)

# Batch 5: one elective large creature, a harder causeway, then anticipation.
d13=main(13,"windblown_plateau","Windblown Plateau","A wide horizon and quiet upper route reveal an elective sandworm basin and a grotto detour.","low",5)
d13.rect([3,13,10,19],"#").rect([16,3,19,7],"#")
d13.line([[1,5],[11,5],[11,1]])
d13.line([[11,5],[22,5],[22,11],[34,11]])
d13.enemy_group("g1",[23,14,31,20],[("sandworm",[27,17])],"Optional first emergence with a wide lateral escape pad; disturbed sand warns before activation.")
d13.chest(1,[32,19],[["desert_rose",1],["potion_greater",1]],"A visible reward beyond the elective basin; no worm kill flag gates it.")
d13.deco("tree_dead",[7,17],"Wind-scoured tree on a blocked island points west with its branches.",True)
d13.deco("rock_small",[18,5]).deco("pebbles",[28,3])
d13.path([[2,5],[11,5],[22,5],[22,11],[33,11]])
d13.notes("No forced storm hazard or current. All sand is ordinary speed. No bridge, water, stairs or drop.","Sandworm emergence is confined to its authored combat pad; never retarget under arrival reserves or chest interaction cells. North exit leads to O5.")

d14=main(14,"royal_causeway","Royal Causeway","One melee guard, an empty crossing, then a caster-and-bandit combination on a broad landing.","high",5,size=(40,24))
d14.rect([17,1,21,22],"C").rect([17,9,21,12],"=")
d14.line([[1,11],[15,11]],"_").line([[23,11],[34,11]],"_")
d14.enemy_group("g1",[5,7,13,15],[("skeleton_warrior",[10,11])],"A known melee guard before the bridge; it cannot pursue onto the deck.")
d14.enemy_group("g2",[25,7,33,15],[("bandit_caster",[29,9]),("bandit",[30,14])],"First required-route caster mix, isolated from the crossing so the player can enter a nine-cell-square landing.")
d14.chest(1,[29,19],[["potion_greater",2]],"Restock after the last dense required-route group.")
d14.structure("bridge_ew",[17,9,21,12],"Four-row deck, five long. West landing x14..16 and east landing x22..24 have no combat, props or projectiles.")
d14.deco("pharaoh_statue",[15,4],"Royal marker on a blocked pedestal.",True).rect([14,3,16,5],"M")
d14.deco("pharaoh_statue",[23,4],"Matching far-bank statue frames the causeway.",True).rect([22,3,24,5],"M")
d14.path([[2,11],[15,11],[23,11],[33,11]])
d14.notes("C is blocked; = deck is walkable. Rails remain outside deck and landings. No combat on the bridge, water, stairs or scripted gate.")

d15=main(15,"tomb_approach","Tomb Approach","A quiet ceremonial approach foreshadows the boss and offers the final optional equipment branch.","quiet",5)
d15.rect([1,1,6,5],"M").rect([17,1,24,3],"M").rect([8,18,17,22],"#")
d15.line([[1,11],[11,11],[11,1]],"_").line([[11,11],[34,11]],"_",5)
d15.chest(1,[27,5],[["potion_greater",2]],"Guaranteed pre-boss consumables on a short, enemy-free side pocket.")
d15.deco("pharaoh_statue",[4,3],"First intact royal statue; the second has lost its head.",True)
d15.deco("ruin_block",[20,2],"Broken companion statue base on solid masonry.",True)
d15.deco("bush_dead",[29,19])
d15.path([[2,11],[11,11],[33,11]])
d15.notes("Five-cell ceremonial paving is flat. No enemies, water, bridge, stairs or gate. O6 branches north before the save room; no branch beyond the star.")
d15.weather=dict(sandstorm=False,tumbleweeds=False)

o5=optional(5,"echo_grotto","Echo Grotto","A clearly optional cave encounter grants the chapter's premium sword.","high",5)
o5.rect([1,1,30,5],"#").rect([4,3,27,5],".").rect([1,6,5,12],"#").rect([27,14,30,20],"#")
o5.line([[11,20],[11,15],[18,15],[18,8],[24,8]])
o5.enemy_group("g1",[14,6,24,14],[("bat",[16,8]),("bat",[22,8]),("python",[20,12])],"Optional three-enemy mastery check: visible bat circles over a telegraphed ground lunge, with an eleven by nine floor.")
o5.chest(1,[26,4],[["sunsteel_blade",1]],"A strong optional weapon, never assumed by Pharaoh health tuning.")
o5.deco("ruin_block",[7,2],"Ancient blade shrine embedded in the cave roof; no hidden breakable wall.",True)
o5.deco("pebbles",[6,17]).deco("skull",[29,16])
o5.path([[11,19],[11,15],[18,15],[18,8],[25,8],[25,5]])
o5.notes("Cave walls are #; all sand pockets connect. No combat lock, water, stairs or bridge; bats respect walls and cannot attack through the roof.")
o5.weather=dict(sandstorm=False,tumbleweeds=False)

# Batch 6: last elective reward, immediate checkpoint, distinct arena, ending.
o6=optional(6,"memorial_vault","Memorial Vault","A final optional terrace duel leads to premium armor, then a quiet return to the star.","medium",6)
o6.rect([1,1,30,3],"M").rect([1,10,30,11],"M").rect([14,10,18,11],"^")
o6.line([[11,20],[11,16],[16,16],[16,13]],"_")
o6.rect([3,4,28,9],"_")
o6.enemy_group("g1",[3,13,9,19],[("skeleton_warrior",[7,16])],"One optional guardian on a broad lower terrace; no enemy occupies the stair or reward landing.")
o6.chest(1,[25,5],[["paladin_mail",1],["potion_greater",1]],"Premium optional armor, earned by taking the memorial detour; never a key or required boss defense tier.")
o6.structure("stairs",[14,10,18,11],"Five-cell-wide memorial stair, z0 south to z1 north, clear two-cell landings.")
o6.spec["elevations"]=[dict(id="lower",level=0,rect=[1,12,30,20]),dict(id="memorial",level=1,rect=[1,4,30,9])]
o6.deco("obelisk",[7,2],"Memorial stones echo the city's lost comrades without claiming the Grail is recovered.",True)
o6.deco("pharaoh_statue",[27,2]).deco("pebbles",[25,18])
o6.path([[11,19],[11,16],[16,16],[16,8],[25,8],[25,7]])
o6.notes("Only ^ cells cross the masonry band. No one-way drop, water, bridge, locked chest or shortcut past the boss.")
o6.weather=dict(sandstorm=False,tumbleweeds=False)

d16=main(16,"pharaohs_gate","Pharaoh's Gate","An entirely safe final save star sits directly on the route to the arena vestibule.","quiet",6)
d16.rect([1,1,34,4],"M").rect([16,5,18,14],"M").rect([16,10,18,12],"_")
d16.line([[1,11],[24,11],[24,17],[34,17]],"_",3)
d16.rect([29,15,33,19],"_").checkpoint([31,17])
d16.deco("pharaoh_statue",[25,3],"Still royal sentinel; no creature or ambush occupies the save room.",True)
d16.deco("obelisk",[11,3],"Inscription faces the last star and the arena entrance.",True)
d16.path([[2,11],[24,11],[24,17],[33,17]])
d16.notes("The star is four tile columns from the east border opening, with no intervening room, reward detour or encounter.","No water, chasm, stairs or bridge. Gate closure occurs inside D17 only after Dave clears the gate plane. Checkpoint remains usable after victory.")
d16.weather=dict(sandstorm=False,tumbleweeds=False)

d17=main(17,"pharaohs_courtyard","Pharaoh's Courtyard","A distinct paved royal arena with a bent entry vestibule supports the Pharaoh's complete encounter.","boss",6,size=(40,24))
d17.rect([1,1,38,22],"M").rect([1,1,38,11],"_").rect([1,16,8,22],"_").rect([4,12,6,15],"_")
d17.rect([20,4,30,10],".")
d17.enemy_group("boss",[9,1,32,10],[("pharaoh",[17,6])],"Large uncluttered arena; pursuit, laser sidesteps, marked thunder and capped summons share no solid props.")
d17.spec["encounters"][0].update(clear_required=True,activation="Only boss_entry dialogue completion; ordinary rectangle activation is disabled.")
d17.structure("entrance_gate",[4,14,6,14],"Horizontal three-cell gate at the bend, matching the 192-pixel gate asset. Closes only when Dave is fully north of y13.")
d17.structure("sealed_exit",[39,7,39,9],"East transition and boundary collision remain sealed until boss_pharaoh_defeated. Use vertical masonry seal/energy effect, not a stretched horizontal gate.")
d17.deco("pharaoh_statue",[10,15],"Statues sit on blocked masonry beneath the fight floor, never inside dodge lanes.",True)
d17.deco("pharaoh_statue",[28,15],"Paired sentinels make this space read as a courtyard rather than another desert room.",True)
d17.spec["scripts"]=[
    dict(id="boss_entry",trigger_rect=[4,12,6,12],event="boss_intro",once_flag="boss_intro_seen",note="Unavoidable throat trigger: test continuous occupancy while idle, not one-shot on_enter. If boss not defeated and full mask clears north of pixel y832 (top of row13): pause damage, walk one cell to safe mark [5,11], close gate [4,14..6,14], frame both actors at intro camera target, play narrative-owned boss_intro. Set intro-seen only when sequence starts. Skip initializes combat identically. Intro-seen flag must never suppress gate/combat restart after a failed attempt."),
    dict(id="pharaoh_defeat",trigger_rect=None,event="boss_hp_zero",once_flag="boss_pharaoh_defeated",note="Stop attacks and disable all damage immediately; disintegration, slow whiteout, remove boss/summons/projectiles/hazards during white, fade back, reopen entrance and east route, commit defeated flag and pending reward together. No Grail reward."),
]
d17.spec["boss"] = dict(
    entrance_gate_rect=[4,14,6,14], entry_trigger_cell=[5,11], locked_exit="east",
    intro_camera_target_pixel=[736,576], intro_dave_cell=[5,11], intro_pharaoh_cell=[17,6],
    teleport_cells=[[24,4],[27,9],[17,6]], bat_spawn_cells=[[14,11],[28,3]],
    undead_spawn_cells=[[12,4],[30,11]], default_caps=dict(bats=2,undead=2),
    summon_exclusion="At least 3 cells from Dave, portal/arrival reserves and committed thunder refuge; postpone if no legal authored cell.",
    thunder_rules="Commit markers once, initial warning >=1.0 s; retain a connected unmarked escape strip >=3 cells wide within current camera. No full-floor coverage, offscreen damage, or marked entrance vestibule.",
    visibility_rule="Fixed 1280x720 follow camera. Aim/impact markers and attacking enemy must be visible before damage; postpone offscreen attacks. Boss closes distance before attacking. No zoom change.",
    bat_cadence="Attempt capped bat summon once per complete attack cycle; no accumulation past cap.",
    laser_rule="Visible aim, charge and committed direction; do not combine beam and thunder into a sealed escape strip.",
    baseline_tuning="3-5 minute target with normal main-route equipment, no optional gear or grinding; Claude tunes HP/timings in IDE.",
    music_by_state=dict(idle="mus_desert",dialogue="duck exploration music; no boss theme yet",combat="mus_pharaoh",defeat="stop boss loop on death; resolve after whiteout",cleared="mus_desert; optional brief mus_ending resolution"),
    reward=dict(id="rm_d17_pharaohs_courtyard:u1",cell=[25,7],loot=[["pharaoh_ankh",1]],claim="Exactly once; pending interactable reward stays if inventory full; no duplication after saves."),
    states=dict(idle="Entrance open, east sealed, boss idle, no damage.",dialogue="Entrance closed, east sealed, all damage paused.",combat="Entrance closed, east sealed, boss and capped summons active.",defeat="All damage disabled; death and whiteout; transitions paused.",cleared="Both routes open; no boss, summons, projectiles or hazards; pending reward only."))
d17.path([[2,17],[5,17],[5,11],[5,9],[16,9],[16,7],[37,7],[37,8]])
d17.notes("The west vestibule enters at y16..18 and turns north through a real horizontal gate. A solid masonry band y12..15 leaves only the x4..6 throat, so the row12 intro trigger cannot be bypassed.","The fight floor is flat: central sand is ordinary floor, not a raised dais. No pits, water, stairs, bridges, pillars or permanent arena hazards.","Seal the east border cells plus transition while idle/dialogue/combat/defeat. On victory remove the seal. No ordinary encounter-clear flag can unlock it.")
d17.weather=dict(sandstorm=False,tumbleweeds=False)
d17.music="mus_desert"
d17.spec["additional_assets"]=["spr_gate_arena","spr_door_sealed","spr_laser_beam","spr_fx_laser_charge","spr_laser_aim","spr_thunder_marker","spr_thunder_exclaim","spr_lightning_bolt","spr_fx_thunder_impact","spr_summon_crack","spr_fx_sand_burst","snd_gate_slam","snd_boss_summon","snd_laser_charge","snd_laser_fire","snd_thunder_warn","snd_thunder_strike","snd_boss_hurt","snd_disintegrate","snd_boss_death","snd_undead_rise","spr_portrait_dave","spr_portrait_pharaoh","mus_desert","mus_pharaoh","mus_ending"]

d18=main(18,"dungeon_threshold","Dungeon Threshold","A quiet victory walk reaches the dungeon mouth and ends Chapter I without entering an interior.","quiet",6)
d18.rect([24,1,34,3],"M").rect([30,3,31,4],"_")
d18.line([[1,8],[18,8],[18,12],[30,12],[30,6]],"_")
d18.deco("dungeon_entrance",[30,4],"Dungeon facade drawn so its existing 128-pixel doorway is aligned with x30..31; art origin needs an integration offset, never infer collision from alpha.",True)
d18.decoration[-1]["offset_px"]=[32,0]
d18.deco("ruin_block",[26,2]).deco("bush_dead",[9,18])
d18.spec["scripts"]=[dict(id="dungeon_threshold",trigger_rect=[30,4,31,4],event="chapter_ending",once_flag="chapter_desert_complete",note="Require boss_pharaoh_defeated; stop movement/damage, transition to rm_ending showing exactly To Be Continued. No dungeon interior. On a loaded completed save, re-entering this trigger may show the ending again; never trap the player behind a once-only empty trigger.")]
d18.path([[2,8],[18,8],[18,12],[30,12],[30,4]])
d18.notes("A three-cell paved approach leads to an internal two-cell art doorway; the contract's three-cell rule still holds for every border exit.","No enemies, chests, water, stairs, bridges, moving hazards or Grail. West backtracking is allowed before entering the threshold.")
d18.weather=dict(sandstorm=False,tumbleweeds=False)
d18.spec["additional_assets"]=["spr_dungeon_entrance","spr_ending_bg","mus_ending"]

MAIN=[d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16,d17,d18]
OPTIONAL=[o1,o2,o3,o4,o5,o6]
BATCHES=[[d1,d2,d3,o1],[d4,d5,d6,o2],[d7,d8,d9,o3],[d10,d11,d12,o4],[d13,d14,d15,o5],[d16,d17,d18,o6]]


def opening(room, local_id, side, span, dest, dest_exit):
    key="rows" if side in "EW" else "cols"
    room.exits.append(dict(id=local_id,side=side,**{key:span},to=dest.id,to_exit=dest_exit))
    a,b=span
    if side in "EW":
        x=0 if side=="W" else room.w-1
        room.rect([x,a,x,b],"_")
        # Fixed three-cell entry corridor and a 3x3 arrival reserve.
        room.rect([0 if side=="W" else room.w-5,a,4 if side=="W" else room.w-1,b],"_")
    else:
        y=0 if side=="N" else room.h-1
        room.rect([a,y,b,y],"_")
        room.rect([a,0 if side=="N" else room.h-5,b,4 if side=="N" else room.h-1],"_")


for a,b in zip(MAIN,MAIN[1:]):
    span=[16,18] if a is d16 else [7,9] if a is d17 else [4,6] if a is d12 else [10,12]
    opening(a,"east","E",span,b,"west")
    opening(b,"west","W",span,a,"east")
for parent,child in zip([d3,d6,d8,d10,d13,d15],OPTIONAL):
    opening(parent,"north","N",[10,12],child,"south")
    opening(child,"south","S",[10,12],parent,"north")


def arrival(room, ex):
    a,b=ex.get("rows",ex.get("cols")); mid=(a+b)//2
    return {"W":[2,mid],"E":[room.w-3,mid],"N":[mid,2],"S":[mid,room.h-3]}[ex["side"]]


for room in ROOMS.values():
    room.spec["arrivals"]=[]
    room.spec["transitions"]=[]
    for ex in room.exits:
        cell=arrival(room,ex)
        reserve=[cell[0]-1,cell[1]-1,cell[0]+1,cell[1]+1]
        room.spec["arrivals"].append(dict(exit_id=ex["id"],cell=cell,
            pixel=[cell[0]*64+32,cell[1]*64+32],safe_rect=reserve,
            facing={"W":0,"E":4,"N":6,"S":2}[ex["side"]]))
        target=ROOMS[ex["to"]]
        other=next(e for e in target.exits if e["id"]==ex["to_exit"])
        dc=arrival(target,other)
        condition="boss_pharaoh_defeated" if (room is d17 and ex["id"]=="east") or room is d18 else "always"
        room.spec["transitions"].append(dict(exit_id=ex["id"],to=target.id,to_exit=other["id"],
            destination_arrival_cell=dc,destination_arrival_pixel=[dc[0]*64+32,dc[1]*64+32],condition=condition))
    if room is d1:
        room.spec["initial_spawn_safe_rect"]=[2,10,4,12]


BASE_ASSETS=["tex_sand_light","tex_sand_dark","tex_rock_top","tex_cliff_face","mus_desert",
             "spr_mask_dave","spr_fx_slash","spr_fx_hit","snd_sword_swing","snd_sword_hit","snd_pickup","snd_step_sand"]
BASE_ASSETS += [f"spr_dave_{anim}_{direction}" for anim in ("idle","walk","attack") for direction in ("down","down_side","side","up_side","up")]


def enemy_assets(kind):
    if kind=="bat": return ["spr_bat_fly","spr_bat_dive","spr_bat_defeat","spr_mask_bat","snd_bat_screech"]
    if kind=="python": return [f"spr_python_{anim}_{d}" for anim in ("slither","lunge") for d in ("down","side","up")]+["spr_python_coil","spr_python_hurt","spr_python_defeat","spr_mask_python","snd_snake_hiss","snd_snake_lunge"]
    if kind=="sandworm": return [f"spr_sandworm_{a}" for a in ("mound","emerge","idle_up","attack","burrow","hurt","defeat")]+["spr_mask_sandworm","snd_worm_rumble","snd_worm_emerge","snd_worm_bite"]
    if kind=="pharaoh": return [f"spr_pharaoh_{a}" for a in ("idle","summon","laser_charge","laser_fire","thunder_cast","hurt","teleport_out","teleport_in","death")]+["spr_mask_pharaoh"]
    a=[f"spr_{kind}_{anim}_{d}" for anim in ("walk","attack") for d in ("down","side","up")]
    a += [f"spr_{kind}_{anim}" for anim in ("idle_down","hurt_down","defeat")]+["spr_mask_medium"]
    if kind=="undead": a += ["spr_undead_rise"]
    if kind=="skeleton_archer": a += ["spr_arrow","spr_fx_arrow_hit","snd_bow_release","snd_arrow_hit"]
    if kind=="bandit_caster": a += ["spr_magic_orb","spr_fx_magic_launch","spr_fx_magic_hit","snd_cast_charge","snd_magic_travel","snd_magic_hit"]
    return a


TERRAIN_ASSETS={";": ["tex_grass"],"~":["tex_water","tex_wet_sand"],"M":["tex_masonry_top","tex_masonry_face"],"_":["tex_paving"],"^":["ts_stairs"],"C":["tex_chasm_wall","tex_chasm_void"],"=":["ts_bridge"],"|":["ts_bridge"],"x":["ts_bridge"]}
asset_rooms={}
for room in ROOMS.values():
    assets=set(BASE_ASSETS+[room.music]+room.spec["additional_assets"])
    for ch in set("".join("".join(r) for r in room.grid)):
        assets.update(TERRAIN_ASSETS.get(ch,[]))
    for obj in room.objects:
        if obj["type"]=="enemy": assets.update(enemy_assets(obj["enemy"]))
        if obj["type"]=="prop": assets.add("spr_"+obj["prop"])
        if obj["type"]=="chest":
            assets.update(["spr_chest_desert","snd_chest_open"])
            assets.update("spr_icon_"+loot[0] for loot in obj["loot"])
        if obj["type"]=="checkpoint": assets.update(["spr_checkpoint_star","spr_fx_sparkle","snd_checkpoint","snd_save"])
    assets.update(d["asset_id"] for d in room.decoration)
    if room.weather["sandstorm"]: assets.add("snd_wind_loop")
    if room.weather["tumbleweeds"]: assets.add("spr_tumbleweed")
    if room is d17:
        assets.update(enemy_assets("bat")+enemy_assets("undead")+["spr_icon_pharaoh_ankh"])
    room.spec["required_asset_ids"]=sorted(assets)
    for asset in assets: asset_rooms.setdefault(asset,[]).append(room.id)


MANIFEST=dict(
    design_version="desert_v1",status="design handoff; not imported, compiled or playtested",
    scope=dict(main_rooms=18,optional_rooms=6,total_rooms=24,ffv_region=None,ffv_version=None,
               room_count_status="Provisional project scope; never a verified Final Fantasy V room count."),
    main_route=[r.id for r in MAIN],optional_attachments=[dict(parent=p.id,optional=o.id) for p,o in zip([d3,d6,d8,d10,d13,d15],OPTIONAL)],
    batches=[dict(batch=i,rooms=[r.id for r in group]) for i,group in enumerate(BATCHES,1)],
    coordinates=dict(tile_pixels=64,cell="[column,row], 0-based, x east/right, y south/down",cell_origin="Character feet or prop base at [64*column+32,64*row+32] pixels",rect="[x_min,y_min,x_max,y_max], inclusive",span="rows or cols inclusive",facing="0 E, 1 NE, 2 N, 3 NW, 4 W, 5 SW, 6 S, 7 SE",arrival="Two cell indices inside border: W x2, E width-3, N y2, S height-3; midpoint of opening.",north_south_exit_format="cols replaces rows; proposed extension because contract shows E/W rows only. Sidecar resolves exact border cells and arrivals."),
    terrain=dict(walkable=".,;_^=|",blocked="#M~Cx",water="All water blocks; no swimming or currents.",elevation="Discrete presentation zones connected by authored stairs/ramps. No jumps, falls, upper-floor overlap or free cliff crossing.",bridge="Bridge cells replace underlying water/chasm collision; broken x never walkable."),
    separation=dict(room_json="Exact contract top-level fields and object keys; no decoration props in objects.",gameplay_specs="Design-only sidecar: arrivals, footprints, encounters, triggers, states, assets; Claude implements their semantics.",decorations="Noncolliding placements only; never infer solids from sprite alpha or artwork. Tall solid props appear only in room objects + footprint specs.",no_project_edits="No .yy, .yyp, GameMaker object, runtime data registry or existing contract changed."),
    movement_rules=dict(main_route_min_clear_width_cells=3,standard_combat_min_rect=[7,7],transition_opening_min_width=3,
        transition="Trigger on deliberate outward crossing at border, never merely occupying a destination arrival. Lock damage/movement during load; discard incoming projectiles; debounce until player leaves destination entry corridor and releases outward intent. Spawn facing inward.",
        protection="No enemy, summon, projectile, loot drop, solid prop or storm occlusion in arrival reserves; enemy feet and solid prop bases >=2 cells from any border opening. Enemies leash to authored pads; attacks cannot enter transition corridors or bridge/stair landings.",
        checkpoints="All three are peaceful; save snapshots include inventory, XP, defeated spawn IDs, opened/part-claimed chests, pending unique reward, boss flags and world seed. Death rolls back the entire snapshot together; do not mix current chest flags with old inventory."),
    procedural=dict(runtime_geometry=False,seed="Persist a world_seed for cosmetic variation. Fixed room/prop/chest/enemy coordinates never reroll.",allowed="Seeded sand material variants, irregular visual blend edges within the same logical tile, pebbles/flat grass decals in declared cosmetic zones, bounded wind particles and tumbleweeds moving E to W.",fixed="Graph, dimensions, terrain blockers, openings, arrivals, solid prop bases, stairs/bridges, encounter IDs and initial cells, chest loot and IDs, landmarks, checkpoint cells, boss gate/threshold geometry and committed thunder targets.",decoration_zones="Only empty . or ; cells >=2 cells from gameplay objects, stairs, bridges, arrival reserves and paths; reject art that hides silhouettes/telegraphs. Authored landmarks never randomize.",tumbleweeds="Noncolliding, at most 2 per outdoor room and 12 ambient particles per emitter as an initial budget; no spawns over combat pads/reserves; lifetime <=10 s; room-exit cleanup. No tumbleweeds in refuges, caves, gate, boss or threshold.",weather="No gameplay effect on speed, accuracy or collision; readability first. Stable cosmetic seed, bounded time-varying particles; their exact transient phase need not persist."),
    persistence=dict(ordinary_enemies="Each sidecar ordinary encounter enemy has a stable spawn ID, matched to its contract object by enemy type and initial cell. Defeated spawns remain defeated across visits and saved snapshots. No farming by transition. Reset only by restoring an earlier snapshot/new game. Pharaoh is excluded from ordinary defeated-spawn storage; his boss flag is authoritative.",chests="Persist opened, remaining item counts and pending overflow by stable chest ID; an empty graphic alone is not authoritative.",boss="Persist boss_pharaoh_defeated + pending/claimed u1 together. Active encounter/projectiles are transient and reset to idle on death/load of an undefeated checkpoint. Saved defeated state skips intro and recreates the cleared arena.",initial="Initial fallback snapshot at D01 [3,11] facing E before first manual save.",healing_spring="Repeatable E interaction, no loot/XP/save; cosmetic animation transient.",threshold="Persist chapter_desert_complete; a completed saved state must still allow the ending UI to be replayed."),
    external_states=dict(intro=dict(room="rm_intro",to=d1.id,arrival_cell=[3,11]),ending=dict(from_room=d18.id,to="rm_ending",trigger_rect=[30,4,31,4],text="To Be Continued",requires="boss_pharaoh_defeated",dungeon_interior=False)),
    sources=[dict(kind="original_brief",title="Create Dave’s action game prompt",thread_id="01a19086-ad27-7ba2-b483-5f550e9c8e07",note="Read original user brief and expanded route; current user's explicit route confirmation is authoritative."),dict(kind="contract",path="docs/PROJECT_CONTRACT.md",sections="2, 6-11"),dict(kind="asset_requests",path="docs/ASSET_REQUESTS.md",sections="A, B, C, D, F"),dict(kind="template",path="notes/Template_Readme/Template_Readme.txt"),dict(kind="template",path="art/reference/template_sprite_inspection.png"),dict(kind="template",path="art/reference/template_inventory.json"),dict(kind="template",path="rooms/rm_level_1/rm_level_1.yy",note="Checked layers and collision objects; original maps are not copied."),dict(kind="reference",url="https://cour89.com/ff5/maps/pyramid.php",note="Version-scoped GBA/mobile guide: visible rewards off the main route, multiple doors, stairs, loops. Inspiration only, not the selected region."),dict(kind="reference",url="https://cour89.com/ff5/maps/quicksand_desert.php",note="Version-scoped guide distinguishes the shifting-sands route and lack of chests; do not claim its treasure pattern or room count as this chapter's source.")])


def build_docs():
    DOC.mkdir(parents=True,exist_ok=True)
    intro = """# Desert chapter - Claude implementation handoff

Design v1. All 18 main rooms and six optional rooms are authored below in six batches. Start with Batch 1: Arrival, Dune Trail, Canyon Approach and Sunken Lookout. **24 rooms is provisional project scope. The FFV reference region and version remain unspecified; this is not a verified FFV room count.**

The original brief was read in the chat **Create Dave’s action game prompt** (thread `01a19086-ad27-7ba2-b483-5f550e9c8e07`); the user's explicit route confirmation in this chat fixes the order. Sources also read: `docs/PROJECT_CONTRACT.md`, `docs/ASSET_REQUESTS.md`, the template README, sprite inspection/inventory, player collision event and original room layers. The two old YoYo tutorial URLs in the README could not be fetched; the local template was inspected directly.

FFV is a reference for reading a landmark, making a choice, finding a reward and returning to a recognizable route. The version-scoped [Pyramid guide](https://cour89.com/ff5/maps/pyramid.php) describes branching doors, stair routes and visible treasure detours. The [Shifting Sands guide](https://cour89.com/ff5/maps/quicksand_desert.php) instead describes a travel puzzle with no treasure chests. These are comparative references, not a declaration of the intended region. This chapter uses original geometry, place names, deliberate combat pads and permanent bridges; it copies neither map nor room count.

## Files and import boundary

- `design/desert/rooms/<room_id>.json`: one contract-format terrain/content document per room, ready for Claude's room builder as incoming design data.
- `design/desert/chapter_manifest.json`: graph, batches, conventions, transition rules, persistence and procedural limits.
- `design/desert/gameplay_specs.json`: exact arrivals, prop footprints, chest approaches, enemy spawn IDs/leashes, scripts, gate states and required asset IDs per room. **Design-only sidecar, not an already-supported runtime schema.**
- `design/desert/decorations.json`: art-only placements with `collision:false`; never put these in collision data.
- `design/desert/asset_manifest.json`: exact referenced IDs, availability and which rooms need them.
- `design/desert/validation_report.json`: automated geometry results and required IDE checks.
- `tools/validate_desert_design.py`: rerun with `python tools/validate_desert_design.py`.
- [Chapter gameplay atlas](../../design/desert/previews/chapter_atlas.png) and [larger opening-batch preview](../../design/desert/previews/batch_01_opening.png): schematic previews, with decoration omitted. Regenerate with `python tools/render_desert_atlas.py`.

No GameMaker `.yy`/`.yyp`, runtime object, existing contract or included-file registry is changed. Claude constructs rooms and implements collision, transitions, scripts and persistence. North/south exits use `cols` instead of `rows`; this is the one explicit schema proposal needed for branches, because the contract only illustrates E/W. Do not treat sidecar fields as features already implemented by the engine.

## Coordinates, legend and collision

One character is one **64 x 64 pixel tile**. Coordinates are `[column,row]`, zero-based from top left. X grows east/right; Y grows south/down. All rectangles and exit spans include both endpoints. A cell ground point is `(64*x+32,64*y+32)` pixels; feet/base origins go there. Room dimensions below are tile counts, not pixels.

` . ` sand; `,` dark sand path; `;` grass; `~` blocked water; `#` blocked cliff/rock; `M` blocked masonry; `_` paved floor; `^` walkable stairs; `C` blocked chasm; `=` E/W bridge; `|` N/S bridge; `x` blocked broken span. The authoritative terrain grids contain no object symbols. Readable batch diagrams overlay `e` enemy, `c` chest, `S` star, `p` solid prop base, `t` scripted trigger, `i` initial spawn, `g` stateful gate; look up exact coordinates below each grid. Decoration is never an object marker or blocker.

Characters use the contract's independent foot masks (Dave 28 x 14 pixels; medium 32 x 16; python 48 x 16; worm 64 x 28; Pharaoh 72 x 30). Props use explicit base footprints. The validator conservatively blocks whole footprint cells and whole chest cells. Tall art may overhang; it must not hide a route, chest, star or attack warning. Decorative solids are drawn only on already blocked terrain, except explicitly flat nonblocking foliage/decals.

All border openings are at least three cells wide. Arrivals are two indices inside: W `[2,mid]`, E `[width-3,mid]`, N `[mid,2]`, S `[mid,height-3]`. Every arrival has a clear 3 x 3 reserve and an unobstructed entry corridor. Explicit cells, pixels and facing are in the sidecar. Transition on outward crossing only; pause damage during loads, discard incoming projectiles, and debounce until Dave leaves the destination corridor and releases outward movement. Never place a character on a border trigger.

Every ordinary combat pad is at least 7 x 7 clear tiles (448 x 448 pixels); the boss has a 24 x 10 clear pad inside a larger floor. Three-cell lanes connect the room graph. Encounters activate only when Dave enters their pad, leash there, and cannot attack entry corridors or stair/bridge landings. All ordinary encounters are bypassable and never gate progress or chest opening. No jump, swim, climbing ability, key, mandatory gear drop or grinding is required. Cliffs are full logical blockers, with stairs/ramps as the only authored level changes. Bridges override underlying chasm/water collision. No walkable roof overlays or one-way drops exist.

## Full room graph

All horizontal main links are reciprocal; each next main room lies east. Branches leave north and return south to the same parent. D17's east link requires `boss_pharaoh_defeated`. D18's threshold goes to the ending UI, not a twenty-fifth desert room.

```mermaid
flowchart LR
  D01[01 Arrival] <--> D02[02 Dune Trail]
  D02 <--> D03[03 Canyon Approach]
  D03 <--> D04[04 Split Cliffs]
  D04 <--> D05[05 Dry Wash]
  D05 <--> D06[06 Oasis Refuge - SAVE]
  D06 <--> D07[07 Ruined Caravan]
  D07 <--> D08[08 Cactus Flats]
  D08 <--> D09[09 Bonefield]
  D09 <--> D10[10 Broken Bridge]
  D10 <--> D11[11 Forgotten Ruins - SAVE]
  D11 <--> D12[12 Great Desert Stairs]
  D12 <--> D13[13 Windblown Plateau]
  D13 <--> D14[14 Royal Causeway]
  D14 <--> D15[15 Tomb Approach]
  D15 <--> D16[16 Pharaoh's Gate - SAVE]
  D16 <--> D17[17 Pharaoh's Courtyard - BOSS]
  D17 <-->|boss defeated| D18[18 Dungeon Threshold]
  D18 --> END[To Be Continued]
  D03 <--> O1[O1 Sunken Lookout]
  D06 <--> O2[O2 Hidden Spring]
  D08 <--> O3[O3 Bandit Cache]
  D10 <--> O4[O4 Buried Cistern]
  D13 <--> O5[O5 Echo Grotto]
  D15 <--> O6[O6 Memorial Vault]
```

## Content and pacing overview

Counts are initial authored enemies; Pharaoh summons are additional, transient and capped. Loot amounts are design proposals using the contract's item IDs. They do not define weapon stats, XP, sale values or enemy tuning. Quiet rooms are deliberate breathers; `low` may mean an entirely elective encounter off the main walking line.

| Stable ID | Name / purpose | Tiles | Intensity; enemies | Treasure intention / checkpoint | Batch |
|---|---|---|---|---|---|
"""
    for room in MAIN+OPTIONAL:
        s=room.spec
        kinds=[o["enemy"] for o in room.objects if o["type"]=="enemy"]
        loot="; ".join(f"c{i+1}: "+", ".join(f"{n} {item}" for item,n in c["loot"]) for i,c in enumerate(s["chests"])) or "none"
        if s["checkpoints"]: loot += "; yellow-star SAVE"
        if room is d17: loot="u1: pharaoh_ankh; both gates reopen after whiteout"
        intro+=f"| `{room.id}` | {room.name}: {s['purpose']} | {room.w} x {room.h} | {s['intensity']}; {', '.join(kinds) or '0'} | {loot} | {s['batch']} |\n"
    intro+="""
## Checkpoints, boss and ending

Oasis Refuge `[25,11]`, Forgotten Ruins `[25,11]`, and Pharaoh's Gate `[31,17]` are the only save stars. They heal on a successful player-initiated save and expose exactly three slots. D16's star is four columns before the east border; the next room's short vestibule turns through the horizontal gate. There is no intervening encounter or branch. Before the first save, death restores the initial D01 `[3,11]` snapshot.

The D17 west opening is y16..18. Dave arrives at `[2,17]`, walks to `[5,17]`, then north through the three-wide horizontal gate at x4..6/y14. This bent vestibule uses the contracted 192-pixel-wide gate correctly. Solid masonry along y12..15 leaves only the x4..6 throat: its row12 trigger is unavoidable. After his entire collision mask clears pixel y832 (the top of row13), pause damage, walk him one cell to safe mark `[5,11]`, close the gate and play the narrative-owned `boss_intro` exchange. Skipping dialogue must initialize the same combat state. East is sealed until victory. An intro-seen flag alone must never skip encounter initialization after death.

Pharaoh begins at `[17,6]`. For the introduction, camera centre `(736,576)` pixels frames his silhouette and Dave at `[5,11]` within the unchanged 1280 x 720 view; blend back to follow camera before combat. Bats spawn from `[14,11]` and `[28,3]`; undead from `[12,4]` and `[30,11]`, with initial caps of two of each. Attempt bat summons per complete attack cycle. Postpone a summon if every authored point is too close to Dave or a committed thunder refuge. Keep attacks and committed warnings visible in the unchanged 1280 x 720 camera. Thunder initially warns for at least one second and preserves a connected, unmarked strip at least three cells wide; no offscreen hits or full-floor coverage. Laser and lightning scheduling must preserve an actual movement escape. Health tuning targets three to five minutes with normal main-route equipment; optional sword/armor cannot be assumed. D17's default room music is exploration music; `mus_pharaoh` starts only after the dialogue completes, according to `boss.music_by_state`.

At zero HP: stop scheduling and all damage immediately; run disintegration, slow fade to white, remove all boss actors, summons, projectiles and hazards during white; fade back; reopen the entrance and east exit; commit `boss_pharaoh_defeated` with pending reward `rm_d17_pharaohs_courtyard:u1` (`pharaoh_ankh`) exactly once. Keep unclaimed reward at `[25,7]` if inventory is full. A loaded defeated save recreates the cleared arena with no intro or threats.

D18 is an enemy-free exterior. Its internal two-cell doorway art is allowed because it is not a border exit. Entering `[30..31,4]` with the defeated flag sets `chapter_desert_complete` and shows **To Be Continued** in `rm_ending`. No interior, Grail recovery or further chapter is specified. The west route remains available until the threshold; a completed save can replay the ending.

## Persistence and procedural limits

Geometry, graph, dimensions, openings, stairs, bridge condition, arrival cells, solid props, authored landmarks, checkpoints, enemy spawn IDs/initial cells, chest IDs/loot and ending trigger remain fixed across revisits and loads. No runtime geometry generation is proposed. The authoring script expands fixed rectangles only. Enemy defeats persist across room visits and saves by spawn ID, so walking back cannot farm XP. A death restores inventory, XP, chest claims, enemy defeats, pending unique rewards and boss state from the same snapshot; restoring only part of that state duplicates or destroys loot.

Only cosmetic material variants, blended visual edges, flat decals and bounded weather may vary. Persist a cosmetic world seed. Random decals are allowed only on vacant sand/grass at least two cells from gameplay objects, paths, structures and reserves; reject any that hide attacks or orientation cues. Authored landmarks never move. Tumbleweeds have no collision, travel E to W, cap at two per outdoor room, expire within ten seconds and are cleaned up on exit. Refuges, caves, pre-boss room, arena and threshold suppress them and storms. Weather never changes collision, speed or accuracy. Exact transient particle phases need not persist.

Use contract layer order and foot-depth sorting. Flat decals use `Visual_Assets`; terrain belongs in its corresponding tile layer; solid prop bases and invisible wall objects remain separate. Do not scatter additional solid rocks/cacti or infer collision from art. Asset IDs inferred from prop names or mask families are marked proposed in the asset manifest; final imports need Claude's mapping. Missing art uses visible template/procedural placeholders without changing geometry.

## Verification and Claude acceptance

The accompanying validator checks exact grid sizes/characters; reciprocal exits and graph order; all actual border openings; explicit arrival cells and reserves; three-cell-wide navigation between arrivals; chest approach reachability; no object overlaps; every enemy inside a clear 7 x 7 or larger pad; footprint clearance; required asset references; fixed stairs/bridges and clear landings; both optional return routes; and the closed/cleared boss gate states. It reads the exported JSON, not the authoring objects. See `validation_report.json` for results.

These checks guarantee the authored static topology under the stated collision model. They do not prove runtime AI, physics, timings, camera occlusion or save code that Claude has not built. Before shipping, Claude must playtest: 8-direction movement/foot masks on corners and stairs; melee arcs and retreat room in every pad; ranged line-of-sight across cliffs; bridge rails; safe entry/return from every exit; chest overflow/save rollback; three independent saves; death before first save and during each boss phase; gate closure without clipping; dialogue skip; late thunder escape using ordinary movement; whiteout cleanup; loaded defeated state; reward claiming with full inventory; and threshold replay. No compilation or gameplay test is claimed by this design delivery.

## Implementation batches

1. [Opening rooms and representative treasure branch](batch_01_opening.md)
2. [Split cliffs, dry wash and oasis](batch_02_oasis.md)
3. [Caravan, cactus flats and bonefield](batch_03_encounters.md)
4. [Bridge, ruins and great stairs](batch_04_ruins.md)
5. [Plateau, causeway and tomb approach](batch_05_royal_route.md)
6. [Final star, Pharaoh arena, ending and memorial branch](batch_06_pharaoh.md)

Build one batch at a time, using placeholders where necessary. Batch 1 is a complete movement/combat/loot/branch slice; add the first save star in Batch 2. The full graph and every destination coordinate are already supplied, so later rooms do not require renaming early IDs.
"""
    (DOC/"DESERT_CHAPTER.md").write_text(intro,encoding="utf-8")
    names=["opening","oasis","encounters","ruins","royal_route","pharaoh"]
    for n,group in enumerate(BATCHES,1):
        text=f"# Desert design - batch {n:02}\n\n[Chapter graph, conventions and import rules](DESERT_CHAPTER.md). Grid = 64 px tiles, zero-based [x,y]. Rectangles and spans inclusive. Terrain JSON is authoritative; diagram letters overlay objects. Legend: . sand, , path, ; grass, ~ blocked water, # blocked cliff, M blocked masonry, _ paving, ^ stairs, C blocked chasm, = E/W bridge, | N/S bridge, x blocked broken span; e enemy, c chest, S star, p solid prop, t trigger, i initial spawn, g gate. Decorative placement has no collision and is listed separately.\n"
        for room in group:
            s=room.spec
            text+=f"\n## {room.name}\n\nStable ID: `{room.id}`. Dimensions: **{room.w} x {room.h} tiles** ({room.w*64} x {room.h*64} px). Purpose: {s['purpose']} Intensity: **{s['intensity']}**.\n\n"
            overlay=[row[:] for row in room.grid]
            for obj in room.objects:
                x,y=obj["cell"]; overlay[y][x]={"enemy":"e","chest":"c","checkpoint":"S","prop":"p"}[obj["type"]]
            for script in s["scripts"]:
                r=script["trigger_rect"]
                if r:
                    for y in range(r[1],r[3]+1):
                        for x in range(r[0],r[2]+1):
                            if overlay[y][x] not in "ecSp": overlay[y][x]="t"
            if s["entry_spawn"]:
                x,y=s["entry_spawn"];overlay[y][x]="i"
            if room is d17:
                for x in range(4,7):overlay[14][x]="g"
            text+="```text\n    "+"".join(str(x//10) if x%10==0 else " " for x in range(room.w))+"\n    "+"".join(str(x%10) for x in range(room.w))+"\n"
            text+="\n".join(f"{y:02}  "+"".join(row) for y,row in enumerate(overlay))+"\n```\n\n"
            text+="Entrances / exits (arrival is inside this room; destination cell is inside the target):\n\n| Exit | Border span | Arrival here [x,y]; facing | Destination / return exit | Safe destination [x,y] | Condition |\n|---|---|---|---|---|---|\n"
            for ex,a,t in zip(room.exits,s["arrivals"],s["transitions"]):
                span=ex.get("rows",ex.get("cols"));axis="rows" if "rows" in ex else "cols"
                text+=f"| {ex['id']} | {ex['side']} {axis} {span} | {a['cell']}; {a['facing']} | `{t['to']}` / {t['to_exit']} | {t['destination_arrival_cell']} | {t['condition']} |\n"
            if s["entry_spawn"]:text+=f"\nIntro / initial restart arrives at {s['entry_spawn']}, facing E, reserved rectangle {s['initial_spawn_safe_rect']}. No west border exit.\n"
            text+="\nAuthored main walking line: "+" -> ".join(str(p) for p in s["route_waypoints"])+". These are guidance waypoints; all legal floor remains walkable.\n\nTerrain and boundaries:\n\n"
            for note in s["terrain_notes"]:text+="- "+note+"\n"
            for structure in s["structures"]:text+=f"- {structure['kind']} {structure['rect']}: {structure['note']}\n"
            for e in s["elevations"]:text+=f"- Visual level {e['level']}, {e['id']} rectangle {e['rect']}; only authored connectors cross a solid level boundary.\n"
            if s["collision_footprints"]:
                text+="\nSolid props (separate from art-only decoration):\n\n"
                for p in s["collision_footprints"]:text+=f"- `{p['prop']}` at {p['cell']}, centred base footprint {p['footprint_px']} px; conservative blocked cells rectangle {p['blocked_rect']}.\n"
            else:text+="\nSolid props: none. Collision comes from terrain, chest bases and any explicitly stateful gate.\n"
            text+="\nEncounters:\n\n"
            if not s["encounters"]:text+="- None; preserve the quiet room.\n"
            for group2 in s["encounters"]:
                text+=f"- `{group2['id']}`: pad/leash {group2['combat_rect']}; max {group2['max_active']} active. {group2['purpose']} {group2['activation']}\n"
                for e in group2["enemies"]:text+=f"  - `{e['id']}`: `{e['enemy']}` at {e['cell']}.\n"
            text+="\nTreasure:\n\n"
            if not s["chests"]:text+="- No chests.\n"
            for c in s["chests"]:text+=f"- `{c['id']}` at {c['cell']}: "+", ".join(f"{q} x `{item}`" for item,q in c["loot"])+f". {c['intention']} Approach {c['approach_cell']}; interact from {c['interaction_cell']}. Unlocked, reachable before any kill; claims persist by ID, with pending overflow.\n"
            if room is d17:text+="- Unique boss reward `rm_d17_pharaohs_courtyard:u1`, `pharaoh_ankh` x1 at [25,7], pending until inventory space exists; no Holy Grail.\n"
            text+="\nCheckpoint / script data:\n\n"
            if not s["scripts"] and not s["checkpoints"]:text+="- No checkpoint or one-off script; ordinary enemies use the shared encounter activation policy.\n"
            for c in s["checkpoints"]:text+=f"- `{c['id']}` at {c['cell']}; respawn {c['respawn_cell']}; clear pad {c['safe_rect']}. {c['activation']}.\n"
            for trigger in s["scripts"]:text+=f"- `{trigger['id']}`, event `{trigger['event']}`, trigger {trigger['trigger_rect']}, persistent flag `{trigger['once_flag']}`: {trigger['note']}\n"
            if room is d17:text+="- Boss state table, teleport/summon cells, caps, safe-strip rules and pending reward semantics: see this room's `boss` in gameplay_specs.json and chapter handoff. The east boundary is physically sealed before victory, not just a disabled portal.\n"
            text+="\nLandmarks and decoration (art-only, no gameplay or collision):\n\n"
            for d in room.decoration:text+=f"- `{d['id']}`: `{d['asset_id']}` at {d['cell']}, pixel offset {d['offset_px']}, layer `{d['layer']}` ({d['depth_policy']}). {d['note'] or 'Sparse dressing; keep readable floor and telegraphs.'}\n"
            text+=f"\nMusic: `{room.music}`; weather flags: `{json.dumps(room.weather)}`. All required asset IDs, including shared Dave/combat materials, are enumerated under this room in `gameplay_specs.json`; availability is in `asset_manifest.json`. Room-specific terrain/prop/enemy/loot IDs:\n\n"
            text+="`"+"`, `".join(x for x in s["required_asset_ids"] if x not in BASE_ASSETS)+"`.\n"
            text+=f"\nImplementation sources: `design/desert/rooms/{room.id}.json`, plus its same-ID entries in `gameplay_specs.json` and `decorations.json`.\n"
        (DOC/f"batch_{n:02}_{names[n-1]}.md").write_text(text,encoding="utf-8")


if __name__=="__main__":
    if (OUT/"scene_manifest.json").exists():
        raise SystemExit("The small-map design is superseded. Use python tools/design_desert_scenes.py for the current scene world; legacy generation is disabled to protect the current handoff.")
    for room in ROOMS.values():dump(OUT/"rooms"/(room.id+".json"),room.export())
    dump(OUT/"chapter_manifest.json",MANIFEST)
    dump(OUT/"gameplay_specs.json",SPECS)
    dump(OUT/"decorations.json",DECOR)
    assets=[]
    for aid,used in sorted(asset_rooms.items()):
        existing=any((ROOT/folder/aid/(aid+".yy")).exists() for folder in ("sprites","sounds","tilesets","objects","fonts"))
        status="existing_template_resource" if existing else "planned_contract_family_exact_suffix_may_need_mapping"
        if aid.startswith("spr_mask_") or any(d["asset_id"]==aid for ds in DECOR.values() for d in ds):
            if not existing:status="proposed_exact_id_requires_Claude_mapping"
        if aid in {"spr_cactus_small","spr_cactus_tall","spr_palm","spr_wagon_wreck","spr_obelisk","spr_tumbleweed"} and not existing:status="proposed_prop_id_requires_Claude_mapping"
        assets.append(dict(asset_id=aid,status=status,rooms=used))
    dump(OUT/"asset_manifest.json",dict(note="IDs specify needs, not claims that artwork exists. Exact prop/mask and animation suffix IDs are incoming proposals unless matched to a resource. Existing template spr_bat_fly still needs contract size/alignment validation. Build-time material textures are not GameMaker sprite resources. Use the contract and asset requests for final asset validation.",assets=assets))
    build_docs()
    print(f"Authored {len(ROOMS)} room JSONs, six batches and sidecars in {OUT}.")
