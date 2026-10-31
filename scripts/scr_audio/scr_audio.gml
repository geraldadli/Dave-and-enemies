// scr_audio - the shared audio service.
// Every trigger goes through aud_play / aud_loop / mus_play / aud_blip. The runtime catalog
// (datafiles/data/audio_catalog.json, derived from AUDIO_CUE_SHEET.csv + AUDIO_MANIFEST.json) supplies
// per-ID gain, bus, budget group, limits, cooldown, priority, loop flag and fades. Rejected requests
// are dropped, never queued. Loops are owned by a key so starting is idempotent.

function aud_init() {
    var _cat = json_load_file("data/audio_catalog.json");
    global.aud = {
        ids: {}, active: [], last_play: {}, last_var: {}, loops: {},
        mus: { id: "", h: -1, base: 1, env: 0, env_to: 0, env_rate: 0 },
        music_fading: [], tick: 0,
        budgets: { sfx: 24, warning: 6, movement: 6, projectile: 4, weather: 1, text: 1, music: 1, music_crossfade: 2 },
        duck_music_db: 0, duck_weather_db: 0, text_duck: false, warn_until: -1,
        blip_h: -1, blip_last: -1000, blip_stop_at: -1, blip_last_var: {},
        world_paused: false, pending: []
    };
    if (!is_struct(_cat)) {
        show_debug_message("audio catalog missing; audio disabled");
        return;
    }
    global.aud.budgets = _cat.budgets;
    var _names = variable_struct_get_names(_cat.ids);
    for (var i = 0; i < array_length(_names); i++) {
        var _src = _cat.ids[$ _names[i]];
        var _res = [];
        for (var r = 0; r < array_length(_src.res); r++) {
            var _a = asset_get_index(_src.res[r]);
            if (_a >= 0) array_push(_res, _a);
        }
        global.aud.ids[$ _names[i]] = {
            res: _res, gain: db_to_lin(_src.db), bus: _src.bus, grp: _src.grp,
            gl: max(1, _src.gl), rt: ms_ticks(_src.rt), pr: _src.pr, loop: _src.loop,
            fi: _src.fi, fo: _src.fo, sp: _src.sp
        };
    }
}

function aud_bus_volume(_bus) {
    switch (_bus) {
        case "music": return global.settings.music;
        case "dialogue": return global.settings.blips;
        default: return global.settings.sfx;
    }
}

/// Distance attenuation from the camera centre for spatial world sounds (no panning).
function aud_atten(_x, _y) {
    if (is_undefined(_x) || is_undefined(_y)) return 1;
    var _cx = global.cam_cx;
    var _cy = global.cam_cy;
    var _d = point_distance(_x, _y, _cx, _cy);
    if (_d <= 360) return 1;
    return clamp(1 - (_d - 360) / 900, 0, 1);
}

function aud_duck_factor(_grp, _bus) {
    if (_bus == "music") return db_to_lin(global.aud.duck_music_db);
    if (_grp == "weather") return db_to_lin(global.aud.duck_weather_db);
    return 1;
}

function aud_count_id(_id) {
    var _n = 0;
    var _a = global.aud.active;
    for (var i = 0; i < array_length(_a); i++) if (_a[i].id == _id) _n++;
    return _n;
}

function aud_count_grp(_grp) {
    var _n = 0;
    var _a = global.aud.active;
    for (var i = 0; i < array_length(_a); i++) if (_a[i].grp == _grp) _n++;
    return _n;
}

function aud_count_sfx() {
    var _n = 0;
    var _a = global.aud.active;
    for (var i = 0; i < array_length(_a); i++) if (_a[i].bus == "sfx") _n++;
    return _n;
}

/// Stops the lowest-priority active voice matching the filter if it is below _pr. Returns success.
function aud_evict(_pr, _grp) {
    var _a = global.aud.active;
    var _best = -1;
    var _best_pr = _pr;
    for (var i = 0; i < array_length(_a); i++) {
        var _e = _a[i];
        if (_e.bus != "sfx" || _e.owner != "") continue;
        if (_grp != "" && _e.grp != _grp) continue;
        if (_e.pr < _best_pr) {
            _best_pr = _e.pr;
            _best = i;
        }
    }
    if (_best < 0) return false;
    audio_stop_sound(_a[_best].h);
    array_delete(_a, _best, 1);
    return true;
}

function aud_pick_variant(_id, _e) {
    var _n = array_length(_e.res);
    if (_n <= 1) return _e.res[0];
    var _last = struct_or(global.aud.last_var, _id, -1);
    var _v = irandom(_n - 1);
    if (_v == _last) _v = (_v + 1 + irandom(_n - 2)) mod _n;
    global.aud.last_var[$ _id] = _v;
    return _e.res[_v];
}

/// Plays a one-shot (or loop when _owner given) for a stable event ID. Returns the handle or -1.
function aud_play(_id, _x = undefined, _y = undefined, _owner = "", _world = true) {
    var _A = global.aud;
    var _e = _A.ids[$ _id];
    if (is_undefined(_e) || array_length(_e.res) == 0) return -1;
    var _att = _e.sp ? aud_atten(_x, _y) : 1;
    if (_att <= 0.02) return -1;
    var _lp = struct_or(_A.last_play, _id, -100000);
    if (_A.tick - _lp < _e.rt) return -1;
    if (aud_count_id(_id) >= _e.gl) return -1;
    var _budget = struct_or(_A.budgets, _e.grp, -1);
    if (_e.grp != "sfx" && _e.grp != "ui" && _budget >= 0 && _e.bus == "sfx") {
        if (aud_count_grp(_e.grp) >= _budget && !aud_evict(_e.pr, _e.grp)) return -1;
    }
    if (_e.bus == "sfx" && aud_count_sfx() >= _A.budgets.sfx && !aud_evict(_e.pr, "")) return -1;
    var _snd = aud_pick_variant(_id, _e);
    var _loop = _e.loop && _owner != "";
    var _h = audio_play_sound(_snd, _e.pr, _loop);
    if (_h < 0) return -1;
    var _base = _e.gain * _att;
    var _rec = {
        h: _h, id: _id, grp: _e.grp, bus: _e.bus, pr: _e.pr, base: _base, x: _x, y: _y, sp: _e.sp,
        owner: _owner, world: _world, env: 1, env_to: 1, env_rate: 0, stop_at_zero: false
    };
    if (_loop && _e.fi > 0) {
        _rec.env = 0;
        _rec.env_rate = 1 / max(1, ms_ticks(_e.fi));
    }
    audio_sound_gain(_h, _base * _rec.env * aud_bus_volume(_e.bus) * aud_duck_factor(_e.grp, _e.bus), 0);
    array_push(_A.active, _rec);
    _A.last_play[$ _id] = _A.tick;
    if (_e.grp == "warning") _A.warn_until = _A.tick + 18;
    if (_A.world_paused && _world) audio_pause_sound(_h);
    return _h;
}

/// Starts (or keeps) an owned loop. Idempotent per owner key.
function aud_loop(_id, _owner, _x = undefined, _y = undefined, _world = true) {
    var _A = global.aud;
    var _cur = _A.loops[$ _owner];
    if (is_struct(_cur) && audio_is_playing(_cur.h) && !_cur.stop_at_zero) {
        _cur.x = _x;
        _cur.y = _y;
        return _cur.h;
    }
    var _h = aud_play(_id, _x, _y, _owner, _world);
    if (_h < 0) return -1;
    _A.loops[$ _owner] = _A.active[array_length(_A.active) - 1];
    return _h;
}

function aud_loop_move(_owner, _x, _y) {
    var _cur = global.aud.loops[$ _owner];
    if (is_struct(_cur)) {
        _cur.x = _x;
        _cur.y = _y;
    }
}

/// Fades and stops an owned loop (fade < 0 uses the catalog fade-out).
function aud_loop_stop(_owner, _fade_ms = -1) {
    var _A = global.aud;
    var _cur = _A.loops[$ _owner];
    if (!is_struct(_cur)) return;
    var _e = _A.ids[$ _cur.id];
    var _f = (_fade_ms < 0) ? (is_struct(_e) ? _e.fo : 40) : _fade_ms;
    if (_f <= 0) {
        audio_stop_sound(_cur.h);
        _cur.stop_at_zero = true;
        _cur.env = 0;
    } else {
        _cur.env_to = 0;
        _cur.env_rate = 1 / max(1, ms_ticks(_f));
        _cur.stop_at_zero = true;
    }
    variable_struct_remove(_A.loops, _owner);
}

/// Stops every owned loop whose key starts with the prefix ("boss", "enc:", "" = all).
function aud_loops_stop_prefix(_prefix, _fade_ms = -1) {
    var _keys = variable_struct_get_names(global.aud.loops);
    for (var i = 0; i < array_length(_keys); i++) {
        if (_prefix == "" || string_pos(_prefix, _keys[i]) == 1) aud_loop_stop(_keys[i], _fade_ms);
    }
}

/// Stops world SFX (one-shots and loops). Used for scene unload, death, load, menu return.
function aud_stop_world(_fade_ms = 60) {
    var _keys = variable_struct_get_names(global.aud.loops);
    for (var k = 0; k < array_length(_keys); k++) {
        var _l = global.aud.loops[$ _keys[k]];
        if (is_struct(_l) && _l.world) aud_loop_stop(_keys[k], _fade_ms);
    }
    var _a = global.aud.active;
    for (var i = 0; i < array_length(_a); i++) {
        var _r = _a[i];
        if (_r.bus == "sfx" && _r.world && !_r.stop_at_zero) {
            _r.env_to = 0;
            _r.env_rate = 1 / max(1, ms_ticks(_fade_ms));
            _r.stop_at_zero = true;
        }
    }
    global.aud.pending = [];
}

/// Plays a cue after a delay (cancelled by aud_cancel_pending(tag)).
function aud_schedule(_id, _delay_ticks, _tag, _x = undefined, _y = undefined) {
    array_push(global.aud.pending, { id: _id, at: global.aud.tick + _delay_ticks, tag: _tag, x: _x, y: _y });
}

function aud_cancel_pending(_tag) {
    var _p = global.aud.pending;
    for (var i = array_length(_p) - 1; i >= 0; i--) {
        if (_tag == "" || _p[i].tag == _tag) array_delete(_p, i, 1);
    }
}

// ------------------------------------------------------------------ music
function mus_play(_id, _fade_in_ms = -1) {
    var _A = global.aud;
    if (_A.mus.id == _id && _A.mus.h >= 0 && audio_is_playing(_A.mus.h)) {
        _A.mus.env_to = 1;
        return;
    }
    var _e = _A.ids[$ _id];
    if (is_undefined(_e) || array_length(_e.res) == 0) return;
    mus_stop(-1);
    // crossfade cap: at most two music voices
    while (array_length(_A.music_fading) > 1) {
        audio_stop_sound(_A.music_fading[0].h);
        array_delete(_A.music_fading, 0, 1);
    }
    var _h = audio_play_sound(_e.res[0], _e.pr, _e.loop);
    var _fi = (_fade_in_ms < 0) ? _e.fi : _fade_in_ms;
    _A.mus = { id: _id, h: _h, base: _e.gain, env: (_fi > 0) ? 0 : 1, env_to: 1,
               env_rate: 1 / max(1, ms_ticks(_fi)) };
    audio_sound_gain(_h, _A.mus.base * _A.mus.env * global.settings.music * db_to_lin(_A.duck_music_db), 0);
}

function mus_stop(_fade_ms = -1) {
    var _A = global.aud;
    if (_A.mus.h < 0) return;
    var _e = _A.ids[$ _A.mus.id];
    var _f = (_fade_ms < 0) ? (is_struct(_e) ? _e.fo : 300) : _fade_ms;
    if (_f <= 0) audio_stop_sound(_A.mus.h);
    else array_push(_A.music_fading, { h: _A.mus.h, base: _A.mus.base, env: _A.mus.env,
                                     rate: _A.mus.env / max(1, ms_ticks(_f)) });
    _A.mus = { id: "", h: -1, base: 1, env: 0, env_to: 0, env_rate: 0 };
}

function mus_current() {
    return global.aud.mus.id;
}

// ------------------------------------------------------------------ dialogue blips
/// One blip for a profile ("voice_dave" ...). Single global voice; occupied = dropped.
function aud_blip(_profile) {
    var _A = global.aud;
    if (_profile == "silent" || _profile == "") return;
    if (_A.blip_h >= 0 && audio_is_playing(_A.blip_h)) return;
    if ((_A.tick - _A.blip_last) * 1000 / TPS < 75) return;
    var _prof = struct_or(struct_or(global.data.narrative, "vocal_blip_profiles", {}), _profile, undefined);
    if (!is_struct(_prof)) return;
    var _assets = array_or(struct_or(_prof, "assets", []));
    var _n = array_length(_assets);
    if (_n == 0) return;
    var _last = struct_or(_A.blip_last_var, _profile, -1);
    var _v = irandom(_n - 1);
    if (_n > 1 && _v == _last) _v = (_v + 1 + irandom(_n - 2)) mod _n;
    _A.blip_last_var[$ _profile] = _v;
    var _id = _assets[_v];
    var _e = _A.ids[$ _id];
    if (is_undefined(_e) || array_length(_e.res) == 0) return;
    var _h = audio_play_sound(_e.res[0], _e.pr, false);
    audio_sound_gain(_h, _e.gain * global.settings.blips, 0);
    audio_sound_pitch(_h, random_range(0.94, 1.06));
    _A.blip_h = _h;
    _A.blip_last = _A.tick;
    _A.blip_stop_at = -1;
}

/// Cancels the active blip with a click-free 5 ms fade.
function aud_blip_cancel() {
    var _A = global.aud;
    if (_A.blip_h >= 0 && audio_is_playing(_A.blip_h)) {
        audio_sound_gain(_A.blip_h, 0, 5);
        _A.blip_stop_at = _A.tick + 1;
    }
}

// ------------------------------------------------------------------ per-tick update
function aud_update(_world_active) {
    var _A = global.aud;
    _A.tick += 1;

    // pending scheduled cues
    var _p = _A.pending;
    for (var i = array_length(_p) - 1; i >= 0; i--) {
        if (_A.tick >= _p[i].at) {
            var _cue = _p[i];
            array_delete(_p, i, 1);
            aud_play(_cue.id, _cue.x, _cue.y);
        }
    }

    // ducking: stronger applicable reduction wins
    var _warn = _A.tick < _A.warn_until;
    var _tm = min(_A.text_duck ? -4 : 0, _warn ? -3 : 0);
    var _tw = min(_A.text_duck ? -8 : 0, _warn ? -6 : 0);
    var _att_ticks = _warn ? 2 : 6;
    var _rel_ticks = _A.text_duck ? 21 : 15;
    if (_A.duck_music_db > _tm) _A.duck_music_db = max(_tm, _A.duck_music_db - 4 / _att_ticks);
    else _A.duck_music_db = min(_tm, _A.duck_music_db + 4 / _rel_ticks);
    if (_A.duck_weather_db > _tw) _A.duck_weather_db = max(_tw, _A.duck_weather_db - 8 / _att_ticks);
    else _A.duck_weather_db = min(_tw, _A.duck_weather_db + 8 / _rel_ticks);

    // world pause: freeze world-owned voices while inventory/pause/dialogue stop the simulation
    if (_world_active == _A.world_paused) {
        _A.world_paused = !_world_active;
        var _aa = _A.active;
        for (var i = 0; i < array_length(_aa); i++) {
            if (!_aa[i].world) continue;
            if (_A.world_paused) audio_pause_sound(_aa[i].h);
            else audio_resume_sound(_aa[i].h);
        }
    }

    // active voices: envelopes, gain, cleanup
    var _a = _A.active;
    for (var i = array_length(_a) - 1; i >= 0; i--) {
        var _r = _a[i];
        if (!audio_is_playing(_r.h)) {
            array_delete(_a, i, 1);
            continue;
        }
        if (_r.env != _r.env_to) _r.env = approach(_r.env, _r.env_to, _r.env_rate);
        if (_r.stop_at_zero && _r.env <= 0) {
            audio_stop_sound(_r.h);
            array_delete(_a, i, 1);
            continue;
        }
        if (_r.owner != "" || _r.env < 1 || _r.grp == "weather") {
            var _att = _r.sp ? aud_atten(_r.x, _r.y) : 1;
            audio_sound_gain(_r.h, _r.base * _r.env * _att * aud_bus_volume(_r.bus) * aud_duck_factor(_r.grp, _r.bus), 0);
        }
    }

    // music
    var _m = _A.mus;
    if (_m.h >= 0) {
        if (!audio_is_playing(_m.h)) {
            _A.mus = { id: "", h: -1, base: 1, env: 0, env_to: 0, env_rate: 0 };
        } else {
            if (_m.env != _m.env_to) _m.env = approach(_m.env, _m.env_to, _m.env_rate);
            audio_sound_gain(_m.h, _m.base * _m.env * global.settings.music * db_to_lin(_A.duck_music_db), 0);
        }
    }
    var _f = _A.music_fading;
    for (var i = array_length(_f) - 1; i >= 0; i--) {
        _f[i].env -= _f[i].rate;
        if (_f[i].env <= 0 || !audio_is_playing(_f[i].h)) {
            audio_stop_sound(_f[i].h);
            array_delete(_f, i, 1);
        } else {
            audio_sound_gain(_f[i].h, _f[i].base * _f[i].env * global.settings.music * db_to_lin(_A.duck_music_db), 0);
        }
    }

    // blip fade-out completion
    if (_A.blip_stop_at >= 0 && _A.tick >= _A.blip_stop_at) {
        if (_A.blip_h >= 0) audio_stop_sound(_A.blip_h);
        _A.blip_h = -1;
        _A.blip_stop_at = -1;
    }
}
