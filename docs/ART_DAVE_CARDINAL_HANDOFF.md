# Dave v002 right left and up animation handoff

This continuation adds **54 animation frames**: a ten-frame walk and eight-frame attack for each of right/east, independently authored left/west, and up/north. Three new facing bases were generated from cleaned Dave v002 and inspected at native size before their animation jobs. Each action/facing was generated, inspected and exported before moving to the next; production used the built-in `image_gen.imagegen` tool.

Download [the native art package](../art/exports/dave/dave_cardinal_v001.zip), watch [the six-action review](../art/review/dave/cardinal_v001/dave_cardinal_animation_review.gif), or inspect [validation results](../art/review/dave/cardinal_v001/validation.json). Numbered PNGs, horizontal strips, sidecars, prompts and sources are supplied. Existing down art remains in [the prior down handoff](ART_DAVE_DOWN_HANDOFF.md).

## Native deliveries

| Asset ID | Canvas and origin | Playback | Strip and timing | Frame review |
|---|---|---|---|---|
| `spr_dave_walk_side` | 96×96; (48,88) | 10 frames, 20fps loop | [960×96 strip](../art/exports/dave/cardinal_v001/spr_dave_walk_side/spr_dave_walk_side_strip10.png) · [sidecar](../art/exports/dave/cardinal_v001/spr_dave_walk_side/spr_dave_walk_side.json) | [contact sheet](../art/review/dave/cardinal_v001/spr_dave_walk_side_contact.png) · [GIF](../art/review/dave/cardinal_v001/spr_dave_walk_side_preview.gif) |
| `spr_dave_attack_side` | 128×128; (64,112) | 8 poses, 450ms once | [1024×128 strip](../art/exports/dave/cardinal_v001/spr_dave_attack_side/spr_dave_attack_side_strip8.png) · [sidecar](../art/exports/dave/cardinal_v001/spr_dave_attack_side/spr_dave_attack_side.json) | [contact sheet](../art/review/dave/cardinal_v001/spr_dave_attack_side_contact.png) · [GIF](../art/review/dave/cardinal_v001/spr_dave_attack_side_preview.gif) |
| `spr_dave_walk_left` | 96×96; (48,88) | 10 frames, 20fps loop | [960×96 strip](../art/exports/dave/cardinal_v001/spr_dave_walk_left/spr_dave_walk_left_strip10.png) · [sidecar](../art/exports/dave/cardinal_v001/spr_dave_walk_left/spr_dave_walk_left.json) | [contact sheet](../art/review/dave/cardinal_v001/spr_dave_walk_left_contact.png) · [GIF](../art/review/dave/cardinal_v001/spr_dave_walk_left_preview.gif) |
| `spr_dave_attack_left` | 128×128; (64,112) | 8 poses, 450ms once | [1024×128 strip](../art/exports/dave/cardinal_v001/spr_dave_attack_left/spr_dave_attack_left_strip8.png) · [sidecar](../art/exports/dave/cardinal_v001/spr_dave_attack_left/spr_dave_attack_left.json) | [contact sheet](../art/review/dave/cardinal_v001/spr_dave_attack_left_contact.png) · [GIF](../art/review/dave/cardinal_v001/spr_dave_attack_left_preview.gif) |
| `spr_dave_walk_up` | 96×96; (48,88) | 10 frames, 20fps loop | [960×96 strip](../art/exports/dave/cardinal_v001/spr_dave_walk_up/spr_dave_walk_up_strip10.png) · [sidecar](../art/exports/dave/cardinal_v001/spr_dave_walk_up/spr_dave_walk_up.json) | [contact sheet](../art/review/dave/cardinal_v001/spr_dave_walk_up_contact.png) · [GIF](../art/review/dave/cardinal_v001/spr_dave_walk_up_preview.gif) |
| `spr_dave_attack_up` | 128×128; (64,112) | 8 poses, 450ms once | [1024×128 strip](../art/exports/dave/cardinal_v001/spr_dave_attack_up/spr_dave_attack_up_strip8.png) · [sidecar](../art/exports/dave/cardinal_v001/spr_dave_attack_up/spr_dave_attack_up.json) | [contact sheet](../art/review/dave/cardinal_v001/spr_dave_attack_up_contact.png) · [GIF](../art/review/dave/cardinal_v001/spr_dave_attack_up_preview.gif) |

Individual frames are in the same folders, named `<asset>_00.png` onward. All have fixed untrimmed native canvases, 8-bit RGBA, straight alpha and an sRGB chunk. Every outer canvas border is fully transparent. Native bases are [right](../art/exports/dave/cardinal_v001/dave_base_side_reference/dave_base_side_reference_00.png), [left](../art/exports/dave/cardinal_v001/dave_base_left_reference/dave_base_left_reference_00.png) and [up](../art/exports/dave/cardinal_v001/dave_base_up_reference/dave_base_up_reference_00.png); each standing base is 78 pixels tall inside 96×96 with origin (48,88).

## Right handedness and direction mapping

Right/east uses the contract’s existing `side` suffix. Up uses `up`. The user explicitly requested left-facing art with unchanged anatomical right-handedness, so **new stable IDs `spr_dave_walk_left` and `spr_dave_attack_left`** are supplied. Claude still needs to register these resources and bind west/direction 4 to them. This is an art delivery extension to the contract’s provisional mirroring plan; `PROJECT_CONTRACT.md` itself was not edited.

- East: anatomical right arm is the near arm and holds the sword; far left hand is empty.
- West: anatomical right arm is far/upstage and holds the sword; near left hand is empty. This view was independently generated, not made by mirroring east.
- North: right arm begins on image right. During cross-body follow-through the weapon hand can appear near the image-left crown while the right arm is partly hidden behind hair; the low left arm remains empty. No face is shown in the rear view.

[Direction mapping](../art/exports/dave/cardinal_v001/direction_mapping.json) records indices 0 east, 2 north, 4 west and 6 south, all with `image_xscale: 1` for these authored cardinal images. It is **handoff metadata, not runtime implementation**. Whole-sprite mirroring would reverse both handedness and the screen-space light; use the authored west files. Diagonals and additional idle states were not requested in this continuation and remain separate work.

## Appearance and motion

All facing bases derive from [cleaned v002](../art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png). The golden-brown hair, silver plate, ivory/brown garment layers, red cape, brass sword guard/grip and shoulder attachments were checked across the source and native contact sheets. In back view the hair covers the upper cape and front clasps are naturally hidden; no new central-back jewelry was added. Upper-left light remains fixed in screen space.

Walking uses 20fps and zero-based contact/event indices **2 and 7**. Cloth and perspective partly hide which leg is in front; these event locations still need comparison with native world movement and footsteps in GameMaker. No exact foot-ground dynamics are inferred solely from a static strip.

Attacks use the exact game-tick schedule **[3,3,3,3,3,4,4,4] at 60Hz**, total 27 ticks/450ms. Anticipation is f0–1; active is f2–4; contact is f3; recovery is f5–7. Every final recovery frame reuses its facing’s checked base at the attack origin, a (+16,+24) translation from the locomotion canvas. Review GIFs approximate recovery as 70/60/70ms; sidecar ticks are authoritative. Slash FX and shared ground shadows remain separate.

The right attack received a blade-size repair. The left attack received a follow-through direction repair. Its source preview appeared to contain a backdrop, but sampled inter-cell pixels already had alpha zero with colour beneath them. The export isolated the actual connected silhouettes, cleared hidden RGB and discarded stray alpha; the native delivery has no backdrop or glow rectangle. Source atlas cells were measured rather than assumed correct, and overlapping figure bounds were separated by connected alpha. Source roots and common scales are in [the export plan](../art/source/dave/cardinal_batch_v001/export_plan.json).

## Inspection and acceptance boundary

Local checks passed for **54 animation frames, three bases and six strips**: exact dimensions, frame counts, RGBA/8-bit/sRGB metadata, transparent outer borders, fixed sidecar origins, pixel-for-pixel strip agreement, step indices and attack timing. The up contact blade retains two transparent native rows above its highest pixel. Sources and every native contact sheet were visually inspected for identity, limb ownership, pose order and clipping. [Walk alpha review](../art/review/dave/cardinal_v001/dave_cardinal_walk_alpha_review.png) and [attack alpha review](../art/review/dave/cardinal_v001/dave_cardinal_attack_alpha_review.png) cover white, black, sand and ruins backgrounds.

Loop-boundary pixel differences were compared with internal transitions; the measured seam ratios are 0.825 right, 0.804 left and 0.724 up. These are diagnostics, not certificates of a perfectly seamless loop. Minor generated line/hair/cape variation and stride smoothing may benefit from further retouch after movement-speed review. The partly occluded north follow-through should also be reviewed at native size with the slash FX.

All six assets are marked **native exports inspected, pending Claude’s engine acceptance**, with `verified_engine_ready: false`. No GameMaker resources or runtime files were replaced. Claude should register the west IDs, verify cardinal mapping without mirroring, preview action transitions, bind walk events and confirm f2–4 active timing against the hitbox. Original high-resolution sources and exact generation prompts remain in `art/source/dave/cardinal_batch_v001/`; the [export wrapper](../art/tools/export_dave_cardinal.py) and [review script](../art/tools/review_dave_cardinal.py) are art tooling only.
