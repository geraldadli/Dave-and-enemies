/// Title screen bootstrap (rm_menu). The menu itself is drawn and routed by obj_game.
if (!instance_exists(obj_game)) instance_create_depth(0, 0, -15000, obj_game);
title_open();
