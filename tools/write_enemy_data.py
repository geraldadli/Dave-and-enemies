"""
write_enemy_data.py - writes datafiles/data/enemies.json (engineering balance + art bindings).

Art bindings list candidates in order: the contracted asset ID first (used automatically once a
delivery is imported), then the labelled placeholder. Template "baddie" sprites use centre origins,
so they carry a dy offset that puts their feet on the contract's ground point. Run from the root.
"""
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def humanoid(entity, tint=None, scale=1.0):
    ph = {"ph": True, "scale": scale}

    def c(contract, template, dy):
        return [{"s": contract}, dict({"s": template, "dy": dy}, **ph)]
    art = {
        "idle": c("spr_%s_idle_down" % entity, "spr_baddie_idle", -38),
        "walk_down": c("spr_%s_walk_down" % entity, "spr_baddie_walk_down", -36),
        "walk_side": c("spr_%s_walk_side" % entity, "spr_baddie_walk_side", -36),
        "walk_up": c("spr_%s_walk_up" % entity, "spr_baddie_walk_up", -36),
        "attack_down": c("spr_%s_attack_down" % entity, "spr_baddie_attack_down", -35),
        "attack_side": c("spr_%s_attack_side" % entity, "spr_baddie_attack_side", -35),
        "attack_up": c("spr_%s_attack_up" % entity, "spr_baddie_attack_up", -35),
        "defeat": c("spr_%s_defeat" % entity, "spr_baddie_defeat", -40),
        "rise": c("spr_%s_rise" % entity, "spr_baddie_idle", -38),
    }
    return art


def ranged_art(entity, cast_anim):
    art = humanoid(entity)
    for d in ("down", "side", "up"):
        art["attack_" + d] = [{"s": "spr_%s_%s_%s" % (entity, cast_anim, d)}, art["attack_" + d][1]]
    return art


ENEMIES = {
    "undead": {
        "ai": "melee", "hp": 30, "damage": 10, "speed": 1.1, "attack_range": 58, "reach": 64,
        "windup": 30, "active": 10, "recover": 34, "xp": 12, "material": "bone", "knockback": 5,
        "hurt_r": 22, "hurt_cy": 30, "shadow_w": 22, "step_ticks": 28, "anim_fps": 12, "mask": "spr_mask_medium",
        "sounds": {"attack": "snd_undead_attack", "death": "snd_undead_death", "move": "snd_undead_move",
                   "rise": "snd_undead_rise"},
        "loot": [{"id": "gold_coins", "n": [2, 5], "chance": 0.45}, {"id": "potion_health", "n": 1, "chance": 0.08}],
        "art": humanoid("undead"),
    },
    "skeleton_warrior": {
        "ai": "melee", "hp": 46, "damage": 13, "speed": 1.6, "attack_range": 62, "reach": 70,
        "windup": 22, "active": 10, "recover": 26, "lunge": 2.5, "xp": 20, "material": "bone", "knockback": 4,
        "hurt_r": 22, "hurt_cy": 32, "shadow_w": 22, "step_ticks": 22, "anim_fps": 14, "mask": "spr_mask_medium",
        "ph_tint": [236, 232, 220],
        "sounds": {"attack": "snd_skeleton_warrior_attack", "death": "snd_skeleton_warrior_death",
                   "move": "snd_skeleton_warrior_move"},
        "loot": [{"id": "gold_coins", "n": [4, 9], "chance": 0.5}, {"id": "potion_health", "n": 1, "chance": 0.12}],
        "art": humanoid("skeleton_warrior", scale=1.05),
    },
    "skeleton_archer": {
        "ai": "archer", "hp": 30, "damage": 11, "speed": 1.5, "keep_min": 190, "keep_max": 330,
        "windup": 40, "recover": 30, "cooldown": [70, 120], "proj_speed": 7, "projectile": "arrow",
        "xp": 18, "material": "bone", "knockback": 4, "hurt_r": 22, "hurt_cy": 30, "shadow_w": 20,
        "step_ticks": 22, "anim_fps": 14, "mask": "spr_mask_medium", "ph_tint": [214, 210, 196],
        "spawn_offsets": {"side": [26, -48], "left": [26, -48], "down": [10, -44], "up": [-6, -58]},
        "release_frame": 5,
        "sounds": {"windup": "snd_bow_draw", "release": "snd_bow_release", "death": "snd_skeleton_archer_death",
                   "move": "snd_skeleton_archer_move"},
        "loot": [{"id": "gold_coins", "n": [3, 7], "chance": 0.5}, {"id": "ancient_coin", "n": 1, "chance": 0.1}],
        "art": humanoid("skeleton_archer", scale=0.95),
    },
    "bandit": {
        "ai": "melee", "hp": 40, "damage": 12, "speed": 2.3, "attack_range": 60, "reach": 68,
        "windup": 16, "active": 12, "recover": 22, "lunge": 3, "xp": 22, "material": "armor", "knockback": 4,
        "hurt_r": 22, "hurt_cy": 30, "shadow_w": 22, "step_ticks": 16, "anim_fps": 16, "mask": "spr_mask_medium",
        "ph_tint": [226, 182, 128],
        "sounds": {"attack": "snd_bandit_attack", "death": "snd_bandit_death", "move": "snd_bandit_move"},
        "loot": [{"id": "gold_coins", "n": [6, 12], "chance": 0.7}, {"id": "potion_health", "n": 1, "chance": 0.15}],
        "art": humanoid("bandit"),
    },
    "bandit_caster": {
        "ai": "caster", "hp": 34, "damage": 14, "speed": 1.3, "keep_min": 200, "keep_max": 340,
        "windup": 50, "recover": 34, "cooldown": [80, 130], "proj_speed": 3.6, "projectile": "orb",
        "xp": 24, "material": "", "knockback": 4, "hurt_r": 22, "hurt_cy": 30, "shadow_w": 20,
        "step_ticks": 24, "anim_fps": 12, "mask": "spr_mask_medium", "ph_tint": [176, 140, 226],
        "spawn_offsets": {"side": [30, -60], "left": [30, -60], "down": [14, -62], "up": [-10, -70]},
        "release_frame": 5,
        "sounds": {"windup": "snd_cast_charge", "release": "snd_magic_launch", "death": "snd_bandit_caster_death",
                   "move": "snd_bandit_caster_move"},
        "loot": [{"id": "gold_coins", "n": [6, 12], "chance": 0.6}, {"id": "potion_health", "n": 1, "chance": 0.2}],
        "art": ranged_art("bandit_caster", "cast"),
    },
    "bat": {
        "ai": "bat", "hp": 18, "damage": 8, "speed": 2.6, "dive_speed": 8, "windup": 28, "active": 20,
        "recover": 40, "cooldown": [100, 170], "xp": 10, "material": "", "knockback": 6,
        "hurt_r": 18, "hurt_cy": 10, "shadow_w": 14, "anim_fps": 15, "mask": "spr_mask_bat",
        "sounds": {"windup": "snd_bat_screech", "dive": "snd_bat_dive", "death": "snd_bat_defeat",
                   "move": "snd_bat_fly"},
        "loot": [{"id": "gold_coins", "n": [1, 3], "chance": 0.3}],
        "art": {
            "idle": [{"s": "spr_bat_fly_64"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
            "walk_down": [{"s": "spr_bat_fly_64"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
            "walk_side": [{"s": "spr_bat_fly_64"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
            "walk_up": [{"s": "spr_bat_fly_64"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
            "attack_down": [{"s": "spr_bat_dive"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
            "attack_side": [{"s": "spr_bat_dive"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
            "attack_up": [{"s": "spr_bat_dive"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
            "defeat": [{"s": "spr_bat_defeat"}, {"s": "spr_bat_fly", "dy": 0, "ph": True, "scale": 0.5}],
        },
    },
    "python": {
        "ai": "python", "hp": 44, "damage": 14, "speed": 1.4, "attack_range": 170, "windup": 40,
        "lunge": 8.5, "active": 18, "recover": 40, "xp": 26, "material": "", "knockback": 3,
        "hurt_r": 26, "hurt_cy": 14, "shadow_w": 34, "step_ticks": 34, "anim_fps": 12, "mask": "spr_mask_python",
        "sounds": {"windup": "snd_snake_hiss", "lunge": "snd_snake_lunge", "death": "snd_python_death",
                   "move": "snd_python_move"},
        "loot": [{"id": "gold_coins", "n": [4, 10], "chance": 0.5}, {"id": "potion_health", "n": 1, "chance": 0.15}],
        "art": {
            "idle": [{"s": "spr_python_slither_down"}, {"s": "spr_ph_python_slither"}],
            "walk_down": [{"s": "spr_python_slither_down"}, {"s": "spr_ph_python_slither"}],
            "walk_side": [{"s": "spr_python_slither_side"}, {"s": "spr_ph_python_slither"}],
            "walk_up": [{"s": "spr_python_slither_up"}, {"s": "spr_ph_python_slither"}],
            "attack_down": [{"s": "spr_python_coil"}, {"s": "spr_ph_python_coil"}],
            "attack_side": [{"s": "spr_python_coil"}, {"s": "spr_ph_python_coil"}],
            "attack_up": [{"s": "spr_python_coil"}, {"s": "spr_ph_python_coil"}],
            "defeat": [{"s": "spr_python_defeat"}, {"s": "spr_ph_python_coil"}],
        },
    },
    "sandworm": {
        "ai": "sandworm", "hp": 80, "damage": 18, "speed": 2.0, "windup": 50, "reach": 84, "exposed": 110,
        "active": 24, "xp": 45, "material": "", "knockback": 0, "hurt_r": 40, "hurt_cy": 50, "shadow_w": 44,
        "anim_fps": 10, "mask": "spr_mask_sandworm",
        "sounds": {"emerge": "snd_worm_emerge", "bite": "snd_worm_bite", "burrow": "snd_worm_burrow",
                   "death": "snd_sandworm_death"},
        "loot": [{"id": "gold_coins", "n": [10, 20], "chance": 0.8}, {"id": "potion_greater", "n": 1, "chance": 0.3}],
        "art": {
            "mound": [{"s": "spr_sandworm_mound"}, {"s": "spr_ph_sandworm_mound"}],
            "emerge": [{"s": "spr_sandworm_emerge"}, {"s": "spr_ph_sandworm_emerge"}],
            "idle": [{"s": "spr_sandworm_idle_up"}, {"s": "spr_ph_sandworm_idle"}],
            "attack_down": [{"s": "spr_sandworm_attack"}, {"s": "spr_ph_sandworm_attack"}],
            "attack_side": [{"s": "spr_sandworm_attack"}, {"s": "spr_ph_sandworm_attack"}],
            "attack_up": [{"s": "spr_sandworm_attack"}, {"s": "spr_ph_sandworm_attack"}],
            "defeat": [{"s": "spr_sandworm_defeat"}, {"s": "spr_ph_sandworm_emerge"}],
        },
    },
    "pharaoh": {
        "ai": "boss", "hp": 1400, "damage": 0, "hurt_r": 42, "hurt_cy": 80, "knockback": 0, "material": "armor",
        "laser_charge": 66, "laser_lock": 16, "laser_fire": 42, "laser_width": 26, "laser_damage": 14,
        "thunder_warn": 66, "thunder_density": [0.30, 0.38, 0.46],
        "wait": [[80, 110], [65, 90], [50, 75]],
        "tuning_note": "3-5 minute target with main-route gear (longsword or bandit scimitar, level 5-6); playtest required.",
    },
}

if __name__ == "__main__":
    with open(os.path.join(ROOT, "datafiles", "data", "enemies.json"), "w", encoding="utf-8") as f:
        json.dump(ENEMIES, f, indent=1)
    print("enemies.json written:", ", ".join(ENEMIES))
