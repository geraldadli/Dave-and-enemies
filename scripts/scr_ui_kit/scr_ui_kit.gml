// scr_ui_kit - drawing primitives for the 1280x720 GUI plane (UI_SPEC sections 2, 10).
// Nine-slices are drawn in code from the supplied prototype frames (panel 24 px, button 16 px,
// HP frame 8 px borders) so destination rectangles can differ from source sizes.

function ui_nine(_spr, _sub, _x, _y, _w, _h, _b, _col = c_white, _alpha = 1) {
    if (_spr < 0) return;
    var _sw = sprite_get_width(_spr);
    var _sh = sprite_get_height(_spr);
    var _b2 = min(_b, floor(_w / 2), floor(_h / 2));
    var _mw = _sw - 2 * _b;
    var _mh = _sh - 2 * _b;
    var _dw = _w - 2 * _b2;
    var _dh = _h - 2 * _b2;
    var _xs = _dw / max(1, _mw);
    var _ys = _dh / max(1, _mh);
    var _bs = _b2 / _b;
    // corners
    draw_sprite_part_ext(_spr, _sub, 0, 0, _b, _b, _x, _y, _bs, _bs, _col, _alpha);
    draw_sprite_part_ext(_spr, _sub, _sw - _b, 0, _b, _b, _x + _w - _b2, _y, _bs, _bs, _col, _alpha);
    draw_sprite_part_ext(_spr, _sub, 0, _sh - _b, _b, _b, _x, _y + _h - _b2, _bs, _bs, _col, _alpha);
    draw_sprite_part_ext(_spr, _sub, _sw - _b, _sh - _b, _b, _b, _x + _w - _b2, _y + _h - _b2, _bs, _bs, _col, _alpha);
    // edges
    draw_sprite_part_ext(_spr, _sub, _b, 0, _mw, _b, _x + _b2, _y, _xs, _bs, _col, _alpha);
    draw_sprite_part_ext(_spr, _sub, _b, _sh - _b, _mw, _b, _x + _b2, _y + _h - _b2, _xs, _bs, _col, _alpha);
    draw_sprite_part_ext(_spr, _sub, 0, _b, _b, _mh, _x, _y + _b2, _bs, _ys, _col, _alpha);
    draw_sprite_part_ext(_spr, _sub, _sw - _b, _b, _b, _mh, _x + _w - _b2, _y + _b2, _bs, _ys, _col, _alpha);
    // centre
    draw_sprite_part_ext(_spr, _sub, _b, _b, _mw, _mh, _x + _b2, _y + _b2, _xs, _ys, _col, _alpha);
}

function ui_panel(_x, _y, _w, _h) {
    ui_nine(spr_ui_panel, 0, _x, _y, _w, _h, 24);
}

function ui_rect(_x, _y, _w, _h, _col, _alpha = 1, _outline = false) {
    draw_set_colour(_col);
    draw_set_alpha(_alpha);
    draw_rectangle(_x, _y, _x + _w - 1, _y + _h - 1, _outline);
    draw_set_alpha(1);
}

function ui_round(_x, _y, _w, _h, _col, _r = 8, _outline = false, _alpha = 1) {
    draw_set_alpha(_alpha);
    draw_roundrect_colour_ext(_x, _y, _x + _w - 1, _y + _h - 1, _r, _r, _col, _col, _outline);
    draw_set_alpha(1);
}

/// Outline of a given thickness (inset).
function ui_outline(_x, _y, _w, _h, _col, _t = 2, _alpha = 1) {
    for (var i = 0; i < _t; i++) ui_rect(_x + i, _y + i, _w - 2 * i, _h - 2 * i, _col, _alpha, true);
}

function ui_dashed(_x, _y, _w, _h, _col, _alpha = 1) {
    draw_set_colour(_col);
    draw_set_alpha(_alpha);
    var _x2 = _x + _w - 1;
    var _y2 = _y + _h - 1;
    for (var i = _x; i < _x2; i += 10) {
        draw_line(i, _y, min(i + 5, _x2), _y);
        draw_line(i, _y2, min(i + 5, _x2), _y2);
    }
    for (var j = _y; j < _y2; j += 10) {
        draw_line(_x, j, _x, min(j + 5, _y2));
        draw_line(_x2, j, _x2, min(j + 5, _y2));
    }
    draw_set_alpha(1);
}

/// Keyboard focus: 2 px gold outline + 4 px corner ticks.
function ui_focus(_x, _y, _w, _h, _col = C_GOLD) {
    ui_outline(_x + 1, _y + 1, _w - 2, _h - 2, _col, 2);
    var _t = 4;
    var _l = 12;
    ui_rect(_x - _t, _y - _t, _l, _t, _col);
    ui_rect(_x - _t, _y - _t, _t, _l, _col);
    ui_rect(_x + _w - _l + _t, _y - _t, _l, _t, _col);
    ui_rect(_x + _w, _y - _t, _t, _l, _col);
    ui_rect(_x - _t, _y + _h, _l, _t, _col);
    ui_rect(_x - _t, _y + _h - _l + _t, _t, _l, _col);
    ui_rect(_x + _w - _l + _t, _y + _h, _l, _t, _col);
    ui_rect(_x + _w, _y + _h - _l + _t, _t, _l, _col);
}

/// Persistent selection marker (outline plus short bottom marker).
function ui_selected(_x, _y, _w, _h) {
    ui_outline(_x + 1, _y + 1, _w - 2, _h - 2, C_GOLD, 2);
    ui_rect(_x + (_w - 20) / 2, _y + _h - 6, 20, 3, C_GOLD);
}

function ui_dim(_alpha) {
    ui_rect(0, 0, GUI_W, GUI_H, C_INK, _alpha);
}

/// Clip to a GUI rectangle using the same logical-to-window transform as drawing.
function ui_clip_begin(_x, _y, _w, _h) {
    var _s = global.gui_s;
    gpu_set_scissor(floor(global.gui_ox + _x * _s), floor(global.gui_oy + _y * _s), ceil(_w * _s), ceil(_h * _s));
}

function ui_clip_end() {
    gpu_set_scissor(0, 0, max(1, window_get_width()), max(1, window_get_height()));
}

/// Button. _st: { enabled, focus, hover, pressed, danger, selected }
function ui_button(_x, _y, _w, _h, _label, _st) {
    var _en = struct_or(_st, "enabled", true);
    var _hov = struct_or(_st, "hover", false) && _en;
    var _pr = struct_or(_st, "pressed", false) && _en;
    var _frame = _pr ? 2 : (_hov ? 1 : 0);
    ui_nine(spr_ui_button, _frame, _x, _y, _w, _h, 16, c_white, _en ? 1 : 0.75);
    if (!_en) ui_dashed(_x + 3, _y + 3, _w - 6, _h - 6, C_DISABLED);
    if (struct_or(_st, "danger", false)) ui_outline(_x, _y, _w, _h, C_ERROR, 2);
    if (struct_or(_st, "selected", false)) ui_rect(_x + (_w - 20) / 2, _y + _h - 6, 20, 3, C_GOLD);
    var _col = _en ? C_TEXT : C_DISABLED;
    if (struct_or(_st, "danger", false) && _en) _col = C_ERROR;
    var _role = (_h <= 40) ? "meta" : "body";
    var _lab = text_fit(_en ? _label : ("— " + _label), _role, _w - 24);
    var _off = _pr ? 1 : 0;
    text_draw(_x + _w / 2, _y + (_h - ui_line_h(_role)) / 2 + _off, _lab, _role, _col, fa_center);
    if (struct_or(_st, "focus", false)) ui_focus(_x, _y, _w, _h);
}

/// Item slot (72x72): frame, 48 px icon, key label, stack count, equipped badge.
function ui_slot(_x, _y, _entry, _key_label, _st) {
    draw_sprite(spr_ui_slot, 0, _x, _y);
    if (is_struct(_entry)) {
        var _icon = item_icon(_entry.id);
        if (_icon >= 0) draw_sprite_stretched(_icon, 0, _x + 12, _y + 8, 48, 48);
        else {
            ui_round(_x + 14, _y + 10, 44, 44, C_RAISED, 8);
            text_draw(_x + 36, _y + 20, string_upper(string_copy(item_name(_entry.id), 1, 2)), "meta", C_MUTED, fa_center);
        }
        if (_entry.n > 1) {
            var _q = "×" + string(_entry.n);
            var _qw = text_w(_q, "meta");
            ui_rect(_x + 64 - _qw - 4, _y + 46, _qw + 6, 22, C_INK, 0.85);
            text_draw(_x + 66, _y + 46, _q, "meta", C_TEXT, fa_right);
        }
    } else {
        ui_rect(_x + 30, _y + 35, 12, 2, C_MUTED);
    }
    if (_key_label != "") {
        if (is_struct(_entry)) ui_rect(_x + 4, _y + 2, 18, 22, C_INK, 0.85);
        text_draw(_x + 7, _y + 1, _key_label, "meta", C_MUTED);
    }
    if (struct_or(_st, "equipped", false)) {
        ui_rect(_x + 47, _y + 2, 22, 24, C_INK, 0.9);
        ui_outline(_x + 47, _y + 2, 22, 24, C_GOLD, 1);
        text_draw(_x + 58, _y + 2, "E", "meta", C_GOLD, fa_center);
    }
    if (struct_or(_st, "selected", false)) draw_sprite(spr_ui_slot_selected, 0, _x, _y);
    if (struct_or(_st, "hover", false)) ui_outline(_x, _y, 72, 72, C_TEXT, 1, 0.6);
    if (struct_or(_st, "source", false)) ui_dashed(_x + 2, _y + 2, 68, 68, C_GOLD);
    if (struct_or(_st, "invalid", false)) ui_outline(_x, _y, 72, 72, C_ERROR, 2);
    if (struct_or(_st, "focus", false)) ui_focus(_x, _y, 72, 72);
}

/// Bar using the supplied HP frame (8 px caps) and a proportional fill clipped to the track.
function ui_bar(_x, _y, _w, _ratio, _col, _use_fill_sprite, _ghost_ratio = -1) {
    ui_nine(spr_ui_hp_frame, 0, _x, _y, _w, 32, 8);
    var _tx = _x + 8;
    var _ty = _y + 8;
    var _tw = _w - 16;
    ui_rect(_tx, _ty, _tw, 16, C_WELL);
    if (_ghost_ratio > _ratio) ui_rect(_tx, _ty, round(_tw * clamp(_ghost_ratio, 0, 1)), 16, C_TEXT, 0.35);
    var _fw = round(_tw * clamp(_ratio, 0, 1));
    if (_fw > 0) {
        if (_use_fill_sprite) draw_sprite_part_ext(spr_ui_hp_fill, 0, 8, 8, max(1, _fw), 16, _tx, _ty, 1, 1, c_white, 1);
        else {
            ui_rect(_tx, _ty, _fw, 16, _col);
            ui_rect(_tx, _ty, _fw, 3, c_white, 0.18);
        }
    }
}

/// Settings slider: track (352x20) with 24 px thumb.
function ui_slider(_x, _y, _w, _value, _focus, _enabled) {
    ui_round(_x, _y, _w, 20, C_WELL, 10);
    ui_round(_x, _y, max(20, _w * _value), 20, _enabled ? C_GOLD : C_DISABLED, 10, false, 0.55);
    var _tx = _x + _w * _value;
    ui_round(_tx - 12, _y - 6, 24, 32, _enabled ? C_TEXT : C_DISABLED, 6);
    if (_focus) ui_focus(_x - 4, _y - 10, _w + 8, 40);
}
