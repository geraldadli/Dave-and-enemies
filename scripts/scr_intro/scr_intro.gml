// scr_intro - the opening cinematic (rm_intro), driven by datafiles/data/intro_storyboard.json.
// Normal playback is 54 s (3240 ticks) including fades. Timing, camera points, Dave's walk and
// every text/audio cue come from the storyboard; finish, final advance and skip share intro_finish.
// Completion enters rm_sc_desert_frontier at cell [7,40] facing east (handoff precedence 2).

function intro_create() {
    sb = global.data.storyboard;
    shots = is_struct(sb) ? sb.shots : [];
    dur = round((is_struct(sb) ? sb.duration_s : 54) * TPS);
    t = 0;
    done = false;
    fired = {};
    tr = undefined;
    tr_line = "";
    tr_start = 0;
    tr_len = 0;
    dave_x = 1040;
    dave_y = 790;
    dave_face = "down";
    dave_moving = false;
    dave_anim = 0;
    prev_x = dave_x;
    banner_t = 0;
    ribbons = [];
    for (var i = 0; i < 90; i++) {
        array_push(ribbons, { x: random(1400), y: random(760), l: random_range(20, 70), s: random_range(4, 9), a: random_range(0.08, 0.2) });
    }
    view_enabled = true;
    view_visible[0] = true;
    camera_set_view_size(view_camera[0], GUI_W, GUI_H);
    global.mode = MODE.CINEMA;
    global.fade_black = 1;
    var _self = id;
    cine_begin({
        skip_allowed: true,
        on_skip: method(_self, function() { intro_finish(true); }),
        on_advance: method(_self, intro_advance),
        draw: method(_self, intro_draw_gui)
    });
    intro_update_camera();
}

function intro_shot_index(_tick) {
    var _s = _tick / TPS;
    for (var i = array_length(shots) - 1; i >= 0; i--) {
        if (_s >= shots[i].start_s) return i;
    }
    return 0;
}

function intro_update_camera() {
    if (array_length(shots) == 0) return;
    var _i = intro_shot_index(t);
    var _sh = shots[_i];
    var _p = smoothstep01((t / TPS - _sh.start_s) / max(0.001, _sh.duration_s));
    var _cx = lerp(_sh.camera.from_px[0], _sh.camera.to_px[0], _p);
    var _cy = lerp(_sh.camera.from_px[1], _sh.camera.to_px[1], _p);
    var _vx = clamp(_cx - GUI_W / 2, 0, room_width - GUI_W);
    var _vy = clamp(_cy - GUI_H / 2, 0, room_height - GUI_H);
    camera_set_view_pos(view_camera[0], round(_vx), round(_vy));
    global.cam_cx = _vx + GUI_W / 2;
    global.cam_cy = _vy + GUI_H / 2;
}

/// Dave's authored blocking: idle before 43 s, 0.5 s turn, then walks east (1040 -> 1232 -> 1536).
function intro_update_dave() {
    var _s = t / TPS;
    prev_x = dave_x;
    dave_moving = false;
    if (_s < 43) {
        dave_x = 1040;
        dave_face = "down";
    } else if (_s < 43.5) {
        dave_x = 1040;
        dave_face = (_s < 43.25) ? "down" : "side";   // down_side art not delivered: down -> side
    } else if (_s < 49) {
        dave_x = lerp(1040, 1232, (_s - 43.5) / 5.5);
        dave_face = "side";
        dave_moving = true;
    } else {
        dave_x = lerp(1232, 1536, clamp((_s - 49) / 5, 0, 1));
        dave_face = "side";
        dave_moving = true;
    }
    var _px_tick = abs(dave_x - prev_x);
    if (dave_moving && _px_tick > 0) {
        // stride matched to ground speed; footsteps only on real contacts while step events are active
        var _prev = floor(dave_anim);
        dave_anim += 20 / TPS * (_px_tick / DAVE_SPEED);
        if (dave_anim >= 10) dave_anim -= 10;
        var _cur = floor(dave_anim);
        var _steps_on = (_s >= 43.5 && _s < 49) || (_s >= 49 && _s < 53);
        if (_cur != _prev && (_cur == 2 || _cur == 7) && _steps_on) aud_play("snd_step_sand", undefined, undefined, "", false);
    } else if (!dave_moving) {
        dave_anim += 10 / TPS;
    }
}

function intro_fire_cues(_execute) {
    var _s = t / TPS;
    for (var i = 0; i < array_length(shots); i++) {
        var _sh = shots[i];
        var _ac = _sh.audio_cues;
        for (var k = 0; k < array_length(_ac); k++) {
            var _key = _sh.id + ":a" + string(k);
            if (struct_or(fired, _key, false)) continue;
            if (_s >= _sh.start_s + _ac[k].offset_s) {
                fired[$ _key] = true;
                if (_execute) cine_audio_cue(_ac[k], "intro");
            }
        }
        var _tc = _sh.text_cues;
        for (var j = 0; j < array_length(_tc); j++) {
            var _tkey = _sh.id + ":t" + string(j);
            if (struct_or(fired, _tkey, false)) continue;
            if (_s >= _sh.start_s + _tc[j].offset_s) {
                fired[$ _tkey] = true;
                if (_execute) {
                    var _line = dialogue_line_by_id(_tc[j].line_id);
                    if (is_struct(_line)) {
                        aud_blip_cancel();
                        tr = textrun_create(_line, "dialogue", (_line.speaker == "narrator") ? CAPTION_W_NARR : CAPTION_W_SPEAKER);
                        tr_line = _tc[j].line_id;
                        tr_start = t;
                        tr_len = round(_tc[j].duration_s * TPS);
                        global.aud.text_duck = true;
                    }
                }
            }
        }
    }
}

function intro_step() {
    if (done) exit;
    t += 1;
    banner_t += 1;
    intro_fire_cues(true);
    if (is_struct(tr)) {
        textrun_step(tr);
        if (t - tr_start >= tr_len) {
            aud_blip_cancel();
            tr = undefined;
            global.aud.text_duck = false;
        }
    }
    intro_update_dave();
    intro_update_camera();
    // fades from the storyboard: 1 s fade from black; fade to black from 53 s (shot 8 local 4 s)
    var _s = t / TPS;
    if (_s < 1) global.fade_black = 1 - _s;
    else if (_s >= 53) global.fade_black = clamp(_s - 53, 0, 1);
    else global.fade_black = 0;
    if (t >= dur) intro_finish(false);
}

/// cutscene_advance: reveal the current text, else jump to the next shot (no cue burst).
function intro_advance() {
    if (done) return;
    if (is_struct(tr) && !textrun_page_done(tr)) {
        textrun_reveal(tr);
        return;
    }
    var _i = intro_shot_index(t);
    if (_i + 1 >= array_length(shots)) {
        intro_finish(false);
        return;
    }
    aud_blip_cancel();
    tr = undefined;
    global.aud.text_duck = false;
    t = round(shots[_i + 1].start_s * TPS);
    intro_fire_cues(false);   // passed cues are marked, not executed in a burst
    t -= 1;
    intro_fire_cues_text_only_current();
    if (mus_current() == "mus_intro") audio_sound_set_track_position(global.aud.mus.h, (t + 1) / TPS);
}

/// After a jump, the new shot's own cues (at its start) fire normally on the next step.
function intro_fire_cues_text_only_current() {
    var _i = intro_shot_index(t + 1);
    var _sh = shots[_i];
    var _ac = _sh.audio_cues;
    for (var k = 0; k < array_length(_ac); k++) {
        if (_ac[k].offset_s <= 0.0001) variable_struct_remove(fired, _sh.id + ":a" + string(k));
    }
    var _tc = _sh.text_cues;
    for (var j = 0; j < array_length(_tc); j++) variable_struct_remove(fired, _sh.id + ":t" + string(j));
}

/// intro_complete: one idempotent routine for normal end, final advance and skip.
function intro_finish(_skipped) {
    if (done) return;
    done = true;
    aud_cancel_pending("intro");
    aud_blip_cancel();
    global.aud.text_duck = false;
    tr = undefined;
    if (mus_current() == "mus_intro") mus_stop(300);   // abandoned intro score fades over 300 ms
    // wind transfers to exploration (same owned loop); the scene manager keeps or fades it
    flag_set("intro_seen", true);
    flag_set("boss_pharaoh_defeated", false);
    flag_set("grail_recovered", false);
    cine_end();
    var _start = cfg("initial", { room: "rm_sc_desert_frontier", cell: [7, 40], facing: "side" });
    global.run.scene_room = _start.room;
    global.run.pos_x = cell_px(_start.cell[0]);
    global.run.pos_y = cell_px(_start.cell[1]);
    global.run.facing = _start.facing;
    global.run.location = "Desert Arrival";
    global.after_arrival = "intro";
    if (_skipped) global.fade_black = 0;
    scene_go(_start.room, global.run.pos_x, global.run.pos_y, _start.facing, "intro");
}

function intro_cleanup() {
    if (!done) {
        aud_blip_cancel();
        global.aud.text_duck = false;
    }
}

// ------------------------------------------------------------------ drawing
function intro_draw_world() {
    var _vx = camera_get_view_x(view_camera[0]);
    var _vy = camera_get_view_y(view_camera[0]);
    // sky and sand (placeholder backdrop until spr_intro_sky / spr_intro_wall are delivered)
    draw_rectangle_colour(0, 0, room_width, 420, make_colour_rgb(222, 170, 120), make_colour_rgb(222, 170, 120),
        make_colour_rgb(242, 210, 160), make_colour_rgb(242, 210, 160), false);
    draw_set_colour(make_colour_rgb(214, 182, 132));
    draw_rectangle(0, 420, room_width, room_height, false);
    var _wall = asset_or("spr_intro_wall", spr_ph_intro_wall);
    draw_sprite(_wall, 0, 0, 0);
    // torn banner pulled west by the wind
    var _bx = 720;
    var _by = 540;
    draw_set_colour(make_colour_rgb(70, 52, 40));
    draw_line_width(_bx, _by, _bx, _by + 200, 5);
    var _b = asset_or("spr_intro_banner", -1);
    if (_b >= 0) draw_sprite(_b, (banner_t div 6) mod sprite_get_number(_b), _bx, _by);
    else {
        draw_set_colour(make_colour_rgb(150, 40, 46));
        for (var i = 0; i < 8; i++) {
            var _w0 = sin(banner_t / 9 + i * 0.7) * 6;
            var _w1 = sin(banner_t / 9 + (i + 1) * 0.7) * 6;
            draw_triangle(_bx - i * 12, _by + 8 + _w0, _bx - (i + 1) * 12, _by + 8 + _w1, _bx - i * 12, _by + 70 + _w0 - i * 4, false);
            draw_triangle(_bx - (i + 1) * 12, _by + 8 + _w1, _bx - (i + 1) * 12, _by + 66 + _w1 - i * 4, _bx - i * 12, _by + 70 + _w0 - i * 4, false);
        }
    }
    // rubble and fallen comrades (motionless; respectful placeholders, no gore)
    var _rub = asset_or("spr_intro_rubble_01", spr_ph_intro_rubble);
    draw_sprite(_rub, 0, 820, 700);
    draw_sprite(_rub, 1, 1150, 690);
    draw_sprite(_rub, 2, 600, 760);
    draw_sprite(_rub, 3, 1320, 760);
    var _fal = asset_or("spr_intro_fallen_01", spr_ph_intro_fallen);
    draw_sprite(_fal, 0, 860, 930);
    draw_sprite(_fal, 1, 1010, 980);
    draw_sprite(_fal, 2, 1180, 925);
    // spears planted in the sand
    draw_set_colour(make_colour_rgb(84, 64, 46));
    draw_line_width(930, 960, 960, 870, 3);
    draw_line_width(1130, 990, 1110, 905, 3);
    // Dave: authored cardinal art at native scale
    draw_set_alpha(0.3);
    draw_ellipse_colour(dave_x - 20, dave_y - 6, dave_x + 20, dave_y + 6, c_black, c_black, false);
    draw_set_alpha(1);
    var _spr;
    if (dave_moving) _spr = spr_dave_walk_side;
    else _spr = (dave_face == "side") ? spr_dave_base_side : spr_dave_idle_down;
    draw_sprite(_spr, floor(dave_anim) mod sprite_get_number(_spr), dave_x, dave_y);
    // sand ribbons drift east to west across the view
    draw_set_colour(make_colour_rgb(240, 222, 180));
    for (var r = 0; r < array_length(ribbons); r++) {
        var _rb = ribbons[r];
        _rb.x -= _rb.s;
        if (_rb.x < -80) {
            _rb.x = 1360 + random(60);
            _rb.y = random(760);
        }
        draw_set_alpha(_rb.a);
        draw_line_width(_vx + _rb.x, _vy + _rb.y, _vx + _rb.x + _rb.l, _vy + _rb.y - 2, 2);
    }
    draw_set_alpha(1);
}

function intro_draw_gui() {
    if (is_struct(tr)) {
        var _lt = t - tr_start;
        var _a = clamp(min(_lt / 15, (tr_len - _lt) / 15), 0, 1);
        cine_draw_text(tr, _a);
    }
    cine_draw_skip_hint();
}
