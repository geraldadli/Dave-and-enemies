// scr_ui_screens - HUD, inventory, title, Game Over, ending and the Draw GUI dispatcher.
// Rectangles follow docs/ui/UI_SPEC.md / UI_LAYOUTS.json exactly (logical 1280x720 pixels).

function ui_screens_init() {
    global.inv_ui = { zone: "main", focus: 0, sel: 0, carry: -1, status: "", status_col: C_TEXT,
                      scroll: 0, btn: 0, summ: 0, last_focus: 0, hover: -1, opened_once: false };
    global.pause_ui = { focus: 0, from_dialogue: false };
    global.set_ui = { focus: 0, drag: -1, caller: "pause" };
    global.sl = { mode: "load", caller: "title", focus_zone: "rows", sel: 0, rows: [], status: "",
                  status_col: C_MUTED, busy: "", busy_t: 0, can_save: false, btn: 1, tab: 1, cp: undefined };
    global.cf = undefined;
    global.go = { t: 0, focus: 0, ready: false };
    global.title_ui = { focus: 0 };
    global.ending = { t: 0, enable_at: 0, fade: 0 };
}

function ui_snd(_id) {
    aud_play(_id, undefined, undefined, "", false);
}

// ================================================================== HUD
function hotbar_slot_x(_i) { return 324 + 80 * _i; }

function hud_step() {
    var _r = global.run;
    var _hover = -1;
    if (hotbar_visible()) {
        for (var i = 0; i < HOTBAR; i++) {
            if (ui_hit(hotbar_slot_x(i), 624, 72, 72)) _hover = i;
        }
        if (_hover >= 0) {
            if (inp_pressed("lmb")) {
                inp_consume("lmb");
                if (_r.hot_sel != _hover) ui_snd("snd_ui_move");
                _r.hot_sel = _hover;
            } else if (inp_pressed("rmb")) {
                inp_consume("rmb");
                inventory_open(_hover);
                return;
            }
        }
        var _wh = inp_wheel();
        if (_wh != 0) {
            inp_use_wheel();
            _r.hot_sel = (_r.hot_sel + _wh + HOTBAR) mod HOTBAR;
            ui_snd("snd_ui_move");
        }
        var _k = inp_slot_pressed();
        if (_k >= 0) {
            inp_consume("s" + string(_k + 1));
            if (_r.hot_sel != _k) ui_snd("snd_ui_move");
            _r.hot_sel = _k;
        }
        if (inp_pressed("use")) {
            inp_consume("use");
            var _e = inv_get(_r.hot_sel);
            if (!is_struct(_e)) {
                toast_show("Select a potion to use.");
            } else if (item_type(_e.id) != "consumable") {
                toast_show(item_name(_e.id) + " cannot be used.");
            } else {
                var _res = inv_use(_r.hot_sel);
                if (!_res.ok) toast_show(_res.msg);
            }
        }
    }
    global.hot_hover = _hover;
    global.hot_hover_t = (_hover >= 0) ? global.hot_hover_t + 1 : 0;
    if (inp_pressed("inventory")) {
        inp_consume("inventory");
        inventory_open(-1);
        return;
    }
    if (inp_pressed("pause")) {
        inp_consume("pause");
        pause_open(false);
    }
}

function hud_draw_hp() {
    var _r = global.run;
    var _max = player_max_hp();
    var _ratio = _r.hp / max(1, _max);
    ui_round(24, 24, 320, 56, C_INK, 10, false, 0.92);
    text_draw(32, 24, "HP", "meta", C_MUTED);
    var _low = _ratio <= 0.25;
    text_draw(336, 24, string(_r.hp) + " / " + string(_max), "meta", _low ? C_ERROR : C_TEXT, fa_right);
    ui_bar(24, 48, 320, _ratio, C_HEALTH, true, global.hp_ghost / max(1, _max));
    if (_low) ui_rect(32, 56, 4, 16, C_TEXT, 0.8);
}

function hud_draw_boss() {
    var _b = global.boss_ui;
    text_draw(640, 24, scene_text("ui_boss_name"), "body", C_TEXT, fa_center);
    var _ghost = (_b.ghost_t > 0) ? _b.ghost / max(1, _b.hp_max) : -1;
    ui_bar(384, 56, 512, _b.hp / max(1, _b.hp_max), C_BOSS, false, _ghost);
    if (_b.ghost_t > 0) _b.ghost_t -= 1;
    else _b.ghost = _b.hp;
}

function hud_draw_hotbar(_inventory_mode) {
    var _r = global.run;
    for (var i = 0; i < HOTBAR; i++) {
        var _st = { equipped: inv_is_equipped(i) };
        if (_inventory_mode) {
            var _iu = global.inv_ui;
            _st.selected = (_iu.sel == i);
            _st.focus = (_iu.zone == "main" && _iu.focus == i);
            _st.source = (_iu.carry == i);
            _st.hover = (_iu.hover == i);
        } else {
            _st.selected = (_r.hot_sel == i);
            _st.hover = (global.hot_hover == i);
        }
        ui_slot(hotbar_slot_x(i), 624, inv_get(i), string(i + 1), _st);
        if (!_inventory_mode && _r.hot_sel == i) {
            // active slot: gold border with corner ticks plus bottom marker
            ui_focus(hotbar_slot_x(i), 624, 72, 72);
        }
    }
    if (!_inventory_mode && global.hot_hover >= 0 && global.hot_hover_t > 30) {
        var _hx = hotbar_slot_x(global.hot_hover) + 36;
        var _tw = text_w("Right-click: inventory", "meta") + 16;
        ui_round(_hx - _tw / 2, 588, _tw, 28, C_INK, 6, false, 0.95);
        text_draw(_hx, 590, "Right-click: inventory", "meta", C_MUTED, fa_center);
    }
}

function hud_draw_toasts() {
    var _t = global.toast;
    if (_t.goal_t > 0 && _t.goal_text != "") {
        var _a = min(1, _t.goal_t / 20, (_t.goal_dur - _t.goal_t + 1) / 12);
        ui_round(384, 96, 512, 44, C_INK, 8, false, 0.92 * _a);
        text_draw(640, 103, text_fit(_t.goal_text, "body", 488), "body", C_GOLD, fa_center, _a);
    }
    if (_t.prompt != "" && world_active()) {
        ui_round(384, 520, 512, 40, C_INK, 8, false, 0.92);
        text_draw(640, 528, _t.prompt, "meta", C_TEXT, fa_center);
    }
    if (_t.msg_t > 0 && _t.msg_text != "") {
        var _a2 = min(1, _t.msg_t / 12);
        ui_round(384, 568, 512, 40, C_INK, 8, false, 0.95 * _a2);
        text_draw(640, 576, text_fit(_t.msg_text, "meta", 496), "meta", _t.msg_col, fa_center, _a2);
    }
}

// ================================================================== inventory
function inventory_open(_slot) {
    if (ui_has(OV.DIALOGUE) || ui_has(OV.INVENTORY)) return;
    var _iu = global.inv_ui;
    _iu.carry = -1;
    _iu.status = "";
    _iu.scroll = 0;
    if (_slot >= 0) _iu.focus = _slot;
    else if (!_iu.opened_once) _iu.focus = 0;
    else _iu.focus = _iu.last_focus;
    _iu.zone = (_iu.focus < HOTBAR) ? "main" : "storage";
    _iu.sel = _iu.focus;
    _iu.opened_once = true;
    ui_push(OV.INVENTORY);
    ui_snd("snd_inventory_open");
    inp_block_all();
}

/// Closing always cancels a carried stack back to its source (no loss, no duplication).
function ui_close_inventory(_silent) {
    var _iu = global.inv_ui;
    _iu.carry = -1;
    _iu.last_focus = _iu.focus;
    ui_remove(OV.INVENTORY);
    if (!_silent) ui_snd("snd_inventory_close");
    inp_block_all();
}

function inv_slot_rect(_i) {
    if (_i < HOTBAR) return [hotbar_slot_x(_i), 624];
    var _k = _i - HOTBAR;
    return [80 + 80 * (_k mod 8), 152 + 80 * (_k div 8)];
}

function inv_set_status(_text, _col) {
    global.inv_ui.status = _text;
    global.inv_ui.status_col = _col;
}

function inventory_primary(_i) {
    var _st = inv_primary_state(_i);
    var _e = inv_get(_i);
    if (!_st.ok) {
        inv_set_status(_st.reason, C_MUTED);
        if (is_struct(_e)) ui_snd("snd_ui_error");
        return;
    }
    switch (item_type(_e.id)) {
        case "consumable":
            var _res = inv_use(_i);
            inv_set_status(_res.msg, _res.ok ? C_SUCCESS : C_ERROR);
            break;
        case "weapon":
        case "armor":
            var _name = item_name(_e.id);
            if (inv_equip(_i)) {
                ui_snd("snd_ui_confirm");
                inv_set_status("Equipped " + _name + ".", C_SUCCESS);
            }
            break;
    }
}

function inventory_place(_dst) {
    var _iu = global.inv_ui;
    var _src = _iu.carry;
    var _res = inv_move(_src, _dst);
    _iu.carry = -1;
    switch (_res) {
        case "cancel": inv_set_status("Move cancelled.", C_MUTED); ui_snd("snd_ui_cancel"); break;
        case "moved": inv_set_status("Moved.", C_TEXT); ui_snd("snd_ui_confirm"); break;
        case "merged": inv_set_status("Stacks merged.", C_TEXT); ui_snd("snd_ui_confirm"); break;
        case "partial": inv_set_status("Stack is full; the rest stays in the original slot.", C_TEXT); ui_snd("snd_ui_confirm"); break;
        case "swapped": inv_set_status("Swapped.", C_TEXT); ui_snd("snd_ui_confirm"); break;
    }
    _iu.sel = _dst;
    _iu.focus = _dst;
}

function inventory_step() {
    var _iu = global.inv_ui;
    // close / cancel
    if (inp_pressed("pause")) {
        inp_consume("pause");
        if (_iu.carry >= 0) {
            _iu.carry = -1;
            inv_set_status("Move cancelled.", C_MUTED);
            ui_snd("snd_ui_cancel");
        } else ui_close_inventory(false);
        return;
    }
    if (inp_pressed("inventory")) {
        inp_consume("inventory");
        ui_close_inventory(false);
        return;
    }
    if (inp_pressed("rmb")) {
        inp_consume("rmb");
        if (_iu.carry >= 0) {
            _iu.carry = -1;
            inv_set_status("Move cancelled.", C_MUTED);
            ui_snd("snd_ui_cancel");
        } else ui_close_inventory(false);
        return;
    }
    // mouse
    _iu.hover = -1;
    for (var i = 0; i < INV_SIZE; i++) {
        var _p = inv_slot_rect(i);
        if (ui_hit(_p[0], _p[1], 72, 72)) _iu.hover = i;
    }
    if (inp_pressed("lmb")) {
        inp_consume("lmb");
        if (ui_hit(1160, 56, 40, 40)) {
            ui_close_inventory(false);
            return;
        }
        if (_iu.hover >= 0) {
            if (_iu.carry >= 0) inventory_place(_iu.hover);
            else {
                if (_iu.sel != _iu.hover) ui_snd("snd_ui_move");
                _iu.sel = _iu.hover;
                _iu.focus = _iu.hover;
                _iu.zone = (_iu.hover < HOTBAR) ? "main" : "storage";
                _iu.scroll = 0;
            }
        } else if (ui_hit(776, 528, 192, 40)) {
            _iu.zone = "buttons";
            _iu.btn = 0;
            inventory_primary(_iu.sel);
        } else if (ui_hit(984, 528, 192, 40)) {
            _iu.zone = "buttons";
            _iu.btn = 1;
            inventory_move_toggle();
        } else if (ui_hit(752, 160, 216, 96)) {
            _iu.zone = "summary";
            _iu.summ = 0;
        } else if (ui_hit(984, 160, 216, 96)) {
            _iu.zone = "summary";
            _iu.summ = 1;
        }
    }
    if (ui_hit(776, 400, 400, 114)) {
        var _wh = inp_wheel();
        if (_wh != 0) {
            inp_use_wheel();
            _iu.scroll = max(0, _iu.scroll + _wh);
        }
    }
    // number keys focus main slots without activating
    var _k = inp_slot_pressed();
    if (_k >= 0) {
        inp_consume("s" + string(_k + 1));
        _iu.zone = "main";
        _iu.focus = _k;
        if (_iu.carry < 0) _iu.sel = _k;
        ui_snd("snd_ui_move");
    }
    // zone cycling
    if (inp_pressed("f6")) {
        inp_consume("f6");
        var _zones = ["storage", "main", "summary", "desc", "buttons", "close"];
        var _zi = array_get_index(_zones, _iu.zone);
        _zi = (_zi + (inp_down("shift") ? -1 : 1) + 6) mod 6;
        _iu.zone = _zones[_zi];
        if (_iu.zone == "storage" && _iu.focus < HOTBAR) _iu.focus = HOTBAR + _iu.focus;
        if (_iu.zone == "main" && _iu.focus >= HOTBAR) _iu.focus = (_iu.focus - HOTBAR) mod 8;
        ui_snd("snd_ui_move");
    }
    // arrows
    var _dx = (inp_repeat("nav_right") ? 1 : 0) - (inp_repeat("nav_left") ? 1 : 0);
    var _dy = (inp_repeat("nav_down") ? 1 : 0) - (inp_repeat("nav_up") ? 1 : 0);
    if (_dx != 0 || _dy != 0) {
        var _old = _iu.focus;
        if (_iu.zone == "storage") {
            var _c = (_iu.focus - HOTBAR) mod 8;
            var _r = (_iu.focus - HOTBAR) div 8;
            _c = clamp(_c + _dx, 0, 7);
            if (_dy > 0 && _r == 3) {
                _iu.zone = "main";
                _iu.focus = _c;
            } else {
                _r = clamp(_r + _dy, 0, 3);
                _iu.focus = HOTBAR + _r * 8 + _c;
            }
        } else if (_iu.zone == "main") {
            if (_dy < 0) {
                _iu.zone = "storage";
                _iu.focus = HOTBAR + 3 * 8 + _iu.focus;
            } else _iu.focus = clamp(_iu.focus + _dx, 0, 7);
        } else if (_iu.zone == "summary") {
            _iu.summ = clamp(_iu.summ + _dx, 0, 1);
        } else if (_iu.zone == "buttons") {
            _iu.btn = clamp(_iu.btn + _dx, 0, 1);
        } else if (_iu.zone == "desc") {
            _iu.scroll = max(0, _iu.scroll + _dy);
        }
        if ((_iu.zone == "storage" || _iu.zone == "main") && _iu.carry < 0) _iu.sel = _iu.focus;
        if (_old != _iu.focus) {
            _iu.scroll = 0;
            ui_snd("snd_ui_move");
        }
    }
    if (_iu.zone == "desc") {
        if (inp_repeat("pgdn")) _iu.scroll += 3;
        if (inp_repeat("pgup")) _iu.scroll = max(0, _iu.scroll - 3);
    }
    // move
    if (inp_pressed("move")) {
        inp_consume("move");
        inventory_move_toggle();
    }
    // activation
    if (inp_pressed("confirm")) {
        inp_consume("confirm");
        switch (_iu.zone) {
            case "storage":
            case "main":
                if (_iu.carry >= 0) inventory_place(_iu.focus);
                else inventory_primary(_iu.sel);
                break;
            case "summary":
                var _ref = (_iu.summ == 0) ? global.run.eq_weapon : global.run.eq_armor;
                if (_ref >= 0) {
                    _iu.sel = _ref;
                    _iu.focus = _ref;
                    _iu.zone = (_ref < HOTBAR) ? "main" : "storage";
                }
                break;
            case "buttons":
                if (_iu.btn == 0) inventory_primary(_iu.sel);
                else inventory_move_toggle();
                break;
            case "close":
                ui_close_inventory(false);
                return;
        }
    }
}

function inventory_move_toggle() {
    var _iu = global.inv_ui;
    if (_iu.carry >= 0) {
        inventory_place((_iu.zone == "storage" || _iu.zone == "main") ? _iu.focus : _iu.sel);
        return;
    }
    if (!is_struct(inv_get(_iu.sel))) {
        inv_set_status("Empty slot. Select an item to move.", C_MUTED);
        return;
    }
    _iu.carry = _iu.sel;
    inv_set_status("Moving " + item_name(inv_get(_iu.sel).id) + ". Choose a slot, Esc cancels.", C_TEXT);
    ui_snd("snd_ui_confirm");
}

function inventory_draw() {
    var _iu = global.inv_ui;
    var _r = global.run;
    ui_dim(0.45);
    ui_panel(56, 40, 1168, 560);
    text_draw(80, 64, "Inventory", "heading", C_TEXT);
    // close
    var _ch = ui_hit(1160, 56, 40, 40);
    ui_round(1160, 56, 40, 40, _ch ? C_RAISED : C_INK, 6);
    ui_outline(1160, 56, 40, 40, C_EDGE, 1);
    text_draw(1180, 63, "X", "meta", C_TEXT, fa_center);
    if (_iu.zone == "close") ui_focus(1160, 56, 40, 40);
    // storage
    var _full = inv_all_occupied();
    text_draw(80, 116, "Storage", "body", C_TEXT);
    var _cap = string(inv_storage_count()) + " / 32" + (_full ? "  Full" : "");
    text_draw(712, 116, _cap, "meta", _full ? C_ERROR : C_MUTED, fa_right);
    for (var i = HOTBAR; i < INV_SIZE; i++) {
        var _p = inv_slot_rect(i);
        ui_slot(_p[0], _p[1], inv_get(i), "", {
            selected: _iu.sel == i, focus: _iu.zone == "storage" && _iu.focus == i,
            equipped: inv_is_equipped(i), source: _iu.carry == i, hover: _iu.hover == i });
    }
    // character
    text_draw(752, 64, "Dave / Level " + string(_r.level), "body", C_TEXT);
    ui_rect(752, 104, 376, 16, C_WELL);
    if (_r.level >= MAX_LEVEL) {
        ui_rect(752, 104, 376, 16, C_XP);
        text_draw(752, 128, "Maximum level", "meta", C_MUTED);
    } else {
        var _need = xp_to_next(_r.level);
        ui_rect(752, 104, round(376 * clamp(_r.xp / _need, 0, 1)), 16, C_XP);
        text_draw(752, 128, "XP " + string(_r.xp) + " / " + string(_need), "meta", C_MUTED);
    }
    inventory_draw_summary(752, "Weapon", _r.eq_weapon, "Damage " + string(player_attack()), _iu.zone == "summary" && _iu.summ == 0);
    inventory_draw_summary(984, "Armor", _r.eq_armor, "Defense " + string(player_defense()), _iu.zone == "summary" && _iu.summ == 1);
    // detail
    ui_round(752, 280, 448, 296, C_WELL, 10);
    var _e = inv_get(_iu.sel);
    if (is_struct(_e)) {
        text_draw_wrapped(776, 304, item_name(_e.id), "body", 400, 2, C_TEXT);
        text_draw(776, 368, text_fit(inv_type_line(_iu.sel), "meta", 400), "meta", C_MUTED);
        var _def = item_def(_e.id);
        var _desc = is_struct(_def) ? _def.desc : "";
        var _st0 = inv_primary_state(_iu.sel);
        if (!_st0.ok && item_type(_e.id) == "consumable") _desc = _st0.reason + " " + _desc;
        var _lines = text_wrap(_desc, "body", 400);
        var _maxs = max(0, array_length(_lines) - 3);
        _iu.scroll = min(_iu.scroll, _maxs);
        ui_clip_begin(776, 400, 400, 114);
        for (var l = 0; l < array_length(_lines); l++) {
            text_draw(776, 400 + (l - _iu.scroll) * 30, _lines[l], "body", C_TEXT);
        }
        ui_clip_end();
        if (_maxs > 0) {
            var _bh = 114 * 3 / array_length(_lines);
            ui_rect(1180, 400 + (114 - _bh) * (_iu.scroll / _maxs), 4, _bh, C_MUTED);
        }
        if (_iu.zone == "desc") ui_focus(772, 396, 408, 122);
    } else {
        text_draw(776, 304, "Empty slot", "body", C_MUTED);
        text_draw(776, 400, "Move an item here.", "body", C_MUTED);
    }
    var _pst = inv_primary_state(_iu.sel);
    ui_button(776, 528, 192, 40, inv_primary_label(_iu.sel), {
        enabled: _pst.ok, hover: ui_hit(776, 528, 192, 40), focus: _iu.zone == "buttons" && _iu.btn == 0 });
    var _can_move = is_struct(_e) || _iu.carry >= 0;
    ui_button(984, 528, 192, 40, (_iu.carry >= 0) ? "Place" : "Move", {
        enabled: _can_move, hover: ui_hit(984, 528, 192, 40), focus: _iu.zone == "buttons" && _iu.btn == 1 });
    // status + hints
    if (_iu.status != "") text_draw_wrapped(80, 492, _iu.status, "body", 632, 2, _iu.status_col);
    text_draw(80, 556, "Enter Action   M Move   F6 Area   I / Tab Close", "meta", C_MUTED);
    // main row in inventory mode, unchanged coordinates
    hud_draw_hotbar(true);
    // carried ghost
    if (_iu.carry >= 0) {
        var _ce = inv_get(_iu.carry);
        if (is_struct(_ce)) {
            var _gx, _gy;
            if (_iu.hover >= 0) {
                var _hp = inv_slot_rect(_iu.hover);
                _gx = global.inp.mx - 24;
                _gy = global.inp.my - 24;
                ui_focus(_hp[0], _hp[1], 72, 72);
            } else {
                var _fp = inv_slot_rect(_iu.focus);
                _gx = _fp[0] + 12;
                _gy = _fp[1] - 30;
            }
            var _ic = item_icon(_ce.id);
            draw_set_alpha(0.8);
            if (_ic >= 0) draw_sprite_stretched_ext(_ic, 0, _gx, _gy, 48, 48, c_white, 0.8);
            else ui_round(_gx, _gy, 48, 48, C_RAISED, 8);
            draw_set_alpha(1);
            if (_ce.n > 1) text_draw(_gx + 50, _gy + 26, "×" + string(_ce.n), "meta", C_TEXT, fa_right);
        }
    }
}

function inventory_draw_summary(_x, _label, _ref, _stat, _focus) {
    ui_round(_x, 160, 216, 96, C_WELL, 10);
    text_draw(_x + 12, 164, _label, "meta", C_MUTED);
    var _e = inv_get(_ref);
    if (is_struct(_e)) {
        var _ic = item_icon(_e.id);
        if (_ic >= 0) draw_sprite_stretched(_ic, 0, _x + 12, 192, 48, 48);
        else ui_round(_x + 12, 192, 48, 48, C_RAISED, 8);
        text_draw(_x + 68, 192, text_fit(item_name(_e.id), "meta", 140), "meta", C_TEXT);
        text_draw(_x + 68, 218, _stat, "meta", C_MUTED);
    } else {
        text_draw(_x + 12, 200, "None equipped", "meta", C_DISABLED);
    }
    if (_focus) ui_focus(_x, 160, 216, 96);
}

// ================================================================== title
function title_open() {
    global.title_ui.focus = 0;
    global.mode = MODE.TITLE;
    mus_stop(800);
    inp_block_all();
}

function title_items() {
    var _has = save_any_valid();
    return [
        { label: "New Game", enabled: true, reason: "" },
        { label: "Load Game", enabled: _has, reason: "No saves available." },
        { label: "Settings", enabled: true, reason: "" },
        { label: "Quit Game", enabled: true, reason: "" }
    ];
}

function title_step() {
    var _t = global.title_ui;
    var _items = title_items();
    var _act = vmenu_input(_items, _t, 464, 380, 352, 48, 64);
    if (_act < 0) return;
    switch (_act) {
        case 0: ui_snd("snd_ui_confirm"); game_new(); break;
        case 1: ui_snd("snd_ui_confirm"); saveload_open("load", "title", undefined); break;
        case 2: ui_snd("snd_ui_confirm"); settings_open("title"); break;
        case 3: game_end(); break;
    }
}

function title_draw() {
    if (sprite_exists(spr_menu_background)) draw_sprite_stretched(spr_menu_background, 0, 0, 0, GUI_W, GUI_H);
    ui_dim(0.55);
    text_draw(640, 150, "Dave's & Enemies", "title", C_TEXT, fa_center);
    text_draw(640, 214, "Chapter I", "body", C_GOLD, fa_center);
    var _items = title_items();
    vmenu_draw(_items, global.title_ui, 464, 380, 352, 48, 64);
    var _f = _items[global.title_ui.focus];
    if (!_f.enabled) text_draw(640, 650, _f.reason, "meta", C_MUTED, fa_center);
}

/// Shared vertical menu input. _ui needs a .focus field. Returns the activated index or -1.
function vmenu_input(_items, _ui, _x, _y, _w, _h, _step) {
    var _n = array_length(_items);
    for (var i = 0; i < _n; i++) {
        if (ui_hit(_x, _y + _step * i, _w, _h) && global.inp.mouse_moved) {
            if (_ui.focus != i) ui_snd("snd_ui_move");
            _ui.focus = i;
        }
    }
    if (inp_repeat("nav_down") || (inp_pressed("tab") && !inp_down("shift"))) {
        _ui.focus = min(_n - 1, _ui.focus + 1);
        ui_snd("snd_ui_move");
        inp_consume("tab");
    }
    if (inp_repeat("nav_up") || (inp_pressed("tab") && inp_down("shift"))) {
        _ui.focus = max(0, _ui.focus - 1);
        ui_snd("snd_ui_move");
        inp_consume("tab");
    }
    if (inp_pressed("lmb")) {
        for (var j = 0; j < _n; j++) {
            if (ui_hit(_x, _y + _step * j, _w, _h)) {
                inp_consume("lmb");
                _ui.focus = j;
                if (_items[j].enabled) return j;
            }
        }
    }
    if (inp_pressed("confirm")) {
        inp_consume("confirm");
        if (_items[_ui.focus].enabled) return _ui.focus;
    }
    return -1;
}

function vmenu_draw(_items, _ui, _x, _y, _w, _h, _step) {
    for (var i = 0; i < array_length(_items); i++) {
        var _yy = _y + _step * i;
        ui_button(_x, _yy, _w, _h, _items[i].label, {
            enabled: _items[i].enabled, focus: _ui.focus == i,
            hover: ui_hit(_x, _yy, _w, _h), pressed: ui_hit(_x, _yy, _w, _h) && inp_down("lmb"),
            danger: struct_or(_items[i], "danger", false) });
    }
}

// ================================================================== game over
function gameover_open() {
    global.go = { t: 0, focus: -1, ready: false };
    inp_block_all();
}

function gameover_items() {
    var _has_cp = !is_undefined(global.checkpoint_snapshot);
    return [
        { label: _has_cp ? "Return to Last Checkpoint" : "Restart Chapter", enabled: true, reason: "" },
        { label: "Load Game", enabled: save_any_valid(), reason: "No saves available." },
        { label: "Main Menu", enabled: true, reason: "" }
    ];
}

function gameover_step() {
    var _g = global.go;
    _g.t += 1;
    if (!_g.ready) {
        if (_g.t >= ms_ticks(600) && !inp_activation_held()) {
            _g.ready = true;
            _g.focus = 0;
        }
        return;
    }
    if (inp_pressed("pause")) {
        inp_consume("pause");
        _g.focus = 2;   // Escape focuses Main Menu but does not activate it
        ui_snd("snd_ui_move");
        return;
    }
    var _act = vmenu_input(gameover_items(), _g, 384, 328, 512, 56, 72);
    if (_act < 0) return;
    ui_snd("snd_ui_confirm");
    mus_stop(150);
    switch (_act) {
        case 0:
            var _snap = is_undefined(global.checkpoint_snapshot) ? global.initial_snapshot : global.checkpoint_snapshot;
            if (is_undefined(_snap)) {
                game_new();
            } else {
                game_restore(_snap, false);
                if (!is_undefined(global.checkpoint_snapshot)) toast_show(scene_text("checkpoint_restored"), 120, C_SUCCESS);
            }
            break;
        case 1: saveload_open("load", "gameover", undefined); break;
        case 2: game_to_menu(); break;
    }
}

function gameover_draw() {
    var _g = global.go;
    ui_dim(0.88);
    text_draw(640, 152, "Game Over", "title", C_TEXT, fa_center);
    text_draw(640, 220, "Dave has fallen in the desert.", "body", C_MUTED, fa_center);
    var _info;
    if (is_undefined(global.checkpoint_snapshot)) _info = "No checkpoint saved yet. Restart from the desert's edge.";
    else _info = "Last checkpoint: " + struct_or(global.checkpoint_snapshot, "location", "Desert");
    text_draw(640, 268, _info, "meta", C_MUTED, fa_center);
    var _f = _g.ready ? _g.focus : -1;
    var _tmp = { focus: _f };
    vmenu_draw(gameover_items(), _tmp, 384, 328, 512, 56, 72);
}

// ================================================================== ending
function ending_open(_skipped) {
    global.ending = { t: 0, enable_at: _skipped ? 0 : ms_ticks(4000), fade: 0, ready: false, focus: false };
    global.mode = MODE.ENDING;
    inp_block_all();
}

function ending_step() {
    var _e = global.ending;
    _e.t += 1;
    _e.fade = min(1, _e.t / ms_ticks(800));
    if (!_e.ready) {
        if (_e.t >= max(_e.enable_at, ms_ticks(800)) && !inp_activation_held() && !inp_down("pause")) {
            _e.ready = true;
            _e.focus = true;
        }
        return;
    }
    var _go = inp_pressed("confirm") || inp_pressed("pause") || (inp_pressed("lmb") && ui_hit(448, 432, 384, 56));
    if (_go) {
        inp_block_all();
        ui_snd("snd_ui_confirm");
        game_to_menu();
    }
}

function ending_draw() {
    var _e = global.ending;
    ui_rect(0, 0, GUI_W, GUI_H, c_black);
    var _bg = asset_or("spr_ending_bg", asset_or("spr_ph_ending_bg", -1));
    if (_bg >= 0) draw_sprite_stretched_ext(_bg, 0, 0, 0, GUI_W, GUI_H, c_white, _e.fade);
    var _a = _e.fade;
    text_draw(640, 168, "CHAPTER I", "meta", C_MUTED, fa_center, _a);
    text_draw(640, 216, scene_text("ui_ending_title"), "title", C_TEXT, fa_center, _a);
    text_draw(640, 296, "Beyond the desert, the search goes on.", "body", C_MUTED, fa_center, _a);
    if (_e.ready) {
        ui_button(448, 432, 384, 56, scene_text("ui_return_menu"), { enabled: true, focus: _e.focus, hover: ui_hit(448, 432, 384, 56) });
        text_draw(640, 520, "Your journey continues in the next chapter.", "meta", C_MUTED, fa_center);
    }
}

// ================================================================== dispatcher
function game_draw_gui() {
    draw_reset();
    var _top = ui_top();
    switch (global.mode) {
        case MODE.TITLE: title_draw(); break;
        case MODE.CINEMA:
            if (is_struct(global.cine_ctl) && is_method(global.cine_ctl.draw)) global.cine_ctl.draw();
            break;
        case MODE.PLAY:
            var _plain = (_top == -1 || _top == OV.DIALOGUE);
            if (_plain && !global.cine_lock) hud_draw_toasts();
            if (global.boss_ui.visible && _top == -1) hud_draw_boss();
            if (_plain && (!global.cine_lock || global.boss_ui.visible || ui_has(OV.DIALOGUE))) hud_draw_hp();
            if (_top == -1 && hotbar_visible()) hud_draw_hotbar(false);
            if (global.cine_lock && is_struct(global.cine_ctl) && is_method(global.cine_ctl.draw)) global.cine_ctl.draw();
            break;
        case MODE.GAMEOVER: gameover_draw(); break;
        case MODE.ENDING: ending_draw(); break;
    }
    var _s = global.ui.stack;
    for (var i = 0; i < array_length(_s); i++) {
        switch (_s[i]) {
            case OV.INVENTORY: inventory_draw(); break;
            case OV.DIALOGUE: dialogue_draw(); break;
            case OV.PAUSE: pause_draw(); break;
            case OV.SETTINGS: settings_draw(); break;
            case OV.SAVELOAD: saveload_draw(); break;
            case OV.CONFIRM: confirm_draw(); break;
        }
    }
    if (global.whiteout.alpha > 0) {
        ui_rect(0, 0, GUI_W, GUI_H, global.whiteout.dark ? c_black : make_colour_rgb(250, 247, 240), global.whiteout.alpha);
    }
    if (global.fade_black > 0) ui_rect(0, 0, GUI_W, GUI_H, c_black, global.fade_black);
    var _ta = transition_alpha();
    if (_ta > 0) ui_rect(0, 0, GUI_W, GUI_H, c_black, _ta);
    draw_reset();
}
