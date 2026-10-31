# Dave v002 cardinal continuation

54 new animation frames: right (`side`), left (`left`) and up (`up`), each with walk and attack. Three native facing bases are also included. Preserve the project-relative archive paths when extracting.

- Walk: 10 frames, 96×96, origin (48,88), 20fps loop; step events at zero-based f2/f7.
- Attack: 8 poses, 128×128, origin (64,112), ticks [3,3,3,3,3,4,4,4] at60Hz =450ms, once. Anticipation0–1, active2–4/contact3, recovery5–7.
- `spr_dave_walk_left` and `spr_dave_attack_left` are independently authored west views. Right hand is the far arm; near left hand stays empty. Claude must register these two new IDs. Use positive xscale, not an east-image mirror.
- PNG frames/strips and timing JSON are the native deliverables. GIFs are review media with approximate recovery intervals. Source atlases and exact `.prompt.txt` files are generation records; they are not native strips.
- Fixed canvases, alpha borders, sRGB/8-bit RGBA, frame counts, timing and strip equality passed local checks. Native-size identity/handedness and contrast sheets were inspected. Minor generated contour/stride variation may need retouch after movement review.
- GameMaker playback and resource registration remain with Claude. `verified_engine_ready` is false. No engine resources were changed.

Read `docs/ART_DAVE_CARDINAL_HANDOFF.md`. Review `art/review/dave/cardinal_v001/dave_cardinal_animation_review.gif` and `validation.json`. Generation used the built-in `image_gen.imagegen` tool, attaching the cleaned v002 model and facing references, one action/facing at a time. The archive includes current sources/prompts/export plan, art-only export scripts and reference PNGs.

Existing down idle/walk/attack are in the previous `down_v001` delivery and are not duplicated here. `direction_mapping.json` documents all cardinal IDs for Claude; it is art handoff metadata only. Diagonal animations and additional idle states remain separate work.
