// scr_text - font roles, measured wrapping and line-box text drawing (UI_SPEC section 2).
// Text y coordinates are the top of a line box; glyph cells are offset so the baseline sits where
// the spec's line box places it.

function ui_font(_role) {
    switch (_role) {
        case "meta": return fnt_ui_meta;
        case "heading": return fnt_ui_heading;
        case "dialogue": return fnt_ui_dialogue;
        case "title": return fnt_ui_title;
        default: return fnt_ui_body;
    }
}

function ui_line_h(_role) {
    switch (_role) {
        case "meta": return 24;
        case "heading": return 36;
        case "dialogue": return 36;
        case "title": return 58;
        default: return 30;
    }
}

function ui_font_dy(_role) {
    switch (_role) {
        case "meta": return -1;
        case "heading": return -1;
        case "dialogue": return -1;
        case "title": return -3;
        default: return 0;
    }
}

function text_w(_str, _role) {
    draw_set_font(ui_font(_role));
    return string_width(_str);
}

/// Draws one line. _ha: fa_left / fa_center / fa_right (x is the anchor).
function text_draw(_x, _y, _str, _role, _col = C_TEXT, _ha = fa_left, _alpha = 1) {
    draw_set_font(ui_font(_role));
    draw_set_halign(_ha);
    draw_set_valign(fa_top);
    draw_set_colour(_col);
    draw_set_alpha(_alpha);
    draw_text(round(_x), round(_y + ui_font_dy(_role)), _str);
    draw_set_alpha(1);
    draw_set_halign(fa_left);
}

/// Ellipsizes to the available width without changing the source data.
function text_fit(_str, _role, _width) {
    draw_set_font(ui_font(_role));
    if (string_width(_str) <= _width) return _str;
    var _ell = "…";
    var _n = string_length(_str);
    while (_n > 0 && string_width(string_copy(_str, 1, _n) + _ell) > _width) _n--;
    return string_copy(_str, 1, _n) + _ell;
}

/// Word-wraps measured text into an array of lines. Words longer than the width break by character.
function text_wrap(_str, _role, _width) {
    draw_set_font(ui_font(_role));
    var _lines = [];
    var _words = string_split(_str, " ");
    var _cur = "";
    for (var i = 0; i < array_length(_words); i++) {
        var _w = _words[i];
        var _try = (_cur == "") ? _w : (_cur + " " + _w);
        if (string_width(_try) <= _width) {
            _cur = _try;
            continue;
        }
        if (_cur != "") array_push(_lines, _cur);
        _cur = _w;
        while (string_width(_cur) > _width && string_length(_cur) > 1) {
            var _k = string_length(_cur);
            while (_k > 1 && string_width(string_copy(_cur, 1, _k)) > _width) _k--;
            array_push(_lines, string_copy(_cur, 1, _k));
            _cur = string_delete(_cur, 1, _k);
        }
    }
    if (_cur != "" || array_length(_lines) == 0) array_push(_lines, _cur);
    return _lines;
}

/// Draws wrapped lines inside a box, clipping to _max_lines (returns lines drawn).
function text_draw_wrapped(_x, _y, _str, _role, _width, _max_lines, _col = C_TEXT, _ha = fa_left) {
    var _lines = text_wrap(_str, _role, _width);
    var _lh = ui_line_h(_role);
    var _n = min(array_length(_lines), _max_lines);
    var _ax = _x;
    if (_ha == fa_center) _ax = _x + _width / 2;
    else if (_ha == fa_right) _ax = _x + _width;
    for (var i = 0; i < _n; i++) text_draw(_ax, _y + i * _lh, _lines[i], _role, _col, _ha);
    return _n;
}

function draw_reset() {
    draw_set_alpha(1);
    draw_set_colour(c_white);
    draw_set_halign(fa_left);
    draw_set_valign(fa_top);
}
