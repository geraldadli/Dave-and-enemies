"""
write_object_events.py - writes the GML event files of every runtime object.

Event bodies are short calls into the script functions (scripts/scr_*), so object behaviour lives
in reviewable scripts. Rewritten template objects (obj_player, obj_manager, obj_menu_manager,
obj_chest) have their old GML Visual event files removed first. Run from the project root.
"""
import glob
import os

P = os.path.join(os.path.dirname(__file__), "..", "objects")

OBJECTS = {}


def obj(name, events, wipe=False):
    OBJECTS[name] = (events, wipe)


obj("obj_game", {
    "Create_0": "/// Persistent controller: data, settings, input, audio, UI state machine.\ngame_init();",
    "Step_1": "/// Input is polled once and routed to exactly one state handler before other objects step.\ngame_begin_step();",
    "Step_0": "game_step();",
    "Draw_64": "game_draw_gui();",
    "Other_4": "game_room_start();",
}, wipe=True)

obj("obj_menu_manager", {
    "Create_0": "/// Title screen bootstrap (rm_menu). The menu itself is drawn and routed by obj_game.\n"
                "if (!instance_exists(obj_game)) instance_create_depth(0, 0, -15000, obj_game);\n"
                "title_open();",
}, wipe=True)

obj("obj_manager", {
    "Create_0": "/// Per-room scene bootstrap: builds collision from scene data, spawns content and places Dave.\n"
                "if (!instance_exists(obj_game)) instance_create_depth(0, 0, -15000, obj_game);\n"
                "scene_manager_create();",
    "Step_0": "scene_manager_step();",
    "Step_2": "/// Depth sort by ground point (contract section 7), then camera.\n"
              "with (all) {\n"
              "    if (variable_instance_exists(id, \"sort_depth\") && sort_depth) depth = -floor(y);\n"
              "}\n"
              "scene_manager_camera();",
    "Draw_0": "scene_manager_draw_weather();",
    "CleanUp_0": "world_free();",
}, wipe=True)

obj("obj_player", {
    "Create_0": "/// Dave.\nplayer_setup();",
    "Step_0": "player_step();",
    "Draw_0": "player_draw();",
}, wipe=True)

obj("obj_enemy", {
    "Create_0": "/// Data-driven enemy (family set by the spawner).\n"
                "if (!variable_instance_exists(id, \"spawn_id\")) spawn_id = \"\";\n"
                "if (!variable_instance_exists(id, \"family\")) family = \"undead\";\n"
                "if (!variable_instance_exists(id, \"leash\")) leash = undefined;\n"
                "if (!variable_instance_exists(id, \"persistent_spawn\")) persistent_spawn = false;\n"
                "if (!variable_instance_exists(id, \"summoned\")) summoned = false;\n"
                "enemy_setup();",
    "Step_0": "enemy_step();",
    "Draw_0": "enemy_draw();",
    "CleanUp_0": "aud_loop_stop(\"w:\" + string(id), 0);",
})

obj("obj_pharaoh", {
    "Create_0": "/// The Undead Pharaoh (boss). Spawned and owned by obj_boss_ctrl.\npharaoh_setup();",
    "Step_0": "pharaoh_step();",
    "Draw_0": "pharaoh_draw();",
    "CleanUp_0": "aud_loops_stop_prefix(\"boss:\", 0);",
})

obj("obj_boss_ctrl", {
    "Create_0": "/// Pharaoh arena: barriers, encounter state, reward and the dungeon doorway.\nboss_ctrl_setup();",
    "Step_0": "boss_ctrl_step();",
})

obj("obj_chest", {
    "Create_0": "/// Persistent chest; contents survive partial pickups.\nchest_setup();",
    "Step_0": "if (lid_t >= 0 && world_active()) {\n"
              "    lid_t += 1;\n"
              "    lid = min(1, lid_t / 28);   // lid stop aligned to snd_chest_open (~0.468 s)\n"
              "    if (lid >= 1) lid_t = -1;\n"
              "}",
    "Draw_0": "chest_draw();",
    "Other_10": "chest_interact();",
}, wipe=True)

obj("obj_checkpoint", {
    "Create_0": "/// Yellow save star.\n"
                "if (!variable_instance_exists(id, \"cp_id\")) cp_id = \"\";\n"
                "if (!variable_instance_exists(id, \"respawn\")) respawn = [px_cell(x), px_cell(y)];\n"
                "if (!variable_instance_exists(id, \"location\")) location = \"\";\n"
                "sort_depth = true;\n"
                "anim = 0;\n"
                "near = false;",
    "Step_0": "anim += 1;\n"
              "var _in = instance_exists(obj_player) && world_active() && point_distance(x, y, obj_player.x, obj_player.y) < 96;\n"
              "if (_in) {\n"
              "    global.toast.prompt = scene_text(\"checkpoint_prompt\");\n"
              "    near = true;\n"
              "} else if (near) {\n"
              "    near = false;\n"
              "    global.toast.prompt = \"\";\n"
              "}",
    "Draw_0": "checkpoint_draw();",
    "Other_10": "checkpoint_interact();",
})

obj("obj_spring", {
    "Create_0": "/// Hidden Spring: E on the bank heals without loot, XP or saving.\n"
                "if (!variable_instance_exists(id, \"rect\")) rect = [px_cell(x), px_cell(y), px_cell(x), px_cell(y)];\n"
                "near = false;",
    "Step_0": "var _in = instance_exists(obj_player) && world_active() && rect_has_px(rect, obj_player.x, obj_player.y);\n"
              "if (_in) {\n"
              "    if (!near && global.toast.prompt == \"\") global.toast.prompt = \"E  Drink from the spring\";\n"
              "    near = true;\n"
              "} else if (near) {\n"
              "    near = false;\n"
              "    if (global.toast.prompt == \"E  Drink from the spring\") global.toast.prompt = \"\";\n"
              "}",
    "Other_10": "spring_interact();",
})

obj("obj_pickup", {
    "Create_0": "/// Loot pickup or the pending unique reward.\npickup_setup();",
    "Step_0": "if (!world_active() || !instance_exists(obj_player)) exit;\n"
              "bob += 1;\n"
              "var _near = point_distance(x, y, obj_player.x, obj_player.y) < 40;\n"
              "if (_near && touch_armed) {\n"
              "    touch_armed = false;\n"
              "    pickup_try();\n"
              "} else if (!_near) touch_armed = true;",
    "Draw_0": "pickup_draw();",
    "Other_10": "pickup_try();",
})

obj("obj_prop", {
    "Create_0": "/// Solid prop: collides on its base footprint only (contract section 6).\n"
                "if (!variable_instance_exists(id, \"spr\")) spr = spr_ph_prop;\n"
                "if (!variable_instance_exists(id, \"fp_w\")) fp_w = 32;\n"
                "if (!variable_instance_exists(id, \"fp_h\")) fp_h = 16;\n"
                "mask_index = spr_mask_unit;\n"
                "image_xscale = fp_w / 64;\n"
                "image_yscale = fp_h / 64;\n"
                "sort_depth = true;",
    "Draw_0": "draw_sprite(spr, 0, x, y);",
})

obj("obj_deco", {
    "Create_0": "/// Non-colliding decoration (scene_decorations.json).\n"
                "if (!variable_instance_exists(id, \"spr\")) spr = -1;\n"
                "if (!variable_instance_exists(id, \"flat\")) flat = false;\n"
                "sort_depth = !flat;",
    "Draw_0": "if (spr >= 0) draw_sprite(spr, 0, x, y);",
})

obj("obj_exit", {
    "Create_0": "/// Scene pass: loads the neighbouring scene on a deliberate outward crossing.\narmed = false;",
    "Step_0": "exit_step();",
})

obj("obj_gate", {
    "Create_0": "/// Arena entrance gate or eastern seal. Closed barriers block walking and projectiles.\n"
                "if (!variable_instance_exists(id, \"kind\")) kind = \"arena\";\n"
                "if (!variable_instance_exists(id, \"closed\")) closed = false;\n"
                "anim = closed ? 1 : 0;\n"
                "anim_dir = 0;\n"
                "sort_depth = true;",
    "Step_0": "gate_step();",
    "Draw_0": "gate_draw();",
})

obj("obj_projectile", {
    "Create_0": "projectile_setup();",
    "Step_0": "projectile_step();",
    "Draw_0": "projectile_draw();",
    "CleanUp_0": "aud_loop_stop(loop_key, 30);",
})

obj("obj_hazard", {
    "Create_0": "hazard_setup();",
    "Step_0": "hazard_step();",
    "Draw_0": "hazard_draw();",
})

obj("obj_fx", {
    "Create_0": "fx_setup();",
    "Step_0": "fx_step();",
    "Draw_0": "fx_draw();",
})

obj("obj_tumbleweed", {
    "Create_0": "/// Cosmetic tumbleweed rolling east to west; never collides.\n"
                "t = 0;\nspd = random_range(3, 4.5);\nhop = 0;\nspin = 0;",
    "Step_0": "if (!world_active()) exit;\n"
              "t += 1;\n"
              "x -= spd;\n"
              "hop = abs(sin(t / 9)) * 10;\n"
              "spin += spd * 4;\n"
              "if (t > 600 || x < global.cam_cx - 760) instance_destroy();",
    "Draw_0": "var _s = asset_or(\"spr_tumbleweed\", spr_ph_tumbleweed);\n"
              "draw_set_alpha(0.25);\n"
              "draw_ellipse_colour(x - 16, y - 4, x + 16, y + 4, c_black, c_black, false);\n"
              "draw_set_alpha(1);\n"
              "draw_sprite_ext(_s, 0, x, y - 22 - hop, 1, 1, spin, c_white, 1);",
})

obj("obj_intro", {
    "Create_0": "/// Opening cinematic director (rm_intro): 54 s, eight shots, data from intro_storyboard.json.\nintro_create();",
    "Step_0": "intro_step();",
    "Draw_0": "intro_draw_world();",
    "CleanUp_0": "intro_cleanup();",
})


def main():
    for name, (events, wipe) in OBJECTS.items():
        d = os.path.join(P, name)
        os.makedirs(d, exist_ok=True)
        if wipe:
            for f in glob.glob(os.path.join(d, "*.gml")) + glob.glob(os.path.join(d, "*.dnd")):
                os.remove(f)
        for ev, code in events.items():
            with open(os.path.join(d, ev + ".gml"), "w", encoding="utf-8", newline="\n") as f:
                f.write(code.strip("\n") + "\n")
    print("wrote events for", len(OBJECTS), "objects")


if __name__ == "__main__":
    main()
