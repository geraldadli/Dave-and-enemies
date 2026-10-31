// scr_ui_menus - pause, settings, three-slot save/load and the nested confirmation (UI_SPEC 7-8).

// ================================================================== pause
function pause_open(_from_dialogue) {
    global.pause_ui = { focus: 0, from_dialogue: _from_dialogue };
    ui_push(OV.PAUSE);
    aud_blip_cancel();
    inp_block_all();
}

function pause_items() {
    var _pu = global.pause_ui;
    var _row2;
    if (_pu.from_dialogue) _row2 = { label: "Skip scene", enabled: true, reason: "" };
    else {
        var _cp = checkpoint_in_range();
        _row2 = { label: "Save Game", enabled: !is_undefined(_cp), reason: "Save at a checkpoint." };
    }
    var _load_ok = save_any_valid();
    return [
        { label: "Resume", enabled: true, reason: "" },
        { label: "Settings", enabled: true, reason: "" },
        _row2,
        { label: "Load Game", enabled: _load_ok, reason: _load_ok ? "" : "No saves available." },
        { label: "Main Menu", enabled: true, reason: "" },
        { label: "Quit Game", enabled: true, reason: "" }
    ];
}

function pause_resume() {
    ui_remove(OV.PAUSE);
    ui_snd("snd_ui_cancel");
    inp_block_all();
}

function pause_step() {
    var _pu = global.pause_ui;
    if (inp_pressed("pause") || inp_pressed("rmb")) {
        inp_consume("pause");
        inp_consume("rmb");
        pause_resume();
        return;
    }
    var _act = vmenu_input(pause_items(), _pu, 464, 200, 352, 48, 60);
    if (_act < 0) return;
    switch (_act) {
        case 0: pause_resume(); break;
        case 1: ui_snd("snd_ui_confirm"); settings_open("pause"); break;
        case 2:
            if (_pu.from_dialogue) {
                ui_snd("snd_ui_confirm");
                confirm_open("Skip scene?", "The encounter begins at once.", "", "Cancel", "Skip scene", false,
                    function() {
                        ui_remove(OV.PAUSE);
                        dialogue_finish();
                    });
            } else {
                ui_snd("snd_checkpoint");
                saveload_open("save", "pause", checkpoint_in_range());
            }
            break;
        case 3: ui_snd("snd_ui_confirm"); saveload_open("load", "pause", undefined); break;
        case 4:
            if (session_unsaved()) {
                confirm_open("Return to main menu?", "Unsaved progress will be lost.", "", "Cancel", "Main Menu", true,
                    function() { game_to_menu(); });
            } else game_to_menu();
            break;
        case 5:
            if (session_unsaved()) {
                confirm_open("Quit the game?", "Unsaved progress will be lost.", "", "Cancel", "Quit Game", true,
                    function() { game_end(); });
            } else game_end();
            break;
    }
}

function pause_draw() {
    var _pu = global.pause_ui;
    ui_dim(0.6);
    ui_panel(440, 88, 400, 544);
    text_draw(464, 112, "Paused", "title", C_TEXT);
    var _items = pause_items();
    vmenu_draw(_items, _pu, 464, 200, 352, 48, 60);
    var _f = _items[_pu.focus];
    var _hover_reason = "";
    for (var i = 0; i < array_length(_items); i++) {
        if (ui_hit(464, 200 + 60 * i, 352, 48) && !_items[i].enabled) _hover_reason = _items[i].reason;
    }
    var _foot = (_hover_reason != "") ? _hover_reason : (_f.enabled ? "" : _f.reason);
    if (_foot == "" && global.mode == MODE.PLAY) _foot = scene_text(global.run.objective);
    text_draw(464, 580, text_fit(_foot, "meta", 352), "meta", C_MUTED);
}

// ================================================================== settings
function settings_open(_caller) {
    global.set_ui = { focus: 0, drag: -1, caller: _caller };
    ui_push(OV.SETTINGS);
    inp_block_all();
}

function settings_close() {
    settings_save();
    ui_remove(OV.SETTINGS);
    ui_snd("snd_ui_cancel");
    inp_block_all();
}

function settings_rows() {
    return [
        { key: "music", label: "Music", kind: "slider" },
        { key: "sfx", label: "Sound effects", kind: "slider" },
        { key: "blips", label: "Dialogue blips", kind: "slider" },
        { key: "reduced_flash", label: "Reduced flash", kind: "toggle" },
        { key: "shake", label: "Screen shake", kind: "toggle" },
        { key: "fullscreen", label: "Window mode", kind: "window" }
    ];
}

function settings_apply(_key, _value) {
    var _old = global.settings[$ _key];
    global.settings[$ _key] = _value;
    if (_key == "fullscreen") {
        window_set_fullscreen(_value);
        gui_update_transform(true);
    }
    if (_old != _value) {
        settings_save();
        if (_key == "sfx") ui_snd("snd_ui_move");
    }
}

function settings_step() {
    var _su = global.set_ui;
    var _rows = settings_rows();
    var _n = array_length(_rows);   // index _n = Back button
    if (inp_pressed("pause") || (inp_pressed("rmb") && _su.drag < 0)) {
        inp_consume("pause");
        inp_consume("rmb");
        settings_close();
        return;
    }
    // slider drag captures the pointer until release
    if (_su.drag >= 0) {
        if (!global.inp.down[$ "lmb"]) _su.drag = -1;
        else {
            var _v = clamp((global.inp.mx - 536) / 352, 0, 1);
            settings_apply(_rows[_su.drag].key, round(_v * 100) / 100);
        }
        return;
    }
    for (var i = 0; i <= _n; i++) {
        var _hit = (i < _n) ? ui_hit(232, 188 + 64 * i, 816, 48) : ui_hit(888, 608, 160, 40);
        if (_hit && global.inp.mouse_moved && _su.focus != i) {
            _su.focus = i;
            ui_snd("snd_ui_move");
        }
    }
    if (inp_pressed("lmb")) {
        inp_consume("lmb");
        if (ui_hit(888, 608, 160, 40)) {
            settings_close();
            return;
        }
        for (var j = 0; j < _n; j++) {
            if (!ui_hit(232, 188 + 64 * j, 816, 48)) continue;
            _su.focus = j;
            var _row = _rows[j];
            if (_row.kind == "slider") {
                if (global.inp.mx >= 524 && global.inp.mx < 900) _su.drag = j;
            } else if (ui_hit(536, 188 + 64 * j, 352, 48)) {
                settings_apply(_row.key, !global.settings[$ _row.key]);
                ui_snd("snd_ui_confirm");
            }
        }
    }
    if (inp_repeat("nav_down") || (inp_pressed("tab") && !inp_down("shift"))) {
        inp_consume("tab");
        _su.focus = min(_n, _su.focus + 1);
        ui_snd("snd_ui_move");
    }
    if (inp_repeat("nav_up") || (inp_pressed("tab") && inp_down("shift"))) {
        inp_consume("tab");
        _su.focus = max(0, _su.focus - 1);
        ui_snd("snd_ui_move");
    }
    if (_su.focus < _n) {
        var _r = _rows[_su.focus];
        var _d = (inp_repeat("nav_right") ? 1 : 0) - (inp_repeat("nav_left") ? 1 : 0);
        if (_r.kind == "slider") {
            var _cur = global.settings[$ _r.key];
            if (_d != 0) settings_apply(_r.key, clamp(round((_cur + _d * (inp_down("shift") ? 0.01 : 0.05)) * 100) / 100, 0, 1));
            if (inp_pressed("home")) settings_apply(_r.key, 0);
            if (inp_pressed("end_key")) settings_apply(_r.key, 1);
        } else {
            if (_d != 0 || inp_pressed("confirm")) {
                inp_consume("confirm");
                settings_apply(_r.key, !global.settings[$ _r.key]);
                ui_snd("snd_ui_confirm");
            }
        }
    } else if (inp_pressed("confirm")) {
        inp_consume("confirm");
        settings_close();
    }
}

function settings_draw() {
    var _su = global.set_ui;
    ui_dim(0.6);
    ui_panel(208, 72, 864, 600);
    text_draw(232, 96, "Settings", "title", C_TEXT);
    var _rows = settings_rows();
    for (var i = 0; i < array_length(_rows); i++) {
        var _y = 188 + 64 * i;
        var _r = _rows[i];
        var _f = (_su.focus == i);
        if (_f || ui_hit(232, _y, 816, 48)) ui_round(232, _y, 816, 48, C_RAISED, 8);
        text_draw(248, _y + 9, _r.label, "body", C_TEXT);
        var _v = global.settings[$ _r.key];
        if (_r.kind == "slider") {
            ui_slider(536, _y + 14, 352, _v, _f, true);
            text_draw(1048, _y + 8, string(round(_v * 100)) + "%", "body", C_TEXT, fa_right);
        } else {
            var _lab;
            if (_r.kind == "window") _lab = _v ? "Fullscreen" : "Windowed";
            else _lab = _v ? "On" : "Off";
            ui_button(536, _y, 352, 48, "< " + _lab + " >", { enabled: true, focus: _f, hover: ui_hit(536, _y, 352, 48) });
        }
    }
    text_draw(232, 608, "Left/Right adjust   Shift fine   Esc Back", "meta", C_MUTED);
    ui_button(888, 608, 160, 40, "Back", { enabled: true, focus: _su.focus == array_length(_rows), hover: ui_hit(888, 608, 160, 40) });
}

// ================================================================== save / load
/// _mode "save" or "load"; _caller "pause", "checkpoint", "title", "gameover"; _cp checkpoint instance data.
function saveload_open(_mode, _caller, _cp) {
    var _sl = global.sl;
    _sl.mode = _mode;
    _sl.caller = _caller;
    _sl.cp = _cp;
    _sl.can_save = !is_undefined(_cp);
    _sl.status = (_mode == "save") ? scene_text("checkpoint_choose") : "";
    _sl.status_col = C_MUTED;
    _sl.busy = "";
    _sl.busy_t = 0;
    saveload_refresh();
    // default row: active slot, else first empty (save), else first usable
    _sl.sel = 0;
    if (_mode == "save") {
        if (global.active_slot >= 0) _sl.sel = global.active_slot;
        else {
            for (var i = 0; i < SAVE_SLOTS; i++) if (_sl.rows[i].state == "empty") { _sl.sel = i; break; }
        }
        _sl.focus_zone = "rows";
    } else {
        var _first = saveload_next_usable(-1, 1);
        if (_first < 0) {
            _sl.focus_zone = "back";
            _sl.status = "No saves available.";
        } else {
            _sl.sel = _first;
            _sl.focus_zone = "rows";
        }
    }
    ui_push(OV.SAVELOAD);
    inp_block_all();
}

function saveload_refresh() {
    var _sl = global.sl;
    _sl.rows = [];
    for (var i = 0; i < SAVE_SLOTS; i++) array_push(_sl.rows, save_read(i));
}

function saveload_row_usable(_i) {
    var _sl = global.sl;
    if (_sl.mode == "save") return true;
    return _sl.rows[_i].state == "ok";
}

function saveload_next_usable(_from, _dir) {
    var _i = _from + _dir;
    while (_i >= 0 && _i < SAVE_SLOTS) {
        if (saveload_row_usable(_i)) return _i;
        _i += _dir;
    }
    return -1;
}

function saveload_close() {
    ui_remove(OV.SAVELOAD);
    ui_snd("snd_ui_cancel");
    inp_block_all();
}

function saveload_primary_enabled() {
    var _sl = global.sl;
    if (_sl.busy != "") return false;
    if (_sl.mode == "save") return _sl.can_save;
    return saveload_row_usable(_sl.sel);
}

function saveload_commit() {
    var _sl = global.sl;
    if (!saveload_primary_enabled()) return;
    if (_sl.mode == "save") {
        if (_sl.rows[_sl.sel].state != "empty") {
            confirm_open("Overwrite slot " + string(_sl.sel + 1) + "?", scene_text("checkpoint_overwrite"),
                "Saved " + struct_or(_sl.rows[_sl.sel], "date", ""), "Cancel", "Overwrite", true,
                function() { saveload_begin_busy("save"); });
        } else saveload_begin_busy("save");
    } else {
        if (_sl.caller == "pause" || _sl.caller == "checkpoint") {
            confirm_open("Load slot " + string(_sl.sel + 1) + "?", "Unsaved progress will be lost.", "", "Cancel", "Load", true,
                function() { saveload_begin_busy("load"); });
        } else saveload_begin_busy("load");
    }
}

function saveload_begin_busy(_what) {
    var _sl = global.sl;
    _sl.busy = _what;
    _sl.busy_t = 0;
    _sl.status = (_what == "save") ? "Saving…" : "Loading…";
    _sl.status_col = C_MUTED;
}

/// Builds the checkpoint snapshot: full health, positioned at the star's respawn cell.
function saveload_do_save() {
    var _sl = global.sl;
    var _cp = _sl.cp;
    var _snap = snapshot_make();
    _snap.hp = player_max_hp();
    _snap.scene_room = room_get_name(room);
    _snap.pos_x = cell_px(_cp.respawn[0]);
    _snap.pos_y = cell_px(_cp.respawn[1]);
    _snap.facing = "down";
    _snap.checkpoint_id = _cp.id;
    _snap.location = _cp.location;
    var _res = save_write(_sl.sel, _snap);
    if (_res.ok) {
        global.run.hp = player_max_hp();
        global.run.checkpoint_id = _cp.id;
        global.run.location = _cp.location;
        global.checkpoint_snapshot = _snap;
        global.active_slot = _sl.sel;
        global.last_saved_playtime = global.run.playtime;
        _sl.status = _res.msg;
        _sl.status_col = C_SUCCESS;
        aud_play("snd_save", undefined, undefined, "", false);
        if (instance_exists(obj_player)) obj_player.flash_heal = 30;
    } else {
        _sl.status = _res.msg;
        _sl.status_col = C_ERROR;
        aud_play("snd_ui_error", undefined, undefined, "", false);
    }
    saveload_refresh();
}

function saveload_step() {
    var _sl = global.sl;
    if (_sl.busy != "") {
        _sl.busy_t += 1;
        if (_sl.busy_t >= 2) {
            var _what = _sl.busy;
            _sl.busy = "";
            if (_what == "save") saveload_do_save();
            else {
                var _res = game_load_slot(_sl.sel);
                if (!_res.ok) {
                    _sl.status = "Cannot load this save. " + _res.msg;
                    _sl.status_col = C_ERROR;
                    aud_play("snd_ui_error", undefined, undefined, "", false);
                    saveload_refresh();
                }
            }
        }
        return;
    }
    if (inp_pressed("pause") || inp_pressed("rmb")) {
        inp_consume("pause");
        inp_consume("rmb");
        saveload_close();
        return;
    }
    var _tabs = (_sl.caller == "pause" || _sl.caller == "checkpoint");
    // mouse
    var _hover_row = -1;
    for (var i = 0; i < SAVE_SLOTS; i++) if (ui_hit(260, 192 + 128 * i, 760, 120)) _hover_row = i;
    if (_hover_row >= 0 && global.inp.mouse_moved && saveload_row_usable(_hover_row)) {
        if (_sl.sel != _hover_row || _sl.focus_zone != "rows") ui_snd("snd_ui_move");
        _sl.sel = _hover_row;
        _sl.focus_zone = "rows";
    }
    if (inp_pressed("lmb")) {
        inp_consume("lmb");
        if (_hover_row >= 0 && saveload_row_usable(_hover_row)) {
            _sl.sel = _hover_row;
            _sl.focus_zone = "rows";
        } else if (ui_hit(232, 608, 160, 40)) {
            saveload_close();
            return;
        } else if (ui_hit(888, 608, 160, 40)) {
            saveload_commit();
        } else if (_tabs && ui_hit(752, 112, 132, 36)) {
            saveload_switch_mode("save");
        } else if (_tabs && ui_hit(896, 112, 132, 36)) {
            saveload_switch_mode("load");
        }
    }
    // keyboard
    if (_sl.focus_zone == "rows") {
        if (inp_repeat("nav_down")) {
            var _n = saveload_next_usable(_sl.sel, 1);
            if (_n >= 0) { _sl.sel = _n; ui_snd("snd_ui_move"); }
        }
        if (inp_repeat("nav_up")) {
            var _u = saveload_next_usable(_sl.sel, -1);
            if (_u >= 0) { _sl.sel = _u; ui_snd("snd_ui_move"); }
        }
    } else if (_sl.focus_zone == "tabs") {
        if (inp_pressed("nav_left")) saveload_switch_mode("save");
        if (inp_pressed("nav_right")) saveload_switch_mode("load");
    }
    if (inp_pressed("tab")) {
        inp_consume("tab");
        var _zones = _tabs ? ["tabs", "rows", "back", "primary"] : ["rows", "back", "primary"];
        var _zi = array_get_index(_zones, _sl.focus_zone);
        _zi = (_zi + (inp_down("shift") ? -1 : 1) + array_length(_zones)) mod array_length(_zones);
        _sl.focus_zone = _zones[_zi];
        if (_sl.focus_zone == "rows" && !saveload_row_usable(_sl.sel)) {
            var _fu = saveload_next_usable(-1, 1);
            if (_fu < 0) _sl.focus_zone = "back"; else _sl.sel = _fu;
        }
        ui_snd("snd_ui_move");
    }
    if (inp_pressed("confirm")) {
        inp_consume("confirm");
        switch (_sl.focus_zone) {
            case "rows": _sl.focus_zone = "primary"; ui_snd("snd_ui_move"); break;   // Enter on a row selects it
            case "back": saveload_close(); return;
            case "primary": saveload_commit(); break;
            case "tabs": break;
        }
    }
}

function saveload_switch_mode(_mode) {
    var _sl = global.sl;
    if (_mode == "save" && !_sl.can_save) {
        _sl.status = "Save at a checkpoint.";
        _sl.status_col = C_MUTED;
        return;
    }
    if (_sl.mode == _mode) return;
    _sl.mode = _mode;
    ui_snd("snd_ui_move");
    if (_mode == "load" && !saveload_row_usable(_sl.sel)) {
        var _u = saveload_next_usable(-1, 1);
        if (_u >= 0) _sl.sel = _u;
    }
    _sl.status = "";
}

function saveload_draw() {
    var _sl = global.sl;
    ui_dim(0.6);
    ui_panel(208, 72, 864, 600);
    text_draw(232, 96, (_sl.mode == "save") ? "Save Game" : "Load Game", "title", C_TEXT);
    var _tabs = (_sl.caller == "pause" || _sl.caller == "checkpoint");
    if (_tabs) {
        ui_button(752, 112, 132, 36, "Save", { enabled: _sl.can_save, selected: _sl.mode == "save",
            hover: ui_hit(752, 112, 132, 36), focus: _sl.focus_zone == "tabs" && _sl.mode == "save" });
        ui_button(896, 112, 132, 36, "Load", { enabled: true, selected: _sl.mode == "load",
            hover: ui_hit(896, 112, 132, 36), focus: _sl.focus_zone == "tabs" && _sl.mode == "load" });
    }
    for (var i = 0; i < SAVE_SLOTS; i++) {
        var _y = 192 + 128 * i;
        var _row = _sl.rows[i];
        var _usable = saveload_row_usable(i);
        var _hov = ui_hit(260, _y, 760, 120) && _usable;
        var _frame = _hov ? 1 : 0;
        var _spr = (_row.state == "ok") ? spr_ui_save_card : spr_ui_save_card_empty;
        draw_sprite_ext(_spr, _frame, 260, _y, 1, 1, 0, c_white, _usable ? 1 : 0.7);
        text_draw(284, _y + 18, string(i + 1), "heading", _usable ? C_TEXT : C_DISABLED);
        var _status2 = "";
        if (_row.state == "ok") {
            text_draw(332, _y + 16, text_fit(_row.location, "body", 664), "body", C_TEXT);
            text_draw(332, _y + 56, "Level " + string(_row.level) + "   " + fmt_playtime(_row.playtime) + "   " + _row.date, "meta", C_MUTED);
        } else if (_row.state == "empty") {
            text_draw(332, _y + 16, "Empty slot", "body", C_MUTED);
            text_draw(332, _y + 56, "No saved journey", "meta", C_DISABLED);
            _status2 = "Empty";
        } else {
            text_draw(332, _y + 16, "Cannot load this save", "body", C_ERROR);
            text_draw(332, _y + 56, text_fit(_row.reason, "meta", 664), "meta", C_MUTED);
            _status2 = "Cannot load";
        }
        if (_sl.sel == i && _usable) _status2 = "Selected";
        text_draw(332, _y + 88, _status2, "meta", (_status2 == "Selected") ? C_GOLD : C_MUTED);
        if (_sl.sel == i && _usable) ui_selected(260, _y, 760, 120);
        if (_sl.focus_zone == "rows" && _sl.sel == i && _usable) ui_focus(260, _y, 760, 120);
    }
    var _foot = _sl.status;
    var _fcol = _sl.status_col;
    if (_foot == "" && _sl.rows[_sl.sel].state == "ok") {
        _foot = _sl.rows[_sl.sel].location;
        _fcol = C_MUTED;
    }
    text_draw(232, 584, text_fit(_foot, "meta", 632), "meta", _fcol);
    var _busy = (_sl.busy != "");
    ui_button(232, 608, 160, 40, "Back", { enabled: !_busy, hover: ui_hit(232, 608, 160, 40), focus: _sl.focus_zone == "back" });
    ui_button(888, 608, 160, 40, (_sl.mode == "save") ? "Save" : "Load", {
        enabled: saveload_primary_enabled(), hover: ui_hit(888, 608, 160, 40), focus: _sl.focus_zone == "primary" });
}

// ================================================================== confirmation
function confirm_open(_title, _msg, _sub, _cancel, _ok, _danger, _on_ok) {
    global.cf = { title: _title, msg: _msg, sub: _sub, cancel: _cancel, ok: _ok, danger: _danger,
                  on_ok: _on_ok, focus: 0 };
    ui_push(OV.CONFIRM);
    inp_block_all();   // the initiating Enter cannot confirm
}

function confirm_close() {
    ui_remove(OV.CONFIRM);
    global.cf = undefined;
    inp_block_all();
}

function confirm_step() {
    var _c = global.cf;
    if (!is_struct(_c)) {
        ui_remove(OV.CONFIRM);
        return;
    }
    if (inp_pressed("pause") || inp_pressed("rmb")) {
        inp_consume("pause");
        inp_consume("rmb");
        ui_snd("snd_ui_cancel");
        confirm_close();
        return;
    }
    if (ui_hit(408, 432, 216, 48) && global.inp.mouse_moved) _c.focus = 0;
    if (ui_hit(648, 432, 224, 48) && global.inp.mouse_moved) _c.focus = 1;
    if (inp_pressed("nav_left") || inp_pressed("nav_right") || inp_pressed("tab")) {
        inp_consume("tab");
        _c.focus = 1 - _c.focus;
        ui_snd("snd_ui_move");
    }
    var _act = -1;
    if (inp_pressed("lmb")) {
        inp_consume("lmb");
        if (ui_hit(408, 432, 216, 48)) _act = 0;
        else if (ui_hit(648, 432, 224, 48)) _act = 1;
    }
    if (inp_pressed("confirm")) {
        inp_consume("confirm");
        _act = _c.focus;
    }
    if (_act == 0) {
        ui_snd("snd_ui_cancel");
        confirm_close();
    } else if (_act == 1) {
        var _cb = _c.on_ok;
        confirm_close();
        if (is_method(_cb)) _cb();
    }
}

function confirm_draw() {
    var _c = global.cf;
    if (!is_struct(_c)) return;
    ui_dim(0.6);
    ui_panel(384, 216, 512, 288);
    text_draw(408, 240, text_fit(_c.title, "heading", 464), "heading", C_TEXT);
    text_draw_wrapped(408, 288, _c.msg, "body", 464, 2, C_TEXT);
    if (_c.sub != "") text_draw(408, 376, _c.sub, "meta", C_MUTED);
    ui_button(408, 432, 216, 48, _c.cancel, { enabled: true, focus: _c.focus == 0, hover: ui_hit(408, 432, 216, 48) });
    ui_button(648, 432, 224, 48, _c.ok, { enabled: true, focus: _c.focus == 1, hover: ui_hit(648, 432, 224, 48), danger: _c.danger });
}
