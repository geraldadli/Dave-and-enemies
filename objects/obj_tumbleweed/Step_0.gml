if (!world_active()) exit;
t += 1;
x -= spd;
hop = abs(sin(t / 9)) * 10;
spin += spd * 4;
if (t > 600 || x < global.cam_cx - 760) instance_destroy();
