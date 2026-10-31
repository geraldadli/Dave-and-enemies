/// Arena entrance gate or eastern seal. Closed barriers block walking and projectiles.
if (!variable_instance_exists(id, "kind")) kind = "arena";
if (!variable_instance_exists(id, "closed")) closed = false;
anim = closed ? 1 : 0;
anim_dir = 0;
sort_depth = true;
