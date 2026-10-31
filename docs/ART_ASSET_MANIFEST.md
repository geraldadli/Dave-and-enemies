# Dave’s and Enemies art asset manifest

Art-only handoff for Claude. Exact contract IDs are preserved; proposed wildcard expansions and undefined layout choices are identified. Assets include planned artwork, generated sources and existing supplied UI prototypes; none is marked engine-verified. Timing and geometry marked proposed are art recommendations, not edits to engineering data.

The complete machine-readable specification is [asset_manifest.json](../art/asset_manifest.json). Every entry contains dimensions, origin, transparency, states, direction, frame count, timing, dependencies, inspection checklist and a complete copy-ready prompt file.

## Milestone A

| Asset ID | Pri | Target per frame | Origin | States and playback | Prompt | Native delivery |
|---|---|---|---|---|---|---|
| `spr_dave_idle_down` | P0 | 96×96 | [48, 88] | 8 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_a/spr_dave_idle_down.txt) | [strip](../art/exports/dave/down_v001/spr_dave_idle_down/spr_dave_idle_down_strip8.png) · [timing](../art/exports/dave/down_v001/spr_dave_idle_down/spr_dave_idle_down.json) · engine check pending |
| `spr_dave_walk_down` | P0 | 96×96 | [48, 88] | 10 f; 20 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_dave_walk_down.txt) | [strip](../art/exports/dave/down_v001/spr_dave_walk_down/spr_dave_walk_down_strip10.png) · [timing](../art/exports/dave/down_v001/spr_dave_walk_down/spr_dave_walk_down.json) · engine check pending |
| `spr_dave_attack_down` | P0 | 128×128 | [64, 112] | 8 f; engine timed [3, 3, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_dave_attack_down.txt) | [strip](../art/exports/dave/down_v001/spr_dave_attack_down/spr_dave_attack_down_strip8.png) · [timing](../art/exports/dave/down_v001/spr_dave_attack_down/spr_dave_attack_down.json) · engine check pending |
| `spr_dave_idle_down_side` | P0 | 96×96 | [48, 88] | 8 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_a/spr_dave_idle_down_side.txt) | planned/source only |
| `spr_dave_walk_down_side` | P0 | 96×96 | [48, 88] | 10 f; 20 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_dave_walk_down_side.txt) | planned/source only |
| `spr_dave_attack_down_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [3, 3, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_dave_attack_down_side.txt) | planned/source only |
| `spr_dave_idle_side` | P0 | 96×96 | [48, 88] | 8 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_a/spr_dave_idle_side.txt) | planned/source only |
| `spr_dave_walk_side` | P0 | 96×96 | [48, 88] | 10 f; 20 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_dave_walk_side.txt) | [strip](../art/exports/dave/cardinal_v001/spr_dave_walk_side/spr_dave_walk_side_strip10.png) · [timing](../art/exports/dave/cardinal_v001/spr_dave_walk_side/spr_dave_walk_side.json) · engine check pending |
| `spr_dave_attack_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [3, 3, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_dave_attack_side.txt) | [strip](../art/exports/dave/cardinal_v001/spr_dave_attack_side/spr_dave_attack_side_strip8.png) · [timing](../art/exports/dave/cardinal_v001/spr_dave_attack_side/spr_dave_attack_side.json) · engine check pending |
| `spr_dave_idle_up_side` | P0 | 96×96 | [48, 88] | 8 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_a/spr_dave_idle_up_side.txt) | planned/source only |
| `spr_dave_walk_up_side` | P0 | 96×96 | [48, 88] | 10 f; 20 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_dave_walk_up_side.txt) | planned/source only |
| `spr_dave_attack_up_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [3, 3, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_dave_attack_up_side.txt) | planned/source only |
| `spr_dave_idle_up` | P0 | 96×96 | [48, 88] | 8 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_a/spr_dave_idle_up.txt) | planned/source only |
| `spr_dave_walk_up` | P0 | 96×96 | [48, 88] | 10 f; 20 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_dave_walk_up.txt) | [strip](../art/exports/dave/cardinal_v001/spr_dave_walk_up/spr_dave_walk_up_strip10.png) · [timing](../art/exports/dave/cardinal_v001/spr_dave_walk_up/spr_dave_walk_up.json) · engine check pending |
| `spr_dave_attack_up` | P0 | 128×128 | [64, 112] | 8 f; engine timed [3, 3, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_dave_attack_up.txt) | [strip](../art/exports/dave/cardinal_v001/spr_dave_attack_up/spr_dave_attack_up_strip8.png) · [timing](../art/exports/dave/cardinal_v001/spr_dave_attack_up/spr_dave_attack_up.json) · engine check pending |
| `spr_dave_walk_left` | P0 | 96×96 | [48, 88] | 10 f; 20 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_dave_walk_left.txt) | [strip](../art/exports/dave/cardinal_v001/spr_dave_walk_left/spr_dave_walk_left_strip10.png) · [timing](../art/exports/dave/cardinal_v001/spr_dave_walk_left/spr_dave_walk_left.json) · engine check pending |
| `spr_dave_attack_left` | P0 | 128×128 | [64, 112] | 8 f; engine timed [3, 3, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_dave_attack_left.txt) | [strip](../art/exports/dave/cardinal_v001/spr_dave_attack_left/spr_dave_attack_left_strip8.png) · [timing](../art/exports/dave/cardinal_v001/spr_dave_attack_left/spr_dave_attack_left.json) · engine check pending |
| `spr_fx_slash` | P0 | 128×96 | [16, 48] | 4 f; 20 fps; once; animation | [prompt](../art/prompts/milestone_a/spr_fx_slash.txt) | planned/source only |
| `tex_sand_light` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt 1](../art/prompts/milestone_a/tex_sand_light.ripples.txt) · [prompt 2](../art/prompts/milestone_a/tex_sand_light.pebbles.txt) · [prompt 3](../art/prompts/milestone_a/tex_sand_light.cracks.txt) | planned/source only |
| `tex_sand_dark` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/tex_sand_dark.txt) | planned/source only |
| `tex_rock_top` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/tex_rock_top.txt) | planned/source only |
| `tex_cliff_face` | P0 | 256×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/tex_cliff_face.txt) | planned/source only |
| `spr_undead_idle_down` | P0 | 128×128 | [64, 112] | 6 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_a/spr_undead_idle_down.txt) | planned/source only |
| `spr_undead_walk_down` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_undead_walk_down.txt) | planned/source only |
| `spr_undead_attack_down` | P0 | 128×128 | [64, 112] | 8 f; engine timed [6, 6, 6, 6, 4, 4, 7, 7] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_undead_attack_down.txt) | planned/source only |
| `spr_undead_walk_side` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_undead_walk_side.txt) | planned/source only |
| `spr_undead_attack_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [6, 6, 6, 6, 4, 4, 7, 7] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_undead_attack_side.txt) | planned/source only |
| `spr_undead_walk_up` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; loop; walk | [prompt](../art/prompts/milestone_a/spr_undead_walk_up.txt) | planned/source only |
| `spr_undead_attack_up` | P0 | 128×128 | [64, 112] | 8 f; engine timed [6, 6, 6, 6, 4, 4, 7, 7] ticks; once; attack | [prompt](../art/prompts/milestone_a/spr_undead_attack_up.txt) | planned/source only |
| `spr_undead_hurt_down` | P0 | 128×128 | [64, 112] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_a/spr_undead_hurt_down.txt) | planned/source only |
| `spr_undead_defeat` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_a/spr_undead_defeat.txt) | planned/source only |
| `spr_undead_rise` | P0 | 128×128 | [64, 112] | 10 f; 12 fps; once; rise | [prompt](../art/prompts/milestone_a/spr_undead_rise.txt) | planned/source only |
| `spr_chest_desert` | P0 | 64×64 | [32, 56] | 6 f; state/static; state_driven; closed: f0; opening: f1-4; open: f5 | [prompt](../art/prompts/milestone_a/spr_chest_desert.txt) | planned/source only |
| `spr_checkpoint_star` | P0 | 64×64 | [32, 48] | 8 f; 10 fps; loop; animation | [prompt](../art/prompts/milestone_a/spr_checkpoint_star.txt) | planned/source only |
| `spr_fx_sparkle` | P0 | 16×16 | [8, 8] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_a/spr_fx_sparkle.txt) | planned/source only |
| `spr_icon_potion_health` | P0 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/spr_icon_potion_health.txt) | planned/source only |
| `spr_ui_hp_frame` | P0 | 320×32 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/spr_ui_hp_frame.txt) | existing UI prototype |
| `spr_ui_hp_fill` | P0 | 320×32 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/spr_ui_hp_fill.txt) | existing UI prototype |
| `spr_ui_slot` | P0 | 72×72 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/spr_ui_slot.txt) | existing UI prototype |
| `spr_ui_slot_selected` | P0 | 72×72 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/spr_ui_slot_selected.txt) | existing UI prototype |
| `spr_ui_panel` | P0 | 96×96 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_a/spr_ui_panel.txt) | existing UI prototype |

## Milestone B

| Asset ID | Pri | Target per frame | Origin | States and playback | Prompt | Native delivery |
|---|---|---|---|---|---|---|
| `spr_icon_longsword` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_longsword.txt) | planned/source only |
| `spr_icon_bandit_scimitar` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_bandit_scimitar.txt) | planned/source only |
| `spr_icon_sunsteel_blade` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_sunsteel_blade.txt) | planned/source only |
| `spr_icon_worn_tabard` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_worn_tabard.txt) | planned/source only |
| `spr_icon_iron_tunic` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_iron_tunic.txt) | planned/source only |
| `spr_icon_paladin_mail` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_paladin_mail.txt) | planned/source only |
| `spr_icon_wanderer_tunic` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_wanderer_tunic.txt) | planned/source only |
| `spr_icon_gold_coins` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_gold_coins.txt) | planned/source only |
| `spr_icon_desert_rose` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_desert_rose.txt) | planned/source only |
| `spr_icon_golden_scarab` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_golden_scarab.txt) | planned/source only |
| `spr_icon_ancient_coin` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_ancient_coin.txt) | planned/source only |
| `spr_icon_pharaoh_ankh` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_pharaoh_ankh.txt) | planned/source only |
| `spr_icon_potion_greater` | P1 | 64×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_icon_potion_greater.txt) | planned/source only |
| `spr_dave_hurt_down` | P0 | 96×96 | [48, 88] | 3 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_dave_hurt_down.txt) | planned/source only |
| `spr_dave_hurt_down_side` | P0 | 96×96 | [48, 88] | 3 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_dave_hurt_down_side.txt) | planned/source only |
| `spr_dave_hurt_side` | P0 | 96×96 | [48, 88] | 3 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_dave_hurt_side.txt) | planned/source only |
| `spr_dave_hurt_up_side` | P0 | 96×96 | [48, 88] | 3 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_dave_hurt_up_side.txt) | planned/source only |
| `spr_dave_hurt_up` | P0 | 96×96 | [48, 88] | 3 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_dave_hurt_up.txt) | planned/source only |
| `spr_dave_death` | P0 | 128×96 | [64, 88] | 10 f; 12 fps; once_hold; death | [prompt](../art/prompts/milestone_b/spr_dave_death.txt) | planned/source only |
| `spr_dave_potion` | P0 | 96×96 | [48, 88] | 8 f; 16 fps; once; potion | [prompt](../art/prompts/milestone_b/spr_dave_potion.txt) | planned/source only |
| `spr_skeleton_warrior_idle_down` | P0 | 128×128 | [64, 112] | 6 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_idle_down.txt) | planned/source only |
| `spr_skeleton_warrior_walk_down` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_walk_down.txt) | planned/source only |
| `spr_skeleton_warrior_attack_down` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 4, 4, 5, 5, 5] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_attack_down.txt) | planned/source only |
| `spr_skeleton_warrior_walk_side` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_walk_side.txt) | planned/source only |
| `spr_skeleton_warrior_attack_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 4, 4, 5, 5, 5] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_attack_side.txt) | planned/source only |
| `spr_skeleton_warrior_walk_up` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_walk_up.txt) | planned/source only |
| `spr_skeleton_warrior_attack_up` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 4, 4, 5, 5, 5] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_attack_up.txt) | planned/source only |
| `spr_skeleton_warrior_hurt_down` | P0 | 128×128 | [64, 112] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_hurt_down.txt) | planned/source only |
| `spr_skeleton_warrior_defeat` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_b/spr_skeleton_warrior_defeat.txt) | planned/source only |
| `spr_skeleton_archer_idle_down` | P0 | 128×128 | [64, 112] | 6 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_idle_down.txt) | planned/source only |
| `spr_skeleton_archer_walk_down` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_walk_down.txt) | planned/source only |
| `spr_skeleton_archer_attack_down` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 5, 5, 3, 5, 5] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_attack_down.txt) | planned/source only |
| `spr_skeleton_archer_walk_side` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_walk_side.txt) | planned/source only |
| `spr_skeleton_archer_attack_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 5, 5, 3, 5, 5] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_attack_side.txt) | planned/source only |
| `spr_skeleton_archer_walk_up` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_walk_up.txt) | planned/source only |
| `spr_skeleton_archer_attack_up` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 5, 5, 3, 5, 5] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_attack_up.txt) | planned/source only |
| `spr_skeleton_archer_hurt_down` | P0 | 128×128 | [64, 112] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_hurt_down.txt) | planned/source only |
| `spr_skeleton_archer_defeat` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_b/spr_skeleton_archer_defeat.txt) | planned/source only |
| `spr_bandit_idle_down` | P0 | 128×128 | [64, 112] | 6 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_b/spr_bandit_idle_down.txt) | planned/source only |
| `spr_bandit_walk_down` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_bandit_walk_down.txt) | planned/source only |
| `spr_bandit_attack_down` | P0 | 128×128 | [64, 112] | 8 f; engine timed [4, 4, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_bandit_attack_down.txt) | planned/source only |
| `spr_bandit_walk_side` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_bandit_walk_side.txt) | planned/source only |
| `spr_bandit_attack_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [4, 4, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_bandit_attack_side.txt) | planned/source only |
| `spr_bandit_walk_up` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_bandit_walk_up.txt) | planned/source only |
| `spr_bandit_attack_up` | P0 | 128×128 | [64, 112] | 8 f; engine timed [4, 4, 3, 3, 3, 4, 4, 4] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_bandit_attack_up.txt) | planned/source only |
| `spr_bandit_hurt_down` | P0 | 128×128 | [64, 112] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_bandit_hurt_down.txt) | planned/source only |
| `spr_bandit_defeat` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_b/spr_bandit_defeat.txt) | planned/source only |
| `spr_bandit_caster_idle_down` | P0 | 128×128 | [64, 112] | 6 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_b/spr_bandit_caster_idle_down.txt) | planned/source only |
| `spr_bandit_caster_walk_down` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_bandit_caster_walk_down.txt) | planned/source only |
| `spr_bandit_caster_cast_down` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 5, 5, 3, 5, 5] ticks; once; cast | [prompt](../art/prompts/milestone_b/spr_bandit_caster_cast_down.txt) | planned/source only |
| `spr_bandit_caster_walk_side` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_bandit_caster_walk_side.txt) | planned/source only |
| `spr_bandit_caster_cast_side` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 5, 5, 3, 5, 5] ticks; once; cast | [prompt](../art/prompts/milestone_b/spr_bandit_caster_cast_side.txt) | planned/source only |
| `spr_bandit_caster_walk_up` | P0 | 128×128 | [64, 112] | 8 f; 16 fps; loop; walk | [prompt](../art/prompts/milestone_b/spr_bandit_caster_walk_up.txt) | planned/source only |
| `spr_bandit_caster_cast_up` | P0 | 128×128 | [64, 112] | 8 f; engine timed [5, 5, 5, 5, 5, 3, 5, 5] ticks; once; cast | [prompt](../art/prompts/milestone_b/spr_bandit_caster_cast_up.txt) | planned/source only |
| `spr_bandit_caster_hurt_down` | P0 | 128×128 | [64, 112] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_bandit_caster_hurt_down.txt) | planned/source only |
| `spr_bandit_caster_defeat` | P0 | 128×128 | [64, 112] | 8 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_b/spr_bandit_caster_defeat.txt) | planned/source only |
| `spr_arrow` | P0 | 32×8 | [16, 4] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_b/spr_arrow.txt) | planned/source only |
| `spr_fx_arrow_hit` | P0 | 48×48 | [24, 24] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_arrow_hit.txt) | planned/source only |
| `spr_magic_orb` | P0 | 32×32 | [16, 16] | 4 f; 24 fps; loop; animation | [prompt](../art/prompts/milestone_b/spr_magic_orb.txt) | planned/source only |
| `spr_fx_magic_launch` | P0 | 64×64 | [32, 32] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_magic_launch.txt) | planned/source only |
| `spr_fx_magic_hit` | P0 | 64×64 | [32, 32] | 8 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_magic_hit.txt) | planned/source only |
| `spr_bat_fly` | P0 | 64×64 | [32, 32] | 6 f; 15 fps; loop; fly | [prompt](../art/prompts/milestone_b/spr_bat_fly.txt) | planned/source only |
| `spr_bat_dive` | P0 | 64×64 | [32, 32] | 4 f; 20 fps; once; dive | [prompt](../art/prompts/milestone_b/spr_bat_dive.txt) | planned/source only |
| `spr_bat_defeat` | P0 | 64×64 | [32, 32] | 6 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_b/spr_bat_defeat.txt) | planned/source only |
| `spr_python_slither_down` | P1 | 128×96 | [64, 72] | 8 f; 12 fps; loop; slither | [prompt](../art/prompts/milestone_b/spr_python_slither_down.txt) | planned/source only |
| `spr_python_lunge_down` | P1 | 128×96 | [64, 72] | 4 f; engine timed [4, 3, 3, 6] ticks; once; lunge | [prompt](../art/prompts/milestone_b/spr_python_lunge_down.txt) | planned/source only |
| `spr_python_slither_side` | P1 | 128×96 | [64, 72] | 8 f; 12 fps; loop; slither | [prompt](../art/prompts/milestone_b/spr_python_slither_side.txt) | planned/source only |
| `spr_python_lunge_side` | P1 | 128×96 | [64, 72] | 4 f; engine timed [4, 3, 3, 6] ticks; once; lunge | [prompt](../art/prompts/milestone_b/spr_python_lunge_side.txt) | planned/source only |
| `spr_python_slither_up` | P1 | 128×96 | [64, 72] | 8 f; 12 fps; loop; slither | [prompt](../art/prompts/milestone_b/spr_python_slither_up.txt) | planned/source only |
| `spr_python_lunge_up` | P1 | 128×96 | [64, 72] | 4 f; engine timed [4, 3, 3, 6] ticks; once; lunge | [prompt](../art/prompts/milestone_b/spr_python_lunge_up.txt) | planned/source only |
| `spr_python_coil` | P1 | 128×96 | [64, 72] | 6 f; 12 fps; once_hold; coil | [prompt](../art/prompts/milestone_b/spr_python_coil.txt) | planned/source only |
| `spr_python_hurt` | P1 | 128×96 | [64, 72] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_python_hurt.txt) | planned/source only |
| `spr_python_defeat` | P1 | 128×96 | [64, 72] | 8 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_b/spr_python_defeat.txt) | planned/source only |
| `spr_sandworm_mound` | P1 | 192×192 | [96, 176] | 6 f; 10 fps; loop; mound | [prompt](../art/prompts/milestone_b/spr_sandworm_mound.txt) | planned/source only |
| `spr_sandworm_emerge` | P1 | 192×192 | [96, 176] | 8 f; 16 fps; once; emerge | [prompt](../art/prompts/milestone_b/spr_sandworm_emerge.txt) | planned/source only |
| `spr_sandworm_idle_up` | P1 | 192×192 | [96, 176] | 6 f; 10 fps; loop; idle_up | [prompt](../art/prompts/milestone_b/spr_sandworm_idle_up.txt) | planned/source only |
| `spr_sandworm_attack` | P1 | 192×192 | [96, 176] | 8 f; engine timed [6, 6, 6, 6, 4, 4, 6, 6] ticks; once; attack | [prompt](../art/prompts/milestone_b/spr_sandworm_attack.txt) | planned/source only |
| `spr_sandworm_burrow` | P1 | 192×192 | [96, 176] | 8 f; 16 fps; once; burrow | [prompt](../art/prompts/milestone_b/spr_sandworm_burrow.txt) | planned/source only |
| `spr_sandworm_hurt` | P1 | 192×192 | [96, 176] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_b/spr_sandworm_hurt.txt) | planned/source only |
| `spr_sandworm_defeat` | P1 | 192×192 | [96, 176] | 10 f; 12 fps; once_hold; defeat | [prompt](../art/prompts/milestone_b/spr_sandworm_defeat.txt) | planned/source only |
| `spr_fx_hit` | P1 | 64×64 | [32, 32] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_hit.txt) | planned/source only |
| `spr_fx_dust` | P1 | 48×32 | [24, 24] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_dust.txt) | planned/source only |
| `spr_fx_poof` | P1 | 96×96 | [48, 72] | 8 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_poof.txt) | planned/source only |
| `spr_fx_heal_ring` | P1 | 128×64 | [64, 32] | 8 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_heal_ring.txt) | planned/source only |
| `spr_fx_heal_particle` | P1 | 16×16 | [8, 8] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_heal_particle.txt) | planned/source only |
| `spr_fx_levelup` | P1 | 128×128 | [64, 112] | 8 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_b/spr_fx_levelup.txt) | planned/source only |

## Milestone C

| Asset ID | Pri | Target per frame | Origin | States and playback | Prompt | Native delivery |
|---|---|---|---|---|---|---|
| `tex_grass` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/tex_grass.txt) | planned/source only |
| `tex_water` | P0 | 256×256 | [0, 0] | 4 f; 6 fps; loop; static | [prompt](../art/prompts/milestone_c/tex_water.txt) | planned/source only |
| `tex_wet_sand` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/tex_wet_sand.txt) | planned/source only |
| `tex_paving` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/tex_paving.txt) | planned/source only |
| `tex_masonry_top` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/tex_masonry_top.txt) | planned/source only |
| `tex_masonry_face` | P0 | 256×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/tex_masonry_face.txt) | planned/source only |
| `tex_chasm_wall` | P0 | 256×64 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/tex_chasm_wall.txt) | planned/source only |
| `tex_chasm_void` | P0 | 256×256 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/tex_chasm_void.txt) | planned/source only |
| `ts_stairs` | P0 | 192×128 | [0, 0] | 1 f; state/static; static; left_top; mid_top; right_top; left_bottom; mid_bottom; right_bottom | [prompt](../art/prompts/milestone_c/ts_stairs.txt) | planned/source only |
| `ts_bridge` | P0 | 448×128 | [0, 0] | 1 f; state/static; static; E-W rope top/bottom/both/none; N-S rope left/right/both/none; broken E-W x2; post x2 | [prompt](../art/prompts/milestone_c/ts_bridge.txt) | planned/source only |
| `spr_cactus_tall` | P0 | 64×128 | [32, 120] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_cactus_tall.txt) | planned/source only |
| `spr_cactus_small` | P0 | 48×64 | [24, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_cactus_small.txt) | planned/source only |
| `spr_rock_small_01` | P0 | 48×40 | [24, 34] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_rock_small_01.txt) | planned/source only |
| `spr_rock_small_02` | P0 | 48×40 | [24, 34] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_rock_small_02.txt) | planned/source only |
| `spr_rock_small_03` | P0 | 48×40 | [24, 34] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_rock_small_03.txt) | planned/source only |
| `spr_boulder_01` | P0 | 128×112 | [64, 100] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_boulder_01.txt) | planned/source only |
| `spr_boulder_02` | P0 | 128×112 | [64, 100] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_boulder_02.txt) | planned/source only |
| `spr_tree_desert` | P0 | 160×160 | [80, 150] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_tree_desert.txt) | planned/source only |
| `spr_tree_dead` | P0 | 128×160 | [64, 150] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_tree_dead.txt) | planned/source only |
| `spr_palm_01` | P0 | 128×192 | [64, 182] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_palm_01.txt) | planned/source only |
| `spr_palm_02` | P0 | 128×192 | [64, 182] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_palm_02.txt) | planned/source only |
| `spr_bush` | P0 | 64×48 | [32, 42] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_bush.txt) | planned/source only |
| `spr_bush_dead` | P0 | 64×48 | [32, 42] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_bush_dead.txt) | planned/source only |
| `spr_pebbles_01` | P0 | 64×64 | [32, 32] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_pebbles_01.txt) | planned/source only |
| `spr_pebbles_02` | P0 | 64×64 | [32, 32] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_pebbles_02.txt) | planned/source only |
| `spr_pebbles_03` | P0 | 64×64 | [32, 32] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_pebbles_03.txt) | planned/source only |
| `spr_skull_01` | P0 | 32×32 | [16, 24] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_skull_01.txt) | planned/source only |
| `spr_skull_02` | P0 | 32×32 | [16, 24] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_skull_02.txt) | planned/source only |
| `spr_ruin_block_01` | P0 | 64×64 | [32, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_ruin_block_01.txt) | planned/source only |
| `spr_ruin_block_02` | P0 | 128×64 | [64, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_ruin_block_02.txt) | planned/source only |
| `spr_ruin_block_03` | P0 | 64×96 | [32, 86] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_ruin_block_03.txt) | planned/source only |
| `spr_wagon_wreck` | P1 | 192×128 | [96, 116] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_wagon_wreck.txt) | planned/source only |
| `spr_obelisk` | P1 | 96×224 | [48, 214] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_obelisk.txt) | planned/source only |
| `spr_pharaoh_statue` | P1 | 128×256 | [64, 244] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_pharaoh_statue.txt) | planned/source only |
| `spr_tumbleweed` | P0 | 48×48 | [24, 24] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_c/spr_tumbleweed.txt) | planned/source only |
| `spr_healing_spring` | P2 | 128×96 | [64, 80] | 4 f; 8 fps; loop; animation | [prompt](../art/prompts/milestone_c/spr_healing_spring.txt) | planned/source only |

## Milestone D

| Asset ID | Pri | Target per frame | Origin | States and playback | Prompt | Native delivery |
|---|---|---|---|---|---|---|
| `spr_ui_save_card` | P1 | 760×120 | [0, 0] | 3 f; state/static; state_driven; normal f0; hover f1; pressed f2 | [prompt](../art/prompts/milestone_d/spr_ui_save_card.txt) | existing UI prototype |
| `spr_ui_save_card_empty` | P1 | 760×120 | [0, 0] | 3 f; state/static; state_driven; normal f0; hover f1; pressed f2 | [prompt](../art/prompts/milestone_d/spr_ui_save_card_empty.txt) | existing UI prototype |
| `spr_ui_button` | P1 | 64×64 | [0, 0] | 3 f; state/static; state_driven; normal f0; hover f1; pressed f2 | [prompt](../art/prompts/milestone_d/spr_ui_button.txt) | existing UI prototype |

## Milestone E

| Asset ID | Pri | Target per frame | Origin | States and playback | Prompt | Native delivery |
|---|---|---|---|---|---|---|
| `spr_intro_wall` | P0 | 1920×640 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_wall.txt) | planned/source only |
| `spr_intro_sky` | P1 | 1280×720 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_sky.txt) | planned/source only |
| `spr_intro_rubble_01` | P0 | 64×64 | [32, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_rubble_01.txt) | planned/source only |
| `spr_intro_rubble_02` | P0 | 96×96 | [48, 88] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_rubble_02.txt) | planned/source only |
| `spr_intro_rubble_03` | P0 | 128×96 | [64, 88] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_rubble_03.txt) | planned/source only |
| `spr_intro_rubble_04` | P0 | 160×128 | [80, 120] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_rubble_04.txt) | planned/source only |
| `spr_intro_fallen_01` | P0 | 128×64 | [64, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_fallen_01.txt) | planned/source only |
| `spr_intro_fallen_02` | P0 | 128×64 | [64, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_fallen_02.txt) | planned/source only |
| `spr_intro_fallen_03` | P0 | 128×64 | [64, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_fallen_03.txt) | planned/source only |
| `spr_intro_banner` | P0 | 128×192 | [64, 176] | 6 f; 8 fps; loop; animation | [prompt](../art/prompts/milestone_e/spr_intro_banner.txt) | planned/source only |
| `spr_intro_spear` | P0 | 128×64 | [64, 56] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_e/spr_intro_spear.txt) | planned/source only |
| `spr_dave_wind_idle_down` | P0 | 96×96 | [48, 88] | 12 f; 12 fps; loop; wind_idle | [prompt](../art/prompts/milestone_e/spr_dave_wind_idle_down.txt) | planned/source only |
| `spr_dave_turn` | P0 | 96×96 | [48, 88] | 4 f; 8 fps; once; turn | [prompt](../art/prompts/milestone_e/spr_dave_turn.txt) | planned/source only |
| `spr_dave_grief_down` | P1 | 96×96 | [48, 88] | 1 f; state/static; static; grief | [prompt](../art/prompts/milestone_e/spr_dave_grief_down.txt) | planned/source only |
| `spr_dave_vow_down` | P1 | 96×96 | [48, 88] | 1 f; state/static; static; vow | [prompt](../art/prompts/milestone_e/spr_dave_vow_down.txt) | planned/source only |
| `spr_portrait_dave` | P0 | 512×512 | [0, 0] | 1 f; state/static; static; neutral | [prompt](../art/prompts/milestone_e/spr_portrait_dave.txt) | planned/source only |
| `spr_portrait_dave_solemn` | P1 | 512×512 | [0, 0] | 1 f; state/static; static; solemn | [prompt](../art/prompts/milestone_e/spr_portrait_dave_solemn.txt) | planned/source only |
| `spr_portrait_dave_determined` | P1 | 512×512 | [0, 0] | 1 f; state/static; static; determined | [prompt](../art/prompts/milestone_e/spr_portrait_dave_determined.txt) | planned/source only |
| `spr_portrait_pharaoh` | P0 | 512×512 | [0, 0] | 1 f; state/static; static; menace | [prompt](../art/prompts/milestone_e/spr_portrait_pharaoh.txt) | planned/source only |
| `spr_portrait_pharaoh_rage` | P2 | 512×512 | [0, 0] | 1 f; state/static; static; rage | [prompt](../art/prompts/milestone_e/spr_portrait_pharaoh_rage.txt) | planned/source only |

## Milestone F

| Asset ID | Pri | Target per frame | Origin | States and playback | Prompt | Native delivery |
|---|---|---|---|---|---|---|
| `spr_pharaoh_idle` | P0 | 192×192 | [96, 176] | 8 f; 10 fps; loop; idle | [prompt](../art/prompts/milestone_f/spr_pharaoh_idle.txt) | planned/source only |
| `spr_pharaoh_summon` | P0 | 192×192 | [96, 176] | 10 f; 12 fps; once; summon | [prompt](../art/prompts/milestone_f/spr_pharaoh_summon.txt) | planned/source only |
| `spr_pharaoh_laser_charge` | P0 | 192×192 | [96, 176] | 8 f; 12 fps; once; laser_charge | [prompt](../art/prompts/milestone_f/spr_pharaoh_laser_charge.txt) | planned/source only |
| `spr_pharaoh_laser_fire` | P0 | 192×192 | [96, 176] | 4 f; 12 fps; loop; laser_fire | [prompt](../art/prompts/milestone_f/spr_pharaoh_laser_fire.txt) | planned/source only |
| `spr_pharaoh_thunder_cast` | P0 | 192×192 | [96, 176] | 8 f; 12 fps; once; thunder_cast | [prompt](../art/prompts/milestone_f/spr_pharaoh_thunder_cast.txt) | planned/source only |
| `spr_pharaoh_hurt` | P0 | 192×192 | [96, 176] | 2 f; 12 fps; once; hurt | [prompt](../art/prompts/milestone_f/spr_pharaoh_hurt.txt) | planned/source only |
| `spr_pharaoh_teleport_out` | P0 | 192×192 | [96, 176] | 6 f; 20 fps; once; teleport_out | [prompt](../art/prompts/milestone_f/spr_pharaoh_teleport_out.txt) | planned/source only |
| `spr_pharaoh_teleport_in` | P0 | 192×192 | [96, 176] | 6 f; 20 fps; once; teleport_in | [prompt](../art/prompts/milestone_f/spr_pharaoh_teleport_in.txt) | planned/source only |
| `spr_pharaoh_death` | P0 | 192×192 | [96, 176] | 16 f; 12 fps; once_hold; death | [prompt](../art/prompts/milestone_f/spr_pharaoh_death.txt) | planned/source only |
| `spr_laser_beam` | P0 | 64×32 | [0, 16] | 4 f; 24 fps; loop; animation | [prompt](../art/prompts/milestone_f/spr_laser_beam.txt) | planned/source only |
| `spr_fx_laser_charge` | P0 | 64×64 | [32, 32] | 8 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_f/spr_fx_laser_charge.txt) | planned/source only |
| `spr_laser_aim` | P0 | 16×16 | [8, 8] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_f/spr_laser_aim.txt) | planned/source only |
| `spr_thunder_marker` | P0 | 128×64 | [64, 32] | 4 f; 10 fps; loop; animation | [prompt](../art/prompts/milestone_f/spr_thunder_marker.txt) | planned/source only |
| `spr_thunder_exclaim` | P0 | 32×48 | [16, 24] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_f/spr_thunder_exclaim.txt) | planned/source only |
| `spr_lightning_bolt` | P0 | 96×384 | [48, 376] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_f/spr_lightning_bolt.txt) | planned/source only |
| `spr_fx_thunder_impact` | P0 | 128×96 | [64, 80] | 8 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_f/spr_fx_thunder_impact.txt) | planned/source only |
| `spr_summon_crack` | P0 | 96×48 | [48, 24] | 6 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_f/spr_summon_crack.txt) | planned/source only |
| `spr_fx_sand_burst` | P0 | 96×64 | [48, 48] | 8 f; 24 fps; once; animation | [prompt](../art/prompts/milestone_f/spr_fx_sand_burst.txt) | planned/source only |
| `spr_gate_arena` | P0 | 192×192 | [96, 176] | 8 f; 16 fps; state_driven; closed f0; opening f0-7; open f7; closing reverse f7-0 | [prompt](../art/prompts/milestone_f/spr_gate_arena.txt) | planned/source only |
| `spr_door_sealed` | P0 | 192×224 | [96, 208] | 1 f; state/static; static; sealed | [prompt](../art/prompts/milestone_f/spr_door_sealed.txt) | planned/source only |
| `spr_dungeon_entrance` | P0 | 384×320 | [192, 304] | 1 f; state/static; static; static threshold | [prompt](../art/prompts/milestone_f/spr_dungeon_entrance.txt) | planned/source only |
| `spr_title_bg` | P2 | 1280×720 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_f/spr_title_bg.txt) | planned/source only |
| `spr_title_logo` | P2 | 640×240 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_f/spr_title_logo.txt) | planned/source only |
| `spr_ending_bg` | P2 | 1280×720 | [0, 0] | 1 f; state/static; static; static | [prompt](../art/prompts/milestone_f/spr_ending_bg.txt) | planned/source only |

## Scope and ID decisions

C4 names are prop keys in the requests rather than specified sprite IDs. Proposed `spr_<prop_key>` mappings are explicitly marked in the JSON. B10 unspecified canvas/origin choices and the C3 atlas layout also require registration by Claude. Narrative-specific IDs and corrected E3 sizes/turn timing follow NARRATIVE_ASSET_REQUESTS. Pharaoh rage is a parked P2 option, unnecessary for the current script. The requested `spr_bat_fly` ID already exists; no existing resource was overwritten.

A10 and D1 UI prototype PNG/SVG sources are already supplied in UI_HANDOFF.zip. The manifest links copied reference assets and marks their generation prompts optional polish; reuse and validate the prototypes before commissioning alternatives. Their schematic world/portrait art is not a style reference.

Audio, font licensing/installation, room layouts, story/dialogue data and cutscene implementation remain with Claude. A11/A12, B11, C5, E1/E6–E9 and F6/F7 are tracked by ASSET_REQUESTS and are outside this art production pack. The original game brief has been read from its source chat and saved verbatim under art/reference. Original template screenshots remain unavailable; actual template PNGs and metadata anchor this art direction.
