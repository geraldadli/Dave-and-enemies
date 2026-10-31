// scr_story - interactions (chests, stars, spring, rewards) and arrival/intro handoff.

/// Data of the save star Dave stands at, or undefined.
function checkpoint_in_range() {
    if (!instance_exists(obj_player)) return undefined;
    var _px = obj_player.x;
    var _py = obj_player.y;
    var _out = undefined;
    with (obj_checkpoint) {
        if (point_distance(_px, _py, x, y) < 96) _out = { id: cp_id, respawn: respawn, location: location };
    }
    return _out;
}

/// Gives a loot list and plays one feedback cue for the accepted batch. Returns the remainder.
function loot_transaction(_loot) {
    var _res = inv_give_loot(_loot);
    if (_res.added_any) {
        if (_res.gold) aud_play("snd_coin", undefined, undefined, "", false);
        else aud_play("snd_pickup", undefined, undefined, "", false);
        var _txt = "";
        for (var i = 0; i < array_length(_loot); i++) {
            var _got = _loot[i][1];
            for (var j = 0; j < array_length(_res.remaining); j++) {
                if (_res.remaining[j][0] == _loot[i][0]) _got -= _res.remaining[j][1];
            }
            if (_got <= 0) continue;
            if (_txt != "") _txt += ", ";
            _txt += item_name(_loot[i][0]) + ((_got > 1) ? (" ×" + string(_got)) : "");
        }
        toast_show("Found " + _txt + ".", 150, C_TEXT);
    }
    if (array_length(_res.remaining) > 0) {
        toast_show("Inventory full. Loot remains here.", 108, C_ERROR);
        if (!_res.added_any) aud_play("snd_ui_error", undefined, undefined, "", false);
    }
    return _res.remaining;
}

// ------------------------------------------------------------------ chest (obj_chest scope)
function chest_setup() {
    if (!variable_instance_exists(id, "chest_id")) chest_id = "";
    if (!variable_instance_exists(id, "loot_all")) loot_all = [];
    var _st = struct_or(global.run.chests, chest_id, undefined);
    opened = is_array(_st);
    remaining = opened ? _st : loot_all;
    opened_empty = opened && array_length(remaining) == 0;
    lid = opened ? 1 : 0;
    lid_t = -1;
    sort_depth = true;
    // base footprint 48x20 (ASSET_REQUESTS A7) on the shared unit mask
    mask_index = spr_mask_unit;
    image_xscale = 48 / 64;
    image_yscale = 20 / 64;
}

function chest_interact() {
    if (opened_empty) return;
    if (!opened) {
        opened = true;
        lid_t = 0;
        aud_play("snd_chest_open", x, y);
        global.run.chests[$ chest_id] = remaining;
    }
    remaining = loot_transaction(remaining);
    global.run.chests[$ chest_id] = remaining;
    opened_empty = array_length(remaining) == 0;
}

// ------------------------------------------------------------------ star checkpoint
function checkpoint_interact() {
    if (ui_top() != -1) return;
    aud_play("snd_checkpoint", undefined, undefined, "", false);
    saveload_open("save", "checkpoint", { id: cp_id, respawn: respawn, location: location });
}

// ------------------------------------------------------------------ healing spring
function spring_interact() {
    var _max = player_max_hp();
    if (global.run.hp >= _max) return;   // at full HP do nothing
    global.run.hp = _max;
    aud_play("snd_heal", undefined, undefined, "", false);
    if (instance_exists(obj_player)) {
        obj_player.flash_heal = 30;
        instance_create_depth(obj_player.x, obj_player.y, obj_player.depth + 1, obj_fx, { kind: "heal_ring", owner: obj_player.id });
    }
    toast_show("The spring restores your strength.", 120, C_SUCCESS);
}

// ------------------------------------------------------------------ pickups and the unique reward
function pickup_setup() {
    if (!variable_instance_exists(id, "loot")) loot = [];
    if (!variable_instance_exists(id, "reward_id")) reward_id = "";
    if (!variable_instance_exists(id, "persistent_reward")) persistent_reward = false;
    touch_armed = true;
    bob = random(100);
    sort_depth = true;
}

function pickup_try() {
    var _rem = loot_transaction(loot);
    loot = _rem;
    if (array_length(loot) == 0) {
        if (reward_id != "") global.run.rewards[$ reward_id] = "claimed";
        instance_destroy();
    }
}

// ------------------------------------------------------------------ arrival
/// Runs after obj_manager placed Dave in a freshly loaded scene.
function scene_arrival_ready() {
    var _why = global.after_arrival;
    global.after_arrival = "";
    if (_why == "intro") {
        toast_objective("objective_desert");
        // safe initial restart snapshot until the first manual save
        global.initial_snapshot = snapshot_make();
        global.last_saved_playtime = -1;
    }
}
