"""Authored continuous desert scenes; emits design data, never GameMaker resources."""
import copy
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"design"/"desert"
DOC=ROOT/"docs"/"level_design"
OLD=json.loads((BASE/"gameplay_specs.json").read_text(encoding="utf-8"))
WALK=set(".,;_^=|")
SCENES={}
MIGRATION={"design_version":"desert_scenes_v2","chests":{},"enemy_spawns":{},"checkpoints":{},"unique_rewards":{},"places":{}}


def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


class Scene:
    def __init__(self,slug,name,size,outline,purpose):
        self.id="sc_"+slug
        self.room_id="rm_sc_"+slug  # Technical GameMaker key required by Claude's JSON format.
        self.name=name;self.w,self.h=size
        canvas=Image.new("1",size);ImageDraw.Draw(canvas).polygon(outline,fill=1)
        self.grid=[["." if canvas.getpixel((x,y)) else "#" for x in range(self.w)] for y in range(self.h)]
        self.objects=[];self.exits=[];self.decor=[]
        self.s=dict(scene_id=self.id,room_id=self.room_id,purpose=purpose,size_cells=list(size),
            places=[],primary_route=[],exploration_loops=[],encounters=[],chests=[],checkpoints=[],
            solid_props=[],structures=[],scripts=[],arrivals=[],transitions=[],initial_spawn=None,
            elevation_notes=[],batches=[],boss=None,additional_asset_ids=[])
        SCENES[self.id]=self

    def rect(self,r,ch):
        for y in range(r[1],r[3]+1):
            for x in range(r[0],r[2]+1):self.grid[y][x]=ch
        return self

    def path(self,points,char=",",width=5):
        radius=width//2
        for (x1,y1),(x2,y2) in zip(points,points[1:]):
            assert x1==x2 or y1==y2
            for y in range(max(1,min(y1,y2)-radius),min(self.h-2,max(y1,y2)+radius)+1):
                for x in range(max(1,min(x1,x2)-radius),min(self.w-2,max(x1,x2)+radius)+1):
                    if self.grid[y][x] in ".,;_":self.grid[y][x]=char
        return self

    def place(self,old,rect,anchor,experience):
        old_id=next(k for k in OLD if k.startswith(old+"_"))
        stem=old_id.split("_",2)[2]
        pid="place_"+stem
        names={"arrival":"Desert Arrival","pharaohs_gate":"Pharaoh's Gate","pharaohs_courtyard":"Pharaoh's Courtyard"}
        name=names.get(stem,stem.replace("_"," ").title())
        self.s["places"].append(dict(place_id=pid,name=name,rect=rect,anchor=anchor,
            legacy_design_id=old_id,experience=experience,transition=False))
        MIGRATION["places"][old_id]=dict(scene_id=self.id,place_id=pid,anchor=anchor)
        return self

    def encounter(self,old,group,rect,positions,purpose):
        old_id=next(k for k in OLD if k.startswith(old+"_"))
        original=next(g for g in OLD[old_id]["encounters"] if g["id"].endswith(":"+group))
        assert len(positions)==len(original["enemies"])
        enemies=[]
        for source,cell in zip(original["enemies"],positions):
            e=dict(id=source["id"],enemy=source["enemy"],cell=cell)
            enemies.append(e);self.objects.append(dict(type="enemy",enemy=e["enemy"],cell=cell))
            MIGRATION["enemy_spawns"][e["id"]]=dict(scene_id=self.id,cell=cell,preserve_id=True)
        self.s["encounters"].append(dict(id=original["id"],combat_rect=rect,leash_rect=rect,
            enemies=enemies,purpose=purpose,max_active=len(enemies),clear_required=group=="boss",
            activation="boss_intro_complete" if group=="boss" else "Player enters pad; no fighting across protected arrival/checkpoint/bridge/stair zones."))
        return self

    def chest(self,old,cell,north=False):
        old_id=next(k for k in OLD if k.startswith(old+"_"));source=OLD[old_id]["chests"][0]
        cid=f"{self.room_id}:c{len(self.s['chests'])+1}"
        direction=-1 if north else 1
        c=dict(id=cid,cell=cell,loot=copy.deepcopy(source["loot"]),legacy_id=source["id"],
            interaction_cell=[cell[0],cell[1]+direction],approach_cell=[cell[0],cell[1]+2*direction],
            intention=source["intention"],locked=False,footprint_px=[48,20])
        self.s["chests"].append(c)
        self.objects.append(dict(type="chest",id=cid,cell=cell,loot=c["loot"]))
        MIGRATION["chests"][source["id"]]=dict(id=cid,scene_id=self.id,cell=cell)
        return self

    def new_place(self,place_id,name,rect,anchor,experience):
        self.s["places"].append(dict(place_id=place_id,name=name,rect=rect,anchor=anchor,
            legacy_design_id=None,experience=experience,transition=False))
        return self

    def new_chest(self,cell,loot,intention):
        cid=f"{self.room_id}:c{len(self.s['chests'])+1}"
        self.s["chests"].append(dict(id=cid,cell=cell,loot=loot,legacy_id=None,
            interaction_cell=[cell[0],cell[1]+1],approach_cell=[cell[0],cell[1]+2],
            intention=intention,locked=False,footprint_px=[48,20]))
        self.objects.append(dict(type="chest",id=cid,cell=cell,loot=loot))
        return self

    def prop(self,name,cell,fp,blocked=None):
        self.objects.append(dict(type="prop",prop=name,cell=cell))
        self.s["solid_props"].append(dict(prop=name,cell=cell,footprint_px=fp,
            blocked_rect=blocked or [*cell,*cell],anchor="cell ground centre"))
        return self

    def deco(self,name,cell,note="",offset=None):
        flat=name in {"pebbles","loose_rocks","skull","bush","bush_dead"}
        self.decor.append(dict(id=f"{self.id}:decor{len(self.decor)+1}",asset_id="spr_"+name,
            cell=cell,offset_px=offset or [0,0],collision=False,
            layer="Visual_Assets" if flat else "Instances",note=note))
        return self

    def structure(self,kind,rect,note):
        ch={"stairs":"^","bridge_ew":"=","bridge_ns":"|","broken_bridge":"x"}[kind]
        self.rect(rect,ch);self.s["structures"].append(dict(kind=kind,rect=rect,note=note))
        return self

    def checkpoint(self,old,cell,quiet_rect):
        old_id=next(k for k in OLD if k.startswith(old+"_"))
        sid=self.id+":checkpoint"
        self.objects.append(dict(type="checkpoint",cell=cell))
        self.s["checkpoints"].append(dict(id=sid,cell=cell,respawn_cell=cell,
            safe_rect=[cell[0]-1,cell[1]-1,cell[0]+1,cell[1]+1],quiet_rect=quiet_rect,
            behavior="E opens exactly 3 save slots; heal on successful save; snapshot all state together."))
        MIGRATION["checkpoints"][old_id+":checkpoint"]=dict(id=sid,scene_id=self.id,respawn_cell=cell)
        return self

    def loop(self,name,points,purpose):
        self.s["exploration_loops"].append(dict(name=name,waypoints=points,purpose=purpose,scene_transition=False))
        self.path(points)
        return self

    def core(self):
        return dict(room_id=self.room_id,display_name=self.name,size_cells=[self.w,self.h],
            terrain=["".join(r) for r in self.grid],exits=self.exits,objects=self.objects,
            music="mus_desert",weather=dict(sandstorm=True,tumbleweeds=True),
            notes=f"CURRENT scene design v2, {self.id}. Places are continuously connected; only explicit border exits load another scene. See scene_gameplay_specs.json; scene weather/encounter overrides are mandatory.")


a=Scene("desert_frontier","Desert Frontier",(128,80),[(2,35),(8,21),(17,13),(35,8),(58,6),(84,10),(105,8),(122,19),(125,40),(121,62),(108,72),(80,75),(60,70),(35,74),(15,65),(6,53)],"A broad first landscape: orient east, choose dune and canyon routes, climb a lookout loop, then recognize the oasis from multiple approaches.")
# One large outline, internal landforms and shared floor. No old rectangular maps are stitched together.
a.rect([17,18,22,24],"#").rect([32,29,36,32],"#")
a.rect([26,8,63,23],"#").rect([29,10,60,21],".")
a.structure("stairs",[32,22,36,23],"Five-wide west ascent to lookout shelf; north/south landings stay empty.")
a.structure("stairs",[54,22,58,23],"Five-wide east descent returns to the canyon's far approach; forms a continuous exploration loop.")
a.rect([48,27,53,52],"#").rect([48,32,53,37],".")
a.rect([61,42,67,50],"#").rect([69,24,74,29],"#")
a.rect([94,23,121,48],";").rect([100,27,112,34],"~").rect([98,29,99,32],"~")
a.rect([101,10,119,21],";").rect([103,12,112,17],"~")
a.place("rm_d01",[3,29,20,53],[9,40],"Breached-city stone gives way to open sand; no enemies around the first chest.")
a.place("rm_d02",[21,25,36,47],[28,40],"A first slow enemy on the main trail; dunes and the northern shelf invite a wider scan.")
a.place("rm_d03",[37,28,54,43],[45,35],"Read a broad canyon notch, the upper lookout return and a southern bypass.")
a.place("rm_d04",[55,26,74,42],[63,35],"Two separated cliff islands frame crossing paths without enclosing another small area.")
a.place("rm_d05",[69,43,96,68],[79,46],"A quiet dry riverbed winds toward green; an elective python pocket lies farther south.")
a.place("rm_d06",[94,23,122,51],[108,42],"A visible lake, palms, connected banks and safe star anchor the whole eastern basin.")
a.place("rm_o1",[26,8,63,23],[45,19],"Sunken Lookout becomes a two-stair shelf loop, with armor seen near the ledge and a separate way down.")
a.place("rm_o2",[99,10,119,22],[108,19],"Hidden Spring sits on the northern oasis-bank circuit; no loading door or dead-end branch.")
a.encounter("rm_d02","g1",[23,34,33,44],[[28,39]],"First undead windup lesson; wide sand around every side.")
a.encounter("rm_d03","g1",[38,30,46,38],[[42,34]],"A familiar attacker near the canyon's west approach.")
a.encounter("rm_d03","g2",[38,49,46,57],[[42,53]],"Elective duel on the southern return route; does not seal a passage.")
a.encounter("rm_d04","g1",[60,31,70,39],[[65,35]],"First skeleton warrior in a broad, uncluttered crossing.")
a.encounter("rm_d05","g1",[81,56,91,66],[[86,61]],"Python telegraph in a southern wash pocket; main oasis approach remains quiet.")
a.encounter("rm_o1","g1",[35,11,43,19],[[39,15]],"Optional shelf duel before the armor; two stairs allow a different return.")
for old,cell,north in [("rm_d01",[14,34],False),("rm_d02",[39,26],False),("rm_d03",[43,61],False),("rm_d04",[67,26],False),("rm_d05",[93,62],False),("rm_d06",[117,44],False),("rm_o1",[45,20],True),("rm_o2",[116,17],False)]:a.chest(old,cell,north)
a.prop("cactus_small",[17,49],[16,12]).prop("obelisk",[45,28],[40,28])
a.prop("palm",[93,33],[24,14]).prop("palm",[119,30],[24,14])
a.deco("ruin_block",[18,21],"City rubble on the blocked dune: westward visual anchor.")
a.deco("obelisk",[61,20],"Lookout marker on the shelf's solid east rim.")
a.deco("tree_dead",[64,46],"Wind-shaped silhouette on the central blocked island.")
a.deco("healing_spring",[108,15],"Noncolliding art on blocked water; healing interaction is on the dry bank.")
a.deco("bush",[97,37]).deco("pebbles",[73,58]).deco("skull",[40,60])
a.checkpoint("rm_d06",[108,42],[99,37,117,48])
a.s["initial_spawn"]=[7,40]
a.s["scripts"]=[dict(id="desert_arrival",trigger_rect=[5,38,11,42],event="chapter_start",once_flag="desert_arrival_seen",note="Intro ends at [7,40] facing east; initial death fallback is a complete snapshot here."),dict(id="hidden_spring_heal",trigger_rect=[105,18,109,20],event="interact_heal",once_flag=None,note="E on the bank heals without loot, XP or saving. At full HP do nothing.")]
a.s["elevation_notes"]=["Lookout shelf z1: [29,10..60,21], fully bounded by solid rock except two five-wide stairs. Basin z0. No free cliff crossing, jumping or one-way drops."]
a.s["primary_route"]=[[7,40],[28,40],[43,40],[43,35],[61,35],[75,35],[75,46],[96,46],[96,42],[108,42],[118,42],[118,40],[125,40]]
a.path(a.s["primary_route"])
a.loop("Lookout ridge circuit",[[28,40],[24,40],[24,25],[34,25],[34,20],[34,16],[56,16],[56,25],[61,25],[61,35]],"Leave the dune trail, climb west, claim shelf treasure, descend east and rejoin beyond the canyon approach.")
a.loop("Southern wash circuit",[[28,40],[28,57],[43,57],[43,53],[43,57],[72,57],[72,46],[96,46]],"A longer open-ground route passes the canyon's south end and reveals a coin pocket and python detour.")
a.loop("Oasis banks circuit",[[96,42],[95,42],[95,20],[117,20],[117,42],[108,42]],"Approach the oasis from either bank, discover the spring and return to a recognizable save landmark.")
a.s["batches"]=[dict(name="Opening expanse",places=["place_arrival","place_dune_trail","place_canyon_approach","place_sunken_lookout"],build="Block the broad basin, first combat and the full two-stair lookout circuit together. Do not make separate scenes for these places."),dict(name="Canyon and wash expansion",places=["place_split_cliffs","place_dry_wash"],build="Add the canyon notch, southern bypass, cliff islands and elective python pocket."),dict(name="Oasis expansion",places=["place_oasis_refuge","place_hidden_spring"],build="Extend into both lake banks, the northern spring circuit, checkpoint and east scene transition.")]

b=Scene("caravan_basin","Caravan Basin",(144,88),[(2,38),(7,22),(26,10),(51,5),(76,9),(99,6),(125,10),(140,17),(142,40),(136,67),(119,79),(90,83),(64,80),(39,84),(16,73),(5,56)],"An expansive travel basin: caravan wreck, cactus routes and bonefield lead to two usable chasm crossings, quiet ruins and a panoramic ascent.")
b.rect([30,31,39,38],"#").rect([51,12,58,27],"#").rect([20,61,32,72],"#").rect([102,14,110,27],"#")
b.rect([84,0,89,87],"C")
b.structure("broken_bridge",[84,26,89,30],"Broken northern span is fully blocked; no repair, jump or key objective.")
b.structure("bridge_ew",[84,44,89,48],"Five-wide main crossing; clear three-cell banks at both ends.")
b.structure("bridge_ew",[84,65,89,69],"Five-wide southern crossing makes a permanent regional loop, not a transition.")
b.rect([57,57,79,77],"_").rect([57,57,79,58],"M").rect([62,62,73,68],"~")
b.structure("bridge_ns",[66,62,68,68],"Three-wide cistern catwalk; both banks and the outer paving form a smaller loop within the basin.")
b.rect([107,28,120,29],"M").rect([105,28,106,36],"M").rect([119,28,120,36],"M")
b.rect([115,9,142,31],"#").rect([117,11,142,29],".")
b.structure("stairs",[126,30,132,31],"Seven-wide Great Desert Stairs; upper shelf connects directly to the next scene at the same elevation.")
b.place("rm_d07",[6,27,33,50],[17,43],"Wreck and scattered cargo can be approached from the trail or northern loop.")
b.place("rm_d08",[30,39,54,71],[42,49],"Loose cactus groves frame wide paths; the cache lies north, the python hollow south.")
b.place("rm_d09",[55,31,81,57],[67,41],"Melee and archer groups occupy separate open pockets around a visible eastward route.")
b.place("rm_d10",[80,23,95,72],[87,46],"The broken span points south toward a usable bridge; farther south another crossing rewards exploration.")
b.place("rm_d11",[103,27,123,55],[113,41],"Quiet open ruins and a save star provide an eastern anchor reached from either bridge.")
b.place("rm_d12",[115,9,142,54],[129,30],"Broad ascent to a walkable upper shelf; looking back west rewards treasure hunting.")
b.place("rm_o3",[29,10,59,29],[42,20],"Bandit Cache is a northern camp reached by a loop, with two routes back into the basin.")
b.place("rm_o4",[56,56,80,78],[67,70],"Buried Cistern is an exposed flooded foundation on the southern bridge circuit, continuously outdoors.")
b.encounter("rm_d07","g1",[13,34,23,44],[[18,39]],"First bandit in a clear clearing beside the wreck.")
b.encounter("rm_d07","g2",[28,44,38,54],[[33,49]],"A second fast attacker near the cactus trail; groups stay separated.")
b.encounter("rm_d08","g1",[40,57,50,67],[[45,62]],"Elective python pocket on the south side of the grove.")
b.encounter("rm_d09","g1",[56,34,66,44],[[61,39]],"Known warrior before the archer pocket.")
b.encounter("rm_d09","g2",[69,33,79,45],[[74,38],[70,44]],"An archer and warrior combine with broad flanking ground; no bridge combat.")
b.encounter("rm_d10","g1",[94,59,104,69],[[98,63]],"Optional bat encounter on the far southern bank, outside the crossing landings.")
b.encounter("rm_d12","g1",[117,45,125,53],[[121,49]],"Elective lower-terrace warrior; the save approach and stairs are calm.")
b.encounter("rm_d12","g2",[125,14,135,24],[[132,19]],"Upper-shelf archer, with a broad landing and routes around its pad.")
b.encounter("rm_o3","g1",[36,15,46,25],[[39,21],[44,18]],"Optional early caster plus fast melee; open camp, no ambush or exit lock.")
for old,cell in [("rm_d07",[29,26]),("rm_d08",[48,70]),("rm_d09",[77,51]),("rm_d10",[98,72]),("rm_d11",[105,53]),("rm_d12",[121,14]),("rm_o3",[49,17]),("rm_o4",[71,72])]:b.chest(old,cell)
b.prop("wagon_wreck",[22,31],[160,40],[21,31,23,31])
for cell in ([35,40],[48,37],[39,55],[51,69],[16,56]):b.prop("cactus_tall",list(cell),[24,16])
b.deco("ruin_block",[32,34],"Caravan stone cargo rests on blocked rock.")
b.deco("obelisk",[110,29],"Ruins inscription is on existing masonry, not a new blocker.")
b.deco("tree_dead",[25,66],"A southern silhouette points toward the cistern circuit.")
b.deco("skull",[63,49]).deco("pebbles",[76,75]).deco("bush_dead",[100,51])
b.checkpoint("rm_d11",[113,41],[103,33,119,44])
b.s["elevation_notes"]=["Great Stairs upper shelf z1: [117,11..142,29], bounded on west/north/south; only stairs and east scene pass connect it. Rest of basin z0. Cistern is a flat flooded foundation, not an overlapping lower floor."]
b.s["primary_route"]=[[2,40],[17,40],[17,43],[42,43],[42,49],[52,49],[52,41],[78,41],[78,46],[96,46],[113,46],[113,41],[128,41],[128,33],[128,20],[141,20]]
b.path(b.s["primary_route"])
b.loop("Northern camp circuit",[[25,43],[25,22],[42,22],[42,30],[62,30],[62,41]],"Detour past the bandit camp, then return on the bonefield's west approach.")
b.loop("Twin crossing circuit",[[52,49],[54,49],[54,74],[78,74],[78,67],[99,67],[109,67],[109,46],[113,46]],"Use the southern bridge and eastern bank to return via the main bridge; permanent geography, no switch or loading.")
b.loop("Cistern rim and catwalk",[[66,74],[67,74],[67,60],[76,60],[76,67],[78,67]],"Cross the water by catwalk or follow the outer paving; reconnect with the southern basin route.")
b.s["batches"]=[dict(name="Caravan and grove",places=["place_ruined_caravan","place_cactus_flats","place_bandit_cache"],build="Lay out shared travel floor, distinct combat pockets and the northern camp circuit."),dict(name="Bridge basin expansion",places=["place_bonefield","place_broken_bridge","place_buried_cistern"],build="Add both intact bridges, broken landmark, southern return and cistern rim/catwalk."),dict(name="Ruins and ascent",places=["place_forgotten_ruins","place_great_desert_stairs"],build="Complete quiet ruins, checkpoint, broad climb, upper treasure and east transition.")]

c=Scene("royal_expanse","Royal Expanse",(160,96),[(2,18),(10,7),(40,3),(74,9),(107,4),(136,7),(156,16),(158,47),(145,77),(115,89),(75,91),(36,84),(12,70),(4,47)],"A high, wind-scoured landscape opens into a royal approach: optional grotto and memorial loops precede the final save, an in-scene boss courtyard and the dungeon exterior.")
c.rect([8,45,14,56],"#")
c.rect([17,5,45,7],"#").rect([17,8,19,23],"#").rect([43,8,45,23],"#").rect([43,15,45,19],".")
c.rect([55,0,60,95],"C")
c.structure("bridge_ew",[55,34,60,40],"Seven-wide Royal Causeway, with clear banks; the visible bridge is a geographical passage, not a scene transition.")
c.rect([87,10,114,27],"M").rect([89,12,112,25],"_")
c.structure("stairs",[92,26,96,27],"West memorial ascent, five wide; all landings clear.")
c.structure("stairs",[105,26,109,27],"East memorial descent completes a pre-boss exploration loop.")
c.rect([148,0,159,95],"#")
c.rect([116,8,149,34],"M").rect([118,10,147,27],"_").rect([121,28,123,34],"_")
c.rect([128,14,140,23],".")
c.rect([150,12,157,27],"_").rect([148,17,149,21],"_")
c.rect([151,9,157,11],"M").rect([153,11,154,12],"_")
c.place("rm_d13",[5,25,51,62],[25,28],"Wide horizon on the same high level as the incoming pass; an elective worm basin lies south.")
c.place("rm_d14",[41,29,79,53],[57,37],"A royal bridge, a guard before it and a caster pocket after it; no combat on the span.")
c.place("rm_d15",[81,31,114,53],[96,37],"Quiet ceremonial ground with a northern memorial circuit and guaranteed consumables.")
c.place("rm_d16",[115,35,133,47],[122,38],"Final yellow star, seven tiles south of the boss gate with no fight or transition between them.")
c.place("rm_d17",[116,8,149,34],[132,20],"A visibly distinct paved courtyard inside this scene, physically gated for combat.")
c.place("rm_d18",[150,9,157,27],[154,19],"A quiet dungeon exterior physically reachable only through the cleared courtyard; the doorway ends Chapter I.")
c.place("rm_o5",[17,5,45,24],[32,16],"Echo Grotto is an open rock recess with south and east access; no interior load or opaque roof.")
c.place("rm_o6",[87,10,114,28],[101,20],"Memorial Vault is a roofless upper terrace with two stairs, a guardian and premium optional armor.")
c.encounter("rm_d13","g1",[24,46,36,58],[[30,52]],"Elective worm emergence basin, with a broad escape ring and a reward beyond it.")
c.encounter("rm_d14","g1",[42,31,50,41],[[47,36]],"One known melee guard, kept away from bridge landings.")
c.encounter("rm_d14","g2",[65,31,77,43],[[71,34],[74,40]],"Caster and bandit combine on a broad far-bank pad; never fire onto the bridge.")
c.encounter("rm_o5","g1",[25,9,37,21],[[28,12],[35,12],[32,18]],"Optional bat pair plus telegraphed lunge; both grotto exits remain open.")
c.encounter("rm_o6","g1",[90,12,98,20],[[95,17]],"One memorial guardian, separated from stairs and the armor's approach.")
c.encounter("rm_d17","boss",[123,12,143,24],[[132,20]],"Uncluttered arena for laser movement, committed thunder warnings and capped summons.")
for old,cell in [("rm_d13",[39,58]),("rm_d14",[73,51]),("rm_d15",[114,48]),("rm_o5",[39,10]),("rm_o6",[105,17])]:c.chest(old,cell)
c.prop("pharaoh_statue",[118,37],[48,28]).prop("pharaoh_statue",[126,37],[48,28])
c.deco("tree_dead",[11,50],"Wind-scoured tree on the western rock island.")
c.deco("ruin_block",[18,10],"Grotto rock-rim shrine; the floor and exits stay fully visible.")
c.deco("obelisk",[101,11],"Memorial inscription on its solid north rim.")
c.deco("pharaoh_statue",[117,15],"Arena statues occupy masonry only, leaving all dodge lanes free.")
c.deco("pharaoh_statue",[148,25],"Matching statue remains outside the fight floor.")
c.deco("dungeon_entrance",[153,12],"Align the existing two-cell doorway with x153..154; ground base offset places its centre between tile centres.",[32,0])
c.deco("bush_dead",[104,49]).deco("pebbles",[41,64])
c.checkpoint("rm_d16",[122,38],[115,35,133,45])
c.s["elevation_notes"]=["Incoming plateau, causeway and royal forecourt are continuous base level z1 after the previous scene's stairs. Memorial terrace z2 is bounded by masonry and connects through its two stairs. Courtyard floor is flat at z1; sand inset is not a raised dais."]
c.s["primary_route"]=[[2,20],[12,20],[12,28],[25,28],[47,28],[47,37],[66,37],[96,37],[110,37],[110,39],[122,39],[122,38],[122,26],[132,26],[132,20],[145,20],[154,20],[154,14]]
c.path(c.s["primary_route"])
c.loop("Grotto circuit",[[12,28],[24,28],[24,22],[24,16],[40,16],[47,16],[47,28]],"Enter from the south, search the rock recess and return through the east opening to the plateau.")
c.loop("Southern worm basin circuit",[[25,28],[21,28],[21,63],[45,63],[45,45],[47,45],[47,37]],"Take a broad southern sweep; the worm remains elective and cannot emerge on the causeway approach.")
c.loop("Memorial terrace circuit",[[82,37],[84,37],[84,30],[94,30],[94,24],[94,22],[107,22],[107,30],[110,30],[110,37]],"Climb one stair and descend the other, then return to the tomb approach before the final star.")
c.rect([90,58,128,78],"_").rect([90,58,128,59],"M").rect([108,58,112,59],"_")
c.rect([90,60,91,76],"M").rect([90,65,91,69],"_")
c.rect([127,60,128,76],"M").rect([127,65,128,69],"_")
c.rect([90,77,128,78],"M").rect([108,77,112,78],"_")
c.new_place("place_sundial_court","Sundial Court",[83,53,136,80],[110,68],"A new quiet southern destination: an obelisk sundial, four broad openings, visible valuable treasure and different approaches back to the royal forecourt. No key, puzzle lock or new scene.")
c.new_chest([119,64],[["ancient_coin",2],["golden_scarab",1]],"Reward the wider southern landscape with collectibles; no power or progression requirement.")
c.prop("obelisk",[110,67],[40,28])
c.deco("ruin_block",[98,58],"Broken sundial-court wall on existing masonry.")
c.deco("pharaoh_statue",[123,78],"Weathered southern landmark, planted on the blocked foundation edge.")
c.loop("Sundial court circuit",[[96,37],[84,37],[84,54],[84,67],[97,67],[97,73],[122,73],[122,67],[134,67],[134,54],[110,54],[110,39]],"Explore the quiet southern court, pass its sundial and valuable cache, then return from another side toward the final star. Its north opening gives a shorter direct approach as well.")
c.s["boss"]=dict(entrance_gate_rect=[121,31,123,31],east_seal_rect=[148,17,149,21],
    entry_trigger_rect=[121,28,123,28],safe_intro_dave_cell=[122,26],pharaoh_cell=[132,20],
    intro_camera_target_pixel=[8160,1456],teleport_cells=[[132,20],[138,16],[127,17]],
    bat_spawn_cells=[[127,14],[142,22]],undead_spawn_cells=[[126,22],[140,13]],caps=dict(bats=2,undead=2),
    reward=dict(id=c.room_id+":u1",cell=[134,19],loot=[["pharaoh_ankh",1]],pending_if_full=True),
    states=dict(idle="Entrance open; east seal closed; boss idle; no encounter damage.",dialogue="Gate closed; east seal closed; all damage paused; play boss_intro.",combat="Both barriers closed; boss theme and capped summon scheduling active.",defeat="Stop every damage source; disintegration and slow whiteout; remove all threats.",cleared="Both barriers open; boss/summons/hazards/projectiles absent; pending reward may remain."),
    entry_rule="Continuously test occupied throat while idle; after full mask clears north of row29 top (pixel y1856), pause damage, walk to [122,26], close gate, frame dialogue. Intro-seen never suppresses encounter initialization after failure.",
    thunder_rule="Initial warning >=1.0 s; committed targets never move. Preserve a connected unmarked strip >=3 cells wide reachable at actual move speed; no offscreen damage or complete coverage.",
    summon_rule="Attempt capped bats per complete cycle. Use authored points >=3 cells from Dave and safe strip; postpone if no legal point.",
    camera_rule="Keep 1280x720. Frame both actors for intro, blend to follow before combat; attacking actors and warnings must be visible. No laser/thunder combination may close every escape.",
    music_by_state=dict(idle="mus_desert",dialogue="duck exploration music",combat="mus_pharaoh",defeat="stop loop, then resolution after whiteout",cleared="mus_desert"),
    health_tuning="3-5 minute initial target with main-route equipment; optional sword/armor and grinding not assumed.")
c.s["scripts"]=[dict(id="boss_entry",trigger_rect=[121,28,123,28],event="boss_intro",once_flag="boss_intro_seen",note=c.s["boss"]["entry_rule"]),dict(id="pharaoh_defeat",trigger_rect=None,event="boss_hp_zero",once_flag="boss_pharaoh_defeated",note="Disable all damage immediately. Disintegrate; slow whiteout; remove every summon, projectile and hazard; fade back; open both barriers and atomically commit defeated flag plus pending unique reward. No scene load; no Grail reward."),dict(id="dungeon_threshold",trigger_rect=[153,12,154,12],event="chapter_ending",once_flag="chapter_desert_complete",note="Require boss_pharaoh_defeated. Enter the doorway to show To Be Continued in rm_ending; no dungeon interior. Completed saves may replay the ending.")]
c.s["additional_asset_ids"]=["spr_gate_arena","spr_door_sealed","spr_dungeon_entrance","spr_ending_bg","spr_portrait_dave","spr_portrait_pharaoh","mus_pharaoh","mus_ending","spr_laser_beam","spr_laser_aim","spr_fx_laser_charge","spr_thunder_marker","spr_thunder_exclaim","spr_lightning_bolt","spr_fx_thunder_impact","spr_summon_crack","spr_fx_sand_burst","snd_gate_slam","snd_boss_summon","snd_laser_charge","snd_laser_fire","snd_thunder_warn","snd_thunder_strike","snd_boss_hurt","snd_disintegrate","snd_boss_death","snd_undead_rise"]
c.s["batches"]=[dict(name="Plateau expansion",places=["place_windblown_plateau","place_echo_grotto","place_royal_causeway"],build="Create the broad plateau, two elective loops, causeway and separated combat pockets."),dict(name="Royal forecourt expansion",places=["place_tomb_approach","place_memorial_vault","place_sundial_court","place_pharaohs_gate"],build="Add the quiet forecourt, two-stair memorial circuit, new southern Sundial Court loop and final star immediately south of the gate."),dict(name="Courtyard and ending",places=["place_pharaohs_courtyard","place_dungeon_threshold"],build="Build the in-scene arena enclosure, unavoidable entry trigger, two stateful barriers and ending exterior.")]
MIGRATION["unique_rewards"]["rm_d17_pharaohs_courtyard:u1"]=dict(id=c.room_id+":u1",scene_id=c.id,cell=[134,19])


def opening(scene,side,span,target,other):
    eid="east" if side=="E" else "west"
    scene.exits.append(dict(id=eid,side=side,rows=span,to=target.room_id,to_exit=other))
    x1,x2=(0,4) if side=="W" else (scene.w-5,scene.w-1)
    scene.rect([x1,span[0],x2,span[1]],"_")


opening(a,"E",[38,42],b,"west");opening(b,"W",[38,42],a,"east")
opening(b,"E",[18,22],c,"west");opening(c,"W",[18,22],b,"east")
for scene in SCENES.values():
    for ex in scene.exits:
        cell=[2 if ex["side"]=="W" else scene.w-3,sum(ex["rows"])//2]
        scene.s["arrivals"].append(dict(exit_id=ex["id"],cell=cell,pixel=[v*64+32 for v in cell],
            safe_rect=[cell[0]-1,cell[1]-1,cell[0]+1,cell[1]+1],facing=0 if ex["side"]=="W" else 4))
    # Quiet places and combat-specific suppression override scene feature enable flags.
    scene.s["weather"] = dict(default="Occasional cosmetic east-to-west wind/tumbleweeds only, never movement or collision effects.",
        suppress_rects=[p["quiet_rect"] for p in scene.s["checkpoints"]]+([c.s["boss"]["entry_trigger_rect"],[118,10,149,34],[150,9,157,27],[17,5,45,24],[87,10,114,28]] if scene is c else [[99,10,119,22]] if scene is a else [[57,57,79,77]]))
for scene in SCENES.values():
    for ex in scene.exits:
        target=next(s for s in SCENES.values() if s.room_id==ex["to"])
        ar=next(ar for ar in target.s["arrivals"] if ar["exit_id"]==ex["to_exit"])
        scene.s["transitions"].append(dict(exit_id=ex["id"],to_scene_id=target.id,to_room_id=target.room_id,
            to_exit=ex["to_exit"],destination_arrival_cell=ar["cell"],destination_arrival_pixel=ar["pixel"],condition="always"))


def asset_needs(scene):
    # Reuse explicit, already specified asset families; all IDs remain incoming requirements.
    needed={"tex_sand_light","tex_sand_dark","tex_rock_top","tex_cliff_face","tex_paving","mus_desert","snd_wind_loop","spr_tumbleweed"}
    for place in scene.s["places"]:
        if place["legacy_design_id"]:needed.update(OLD[place["legacy_design_id"]]["required_asset_ids"])
    needed.update(scene.s["additional_asset_ids"])
    needed.update(d["asset_id"] for d in scene.decor)
    needed.update("spr_"+p["prop"] for p in scene.s["solid_props"])
    for chest in scene.s["chests"]:needed.update("spr_icon_"+item for item,_ in chest["loot"])
    for ch,ids in {"~":["tex_water","tex_wet_sand"],";":["tex_grass"],"M":["tex_masonry_top","tex_masonry_face"],"C":["tex_chasm_wall","tex_chasm_void"],"^":["ts_stairs"],"=":["ts_bridge"],"|":["ts_bridge"]}.items():
        if any(ch in row for row in scene.grid):needed.update(ids)
    return sorted(needed)


MANIFEST=dict(design_version="desert_scenes_v2",status="current design handoff; not imported or playtested",
    supersedes="desert_v1: scene-based world design replaces the 24-small-map structure, not just its terminology.",
    scope=dict(principle="Expand explorable landscapes around landmarks, internal loops and rewards. No target number of scenes, places, branches or FFV maps.",partition_rationale="Three initial scenes follow distinct landscapes and meaningful travel passes. Dimensions are authored starting extents, expandable after exploration playtests.",ffv_region=None,ffv_version=None),
    scene_order=list(SCENES),scene_files={s.id:"scenes/"+s.room_id+".json" for s in SCENES.values()},
    world_origins_cells={a.id:[0,0],b.id:[128,0],c.id:[272,0]},
    terminology=dict(scene="A large continuous explorable landscape; only explicit scene-border exits load another scene.",place="Named landmark/district/pocket within a scene; crossing its bounds never loads, fades, teleports, resets enemies or closes a door.",technical_mapping="Keep room_id and rm_ keys only where Claude's GameMaker format requires them. Player/design language is scene and place.",batch="An implementation expansion of one scene. Batch boundaries are not player-facing borders or transitions."),
    coordinates=dict(tile_pixels=64,cell="[column,row], zero-based, x east, y south; ground point at [64*x+32,64*y+32]",rect="[x1,y1,x2,y2] inclusive",terrain_walkable=".,;_^=|",terrain_blocked="#M~Cx",arrival="W x2; E width-3; opening midpoint; clear 3x3 reserve.",view_pixels=[1280,720]),
    transition_rules="Only the two landscape passes change scenes. Border openings are five cells wide, clear for five cells inside; actors stay out of their corridors. Trigger on deliberate outward crossing, pause damage during load, clear projectiles and debounce until Dave leaves the destination corridor and releases outward intent. Returning uses the matching destination arrival, never the previous arbitrary position.",
    exploration_rules="Preferred eastward landmark order is preserved for wayfinding, not an invisible checklist. Players may roam, approach a landmark from another side, take longer routes, return by a different path and backtrack between scenes. Only Pharaoh gates the dungeon exterior; optional gear and grinding never gate progress.",
    fixed_across_revisits="World outline, landforms, routes, bridges/stairs, scene connections, checkpoint cells, enemy initial positions/IDs, chest loot/IDs, authored landmarks, arena barriers and threshold trigger. Internal exploration never respawns enemies or rerolls loot.",
    procedural_rules="No runtime topology generation. Seeded material/decal variation and bounded E-to-W ambient wind only, outside paths, combat pads, reserves and important silhouettes. No random solid cactus/rock placement. At most two nearby visible tumbleweeds; expire within ten seconds and remove on scene leave. Suppress weather at refuges, memorial/grotto, gate, arena and threshold.",
    open_world_implementation="Camera scrolls continuously across every place. Claude may chunk rendering/AI internally; chunk boundaries never cause scene transitions, fades, enemy resets or save boundaries. Sleep distant AI without deleting persistent spawn state; activate authored encounter pockets near the player. Use contract tile layers, foot masks and base-only prop collision.",
    migration="V1 files are superseded references. New core JSON retains Claude's exact keys; all exits remain E/W rows, so no cols schema extension is needed. Old chest IDs map explicitly to new scene-prefixed IDs in scene_migration.json; enemy spawn IDs remain stable. Save-format migration must remap checkpoint positions and reward claims atomically, or label old saves incompatible. Never silently load old local coordinates into a new scene.",
    provisional_contract_overrides="The user's scene-world directive replaces the provisional rm_d01..rm_d18 plus rm_o1..rm_o6 resource scheme in PROJECT_CONTRACT section 8 and the x24 layouts request in ASSET_REQUESTS C5. Retain tile size, core JSON keys, combat masks, art formats and layers. New resource IDs are incoming scene-content proposals for Claude's integration, not an edited engineering contract.",
    persistence="Keep three manual save stars. Snapshot scene ID/checkpoint cell, inventory, stats/XP, ordinary defeated-spawn IDs, chest remaining/claimed counts, pending unique reward, flags and cosmetic seed together. Death rolls back that snapshot as a unit. Pharaoh uses boss_pharaoh_defeated, not ordinary spawn-death state. Active encounter and projectiles reset on an undefeated checkpoint load; a defeated save recreates a cleared courtyard inside Royal Expanse.",
    initial=dict(scene_id=a.id,cell=[7,40],facing=0,checkpoint_fallback="Initial complete snapshot until first manual save."),
    ending=dict(scene_id=c.id,trigger_rect=[153,12,154,12],requires="boss_pharaoh_defeated",flag="chapter_desert_complete",ui="rm_ending",text="To Be Continued",dungeon_interior=False),
    active_files=["scene_manifest.json","scene_gameplay_specs.json","scene_decorations.json","scene_asset_manifest.json","scene_migration.json","scene_validation_report.json"],
    sources="Original brief and user's confirmed route, PROJECT_CONTRACT and ASSET_REQUESTS, local template references; current user steering replaces room-count planning with larger explorable scenes. FFV remains qualitative exploration inspiration, with no selected region/version or asserted map count.")


def ascii_grid(scene,rect=None,scale=1,overlays=True):
    rect=rect or [0,0,scene.w-1,scene.h-1]
    g=[r[:] for r in scene.grid]
    if overlays:
        for o in scene.objects:
            x,y=o["cell"];g[y][x]={"enemy":"e","chest":"c","checkpoint":"S","prop":"p"}[o["type"]]
        if scene.s["initial_spawn"]:
            x,y=scene.s["initial_spawn"];g[y][x]="i"
        for ar in scene.s["arrivals"]:
            x,y=ar["cell"];g[y][x]="a"
        if scene.s["boss"]:
            r=scene.s["boss"]["entrance_gate_rect"]
            for x in range(r[0],r[2]+1):g[r[1]][x]="g"
        for script in scene.s["scripts"]:
            r=script["trigger_rect"]
            if r:
                for y in range(r[1],r[3]+1):
                    for x in range(r[0],r[2]+1):
                        if g[y][x] not in "ceSpiag":g[y][x]="t"
    lines=[]
    for y in range(rect[1],rect[3]+1,scale):
        row=""
        for x in range(rect[0],rect[2]+1,scale):
            block=[g[yy][xx] for yy in range(y,min(y+scale,rect[3]+1)) for xx in range(x,min(x+scale,rect[2]+1))]
            priority="Scgieatp^=|x~CM#,;_."
            # Reduced maps prioritize gameplay markers, then the dominant terrain.
            special=next((c for c in "Scgieatp^=|x" if c in block),None)
            row+=special or max(set(block),key=lambda c:(block.count(c),-priority.index(c)))
        lines.append(f"{y:02} "+row)
    return "\n".join(lines)


def docs():
    DOC.mkdir(parents=True,exist_ok=True)
    text="""# Desert chapter - expanding scene world

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
"""
    text+="\n## Content-focused layout revision\n\nThe scene extents stay large, but unused sand is folded into irregular rock shoulders. Routes widen into distinct destinations rather than crossing a uniformly open basin. Authored scenery beats use caravan cargo, cactus shelters, bone trails, green banks and ceremonial ruins. Static placement is rebuilt by `focus_desert_layouts.py`, never randomized during play. Existing spawn identities, loot, stars, circuits and gates remain authoritative.\n\nTravel views target four persistent details and two landmark silhouettes; combat approaches use a lighter two-detail frame, with the full fighting pads and warning floor clear. Quiet refuges receive scenery outside the actual save interaction reserve. Coverage ignores defeated enemies and follows the camera's border clamping. The central Pharaoh arena deliberately keeps its readable sand/paving floor.\n\nRebuild imported rooms with `python tools/build_world.py rooms`. Run `python tools/validate_layout_focus.py` after the topology validator. Generate [the actual tile/sprite atlas](../../design/desert/previews/focused_world_rendered.png) and [nine player-view compositions](../../design/desert/previews/focused_camera_review.png) with `python tools/preview_desert_layouts.py`. These are static render reviews; GameMaker play-testing is still pending.\n"
    text+="\n## Runtime tile export and visibility correction\n\nTerrain rebuilds must regenerate `output_tileset.png`, including two-pixel edge extrusion, with the exact declared output stride. Stale prepared images caused the skull/enemy fragments and checkerboard terrain seen in the original runtime screenshot. Previews now read the same prepared images as the compiler; `validate_compiled_tilesets.py` verifies the packed atlases inside a GameMaker 2026 `.win` file.\n\nLocal repeat limits keep obelisks, wagons and identical tree silhouettes from forming rows. Routine ground dressing uses rocks and shrubs; only two authored skull decals remain. Tall scenery becomes 25% opaque when it would cover Dave or an enemy. Prop base collision and clear routes remain intact.\n\nRuntime verification on 2026-10-31 covered eleven views across all scenes and movement past a palm, over the basin bridge and cistern catwalk, and up the Great Desert Stairs. Palm and obelisk transparency were visually inspected. See `design/desert/runtime_layout_report.json`, `runtime_tile_validation_report.json`, and the captured images under `design/desert/previews/runtime/`. One audio-service warning occurred during scripted scene warps; no fatal runtime errors. The chapter now compiles from the command line with explicit project/user/runtime/cache paths.\n"
    text+="\n## Discovery routes and close scenery\n\nNarrow worn trails now bend gently and change width, with sand shoulders and broken stone stretches along the royal procession route. Small returning trails lead to twelve new, optional supply caches. Each has a named camp, garden, overlook or ruin composition; entering it shows a brief discovery caption once per saved run. Cache contents and the discovery flag use existing snapshot persistence. Rewards add consumables and collectibles, with no progression keys or mandatory equipment.\n\nFive scenery variants reuse the template's barrel and column pixels with ground-contact origins and complete opaque silhouette bounds. Build them with `python tools/build_scenery_library.py` before generating the design. Contextual ground materials distinguish planted gardens, survey aprons, shrines and worn cargo areas. Low shrubs and stones can dress route shoulders; the centre line, full fighting pads, treasure approaches, save reserves and structure landings stay readable.\n\nTravel views also require nearby details within the middle 11 by 7 tiles, so a tiny prop at a distant screen edge cannot satisfy the layout review. A green planting can anchor a junction while keeping the view low. Bridge/stair compositions, shores and the deliberately clear Pharaoh court have explicit framing rules. Static inspection compares actual opaque sprite bounds, including camera clamping.\n\n| Scene | New discovery | Persistent cache | Reward |\n|---|---|---|---|\n"
    for scene in SCENES.values():
        for discovery in scene.s["discoveries"]:
            reward=", ".join(f"{n} x {item}" for item,n in discovery["reward"])
            text+=f"| {scene.name} | {discovery['name']} | `{discovery['chest_id']}` | {reward} |\n"
    text+="\n[Discovery compositions](../../design/desert/previews/exploration_discoveries_review.png). Rebuild with `python tools/design_desert_scenes.py`, `python tools/build_world.py rooms`, then run both design/layout validators and the compiled-atlas validator.\n"
    text+="\nThe final compiled-game discovery run triggered all twelve captions, claimed every new cache, verified that repeated interaction grants no duplicate loot, and crossed the palm lane, bridge, cistern catwalk and stairs. It used the current scene exports and produced no runtime errors or audio warnings. User saves were not written. See [the native verification report](../../design/desert/discovery_runtime_report.json) and [captured discovery views](../../design/desert/previews/exploration_runtime/). These checks cover representative movement and interactions; combat balance and long-session performance remain separate work.\n"
    text=text.replace("These are static render reviews; GameMaker play-testing is still pending.","These are static render reviews; representative native-game checks are documented below.")
    (DOC/"DESERT_CHAPTER.md").write_text(text,encoding="utf-8")
    for scene in SCENES.values():
        s=scene.s
        text=f"# {scene.name} - expanding scene design\n\n[Current chapter structure](DESERT_CHAPTER.md). Stable scene ID `{scene.id}`; technical GameMaker resource `{scene.room_id}`. Starting extent **{scene.w} x {scene.h} tiles** ({scene.w*64} x {scene.h*64} px). {s['purpose']}\n\nNo place below is a separate loaded scene. All place boundaries and batch edges are metadata only.\n\n## Landscape overview\n\nReduced grid: one character summarizes 4 x 4 tiles; row labels are global tile rows. Full exact grid: `design/desert/scenes/{scene.room_id}.json`. Legend and coordinate rules are in the chapter document.\n\n```text\n"+ascii_grid(scene,scale=4)+"\n```\n\n"
        text+="Scene transitions:\n\n| Border | Opening rows | Arrival here | Destination scene / arrival |\n|---|---|---|---|\n"
        for ex,ar,tr in zip(scene.exits,s["arrivals"],s["transitions"]):text+=f"| {ex['side']} | {ex['rows']} | {ar['cell']}, pixels {ar['pixel']} | `{tr['to_scene_id']}` / {tr['destination_arrival_cell']} |\n"
        if s["initial_spawn"]:text+=f"\nIntro/first-death fallback: {s['initial_spawn']}, facing east. West scene border stays closed.\n"
        text+="\nPreferred walking route: "+" -> ".join(str(p) for p in s["primary_route"])+". This is a route suggestion, not a compulsory chain of place triggers.\n\nExploration circuits:\n\n"
        for loop in s["exploration_loops"]:text+=f"- **{loop['name']}**: {loop['purpose']} Waypoints: "+" -> ".join(str(p) for p in loop["waypoints"])+".\n"
        text+="\nElevation and structures:\n\n"
        for note in s["elevation_notes"]:text+="- "+note+"\n"
        for st in s["structures"]:text+=f"- `{st['kind']}` {st['rect']}: {st['note']}\n"
        text+="\n## Build this scene by expansion\n\n"
        for i,batch in enumerate(s["batches"],1):text+=f"{i}. **{batch['name']}**: {batch['build']} Places: "+", ".join("`"+p+"`" for p in batch["places"])+".\n"
        text+="\n## Places and readable local grids\n\nEach crop below uses global `[x,y]` coordinates, one character per tile. It is an inspection window into the shared scene, not an enclosed map or scene boundary. The crop's x origin is stated; row labels remain global. Objects outside a crop are still present in the same scene.\n"
        for place in s["places"]:
            r=place["rect"]
            text+=f"\n### {place['name']}\n\n`{place['place_id']}`; anchor {place['anchor']}; inspection extent {r}; x origin **{r[0]}**. {place['experience']}\n\n```text\n"+ascii_grid(scene,r)+"\n```\n"
        text+="\n## Gameplay placement\n\nEncounters (IDs retained across the redesign):\n\n"
        for enc in s["encounters"]:
            text+=f"- `{enc['id']}`: pad/leash {enc['combat_rect']}, max {enc['max_active']} active. {enc['purpose']} Activation: {enc['activation']}\n"
            for e in enc["enemies"]:text+=f"  - `{e['id']}`: `{e['enemy']}` at {e['cell']}.\n"
        text+="\nChests (all unlocked, no ordinary kill lock; overflow stays pending):\n\n"
        for chest in s["chests"]:
            history=f"Legacy ID `{chest['legacy_id']}` is mapped explicitly." if chest["legacy_id"] else "New scene-world reward; no legacy claim to migrate."
            text+=f"- `{chest['id']}` at {chest['cell']}: "+", ".join(f"{n} x `{item}`" for item,n in chest["loot"])+f". Approach {chest['approach_cell']}, interaction {chest['interaction_cell']}. {chest['intention']} {history}\n"
        text+="\nCheckpoint and scripts:\n\n"
        for cp in s["checkpoints"]:text+=f"- `{cp['id']}` at/respawn {cp['cell']}; clear 3 x 3 {cp['safe_rect']}; peaceful district {cp['quiet_rect']}. {cp['behavior']}\n"
        for script in s["scripts"]:text+=f"- `{script['id']}` at {script['trigger_rect']}, event `{script['event']}`, flag `{script['once_flag']}`: {script['note']}\n"
        if s["boss"]:
            text+="- Boss state/camera/music/caps: this scene's `boss` in `scene_gameplay_specs.json`. Gate "+str(s["boss"]["entrance_gate_rect"])+", east seal "+str(s["boss"]["east_seal_rect"])+"; unique reward `"+s["boss"]["reward"]["id"]+"` at "+str(s["boss"]["reward"]["cell"])+". Both barriers are within this scene, not loading exits.\n"
        text+="\nSolid props (terrain/chests handled separately):\n\n"
        for prop in s["solid_props"]:text+=f"- `{prop['prop']}` at {prop['cell']}; centred base {prop['footprint_px']} px, conservative blocked cells {prop['blocked_rect']}.\n"
        text+="\n## Decoration and required assets\n\nDecoration is separate, noncolliding art. Tall landmarks sit on existing blocked terrain unless their real base is listed as a solid prop above.\n\n"
        for d in scene.decor:text+=f"- `{d['asset_id']}` at {d['cell']}, offset {d['offset_px']}, layer `{d['layer']}`. {d['note'] or 'Sparse, readable dressing.'}\n"
        text+="\nEvery required asset ID (including shared character/combat families) is enumerated for this scene in `scene_gameplay_specs.json` and `scene_asset_manifest.json`. These are incoming requirements; exact prop aliases and animation suffixes still need Claude's asset mapping. Weather suppression rectangles are explicit in this scene's sidecar entry.\n\n"
        text+="`"+"`, `".join(s["required_asset_ids"])+"`.\n"
        (DOC/("scene_"+scene.id[3:]+".md")).write_text(text,encoding="utf-8")


def render():
    colors={".":"#e7cd90",",":"#b89c66",";":"#7d9f65","~":"#509fbd","#":"#785d48","M":"#817c70","_":"#c6bda1","^":"#dc9d4e","C":"#302e3c","=":"#ad7646","|":"#ad7646","x":"#78474c"}
    previews=[]
    for scene in SCENES.values():
        tile=8;legend_height=((len(scene.s['places'])+1)//2)*22
        im=Image.new("RGB",(scene.w*tile+36,scene.h*tile+102+legend_height),"#17212d");d=ImageDraw.Draw(im,"RGBA")
        font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",15);bold=ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf",23)
        d.text((16,8),scene.name+" / continuous exploration",font=bold,fill="#fff0cc")
        d.text((16,39),f"{scene.w} x {scene.h} tiles  |  named places never load another scene",font=font,fill="#bccbd6")
        ox,oy=16,68
        for y,row in enumerate(scene.grid):
            for x,ch in enumerate(row):d.rectangle([ox+x*tile,oy+y*tile,ox+(x+1)*tile-1,oy+(y+1)*tile-1],fill=colors[ch])
        for loop in scene.s["exploration_loops"]:
            d.line([(ox+(x+.5)*tile,oy+(y+.5)*tile) for x,y in loop["waypoints"]],fill=(43,147,166,155),width=2)
        for enc in scene.s["encounters"]:
            x1,y1,x2,y2=enc["combat_rect"];d.rectangle([ox+x1*tile,oy+y1*tile,ox+(x2+1)*tile-1,oy+(y2+1)*tile-1],outline="#bb514c")
        for obj in scene.objects:
            x,y=obj["cell"];cx=ox+(x+.5)*tile;cy=oy+(y+.5)*tile
            if obj["type"]=="enemy":d.ellipse([cx-3,cy-3,cx+3,cy+3],fill="#c33139",outline="#fff3d2")
            if obj["type"]=="chest":d.rectangle([cx-3,cy-3,cx+3,cy+3],fill="#ffdf54",outline="#67500d")
            if obj["type"]=="checkpoint":d.polygon([(cx,cy-5),(cx+5,cy),(cx,cy+5),(cx-5,cy)],fill="#fff348",outline="#786719")
            if obj["type"]=="prop":d.rectangle([cx-3,cy-3,cx+3,cy+3],fill="#50402b")
        for i,p in enumerate(scene.s["places"]):
            x,y=p["anchor"];cx=ox+(x+.5)*tile;cy=oy+(y+.5)*tile
            label=chr(65+i);d.rectangle([cx-9,cy-22,cx+9,cy-6],fill="#17212d")
            d.text((cx-5,cy-24),label,font=font,fill="#fff5db")
        if scene.s["boss"]:
            for key in ("entrance_gate_rect","east_seal_rect"):
                x1,y1,x2,y2=scene.s["boss"][key];d.rectangle([ox+x1*tile,oy+y1*tile,ox+(x2+1)*tile-1,oy+(y2+1)*tile-1],fill="#b270c2")
        for i,p in enumerate(scene.s["places"]):
            lx=16+(i%2)*(scene.w*tile//2);ly=scene.h*tile+78+(i//2)*22
            d.text((lx,ly),chr(65+i)+"  "+p["name"],font=font,fill="#d7e0e8")
        d.text((16,im.height-22),"Cyan: route circuits | Gold: chest / star | Red: encounter | Purple: barrier",font=font,fill="#d7e0e8")
        path=BASE/"previews"/(scene.id+".png");path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
        previews.append(im)
    width=max(i.width for i in previews);height=sum(i.height for i in previews)+22
    atlas=Image.new("RGB",(width,height),"#17212d");y=0
    for im in previews:atlas.paste(im,(0,y));y+=im.height
    atlas.save(BASE/"previews"/"scene_world_atlas.png")


if __name__=="__main__":
    from detail_desert_exploration import prepare_discoveries
    prepare_discoveries(SCENES.values())
    from focus_desert_layouts import focus_scenes
    focus_scenes(SCENES.values())
    MANIFEST["status"]="current integrated scene layout; GameMaker playtest pending"
    for scene in SCENES.values():
        scene.s["required_asset_ids"]=asset_needs(scene)
        dump(BASE/"scenes"/(scene.room_id+".json"),scene.core())
    dump(BASE/"scene_manifest.json",MANIFEST)
    dump(BASE/"scene_gameplay_specs.json",{s.id:s.s for s in SCENES.values()})
    dump(BASE/"scene_decorations.json",{s.id:s.decor for s in SCENES.values()})
    dump(BASE/"scene_migration.json",MIGRATION)
    old_assets={x["asset_id"]:x for x in json.loads((BASE/"asset_manifest.json").read_text(encoding="utf-8"))["assets"]}
    asset_scenes={}
    for scene in SCENES.values():
        for aid in scene.s["required_asset_ids"]:asset_scenes.setdefault(aid,[]).append(scene.id)
    dump(BASE/"scene_asset_manifest.json",dict(note="Required or inherited shared asset families, not an import-completion claim. Exact prop and animation aliases require Claude's mapping. See original ASSET_REQUESTS for art contracts.",assets=[dict(asset_id=aid,status=old_assets.get(aid,{}).get("status","planned_or_proposed_requires_mapping"),scenes=uses) for aid,uses in sorted(asset_scenes.items())]))
    # Make the previous manifest unambiguously inactive; preserve its data for review/migration.
    previous=json.loads((BASE/"chapter_manifest.json").read_text(encoding="utf-8"))
    previous.update(status="SUPERSEDED reference only; do not import",import_allowed=False,superseded_by="scene_manifest.json")
    dump(BASE/"chapter_manifest.json",previous)
    for path in DOC.glob("batch_*.md"):
        body=path.read_text(encoding="utf-8")
        marker="> SUPERSEDED: reference only. Use [the expanding scene design](DESERT_CHAPTER.md). These are no longer separate loaded areas.\n\n"
        if not body.startswith(marker):path.write_text(marker+body,encoding="utf-8")
    docs();render()
    print("Authored continuous scenes, place layouts, migration, current handoff and previews.")
