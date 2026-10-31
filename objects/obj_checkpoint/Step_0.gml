anim += 1;
var _in = instance_exists(obj_player) && world_active() && point_distance(x, y, obj_player.x, obj_player.y) < 96;
if (_in) {
    global.toast.prompt = scene_text("checkpoint_prompt");
    near = true;
} else if (near) {
    near = false;
    global.toast.prompt = "";
}
