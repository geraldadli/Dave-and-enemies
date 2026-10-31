var _s = asset_or("spr_tumbleweed", spr_ph_tumbleweed);
draw_set_alpha(0.25);
draw_ellipse_colour(x - 16, y - 4, x + 16, y + 4, c_black, c_black, false);
draw_set_alpha(1);
draw_sprite_ext(_s, 0, x, y - 22 - hop, 1, 1, spin, c_white, 1);
