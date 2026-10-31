/// Depth sort by ground point (contract section 7), then camera.
with (all) {
    if (variable_instance_exists(id, "sort_depth") && sort_depth) depth = -floor(y);
}
scene_manager_camera();
