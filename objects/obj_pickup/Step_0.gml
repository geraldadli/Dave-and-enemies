if (!world_active() || !instance_exists(obj_player)) exit;
bob += 1;
var _near = point_distance(x, y, obj_player.x, obj_player.y) < 40;
if (_near && touch_armed) {
    touch_armed = false;
    pickup_try();
} else if (!_near) touch_armed = true;
