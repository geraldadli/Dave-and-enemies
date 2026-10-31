# Dave’s and Enemies visual guide

This art handoff follows Claude’s `PROJECT_CONTRACT.md` and `ASSET_REQUESTS.md` for Chapter I Desert. Milestone A is the immediate production target: movement, sword combat, one undead enemy, a chest, a checkpoint and two rooms. Claude owns GameMaker resources, runtime data and integration; this pack supplies artwork direction, generation prompts, animation plans and inspection requirements.

## Reference authority

Use these sources in order:

1. The [original user brief](../art/reference/original_game_brief.txt), recovered verbatim from the source chat identified by the narrative handoff. It establishes the siege, sole survivor, Grail vow, eastward desert journey, enemy families, red healing and Pharaoh encounter. Original template screenshots remain unavailable; use the actual template assets for perspective and density.
2. `PROJECT_CONTRACT.md`, including its verified facts and its expressly provisional engineering decisions. Follow the specified canvases and IDs in production; record conflicts rather than editing the contract.
3. `ASSET_REQUESTS.md`, whose per-asset exceptions override generic animation defaults. For example, undead walk is **8** frames, not Dave’s 10, and undead idle is **6**, not Dave’s 8.
4. The actual template PNGs and canonical `.yy` resources. [Template inspection board](../art/reference/template_sprite_inspection.png) shows the original sprites at an integer enlargement for inspection. It is an assembled reference board, not a gameplay screenshot. [Template inventory](../art/reference/template_inventory.json) records original dimensions and origins.
5. [NARRATIVE_ASSET_REQUESTS.md](NARRATIVE_ASSET_REQUESTS.md) and [NARRATIVE_SCRIPT.md](NARRATIVE_SCRIPT.md) refine the intro staging, exact rubble sizes, turn timing and portrait moods. [UI_HANDOFF.zip](UI_HANDOFF.zip) supplies the existing UI prototypes and layout rules. Its schematic world, item and portrait drawings are placement placeholders, not final art references.
6. The established model reference for a character. Dave’s identity remains [v002](../art/source/dave/dave_base_down_v002.png), now with a [cleaned down master](../art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png) and [checked 96×96 down base](../art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png). Use these and the checked [right, left and up bases](ART_DAVE_CARDINAL_HANDOFF.md) for subsequent work; do not use v001 as a competing design. Down idle and all four cardinal walks/attacks are locally inspected native candidates in the [down](ART_DAVE_DOWN_HANDOFF.md) and [cardinal](ART_DAVE_CARDINAL_HANDOFF.md) handoffs.

The first Dave draft preceded the contract’s arrival. Both drafts remain archived as sources; neither is a replacement engine sprite.

## Perspective and native visual density

The template is **smooth, antialiased cartoon art**, with dark outlines and softly shaded broad forms. It is not coarse pixel art. It uses an elevated top-down three-quarter adventure camera: heads and shoulder tops are visible, feet sit on a ground plane, walls show front faces and top edges. Use orthographic-looking parallel world edges; avoid a horizon, vanishing-point scenery or isometric diamond tiles in gameplay assets.

The camera is 1280×720 and terrain cells are 64×64. The original idle knight canvas is 60×77; the original downward walk canvas is 58×74. The original files contain partial-alpha edge pixels, confirming antialiasing. An integer-nearest enlargement in the inspection board exposes source pixels; it is not an instruction to redraw chunky pixel blocks. Contract texture filtering is enabled.

Dave’s new canvas is 96×96, but his **body stays 76–80 pixels tall**. Extra transparent canvas accommodates hair, cape and sword. Do not grow the body to fill 96 pixels. Humanoid enemies remain 70–84 pixels tall inside 128×128 frames. Head height is about 35–40% of body height; broad shoulders, short legs and small boots follow the template. Detail should read at actual size before enlarged inspection. One or two clean highlight masses communicate armor better than tiny scratches.

## Palette and lighting

All gameplay objects share a primary upper-left light. Dark outlines separate silhouettes on pale sand; brighter upper planes keep the same silhouettes readable in dark ruins. Shadows inside the art describe form; the engine draws the shared ground shadow. Do not bake an ellipse or a square shadow matte into new sprites.

These are **proposed production colour ramps**, not a claimed palette extraction or a hard indexed-palette restriction. Antialiased transition colours are allowed. Preserve the same ramp roles across frames.

| Material | Highlight | Midtone | Shadow | Direction |
|---|---|---|---|---|
| Outline | — | `#252A2D` | `#151A1D` | thin charcoal, not a thick pure-black sticker border |
| Dave steel | `#E4EBEF` | `#A8B3C0` | `#55616F` | small bright upper-left glints, broad slate shadow |
| Dave hair | `#E7B85D` | `#B77B35` | `#6C4525` | golden-brown, not yellow blond or orange flame |
| Dave cape | `#C8323C` | `#9C172B` | `#510F20` | red remains recognisable in every facing |
| Ivory cloth and bone | `#EEE5CE` | `#C4B79A` | `#81765D` | distinguish cloth folds from bone planes |
| Brass and gold | `#F1CF76` | `#BC913F` | `#71522A` | limited accent, no all-over glow |
| Brown garments and wood | `#9B754A` | `#705035` | `#3D3026` | muted and warm |
| Light sand | `#E0C994` | `#C9AF79` | `#AE925F` | low-contrast surface texture |
| Dark sand | `#C0A36F` | `#A48959` | `#806B49` | same grain scale as light sand |
| Canyon and ruins | `#C7B28A` | `#97866A` | `#5C5548` | broad stone planes, restrained fissures |
| Oasis vegetation | `#A1AE72` | `#727E4E` | `#47543B` | dusty olive, not neon green |
| Oasis water | `#A5D1CA` | `#6AA49F` | `#3F777A` | quiet turquoise, low-contrast animation |
| Healing | `#FF8B78` | `#DB3F43` | `#8D2234` | **red** ring and particles |
| Checkpoint | `#FFF2A2` | `#F1CA4A` | `#B47B27` | gentle yellow pulse, no flashing |

The source images are not guaranteed to use those exact hex values. Palette cleanup is an export task. Sunlit desert materials may be warmer than the original dungeon; outline weight, shape treatment, detail density and light direction remain consistent.

## Dave identity lock

Dave is an adult paladin rendered with the template’s compact gameplay proportions. His working identity uses an uncovered face, long swept golden-brown hair falling to the shoulder blades, rounded shining silver plate, ivory layered tabard over warm brown garments, brown belt and boots, and a deep red cape. Two small brass shoulder clasps attach the cape to the upper back; hair sits over the cape, never replacing it. Keep the garment layer order visible: armor over undergarments, tabard panels over the upper legs, belt over the waist, cape behind the torso. A few broad restrained scuffs can convey the narrative’s battle-worn armor without adding noisy tiny scratches.

His straight steel sword has a simple brass crossguard and brown grip. It stays in his **anatomical right hand**. In the down-facing pose that hand is on the viewer’s left. In other views, follow shoulder, elbow, wrist and grip anatomy. Do not infer handedness from which side of the canvas the blade happens to occupy. The lowered blade must stay clear of the boots and above the sole line; the complete tip must fit inside the export canvas. There is no shield in Dave’s design.

Keep the crown-to-chin ratio, shoulder width, arm length, boot size, blade length, crossguard shape, clasps and colour roles on a model overlay. Right, independently authored left and rear/up bases were derived from cleaned v002 and passed their local native-size checks before animation. All four cardinal bases now have native references; diagonal bases remain pending. The down animation review records small generated outline variations and an idle loop-boundary settle for optional further retouch; the cardinal handoff records stride and occlusion checks for engine preview.

Produce Dave animation variants only after the native-size base and relevant facing pass inspection. The four cardinal gates are complete: down idle/walk/attack and right/left/up walk/attack were generated one action and facing at a time. Every subsequent image call must attach the selected model reference and relevant rendering reference. A text description alone is insufficient for identity continuity.

## Character shape hierarchy

| Family | Silhouette and materials | Readable attack cue |
|---|---|---|
| Undead | dusty olive-grey flesh, ochre/brown rags, heavy reaching arms, stoop | shoulders pull back, then a forward swipe |
| Skeleton warrior | dry ivory exposed ribs/skull, ochre guards, short sword right, small shield left | visible sword windup before contact |
| Skeleton archer | ivory bones, ochre hood remnant, bow left, draw hand right, quiver | bow arm sets, string draws, release at f5 |
| Bandit | tan face, ochre wrap, brown tunic, russet sash, curved scimitar right | low quick crouch and sweep |
| Bandit caster | indigo hood, ochre robe, wooden staff with small turquoise tip right | staff held steady before release at f5 |
| Bat | charcoal-brown body, brown membrane, clear ears, 56px wingspan | wings tuck before dive |
| Python | ochre body, broad brown saddle patches, cream underside, one continuous spine | tightening coil and raised head |
| Sandworm | 128–160px emerged body, broad tan segments, radial mouth | visible shifting mound from the start |
| Undead Pharaoh | 140px floating mummy king, ivory wraps, lapis/gold nemes, broad collar, gold rod with amber crown | distinct summon hand, held rod charge, raised thunder gesture |

Those enemy costume details are art proposals where the brief does not define exact clothing. Establish one neutral reference per family before animating it. Do not redesign between actions. The skeleton warrior uses the sword option consistently; a spear loadout would need a separate planned variant. Projectile enemies are the skeleton archer and bandit caster, with arrows/orbs delivered separately. The Pharaoh’s rod remains the same length and silhouette in the portrait, charge and fire poses.

## Alignment and direction contract

| Asset class | Frame canvas | Origin | Body or anchor |
|---|---|---|---|
| Dave idle/walk/hurt/potion/cutscene acting | 96×96 | (48,88) | crown near y=10 for a 78px body; boots at ground anchor |
| Dave attack | 128×128 | (64,112) | same body size; translate neutral model by (+16,+24) from locomotion |
| Dave death | 128×96 | (64,88) | final body may lie flat; do not recrop |
| Medium enemy | 128×128 | (64,112) | 70–84px body |
| Bat | 64×64 | (32,32) | centre anchor; shadow drawn separately |
| Python | 128×96 | (64,72) | roughly 100px body length |
| Sandworm/Pharaoh | 192×192 | (96,176) | ground under emerged/floating body |
| Icon | 64×64 | GUI top-left (0,0), per UI handoff | visual mass centred around (32,32); 3px transparent outer padding; readable at 48px |
| Portrait | 512×512 | GUI top-left | bust faces right; shown at 208×208 |

The coordinates above are the contract’s new origins, not the template’s old centre origins. Do not overwrite old resources or claim they already align. Claude supplies offsets for placeholders. Constant per-frame canvas and origin are mandatory; automatic trimming is unsuitable. A rigid weapon can extend across the canvas, but the body and planted-foot reference cannot drift to accommodate it.

The contract defines Dave’s five authored facings: `down`, `down_side`, `side`, `up_side`, `up`; right-side facings point screen right. The user’s continuation adds an independently authored `left` walk and attack, preserving his right sword hand. Medium humanoids have down/side/up. Python slither/lunge has three facings. Bat, sandworm and Pharaoh face down toward the camera. The requested `spr_sandworm_idle_up` means the emerged upright state, not a view of the back.

Indices follow GameMaker: 0 E, 1 NE, 2 N, 3 NW, 4 W, 5 SW, 6 S, 7 SE. The contract’s provisional plan mirrors the left half. The new [cardinal mapping](../art/exports/dave/cardinal_v001/direction_mapping.json) instead uses authored west walk/attack with positive xscale; Claude still needs to register those two IDs. Diagonal left views remain unresolved and are not included in this continuation.

## Animation production

All frame indices are **zero based**. Generate one character, one action and one facing per call. Within that call, request only the required chronological poses, preferably one horizontal strip. If the generator loses identity across a strip, generate individual poses against the selected reference and previous accepted pose; do not expand into a larger sheet. Reassemble and inspect the frames afterward.

| Action | Count and timing | Pose landmarks | End behaviour |
|---|---|---|---|
| Dave idle | 8 at 10fps, 800ms | f0 neutral, f4 breath crest; hair/cape lag subtly | loop f7→f0 without jump |
| Dave walk | 10 at 20fps, 500ms | contacts f2/f7; opposite passing positions around f0/f5 | continuous loop; no duplicate terminal pose |
| Dave attack | 8 poses; holds [3,3,3,3,3,4,4,4] ticks at 60Hz, total 450ms | anticipation f0–1; active f2–4; visual contact f3; recovery f5–7 | once, return to idle |
| Undead idle | 6 at 10fps, 600ms | dry slow sway; 10fps follows contract idle default | loop |
| Undead walk | 8; proposed 12fps | proposed contacts f2/f6, not Dave’s step-event indices | loop |
| Undead attack | 8, ranges locked; proposed ticks [6,6,6,6,4,4,7,7] | anticipation f0–3; active f4–5; contact f5; recovery f6–7 | once |
| Damage | Dave 3, undead 2 at 12fps | recoil then guarded return | once |
| Defeat/death | per asset, 8–16 poses | lose balance, ground contact/disintegrate, settle | once, hold last |
| Archer/caster | 8, release f5 | charge/draw before f5; measured tip/nock offset on f5 | once |
| Bat flight | 6 at 15fps, 400ms | coherent wing joints and a full stroke | loop |
| Python slither | 8 at 12fps | continuous travelling S-curve | loop |
| FX | exact per request, usually 6–8 at proposed 24fps | onset, contact/crest, taper, fade | once unless explicitly looping |

Enemy durations not fixed in the contract are labelled **proposed** in the manifest; Claude owns their gameplay tuning. Keep anticipation and active boundaries intact while tuning hold durations. Projectile release is not an arbitrary middle frame. Measure a signed pixel offset from the final frame origin, not from a high-resolution source crop. The sidecar template keeps these offsets `null` until measured.

Grounded walks can bob the torso by at most roughly 2 native pixels; planted soles must not slide. Cape and hair secondary motion lag the torso, while clasps remain fixed. The sword’s grip point stays inside the right hand through anticipation, contact and recovery. The body does not shrink or stretch to keep the weapon in bounds; use the contracted attack canvas.

## Environment construction

Deliver `tex_sand_light` as three separate material detail variants: ripples, embedded pebbles and shallow cracks. They share the same sand ramp and scale. `tex_sand_dark` is a plain compatible path material, not a prepainted path tile. Claude generates irregular 47-tile edge/corner blends, so art must not deliver a falsely labelled finished autotile atlas. Rock tops and front faces are separate surfaces; front face textures are 256×64 and repeat horizontally, while flat materials are 256×256 and repeat on all edges.

Oasis grass, water and wet sand share quiet boundary values. Water’s optional four phases need both spatial tiling and a temporal loop. Never infer either from a generation prompt. Test every phase in a 3×3 repeat and inspect the last-to-first cycle. Avoid central landmarks and large diagonal streaks that expose repetition.

Wide stairs use the specified six-cell 192×128 source layout. Middle stair columns repeat horizontally. Bridges use a **proposed** explicit 448×128 atlas layout in the manifest: rope/no-rope E–W and N–S pieces, two broken E–W ends and two 32×64 posts. Inspect joined pieces, not just isolated tiles. Keep entrances clear and rope alignment continuous. The contract’s empty tile zero requirement is preserved when Claude packs the final engine tileset.

Prop origins sit at the base/trunk footprint rather than the centre of tall foliage. Bushes, dead bushes, pebbles and skulls have no collision. Tall tree tops can cover characters passing behind; Claude handles depth and collision. C4 specifies prop keys rather than exact sprite IDs, so the manifest proposes `spr_<prop_key>` mappings and records exact proposed anchors/remaining footprints for review. Tumbleweed is one 48×48 image with its pivot at (24,24); the engine rotates it. Use weak ambient shading on the sphere so a rotating baked highlight does not contradict the world light.

## Portraits and interface art

Portraits are deliberate hand-painted fantasy illustrations with believable adult skull, eye, neck and shoulder anatomy. They are not enlarged chibi gameplay heads. Retain Dave’s hairline, golden-brown hair, facial landmarks, silver armor, ivory tabard and brass cape clasps; translate the anatomy into a natural adult bust. The Pharaoh retains the same emaciated face, nemes stripes, collar, wrappings and rod design. Busts face **right** toward text. Inspect at both 512px and the actual 208px GUI size for gaze, expression, symmetry and silhouette. Keep the background transparent and supply no baked dialogue frame or text.

Icons use one clear object, 3px transparent padding and a centred visual mass. A red potion is not a green flask or a labelled medical product. Distinguish greater potion by silhouette as well as colour. Weapons match their character models. The Pharaoh ankh is a reward; the Grail is never shown recovered in Chapter I.

Milestone A includes the HUD kit even though it was not enumerated separately in the initial art list. It is a dependency of the next playable milestone. Keep health frame/fill at 320×32, slots at 72×72 and panel source at 96×96 with 24px nine-slice borders. **Reuse the prototype PNG/SVG kit already supplied in UI_HANDOFF.zip**; copied reference assets are under `art/reference/ui_handoff/assets/`. Its dark ink, cool grey rims and gold selection accents define GUI geometry and palette. Health caps use the handoff’s 8px convention; the full-size fill is clipped in code. HUD graphics contain no baked labels, numbers or item icons. Generation prompts for these existing components are optional later polish, not a request to replace the kit. Text layout and fonts remain with Claude; the archive supplies Noto Sans and its OFL licence.

The narrative handoff sets the 1920×640 wall breach at x=760–1160 on a 1920×1080 stage, with Dave’s ground point at (1040,790). Rubble canvases are 64×64, 96×96, 128×96 and 160×128; the three fallen defenders remain still. `spr_intro_banner` is 128×192 with six frames at 8fps, right attachment fixed and cloth pulling left; `spr_intro_spear` is 128×64. Dave’s turn is four frames at **8fps**, exactly 0.5 seconds. Optional `spr_dave_grief_down` and `spr_dave_vow_down` are still poses. Dave has base, solemn and determined portraits; Pharaoh’s base is controlled menace. Rage is an unused P2 option. These refinements are reflected in the manifest and prompts.

## Engine handoff issues

| Issue | Evidence and impact | Concrete correction for Claude |
|---|---|---|
| Right-hand sword versus mirroring | Contract §4 mirrors E/NE/SE for W/NW/SW. A full sprite mirror swaps anatomical handedness and moves the upper-left light to upper-right. The user explicitly requested authored left/right/up walks and attacks with the right hand preserved. | West is now delivered as `spr_dave_walk_left` / `spr_dave_attack_left`, independently authored from v002. Claude should register those IDs and bind index 4 with positive xscale. The contract was not edited and no runtime mapping was applied. Left diagonals still need separately authored art or a composed arm/lighting solution. |
| Slash playback versus active gate | Four slash frames at 20fps last 200ms; Dave’s active f2–4 last 9 game ticks, 150ms. At uniform 20fps the last slash pose begins as the active gate closes. | Preferred proposed runtime mapping: show the four poses for [2,2,2,3] game ticks within the active window. This changes the uniform playback instruction, so Claude should record that timing decision. Deliver the requested four poses and retain the 20fps specification pending that update. |
| Stairs source versus empty tile zero | The specified 192×128 source contains six occupied 64px cells. Treating its first cell as engine empty tile zero loses left_top. | Import/repack to an engine atlas with a separate empty slot and correct cell mapping. Keep the requested source sheet intact. |
| Projectile/rod coordinates | Nock and staff-tip offsets cannot be measured until native frames exist. | Keep offsets `null` while pending. Measure dx,dy at f5 for ranged enemies and every charge/fire frame for the Pharaoh. Engine mirroring must transform signed offsets consistently. |
| Original template screenshots unavailable | The original brief has been recovered, and the narrative/UI handoffs have been read. No original gameplay screenshots were attached or found. UI mockups are explicitly schematic. | Actual template PNGs and metadata anchor this guide. Recheck screenshot-specific composition or palette differences when original gameplay captures are available. Do not substitute schematic UI scene drawings as a gameplay style reference. |

These are reviewable art/integration decisions. No `.yy`, `.yyp`, `.gml`, room layout or runtime JSON was modified by this handoff.

## Delivery and inspection gates

1. **Generated source:** keep the original returned PNG and its prompt in `art/source/`. Record actual size and alpha statistics. Source size, apparent grid, apparent transparency and a requested loop are not evidence of a valid export.
2. **Identity and pose review:** compare native-size reference, silhouette, upper-left light, anatomy, hand, costume layers and ground point. Approve one base and one facing before animation variants.
3. **Cleanup and export candidate:** manually correct drifting anatomy, outlines, palette noise and stray alpha. Fit/export to the exact contracted canvas without per-frame trimming. Preserve straight alpha, sRGB and 8-bit channels. Do not simply resize a whole multi-frame source and assume equal cells.
4. **Mechanical inspection:** verify each frame’s dimensions, count, filename order, alpha, origin, body bounds and padding. Composite over white, black, pale sand and dark ruins to expose fringes. Confirm solid interiors where appropriate; FX and glass may be intentionally translucent. Sample the source/export colour at alpha edges to check for premultiplied dark fringes.
5. **Animation inspection:** play at actual timings, slow-scrub every pose, overlay planted feet and body landmarks, check sword attachment and release/contact indices. Inspect at least three repeated cycles for loops and the explicit last-to-first seam. Generate a strip/GIF review only after frame extraction has been checked. Check death holds and transparent final FX frames.
6. **Material/modular inspection:** inspect 3×3 spatial repeats, offset seams and adjoining terrain blends. Assemble stairs/bridges and test their repeated middle sections. No seamless or correct-grid claim is made until these checks pass.
7. **Claude integration acceptance:** deliver individual `<asset>_00.png` frames or `<asset>_stripN.png`, a sidecar with exact origin/timing/measured offsets, the selected model reference, and a completed inspection report. Claude validates native in-game scale, terrain contrast, placeholders, depth and timing in the IDE. Only then mark the asset `verified_engine_ready` and replace its placeholder.

The machine-readable [manifest](../art/asset_manifest.json) and its linked prompts supply these fields for every art asset. `verified_engine_ready` is currently false for every entry because engine acceptance remains with Claude. Nine Dave animation entries now link locally inspected native frames/strips and populated sidecars: 80 frames in total. [Generation log](ART_GENERATION_LOG.md) distinguishes source, native-export and engine-acceptance states. The reusable [sidecar template](../art/reference/asset_sidecar_template.json) deliberately uses nulls for unmeasured values.

## Small batch queue

1. Base lock: Dave down cleanup and right/left/up facing references are complete. Use these checked bases; derive diagonal bases before animating them.
2. Dave down idle/walk/attack and right/left/up walk/attack are delivered from separate jobs. See both handoffs for files, checks and remaining polish; Claude’s native-speed integration preview is next.
3. Slash alone. Then remaining diagonal bases, diagonal actions and additional idle states, one action and facing per job. Preserve the authored west handedness convention.
4. Undead neutral base, down idle/walk/attack/hurt/defeat/rise separately, then side/up walk and attack separately.
5. Light sand detail variants separately, dark sand, rock top and cliff face separately; inspect repeats and blend compatibility.
6. Chest, checkpoint star, sparkle and health potion separately. The health-potion source has been started independently. Validate and reuse the existing HUD prototype kit; its generation prompts are optional polish.

Follow the later manifest milestones in order. Work on static props/materials while a character is waiting for cleanup. Portraits follow the identity model, and Pharaoh animation follows his base/rod lock. All later prompts are prepared; this is not an instruction to generate them as a giant sheet or to bypass base approval.
