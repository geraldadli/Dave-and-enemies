// scr_inventory - 40-entry storage (0-7 main slots, 8-39 storage grid) with equipment references.
// Equipment fields hold indices of entries already in storage; they never add capacity or copies.

function inv_get(_i) {
    if (_i < 0 || _i >= INV_SIZE) return undefined;
    var _e = global.run.inv[_i];
    return is_struct(_e) ? _e : undefined;
}

function inv_set(_i, _e) {
    global.run.inv[_i] = _e;
}

function item_stack(_id) {
    var _d = item_def(_id);
    return is_undefined(_d) ? 1 : max(1, _d.stack);
}

function item_type(_id) {
    var _d = item_def(_id);
    return is_undefined(_d) ? "valuable" : _d.type;
}

function item_stat(_id, _key, _default) {
    var _d = item_def(_id);
    if (is_undefined(_d)) return _default;
    return struct_or(struct_or(_d, "stats", {}), _key, _default);
}

/// Simulates adding; returns how many of n would fit.
function inv_fit_count(_id, _n) {
    var _cap = item_stack(_id);
    var _left = _n;
    for (var i = 0; i < INV_SIZE && _left > 0; i++) {
        var _e = inv_get(i);
        if (is_struct(_e) && _e.id == _id) _left -= min(_left, _cap - _e.n);
    }
    for (var i = 0; i < INV_SIZE && _left > 0; i++) {
        if (!is_struct(inv_get(i))) _left -= min(_left, _cap);
    }
    return _n - _left;
}

/// Adds up to n items (merging first, then empty slots). Returns the remainder that did not fit.
function inv_add(_id, _n) {
    var _cap = item_stack(_id);
    var _left = _n;
    for (var i = 0; i < INV_SIZE && _left > 0; i++) {
        var _e = inv_get(i);
        if (is_struct(_e) && _e.id == _id && _e.n < _cap) {
            var _k = min(_left, _cap - _e.n);
            _e.n += _k;
            _left -= _k;
        }
    }
    for (var i = 0; i < INV_SIZE && _left > 0; i++) {
        if (!is_struct(inv_get(i))) {
            var _k = min(_left, _cap);
            inv_set(i, { id: _id, n: _k });
            _left -= _k;
        }
    }
    return _left;
}

function inv_storage_count() {
    var _c = 0;
    for (var i = HOTBAR; i < INV_SIZE; i++) if (is_struct(inv_get(i))) _c++;
    return _c;
}

function inv_all_occupied() {
    for (var i = 0; i < INV_SIZE; i++) if (!is_struct(inv_get(i))) return false;
    return true;
}

/// Gives a loot list [[id, n], ...]; returns { remaining, added_any, gold, levels }.
/// Partial pickups take what fits and leave the exact remainder (UI_SPEC section 5).
function inv_give_loot(_loot) {
    var _rem = [];
    var _added = false;
    var _gold = false;
    for (var i = 0; i < array_length(_loot); i++) {
        var _id = _loot[i][0];
        var _n = _loot[i][1];
        if (is_undefined(item_def(_id))) continue;
        var _left = inv_add(_id, _n);
        if (_left < _n) {
            _added = true;
            if (_id == "gold_coins") _gold = true;
        }
        if (_left > 0) array_push(_rem, [_id, _left]);
    }
    return { remaining: _rem, added_any: _added, gold: _gold };
}

function inv_fix_refs_after_move(_src, _dst, _swapped) {
    var _r = global.run;
    if (_r.eq_weapon == _src) _r.eq_weapon = _dst;
    else if (_swapped && _r.eq_weapon == _dst) _r.eq_weapon = _src;
    if (_r.eq_armor == _src) _r.eq_armor = _dst;
    else if (_swapped && _r.eq_armor == _dst) _r.eq_armor = _src;
}

/// Commits a move. Returns "cancel", "moved", "merged", "partial" or "swapped". Nothing is lost.
function inv_move(_src, _dst) {
    if (_src == _dst) return "cancel";
    var _a = inv_get(_src);
    if (!is_struct(_a)) return "cancel";
    var _b = inv_get(_dst);
    if (!is_struct(_b)) {
        inv_set(_dst, _a);
        inv_set(_src, undefined);
        inv_fix_refs_after_move(_src, _dst, false);
        return "moved";
    }
    if (_b.id == _a.id && item_stack(_a.id) > 1) {
        var _cap = item_stack(_a.id);
        var _k = min(_a.n, _cap - _b.n);
        if (_k <= 0) {
            inv_set(_dst, _a);
            inv_set(_src, _b);
            inv_fix_refs_after_move(_src, _dst, true);
            return "swapped";
        }
        _b.n += _k;
        _a.n -= _k;
        if (_a.n <= 0) {
            inv_set(_src, undefined);
            return "merged";
        }
        return "partial";
    }
    inv_set(_dst, _a);
    inv_set(_src, _b);
    inv_fix_refs_after_move(_src, _dst, true);
    return "swapped";
}

function equipped_weapon_id() {
    var _e = inv_get(global.run.eq_weapon);
    return is_struct(_e) ? _e.id : "";
}

function equipped_armor_id() {
    var _e = inv_get(global.run.eq_armor);
    return is_struct(_e) ? _e.id : "";
}

function inv_is_equipped(_i) {
    return _i >= 0 && (_i == global.run.eq_weapon || _i == global.run.eq_armor);
}

/// Primary action label for an entry (UI_SPEC section 5).
function inv_primary_label(_i) {
    var _e = inv_get(_i);
    if (!is_struct(_e)) return "No action";
    if (inv_is_equipped(_i)) return "Equipped";
    switch (item_type(_e.id)) {
        case "consumable": return "Use";
        case "weapon": case "armor": return "Equip";
        default: return "No action";
    }
}

/// Whether the primary action can run now, and why not.
function inv_primary_state(_i) {
    var _e = inv_get(_i);
    if (!is_struct(_e)) return { ok: false, reason: "Move an item here." };
    if (inv_is_equipped(_i)) return { ok: false, reason: "Already equipped." };
    switch (item_type(_e.id)) {
        case "consumable":
            if (global.run.hp >= player_max_hp()) return { ok: false, reason: "Health is already full." };
            return { ok: true, reason: "" };
        case "weapon": case "armor":
            return { ok: true, reason: "" };
        default:
            return { ok: false, reason: "Valuables have no use in this chapter." };
    }
}

/// Uses a consumable. Accepted only when HP actually increases.
function inv_use(_i) {
    var _e = inv_get(_i);
    if (!is_struct(_e) || item_type(_e.id) != "consumable") return { ok: false, msg: "Nothing to use." };
    var _max = player_max_hp();
    if (global.run.hp >= _max) return { ok: false, msg: "Health is already full." };
    var _heal = min(item_stat(_e.id, "heal", 30), _max - global.run.hp);
    global.run.hp += _heal;
    _e.n -= 1;
    if (_e.n <= 0) inv_set(_i, undefined);
    aud_play("snd_potion_drink");
    aud_play("snd_heal");
    if (instance_exists(obj_player)) {
        instance_create_depth(obj_player.x, obj_player.y, obj_player.depth + 1, obj_fx, { kind: "heal_ring", owner: obj_player.id });
        obj_player.flash_heal = 30;
    }
    return { ok: true, msg: "Restored " + string(_heal) + " HP." };
}

function inv_equip(_i) {
    var _e = inv_get(_i);
    if (!is_struct(_e)) return false;
    var _t = item_type(_e.id);
    if (_t == "weapon") global.run.eq_weapon = _i;
    else if (_t == "armor") global.run.eq_armor = _i;
    else return false;
    global.run.hp = min(global.run.hp, player_max_hp());
    return true;
}

/// Description line under the item name: type plus actual resulting stat comparison.
function inv_type_line(_i) {
    var _e = inv_get(_i);
    if (!is_struct(_e)) return "";
    var _id = _e.id;
    switch (item_type(_id)) {
        case "consumable": return "Consumable / Restores " + string(item_stat(_id, "heal", 0)) + " HP";
        case "weapon":
            var _cur = player_attack();
            var _new = item_stat(_id, "damage", 0) + (global.run.level - 1);
            if (inv_is_equipped(_i)) return "Weapon / Damage " + string(_cur);
            return "Weapon / Damage " + string(_cur) + " to " + string(_new);
        case "armor":
            var _cd = player_defense();
            var _nd = item_stat(_id, "defense", 0) + floor((global.run.level - 1) / 2);
            if (inv_is_equipped(_i)) return "Armor / Defense " + string(_cd);
            return "Armor / Defense " + string(_cd) + " to " + string(_nd);
        default: return "Valuable / No action";
    }
}
