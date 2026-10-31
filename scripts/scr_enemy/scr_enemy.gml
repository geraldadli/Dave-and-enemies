// scr_enemy - data-driven enemy behaviour (datafiles/data/enemies.json).
// Families: melee (undead, skeleton_warrior, bandit), archer, caster, bat, python, sandworm.
// Enemies sleep when far away without losing state, engage when Dave enters their leash rect,
// never leave it, and persist their defeat by stable spawn ID in global.run.defeated.

/// Resolves a sprite slot from the family's art table: first existing candidate wins.
function enemy_art(_def, _slot) {
    var _art = struct_or(_def, "art", {});
    var _list = struct_or(_art, _slot, undefined);
    if (!is_array(_list)) return { spr: -1, dy: 0, ph: false, scale: 1 };
    for (var i = 0; i < array_length(_list); i++) {
        var _c = _list[i];
        var _s = asset_get_index(_c.s);
        if (_s >= 0) return { spr: _s, dy: struct_or(_c, "dy", 0), ph: struct_or(_c, "ph", false), scale: struct_or(_c, "scale", 1) };
    }
    return { spr: -1, dy: 0, ph: false, scale: 1 };
}

function enemy_setup() {
    def = enemy_def(family);
    if (is_undefined(def)) {
        show_debug_message("unknown enemy family " + string(family));
        instance_destroy();
        exit;
    }
    ai = def.ai;
    hp = def.hp;
    hp_max = def.hp;
    state = (ai == "sandworm") ? "hidden" : "idle";
    t = 0;
    anim_t = 0;
    facing = "down";
    home_x = x;
    home_y = y;
    engaged = false;
    asleep = false;
    hurt_t = 0;
    flash = 0;
    kb_x = 0;
    kb_y = 0;
    last_swing = -1;
    hit_done = false;
    dying_t = 0;
    lock_dir = 270;
    lock_x = x;
    lock_y = y;
    hover_a = random(360);
    next_attack = irandom_range(30, 90);
    step_acc = 0;
    invuln = false;
    sort_depth = true;
    loop_key = "w:" + string(id);
    hurt_r = struct_or(def, "hurt_r", 22);
    hurt_cy = struct_or(def, "hurt_cy", 30);
    flying = (ai == "bat");
    mask_index = asset_or(struct_or(def, "mask", "spr_mask_medium"), spr_mask_medium);
    var _tint = struct_or(def, "ph_tint", undefined);
    ph_colour = is_array(_tint) ? make_colour_rgb(_tint[0], _tint[1], _tint[2]) : c_white;
    art_cache = {};
    if (is_array(leash)) {
        leash_l = leash[0] * TILE + 16;
        leash_t = leash[1] * TILE + 16;
        leash_r = (leash[2] + 1) * TILE - 16;
        leash_b = (leash[3] + 1) * TILE - 16;
    } else {
        leash_l = x - 320;
        leash_t = y - 320;
        leash_r = x + 320;
        leash_b = y + 320;
    }
}

function enemy_art_cached(_slot) {
    var _a = art_cache[$ _slot];
    if (is_undefined(_a)) {
        _a = enemy_art(def, _slot);
        art_cache[$ _slot] = _a;
    }
    return _a;
}

function enemy_player_in_leash(_margin) {
    if (!instance_exists(obj_player)) return false;
    var _p = obj_player;
    return _p.x >= leash_l - _margin && _p.x <= leash_r + _margin && _p.y >= leash_t - _margin && _p.y <= leash_b + _margin;
}

function enemy_clamp_leash() {
    x = clamp(x, leash_l, leash_r);
    y = clamp(y, leash_t, leash_b);
}

function enemy_move(_dx, _dy) {
    if (flying) {
        x += _dx;
        y += _dy;
    } else {
        actor_move(_dx, _dy);
    }
    enemy_clamp_leash();
}

/// Moves toward a point; uses the motion grid when the straight line is blocked.
function enemy_move_to(_tx, _ty, _spd) {
    var _d = point_distance(x, y, _tx, _ty);
    if (_d < 2) return;
    var _a = point_direction(x, y, _tx, _ty);
    if (!flying && world_ready() && !world_los(x, y - 8, _tx, _ty - 8)) {
        var _path = path_add();
        if (mp_grid_path(global.world.mp, _path, x, y, _tx, _ty, true) && path_get_number(_path) > 1) {
            _a = point_direction(x, y, path_get_point_x(_path, 1), path_get_point_y(_path, 1));
        }
        path_delete(_path);
    }
    enemy_move(lengthdir_x(min(_spd, _d), _a), lengthdir_y(min(_spd, _d), _a));
    enemy_face(_a);
}

function enemy_face(_a) {
    var _f = facing_from_angle(_a);
    facing = (_f == "left") ? "left" : _f;
}

/// Plays a family event sound ("attack", "death", "move" ...) from the data table.
function enemy_sound(_event) {
    var _s = struct_or(struct_or(def, "sounds", {}), _event, "");
    if (_s != "") aud_play(_s, x, y);
}

function enemy_footstep() {
    step_acc += 1;
    if (step_acc >= struct_or(def, "step_ticks", 24)) {
        step_acc = 0;
        if (instance_exists(obj_player) && point_distance(x, y, obj_player.x, obj_player.y) < 700) enemy_sound("move");
    }
}

/// Damage from Dave's sword. Returns true when the hit was accepted.
function enemy_take_hit(_dmg, _swing, _fx, _fy) {
    if (state == "dead" || invuln) return false;
    if (_swing == last_swing) return false;   // once per swing-target pair
    last_swing = _swing;
    hp -= _dmg;
    flash = 8;
    instance_create_depth(x, y - hurt_cy - 20, depth - 1, obj_fx, { kind: "num", text: string(_dmg) });
    instance_create_depth(x, y - hurt_cy, depth - 1, obj_fx, { kind: "hit" });
    var _kb = struct_or(def, "knockback", 4);
    if (_kb > 0) {
        var _a = point_direction(_fx, _fy, x, y);
        kb_x = lengthdir_x(_kb, _a);
        kb_y = lengthdir_y(_kb, _a);
    }
    if (variable_instance_exists(id, "is_boss")) {
        boss_on_hit(_dmg);
        return true;
    }
    if (hp <= 0) {
        enemy_die(true);
    } else {
        // ranged windups are interrupted by a hit (their cues stop with them)
        if ((ai == "archer" || ai == "caster") && state == "windup") {
            state = "recover";
            t = 0;
            aud_loop_stop(loop_key, 30);
        }
        hurt_t = 10;
    }
    return true;
}

function enemy_die(_with_rewards) {
    state = "dead";
    dying_t = 0;
    hp = 0;
    aud_loop_stop(loop_key, 40);
    if (!_with_rewards) return;
    enemy_sound("death");
    if (persistent_spawn) global.run.defeated[$ spawn_id] = true;
    grant_xp(struct_or(def, "xp", 10));
    var _loot = array_or(struct_or(def, "loot", []));
    var _drop = [];
    for (var i = 0; i < array_length(_loot); i++) {
        var _l = _loot[i];
        if (random(1) < _l.chance) {
            var _n = is_array(_l.n) ? irandom_range(_l.n[0], _l.n[1]) : _l.n;
            array_push(_drop, [_l.id, _n]);
        }
    }
    if (array_length(_drop) > 0) instance_create_depth(x, y, depth, obj_pickup, { loot: _drop });
}

/// Silent removal (boss whiteout cleanup): no sound, XP, loot or persistence.
function enemy_despawn_silent() {
    aud_loop_stop(loop_key, 0);
    instance_destroy();
}

function enemy_try_melee_hit(_reach) {
    if (hit_done || !instance_exists(obj_player)) return;
    var _p = obj_player;
    var _cx = x + lengthdir_x(_reach * 0.5, lock_dir);
    var _cy = y - 20 + lengthdir_y(_reach * 0.5, lock_dir);
    if (point_distance(_cx, _cy, _p.x, _p.y - 24) <= _reach * 0.6 + 16) {
        hit_done = true;
        damage_player(def.damage, x, y, "melee");
    }
}

function enemy_spawn_projectile(_kind) {
    var _off = struct_or(struct_or(def, "spawn_offsets", {}), facing, [0, -40]);
    var _sx = x + ((facing == "left") ? -_off[0] : _off[0]);
    var _sy = y + _off[1];
    var _a = instance_exists(obj_player) ? point_direction(_sx, _sy, obj_player.x, obj_player.y - 24) : lock_dir;
    return instance_create_depth(_sx, _sy, depth - 1, obj_projectile,
        { kind: _kind, dir: _a, spd: def.proj_speed, dmg: def.damage, owner_family: family });
}

// ------------------------------------------------------------------ per-family logic
function enemy_step() {
    if (!world_active()) exit;
    anim_t += 1;
    if (flash > 0) flash -= 1;
    if (state == "dead") {
        dying_t += 1;
        if (dying_t > 45) instance_destroy();
        exit;
    }
    var _p = instance_exists(obj_player) ? obj_player.id : noone;
    if (_p == noone || _p.state == "dead") {
        engaged = false;
        exit;
    }
    var _dist = point_distance(x, y, _p.x, _p.y);
    if (!engaged && _dist > 1500) {
        asleep = true;
        exit;
    }
    asleep = false;
    if (abs(kb_x) + abs(kb_y) > 0.2) {
        enemy_move(kb_x, kb_y);
        kb_x *= 0.75;
        kb_y *= 0.75;
    }
    if (hurt_t > 0) {
        hurt_t -= 1;
        if (ai != "sandworm") exit;
    }
    var _was = engaged;
    if (!engaged && enemy_player_in_leash(TILE) && !global.damage_paused) engaged = true;
    if (engaged && !enemy_player_in_leash(TILE * 3)) engaged = false;
    if (_was && !engaged && ai != "sandworm") {
        state = "return";
        aud_loop_stop(loop_key, 60);
    }
    switch (ai) {
        case "melee": enemy_ai_melee(_p, _dist); break;
        case "archer":
        case "caster": enemy_ai_ranged(_p, _dist); break;
        case "bat": enemy_ai_bat(_p, _dist); break;
        case "python": enemy_ai_python(_p, _dist); break;
        case "sandworm": enemy_ai_worm(_p, _dist); break;
    }
}

function enemy_ai_return() {
    enemy_move_to(home_x, home_y, def.speed);
    enemy_footstep();
    if (point_distance(x, y, home_x, home_y) < 8) {
        state = "idle";
        t = 0;
    }
}

function enemy_ai_melee(_p, _dist) {
    t += 1;
    switch (state) {
        case "idle":
            if (engaged) { state = "chase"; t = 0; }
            break;
        case "return": enemy_ai_return(); break;
        case "rise":
            if (t >= 30) { state = "chase"; t = 0; }
            break;
        case "chase":
            if (!engaged) break;
            if (_dist <= def.attack_range && t > 10) {
                state = "windup";
                t = 0;
                lock_dir = point_direction(x, y, _p.x, _p.y);
                enemy_face(lock_dir);
                enemy_sound("attack");
            } else {
                enemy_move_to(_p.x, _p.y, def.speed);
                enemy_footstep();
            }
            break;
        case "windup":
            if (t >= def.windup) { state = "active"; t = 0; hit_done = false; }
            break;
        case "active":
            if (struct_or(def, "lunge", 0) > 0) enemy_move(lengthdir_x(def.lunge, lock_dir), lengthdir_y(def.lunge, lock_dir));
            enemy_try_melee_hit(def.reach);
            if (t >= def.active) { state = "recover"; t = 0; }
            break;
        case "recover":
            if (t >= def.recover) { state = engaged ? "chase" : "return"; t = 0; }
            break;
    }
}

function enemy_ai_ranged(_p, _dist) {
    t += 1;
    var _los = world_los(x, y - 30, _p.x, _p.y - 24);
    switch (state) {
        case "idle":
            if (engaged) { state = "chase"; t = 0; }
            break;
        case "return": enemy_ai_return(); break;
        case "chase":
            if (!engaged) break;
            enemy_face(point_direction(x, y, _p.x, _p.y));
            if (_dist < def.keep_min) {
                var _a = point_direction(_p.x, _p.y, x, y);
                enemy_move(lengthdir_x(def.speed, _a), lengthdir_y(def.speed, _a));
                enemy_footstep();
            } else if (_dist > def.keep_max || !_los) {
                enemy_move_to(_p.x, _p.y, def.speed);
                enemy_footstep();
            } else if (t > next_attack) {
                state = "windup";
                t = 0;
                lock_dir = point_direction(x, y, _p.x, _p.y);
                enemy_sound("windup");
            }
            break;
        case "windup":
            enemy_face(point_direction(x, y, _p.x, _p.y));
            if (t >= def.windup) {
                // release frame: the cue plays only when the projectile actually spawns
                if (_los && combat_enabled()) {
                    var _pr = enemy_spawn_projectile(def.projectile);
                    if (instance_exists(_pr)) enemy_sound("release");
                }
                state = "recover";
                t = 0;
            }
            break;
        case "recover":
            if (t >= def.recover) {
                state = engaged ? "chase" : "return";
                t = 0;
                next_attack = irandom_range(def.cooldown[0], def.cooldown[1]);
            }
            break;
    }
}

function enemy_ai_bat(_p, _dist) {
    t += 1;
    if (anim_t mod 30 == 0 && _dist < 600) enemy_sound("move");
    switch (state) {
        case "idle":
            y = home_y + sin(anim_t / 20) * 6;
            if (engaged) { state = "hover"; t = 0; }
            break;
        case "return":
            enemy_move_to(home_x, home_y, def.speed);
            if (point_distance(x, y, home_x, home_y) < 8) { state = "idle"; t = 0; }
            break;
        case "hover":
            if (!engaged) break;
            hover_a += 1.5;
            var _hx = _p.x + lengthdir_x(140, hover_a);
            var _hy = _p.y - 30 + lengthdir_y(90, hover_a);
            enemy_move_to(_hx, _hy, def.speed);
            if (t > next_attack) {
                state = "windup";
                t = 0;
                enemy_sound("windup");
            }
            break;
        case "windup":
            lock_x = _p.x;
            lock_y = _p.y - 20;
            if (t >= def.windup) {
                state = "active";
                t = 0;
                hit_done = false;
                lock_dir = point_direction(x, y, lock_x, lock_y);
                enemy_sound("dive");
            }
            break;
        case "active":
            enemy_move(lengthdir_x(def.dive_speed, lock_dir), lengthdir_y(def.dive_speed, lock_dir));
            if (!hit_done && point_distance(x, y, _p.x, _p.y - 24) < 30) {
                hit_done = true;
                damage_player(def.damage, x, y, "melee");
            }
            if (t >= def.active) { state = "recover"; t = 0; }
            break;
        case "recover":
            var _ra = point_direction(_p.x, _p.y, x, y);
            enemy_move(lengthdir_x(def.speed, _ra), lengthdir_y(def.speed, _ra));
            if (t >= def.recover) {
                state = engaged ? "hover" : "return";
                t = 0;
                next_attack = irandom_range(def.cooldown[0], def.cooldown[1]);
            }
            break;
    }
}

function enemy_ai_python(_p, _dist) {
    t += 1;
    switch (state) {
        case "idle":
            if (engaged) { state = "chase"; t = 0; }
            break;
        case "return": enemy_ai_return(); break;
        case "chase":
            if (!engaged) break;
            if (_dist < def.attack_range && t > 30 && world_los(x, y - 10, _p.x, _p.y - 10)) {
                state = "windup";
                t = 0;
                lock_dir = point_direction(x, y, _p.x, _p.y);
                enemy_face(lock_dir);
                enemy_sound("windup");
            } else {
                enemy_move_to(_p.x, _p.y, def.speed);
                enemy_footstep();
            }
            break;
        case "windup":
            if (t >= def.windup) {
                state = "active";
                t = 0;
                hit_done = false;
                enemy_sound("lunge");
            }
            break;
        case "active":
            enemy_move(lengthdir_x(def.lunge, lock_dir), lengthdir_y(def.lunge, lock_dir));
            if (!hit_done && point_distance(x, y, _p.x, _p.y) < 40) {
                hit_done = true;
                damage_player(def.damage, x, y, "melee");
            }
            if (t >= def.active) { state = "recover"; t = 0; }
            break;
        case "recover":
            if (t >= def.recover) { state = engaged ? "chase" : "return"; t = 0; }
            break;
    }
}

function enemy_ai_worm(_p, _dist) {
    t += 1;
    invuln = (state == "hidden" || state == "warning");
    switch (state) {
        case "hidden":
            if (!engaged) {
                aud_loop_stop(loop_key, 80);
                enemy_move_to(home_x, home_y, def.speed);
                break;
            }
            aud_loop("snd_worm_rumble", loop_key, x, y);
            enemy_move_to(_p.x, _p.y, def.speed);
            if (_dist < 90 && t > 40) {
                state = "warning";
                t = 0;
            }
            break;
        case "warning":
            aud_loop_move(loop_key, x, y);
            if (t >= def.windup) {
                aud_loop_stop(loop_key, 80);
                enemy_sound("emerge");
                state = "emerge";
                t = 0;
                hit_done = false;
            }
            break;
        case "emerge":
            if (t >= 8 && t <= 16 && !hit_done && _dist < def.reach) {
                hit_done = true;
                damage_player(def.damage, x, y, "melee");
            }
            if (t >= 24) { state = "exposed"; t = 0; next_attack = 40; }
            break;
        case "exposed":
            if (_dist < def.reach + 20 && t > next_attack) {
                state = "active";
                t = 0;
                hit_done = false;
                lock_dir = point_direction(x, y, _p.x, _p.y);
            }
            if (t >= def.exposed) {
                state = "burrow";
                t = 0;
                enemy_sound("burrow");
            }
            break;
        case "active":
            if (t == 12) enemy_sound("bite");
            if (t >= 12 && t <= 20) enemy_try_melee_hit(def.reach);
            if (t >= def.active) { state = "exposed"; t = 0; next_attack = 50; }
            break;
        case "burrow":
            if (t >= 30) { state = "hidden"; t = 0; }
            break;
    }
}

// ------------------------------------------------------------------ drawing
function enemy_draw() {
    var _alpha = 1;
    if (state == "dead") _alpha = 1 - dying_t / 45;
    if (asleep && !point_in_rectangle(x, y, global.cam_cx - 760, global.cam_cy - 480, global.cam_cx + 760, global.cam_cy + 520)) exit;
    // shared soft ground shadow (no baked shadows in contract art)
    var _sw = struct_or(def, "shadow_w", 34);
    if (!(ai == "sandworm" && (state == "hidden" || state == "warning"))) {
        draw_set_alpha(0.28 * _alpha);
        draw_ellipse_colour(x - _sw, y - _sw * 0.3, x + _sw, y + _sw * 0.3, c_black, c_black, false);
        draw_set_alpha(1);
    }
    var _slot = "idle";
    var _dir = (facing == "left") ? "side" : facing;
    var _flip = (facing == "left") ? -1 : 1;
    var _frac = 0;
    switch (state) {
        case "chase": case "return": case "hover": _slot = "walk_" + _dir; break;
        case "windup": _slot = "attack_" + _dir; _frac = 0.45 * t / max(1, def.windup); break;
        case "active": _slot = "attack_" + _dir; _frac = 0.45 + 0.25 * t / max(1, def.active); break;
        case "recover": _slot = ((ai == "melee") ? "attack_" : "walk_") + _dir; _frac = 0.7 + 0.3 * t / max(1, def.recover); break;
        case "dead": _slot = "defeat"; break;
        case "hidden": case "warning": _slot = "mound"; break;
        case "emerge": _slot = "emerge"; _frac = t / 24; break;
        case "burrow": _slot = "emerge"; _frac = 1 - t / 30; break;
        case "exposed": _slot = "idle"; break;
        case "rise": _slot = "rise"; _frac = t / 30; break;
    }
    var _a = enemy_art_cached(_slot);
    if (_a.spr < 0) _a = enemy_art_cached("idle");
    if (_a.spr < 0) exit;
    var _n = sprite_get_number(_a.spr);
    var _img;
    if (state == "windup" || state == "active" || state == "recover" || state == "emerge" || state == "burrow" || state == "rise") _img = clamp(floor(_frac * _n), 0, _n - 1);
    else _img = floor(anim_t * struct_or(def, "anim_fps", 12) / TPS) mod _n;
    var _col = _a.ph ? ph_colour : c_white;
    var _sc = _a.scale;
    var _yy = y + _a.dy * _sc;
    if (ai == "sandworm" && state == "warning") _yy += sin(anim_t * 1.3) * 2;
    if (flying) _yy -= 30;
    draw_sprite_ext(_a.spr, _img, x, _yy, _flip * _sc, _sc, 0, _col, _alpha);
    if (flash > 0) {
        gpu_set_fog(true, c_white, 0, 1);
        draw_sprite_ext(_a.spr, _img, x, _yy, _flip * _sc, _sc, 0, c_white, 0.6 * _alpha);
        gpu_set_fog(false, c_white, 0, 0);
    }
    // windup telegraph ring, readable within ~0.25 s
    if (state == "windup" || (ai == "sandworm" && state == "warning")) {
        var _k = min(1, t / 12);
        draw_set_alpha(0.55 * _k);
        draw_set_colour(C_ERROR);
        draw_circle(x, y - hurt_cy - 46 - (flying ? 30 : 0), 7, false);
        if (ai == "sandworm") draw_ellipse(x - 60, y - 22, x + 60, y + 22, true);
        draw_set_alpha(1);
    }
}
