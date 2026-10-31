// scr_dialogue - typewriter text runner and the dialogue overlay (UI_SPEC section 6).
// One runner drives both modal dialogue (boss_intro) and timed cinematic text windows, so blips use
// a single scheduler: one blip per second newly revealed letter/digit, punctuation pauses of
// 120 ms (comma/semicolon) and 240 ms (sentence end/ellipsis), cancelled on instant reveal or exit.

function textrun_create(_line, _role, _width) {
    var _lines = text_wrap(_line.text, _role, _width);
    var _pages = [];
    for (var i = 0; i < array_length(_lines); i += 2) {
        var _pg = [_lines[i]];
        if (i + 1 < array_length(_lines)) array_push(_pg, _lines[i + 1]);
        array_push(_pages, _pg);
    }
    var _tr = {
        line: _line, pages: _pages, page: 0, shown: 0, total: 0, acc: 0, pause: 0,
        eligible: 0, cps: cfg("text_cps", 24), role: _role
    };
    textrun_set_page(_tr, 0);
    return _tr;
}

function textrun_set_page(_tr, _p) {
    _tr.page = _p;
    _tr.shown = 0;
    _tr.acc = 0;
    _tr.pause = 0;
    _tr.eligible = 0;
    var _t = 0;
    var _pg = _tr.pages[_p];
    for (var i = 0; i < array_length(_pg); i++) _t += string_length(_pg[i]);
    _tr.total = _t;
}

function textrun_char(_tr, _k) {
    var _pg = _tr.pages[_tr.page];
    for (var i = 0; i < array_length(_pg); i++) {
        var _len = string_length(_pg[i]);
        if (_k < _len) return string_char_at(_pg[i], _k + 1);
        _k -= _len;
    }
    return "";
}

function textrun_page_done(_tr) {
    return _tr.shown >= _tr.total;
}

function textrun_step(_tr) {
    if (textrun_page_done(_tr)) return;
    if (_tr.pause > 0) {
        _tr.pause -= 1;
        return;
    }
    _tr.acc += _tr.cps / TPS;
    while (_tr.acc >= 1 && _tr.shown < _tr.total) {
        _tr.acc -= 1;
        var _ch = textrun_char(_tr, _tr.shown);
        _tr.shown += 1;
        if (char_is_alnum(_ch)) {
            _tr.eligible += 1;
            if (_tr.eligible mod 2 == 1) aud_blip(_tr.line.blip);
        }
        if (_ch == "," || _ch == ";") {
            _tr.pause = ms_ticks(120);
            _tr.acc = 0;
            break;
        }
        if (_ch == "." || _ch == "!" || _ch == "?" || _ch == "…") {
            _tr.pause = ms_ticks(240);
            _tr.acc = 0;
            break;
        }
    }
}

/// Completes the current page instantly; never synthesizes the unrevealed blips.
function textrun_reveal(_tr) {
    _tr.shown = _tr.total;
    _tr.pause = 0;
    aud_blip_cancel();
}

/// Moves to the next page. Returns false when the line has no more pages.
function textrun_next(_tr) {
    if (_tr.page + 1 >= array_length(_tr.pages)) return false;
    textrun_set_page(_tr, _tr.page + 1);
    return true;
}

function textrun_draw(_tr, _x, _y, _alpha = 1) {
    var _pg = _tr.pages[_tr.page];
    var _left = _tr.shown;
    var _lh = ui_line_h(_tr.role);
    for (var i = 0; i < array_length(_pg); i++) {
        if (_left <= 0) break;
        var _s = _pg[i];
        var _vis = string_copy(_s, 1, min(_left, string_length(_s)));
        text_draw(_x, _y + i * _lh, _vis, _tr.role, C_TEXT, fa_left, _alpha);
        _left -= string_length(_s);
    }
}

// ------------------------------------------------------------------ modal dialogue overlay
function dialogue_open(_scene_id, _on_complete) {
    if (ui_has(OV.INVENTORY)) ui_close_inventory(true);
    global.dlg = { scene_id: _scene_id, index: 0, count: dialogue_count(_scene_id), tr: undefined,
                   on_complete: _on_complete, done: false };
    dialogue_load_line(0);
    ui_push(OV.DIALOGUE);
    global.aud.text_duck = true;
    inp_block_all();
}

function dialogue_load_line(_i) {
    var _d = global.dlg;
    _d.index = _i;
    var _line = dialogue_line(_d.scene_id, _i);
    if (is_undefined(_line)) {
        _d.tr = undefined;
        return;
    }
    var _narr = (_line.speaker == "narrator");
    _d.tr = textrun_create(_line, "dialogue", _narr ? 1160 : 928);
}

function dialogue_step() {
    var _d = global.dlg;
    if (!is_struct(_d) || _d.done) return;
    if (inp_pressed("pause")) {
        inp_consume("pause");
        pause_open(true);
        return;
    }
    var _tr = _d.tr;
    if (is_undefined(_tr)) {
        dialogue_finish();
        return;
    }
    textrun_step(_tr);
    var _act = inp_pressed("confirm") || inp_pressed("lmb");
    if (!_act) return;
    inp_consume("confirm");
    inp_consume("lmb");
    if (!textrun_page_done(_tr)) {
        textrun_reveal(_tr);   // a fresh activation reveals; it never also advances
        return;
    }
    if (textrun_next(_tr)) return;
    aud_blip_cancel();
    if (_d.index + 1 < _d.count) dialogue_load_line(_d.index + 1);
    else dialogue_finish();
}

/// Normal end and skip share this path; completion runs exactly once.
function dialogue_finish() {
    var _d = global.dlg;
    if (!is_struct(_d) || _d.done) return;
    _d.done = true;
    aud_blip_cancel();
    global.aud.text_duck = false;
    ui_remove(OV.DIALOGUE);
    inp_block_all();
    var _cb = _d.on_complete;
    global.dlg = undefined;
    if (is_method(_cb)) _cb();
}

function dialogue_draw() {
    var _d = global.dlg;
    if (!is_struct(_d) || is_undefined(_d.tr)) return;
    var _tr = _d.tr;
    var _line = _tr.line;
    ui_panel(24, 440, 1232, 256);
    var _narr = (_line.speaker == "narrator");
    if (_narr) {
        textrun_draw(_tr, 48, 496);
    } else {
        var _spr = portrait_sprite(_line.portrait_id, _line.expression);
        if (_spr < 0) _spr = asset_or("spr_ph_portrait_" + _line.speaker, -1);
        ui_rect(48, 464, 208, 208, C_WELL);
        if (_spr >= 0) draw_sprite_stretched(_spr, 0, 48, 464, 208, 208);
        ui_outline(50, 466, 204, 204, C_EDGE, 2);
        text_draw(280, 464, speaker_name(_line.speaker), "heading", C_TEXT);
        textrun_draw(_tr, 280, 512);
    }
    var _hint = textrun_page_done(_tr) ? "… Continue" : "Enter / Space / LMB  Reveal";
    text_draw(_narr ? 48 : 280, 648, _hint, "meta", C_MUTED);
    if (array_length(_tr.pages) > 1) {
        text_draw(1208, 648, string(_tr.page + 1) + " / " + string(array_length(_tr.pages)), "meta", C_MUTED, fa_right);
    }
}
