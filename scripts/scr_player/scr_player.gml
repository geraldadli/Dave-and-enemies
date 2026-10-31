// scr_player - Dave (obj_player): 8-direction movement, authored cardinal art, data-timed attack.
// Direction mapping (handoff section 4): east 0 -> spr_dave_*_side, north 2 -> *_up,
// west 4 -> *_left (independently authored, never mirrored), south 6 -> *_down; image_xscale = 1.
// Diagonals keep the horizontal facing until diagonal art exists (documented fallback).

function player_setup() {
    state = "normal";
    facing = "side";
    moving = false;
    anim_t = 0;
    atk_t = 0;
    atk_frame = 0;
    atk_dir = 0;
    atk_queued = false;
    atk_ticks = cfg("dave_attack_ticks", [3, 3, 3, 3, 3, 4, 4, 4]);
    atk_active = cfg("dave_attack_active", [2, 4]);
    atk_total = 0;
    for (var i = 0; i < array_length(atk_ticks); i++) atk_total += atk_ticks[i];
    swing_id = 0;
    iframes = 0;
    hurt_t = 0;
    kb_x = 0;
    kb_y = 0;
    scripted = false;
    script_tx = x;
    script_ty = y;
    script_face = "down";
    flash_heal = 0;
    death_t = 0;
    sort_depth = true;
    mask_index = spr_mask_dave;
}

function player_sprite_walk(_f) {
    switch (_f) {
        case "side": return spr_dave_walk_side;
        case "left": return spr_dave_walk_left;
        case "up": return spr_dave_walk_up;
        default: return spr_dave_walk_down;
    }
}

function player_sprite_attack(_f) {
    switch (_f) {
        case "side": return spr_dave_attack_side;
        case "left": return spr_dave_attack_left;
        case "up": return spr_dave_attack_up;
        default: return spr_dave_attack_down;
    }
}

/// Idle: authored down idle; other facings hold their delivered reference base (placeholder).
function player_sprite_idle(_f) {
    switch (_f) {
        case "side": return spr_dave_base_side;
        case "left": return spr_dave_base_left;
        case "up": return spr_dave_base_up;
        default: return spr_dave_idle_down;
    }
}

/// World-space mouse position through the shared GUI transform (GUI plane == camera view size).
function player_mouse_world() {
    var _cam = view_camera[0];
    return [camera_get_view_x(_cam) + global.inp.mx, camera_get_view_y(_cam) + global.inp.my];
}

function player_attack_frame(_t) {
    var _acc = 0;
    for (var i = 0; i < array_length(atk_ticks); i++) {
        _acc += atk_ticks[i];
        if (_t < _acc) return i;
    }
    return array_length(atk_ticks) - 1;
}

function player_start_attack() {
    var _m = player_mouse_world();
    atk_dir = point_direction(x, y - 30, _m[0], _m[1]);
    facing = facing_from_angle(atk_dir);
    state = "attack";
    atk_t = 0;
    atk_frame = 0;
    atk_queued = false;
    global.swing_counter += 1;
    swing_id = global.swing_counter;
}

function player_footstep() {
    var _s = world_surface(x, y);
    var _id = "snd_step_sand";
    if (_s == "stone") _id = "snd_step_stone";
    else if (_s == "wood") _id = "snd_step_wood";
    aud_play(_id, x, y, "", false);   // Dave's own cues stay audible during scripted walks
}

/// Advances the walk cycle; footsteps fire only on actual moving contacts at frames 2 and 7.
function player_walk_anim(_speed_scale) {
    var _prev = floor(anim_t);
    anim_t += 20 / TPS * _speed_scale;
    var _n = sprite_get_number(player_sprite_walk(facing));
    if (anim_t >= _n) anim_t -= _n;
    var _cur = floor(anim_t);
    if (_cur != _prev && (_cur == 2 || _cur == 7)) player_footstep();
}

function player_sword_hits() {
    var _reach = player_weapon_stat("reach", 76);
    var _arc = player_weapon_stat("arc_deg", 120);
    var _dmg = player_attack();
    var _ox = x;
    var _oy = y - 30;
    var _dir = atk_dir;
    var _sid = swing_id;
    with (obj_enemy_parent) {
        if (!variable_instance_exists(id, "hurt_r") || state == "dead") continue;
        var _ex = x;
        var _ey = y - hurt_cy - (variable_instance_exists(id, "flying") && flying ? 30 : 0);
        var _d = point_distance(_ox, _oy, _ex, _ey);
        if (_d > _reach + hurt_r) continue;
        var _diff = abs(angle_difference(_dir, point_direction(_ox, _oy, _ex, _ey)));
        if (_d > hurt_r + 16 && _diff > _arc / 2) continue;
        if (enemy_take_hit(_dmg, _sid, _ox, _oy)) {
            aud_play("snd_sword_hit", _ex, _ey);
            var _mat = struct_or(def, "material", "");
            if (_mat == "bone") aud_play("snd_sword_hit_bone", _ex, _ey);
            else if (_mat == "armor") aud_play("snd_sword_hit_armor", _ex, _ey);
            shake_camera(2, 4);
        }
    }
}

function player_interact() {
    var _best = noone;
    var _bd = 84;
    var _px = x;
    var _py = y;
    with (obj_chest) {
        var _d = point_distance(_px, _py, x, y + 40);
        if (!opened_empty && _d < _bd) { _bd = _d; _best = id; }
    }
    with (obj_checkpoint) {
        var _d2 = point_distance(_px, _py, x, y);
        if (_d2 < _bd) { _bd = _d2; _best = id; }
    }
    with (obj_spring) {
        if (rect_has_px(rect, _px, _py)) { _bd = 0; _best = id; }
    }
    with (obj_pickup) {
        var _d3 = point_distance(_px, _py, x, y);
        if (_d3 < _bd) { _bd = _d3; _best = id; }
    }
    if (_best == noone) {
        // explicit attempt on the sealed route: locked feedback once per accepted interaction
        var _sealed = false;
        with (obj_gate) {
            var _gx = (rect[0] + rect[2] + 1) * TILE / 2;
            var _gy = (rect[1] + rect[3] + 1) * TILE / 2;
            if (closed && point_distance(_px, _py, _gx, _gy) < 150) _sealed = true;
        }
        if (_sealed) {
            aud_play("snd_chest_locked", _px, _py, "", false);
            toast_show("The way is sealed.");
        }
        return;
    }
    with (_best) event_user(0);
}

function player_step() {
    if (iframes > 0 && world_active()) iframes -= 1;
    if (flash_heal > 0) flash_heal -= 1;
    if (state == "dead") {
        death_t += 1;
        if (death_t == ms_ticks(250)) mus_play("mus_gameover");
        if (death_t == 80 && global.mode == MODE.PLAY) game_over_begin();   // once per death
        exit;
    }
    // scripted movement (boss entry, ending) runs while gameplay input is locked
    if (scripted) {
        var _d = point_distance(x, y, script_tx, script_ty);
        if (_d <= 3) {
            x = script_tx;
            y = script_ty;
            facing = script_face;
            moving = false;
            anim_t = 0;
            scripted = false;
        } else {
            var _a = point_direction(x, y, script_tx, script_ty);
            facing = facing_from_angle(_a);
            var _spd = min(_d, DAVE_SPEED * 0.75);
            x += lengthdir_x(_spd, _a);
            y += lengthdir_y(_spd, _a);
            moving = true;
            player_walk_anim(0.75);
        }
        exit;
    }
    if (!world_active()) exit;
    if (abs(kb_x) + abs(kb_y) > 0.2) {
        actor_move(kb_x, kb_y);
        kb_x *= 0.7;
        kb_y *= 0.7;
    }
    if (hurt_t > 0) hurt_t -= 1;
    var _input = game_input_ok();
    if (state == "attack") {
        var _prev = atk_frame;
        atk_t += 1;
        atk_frame = player_attack_frame(atk_t);
        if (_prev < atk_active[0] && atk_frame >= atk_active[0]) {
            // swing cue fires once, on entering active frame 2
            aud_play("snd_sword_swing", x, y, "", false);
            instance_create_depth(x, y - 30, depth - 1, obj_fx, { kind: "slash", dir: atk_dir, owner: id,
                life: atk_ticks[2] + atk_ticks[3] + atk_ticks[4] });
        }
        if (atk_frame >= atk_active[0] && atk_frame <= atk_active[1]) player_sword_hits();
        if (_input && inp_pressed("lmb") && atk_frame >= atk_active[1] + 1) {
            inp_consume("lmb");
            atk_queued = true;
        }
        if (atk_t >= atk_total) {
            state = "normal";
            anim_t = 0;
            if (atk_queued && _input) player_start_attack();
        }
        exit;
    }
    // movement
    var _mx = 0;
    var _my = 0;
    if (_input) {
        _mx = (inp_down("right") ? 1 : 0) - (inp_down("left") ? 1 : 0);
        _my = (inp_down("down") ? 1 : 0) - (inp_down("up") ? 1 : 0);
    }
    moving = (_mx != 0 || _my != 0);
    if (moving) {
        var _ang = point_direction(0, 0, _mx, _my);
        facing = facing_from_index(dir8(_ang));
        var _moved = actor_move(lengthdir_x(DAVE_SPEED, _ang), lengthdir_y(DAVE_SPEED, _ang));
        if (_moved > 0.5) player_walk_anim(_moved / DAVE_SPEED);
        else moving = false;
    }
    if (!moving) {
        if (facing == "down") anim_t += 10 / TPS;
        else anim_t = 0;
    }
    if (!_input) exit;
    if (inp_pressed("lmb")) {
        inp_consume("lmb");
        player_start_attack();
        exit;
    }
    if (inp_pressed("interact")) {
        inp_consume("interact");
        player_interact();
    }
}

function player_die() {
    if (state == "dead") return;
    state = "dead";
    death_t = 0;
    scripted = false;
    moving = false;
    iframes = 0;
    aud_loops_stop_prefix("boss:", 100);
    if (mus_current() != "") mus_stop(250);
    global.boss_ui.visible = false;
}

function player_script_walk(_tx, _ty, _face) {
    scripted = true;
    script_tx = _tx;
    script_ty = _ty;
    script_face = _face;
    state = "normal";
}

function player_script_stop() {
    scripted = false;
    moving = false;
    anim_t = 0;
    if (state == "attack") state = "normal";
}

function player_draw() {
    var _spr, _img;
    // shared soft ground shadow (contract: no baked shadows)
    draw_set_alpha(0.3);
    draw_ellipse_colour(x - 20, y - 6, x + 20, y + 6, c_black, c_black, false);
    draw_set_alpha(1);
    if (flash_heal > 0) {
        var _r = 30 + (30 - flash_heal);
        draw_set_alpha(flash_heal / 30 * 0.6);
        draw_ellipse_colour(x - _r, y - _r * 0.35, x + _r, y + _r * 0.35, C_HEALTH, C_HEALTH, true);
        draw_ellipse_colour(x - _r + 3, y - _r * 0.35 + 1, x + _r - 3, y + _r * 0.35 - 1, C_HEALTH, C_HEALTH, true);
        draw_set_alpha(1);
    }
    if (state == "attack") {
        _spr = player_sprite_attack(facing);
        _img = atk_frame;
    } else if (moving) {
        _spr = player_sprite_walk(facing);
        _img = floor(anim_t) mod sprite_get_number(_spr);
    } else {
        _spr = player_sprite_idle(facing);
        _img = floor(anim_t) mod sprite_get_number(_spr);
    }
    var _alpha = 1;
    var _col = c_white;
    var _dy = 0;
    if (state == "dead") {
        // placeholder death presentation until spr_dave_death is delivered
        _spr = player_sprite_idle(facing);
        _img = 0;
        _col = merge_colour(c_white, C_HEALTH, min(1, death_t / 20));
        _alpha = clamp(1.4 - death_t / 60, 0, 1);
        _dy = min(death_t, 30) * 0.4;
    } else if (iframes > 0 && (iframes div 4) mod 2 == 0) {
        _alpha = 0.55;
    }
    draw_sprite_ext(_spr, _img, x, y + _dy, 1, 1, 0, _col, _alpha);
    if (hurt_t > 0) {
        gpu_set_fog(true, c_white, 0, 1);
        draw_sprite_ext(_spr, _img, x, y + _dy, 1, 1, 0, c_white, 0.5);
        gpu_set_fog(false, c_white, 0, 0);
    }
}
