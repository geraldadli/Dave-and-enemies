/// Per-room scene bootstrap: builds collision from scene data, spawns content and places Dave.
if (!instance_exists(obj_game)) instance_create_depth(0, 0, -15000, obj_game);
scene_manager_create();
