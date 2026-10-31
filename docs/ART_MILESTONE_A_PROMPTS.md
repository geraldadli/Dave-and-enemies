# Dave’s and Enemies Milestone A art prompts

Copy-ready generation prompts for the next playable milestone. Run only one prompt at a time. Establish and inspect each character base before its animation prompts. All numeric sizes below are final export targets, not claims about generator output. Full inspection specifications are in the JSON manifest.

Recommended queue: Dave base reference → down idle → down walk → down attack → slash → other Dave facings one action at a time → undead base and its down-facing actions → remaining undead facings → materials one variant at a time → chest → checkpoint and sparkle → potion icon. Reuse the existing HUD prototype kit from UI_HANDOFF.zip; HUD prompts are optional later polish. Independent static assets may proceed while character cleanup is pending.

Dave v002 now has native down idle plus walk/attack for down, right, independently authored left, and up:80 animation frames total. See ART_DAVE_DOWN_HANDOFF.md and ART_DAVE_CARDINAL_HANDOFF.md before regenerating them. The latest batch adds54 frames. Native PNG/strip checks passed; engine acceptance remains with Claude. Left walk/attack IDs were added under the explicit user continuation; bind them for west without mirroring. Health-potion source v001 still needs export.

## spr_dave_idle_down

```text
Use case: identity-preserve.

Asset ID: spr_dave_idle_down. Purpose: dave idle. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 768x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 neutral baseline; f1-3 inhale and cape/hair trail by at most 1-2 native pixels; f4 breath crest; f5-7 settle. No foot lifting. Last-to-first continues the motion without a duplicate terminal frame.

Playback specification: 10 fps; loop. contract.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_walk_down

```text
Use case: identity-preserve.

Asset ID: spr_dave_walk_down. Purpose: dave walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 10 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 960x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 passing into first stride; f1 approach; f2 first foot CONTACT; f3 load; f4 push; f5 opposite passing; f6 approach; f7 opposite foot CONTACT; f8 load; f9 push returning to f0. Ground anchor fixed, body bob <=2 native pixels; cape and hair lag the torso by one pose.

Playback specification: 20 fps; loop. contract.

Additional constraints: Contacts are zero-based frame indices 2 and 7. Keep both soles aligned to the ground plane; do not duplicate f0 as an extra end frame.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_attack_down

```text
Use case: identity-preserve.

Asset ID: spr_dave_attack_down. Purpose: dave attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0 planted stance, f1 right-hand windup; ACTIVE f2 begin right-to-left sweep, f3 CONTACT/strongest cut, f4 follow-through; RECOVERY f5 decelerate, f6 lower blade, f7 return toward neutral. Only f2-4 are active.

Timing: at 60Hz hold frames 0..7 for [3, 3, 3, 3, 3, 4, 4, 4] game ticks respectively; not uniform sprite fps. contract: 27 game ticks at 60 Hz, 450 ms.

Additional constraints: Body is the same 76-80 pixels tall as locomotion, simply repositioned for the new origin. Do not bake a slash arc into the character frames. Weapon follows an anatomically continuous path with the right hand closed around the grip.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_idle_down_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_idle_down_side. Purpose: dave idle. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen down-right at 45 degrees; preserve the elevated camera and anatomical right sword hand.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 768x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 neutral baseline; f1-3 inhale and cape/hair trail by at most 1-2 native pixels; f4 breath crest; f5-7 settle. No foot lifting. Last-to-first continues the motion without a duplicate terminal frame.

Playback specification: 10 fps; loop. contract.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_walk_down_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_walk_down_side. Purpose: dave walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen down-right at 45 degrees; preserve the elevated camera and anatomical right sword hand.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 10 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 960x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 passing into first stride; f1 approach; f2 first foot CONTACT; f3 load; f4 push; f5 opposite passing; f6 approach; f7 opposite foot CONTACT; f8 load; f9 push returning to f0. Ground anchor fixed, body bob <=2 native pixels; cape and hair lag the torso by one pose.

Playback specification: 20 fps; loop. contract.

Additional constraints: Contacts are zero-based frame indices 2 and 7. Keep both soles aligned to the ground plane; do not duplicate f0 as an extra end frame.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_attack_down_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_attack_down_side. Purpose: dave attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen down-right at 45 degrees; preserve the elevated camera and anatomical right sword hand.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0 planted stance, f1 right-hand windup; ACTIVE f2 begin right-to-left sweep, f3 CONTACT/strongest cut, f4 follow-through; RECOVERY f5 decelerate, f6 lower blade, f7 return toward neutral. Only f2-4 are active.

Timing: at 60Hz hold frames 0..7 for [3, 3, 3, 3, 3, 4, 4, 4] game ticks respectively; not uniform sprite fps. contract: 27 game ticks at 60 Hz, 450 ms.

Additional constraints: Body is the same 76-80 pixels tall as locomotion, simply repositioned for the new origin. Do not bake a slash arc into the character frames. Weapon follows an anatomically continuous path with the right hand closed around the grip.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_idle_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_idle_side. Purpose: dave idle. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen right; retain visible top surfaces and readable overlapping forms, not a flat side-scroller camera.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 768x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 neutral baseline; f1-3 inhale and cape/hair trail by at most 1-2 native pixels; f4 breath crest; f5-7 settle. No foot lifting. Last-to-first continues the motion without a duplicate terminal frame.

Playback specification: 10 fps; loop. contract.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_walk_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_walk_side. Purpose: dave walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen right; retain visible top surfaces and readable overlapping forms, not a flat side-scroller camera.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 10 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 960x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 passing into first stride; f1 approach; f2 first foot CONTACT; f3 load; f4 push; f5 opposite passing; f6 approach; f7 opposite foot CONTACT; f8 load; f9 push returning to f0. Ground anchor fixed, body bob <=2 native pixels; cape and hair lag the torso by one pose.

Playback specification: 20 fps; loop. contract.

Additional constraints: Contacts are zero-based frame indices 2 and 7. Keep both soles aligned to the ground plane; do not duplicate f0 as an extra end frame.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_attack_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_attack_side. Purpose: dave attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen right; retain visible top surfaces and readable overlapping forms, not a flat side-scroller camera.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0 planted stance, f1 right-hand windup; ACTIVE f2 begin right-to-left sweep, f3 CONTACT/strongest cut, f4 follow-through; RECOVERY f5 decelerate, f6 lower blade, f7 return toward neutral. Only f2-4 are active.

Timing: at 60Hz hold frames 0..7 for [3, 3, 3, 3, 3, 4, 4, 4] game ticks respectively; not uniform sprite fps. contract: 27 game ticks at 60 Hz, 450 ms.

Additional constraints: Body is the same 76-80 pixels tall as locomotion, simply repositioned for the new origin. Do not bake a slash arc into the character frames. Weapon follows an anatomically continuous path with the right hand closed around the grip.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_idle_up_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_idle_up_side. Purpose: dave idle. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen up-right at 45 degrees; show rear three-quarter forms with coherent foreshortening.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 768x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 neutral baseline; f1-3 inhale and cape/hair trail by at most 1-2 native pixels; f4 breath crest; f5-7 settle. No foot lifting. Last-to-first continues the motion without a duplicate terminal frame.

Playback specification: 10 fps; loop. contract.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_walk_up_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_walk_up_side. Purpose: dave walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen up-right at 45 degrees; show rear three-quarter forms with coherent foreshortening.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 10 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 960x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 passing into first stride; f1 approach; f2 first foot CONTACT; f3 load; f4 push; f5 opposite passing; f6 approach; f7 opposite foot CONTACT; f8 load; f9 push returning to f0. Ground anchor fixed, body bob <=2 native pixels; cape and hair lag the torso by one pose.

Playback specification: 20 fps; loop. contract.

Additional constraints: Contacts are zero-based frame indices 2 and 7. Keep both soles aligned to the ground plane; do not duplicate f0 as an extra end frame.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_attack_up_side

```text
Use case: identity-preserve.

Asset ID: spr_dave_attack_up_side. Purpose: dave attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen up-right at 45 degrees; show rear three-quarter forms with coherent foreshortening.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0 planted stance, f1 right-hand windup; ACTIVE f2 begin right-to-left sweep, f3 CONTACT/strongest cut, f4 follow-through; RECOVERY f5 decelerate, f6 lower blade, f7 return toward neutral. Only f2-4 are active.

Timing: at 60Hz hold frames 0..7 for [3, 3, 3, 3, 3, 4, 4, 4] game ticks respectively; not uniform sprite fps. contract: 27 game ticks at 60 Hz, 450 ms.

Additional constraints: Body is the same 76-80 pixels tall as locomotion, simply repositioned for the new origin. Do not bake a slash arc into the character frames. Weapon follows an anatomically continuous path with the right hand closed around the grip.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_idle_up

```text
Use case: identity-preserve.

Asset ID: spr_dave_idle_up. Purpose: dave idle. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen up away from the camera; show rear surfaces and correctly occluded body attachments while preserving the elevated camera.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 768x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 neutral baseline; f1-3 inhale and cape/hair trail by at most 1-2 native pixels; f4 breath crest; f5-7 settle. No foot lifting. Last-to-first continues the motion without a duplicate terminal frame.

Playback specification: 10 fps; loop. contract.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_walk_up

```text
Use case: identity-preserve.

Asset ID: spr_dave_walk_up. Purpose: dave walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen up away from the camera; show rear surfaces and correctly occluded body attachments while preserving the elevated camera.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 10 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 960x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 passing into first stride; f1 approach; f2 first foot CONTACT; f3 load; f4 push; f5 opposite passing; f6 approach; f7 opposite foot CONTACT; f8 load; f9 push returning to f0. Ground anchor fixed, body bob <=2 native pixels; cape and hair lag the torso by one pose.

Playback specification: 20 fps; loop. contract.

Additional constraints: Contacts are zero-based frame indices 2 and 7. Keep both soles aligned to the ground plane; do not duplicate f0 as an extra end frame.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_attack_up

```text
Use case: identity-preserve.

Asset ID: spr_dave_attack_up. Purpose: dave attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen up away from the camera; show rear surfaces and correctly occluded body attachments while preserving the elevated camera.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0 planted stance, f1 right-hand windup; ACTIVE f2 begin right-to-left sweep, f3 CONTACT/strongest cut, f4 follow-through; RECOVERY f5 decelerate, f6 lower blade, f7 return toward neutral. Only f2-4 are active.

Timing: at 60Hz hold frames 0..7 for [3, 3, 3, 3, 3, 4, 4, 4] game ticks respectively; not uniform sprite fps. contract: 27 game ticks at 60 Hz, 450 ms.

Additional constraints: Body is the same 76-80 pixels tall as locomotion, simply repositioned for the new origin. Do not bake a slash arc into the character frames. Weapon follows an anatomically continuous path with the right hand closed around the grip.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_walk_left

```text
Use case: identity-preserve.

Asset ID: spr_dave_walk_left. Purpose: dave walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen left in the independently authored west view. Right anatomical arm is far/upstage and holds the sword; near left hand stays empty. Preserve upper-left screen lighting; do not mirror an east-facing image.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (48, 88). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 10 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 960x96, or individual fixed 96x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 passing; f1 first leg swing; f2 first CONTACT; f3 load; f4 push; f5 opposite passing; f6 opposite swing; f7 opposite CONTACT; f8 load; f9 push into f0. Walk west in place; no duplicate terminal frame.

Playback specification: 20 fps; loop. contract walk count/rate; independent left authoring explicitly requested by user.

Additional constraints: Attach art/source/dave/cardinal_batch_v001/dave_base_left_source_v001.png as the facing model. Far anatomical right hand holds sword; near left hand is empty. No full-sprite mirror. Contacts f2/f7.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_dave_attack_left

```text
Use case: identity-preserve.

Asset ID: spr_dave_attack_left. Purpose: dave attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Subject: Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand.

Direction: Face screen left in the independently authored west view. Right anatomical arm is far/upstage and holds the sword; near left hand stays empty. Preserve upper-left screen lighting; do not mirror an east-facing image.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0-1; ACTIVE f2-4 with CONTACT f3 toward west; RECOVERY f5-7. Keep the far right-shoulder/elbow/wrist/grip chain; near left hand remains empty.

Timing: at 60Hz hold frames 0..7 for [3, 3, 3, 3, 3, 4, 4, 4] game ticks respectively; not uniform sprite fps. contract:27 game ticks at60Hz,450ms.

Additional constraints: Attach the established authored-left base. Upper-left light stays fixed. Do not mirror the right attack; use the anatomical right arm. Slash FX separate.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_fx_slash

```text
Use case: stylized-concept.

Asset ID: spr_fx_slash. Purpose: A white-gold sword crescent growing from its pivot and sweeping toward east. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Subject: A white-gold sword crescent growing from its pivot and sweeping toward east

Direction: Point along +x, screen east. The engine will rotate the image; no additional rotated copies.

Final target: 128x96 native pixels PER FRAME; All frames fixed 128x96 canvas, no trimming; origin (16, 48). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 4 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 512x96, or individual fixed 128x96 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 thin leading edge; f1 broad CONTACT crescent; f2 taper and split tail; f3 residual taper, mostly transparent.

Playback specification: 20 fps; once. contract: 20 fps once; runtime gate conflict recorded in visual guide.

Additional constraints: Only the arc, no sword or character. The pivot is at (16,48), positive x to the right. The engine rotates it toward the mouse and shows it only while the attack is active. Source duration 200 ms conflicts with 150 ms active window; do not silently retime it.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Effect centre/pivot stays fixed and fits every frame. Readable silhouette at 1280x720 on both terrain extremes. No opaque rectangle, stray alpha or dark premultiplied fringe. No full-screen strobe; loop luminance and seam inspected if looping. Any ground ring is an elevated-view ellipse, not a face-on circle.
```

## tex_sand_light ripples

```text
Use case: stylized-concept.

Asset ID: tex_sand_light. Purpose: Seamless terrain material. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach the original template floor/wall images for material density, broad shading and restrained contrast. Render an orthographic flat material sample, no perspective or vignette. Smooth illustrated game texture, not coarse pixel art.

Subject: Pale warm beige desert sand with low-contrast fine grain, broad sparse shallow ripple clusters and restrained upper-left relief. Keep dark contours off flat terrain.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 256x256 native pixels PER FRAME; Material origin top-left (0,0); no camera perspective or directional lighting gradient.

Transparency: opaque RGBA, alpha 255 throughout.

Material detail variant ripples ONLY: Sparse broad wind ripples, no pebble objects. Do not generate the other variants in the same image.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Repeat on all four edges; no visible central landmark, border or lighting vignette. This is a material texture, not a 47-tile autotile sheet. Engineering creates the blends.

Inspection before acceptance: Check exact final dimensions and alpha 255 everywhere. Inspect a 3x3 repeat and a half-width/half-height offset for seams; repair visible breaks before acceptance. Compare grain and motif scale against the 64-pixel template tiles. Test blending with adjacent terrain in a room preview; do not claim seamlessness from a prompt alone.
```

## tex_sand_light pebbles

```text
Use case: stylized-concept.

Asset ID: tex_sand_light. Purpose: Seamless terrain material. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach the original template floor/wall images for material density, broad shading and restrained contrast. Render an orthographic flat material sample, no perspective or vignette. Smooth illustrated game texture, not coarse pixel art.

Subject: Pale warm beige desert sand with low-contrast fine grain, broad sparse shallow ripple clusters and restrained upper-left relief. Keep dark contours off flat terrain.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 256x256 native pixels PER FRAME; Material origin top-left (0,0); no camera perspective or directional lighting gradient.

Transparency: opaque RGBA, alpha 255 throughout.

Material detail variant pebbles ONLY: Sparse tiny embedded ochre and cool-grey pebbles, below object-art contrast. Do not generate the other variants in the same image.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Repeat on all four edges; no visible central landmark, border or lighting vignette. This is a material texture, not a 47-tile autotile sheet. Engineering creates the blends.

Inspection before acceptance: Check exact final dimensions and alpha 255 everywhere. Inspect a 3x3 repeat and a half-width/half-height offset for seams; repair visible breaks before acceptance. Compare grain and motif scale against the 64-pixel template tiles. Test blending with adjacent terrain in a room preview; do not claim seamlessness from a prompt alone.
```

## tex_sand_light cracks

```text
Use case: stylized-concept.

Asset ID: tex_sand_light. Purpose: Seamless terrain material. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach the original template floor/wall images for material density, broad shading and restrained contrast. Render an orthographic flat material sample, no perspective or vignette. Smooth illustrated game texture, not coarse pixel art.

Subject: Pale warm beige desert sand with low-contrast fine grain, broad sparse shallow ripple clusters and restrained upper-left relief. Keep dark contours off flat terrain.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 256x256 native pixels PER FRAME; Material origin top-left (0,0); no camera perspective or directional lighting gradient.

Transparency: opaque RGBA, alpha 255 throughout.

Material detail variant cracks ONLY: Very sparse shallow hairline dry cracks, low contrast, no giant mud plates. Do not generate the other variants in the same image.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Repeat on all four edges; no visible central landmark, border or lighting vignette. This is a material texture, not a 47-tile autotile sheet. Engineering creates the blends.

Inspection before acceptance: Check exact final dimensions and alpha 255 everywhere. Inspect a 3x3 repeat and a half-width/half-height offset for seams; repair visible breaks before acceptance. Compare grain and motif scale against the 64-pixel template tiles. Test blending with adjacent terrain in a room preview; do not claim seamlessness from a prompt alone.
```

## tex_sand_dark

```text
Use case: stylized-concept.

Asset ID: tex_sand_dark. Purpose: Seamless terrain material. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach the original template floor/wall images for material density, broad shading and restrained contrast. Render an orthographic flat material sample, no perspective or vignette. Smooth illustrated game texture, not coarse pixel art.

Subject: Muted medium warm ochre sand, same grain scale as tex_sand_light, gently compacted path material. No painted path edges or dark outline; engineering blends its irregular margins.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 256x256 native pixels PER FRAME; Material origin top-left (0,0); no camera perspective or directional lighting gradient.

Transparency: opaque RGBA, alpha 255 throughout.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Repeat on all four edges; no visible central landmark, border or lighting vignette. This is a material texture, not a 47-tile autotile sheet. Engineering creates the blends.

Inspection before acceptance: Check exact final dimensions and alpha 255 everywhere. Inspect a 3x3 repeat and a half-width/half-height offset for seams; repair visible breaks before acceptance. Compare grain and motif scale against the 64-pixel template tiles. Test blending with adjacent terrain in a room preview; do not claim seamlessness from a prompt alone.
```

## tex_rock_top

```text
Use case: stylized-concept.

Asset ID: tex_rock_top. Purpose: Seamless terrain material. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach the original template floor/wall images for material density, broad shading and restrained contrast. Render an orthographic flat material sample, no perspective or vignette. Smooth illustrated game texture, not coarse pixel art.

Subject: Desert canyon top rock: muted ochre-grey broad flat angular planes, occasional fine fissures. Match the template stone density and upper-left highlights without strong continuous diagonal stripes.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 256x256 native pixels PER FRAME; Material origin top-left (0,0); no camera perspective or directional lighting gradient.

Transparency: opaque RGBA, alpha 255 throughout.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Repeat on all four edges; no visible central landmark, border or lighting vignette. This is a material texture, not a 47-tile autotile sheet. Engineering creates the blends.

Inspection before acceptance: Check exact final dimensions and alpha 255 everywhere. Inspect a 3x3 repeat and a half-width/half-height offset for seams; repair visible breaks before acceptance. Compare grain and motif scale against the 64-pixel template tiles. Test blending with adjacent terrain in a room preview; do not claim seamlessness from a prompt alone.
```

## tex_cliff_face

```text
Use case: stylized-concept.

Asset ID: tex_cliff_face. Purpose: Seamless terrain material. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach the original template floor/wall images for material density, broad shading and restrained contrast. Render an orthographic flat material sample, no perspective or vignette. Smooth illustrated game texture, not coarse pixel art.

Subject: Vertical front face of desert canyon rock with horizontal strata, broad ochre-brown slab faces, dark lower-right recesses and restrained top-left ledge light. No top cap, freestanding rock or horizon.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 256x64 native pixels PER FRAME; Material origin top-left (0,0); no camera perspective or directional lighting gradient.

Transparency: opaque RGBA, alpha 255 throughout.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Repeat horizontally only; preserve continuous top and bottom strata. This is a material texture, not a 47-tile autotile sheet. Engineering creates the blends.

Inspection before acceptance: Check exact final dimensions and alpha 255 everywhere. Inspect a 3x3 repeat and a half-width/half-height offset for seams; repair visible breaks before acceptance. Compare grain and motif scale against the 64-pixel template tiles. Test blending with adjacent terrain in a room preview; do not claim seamlessness from a prompt alone.
```

## spr_undead_idle_down

```text
Use case: identity-preserve.

Asset ID: spr_undead_idle_down. Purpose: undead idle. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 6 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 768x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 baseline; f1-2 shoulders rise; f3 crest; f4-5 settle, grounded feet. A slow dry breathing sway.

Playback specification: 10 fps; loop. 6 frames from A6; 10 fps from contract idle default.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_walk_down

```text
Use case: identity-preserve.

Asset ID: spr_undead_walk_down. Purpose: undead walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 drag; f1 approach; f2 first CONTACT; f3 load; f4 drag opposite; f5 approach; f6 opposite CONTACT; f7 load. Slow uneven gait without changing leg length.

Playback specification: 12 fps; loop. 8 frames from A6; 12 fps and contacts f2/f6 are art recommendations (not Dave step indices).

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_attack_down

```text
Use case: identity-preserve.

Asset ID: spr_undead_attack_down. Purpose: undead attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0-3 shoulders rise and reaching arm pulls back; ACTIVE f4 reach begins, f5 CONTACT swipe; RECOVERY f6 decelerate, f7 return. Keep the planted foot anchor.

Timing: at 60Hz hold frames 0..7 for [6, 6, 6, 6, 4, 4, 7, 7] game ticks respectively; not uniform sprite fps. frame ranges from A6; durations proposed for Claude enemy data.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_walk_side

```text
Use case: identity-preserve.

Asset ID: spr_undead_walk_side. Purpose: undead walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen right; retain visible top surfaces and readable overlapping forms, not a flat side-scroller camera.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 drag; f1 approach; f2 first CONTACT; f3 load; f4 drag opposite; f5 approach; f6 opposite CONTACT; f7 load. Slow uneven gait without changing leg length.

Playback specification: 12 fps; loop. 8 frames from A6; 12 fps and contacts f2/f6 are art recommendations (not Dave step indices).

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_attack_side

```text
Use case: identity-preserve.

Asset ID: spr_undead_attack_side. Purpose: undead attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen right; retain visible top surfaces and readable overlapping forms, not a flat side-scroller camera.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0-3 shoulders rise and reaching arm pulls back; ACTIVE f4 reach begins, f5 CONTACT swipe; RECOVERY f6 decelerate, f7 return. Keep the planted foot anchor.

Timing: at 60Hz hold frames 0..7 for [6, 6, 6, 6, 4, 4, 7, 7] game ticks respectively; not uniform sprite fps. frame ranges from A6; durations proposed for Claude enemy data.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_walk_up

```text
Use case: identity-preserve.

Asset ID: spr_undead_walk_up. Purpose: undead walk. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen up away from the camera; show rear surfaces and correctly occluded body attachments while preserving the elevated camera.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 drag; f1 approach; f2 first CONTACT; f3 load; f4 drag opposite; f5 approach; f6 opposite CONTACT; f7 load. Slow uneven gait without changing leg length.

Playback specification: 12 fps; loop. 8 frames from A6; 12 fps and contacts f2/f6 are art recommendations (not Dave step indices).

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_attack_up

```text
Use case: identity-preserve.

Asset ID: spr_undead_attack_up. Purpose: undead attack. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen up away from the camera; show rear surfaces and correctly occluded body attachments while preserving the elevated camera.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: ANTICIPATION f0-3 shoulders rise and reaching arm pulls back; ACTIVE f4 reach begins, f5 CONTACT swipe; RECOVERY f6 decelerate, f7 return. Keep the planted foot anchor.

Timing: at 60Hz hold frames 0..7 for [6, 6, 6, 6, 4, 4, 7, 7] game ticks respectively; not uniform sprite fps. frame ranges from A6; durations proposed for Claude enemy data.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_hurt_down

```text
Use case: identity-preserve.

Asset ID: spr_undead_hurt_down. Purpose: undead hurt. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 2 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 256x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 impact recoil with body compression; f1 guarded settle. No full-canvas white flash.

Playback specification: 12 fps; once. contract default hurt playback.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_defeat

```text
Use case: identity-preserve.

Asset ID: spr_undead_defeat. Purpose: undead defeat. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face down toward the camera; do not generate additional directions.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1024x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 losing balance; f1-2 knees buckle; f3 ground CONTACT; f4-6 cloth and limbs settle; f7 still remains. No gore or full-screen flash.

Playback specification: 12 fps; once_hold. 8 frames from A6; 12 fps chosen within contract range.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_undead_rise

```text
Use case: identity-preserve.

Asset ID: spr_undead_rise. Purpose: undead rise. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.

Attach the established undead base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.

Subject: A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.

Direction: Face down toward the camera; do not generate additional directions.

Final target: 128x128 native pixels PER FRAME; All frames fixed 128x128 canvas, no trimming; origin (64, 112). Anchor is the feet or ground point; no baked ground shadow.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 10 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 1280x128, or individual fixed 128x128 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 concealed below sand; f1-2 cloth and hand protrude; f3-5 shoulders and skull lift; f6-7 knees plant; f8 weight transfer; f9 baseline standing silhouette. Keep the same ground point.

Playback specification: 12 fps; once. 10 frames from A6; 12 fps proposed.

Additional constraints: Only the undead body and attached loose sand; separate summoning cracks and sand-burst FX are supplied for the boss milestone.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Inspect all frames over the same body/ground overlay; no head-size or anatomy drift. Weapon hand, garment layers, palette and upper-left highlights remain fixed. Read the silhouette at native size on pale sand and dark ruins. Check chronological pose order, contact/release frames and last-to-first transition if looping. No weapon, cape, ear or effect clipped at a canvas edge.
```

## spr_chest_desert

```text
Use case: stylized-concept.

Asset ID: spr_chest_desert. Purpose: Treasure chest states. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Subject: A squat desert treasure chest, warm weathered golden-brown planks, cool iron edge bands and a simple centred latch. Visible lid top and front in the template elevated camera, no elaborate emblem.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 64x64 native pixels PER FRAME; All frames fixed 64x64 canvas, no trimming; origin (32, 56). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 6 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 384x64, or individual fixed 64x64 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 closed; f1 latch releases and lid cracks; f2 half open; f3 approaching full lift; f4 opening settles; f5 fully open and held. Base and hinge remain registered.

Playback/state selection: state_driven. states and counts from A7; opening proposed at 12 fps for four frames.

Collision footprint reference (not painted into art): 48x20 pixels at the base.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: All six frames use the same base and hinge location. Footprint 48x20 is centred on (32,56). Open lid fits inside 64x64 without shrinking the chest. Closed/open are holds; opening is a four-frame one-shot.
```

## spr_checkpoint_star

```text
Use case: stylized-concept.

Asset ID: spr_checkpoint_star. Purpose: A warm yellow five-point checkpoint star, small amber outline and gentle gold inner glow, hovering over its fixed anchor. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Subject: A warm yellow five-point checkpoint star, small amber outline and gentle gold inner glow, hovering over its fixed anchor

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 64x64 native pixels PER FRAME; All frames fixed 64x64 canvas, no trimming; origin (32, 48). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 8 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 512x64, or individual fixed 64x64 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 low glow; f1-3 rise gently; f4 glow crest; f5-7 return. Star shape and location remain stable; pulse luminance gently, no flashing.

Playback specification: 10 fps; loop. contract.

Additional constraints: The bottom hover anchor is (32,48). Glow must stay within bounds. Star core is opaque, outer glow can use graded alpha. No baked ground shadow, save text or pedestal.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Effect centre/pivot stays fixed and fits every frame. Readable silhouette at 1280x720 on both terrain extremes. No opaque rectangle, stray alpha or dark premultiplied fringe. No full-screen strobe; loop luminance and seam inspected if looping. Any ground ring is an elevated-view ellipse, not a face-on circle.
```

## spr_fx_sparkle

```text
Use case: stylized-concept.

Asset ID: spr_fx_sparkle. Purpose: A tiny pale-gold four-point star glint. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Subject: A tiny pale-gold four-point star glint

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 16x16 native pixels PER FRAME; All frames fixed 16x16 canvas, no trimming; origin (8, 8). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate ONLY this one asset/action/direction as 6 chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is 96x16, or individual fixed 16x16 frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.

Pose plan, zero-based indices: f0 point; f1-2 expand; f3 crest; f4 taper; f5 fade fully transparent.

Playback specification: 24 fps; once. art recommendation where request does not specify fps.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: Effect centre/pivot stays fixed and fits every frame. Readable silhouette at 1280x720 on both terrain extremes. No opaque rectangle, stray alpha or dark premultiplied fringe. No full-screen strobe; loop luminance and seam inspected if looping. Any ground ring is an elevated-view ellipse, not a face-on circle.
```

## spr_icon_potion_health

```text
Use case: stylized-concept.

Asset ID: spr_icon_potion_health. Purpose: Inventory item icon: potion_health. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, text, watermark, labels or checkerboard painted into pixels.

Subject: One squat clear glass flask, red healing liquid, cork stopper, simple brass neck band. No label or cross; broad soft shading, not faceted 3D.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 64x64 native pixels PER FRAME; All frames fixed 64x64 canvas, no trimming; origin (0, 0). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Single inventory item, readable at 48 pixels, full silhouette contained inside x=3..60 and y=3..60. Natural glass translucency is allowed, but no opaque rectangle.

Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.

Inspection before acceptance: At least 3 pixels of fully transparent padding on every side. Centred visual mass; readable at 48x48. No title, frame, cast shadow or white matte. Weapon/costume silhouette matches its character reference.
```

## spr_ui_hp_frame

```text
Use case: stylized-concept.

Asset ID: spr_ui_hp_frame. Purpose: Core HUD kit. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach this component from art/reference/ui_handoff/assets/ as the authoritative geometry and palette reference. The prototype is already supplied; reuse it for the current milestone. This optional generation prompt is for later approved art polish only. Preserve the existing dark ink/cool grey/gold hierarchy. This is flat screen-space UI, no world camera foreshortening.

Subject: Reuse the supplied UI health frame: dark ink well with cool grey rim, 8px cap/border scaling convention. It is an empty bar backing, with no baked text or health fill.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 320x32 native pixels PER FRAME; All frames fixed 320x32 canvas, no trimming; origin (0, 0). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Screen-space UI, not a top-down world object. No baked letters, numbers, labels or item art; preserve border sizes exactly.

Inspection before acceptance: Read at native 1280x720 GUI scale. Bar fill and frame align pixel for pixel. Selection reads through shape and value. Panel corners survive nine-slice stretch tests at 320x160 and 760x300.
```

## spr_ui_hp_fill

```text
Use case: stylized-concept.

Asset ID: spr_ui_hp_fill. Purpose: Core HUD kit. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach this component from art/reference/ui_handoff/assets/ as the authoritative geometry and palette reference. The prototype is already supplied; reuse it for the current milestone. This optional generation prompt is for later approved art polish only. Preserve the existing dark ink/cool grey/gold hierarchy. This is flat screen-space UI, no world camera foreshortening.

Subject: Reuse the supplied full-size red health fill, no border, text, skull or heart. Source 320x32, same full dimensions as the frame; engine clips it to the destination track. Do not add a new 4px source inset.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 320x32 native pixels PER FRAME; All frames fixed 320x32 canvas, no trimming; origin (0, 0). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Screen-space UI, not a top-down world object. No baked letters, numbers, labels or item art; preserve border sizes exactly.

Inspection before acceptance: Read at native 1280x720 GUI scale. Bar fill and frame align pixel for pixel. Selection reads through shape and value. Panel corners survive nine-slice stretch tests at 320x160 and 760x300.
```

## spr_ui_slot

```text
Use case: stylized-concept.

Asset ID: spr_ui_slot. Purpose: Core HUD kit. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach this component from art/reference/ui_handoff/assets/ as the authoritative geometry and palette reference. The prototype is already supplied; reuse it for the current milestone. This optional generation prompt is for later approved art polish only. Preserve the existing dark ink/cool grey/gold hierarchy. This is flat screen-space UI, no world camera foreshortening.

Subject: Reuse the supplied empty square inventory slot, dark ink centre and cool grey rim. No icon, key glyph, equipment badge or text.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 72x72 native pixels PER FRAME; All frames fixed 72x72 canvas, no trimming; origin (0, 0). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Screen-space UI, not a top-down world object. No baked letters, numbers, labels or item art; preserve border sizes exactly.

Inspection before acceptance: Read at native 1280x720 GUI scale. Bar fill and frame align pixel for pixel. Selection reads through shape and value. Panel corners survive nine-slice stretch tests at 320x160 and 760x300.
```

## spr_ui_slot_selected

```text
Use case: stylized-concept.

Asset ID: spr_ui_slot_selected. Purpose: Core HUD kit. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach this component from art/reference/ui_handoff/assets/ as the authoritative geometry and palette reference. The prototype is already supplied; reuse it for the current milestone. This optional generation prompt is for later approved art polish only. Preserve the existing dark ink/cool grey/gold hierarchy. This is flat screen-space UI, no world camera foreshortening.

Subject: Reuse the supplied selected-slot OVERLAY: transparent centre, gold outline, corners and selected marker aligned exactly to the base 72x72 slot. No icon or text.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 72x72 native pixels PER FRAME; All frames fixed 72x72 canvas, no trimming; origin (0, 0). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Screen-space UI, not a top-down world object. No baked letters, numbers, labels or item art; preserve border sizes exactly.

Inspection before acceptance: Read at native 1280x720 GUI scale. Bar fill and frame align pixel for pixel. Selection reads through shape and value. Panel corners survive nine-slice stretch tests at 320x160 and 760x300.
```

## spr_ui_panel

```text
Use case: stylized-concept.

Asset ID: spr_ui_panel. Purpose: Core HUD kit. Game: Dave's & Enemies, Chapter I Desert.

Reference roles: attach this component from art/reference/ui_handoff/assets/ as the authoritative geometry and palette reference. The prototype is already supplied; reuse it for the current milestone. This optional generation prompt is for later approved art polish only. Preserve the existing dark ink/cool grey/gold hierarchy. This is flat screen-space UI, no world camera foreshortening.

Subject: Reuse the supplied nine-slice UI panel: calm dark ink centre, cool grey border. Exact 24px borders on all sides, stretchable 48x48 centre without motifs. No baked text.

Direction: Use the exact single orientation described; do not generate additional views.

Final target: 96x96 native pixels PER FRAME; All frames fixed 96x96 canvas, no trimming; origin (0, 0). Keep placement fixed between frames.

Transparency: 8-bit RGBA, sRGB, straight alpha, transparent outside artwork.

Generate one static asset only, no contact sheet or alternative views.

Playback/state selection: static. contract.

Additional constraints: Screen-space UI, not a top-down world object. No baked letters, numbers, labels or item art; preserve border sizes exactly.

Inspection before acceptance: Read at native 1280x720 GUI scale. Bar fill and frame align pixel for pixel. Selection reads through shape and value. Panel corners survive nine-slice stretch tests at 320x160 and 760x300.
```
