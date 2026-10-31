// scr_boss - the in-scene Pharaoh encounter (Royal Expanse) and the chapter ending.
// obj_boss_ctrl owns the arena state (idle, entering, dialogue, combat, defeat, cleared), both
// barriers, the reward and the doorway trigger. obj_pharaoh owns attack scheduling.
// Normal completion and skip call the same idempotent routines.

#macro BOSS_REWARD_ID "rm_sc_royal_expanse:u1"

function boss_ctrl() {
    return instance_exists(obj_boss_ctrl) ? obj_boss_ctrl.id : noone;
}

/// Instance scope (obj_boss_ctrl): builds the arena for the current persistent state.
function boss_ctrl_setup() {
    var _b = boss;
    state = "idle";
    t = 0;
    intro_done = false;
    defeat_done = false;
    cleanup_done = false;
    ending_started = false;
    pharaoh = noone;
    gate = instance_create_depth(cell_px(_b.entrance_gate_rect[0]) - 32, cell_px(_b.entrance_gate_rect[3]), 0, obj_gate,
        { rect: _b.entrance_gate_rect, kind: "arena", closed: false });
    seal = instance_create_depth(cell_px(_b.east_seal_rect[0]) - 32, cell_px(_b.east_seal_rect[3]), 0, obj_gate,
        { rect: _b.east_seal_rect, kind: "seal", closed: true });
    threshold_rect = [153, 12, 154, 12];
    for (var i = 0; i < array_length(scripts); i++) {
        if (scripts[i].event == "chapter_ending") threshold_rect = scripts[i].rect;
    }
    if (flag("boss_pharaoh_defeated")) {
        state = "cleared";
        gate.closed = false;
        seal.closed = false;
        boss_spawn_reward_if_pending();
    } else {
        pharaoh = instance_create_depth(cell_px(_b.pharaoh_cell[0]), cell_px(_b.pharaoh_cell[1]), 0, obj_pharaoh,
            { boss: _b, ctrl: id });
    }
    with (gate) gate_apply();
    with (seal) gate_apply();
}

function boss_spawn_reward_if_pending() {
    var _st = struct_or(global.run.rewards, BOSS_REWARD_ID, "");
    if (_st != "pending") return;
    var _exists = false;
    with (obj_pickup) if (reward_id == BOSS_REWARD_ID) _exists = true;
    if (_exists) return;
    var _c = boss.reward.cell;
    instance_create_depth(cell_px(_c[0]), cell_px(_c[1]), 0, obj_pickup,
        { loot: boss.reward.loot, reward_id: BOSS_REWARD_ID, persistent_reward: true });
}

function boss_ctrl_step() {
    t += 1;
    switch (state) {
        case "idle": boss_check_entry(); break;
        case "entering": boss_entering_step(); break;
        case "defeat": boss_defeat_step(); break;
        case "cleared": boss_check_threshold(); break;
        case "ending": boss_ending_step(); break;
    }
}

// ------------------------------------------------------------------ entry and intro
/// The throat trigger is unavoidable: Dave's whole mask must be north of row 29's top (y 1856).
function boss_check_entry() {
    if (!world_active() || global.cine_lock || !instance_exists(obj_player)) return;
    var _p = obj_player;
    var _r = boss.entry_trigger_rect;
    var _x1 = _r[0] * TILE;
    var _x2 = (_r[2] + 1) * TILE;
    var _limit = (_r[1] + 1) * TILE;   // row 29 top
    if (_p.bbox_left >= _x1 - 8 && _p.bbox_right <= _x2 + 8 && _p.bbox_bottom < _limit && _p.y > _limit - 3 * TILE) {
        boss_begin_intro();
    }
}

function boss_begin_intro() {
    state = "entering";
    t = 0;
    intro_done = false;
    global.cine_lock = true;
    global.damage_paused = true;
    with (obj_projectile) instance_destroy();
    var _sc = boss.safe_intro_dave_cell;
    with (obj_player) player_script_walk(cell_px(_sc[0]), cell_px(_sc[1]), "up");
    global.cam_target = { x: boss.intro_camera_target_pixel[0], y: boss.intro_camera_target_pixel[1] };
    mus_stop(1200);
    var _self = id;
    cine_begin({
        skip_allowed: true,
        on_skip: method(_self, boss_intro_complete),
        on_advance: undefined,
        draw: function() { cine_draw_skip_hint(); }
    });
}

function boss_entering_step() {
    var _p = instance_exists(obj_player) ? obj_player.id : noone;
    var _arrived = (_p == noone) || !_p.scripted;
    if (_arrived && !gate.closed && gate.anim_dir == 0) {
        gate_close_animated(gate);
    }
    if (gate.closed && gate.anim_dir == 0 && !ui_has(OV.DIALOGUE) && !intro_done) {
        if (t > 30) {
            state = "dialogue";
            dialogue_open("boss_intro", method(id, boss_intro_complete));
        }
    }
}

/// boss_intro_complete: identical state after acknowledgement, pause-menu skip or hold-skip.
function boss_intro_complete() {
    if (intro_done) return;
    intro_done = true;
    if (ui_has(OV.DIALOGUE)) {
        global.dlg.done = true;
        ui_remove(OV.DIALOGUE);
        global.dlg = undefined;
    }
    ui_remove(OV.PAUSE);
    aud_blip_cancel();
    global.aud.text_duck = false;
    var _sc = boss.safe_intro_dave_cell;
    with (obj_player) {
        player_script_stop();
        if (point_distance(x, y, cell_px(_sc[0]), cell_px(_sc[1])) > 4) {
            x = cell_px(_sc[0]);
            y = cell_px(_sc[1]);
        }
        facing = "up";
    }
    gate.closed = true;
    gate.anim_dir = 0;
    gate.anim = 1;
    with (gate) gate_apply();
    seal.closed = true;
    with (seal) gate_apply();
    if (!instance_exists(pharaoh)) {
        pharaoh = instance_create_depth(cell_px(boss.pharaoh_cell[0]), cell_px(boss.pharaoh_cell[1]), 0, obj_pharaoh,
            { boss: boss, ctrl: id });
    }
    with (obj_pharaoh) if (id != other.pharaoh) instance_destroy();
    flag_set("boss_intro_seen", true);
    state = "combat";
    t = 0;
    global.cam_target = undefined;
    global.boss_ui.visible = true;
    global.boss_ui.hp = pharaoh.hp;
    global.boss_ui.hp_max = pharaoh.hp_max;
    global.boss_ui.ghost = pharaoh.hp;
    mus_play("mus_pharaoh");
    toast_objective("objective_pharaoh");
    with (pharaoh) {
        state = "wait";
        t = 0;
        wait_len = ms_ticks(750) + 20;   // first telegraph no earlier than 0.75 s after control returns
    }
    cine_end();
    global.cine_lock = false;
    global.damage_paused = false;
    inp_block_all();
}

// ------------------------------------------------------------------ defeat
/// Called by the Pharaoh at legitimate zero HP. Stops every damage source immediately.
function boss_begin_defeat() {
    if (state == "defeat" || state == "cleared") return;
    state = "defeat";
    t = 0;
    defeat_done = false;
    cleanup_done = false;
    global.cine_lock = true;
    global.damage_paused = true;
    global.boss_ui.hp = 0;
    with (obj_projectile) instance_destroy();
    with (obj_hazard) active = false;
    aud_loops_stop_prefix("boss:", 0);
    aud_loops_stop_prefix("w:", 30);
    mus_stop(250);
    aud_play("snd_boss_death", undefined, undefined, "", false);
    aud_play("snd_disintegrate", undefined, undefined, "", false);
    shake_camera(5, 30);
    with (obj_player) player_script_stop();
    var _self = id;
    cine_begin({
        skip_allowed: true,
        on_skip: method(_self, boss_defeat_complete),
        on_advance: undefined,
        draw: function() { cine_draw_skip_hint(); }
    });
}

function boss_defeat_step() {
    var _sec = t / TPS;
    if (t == ms_ticks(250)) mus_play("mus_boss_defeat");
    var _dark = global.settings.reduced_flash;
    global.whiteout.dark = _dark;
    if (_sec >= 1.5 && _sec < 3.5) global.whiteout.alpha = smoothstep01((_sec - 1.5) / 2);
    else if (_sec >= 3.5 && _sec < 4.5) {
        global.whiteout.alpha = 1;
        boss_cleanup();
    } else if (_sec >= 4.5 && _sec < 6.5) {
        if (t == ms_ticks(4500)) {
            aud_loop("snd_wind_loop", "weather", undefined, undefined, false);
            aud_play("snd_gate_open", undefined, undefined, "", false);
        }
        global.whiteout.alpha = 1 - smoothstep01((_sec - 4.5) / 2);
    } else if (_sec >= 6.5) {
        global.whiteout.alpha = 0;
        if (t == ms_ticks(6500)) mus_play("mus_desert", 1000);
        if (_sec >= 7.5) boss_defeat_complete();
    }
}

/// Removes every threat while obscured, opens both barriers and atomically commits the victory.
function boss_cleanup() {
    if (cleanup_done) return;
    cleanup_done = true;
    with (obj_pharaoh) instance_destroy();
    pharaoh = noone;
    with (obj_enemy) if (summoned) enemy_despawn_silent();
    with (obj_projectile) instance_destroy();
    with (obj_hazard) instance_destroy();
    aud_loops_stop_prefix("boss:", 0);
    // atomic: defeated flag and pending unique reward are written together, before any claim
    flag_set("boss_pharaoh_defeated", true);
    if (struct_or(global.run.rewards, BOSS_REWARD_ID, "") != "claimed") global.run.rewards[$ BOSS_REWARD_ID] = "pending";
    gate.closed = false;
    gate.anim = 0;
    gate.anim_dir = 0;
    with (gate) gate_apply();
    seal.closed = false;
    seal.anim = 0;
    seal.anim_dir = 0;
    with (seal) gate_apply();
    global.boss_ui.visible = false;
    boss_spawn_reward_if_pending();
}

/// boss_defeat_complete: shared by the timed end (7.5 s) and the hold-skip after zero HP.
function boss_defeat_complete() {
    if (defeat_done) return;
    defeat_done = true;
    boss_cleanup();
    if (t < ms_ticks(250)) aud_cancel_pending("");
    if (mus_current() != "mus_desert") mus_play("mus_desert", 1000);
    aud_loop("snd_wind_loop", "weather", undefined, undefined, false);
    global.whiteout.alpha = 0;
    state = "cleared";
    t = 0;
    cine_end();
    global.cine_lock = false;
    global.damage_paused = false;
    toast_objective("objective_dungeon");
    inp_block_all();
}

// ------------------------------------------------------------------ ending
function boss_check_threshold() {
    if (!world_active() || global.cine_lock || !instance_exists(obj_player)) return;
    if (!flag("boss_pharaoh_defeated")) return;
    var _p = obj_player;
    var _r = threshold_rect;
    if (_p.x >= _r[0] * TILE && _p.x < (_r[2] + 1) * TILE && _p.bbox_bottom < (_r[3] + 1) * TILE && _p.bbox_top >= _r[1] * TILE - TILE) {
        boss_begin_ending();
    }
}

function boss_begin_ending() {
    state = "ending";
    t = 0;
    ending_started = true;
    ending_tr = undefined;
    global.cine_lock = true;
    global.damage_paused = true;
    with (obj_player) player_script_walk(x, y - 2 * TILE + 16, "up");
    mus_stop(1000);
    mus_play("mus_ending");
    aud_loop_stop("weather", 2000);
    var _self = id;
    cine_begin({
        skip_allowed: true,
        on_skip: method(_self, function() { boss_ending_finish(true); }),
        on_advance: method(_self, function() { if (is_struct(ending_tr)) textrun_reveal(ending_tr); }),
        draw: method(_self, function() {
            var _ln = ending_tr;
            if (is_struct(_ln)) {
                var _lt = t - ms_ticks(2000);
                var _a = min(1, _lt / 12, (ms_ticks(3000) - _lt) / 12);
                cine_draw_text(_ln, _a);
            }
            cine_draw_skip_hint();
        })
    });
}

function boss_ending_step() {
    if (t == ms_ticks(2000)) {
        var _l = dialogue_line("ending", 0);
        if (is_struct(_l)) ending_tr = textrun_create(_l, "dialogue", CAPTION_W_SPEAKER);
    }
    if (is_struct(ending_tr)) {
        textrun_step(ending_tr);
        if (t >= ms_ticks(5000)) {
            aud_blip_cancel();
            ending_tr = undefined;
        }
    }
    if (t >= ms_ticks(5000)) global.fade_black = clamp((t - ms_ticks(5000)) / TPS, 0, 1);
    if (t >= ms_ticks(6000)) boss_ending_finish(false);
}

/// ending_complete: flags, held title, no save write. Skip lands on the same held title.
function boss_ending_finish(_skipped) {
    if (state == "ended") return;
    state = "ended";
    aud_blip_cancel();
    flag_set("chapter_1_complete", true);
    flag_set("ending_seen", true);
    flag_set("grail_recovered", false);
    cine_end();
    global.cine_lock = false;
    global.fade_black = 0;
    ui_clear();
    aud_stop_world(200);
    ending_open(_skipped);
    room_goto(rm_ending);
}

// ------------------------------------------------------------------ Pharaoh behaviour (obj_pharaoh scope)
function pharaoh_setup() {
    family = "pharaoh";
    def = enemy_def("pharaoh");
    hp = def.hp;
    hp_max = def.hp;
    is_boss = true;
    state = "idle";
    t = 0;
    anim_t = 0;
    flash = 0;
    invuln = true;
    last_swing = -1;
    wait_len = 60;
    actions = 0;
    aim_dir = 270;
    beam_len = 0;
    hurt_r = def.hurt_r;
    hurt_cy = def.hurt_cy;
    sort_depth = true;
    kb_x = 0;
    kb_y = 0;
    hurt_t = 0;
    leash = undefined;
    persistent_spawn = false;
    summoned = false;
    tele_target = [x, y];
    mask_index = spr_mask_pharaoh;
    thunder_wave = 0;
}

function pharaoh_phase() {
    var _r = hp / hp_max;
    if (_r > 0.65) return 1;
    if (_r > 0.30) return 2;
    return 3;
}

function boss_on_hit(_dmg) {
    global.boss_ui.ghost = max(global.boss_ui.ghost, hp + _dmg);
    global.boss_ui.ghost_t = ms_ticks(250);
    global.boss_ui.hp = max(0, hp);
    if (hp <= 0) {
        hp = 0;
        state = "dying";
        t = 0;
        invuln = true;
        with (ctrl) boss_begin_defeat();
    } else {
        aud_play("snd_boss_hurt", x, y);
    }
}

function pharaoh_count(_family) {
    var _n = 0;
    with (obj_enemy) if (summoned && family == _family && state != "dead") _n++;
    return _n;
}

/// Random authored cell at least _min_cells from Dave, skipping cells listed in _used.
function pharaoh_pick_cell(_cells, _min_cells, _used = []) {
    var _p = instance_exists(obj_player) ? obj_player.id : noone;
    var _ok = [];
    for (var i = 0; i < array_length(_cells); i++) {
        if (array_contains(_used, i)) continue;
        var _px = cell_px(_cells[i][0]);
        var _py = cell_px(_cells[i][1]);
        if (_p == noone || point_distance(_px, _py, _p.x, _p.y) >= _min_cells * TILE) array_push(_ok, i);
    }
    if (array_length(_ok) == 0) return undefined;
    var _k = _ok[irandom(array_length(_ok) - 1)];
    array_push(_used, _k);
    return _cells[_k];
}

function pharaoh_step() {
    anim_t += 1;
    if (flash > 0 && world_active()) flash -= 1;
    if (state == "dying") {
        t += 1;   // cinematic-owned: the disintegration plays while the world is suspended
        exit;
    }
    if (state == "idle") exit;
    if (!world_active()) exit;
    t += 1;
    var _ph = pharaoh_phase();
    var _p = instance_exists(obj_player) ? obj_player.id : noone;
    if (_p == noone) exit;
    switch (state) {
        case "wait":
            invuln = false;
            if (t >= wait_len) pharaoh_choose(_ph);
            break;
        case "teleport_out":
            invuln = true;
            if (t >= 24) {
                x = tele_target[0];
                y = tele_target[1];
                state = "teleport_in";
                t = 0;
                aud_play("snd_boss_teleport_in", x, y);
            }
            break;
        case "teleport_in":
            invuln = true;
            if (t >= 24) pharaoh_rest(_ph);
            break;
        case "laser_charge":
            invuln = false;
            aud_loop_move("boss:laser", x, y);
            var _lock = def.laser_charge - def.laser_lock;
            if (t < _lock) aim_dir = point_direction(x, y - 110, _p.x, _p.y - 24);
            beam_len = pharaoh_beam_length(aim_dir);
            if (t >= def.laser_charge) {
                state = "laser_fire";
                t = 0;
                aud_loop_stop("boss:laser", 0);
                aud_loop("snd_laser_fire", "boss:laser", x, y);
            }
            break;
        case "laser_fire":
            beam_len = pharaoh_beam_length(aim_dir);
            var _sx = x;
            var _sy = y - 110;
            var _ex = _sx + lengthdir_x(beam_len, aim_dir);
            var _ey = _sy + lengthdir_y(beam_len, aim_dir);
            if (pharaoh_seg_dist(_p.x, _p.y - 24, _sx, _sy, _ex, _ey) < def.laser_width / 2 + 12) {
                damage_player(def.laser_damage, _sx, _sy, "laser");
            }
            if (t >= def.laser_fire) {
                aud_loop_stop("boss:laser", -1);
                pharaoh_rest(_ph);
            }
            break;
        case "summon":
            if (t == 20) pharaoh_do_summon(_ph);
            if (t >= 50) pharaoh_rest(_ph);
            break;
        case "thunder":
            if (t == 10) pharaoh_thunder_wave(_ph);
            if (t >= 50) pharaoh_rest(_ph);
            break;
    }
}

function pharaoh_rest(_ph) {
    state = "wait";
    t = 0;
    var _w = def.wait[_ph - 1];
    wait_len = irandom_range(_w[0], _w[1]);
}

function pharaoh_choose(_ph) {
    actions += 1;
    var _p = obj_player;
    // teleport every few actions, or when Dave is pressing close
    if (actions mod 3 == 0 || point_distance(x, y, _p.x, _p.y) < 110) {
        var _c = pharaoh_pick_cell(boss.teleport_cells, 4);
        if (!is_undefined(_c) && (cell_px(_c[0]) != x || cell_px(_c[1]) != y)) {
            tele_target = [cell_px(_c[0]), cell_px(_c[1])];
            state = "teleport_out";
            t = 0;
            aud_play("snd_boss_teleport_out", x, y);
            return;
        }
    }
    var _bats = pharaoh_count("bat");
    var _und = pharaoh_count("undead");
    var _opts = ["laser", "thunder"];
    if (_bats < boss.caps.bats) array_push(_opts, "bats");
    if (_ph >= 2 && _und < boss.caps.undead) array_push(_opts, "undead");
    var _pick = _opts[irandom(array_length(_opts) - 1)];
    // no laser/thunder overlap: each action finishes before the next begins
    switch (_pick) {
        case "laser":
            state = "laser_charge";
            t = 0;
            aim_dir = point_direction(x, y - 110, _p.x, _p.y - 24);
            aud_loop("snd_laser_charge", "boss:laser", x, y);
            break;
        case "thunder":
            state = "thunder";
            t = 0;
            break;
        case "bats":
        case "undead":
            state = "summon";
            t = 0;
            summon_kind = _pick;
            break;
    }
}

function pharaoh_do_summon(_ph) {
    aud_play("snd_boss_summon", x, y);
    if (summon_kind == "bats") {
        var _cap = boss.caps.bats - pharaoh_count("bat");
        var _used = [];
        for (var i = 0; i < _cap; i++) {
            var _c = pharaoh_pick_cell(boss.bat_spawn_cells, 3, _used);
            if (is_undefined(_c)) break;   // postpone when no legal point
            var _b = instance_create_depth(cell_px(_c[0]), cell_px(_c[1]), 0, obj_enemy,
                { spawn_id: "", family: "bat", leash: boss.arena_rect, persistent_spawn: false, summoned: true });
            _b.engaged = true;
            _b.state = "hover";
            aud_play("snd_boss_bat_spawn", _b.x, _b.y);
        }
    } else {
        var _cap2 = boss.caps.undead - pharaoh_count("undead");
        var _first = true;
        var _used2 = [];
        for (var j = 0; j < _cap2; j++) {
            var _c2 = pharaoh_pick_cell(boss.undead_spawn_cells, 3, _used2);
            if (is_undefined(_c2)) break;
            instance_create_depth(cell_px(_c2[0]), cell_px(_c2[1]), 0, obj_hazard,
                { kind: "crack", life: 45, play_cue: _first });
            _first = false;
        }
    }
}

/// Thunder wave: committed targets never move; a connected 3-cell-wide safe strip near Dave stays
/// unmarked, and the first warning lasts at least 1.0 s (reachable at Dave's 4 px/tick).
function pharaoh_thunder_wave(_ph) {
    var _r = boss.arena_rect;
    var _p = obj_player;
    var _pcx = clamp(px_cell(_p.x), _r[0], _r[2]);
    var _pcy = clamp(px_cell(_p.y), _r[1], _r[3]);
    var _vertical = irandom(1) == 0;
    var _c = _vertical ? clamp(_pcx + irandom_range(-2, 2), _r[0] + 1, _r[2] - 1) : clamp(_pcy + irandom_range(-2, 2), _r[1] + 1, _r[3] - 1);
    var _density = def.thunder_density[_ph - 1];
    var _vx1 = px_cell(global.cam_cx - 600);
    var _vx2 = px_cell(global.cam_cx + 600);
    var _vy1 = px_cell(global.cam_cy - 330);
    var _vy2 = px_cell(global.cam_cy + 330);
    var _count = 0;
    thunder_wave += 1;
    for (var _x = max(_r[0], _vx1); _x <= min(_r[2], _vx2); _x++) {
        for (var _y = max(_r[1], _vy1); _y <= min(_r[3], _vy2); _y++) {
            var _k = _vertical ? _x : _y;
            if (abs(_k - _c) <= 1) continue;
            if (world_cell(_x, _y) != CELL.WALK) continue;
            if (random(1) >= _density) continue;
            instance_create_depth(cell_px(_x), cell_px(_y), 50, obj_hazard,
                { kind: "thunder", warn: def.thunder_warn, wave: thunder_wave, cue: (_count == 0) });
            _count += 1;
        }
    }
    if (_count > 0) aud_play("snd_thunder_warn", x, y);
}

function pharaoh_beam_length(_dir) {
    var _sx = x;
    var _sy = y - 110;
    for (var _d = 32; _d < 1500; _d += 16) {
        if (world_proj_blocked_px(_sx + lengthdir_x(_d, _dir), _sy + 100 + lengthdir_y(_d, _dir))) return _d;
    }
    return 1500;
}

function pharaoh_seg_dist(_px, _py, _x1, _y1, _x2, _y2) {
    var _dx = _x2 - _x1;
    var _dy = _y2 - _y1;
    var _l2 = _dx * _dx + _dy * _dy;
    if (_l2 <= 0) return point_distance(_px, _py, _x1, _y1);
    var _t = clamp(((_px - _x1) * _dx + (_py - _y1) * _dy) / _l2, 0, 1);
    return point_distance(_px, _py, _x1 + _t * _dx, _y1 + _t * _dy);
}

function pharaoh_draw() {
    var _fl = sin(anim_t / 20) * 6;
    var _alpha = 1;
    var _sink = 0;
    if (state == "teleport_out") { _alpha = 1 - t / 24; _sink = t; }
    else if (state == "teleport_in") { _alpha = t / 24; _sink = 24 - t; }
    draw_set_alpha(0.3 * _alpha);
    draw_ellipse_colour(x - 40, y - 12, x + 40, y + 12, c_black, c_black, false);
    draw_set_alpha(1);
    if (state == "dying") {
        var _ds = asset_or("spr_pharaoh_death", -1);
        if (_ds >= 0) {
            draw_sprite(_ds, min(sprite_get_number(_ds) - 1, floor(t * 12 / TPS)), x, y + _fl);
        } else {
            // placeholder disintegration: fade upward into sand motes
            var _k = clamp(t / 80, 0, 1);
            var _base = asset_or("spr_pharaoh_idle", spr_ph_pharaoh_idle);
            draw_sprite_ext(_base, 0, x, y + _fl - _k * 20, 1, 1 - _k * 0.3, 0, merge_colour(c_white, make_colour_rgb(230, 200, 140), _k), 1 - _k);
            draw_set_colour(make_colour_rgb(236, 210, 160));
            for (var i = 0; i < 24; i++) {
                var _a = i * 37 + t * 2;
                draw_set_alpha((1 - _k) * 0.8);
                draw_circle(x + lengthdir_x(20 + i * 2 + t, _a), y - 80 - t * (0.6 + (i mod 5) * 0.2), 2, false);
            }
            draw_set_alpha(1);
        }
        exit;
    }
    var _cast = (state == "summon" || state == "thunder" || state == "laser_charge" || state == "laser_fire");
    var _spr = asset_or(_cast ? "spr_pharaoh_thunder_cast" : "spr_pharaoh_idle", _cast ? spr_ph_pharaoh_cast : spr_ph_pharaoh_idle);
    var _n = sprite_get_number(_spr);
    draw_sprite_ext(_spr, (anim_t div 8) mod _n, x, y + _fl + _sink, 1, 1, 0, c_white, _alpha);
    if (flash > 0) {
        gpu_set_fog(true, c_white, 0, 1);
        draw_sprite_ext(_spr, (anim_t div 8) mod _n, x, y + _fl + _sink, 1, 1, 0, c_white, 0.5);
        gpu_set_fog(false, c_white, 0, 0);
    }
    var _sx = x;
    var _sy = y - 110 + _fl;
    if (state == "laser_charge") {
        var _locked = t >= def.laser_charge - def.laser_lock;
        var _k2 = t / def.laser_charge;
        draw_set_alpha(0.35 + 0.5 * _k2);
        draw_set_colour(_locked ? make_colour_rgb(255, 120, 110) : make_colour_rgb(255, 170, 150));
        draw_line_width(_sx, _sy, _sx + lengthdir_x(beam_len, aim_dir), _sy + lengthdir_y(beam_len, aim_dir), _locked ? 4 : 2);
        draw_set_colour(C_BOSS);
        draw_circle(_sx, _sy, 6 + 10 * _k2, false);
        draw_set_alpha(1);
    } else if (state == "laser_fire") {
        var _ex = _sx + lengthdir_x(beam_len, aim_dir);
        var _ey = _sy + lengthdir_y(beam_len, aim_dir);
        draw_set_alpha(0.55);
        draw_set_colour(C_BOSS);
        draw_line_width(_sx, _sy, _ex, _ey, def.laser_width + 8);
        draw_set_alpha(0.95);
        draw_set_colour(make_colour_rgb(255, 235, 255));
        draw_line_width(_sx, _sy, _ex, _ey, def.laser_width * 0.45);
        draw_set_alpha(1);
    }
}
