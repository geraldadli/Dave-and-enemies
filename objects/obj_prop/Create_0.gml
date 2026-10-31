/// Solid prop: collides on its base footprint only (contract section 6).
if (!variable_instance_exists(id, "spr")) spr = spr_ph_prop;
if (!variable_instance_exists(id, "fp_w")) fp_w = 32;
if (!variable_instance_exists(id, "fp_h")) fp_h = 16;
mask_index = spr_mask_unit;
image_xscale = fp_w / 64;
image_yscale = fp_h / 64;
sort_depth = true;
