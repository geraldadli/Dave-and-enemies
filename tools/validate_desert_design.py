"""Validate exported design JSON without assuming GameMaker runtime behavior."""
from collections import deque
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "design" / "desert"
WALK = set(".,;_^=|")
LEGEND = WALK | set("#M~Cx")


def read(name):
    return json.loads((BASE/name).read_text(encoding="utf-8"))


def cells(rect):
    x1,y1,x2,y2=rect
    return {(x,y) for y in range(y1,y2+1) for x in range(x1,x2+1)}


def flood(allowed, start):
    start=tuple(start)
    if start not in allowed:return set()
    seen={start};q=deque([start])
    while q:
        x,y=q.popleft()
        for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if p in allowed and p not in seen:
                seen.add(p);q.append(p)
    return seen


def clearance(allowed):
    # Centre positions where a full 3x3 square of floor is free.
    return {(x,y) for x,y in allowed if all((x+dx,y+dy) in allowed for dx in (-1,0,1) for dy in (-1,0,1))}


def border(room, ex):
    w,h=room["size_cells"];a,b=ex.get("rows",ex.get("cols"))
    if ex["side"] in "EW":return {(0 if ex["side"]=="W" else w-1,y) for y in range(a,b+1)}
    return {(x,0 if ex["side"]=="N" else h-1) for x in range(a,b+1)}


def corridor(room, ex):
    w,h=room["size_cells"];a,b=ex.get("rows",ex.get("cols"))
    if ex["side"]=="W":return cells([0,a,4,b])
    if ex["side"]=="E":return cells([w-5,a,w-1,b])
    if ex["side"]=="N":return cells([a,0,b,4])
    return cells([a,h-5,b,h-1])


def run():
    manifest=read("chapter_manifest.json")
    specs=read("gameplay_specs.json")
    decorations=read("decorations.json")
    catalog={a["asset_id"]:a for a in read("asset_manifest.json")["assets"]}
    rooms={p.stem:json.loads(p.read_text(encoding="utf-8")) for p in (BASE/"rooms").glob("*.json")}
    errors=[];checks=0;room_results={};topologies={};all_ids=set()

    def check(ok, message):
        nonlocal checks
        checks+=1
        if not ok:errors.append(message)

    check(len(rooms)==24,"Scope: expected exactly 24 rooms")
    check(len(manifest["main_route"])==18,"Scope: 18 main rooms")
    check(len(manifest["optional_attachments"])==6,"Scope: six optional rooms")
    check(set(rooms)==set(specs)==set(decorations),"Room/sidecar IDs differ")
    check(manifest["scope"]["ffv_region"] is None and manifest["scope"]["ffv_version"] is None,"Unspecified FFV scope changed")
    check(len(set(r for b in manifest["batches"] for r in b["rooms"]))==24,"Batches must partition all rooms")
    expected_keys={"room_id","display_name","size_cells","terrain","exits","objects","music","weather","notes"}
    expected_objects={"enemy":{"type","enemy","cell"},"chest":{"type","id","cell","loot"},"prop":{"type","prop","cell"},"checkpoint":{"type","cell"}}
    for rid,room in rooms.items():
        before=len(errors);spec=specs[rid];w,h=room["size_cells"];grid=room["terrain"]
        check(set(room)==expected_keys,f"{rid}: extra/missing contract top-level keys")
        check(room["room_id"]==rid,f"{rid}: filename/ID mismatch")
        check(len(grid)==h and all(len(row)==w for row in grid),f"{rid}: grid size mismatch")
        check(set("".join(grid))<=LEGEND,f"{rid}: unsupported terrain character")
        terrain={(x,y) for y,row in enumerate(grid) for x,ch in enumerate(row) if ch in WALK}
        occupied={};blocked=set()
        for obj in room["objects"]:
            kind=obj["type"];p=tuple(obj["cell"])
            check(set(obj)==expected_objects.get(kind,set()),f"{rid}: invalid contract object keys {obj}")
            check(p in terrain,f"{rid}: {kind} on blocked terrain {p}")
            check(p not in occupied,f"{rid}: overlapping object at {p}")
            occupied[p]=kind
            if kind=="chest":blocked.add(p)
        for prop in spec["collision_footprints"]:
            footprint=cells(prop["blocked_rect"])
            check(footprint<=terrain,f"{rid}: prop footprint intersects blocked terrain")
            check(not (blocked & footprint),f"{rid}: overlapping footprints")
            check(all(occupied.get(p,"prop")=="prop" for p in footprint),f"{rid}: prop footprint overlaps gameplay object")
            blocked.update(footprint)
        allowed=terrain-blocked
        wide=clearance(allowed)
        arrivals={a["exit_id"]:a for a in spec["arrivals"]}
        starts=[a["cell"] for a in spec["arrivals"]]
        if spec["entry_spawn"]:starts.append(spec["entry_spawn"])
        check(bool(starts),f"{rid}: no entrance or initial spawn")
        reachable=flood(allowed,starts[0]);wide_reachable=flood(wide,starts[0])
        check(reachable==allowed,f"{rid}: disconnected walkable pocket")
        check(all(tuple(p) in reachable for p in starts),f"{rid}: arrivals disconnected")
        check(all(tuple(p) in wide_reachable for p in starts),f"{rid}: arrivals lack connected three-cell-wide paths")
        for p in spec["route_waypoints"]:
            check(tuple(p) in reachable,f"{rid}: route waypoint {p} not reachable")
            # Last 2 cells into a chest/internal doorway can be narrower; core route must not be.
            if rid in manifest["main_route"] and rid!="rm_d18_dungeon_threshold":
                check(tuple(p) in wide_reachable,f"{rid}: route waypoint {p} lacks 3-cell clearance")
        expected_border=set();entry_corridors=set()
        for ex in room["exits"]:
            check(ex["to"] in rooms,f"{rid}: dangling destination")
            dest=rooms[ex["to"]]
            others=[e for e in dest["exits"] if e["id"]==ex["to_exit"]]
            check(len(others)==1 and others[0]["to"]==rid and others[0]["to_exit"]==ex["id"],f"{rid}: nonreciprocal {ex['id']}")
            span=ex.get("rows",ex.get("cols"));check(span[1]-span[0]+1>=3,f"{rid}: narrow exit")
            expected_border.update(border(room,ex))
            entry_corridors.update(corridor(room,ex))
            check(border(room,ex)<=terrain,f"{rid}: blocked exit {ex['id']}")
            a=arrivals[ex["id"]];x,y=a["cell"]
            expected={"W":[2,(sum(span)//2)],"E":[w-3,(sum(span)//2)],"N":[(sum(span)//2),2],"S":[(sum(span)//2),h-3]}[ex["side"]]
            check(a["cell"]==expected and a["pixel"]==[x*64+32,y*64+32],f"{rid}: incorrect arrival {ex['id']}")
            check(cells(a["safe_rect"])<=allowed,f"{rid}: unsafe arrival reserve {ex['id']}")
            check(corridor(room,ex)<=allowed,f"{rid}: entry corridor blocked {ex['id']}")
            check(not(set(occupied)&cells(a["safe_rect"])),f"{rid}: object in arrival reserve {ex['id']}")
            t=next(t for t in spec["transitions"] if t["exit_id"]==ex["id"])
            da=next(a2 for a2 in specs[ex["to"]]["arrivals"] if a2["exit_id"]==ex["to_exit"])
            check(t["destination_arrival_cell"]==da["cell"] and t["destination_arrival_pixel"]==da["pixel"],f"{rid}: transition arrival mismatch")
            for obj in room["objects"]:
                if obj["type"] in ("enemy","prop"):
                    dist=min(max(abs(obj["cell"][0]-bx),abs(obj["cell"][1]-by)) for bx,by in border(room,ex))
                    check(dist>=2,f"{rid}: actor too near opening")
        actual_border={p for p in terrain if p[0] in (0,w-1) or p[1] in (0,h-1)}
        check(actual_border==expected_border,f"{rid}: unintended border hole or missing opening")
        for c in spec["chests"]:
            check(c["id"].startswith(rid+":c"),f"{rid}: invalid chest ID")
            check(c["id"] not in all_ids,f"{rid}: duplicate persistent ID")
            all_ids.add(c["id"])
            check(tuple(c["interaction_cell"]) in reachable and tuple(c["approach_cell"]) in reachable,f"{rid}: unreachable chest {c['id']}")
            check(tuple(c["approach_cell"]) in wide_reachable,f"{rid}: chest approach lacks three-cell clearance {c['id']}")
            check(tuple(c["interaction_cell"]) not in entry_corridors,f"{rid}: chest interaction in entry corridor")
            check(abs(c["interaction_cell"][0]-c["cell"][0])+abs(c["interaction_cell"][1]-c["cell"][1])==1,f"{rid}: chest approach not adjacent")
        for cp in spec["checkpoints"]:
            check(tuple(cp["respawn_cell"]) in reachable and cells(cp["safe_rect"])<=allowed,f"{rid}: unsafe checkpoint")
            check(not spec["encounters"],f"{rid}: checkpoint room contains enemies")
        mapped=[]
        for encounter in spec["encounters"]:
            rect=encounter["combat_rect"];x1,y1,x2,y2=rect
            check(x2-x1+1>=7 and y2-y1+1>=7,f"{rid}: combat pad below 7x7")
            check(cells(rect)<=allowed,f"{rid}: combat pad contains terrain/prop/chest blocker {encounter['id']}")
            check(not(cells(rect)&entry_corridors),f"{rid}: combat pad overlaps entry corridor {encounter['id']}")
            for e in encounter["enemies"]:
                check(tuple(e["cell"]) in cells(rect),f"{rid}: enemy outside combat pad")
                check(e["id"] not in all_ids,f"{rid}: duplicate enemy ID")
                all_ids.add(e["id"]);mapped.append((e["enemy"],e["cell"]))
        check(sorted((e["enemy"],e["cell"]) for e in room["objects"] if e["type"]=="enemy")==sorted(mapped),f"{rid}: enemy stable-ID mapping differs")
        for structure in spec["structures"]:
            kind=structure["kind"];rect=structure["rect"]
            char={"stairs":"^","bridge_ew":"=","bridge_ns":"|","broken_bridge":"x"}.get(kind)
            if char:
                check(all(grid[y][x]==char for x,y in cells(rect)),f"{rid}: structure footprint terrain mismatch {kind}")
            x1,y1,x2,y2=rect
            if kind in ("stairs","bridge_ns"):
                landings=cells([x1,y1-2,x2,y1-1])|cells([x1,y2+1,x2,y2+2])
            elif kind=="bridge_ew":
                landings=cells([x1-3,y1,x1-1,y2])|cells([x2+1,y1,x2+3,y2])
            else:landings=set()
            if landings:
                check(landings<=allowed,f"{rid}: landing not clear for {kind}")
                check(not (landings & set(occupied)),f"{rid}: actor/prop on landing for {kind}")
                check(all(not(landings & cells(g["combat_rect"])) for g in spec["encounters"]),f"{rid}: combat leash overlaps landing for {kind}")
        for script in spec["scripts"]:
            if script["trigger_rect"]:
                check(cells(script["trigger_rect"])<=allowed,f"{rid}: script trigger on blocked cell")
                check(bool(cells(script["trigger_rect"])&reachable),f"{rid}: unreachable script trigger")
        for deco in decorations[rid]:
            check(deco["collision"] is False,f"{rid}: decoration includes collision")
            x,y=deco["cell"];check(0<=x<w and 0<=y<h,f"{rid}: decoration out of bounds")
            check(tuple(deco["cell"]) not in occupied,f"{rid}: decoration over gameplay object")
        check(set(spec["required_asset_ids"])<=set(catalog),f"{rid}: missing asset manifest entry")
        room_results[rid]=dict(status="pass" if len(errors)==before else "fail",walkable_cells=len(allowed),reachable_cells=len(reachable),three_wide_centres=len(wide_reachable),arrivals=len(starts),chests=len(spec["chests"]),enemies=len(mapped))
        topologies[rid]=allowed

    main=manifest["main_route"]
    for i,rid in enumerate(main):
        expected=set(([main[i-1]] if i else [])+([main[i+1]] if i+1<len(main) else []))
        actual={e["to"] for e in rooms[rid]["exits"] if e["to"] in main}
        check(actual==expected,f"Main route order altered at {rid}")
        if i+1<len(main):check(any(e["side"]=="E" and e["to"]==main[i+1] for e in rooms[rid]["exits"]),f"{rid}: main journey not eastward")
    for link in manifest["optional_attachments"]:
        child=rooms[link["optional"]]
        check(len(child["exits"])==1 and child["exits"][0]["to"]==link["parent"],f"{child['room_id']}: optional not a reciprocal dead-end branch")
    boss_id="rm_d17_pharaohs_courtyard";boss=specs[boss_id]["boss"]
    floor=topologies[boss_id];gate=cells(boss["entrance_gate_rect"])
    east=next(e for e in rooms[boss_id]["exits"] if e["id"]=="east")
    sealed=border(rooms[boss_id],east)
    combat=flood(floor-gate-sealed,boss["entry_trigger_cell"])
    check((2,17) not in combat,"Boss entrance gate has a bypass while closed")
    check(not(combat&sealed),"Boss east seal bypass")
    check(tuple(boss["reward"]["cell"]) in combat,"Boss reward point not reachable in arena")
    clear=flood(floor,[2,17])
    east_arrival=next(a["cell"] for a in specs[boss_id]["arrivals"] if a["exit_id"]=="east")
    check(tuple(east_arrival) in clear,"Boss cleared exits not connected")
    entry_trigger=cells(next(s["trigger_rect"] for s in specs[boss_id]["scripts"] if s["id"]=="boss_entry"))
    boss_spawn=specs[boss_id]["encounters"][0]["enemies"][0]["cell"]
    check(tuple(boss_spawn) not in flood(floor-entry_trigger,[2,17]),"Boss entry trigger can be bypassed from vestibule")
    for key in ("teleport_cells","bat_spawn_cells","undead_spawn_cells"):
        check(all(tuple(p) in combat for p in boss[key]),f"Boss {key} inaccessible")
    check(all(t["condition"]=="boss_pharaoh_defeated" for t in specs[boss_id]["transitions"] if t["exit_id"]=="east"),"Boss exit missing state condition")
    threshold="rm_d18_dungeon_threshold"
    check(specs[threshold]["scripts"][0]["trigger_rect"]==[30,4,31,4],"Ending trigger changed")
    check(manifest["external_states"]["ending"]["dungeon_interior"] is False,"Dungeon interior unexpectedly requested")
    report=dict(status="pass" if not errors else "fail",checks=checks,errors=errors,
        rooms=room_results,summary=dict(rooms=len(rooms),directed_exits=sum(len(r["exits"]) for r in rooms.values()),chests=sum(len(s["chests"]) for s in specs.values()),initial_enemies=sum(len(g["enemies"]) for s in specs.values() for g in s["encounters"]),checkpoints=sum(len(s["checkpoints"]) for s in specs.values())),
        guarantee="Static authored topology under full-cell terrain blockers, conservative prop/chest blockers, and explicit boss gate states. Actual collision masks are smaller. No dynamic AI/physics/timing claim.",
        required_IDE_checks=["8-direction movement and corner sliding with dedicated masks", "melee swing arc, knockback, kiting and enemy leash behavior in each pad", "ranged LOS against cliff/masonry; no attacks on entry corridors or structure landings", "bridge rails and stair art leave authored openings intact", "all outbound and reciprocal transitions including held input", "chest overflow, partial claims and checkpoint rollback", "three independent saves and restart before first save", "boss gate closure after whole mask passes; dialogue skip and death restart", "thunder safe-strip reachability at final movement speed in every phase", "whiteout disables damage then removes all threats", "load cleared arena, pending unique reward/full inventory", "threshold ending and completed-save replay"])
    (BASE/"validation_report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"{report['status'].upper()}: {checks} checks; {len(rooms)} rooms; {len(errors)} errors.")
    for error in errors:print("  "+error)
    return 1 if errors else 0


if __name__=="__main__":
    raise SystemExit(run())
