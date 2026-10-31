// scr_data - loads Included Files (datafiles/data) into global.data.
// Delivered narrative files keep their authored format; adapters below resolve them by scene ID
// and zero-based line index, exposing stable line IDs (narrative_manifest.json) to callers.

function data_load_all() {
    global.data = {
        items: {},
        enemies: {},
        config: {},
        dialogue: {},
        narrative: {},
        storyboard: {},
        scenes: {},
        migration: {},
        load_errors: []
    };
    var _d = global.data;

    var _items = json_load_file("data/items.json");
    if (is_array(_items)) {
        for (var i = 0; i < array_length(_items); i++) {
            var _it = _items[i];
            _d.items[$ _it.id] = _it;
        }
    } else array_push(_d.load_errors, "data/items.json");

    var _en = json_load_file("data/enemies.json");
    if (is_struct(_en)) _d.enemies = _en; else array_push(_d.load_errors, "data/enemies.json");

    var _cfg = json_load_file("data/game_config.json");
    if (is_struct(_cfg)) _d.config = _cfg; else array_push(_d.load_errors, "data/game_config.json");

    var _dl = json_load_file("data/dialogue.json");
    if (is_struct(_dl)) _d.dialogue = _dl; else array_push(_d.load_errors, "data/dialogue.json");

    var _nm = json_load_file("data/narrative_manifest.json");
    if (is_struct(_nm)) _d.narrative = _nm; else array_push(_d.load_errors, "data/narrative_manifest.json");

    var _sb = json_load_file("data/intro_storyboard.json");
    if (is_struct(_sb)) _d.storyboard = _sb; else array_push(_d.load_errors, "data/intro_storyboard.json");

    var _mig = json_load_file("data/scene_migration.json");
    if (is_struct(_mig)) _d.migration = _mig; else array_push(_d.load_errors, "data/scene_migration.json");

    var _rooms = struct_or(_d.config, "scene_rooms", []);
    for (var i = 0; i < array_length(_rooms); i++) {
        var _sc = json_load_file("data/scenes/" + _rooms[i] + ".json");
        if (is_struct(_sc)) _d.scenes[$ _rooms[i]] = _sc;
        else array_push(_d.load_errors, "data/scenes/" + _rooms[i] + ".json");
    }
    if (array_length(_d.load_errors) > 0) {
        show_debug_message("DATA LOAD ERRORS: " + string(_d.load_errors));
    }
}

function item_def(_id) {
    if (!is_string(_id)) return undefined;
    return global.data.items[$ _id];
}

function item_name(_id) {
    var _d = item_def(_id);
    return is_undefined(_d) ? _id : _d.name;
}

/// Delivered icon (contract ID) when imported, else the labelled placeholder icon.
function item_icon(_id) {
    var _d = item_def(_id);
    if (is_undefined(_d)) return -1;
    return asset_or(_d.icon, asset_or(struct_or(_d, "icon_placeholder", ""), -1));
}

function enemy_def(_family) {
    return global.data.enemies[$ _family];
}

function scene_data(_room_name) {
    return global.data.scenes[$ _room_name];
}

function cfg(_key, _default) {
    return struct_or(global.data.config, _key, _default);
}

/// Resolves one authored dialogue entry plus its manifest metadata.
function dialogue_line(_scene_id, _index) {
    var _scene = global.data.dialogue[$ _scene_id];
    if (!is_struct(_scene)) return undefined;
    var _lines = _scene.lines;
    if (_index < 0 || _index >= array_length(_lines)) return undefined;
    var _src = _lines[_index];
    var _out = {
        scene_id: _scene_id,
        index: _index,
        line_id: _scene_id + "_" + string(_index),
        speaker: _src.speaker,
        text: _src.text,
        mood: struct_or(_src, "mood", "neutral"),
        expression: struct_or(_src, "mood", "neutral"),
        portrait_id: undefined,
        blip: "voice_" + _src.speaker
    };
    var _ids = struct_or(struct_or(global.data.narrative, "scene_line_ids", {}), _scene_id, undefined);
    if (is_array(_ids) && _index < array_length(_ids)) {
        var _meta = struct_or(struct_or(global.data.narrative, "lines", {}), _ids[_index], undefined);
        if (is_struct(_meta)) {
            _out.line_id = _meta.id;
            _out.expression = struct_or(_meta, "expression", _out.mood);
            _out.portrait_id = struct_or(_meta, "portrait_id", undefined);
            _out.blip = struct_or(_meta, "vocal_blip_profile", _out.blip);
        }
    }
    if (is_undefined(_out.portrait_id)) {
        var _sp = struct_or(struct_or(global.data.narrative, "speakers", {}), _out.speaker, undefined);
        if (is_struct(_sp)) _out.portrait_id = struct_or(_sp, "portrait_id", undefined);
    }
    return _out;
}

/// Finds a line by its stable manifest ID ("intro_040").
function dialogue_line_by_id(_line_id) {
    var _meta = struct_or(struct_or(global.data.narrative, "lines", {}), _line_id, undefined);
    if (!is_struct(_meta)) return undefined;
    return dialogue_line(_meta.scene_id, _meta.line_index);
}

function dialogue_count(_scene_id) {
    var _scene = global.data.dialogue[$ _scene_id];
    if (!is_struct(_scene)) return 0;
    return array_length(_scene.lines);
}

function speaker_name(_speaker) {
    var _sp = struct_or(struct_or(global.data.narrative, "speakers", {}), _speaker, undefined);
    return is_struct(_sp) ? struct_or(_sp, "display_name", "") : "";
}

/// Portrait sprite for a line: manifest expression variant, else the base portrait, else -1.
function portrait_sprite(_portrait_id, _expression) {
    if (!is_string(_portrait_id)) return -1;
    var _map = struct_or(struct_or(global.data.narrative, "portrait_expression_assets", {}), _portrait_id, undefined);
    var _name = _portrait_id;
    if (is_struct(_map)) {
        var _v = struct_or(_map, _expression, undefined);
        if (is_string(_v) && asset_get_index(_v) >= 0) _name = _v;
        else _name = struct_or(_map, "missing_expression_fallback", _portrait_id);
    }
    return asset_or(_name, asset_or(_portrait_id, -1));
}

/// Text of a single-line UI/objective scene (objective_desert, ui_boss_name ...).
function scene_text(_scene_id) {
    var _l = dialogue_line(_scene_id, 0);
    return is_struct(_l) ? _l.text : "";
}

function objective_duration_ticks(_objective) {
    var _ev = struct_or(struct_or(global.data.narrative, "objective_events", {}), _objective, undefined);
    var _s = is_struct(_ev) ? struct_or(_ev, "duration_s", 3) : 3;
    if (!is_real(_s)) _s = 3;
    return round(_s * TPS);
}
