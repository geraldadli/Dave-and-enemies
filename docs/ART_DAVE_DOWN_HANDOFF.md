# Dave v002 down animation handoff

Dave v002 has a cleaned native base and three down-facing animation deliveries: **26 animation frames plus the base reference**. Production used the built-in image-generation tool sequentially: cleanup, idle, walk and its leg-pose repairs, then attack and its sword-size repair. No GameMaker resource, room, object, project configuration or runtime data was changed.

Download the [native delivery package](../art/exports/dave/dave_down_v001.zip). Watch the [aligned three-action review](../art/review/dave/down_v001/dave_down_animation_review.gif), or inspect the per-action contact sheets below. The GIFs are review media; PNGs and timing sidecars are the integration deliverables.

## Native deliveries

| Asset | Frames and canvas | Origin | Timing | Files and review |
|---|---|---|---|---|
| Base reference | 1 × 96×96 | (48,88) | static | [PNG](../art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png) · [metadata](../art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference.json) |
| `spr_dave_idle_down` | 8 × 96×96; strip 768×96 | (48,88) | 10fps, 800ms loop | [strip](../art/exports/dave/down_v001/spr_dave_idle_down/spr_dave_idle_down_strip8.png) · [sidecar](../art/exports/dave/down_v001/spr_dave_idle_down/spr_dave_idle_down.json) · [contact sheet](../art/review/dave/down_v001/spr_dave_idle_down_contact.png) · [GIF](../art/review/dave/down_v001/spr_dave_idle_down_preview.gif) |
| `spr_dave_walk_down` | 10 × 96×96; strip 960×96 | (48,88) | 20fps, 500ms loop; contacts f2/f7 | [strip](../art/exports/dave/down_v001/spr_dave_walk_down/spr_dave_walk_down_strip10.png) · [sidecar](../art/exports/dave/down_v001/spr_dave_walk_down/spr_dave_walk_down.json) · [contact sheet](../art/review/dave/down_v001/spr_dave_walk_down_contact.png) · [GIF](../art/review/dave/down_v001/spr_dave_walk_down_preview.gif) |
| `spr_dave_attack_down` | 8 × 128×128; strip 1024×128 | (64,112) | holds [3,3,3,3,3,4,4,4] ticks at 60Hz; 450ms once | [strip](../art/exports/dave/down_v001/spr_dave_attack_down/spr_dave_attack_down_strip8.png) · [sidecar](../art/exports/dave/down_v001/spr_dave_attack_down/spr_dave_attack_down.json) · [contact sheet](../art/review/dave/down_v001/spr_dave_attack_down_contact.png) · [GIF](../art/review/dave/down_v001/spr_dave_attack_down_preview.gif) |

Individual files are alongside each strip, named `<asset>_00.png` onward. All are exact fixed-size, untrimmed 8-bit RGBA PNGs with an sRGB chunk and straight alpha. The base’s visible silhouette is 78 pixels tall. Its origin translates by (+16,+24) into the larger attack canvas. The final attack recovery pose uses that same checked base registration.

## Appearance and action checks

The selected [cleaned v002 master](../art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png) retains the face, long golden-brown swept hair, shining silver plate, ivory layered tabard, brown garments and boots, red cape and two brass shoulder clasps. The source’s small belt details were simplified. Disconnected alpha noise was removed mechanically, near-opaque solid pixels normalized, and the art resampled with associated-alpha filtering before returning to straight RGBA for export. No ground shadows were baked in.

Dave’s anatomical right hand remains the sword hand in **all 26 animation frames**. In down view it begins on the viewer’s left. During attack contact, the right forearm crosses the torso from the viewer-left shoulder; the sword appearing on the viewer’s right is the end of that same right-arm swing. The left hand remains empty. All figures keep the upper-left lighting convention; no entire figure was mirrored.

Walk f2 is the right boot/viewer-left contact. F7 is the left boot/viewer-right contact. The first generated sheet had incorrect legs in several cells; corrected f7 and four smaller inbetween drawings supply passing and push-off/flight poses. The source atlas’s figure bounds overlapped nominal cell boundaries, so figures were isolated by their connected alpha rather than blindly sliced. Sources at different resolutions use a documented common scale per source set, then registered roots; no body parts were resized independently. Brief raised-foot silhouettes at f4/f9 belong to the energetic gait.

Attack f0–1 are **anticipation**, f2–4 **active**, f3 the strongest **contact** pose, and f5–7 **recovery**. A targeted repair shortened blades that grew in the first strike source and adjusted the start of the descending cut. Slash FX is separate and is not baked into these frames. Use exact sidecar ticks in the engine: the individual attack GIF approximates recovery holds as 70/60/70ms because GIF stores timing in 10ms units. That preview approximation is not the gameplay timing.

## Verification and remaining work

[Validation report](../art/review/dave/down_v001/validation.json) has no mechanical errors. Checks covered the 26 animation frames, fixed origins, RGBA mode, sRGB metadata, transparent canvas borders, exact strip dimensions and pixel-for-pixel strip/frame agreement. The [alpha review](../art/review/dave/down_v001/dave_down_alpha_review.png) was inspected over white, black, pale sand and dark ruins. All source and native contact sheets were inspected for sword hand, costume identity, pose order and clipping. Loop boundaries were compared with internal frame transitions.

The idle f7→f0 transition has a small visible silhouette settle. Its average premultiplied RGBA difference is 16.523 against the largest internal transition of 14.801; the metric is diagnostic, not a perceptual quality certificate. Minor generated facial/outline variation remains between poses. These are available for further pixel retouch; **a perfectly seamless hand-polished loop is not claimed**. The walk’s last-to-first progression and corrected contact poses were inspected, but native GameMaker movement must still establish whether any foot sliding needs adjustment.

These files are **native export candidates awaiting Claude’s engine acceptance**, with `verified_engine_ready: false`. Claude should preview them at native scale and contracted timing, check idle/walk/attack transitions, bind walk step events to f2/f7, and verify attack active range f2–4 against the code hitbox. Existing engine placeholders remain untouched. The earlier slash-duration and left-mirroring issues in [the visual guide](ART_VISUAL_GUIDE.md) remain separate integration decisions.

Original generation prompts and high-resolution sources are in `art/source/dave/down_batch_v001/`. [Export plan](../art/source/dave/down_batch_v001/export_plan.json) records each measured source extraction rectangle, connected component, registration point and scale. The art-only [export script](../art/tools/export_dave_down.py) and [review script](../art/tools/review_dave_down.py) reproduce the native files and review media; they do not integrate or implement the character in GameMaker.
