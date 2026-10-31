// scr_fx - effects, projectiles and boss hazards. Code-drawn shapes stand in for FX art that has not
// been delivered yet (spr_fx_hit, spr_fx_heal_ring, spr_thunder_marker ...); delivered sprites with
// the contract IDs are used automatically when present.

// ------------------------------------------------------------------ obj_fx
function fx_setup() {
    if (!variable_instance_exists(id, "kind")) kind = "hit";
    if (!variable_instance_exists(id, "dir")) dir = 0;
    if (!variable_instance_exists(id, "owner")) owner = noone;
    if (!variable_instance_exists(id, "text")) text = "";
    if (!variable_instance_exists(id, "life")) {
        switch (kind) {
            case "num": life = 40; break;
            case "heal_ring": life = 36; break;
            case "levelup": life = 60; break;
            case "slash": life = 9; break;
            default: life = 18; break;
        }
    }
    t = 0;
}

function fx_step() {
    if (!world_active() && kind != "levelup") exit;
    t += 1;
    if (kind == "num") y -= 0.8;
    if (instance_exists(owner) && (kind == "heal_ring" || kind == "levelup")) {
        x = owner.x;
        y = owner.y;
    }
    if (instance_exists(owner) && kind == "slash") {
        x = owner.x;
        y = owner.y - 30;
    }
    if (t >= life) instance_destroy();
}

function fx_draw() {
    var _k = t / max(1, life);
    switch (kind) {
        case "slash":
            var _spr = asset_or("spr_fx_slash", spr_sword_attack);
            var _n = sprite_get_number(_spr);
            draw_sprite_ext(_spr, clamp(floor(_k * _n), 0, _n - 1), x, y, 1, 1, dir, c_white, 1);
            break;
        case "hit":
            var _hs = asset_or("spr_fx_hit", -1);
            if (_hs >= 0) draw_sprite(_hs, floor(_k * sprite_get_number(_hs)), x, y);
            else {
                draw_set_alpha(1 - _k);
                draw_set_colour(c_white);
                for (var i = 0; i < 6; i++) {
                    var _a = i * 60 + 15;
                    draw_line_width(x + lengthdir_x(6 + 14 * _k, _a), y + lengthdir_y(6 + 14 * _k, _a),
                        x + lengthdir_x(14 + 22 * _k, _a), y + lengthdir_y(14 + 22 * _k, _a), 3);
                }
                draw_set_alpha(1);
            }
            break;
        case "num":
            draw_set_font(fnt_ui_meta);
            draw_set_halign(fa_center);
            draw_set_colour(c_black);
            draw_set_alpha(1 - _k);
            draw_text(x + 1, y + 1, text);
            draw_set_colour(C_TEXT);
            draw_text(x, y, text);
            draw_set_alpha(1);
            draw_set_halign(fa_left);
            break;
        case "heal_ring":
            // red healing aura (brief: health potions with a red aura)
            var _r = 20 + 40 * _k;
            draw_set_alpha(0.7 * (1 - _k));
            draw_set_colour(C_HEALTH);
            draw_ellipse(x - _r, y - _r * 0.35, x + _r, y + _r * 0.35, true);
            draw_ellipse(x - _r * 0.7, y - _r * 0.25, x + _r * 0.7, y + _r * 0.25, true);
            for (var j = 0; j < 5; j++) {
                var _px = x + lengthdir_x(18, j * 72 + t * 6);
                draw_circle(_px, y - 10 - 60 * _k - j * 4, 3, false);
            }
            draw_set_alpha(1);
            break;
        case "levelup":
            draw_set_alpha(1 - _k);
            draw_set_colour(C_GOLD);
            draw_circle(x, y - 40, 20 + 50 * _k, true);
            draw_set_alpha(1);
            break;
    }
}

// ------------------------------------------------------------------ obj_projectile
function projectile_setup() {
    if (!variable_instance_exists(id, "kind")) kind = "arrow";
    life = 150;
    t = 0;
    hit = false;
    loop_key = "w:proj:" + string(id);
    sort_depth = true;
    flight_y = 0;
    if (kind == "orb") aud_loop("snd_magic_travel", loop_key, x, y);
    else if (kind == "arrow") aud_play("snd_arrow_travel", x, y);
}

function projectile_step() {
    if (!world_active()) exit;
    t += 1;
    var _vx = lengthdir_x(spd, dir);
    var _vy = lengthdir_y(spd, dir);
    x += _vx;
    y += _vy;
    if (kind == "orb") aud_loop_move(loop_key, x, y);
    // ground point of the flight path is ~24 px below the drawn missile
    if (world_proj_blocked_px(x, y + 24)) {
        if (kind == "arrow") aud_play("snd_arrow_hit_world", x, y);
        else aud_play("snd_magic_hit", x, y);
        projectile_end();
        exit;
    }
    if (instance_exists(obj_player)) {
        var _p = obj_player;
        if (point_distance(x, y, _p.x, _p.y - 26) < 20 && _p.state != "dead") {
            if (kind == "arrow") aud_play("snd_arrow_hit", x, y);
            else aud_play("snd_magic_hit", x, y);
            damage_player(dmg, x, y, "projectile");
            projectile_end();
            exit;
        }
    }
    if (t >= life) projectile_end();
}

function projectile_end() {
    aud_loop_stop(loop_key, 30);
    instance_destroy();
}

function projectile_draw() {
    if (kind == "arrow") {
        var _s = asset_or("spr_arrow", -1);
        if (_s >= 0) draw_sprite_ext(_s, 0, x, y, 1, 1, dir, c_white, 1);
        else {
            draw_set_colour(make_colour_rgb(90, 64, 40));
            draw_line_width(x - lengthdir_x(14, dir), y - lengthdir_y(14, dir), x + lengthdir_x(14, dir), y + lengthdir_y(14, dir), 3);
            draw_set_colour(C_TEXT);
            draw_circle(x + lengthdir_x(15, dir), y + lengthdir_y(15, dir), 3, false);
        }
    } else {
        var _o = asset_or("spr_magic_orb", -1);
        if (_o >= 0) draw_sprite(_o, (t div 4) mod sprite_get_number(_o), x, y);
        else {
            draw_set_alpha(0.35);
            draw_set_colour(C_BOSS);
            draw_circle(x, y, 16 + sin(t / 3) * 2, false);
            draw_set_alpha(1);
            draw_set_colour(make_colour_rgb(240, 200, 255));
            draw_circle(x, y, 8, false);
        }
    }
    draw_set_alpha(0.25);
    draw_ellipse_colour(x - 8, y + 21, x + 8, y + 27, c_black, c_black, false);
    draw_set_alpha(1);
}

// ------------------------------------------------------------------ obj_hazard (boss)
function hazard_setup() {
    if (!variable_instance_exists(id, "kind")) kind = "thunder";
    if (!variable_instance_exists(id, "warn")) warn = 66;
    if (!variable_instance_exists(id, "cue")) cue = false;
    if (!variable_instance_exists(id, "play_cue")) play_cue = false;
    if (!variable_instance_exists(id, "life")) life = 45;
    active = true;
    t = 0;
    struck = false;
    if (kind == "crack" && play_cue) aud_play("snd_summon_crack", x, y);
}

function hazard_step() {
    if (!world_active()) exit;
    t += 1;
    if (kind == "thunder") {
        if (t == warn) {
            struck = true;
            if (cue) aud_play("snd_thunder_strike", x, y);
            shake_camera(3, 8);
        }
        if (struck && active && t <= warn + 6 && instance_exists(obj_player)) {
            var _p = obj_player;
            if (px_cell(_p.x) == px_cell(x) && px_cell(_p.y) == px_cell(y)) damage_player(18, x, y, "thunder");
        }
        if (t >= warn + 24) instance_destroy();
    } else if (kind == "crack") {
        if (t >= life) {
            if (active && combat_enabled()) {
                var _u = instance_create_depth(x, y, 0, obj_enemy,
                    { spawn_id: "", family: "undead", leash: obj_boss_ctrl.boss.arena_rect, persistent_spawn: false, summoned: true });
                _u.engaged = true;
                _u.state = "rise";
                _u.t = 0;
                aud_play("snd_undead_rise", x, y);
            }
            instance_destroy();
        }
    }
}

function hazard_draw() {
    if (kind == "thunder") {
        if (!struck) {
            // committed warning marker, readable within ~0.25 s, no strobing
            var _k = min(1, t / 15);
            var _m = asset_or("spr_thunder_marker", -1);
            if (_m >= 0) draw_sprite_ext(_m, (t div 6) mod sprite_get_number(_m), x, y, 1, 1, 0, c_white, _k);
            else {
                draw_set_alpha(0.4 * _k + 0.3 * (t / warn));
                draw_set_colour(make_colour_rgb(255, 214, 90));
                draw_rectangle(x - 30, y - 30, x + 29, y + 29, false);
                draw_set_alpha(_k);
                draw_set_colour(make_colour_rgb(150, 70, 20));
                draw_rectangle(x - 30, y - 30, x + 29, y + 29, true);
                draw_rectangle(x - 29, y - 29, x + 28, y + 28, true);
                draw_set_colour(make_colour_rgb(255, 236, 150));
                draw_set_font(fnt_ui_heading);
                draw_set_halign(fa_center);
                draw_text(x, y - 20, "!");
                draw_set_halign(fa_left);
                draw_set_alpha(1);
            }
        } else {
            var _f = (t - warn) / 24;
            var _bolt = asset_or("spr_lightning_bolt", -1);
            if (_bolt >= 0) draw_sprite_ext(_bolt, floor(_f * sprite_get_number(_bolt)), x, y + 24, 1, 1, 0, c_white, 1 - _f);
            else {
                var _fl = global.settings.reduced_flash ? 0.5 : 1;
                draw_set_alpha((1 - _f) * _fl);
                draw_set_colour(make_colour_rgb(255, 250, 220));
                draw_line_width(x + 6, y - 400, x - 4, y - 200, 6);
                draw_line_width(x - 4, y - 200, x + 8, y - 90, 5);
                draw_line_width(x + 8, y - 90, x, y, 4);
                draw_set_colour(make_colour_rgb(255, 220, 120));
                draw_ellipse(x - 30, y - 12, x + 30, y + 12, false);
                draw_set_alpha(1);
            }
        }
    } else if (kind == "crack") {
        var _c = asset_or("spr_summon_crack", -1);
        if (_c >= 0) draw_sprite(_c, floor(t / life * sprite_get_number(_c)), x, y);
        else {
            draw_set_alpha(0.8);
            draw_set_colour(make_colour_rgb(60, 30, 50));
            draw_ellipse(x - 30 * min(1, t / 15), y - 10, x + 30 * min(1, t / 15), y + 10, false);
            draw_set_colour(C_BOSS);
            draw_ellipse(x - 34, y - 13, x + 34, y + 13, true);
            draw_set_alpha(1);
        }
    }
}
