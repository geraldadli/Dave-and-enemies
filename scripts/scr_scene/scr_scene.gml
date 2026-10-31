// scr_scene - per-room manager (obj_manager), scene passes, barriers, weather and world drawing
// of interactables. One manager per scene room; crossing places or chunks never reloads anything.

function scene_manager_create() {
    depth = -11000;
    var _rn = room_get_name(room);
    scene = scene_data(_rn);
    global.scene = scene;
    weather_k = 0;
    wind_on = is_struct(global.aud.loops[$ "weather"]);   // a bed carried over from the previous scene
    tumble_t = irandom_range(120, 300);
    streaks = [];
    for (var i = 0; i < 70; i++) {
        array_push(streaks, { x: random(1400), y: random(780), l: random_range(18, 60), s: random_range(5, 11), a: random_range(0.08, 0.22) });
    }
    if (!is_struct(scene)) exit;   // template rooms keep their own content
    view_enabled = true;
    view_visible[0] = true;
    camera_set_view_size(view_camera[0], GUI_W, GUI_H);
    world_build(scene);
    scene_spawn_all(scene);
    var _arr = global.pending_arrival;
    var _px = global.run.pos_x;
    var _py = global.run.pos_y;
    var _f = global.run.facing;
    if (is_struct(_arr)) {
        _px = _arr.x;
        _py = _arr.y;
        _f = _arr.facing;
        global.pending_arrival = undefined;
    }
    with (obj_player) instance_destroy();
    var _p = instance_create_depth(_px, _py, 0, obj_player);
    _p.facing = _f;
    global.run.scene_room = _rn;
    global.run.pos_x = _px;
    global.run.pos_y = _py;
    if (global.mode == MODE.CINEMA) global.mode = MODE.PLAY;
    global.toast.prompt = "";
    global.cam_target = undefined;
    cam_x = clamp(_px - GUI_W / 2, 0, room_width - GUI_W);
    cam_y = clamp(_py - GUI_H / 2, 0, room_height - GUI_H);
    camera_set_view_pos(view_camera[0], cam_x, cam_y);
    global.cam_cx = cam_x + GUI_W / 2;
    global.cam_cy = cam_y + GUI_H / 2;
    mus_play(scene.music);   // idempotent: desert music keeps playing across scene passes
    scene_arrival_ready();
}

function scene_weather_target() {
    if (!is_struct(scene) || !instance_exists(obj_player)) return 0;
    var _w = scene.weather;
    if (!struct_or(_w, "sandstorm", false)) return 0;
    var _cx = px_cell(obj_player.x);
    var _cy = px_cell(obj_player.y);
    var _sup = array_or(struct_or(_w, "suppress", []));
    for (var i = 0; i < array_length(_sup); i++) if (rect_has_cell(_sup[i], _cx, _cy)) return 0;
    return 1;
}

function scene_manager_step() {
    if (!is_struct(scene)) exit;
    var _target = scene_weather_target();
    if (global.boss_ui.visible || global.cine_lock) _target = 0;
    weather_k = approach(weather_k, _target, 1 / 90);
    // one owned weather bed with hysteresis; never restarted per step
    if (weather_k > 0.6 && !wind_on) {
        wind_on = true;
        aud_loop("snd_wind_loop", "weather", undefined, undefined, false);
    } else if (weather_k < 0.2 && wind_on) {
        wind_on = false;
        aud_loop_stop("weather", -1);
    }
    if (!world_active()) exit;
    // scripted places
    if (instance_exists(obj_player)) {
        var _p = obj_player;
        var _discoveries = array_or(struct_or(scene, "discoveries", []));
        for (var d = 0; d < array_length(_discoveries); d++) {
            var _discovery = _discoveries[d];
            var _discovery_flag = "discovery_" + _discovery.id;
            if (!flag(_discovery_flag) && rect_has_px(_discovery.rect, _p.x, _p.y)) {
                flag_set(_discovery_flag, true);
                toast_show("Discovered: " + _discovery.name, 150, C_GOLD);
                break;
            }
        }
        var _sc = array_or(scene.scripts);
        for (var i = 0; i < array_length(_sc); i++) {
            var _s = _sc[i];
            if (_s.event == "chapter_start" && !flag("desert_arrival_seen") && rect_has_px(_s.rect, _p.x, _p.y)) {
                flag_set("desert_arrival_seen", true);
            }
        }
    }
    // tumbleweeds: at most two nearby, east-to-west, expire within ten seconds
    if (struct_or(scene.weather, "tumbleweeds", false) && weather_k > 0.5) {
        tumble_t -= 1;
        if (tumble_t <= 0) {
            tumble_t = irandom_range(240, 480);
            if (instance_number(obj_tumbleweed) < 2) {
                var _ty = global.cam_cy + random_range(-250, 250);
                var _tx = global.cam_cx + 700;
                if (world_walkable_px(_tx - 200, _ty)) instance_create_depth(_tx, _ty, -_ty, obj_tumbleweed);
            }
        }
    }
}

function scene_manager_camera() {
    if (!is_struct(scene)) exit;
    var _tx = cam_x + GUI_W / 2;
    var _ty = cam_y + GUI_H / 2;
    if (is_struct(global.cam_target)) {
        _tx = global.cam_target.x;
        _ty = global.cam_target.y;
    } else if (instance_exists(obj_player)) {
        _tx = obj_player.x;
        _ty = obj_player.y - 24;
        // boss combat: frame Dave and the Pharaoh together (attacking actors stay visible),
        // weighted toward Dave and never pushing him out of the view margin
        if (global.boss_ui.visible && instance_exists(obj_pharaoh)) {
            var _bx = obj_pharaoh.x;
            var _by = obj_pharaoh.y - 150;   // keep his headdress clear of the boss bar
            _tx = clamp(lerp(_tx, _bx, 0.45), obj_player.x - 520, obj_player.x + 520);
            _ty = clamp(lerp(_ty, _by, 0.45), obj_player.y - 24 - 250, obj_player.y - 24 + 250);
        }
    }
    var _k = is_struct(global.cam_target) ? 0.06 : 0.2;
    var _cx = lerp(cam_x + GUI_W / 2, _tx, _k);
    var _cy = lerp(cam_y + GUI_H / 2, _ty, _k);
    cam_x = clamp(_cx - GUI_W / 2, 0, room_width - GUI_W);
    cam_y = clamp(_cy - GUI_H / 2, 0, room_height - GUI_H);
    var _sx = 0;
    var _sy = 0;
    if (global.cam_shake_t > 0 && global.settings.shake) {
        _sx = random_range(-global.cam_shake_amp, global.cam_shake_amp);
        _sy = random_range(-global.cam_shake_amp, global.cam_shake_amp);
    }
    camera_set_view_pos(view_camera[0], round(cam_x + _sx), round(cam_y + _sy));
    global.cam_cx = cam_x + GUI_W / 2;
    global.cam_cy = cam_y + GUI_H / 2;
    if (instance_exists(obj_player)) {
        global.run.pos_x = obj_player.x;
        global.run.pos_y = obj_player.y;
        global.run.facing = obj_player.facing;
    }
}

/// Cosmetic east-to-west sand ribbons in view space (never affects movement or collision).
function scene_manager_draw_weather() {
    if (!is_struct(scene) || weather_k <= 0.01) exit;
    var _vx = camera_get_view_x(view_camera[0]);
    var _vy = camera_get_view_y(view_camera[0]);
    var _run = world_active();
    draw_set_colour(make_colour_rgb(236, 214, 170));
    for (var i = 0; i < array_length(streaks); i++) {
        var _s = streaks[i];
        if (_run) {
            _s.x -= _s.s;
            _s.y += _s.s * 0.08;
            if (_s.x < -80) {
                _s.x = 1360 + random(80);
                _s.y = random(760) - 20;
            }
        }
        draw_set_alpha(_s.a * weather_k);
        draw_line_width(_vx + _s.x, _vy + _s.y, _vx + _s.x + _s.l, _vy + _s.y - _s.l * 0.08, 2);
    }
    draw_set_alpha(1);
}

// ------------------------------------------------------------------ scene passes
function exit_step() {
    if (!instance_exists(obj_player) || !world_active() || global.cine_lock) exit;
    var _e = exit_data;
    var _p = obj_player;
    var _cx = px_cell(_p.x);
    var _cy = px_cell(_p.y);
    var _out_key = (_e.side == "E") ? "right" : "left";
    if (!armed) {
        // debounce: arm only after Dave leaves the arrival corridor and releases outward intent
        if (!rect_has_cell(_e.corridor, _cx, _cy) && !global.inp.down[$ _out_key]) armed = true;
        exit;
    }
    if (_cy < _e.rows[0] || _cy > _e.rows[1]) exit;
    var _crossing = (_e.side == "E") ? (_p.x >= room_width - 24) : (_p.x <= 24);
    if (_crossing && inp_down(_out_key)) {
        armed = false;
        scene_go(_e.to_room, cell_px(_e.to_cell[0]), cell_px(_e.to_cell[1]), _e.to_facing, "pass");
    }
}

// ------------------------------------------------------------------ barriers
function gate_apply() {
    world_set_barrier(rect, closed);
}

function gate_close_animated(_g) {
    with (_g) {
        if (closed || anim_dir != 0) break;
        anim_dir = 1;
        anim = 0;
        aud_play("snd_gate_slam", undefined, undefined, "", false);   // slam contact ~0.495 s = 30 ticks
    }
}

function gate_step() {
    if (anim_dir == 0) exit;
    anim = clamp(anim + anim_dir / 30, 0, 1);
    if (anim >= 1 && anim_dir > 0) {
        anim_dir = 0;
        closed = true;
        gate_apply();
        shake_camera(3, 8);
    } else if (anim <= 0 && anim_dir < 0) {
        anim_dir = 0;
        closed = false;
        gate_apply();
    }
}

/// Placeholder drawing for spr_gate_arena / spr_door_sealed until their art is delivered.
function gate_draw() {
    var _x1 = rect[0] * TILE;
    var _x2 = (rect[2] + 1) * TILE;
    var _y1 = rect[1] * TILE;
    var _y2 = (rect[3] + 1) * TILE;
    if (kind == "arena") {
        var _spr = asset_or("spr_gate_arena", -1);
        if (_spr >= 0) {
            draw_sprite(_spr, floor(anim * (sprite_get_number(_spr) - 1)), (_x1 + _x2) / 2, _y2);
            exit;
        }
        var _h = 112 * anim;
        draw_set_colour(make_colour_rgb(58, 48, 44));
        draw_rectangle(_x1 - 8, _y2 - 120, _x1 + 4, _y2, false);
        draw_rectangle(_x2 - 4, _y2 - 120, _x2 + 8, _y2, false);
        draw_rectangle(_x1 - 8, _y2 - 126, _x2 + 8, _y2 - 112, false);
        if (_h > 2) {
            draw_set_colour(make_colour_rgb(70, 66, 74));
            for (var bx = _x1 + 10; bx < _x2 - 4; bx += 16) draw_rectangle(bx, _y2 - 112, bx + 6, _y2 - 112 + _h, false);
            draw_rectangle(_x1, _y2 - 112 + _h * 0.45, _x2, _y2 - 112 + _h * 0.45 + 6, false);
            draw_set_colour(make_colour_rgb(30, 26, 28));
            draw_rectangle(_x1, _y2 - 116 + _h, _x2, _y2 - 110 + _h, false);
        }
    } else {
        var _spr2 = asset_or("spr_door_sealed", -1);
        if (_spr2 >= 0) {
            if (closed) draw_sprite(_spr2, 0, (_x1 + _x2) / 2, _y2);
            exit;
        }
        if (!closed) exit;
        draw_set_colour(make_colour_rgb(96, 84, 74));
        draw_rectangle(_x1, _y1 - 48, _x2, _y2, false);
        draw_set_colour(make_colour_rgb(60, 52, 48));
        for (var by = _y1 - 48; by < _y2; by += 32) draw_line(_x1, by, _x2, by);
        draw_set_alpha(0.35 + 0.15 * sin(current_time / 300));
        draw_set_colour(C_BOSS);
        draw_rectangle(_x1 + 6, _y1 - 40, _x2 - 6, _y2 - 8, true);
        draw_set_alpha(1);
    }
}

// Tall foreground art must not conceal a moving player or an enemy telegraph.
// Collision stays at the prop's base; only its drawing becomes translucent.
function scenery_covers_actor(_actor, _front_y, _left, _top, _right, _bottom) {
    if (!instance_exists(_actor) || _actor.y >= _front_y) return false;
    return _actor.x + 30 > _left && _actor.x - 30 < _right
        && _actor.y - 8 > _top && _actor.y - 96 < _bottom;
}

function scenery_draw(_sprite, _flat) {
    if (_sprite < 0) return;
    var _alpha = 1;
    if (!_flat) {
        var _left = x + sprite_get_bbox_left(_sprite) - sprite_get_xoffset(_sprite);
        var _top = y + sprite_get_bbox_top(_sprite) - sprite_get_yoffset(_sprite);
        var _right = x + sprite_get_bbox_right(_sprite) - sprite_get_xoffset(_sprite);
        var _bottom = y + sprite_get_bbox_bottom(_sprite) - sprite_get_yoffset(_sprite);
        var _front_y = y;
        if (instance_exists(obj_player) && scenery_covers_actor(obj_player, _front_y, _left, _top, _right, _bottom)) _alpha = 0.25;
        if (_alpha == 1) {
            with (obj_enemy) {
                if (hp > 0 && state != "hidden" && scenery_covers_actor(id, _front_y, _left, _top, _right, _bottom)) _alpha = 0.25;
            }
        }
        if (_alpha == 1) {
            with (obj_pharaoh) {
                if (hp > 0 && scenery_covers_actor(id, _front_y, _left, _top, _right, _bottom)) _alpha = 0.25;
            }
        }
    }
    draw_sprite_ext(_sprite, 0, x, y, 1, 1, 0, c_white, _alpha);
}

// ------------------------------------------------------------------ interactable drawing
function chest_draw() {
    draw_set_alpha(0.25);
    draw_ellipse_colour(x - 22, y - 6, x + 22, y + 6, c_black, c_black, false);
    draw_set_alpha(1);
    var _d = asset_or("spr_chest_desert", -1);
    if (_d >= 0) {
        var _n = sprite_get_number(_d);
        draw_sprite(_d, opened ? clamp(floor(lid * (_n - 1)), 0, _n - 1) : 0, x, y);
    } else {
        // template chest placeholder (A7 temp): scaled to the contract's 64 px class
        if (opened && lid >= 0.5) draw_sprite_ext(spr_chest_open, 0, x, y - 10, 1.6, 1.6, 0, c_white, 1);
        else draw_sprite_ext(spr_chest, 0, x, y - 10, 1.6, 1.6, 0, c_white, 1);
    }
    if (opened && !opened_empty) {
        draw_set_alpha(0.5 + 0.3 * sin(current_time / 200));
        draw_set_colour(C_GOLD);
        draw_circle(x + 18, y - 52, 3, false);
        draw_set_alpha(1);
    }
}

function checkpoint_draw() {
    var _s = asset_or("spr_checkpoint_star", spr_ph_checkpoint_star);
    var _n = sprite_get_number(_s);
    var _bob = sin(anim / 25) * 4;
    draw_set_alpha(0.3);
    draw_ellipse_colour(x - 20, y - 6, x + 20, y + 6, c_black, c_black, false);
    draw_set_alpha(0.25 + 0.1 * sin(anim / 15));
    draw_circle_colour(x, y - 40 + _bob, 34, C_GOLD, c_black, false);
    draw_set_alpha(1);
    draw_sprite(_s, (anim div 6) mod _n, x, y + _bob);
}

function pickup_draw() {
    var _bob = sin(bob / 12) * 3;
    draw_set_alpha(0.25);
    draw_ellipse_colour(x - 14, y - 4, x + 14, y + 4, c_black, c_black, false);
    draw_set_alpha(1);
    if (array_length(loot) == 0) exit;
    var _ic = item_icon(loot[0][0]);
    if (reward_id != "") {
        draw_set_alpha(0.35 + 0.15 * sin(bob / 10));
        draw_circle_colour(x, y - 30, 28, C_GOLD, c_black, false);
        draw_set_alpha(1);
    }
    if (_ic >= 0) draw_sprite_stretched(_ic, 0, x - 20, y - 50 + _bob, 40, 40);
    else {
        draw_set_colour(C_GOLD);
        draw_circle(x, y - 30 + _bob, 9, false);
    }
}
