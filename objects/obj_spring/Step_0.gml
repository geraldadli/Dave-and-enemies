var _in = instance_exists(obj_player) && world_active() && rect_has_px(rect, obj_player.x, obj_player.y);
if (_in) {
    if (!near && global.toast.prompt == "") global.toast.prompt = "E  Drink from the spring";
    near = true;
} else if (near) {
    near = false;
    if (global.toast.prompt == "E  Drink from the spring") global.toast.prompt = "";
}
