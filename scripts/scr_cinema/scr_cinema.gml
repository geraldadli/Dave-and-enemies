// scr_cinema - shared cinematic control: advance/skip input, text windows and completion guards.
// cutscene_advance = Enter/Space (or LMB); cutscene_skip = hold Escape for 0.6 s. During a timed
// cinematic, Escape belongs to the cinematic and never also opens pause. Every scene calls one
// idempotent completion routine for normal end, final advance and skip.

/// _ctl fields: on_skip, on_advance, draw (methods), skip_allowed (bool).
function cine_begin(_ctl) {
    _ctl.hold = 0;
    _ctl.hint_t = 0;
    if (!variable_struct_exists(_ctl, "skip_allowed")) _ctl.skip_allowed = true;
    global.cine_ctl = _ctl;
    inp_block_all();
}

function cine_end() {
    global.cine_ctl = undefined;
    inp_block_all();
}

function cine_input_step() {
    var _c = global.cine_ctl;
    if (!is_struct(_c)) return;
    if (_c.hint_t > 0) _c.hint_t -= 1;
    if (inp_pressed("pause")) _c.hint_t = 120;
    // only a fresh, deliberate hold counts: inp_down ignores keys still blocked from a previous state
    if (_c.skip_allowed && inp_down("pause")) {
        _c.hold += 1;
        _c.hint_t = max(_c.hint_t, 30);
        if (_c.hold >= ms_ticks(600)) {
            _c.hold = 0;
            inp_block_all();
            if (is_method(_c.on_skip)) _c.on_skip();
            return;
        }
    } else _c.hold = 0;
    if (inp_pressed("confirm") || inp_pressed("lmb")) {
        inp_consume("confirm");
        inp_consume("lmb");
        _c.hint_t = 120;
        if (is_method(_c.on_advance)) _c.on_advance();
    }
}

function cine_draw_skip_hint() {
    var _c = global.cine_ctl;
    if (!is_struct(_c) || !_c.skip_allowed) return;
    var _a = (_c.hint_t > 0) ? min(1, _c.hint_t / 20) : 0.35;
    var _label = "Esc  " + scene_text("ui_skip");
    var _w = text_w(_label, "meta") + 28;
    ui_round(1256 - _w, 24, _w, 32, C_INK, 8, false, 0.8 * _a);
    text_draw(1256 - _w + 14, 28, _label, "meta", C_TEXT, fa_left, _a);
    if (_c.hold > 0) ui_rect(1256 - _w, 52, _w * (_c.hold / ms_ticks(600)), 4, C_GOLD, _a);
}

/// Timed cinematic caption: a compact band at the top of the screen, so the storyboard's framing
/// (Dave and the fallen soldiers sit low in the frame) stays visible. Narrator lines have no portrait.
#macro CAPTION_W_NARR 896
#macro CAPTION_W_SPEAKER 800
function cine_draw_text(_tr, _alpha) {
    if (!is_struct(_tr) || _alpha <= 0) return;
    var _line = _tr.line;
    ui_nine(spr_ui_panel, 0, 120, 24, 960, 132, 24, c_white, 0.94 * _alpha);
    if (_line.speaker == "narrator") {
        textrun_draw(_tr, 152, 54, _alpha);
    } else {
        var _spr = portrait_sprite(_line.portrait_id, _line.expression);
        if (_spr < 0) _spr = asset_or("spr_ph_portrait_" + _line.speaker, -1);
        ui_rect(136, 42, 96, 96, C_WELL, _alpha);
        if (_spr >= 0) draw_sprite_stretched_ext(_spr, 0, 136, 42, 96, 96, c_white, _alpha);
        ui_outline(136, 42, 96, 96, C_EDGE, 2, _alpha);
        text_draw(256, 38, speaker_name(_line.speaker), "heading", C_TEXT, fa_left, _alpha);
        textrun_draw(_tr, 256, 76, _alpha);
    }
    draw_set_alpha(1);
}

/// Executes one storyboard audio cue (shared by intro, boss intro, defeat and ending).
function cine_audio_cue(_cue, _tag) {
    var _id = _cue.asset_id;
    var _fade = round(struct_or(_cue, "fade_s", -1) * 1000);
    switch (_cue.action) {
        case "start_non_loop":
        case "start_loop":
            mus_play(_id);
            break;
        case "fade_in_loop":
            if (_id == "snd_wind_loop") aud_loop(_id, "weather", undefined, undefined, false);
            else mus_play(_id, _fade);
            break;
        case "resume_quietly":
            aud_loop(_id, "weather", undefined, undefined, false);
            break;
        case "fade_out":
            if (string_pos("mus_", _id) == 1) {
                if (mus_current() == _id) mus_stop(_fade);
            } else aud_loop_stop("weather", _fade);
            break;
        case "play_once":
        case "play_once_optional":
            aud_play(_id, undefined, undefined, "", false);
            break;
        default:
            // score_direction / animation_step_events / transfer notes are realised by the scene itself
            break;
    }
}
