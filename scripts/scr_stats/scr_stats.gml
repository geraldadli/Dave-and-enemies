// scr_stats - progression, derived stats and damage acceptance.

function xp_to_next(_level) {
    var _base = cfg("xp_base", 30);
    var _exp = cfg("xp_exponent", 1.5);
    return round(_base * power(_level, _exp));
}

function player_max_hp() {
    var _r = global.run;
    var _hp = cfg("base_hp", 100) + cfg("hp_per_level", 6) * (_r.level - 1);
    var _a = equipped_armor_id();
    if (_a != "") _hp += item_stat(_a, "max_hp_bonus", 0);
    return _hp;
}

function player_attack() {
    var _w = equipped_weapon_id();
    var _base = (_w == "") ? cfg("unarmed_damage", 4) : item_stat(_w, "damage", 4);
    return _base + (global.run.level - 1);
}

function player_defense() {
    var _a = equipped_armor_id();
    var _base = (_a == "") ? 0 : item_stat(_a, "defense", 0);
    return _base + floor((global.run.level - 1) / 2);
}

function player_weapon_stat(_key, _default) {
    var _w = equipped_weapon_id();
    if (_w == "") return _default;
    return item_stat(_w, _key, _default);
}

/// Awards XP; consolidates several level-ups into one cue. Returns levels gained.
function grant_xp(_n) {
    var _r = global.run;
    if (_r.level >= MAX_LEVEL) return 0;
    _r.xp += _n;
    var _gained = 0;
    while (_r.level < MAX_LEVEL && _r.xp >= xp_to_next(_r.level)) {
        _r.xp -= xp_to_next(_r.level);
        _r.level += 1;
        _gained += 1;
        _r.hp = min(_r.hp + cfg("hp_per_level", 6), player_max_hp());
    }
    if (_r.level >= MAX_LEVEL) _r.xp = 0;
    if (_gained > 0) {
        aud_play("snd_levelup");
        toast_show("Level " + string(_r.level), 150, C_GOLD);
        if (instance_exists(obj_player)) {
            instance_create_depth(obj_player.x, obj_player.y, obj_player.depth - 1, obj_fx, { kind: "levelup", owner: obj_player.id });
        }
    }
    return _gained;
}

/// Global switch that gates every damage source (transitions, cinematics, boss defeat).
function combat_enabled() {
    return world_active() && !global.damage_paused;
}

/// Damage to Dave after invulnerability and acceptance checks. Returns true when HP decreased.
function damage_player(_amount, _src_x, _src_y, _kind = "melee") {
    if (!combat_enabled()) return false;
    if (!instance_exists(obj_player)) return false;
    var _p = obj_player.id;
    if (_p.state == "dead" || _p.iframes > 0 || _p.scripted) return false;
    var _def = player_defense();
    var _dmg = max(1, round(_amount * 15 / (15 + _def)));
    var _r = global.run;
    _r.hp = max(0, _r.hp - _dmg);
    global.hp_ghost = max(global.hp_ghost, _r.hp + _dmg);
    global.hp_ghost_t = ms_ticks(250);
    _p.iframes = DAVE_IFRAMES;
    _p.hurt_t = 12;
    var _a = point_direction(_src_x, _src_y, _p.x, _p.y);
    _p.kb_x = lengthdir_x(5, _a);
    _p.kb_y = lengthdir_y(5, _a);
    shake_camera(4, 10);
    if (_r.hp <= 0) {
        aud_play("snd_player_defeated");
        with (_p) player_die();
    } else {
        aud_play("snd_hurt");
        if (_kind == "melee") aud_play("snd_enemy_melee_hit", _src_x, _src_y);
        else if (_kind == "laser") aud_play("snd_laser_hit");
    }
    return true;
}
