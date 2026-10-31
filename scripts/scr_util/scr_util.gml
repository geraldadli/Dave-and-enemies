// scr_util - small helpers shared by every system.

/// Reads a UTF-8 JSON file (included file or save file). Returns undefined on any failure.
function json_load_file(_path) {
    if (!file_exists(_path)) return undefined;
    var _buf = buffer_load(_path);
    if (_buf < 0) return undefined;
    var _txt = buffer_read(_buf, buffer_string);
    buffer_delete(_buf);
    if (string_length(_txt) > 0 && ord(string_char_at(_txt, 1)) == 65279) _txt = string_delete(_txt, 1, 1);
    var _out = undefined;
    try {
        _out = json_parse(_txt);
    } catch (_e) {
        _out = undefined;
    }
    return _out;
}

/// Writes a struct as JSON. Returns true only when every byte was written.
function json_save_file(_path, _value) {
    var _ok = false;
    try {
        var _txt = json_stringify(_value);
        var _buf = buffer_create(max(1, string_byte_length(_txt)), buffer_fixed, 1);
        buffer_write(_buf, buffer_text, _txt);
        buffer_save(_buf, _path);
        buffer_delete(_buf);
        _ok = file_exists(_path);
    } catch (_e) {
        _ok = false;
    }
    return _ok;
}

function cell_px(_c) { return _c * TILE + TILE / 2; }
function px_cell(_p) { return floor(_p / TILE); }

/// Inclusive cell rectangle [x1,y1,x2,y2] contains cell (cx, cy).
function rect_has_cell(_r, _cx, _cy) {
    if (!is_array(_r)) return false;
    return _cx >= _r[0] && _cx <= _r[2] && _cy >= _r[1] && _cy <= _r[3];
}

/// Inclusive cell rectangle contains the ground pixel (px, py).
function rect_has_px(_r, _px, _py) {
    return rect_has_cell(_r, px_cell(_px), px_cell(_py));
}

function approach(_a, _b, _amt) {
    if (_a < _b) return min(_a + _amt, _b);
    return max(_a - _amt, _b);
}

function smoothstep01(_t) {
    _t = clamp(_t, 0, 1);
    return _t * _t * (3 - 2 * _t);
}

function db_to_lin(_db) { return power(10, _db / 20); }
function ms_ticks(_ms) { return ceil(_ms * TPS / 1000); }

/// 8-way direction index, 0 = east, counter-clockwise (contract section 4).
function dir8(_angle) {
    return ((round(_angle / 45) mod 8) + 8) mod 8;
}

/// Facing name for Dave's authored cardinals: side (east), up, left (west), down.
/// Diagonals keep the horizontal facing, the documented fallback until diagonals are delivered.
function facing_from_angle(_angle) {
    var _a = ((_angle mod 360) + 360) mod 360;
    if (_a <= 50 || _a >= 310) return "side";
    if (_a > 50 && _a < 130) return "up";
    if (_a >= 130 && _a <= 230) return "left";
    return "down";
}

function facing_from_index(_i) {
    switch (_i) {
        case 0: case 1: case 7: return "side";
        case 2: return "up";
        case 3: case 4: case 5: return "left";
        default: return "down";
    }
}

function facing_angle(_f) {
    switch (_f) {
        case "side": return 0;
        case "up": return 90;
        case "left": return 180;
        default: return 270;
    }
}

function fmt_playtime(_ticks) {
    var _s = floor(_ticks / TPS);
    var _h = _s div 3600;
    var _m = (_s div 60) mod 60;
    var _sec = _s mod 60;
    return string_replace_all(string_format(_h, 2, 0), " ", "0") + ":" +
           string_replace_all(string_format(_m, 2, 0), " ", "0") + ":" +
           string_replace_all(string_format(_sec, 2, 0), " ", "0");
}

function fmt_date(_dt) {
    var _months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var _mo = clamp(date_get_month(_dt), 1, 12);
    var _hh = string_replace_all(string_format(date_get_hour(_dt), 2, 0), " ", "0");
    var _mi = string_replace_all(string_format(date_get_minute(_dt), 2, 0), " ", "0");
    return string(date_get_day(_dt)) + " " + _months[_mo - 1] + " " + string(date_get_year(_dt)) + " " + _hh + ":" + _mi;
}

/// True for ASCII letters and digits (blip-eligible characters).
function char_is_alnum(_ch) {
    var _o = ord(_ch);
    return (_o >= 48 && _o <= 57) || (_o >= 65 && _o <= 90) || (_o >= 97 && _o <= 122);
}

function struct_or(_s, _key, _default) {
    if (!is_struct(_s)) return _default;
    var _v = _s[$ _key];
    return is_undefined(_v) ? _default : _v;
}

function array_or(_v) {
    return is_array(_v) ? _v : [];
}

/// Asset index by name, or -1 when the resource is not in the project (placeholder fallback).
function asset_or(_name, _fallback) {
    if (!is_string(_name) || _name == "") return _fallback;
    var _i = asset_get_index(_name);
    return (_i < 0) ? _fallback : _i;
}

function shake_camera(_amp, _ticks) {
    if (!global.settings.shake) return;
    global.cam_shake_amp = max(global.cam_shake_amp, _amp);
    global.cam_shake_t = max(global.cam_shake_t, _ticks);
}
