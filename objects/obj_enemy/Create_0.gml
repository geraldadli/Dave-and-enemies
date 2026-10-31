/// Data-driven enemy (family set by the spawner).
if (!variable_instance_exists(id, "spawn_id")) spawn_id = "";
if (!variable_instance_exists(id, "family")) family = "undead";
if (!variable_instance_exists(id, "leash")) leash = undefined;
if (!variable_instance_exists(id, "persistent_spawn")) persistent_spawn = false;
if (!variable_instance_exists(id, "summoned")) summoned = false;
enemy_setup();
