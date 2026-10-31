"""Independent checks of exported continuous-scene design JSON."""
import json
from pathlib import Path
from validate_desert_design import cells, flood, clearance, border, corridor

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"design"/"desert"
WALK=set(".,;_^=|")
LEGEND=WALK|set("#M~Cx")


def read(path):return json.loads((BASE/path).read_text(encoding="utf-8"))


def line_points(points):
    out=set()
    for (x1,y1),(x2,y2) in zip(points,points[1:]):
        if x1!=x2 and y1!=y2:raise ValueError("Nonorthogonal route segment")
        out.update(cells([min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2)]))
    return out


def run():
    m=read("scene_manifest.json");specs=read("scene_gameplay_specs.json")
    decor=read("scene_decorations.json");migration=read("scene_migration.json")
    legacy=read("gameplay_specs.json");asset_ids={a["asset_id"] for a in read("scene_asset_manifest.json")["assets"]}
    cores={sid:read(file) for sid,file in m["scene_files"].items()}
    by_room={v["room_id"]:sid for sid,v in cores.items()}
    errors=[];checks=0;results={};floors={};persistent_ids=set();mapped_chests=set();mapped_spawns=set()

    def check(ok,msg):
        nonlocal checks
        checks+=1
        if not ok:errors.append(msg)

    check(set(cores)==set(specs)==set(decor)==set(m["scene_order"]),"Current scene IDs differ")
    check(read("chapter_manifest.json").get("import_allowed") is False,"Legacy manifest not marked inactive")
    check(m["scope"]["ffv_region"] is None and m["scope"]["ffv_version"] is None,"FFV reference scope falsely specified")
    check("main_rooms" not in m["scope"] and "total_rooms" not in m["scope"],"Old room-count quota remains active")
    for sid,core in cores.items():
        start_errors=len(errors);s=specs[sid];w,h=core["size_cells"];grid=core["terrain"]
        check(set(core)=={"room_id","display_name","size_cells","terrain","exits","objects","music","weather","notes"},f"{sid}: core format differs from contract")
        check(s["room_id"]==core["room_id"],f"{sid}: technical resource ID mismatch")
        check(len(grid)==h and all(len(row)==w for row in grid),f"{sid}: malformed terrain dimensions")
        check(set("".join(grid))<=LEGEND,f"{sid}: unsupported terrain")
        terrain={(x,y) for y,row in enumerate(grid) for x,ch in enumerate(row) if ch in WALK}
        objects={};blocked=set()
        for obj in core["objects"]:
            typ=obj["type"];pos=tuple(obj["cell"])
            keys={"enemy":{"type","enemy","cell"},"chest":{"type","id","cell","loot"},"prop":{"type","prop","cell"},"checkpoint":{"type","cell"}}
            check(set(obj)==keys.get(typ,set()),f"{sid}: object schema mismatch")
            check(pos in terrain,f"{sid}: object {typ} at {pos} on blocked terrain")
            check(pos not in objects,f"{sid}: overlapping objects {pos}")
            objects[pos]=typ
            if typ=="chest":blocked.add(pos)
        for prop in s["solid_props"]:
            shape=cells(prop["blocked_rect"])
            check(shape<=terrain,f"{sid}: solid prop footprint off floor")
            check(not(shape&blocked),f"{sid}: solid prop/chest overlap")
            check(all(objects.get(p,"prop")=="prop" for p in shape),f"{sid}: footprint overlaps another actor")
            blocked.update(shape)
        floor=terrain-blocked;wide=clearance(floor)
        start=s["initial_spawn"] or s["arrivals"][0]["cell"]
        reach=flood(floor,start);wide_reach=flood(wide,start)
        check(reach==floor,f"{sid}: disconnected travel floor ({len(floor-reach)} cells)")
        if s["initial_spawn"]:
            x,y=s["initial_spawn"];check(cells([x-1,y-1,x+1,y+1])<=floor,f"{sid}: unsafe initial snapshot")
        borders=set();corridors=set()
        for ex in core["exits"]:
            check(set(ex)=={"id","side","rows","to","to_exit"},f"{sid}: exit not contract E/W rows format")
            check(ex["side"] in ("E","W"),f"{sid}: unexpected scene-boundary orientation")
            check(ex["rows"][1]-ex["rows"][0]+1>=5,f"{sid}: scene pass narrower than five")
            edge=border(core,ex);inside=corridor(core,ex);borders.update(edge);corridors.update(inside)
            check(edge<=terrain and inside<=floor,f"{sid}: blocked scene pass")
            check(not(set(objects)&inside),f"{sid}: object in scene transition corridor")
            dest_sid=by_room.get(ex["to"]);check(dest_sid is not None,f"{sid}: dangling scene destination")
            dest=cores[dest_sid];other=next(e for e in dest["exits"] if e["id"]==ex["to_exit"])
            check(other["to"]==core["room_id"] and other["to_exit"]==ex["id"],f"{sid}: nonreciprocal scene pass")
            ar=next(a for a in s["arrivals"] if a["exit_id"]==ex["id"])
            expected=[2 if ex["side"]=="W" else w-3,sum(ex["rows"])//2]
            check(ar["cell"]==expected and ar["pixel"]==[v*64+32 for v in expected],f"{sid}: bad safe arrival coordinate")
            check(cells(ar["safe_rect"])<=floor and not(cells(ar["safe_rect"])&set(objects)),f"{sid}: arrival reserve obstructed")
            check(tuple(ar["cell"]) in wide_reach,f"{sid}: arrival not connected by three-wide route")
            tr=next(t for t in s["transitions"] if t["exit_id"]==ex["id"])
            da=next(a for a in specs[dest_sid]["arrivals"] if a["exit_id"]==ex["to_exit"])
            check(tr["to_scene_id"]==dest_sid and tr["destination_arrival_cell"]==da["cell"] and tr["destination_arrival_pixel"]==da["pixel"],f"{sid}: destination arrival mismatch")
        actual={p for p in terrain if p[0] in (0,w-1) or p[1] in (0,h-1)}
        check(actual==borders,f"{sid}: unlisted scene border opening")
        all_paths=[dict(name="primary",waypoints=s["primary_route"])]+s["exploration_loops"]
        for path in all_paths:
            trace=line_points(path["waypoints"])
            missing=trace-wide_reach
            check(not missing,f"{sid}: {path['name']} has narrow/blocked route centres {sorted(missing)[:8]}")
            if path["name"]!="primary":
                check(path.get("scene_transition") is False,f"{sid}: local circuit contains loading transition")
                network=set().union(*(line_points(p["waypoints"]) for p in all_paths if p is not path))
                check(tuple(path["waypoints"][0]) in network and tuple(path["waypoints"][-1]) in network and path["waypoints"][0]!=path["waypoints"][-1],f"{sid}: circuit does not reconnect through distinct approaches {path['name']}")
        for place in s["places"]:
            check(place["transition"] is False,f"{sid}: place has a scene transition")
            check(tuple(place["anchor"]) in reach,f"{sid}: landmark anchor unreachable {place['place_id']}")
            check(tuple(place["anchor"]) in cells(place["rect"]),f"{sid}: landmark anchor outside inspection area")
        for chest in s["chests"]:
            cid=chest["id"];check(cid.startswith(core["room_id"]+":c"),f"{sid}: chest ID prefix")
            check(cid not in persistent_ids,f"{sid}: duplicated persistent chest ID");persistent_ids.add(cid)
            check(tuple(chest["interaction_cell"]) in reach,f"{sid}: unreachable chest interaction {cid}")
            check(tuple(chest["approach_cell"]) in wide_reach,f"{sid}: chest approach lacks three-wide access {cid}")
            check(sum(abs(a-b) for a,b in zip(chest["cell"],chest["interaction_cell"]))==1,f"{sid}: nonadjacent chest interaction")
            if chest["legacy_id"]:
                alias=migration["chests"].get(chest["legacy_id"])
                check(alias and alias["id"]==cid and alias["scene_id"]==sid,f"{sid}: missing chest ID migration")
                mapped_chests.add(chest["legacy_id"])
                original=next(c for sp in legacy.values() for c in sp["chests"] if c["id"]==chest["legacy_id"])
                check(original["loot"]==chest["loot"],f"{sid}: chest loot unintentionally changed")
        for cp in s["checkpoints"]:
            check(cells(cp["safe_rect"])<=floor and tuple(cp["cell"]) in wide_reach,f"{sid}: checkpoint unsafe")
            check(all(not(cells(cp["quiet_rect"])&cells(g["combat_rect"])) for g in s["encounters"]),f"{sid}: combat in checkpoint district")
        mapped=[]
        for group in s["encounters"]:
            r=group["combat_rect"];shape=cells(r)
            check(r[2]-r[0]+1>=7 and r[3]-r[1]+1>=7,f"{sid}: combat pad below 7x7")
            check(shape<=floor,f"{sid}: combat pad blocked {group['id']}")
            check(not(shape&corridors),f"{sid}: combat reaches scene pass {group['id']}")
            for e in group["enemies"]:
                check(tuple(e["cell"]) in shape,f"{sid}: enemy outside clear pad")
                check(e["id"] not in persistent_ids,f"{sid}: duplicate spawn ID");persistent_ids.add(e["id"])
                check(migration["enemy_spawns"].get(e["id"],{}).get("cell")==e["cell"],f"{sid}: spawn migration mismatch")
                mapped.append((e["enemy"],e["cell"]));mapped_spawns.add(e["id"])
        check(sorted(mapped)==sorted((o["enemy"],o["cell"]) for o in core["objects"] if o["type"]=="enemy"),f"{sid}: enemy core/sidecar mismatch")
        for structure in s["structures"]:
            kind=structure["kind"];r=structure["rect"]
            char={"stairs":"^","bridge_ew":"=","bridge_ns":"|","broken_bridge":"x"}[kind]
            check(all(grid[y][x]==char for x,y in cells(r)),f"{sid}: structure tile mismatch {kind}")
            x1,y1,x2,y2=r
            if kind in ("stairs","bridge_ns"):
                land=cells([x1,y1-2,x2,y1-1])|cells([x1,y2+1,x2,y2+2])
            elif kind=="bridge_ew":
                land=cells([x1-3,y1,x1-1,y2])|cells([x2+1,y1,x2+3,y2])
            else:land=set()
            if land:
                check(land<=floor and not(land&set(objects)),f"{sid}: structure landing obstructed {kind}")
                check(all(not(land&cells(g["combat_rect"])) for g in s["encounters"]),f"{sid}: combat overlaps landing {kind}")
        for script in s["scripts"]:
            if script["trigger_rect"]:check(cells(script["trigger_rect"])<=reach,f"{sid}: script trigger inaccessible/blocked")
        for d in decor[sid]:
            check(d["collision"] is False,f"{sid}: decoration contains collision")
            x,y=d["cell"];check(0<=x<w and 0<=y<h,f"{sid}: dressing outside scene")
            check((x,y) not in objects,f"{sid}: dressing covers gameplay object")
        check(set(s["required_asset_ids"])<=asset_ids,f"{sid}: missing required asset references")
        results[sid]=dict(status="pass" if len(errors)==start_errors else "fail",dimensions=[w,h],walkable_cells=len(floor),reachable_cells=len(reach),three_wide_centres=len(wide_reach),places=[p["name"] for p in s["places"]],circuits=[x["name"] for x in s["exploration_loops"]],scene_transitions=len(core["exits"]))
        floors[sid]=floor

    check(mapped_chests=={c["id"] for s in legacy.values() for c in s["chests"]},"Some original chest claims have no migration")
    check(mapped_spawns=={e["id"] for s in legacy.values() for g in s["encounters"] for e in g["enemies"]},"Some original enemy IDs were lost")
    order=m["scene_order"]
    for i,sid in enumerate(order):
        neighbors=set(([order[i-1]] if i else [])+([order[i+1]] if i+1<len(order) else []))
        check({by_room[e["to"]] for e in cores[sid]["exits"]}==neighbors,f"{sid}: scene graph differs from continuous eastward route")
    # Two usable bridges are genuinely alternative crossings, not cosmetic branches.
    basin="sc_caravan_basin";bridges=[s for s in specs[basin]["structures"] if s["kind"]=="bridge_ew"]
    for bridge in bridges:
        check((141,20) in flood(floors[basin]-cells(bridge["rect"]),[2,40]),"Caravan alternative crossing is not connected")
    # Boss gate, intro throat and final seal must remain meaningful inside a single scene.
    royal="sc_royal_expanse";s=specs[royal];boss=s["boss"];floor=floors[royal]
    gate=cells(boss["entrance_gate_rect"]);seal=cells(boss["east_seal_rect"]);trigger=cells(boss["entry_trigger_rect"])
    west=[2,20];target=[154,14]
    check(tuple(target) not in flood(floor-seal,west),"Dungeon exterior bypasses boss seal through wider landscape")
    check(tuple(boss["pharaoh_cell"]) not in flood(floor-trigger,west),"Boss intro throat can be bypassed")
    combat=flood(floor-gate-seal,boss["pharaoh_cell"])
    check(tuple(s["checkpoints"][0]["cell"]) not in combat,"Closed arena gate has an escape bypass")
    check(tuple(target) not in combat,"Combat can escape through east seal")
    check(tuple(target) in flood(floor,west),"Cleared courtyard does not reach dungeon exterior")
    for name in ("teleport_cells","bat_spawn_cells","undead_spawn_cells"):
        check(all(tuple(p) in combat for p in boss[name]),f"Boss {name} inaccessible")
    check(tuple(boss["reward"]["cell"]) in combat,"Boss pending reward unreachable")
    check(m["ending"]["dungeon_interior"] is False and m["ending"]["requires"]=="boss_pharaoh_defeated","Ending requirements changed")
    report=dict(design_version=m["design_version"],status="pass" if not errors else "fail",checks=checks,errors=errors,
        scenes=results,summary=dict(scene_resources=len(cores),landscape_passes=sum(len(c["exits"]) for c in cores.values())//2,internal_place_transitions=0,
            connected_circuits=sum(len(s["exploration_loops"]) for s in specs.values()),checkpoints=sum(len(s["checkpoints"]) for s in specs.values()),
            note="Counts describe this draft; they are not a scope quota or an FFV map count."),
        guarantee="Connected static scene topology, explicit three-tile-wide preferred/circuit routes, conservative prop/chest blockers, safe transitions and boss gate states. No runtime AI, performance, physics or save-code claim.",
        required_GameMaker_tests=["continuous camera and AI across place/chunk boundaries without resets", "far enemy sleeping without losing persistent spawn identity", "mask corner sliding, stairs, bridges, melee arc and knockback space", "ranged LOS and no attacks onto protected arrivals/landings", "both landscape passes, backtracking and held-input debounce", "save-format migration of IDs and checkpoint coordinates", "chest overflow and full snapshot rollback", "boss throat closure after whole mask clears, dialogue skip and retry", "warning visibility and reachable thunder strip at final move speed", "whiteout cleanup and cleared arena loaded inside the same scene", "pending unique reward and ending replay", "large-scene performance with bounded ambient effects"])
    (BASE/"scene_validation_report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"{report['status'].upper()}: {checks} checks; {len(errors)} errors.")
    for error in errors:print("  "+error)
    return 1 if errors else 0


if __name__=="__main__":raise SystemExit(run())
