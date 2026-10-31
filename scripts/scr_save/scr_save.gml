// scr_save - three independent manual save slots, settings, snapshots and migration.
// A save file holds one complete snapshot of global.run (location, stats, inventory, equipment
// references, defeated spawn IDs, chest remainders, pending/claimed unique rewards, flags, seed).
// Writes go to a temporary file that is read back and validated before replacing the slot, so a
// failed write leaves the previous save intact. Settings live in settings.json, never in a slot.

function save_path(_slot) { return "save_" + string(_slot + 1) + ".json"; }

// ------------------------------------------------------------------ settings
function settings_defaults() {
    return { music: 0.7, sfx: 0.8, blips: 0.65, reduced_flash: false, shake: true, fullscreen: false };
}

function settings_load() {
    global.settings = settings_defaults();
    var _s = json_load_file("settings.json");
    if (!is_struct(_s)) return;
    var _k = variable_struct_get_names(global.settings);
    for (var i = 0; i < array_length(_k); i++) {
        var _v = _s[$ _k[i]];
        if (!is_undefined(_v)) global.settings[$ _k[i]] = _v;
    }
    global.settings.music = clamp(global.settings.music, 0, 1);
    global.settings.sfx = clamp(global.settings.sfx, 0, 1);
    global.settings.blips = clamp(global.settings.blips, 0, 1);
}

function settings_save() {
    return json_save_file("settings.json", global.settings);
}

// ------------------------------------------------------------------ run state
function run_new() {
    var _start = cfg("initial", { room: "rm_sc_desert_frontier", cell: [7, 40], facing: "side" });
    var _r = {
        version: SAVE_VERSION,
        scene_room: _start.room,
        pos_x: cell_px(_start.cell[0]),
        pos_y: cell_px(_start.cell[1]),
        facing: _start.facing,
        checkpoint_id: "",
        location: "Desert Arrival",
        hp: cfg("base_hp", 100),
        level: 1,
        xp: 0,
        inv: array_create(INV_SIZE, undefined),
        eq_weapon: -1,
        eq_armor: -1,
        hot_sel: 0,
        defeated: {},
        chests: {},
        rewards: {},
        flags: {
            intro_seen: false, boss_intro_seen: false, boss_pharaoh_defeated: false,
            grail_recovered: false, chapter_1_complete: false, ending_seen: false, desert_arrival_seen: false
        },
        seed: irandom(999999),
        playtime: 0,
        objective: "objective_desert"
    };
    global.run = _r;
    var _loadout = cfg("starting_loadout", []);
    for (var i = 0; i < array_length(_loadout); i++) {
        var _it = _loadout[i];
        inv_set(i, { id: _it.id, n: _it.n });
        if (struct_or(_it, "equip", false)) inv_equip(i);
    }
    _r.hp = player_max_hp();
    return _r;
}

function flag(_name) {
    return struct_or(global.run.flags, _name, false);
}

function flag_set(_name, _value) {
    global.run.flags[$ _name] = _value;
}

/// Complete deep copy of the run state.
function snapshot_make() {
    return variable_clone(global.run);
}

/// Replaces the whole run with a snapshot (death rollback / load). Never mixes states.
function snapshot_restore(_snap) {
    global.run = variable_clone(_snap);
    var _inv = global.run.inv;
    if (!is_array(_inv) || array_length(_inv) != INV_SIZE) {
        var _fixed = array_create(INV_SIZE, undefined);
        if (is_array(_inv)) for (var i = 0; i < min(INV_SIZE, array_length(_inv)); i++) _fixed[i] = _inv[i];
        global.run.inv = _fixed;
    }
    for (var i = 0; i < INV_SIZE; i++) if (!is_struct(global.run.inv[i])) global.run.inv[i] = undefined;
}

// ------------------------------------------------------------------ slot metadata
/// Returns { state: "empty"|"ok"|"bad", reason, data, location, level, playtime, date }.
function save_read(_slot) {
    var _p = save_path(_slot);
    if (!file_exists(_p)) return { state: "empty", reason: "", data: undefined };
    var _d = json_load_file(_p);
    if (!is_struct(_d)) return { state: "bad", reason: "The save file is damaged.", data: undefined };
    var _v = struct_or(_d, "version", 0);
    if (_v != SAVE_VERSION) {
        var _m = save_migrate(_d, _slot);
        if (!_m.ok) return { state: "bad", reason: _m.reason, data: undefined };
        _d = _m.data;
    }
    var _run = struct_or(_d, "run", undefined);
    if (!is_struct(_run) || is_undefined(scene_data(struct_or(_run, "scene_room", "")))) {
        return { state: "bad", reason: "This save refers to an unknown scene.", data: undefined };
    }
    return {
        state: "ok", reason: "", data: _d,
        location: struct_or(_d, "location", struct_or(_run, "location", "Desert")),
        level: struct_or(_run, "level", 1),
        playtime: struct_or(_run, "playtime", 0),
        date: struct_or(_d, "saved_at", "")
    };
}

function save_any_valid() {
    for (var i = 0; i < SAVE_SLOTS; i++) if (save_read(i).state == "ok") return true;
    return false;
}

/// Writes a snapshot to a slot. Returns { ok, msg }. The previous file survives any failure.
function save_write(_slot, _snap) {
    var _p = save_path(_slot);
    var _tmp = _p + ".tmp";
    var _bak = _p + ".bak";
    var _doc = {
        version: SAVE_VERSION,
        chapter: "chapter_1_desert",
        saved_at: fmt_date(date_current_datetime()),
        location: struct_or(_snap, "location", "Desert"),
        run: _snap
    };
    if (file_exists(_tmp)) file_delete(_tmp);
    if (!json_save_file(_tmp, _doc)) {
        if (file_exists(_tmp)) file_delete(_tmp);
        return { ok: false, msg: "Save failed. Your previous save is unchanged. Try again." };
    }
    var _chk = json_load_file(_tmp);
    if (!is_struct(_chk) || struct_or(_chk, "version", 0) != SAVE_VERSION || !is_struct(struct_or(_chk, "run", undefined))) {
        file_delete(_tmp);
        return { ok: false, msg: "Save failed. Your previous save is unchanged. Try again." };
    }
    var _had_old = file_exists(_p);
    if (_had_old) {
        if (file_exists(_bak)) file_delete(_bak);
        if (!file_rename(_p, _bak)) {
            file_delete(_tmp);
            return { ok: false, msg: "Save failed. Your previous save is unchanged. Try again." };
        }
    }
    if (!file_rename(_tmp, _p)) {
        if (_had_old && file_exists(_bak)) file_rename(_bak, _p);
        if (file_exists(_tmp)) file_delete(_tmp);
        return { ok: false, msg: "Save failed. Your previous save is unchanged. Try again." };
    }
    return { ok: true, msg: "Saved to slot " + string(_slot + 1) + ". Health restored." };
}

// ------------------------------------------------------------------ migration
/// Version 1 = the superseded 24-room draft. Checkpoint location and persistent identities migrate
/// together through scene_migration.json; anything without a mapped checkpoint is incompatible.
/// The original file is preserved as save_N.v1.json before any migrated data is used.
function save_migrate(_d, _slot) {
    var _v = struct_or(_d, "version", 0);
    if (_v != 1) return { ok: false, reason: "This save was made by an incompatible version (format " + string(_v) + ")." };
    var _mig = global.data.migration;
    var _old = struct_or(_d, "run", undefined);
    if (!is_struct(_old) || !is_struct(_mig)) return { ok: false, reason: "This save is incomplete." };
    var _cp_old = struct_or(_old, "checkpoint_id", "");
    var _cp = struct_or(struct_or(_mig, "checkpoints", {}), _cp_old, undefined);
    if (!is_struct(_cp)) return { ok: false, reason: "This old save has no checkpoint that exists in the new desert." };
    var _room = "rm_" + _cp.scene_id;
    var _new = variable_clone(_old);
    _new.version = SAVE_VERSION;
    _new.scene_room = _room;
    _new.pos_x = cell_px(_cp.respawn_cell[0]);
    _new.pos_y = cell_px(_cp.respawn_cell[1]);
    _new.checkpoint_id = _cp.id;
    // chests: legacy id -> scene id (remaining contents move with their identity)
    var _chests = {};
    var _oc = struct_or(_old, "chests", {});
    var _ck = variable_struct_get_names(_oc);
    for (var i = 0; i < array_length(_ck); i++) {
        var _map = struct_or(struct_or(_mig, "chests", {}), _ck[i], undefined);
        var _nid = is_struct(_map) ? _map.id : _ck[i];
        _chests[$ _nid] = _oc[$ _ck[i]];
    }
    _new.chests = _chests;
    var _rew = {};
    var _or = struct_or(_old, "rewards", {});
    var _rk = variable_struct_get_names(_or);
    for (var i = 0; i < array_length(_rk); i++) {
        var _map2 = struct_or(struct_or(_mig, "unique_rewards", {}), _rk[i], undefined);
        var _nid2 = is_struct(_map2) ? _map2.id : _rk[i];
        _rew[$ _nid2] = _or[$ _rk[i]];
    }
    _new.rewards = _rew;
    // enemy spawn IDs are stable across the migration and are kept as-is
    var _keep = save_path(_slot) + ".v1.json";
    if (!file_exists(_keep)) file_copy(save_path(_slot), _keep);
    var _doc = variable_clone(_d);
    _doc.version = SAVE_VERSION;
    _doc.run = _new;
    return { ok: true, reason: "", data: _doc };
}
