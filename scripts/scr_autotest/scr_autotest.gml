// scr_autotest - development-only scripted play-test driver.
// Inactive unless a file named "autotest.json" sits next to the game data; a normal install never has
// one. When active it replaces device input with scripted actions through the same input owner, so
// tests exercise the real state machine without needing window focus, and saves screenshots with
// screen_save. Steps (array "steps"):
//   {"wait": ticks}  {"press": action}  {"hold": action, "ticks": n}  {"mouse": [gx, gy]}
//   {"until_mode": MODE value, "max": ticks}  {"until_room": "rm_x", "max": ticks}
//   {"shot": "name"}  {"log": "text"}  {"state": true}  {"quit": true}
//   {"warp": {"room": "rm_sc_x", "cell": [x, y], "facing": "side"}}  {"flag": ["name", value]}
//   {"give": ["item_id", n]}  {"hp": n}  {"newgame": true}

function autotest_init() {
    global.autotest = undefined;
    if (!file_exists("autotest.json")) return;
    var _d = json_load_file("autotest.json");
    if (!is_struct(_d) || !is_array(struct_or(_d, "steps", undefined))) return;
    global.autotest = { steps: _d.steps, i: 0, wait: 0, until: undefined, until_max: 0, tick: 0,
                        hold_until: {}, prev: {}, mx: 640, my: 360 };
    show_debug_message("AUTOTEST active: " + string(array_length(_d.steps)) + " steps");
}

function autotest_active() {
    return variable_global_exists("autotest") && is_struct(global.autotest);
}

function autotest_down(_a) {
    var _u = struct_or(global.autotest.hold_until, _a, -1);
    return global.autotest.tick < _u;
}

function autotest_state() {
    var _s = "mode=" + string(global.mode) + " room=" + room_get_name(room) + " stack=" + string(global.ui.stack);
    if (instance_exists(obj_player)) {
        _s += " dave=" + string(round(obj_player.x)) + "," + string(round(obj_player.y)) + " cell=" +
              string(px_cell(obj_player.x)) + "," + string(px_cell(obj_player.y)) + " face=" + obj_player.facing +
              " state=" + obj_player.state;
    }
    _s += " hp=" + string(global.run.hp) + "/" + string(player_max_hp()) + " lvl=" + string(global.run.level) +
          " xp=" + string(global.run.xp) + " music=" + mus_current() + " cine=" + string(global.cine_lock) +
          " trans=" + string(is_struct(global.transition));
    if (instance_exists(obj_boss_ctrl)) _s += " boss=" + obj_boss_ctrl.state;
    return _s;
}

/// Advances the script once per tick, before input_update reads the virtual devices.
function autotest_tick() {
    if (!autotest_active()) return;
    var _t = global.autotest;
    _t.tick += 1;
    if (_t.wait > 0) {
        _t.wait -= 1;
        return;
    }
    if (is_struct(_t.until)) {
        _t.until_max -= 1;
        var _done = false;
        if (variable_struct_exists(_t.until, "mode")) _done = (global.mode == _t.until.mode) && !is_struct(global.transition);
        if (variable_struct_exists(_t.until, "room")) _done = (room_get_name(room) == _t.until.room) && !is_struct(global.transition);
        if (!_done && _t.until_max > 0) return;
        show_debug_message("AUTOTEST until " + (_done ? "met" : "TIMEOUT") + " " + autotest_state());
        _t.until = undefined;
    }
    while (_t.i < array_length(_t.steps) && _t.wait <= 0 && !is_struct(_t.until)) {
        var _s = _t.steps[_t.i];
        _t.i += 1;
        if (variable_struct_exists(_s, "wait")) _t.wait = _s.wait;
        else if (variable_struct_exists(_s, "press")) _t.hold_until[$ _s.press] = _t.tick + 2;
        else if (variable_struct_exists(_s, "hold")) _t.hold_until[$ _s.hold] = _t.tick + struct_or(_s, "ticks", 30);
        else if (variable_struct_exists(_s, "mouse")) { _t.mx = _s.mouse[0]; _t.my = _s.mouse[1]; }
        else if (variable_struct_exists(_s, "until_mode")) { _t.until = { mode: _s.until_mode }; _t.until_max = struct_or(_s, "max", 600); }
        else if (variable_struct_exists(_s, "until_room")) { _t.until = { room: _s.until_room }; _t.until_max = struct_or(_s, "max", 600); }
        else if (variable_struct_exists(_s, "shot")) screen_save(_s.shot + ".png");
        else if (variable_struct_exists(_s, "log")) show_debug_message("AUTOTEST " + _s.log + " | " + autotest_state());
        else if (variable_struct_exists(_s, "state")) show_debug_message("AUTOTEST state " + autotest_state());
        else if (variable_struct_exists(_s, "quit")) game_end();
        else if (variable_struct_exists(_s, "newgame")) game_new();
        else if (variable_struct_exists(_s, "flag")) flag_set(_s.flag[0], _s.flag[1]);
        else if (variable_struct_exists(_s, "give")) inv_add(_s.give[0], _s.give[1]);
        else if (variable_struct_exists(_s, "hp")) global.run.hp = _s.hp;
        else if (variable_struct_exists(_s, "kill_boss")) { with (obj_pharaoh) { invuln = false; last_swing = -1; enemy_take_hit(hp, -999, x, y); } }
        else if (variable_struct_exists(_s, "inv")) {
            var _txt = "";
            for (var k = 0; k < INV_SIZE; k++) { var _e = inv_get(k); if (is_struct(_e)) _txt += string(k) + ":" + _e.id + "x" + string(_e.n) + " "; }
            show_debug_message("AUTOTEST inv " + _txt + "| weapon=" + string(global.run.eq_weapon) + " armor=" + string(global.run.eq_armor));
        }
        else if (variable_struct_exists(_s, "flags")) show_debug_message("AUTOTEST flags " + json_stringify(global.run.flags) + " rewards=" + json_stringify(global.run.rewards) + " chests=" + json_stringify(global.run.chests) + " defeated=" + json_stringify(global.run.defeated));
        else if (variable_struct_exists(_s, "enemies")) {
            var _el = "";
            with (obj_enemy) _el += family + "@" + string(px_cell(x)) + "," + string(px_cell(y)) + ":" + state + ":hp" + string(hp) + " ";
            with (obj_pharaoh) _el += "pharaoh:" + state + ":hp" + string(hp) + " ";
            show_debug_message("AUTOTEST enemies " + _el);
        }
        else if (variable_struct_exists(_s, "warp")) {
            var _w = _s.warp;
            ui_clear();
            global.mode = MODE.PLAY;
            global.cine_lock = false;
            scene_go(_w.room, cell_px(_w.cell[0]), cell_px(_w.cell[1]), struct_or(_w, "facing", "down"), "load");
        }
    }
}

/// Virtual device state for one action (called from input_update when the driver is active).
function autotest_action(_a) {
    var _t = global.autotest;
    var _d = autotest_down(_a);
    var _was = struct_or(_t.prev, _a, false);
    _t.prev[$ _a] = _d;
    return [_d, _d && !_was];
}
