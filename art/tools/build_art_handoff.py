"""Build art-only manifests and copy-ready prompts. Does not modify GameMaker resources."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'art'
DOCS = ROOT / 'docs'
ASSETS: list[dict] = []

STYLE = (
    "Match the supplied Hero's Trail template reference: elevated top-down three-quarter orthographic adventure view, "
    "smooth antialiased illustrated cartoon game art, dark charcoal outlines about 1-2 native pixels wide, broad soft cel shading, "
    "light from upper left, restrained highlights and slate or warm brown shadows. Human-sized humanoids have compact chibi proportions "
    "with heads about 35-40 percent of body height; creatures keep the specific anatomy described below. These are 64-pixel tiles with roughly 78-pixel-tall human bodies. "
    "Preserve native visual density; no coarse pixel grid, realistic rendering, anime redesign, isometric diamond grid, noisy microtexture, "
    "text, watermark, labels or checkerboard painted into pixels."
)
DAVE = (
    "Dave's established identity is v002. Use its cleaned master art/source/dave/down_batch_v001/dave_base_down_v002_clean_v001.png, "
    "with native registration art/exports/dave/down_v001/dave_base_down_reference/dave_base_down_reference_00.png; attach these together with "
    "art/reference/template_sprite_inspection.png. Preserve his swept long golden-brown hair to the shoulder blades, "
    "warm friendly resolute face, shining cool silver rounded paladin armor, ivory layered tabard, warm brown undergarments, "
    "brown belt and boots, deep red cape attached by two small brass shoulder clasps, and straight steel sword with brass "
    "crossguard and brown grip in his ANATOMICAL RIGHT hand. No shield. Keep the face, head-to-body ratio, shoulders, "
    "blade length, costume layers, cape attachment and upper-left light consistent. Body height 76-80 native pixels. "
    "For down view the sword hand is on image left; derive other facings by anatomy, never swap the weapon to the other hand."
)
ENTITIES = {
    'undead': 'A slow desiccated human undead with dusty olive-grey skin, hollow dark eyes, torn muted ochre wrappings and brown ragged garments. Heavy reaching arms, stooped readable silhouette, no sword, no fresh gore. Body height 76-80 pixels. Keep its silhouette distinct from the clean exposed skeleton families.',
    'skeleton_warrior': 'A dry ivory skeleton warrior, hollow charcoal sockets, clear ribcage, worn ochre shoulder guards, brown waist cloth, a short straight iron sword in anatomical right hand and a small worn round shield on the left forearm. Use the sword option consistently, not an interchangeable spear. Body height 76-80 pixels.',
    'skeleton_archer': 'A lean dry ivory skeleton archer with hollow sockets, muted ochre hood remnant, brown waist cloth and quiver, wooden recurved shortbow held in anatomical left hand and right hand drawing the string. Readable ribs and bow silhouette. Body height 76-80 pixels.',
    'bandit': 'An adult human desert bandit with a warm tan face, ochre head wrap exposing the eyes and lower face, muted brown layered tunic, russet sash, brown boots and one curved scimitar in anatomical right hand. No modern weapon or bright red cape. Fast compact silhouette, body height 76-80 pixels.',
    'bandit_caster': 'An adult human desert caster with a warm tan face, muted indigo hood and ochre layered robe, brown boots and a simple dark wooden staff capped by one small turquoise stone in anatomical right hand. Compact human silhouette, body height 76-80 pixels. Preserve the staff and tip location during holds.',
    'bat': 'A small charcoal-brown desert bat with warm brown wing membranes, clear ears and a compact face, about 40 pixels body/wing height and 56 pixels full wingspan. Symmetrical front-facing hovering body; keep the rib structure and wing joints consistent. No baked shadow.',
    'python': 'A heavy desert python about 100 native pixels long, ochre-tan scales with broad dark brown saddle patches, cream underside, dark eyes and a blunt believable snake head. Keep head size, pattern landmarks and continuous single spine consistent; no limbs, horns or multiple heads.',
    'sandworm': 'A large ochre sandworm 128-160 native pixels tall when emerged, broad segmented tan body, darker ring seams and a readable radial mouth with restrained ivory teeth. Front-facing, rising vertically from sand; no eyes added between frames, no tentacles, no gore. Keep mouth ring and segment count stable.',
    'pharaoh': 'The Undead Pharaoh, a regal desiccated adult mummy king, about 140 native pixels tall, floating above a fixed ground anchor. Narrow skeletal face, dark sockets with restrained amber inner light, ivory wrappings, muted lapis-and-gold striped nemes, broad gold collar and layered ivory robes with lapis and ochre trim. One consistent gold laser rod with an amber inset crown in anatomical right hand (image left while facing down). No scimitar, extra arms or recovered Grail. Fix the rod length and crown silhouette before animation.',
}
FACING = {
    'down': 'Face screen down toward the camera; elevated view, visible shoulder tops, feet on the fixed ground line.',
    'down_side': 'Face screen down-right at 45 degrees; preserve the elevated camera and anatomical right sword hand.',
    'side': 'Face screen right; retain visible top surfaces and readable overlapping forms, not a flat side-scroller camera.',
    'left': 'Face screen left in the independently authored west view. Right anatomical arm is far/upstage and holds the sword; near left hand stays empty. Preserve upper-left screen lighting; do not mirror an east-facing image.',
    'up_side': 'Face screen up-right at 45 degrees; show rear three-quarter forms with coherent foreshortening.',
    'up': 'Face screen up away from the camera; show rear surfaces and correctly occluded body attachments while preserving the elevated camera.',
    'front': 'Face down toward the camera; do not generate additional directions.',
    'east': 'Point along +x, screen east. The engine will rotate the image; no additional rotated copies.',
    'none': 'Use the exact single orientation described; do not generate additional views.',
}


def add(asset_id, milestone, request, purpose, size, origin, *, frames=1, fps=None,
        loop='static', facing='none', poses='', subject='', checks=(), kind='sprite',
        priority='P0', footprint=None, naming='contract', timing='contract', ticks=None,
        variants=None, extra='', depends=(), states=None):
    a = {
        'asset_id': asset_id, 'milestone': milestone, 'request': request, 'priority': priority,
        'purpose': purpose, 'kind': kind, 'id_status': naming,
        'target_dimensions_px': list(size), 'origin_px': list(origin) if origin is not None else None,
        'footprint_px': list(footprint) if footprint else None,
        'required_states': states or ['static' if frames == 1 else 'animation'],
        'animation': {'direction': facing, 'frame_count': frames, 'fps': fps, 'loop': loop,
                      'game_ticks_per_frame': ticks, 'timing_status': timing, 'pose_plan': poses},
        'transparency': 'opaque RGBA, alpha 255 throughout' if kind == 'material' else '8-bit RGBA, sRGB, straight alpha, transparent outside artwork',
        'alignment': ('Material origin top-left (0,0); no camera perspective or directional lighting gradient.' if kind == 'material'
                      else f'All frames fixed {size[0]}x{size[1]} canvas, no trimming; origin {origin}. ' +
                      ('Anchor is the feet or ground point; no baked ground shadow.' if kind == 'character' else 'Keep placement fixed between frames.')),
        'subject': subject, 'additional_instructions': extra, 'inspection_checklist': list(checks),
        'dependencies': list(depends), 'variants': variants or [], 'status': 'planned',
        'source_files': [], 'verified_engine_ready': False,
    }
    ASSETS.append(a)
    return a


def character(entity, action, direction, milestone, request, frames, fps, poses, *,
              loop='once', size=(128, 128), origin=(64, 112), ticks=None,
              timing='contract; unspecified duration is an art recommendation', extra='', priority='P0'):
    suffix = '' if direction == 'front' else '_' + direction
    aid = f'spr_{entity}_{action}{suffix}'
    return add(aid, milestone, request, f'{entity.replace("_", " ")} {action.replace("_", " ")}', size, origin,
               frames=frames, fps=fps, loop=loop, facing=direction, poses=poses,
               subject=DAVE if entity == 'dave' else ENTITIES[entity],
               kind='character', ticks=ticks, timing=timing, priority=priority, extra=extra,
               states=[action], depends=['established ' + entity + ' base appearance'],
               checks=['Inspect all frames over the same body/ground overlay; no head-size or anatomy drift.',
                       'Weapon hand, garment layers, palette and upper-left highlights remain fixed.',
                       'Read the silhouette at native size on pale sand and dark ruins.',
                       'Check chronological pose order, contact/release frames and last-to-first transition if looping.',
                       'No weapon, cape, ear or effect clipped at a canvas edge.'])


def material(aid, milestone, request, description, *, face=False, variants=None):
    return add(aid, milestone, request, 'Seamless terrain material', (256, 64) if face else (256, 256), (0, 0),
               kind='material', subject=description, variants=variants,
               extra=('Repeat horizontally only; preserve continuous top and bottom strata.' if face else 'Repeat on all four edges; no visible central landmark, border or lighting vignette.') +
                     ' This is a material texture, not a 47-tile autotile sheet. Engineering creates the blends.',
               checks=['Check exact final dimensions and alpha 255 everywhere.',
                       'Inspect a 3x3 repeat and a half-width/half-height offset for seams; repair visible breaks before acceptance.',
                       'Compare grain and motif scale against the 64-pixel template tiles.',
                       'Test blending with adjacent terrain in a room preview; do not claim seamlessness from a prompt alone.'])


def fx(aid, milestone, request, size, frames, description, *, origin=None, fps=24, loop='once',
       facing='none', poses='', extra='', timing='art recommendation where request does not specify fps', priority='P0'):
    return add(aid, milestone, request, description, size, origin or (size[0]//2, size[1]//2),
               frames=frames, fps=fps, loop=loop, facing=facing, poses=poses, subject=description,
               extra=extra, timing=timing, priority=priority,
               checks=['Effect centre/pivot stays fixed and fits every frame.',
                       'Readable silhouette at 1280x720 on both terrain extremes.',
                       'No opaque rectangle, stray alpha or dark premultiplied fringe.',
                       'No full-screen strobe; loop luminance and seam inspected if looping.',
                       'Any ground ring is an elevated-view ellipse, not a face-on circle.'])


# Milestone A: exact requested IDs, not template resource replacements.
for direction in ['down', 'down_side', 'side', 'up_side', 'up']:
    character('dave', 'idle', direction, 'A', 'A1', 8, 10,
              'f0 neutral baseline; f1-3 inhale and cape/hair trail by at most 1-2 native pixels; f4 breath crest; f5-7 settle. No foot lifting. Last-to-first continues the motion without a duplicate terminal frame.',
              loop='loop', size=(96, 96), origin=(48, 88), timing='contract')
    character('dave', 'walk', direction, 'A', 'A2', 10, 20,
              'f0 passing into first stride; f1 approach; f2 first foot CONTACT; f3 load; f4 push; f5 opposite passing; f6 approach; f7 opposite foot CONTACT; f8 load; f9 push returning to f0. Ground anchor fixed, body bob <=2 native pixels; cape and hair lag the torso by one pose.',
              loop='loop', size=(96, 96), origin=(48, 88), timing='contract',
              extra='Contacts are zero-based frame indices 2 and 7. Keep both soles aligned to the ground plane; do not duplicate f0 as an extra end frame.')
    character('dave', 'attack', direction, 'A', 'A3', 8, None,
              'ANTICIPATION f0 planted stance, f1 right-hand windup; ACTIVE f2 begin right-to-left sweep, f3 CONTACT/strongest cut, f4 follow-through; RECOVERY f5 decelerate, f6 lower blade, f7 return toward neutral. Only f2-4 are active.',
              size=(128, 128), origin=(64, 112), ticks=[3, 3, 3, 3, 3, 4, 4, 4], timing='contract: 27 game ticks at 60 Hz, 450 ms',
              extra='Body is the same 76-80 pixels tall as locomotion, simply repositioned for the new origin. Do not bake a slash arc into the character frames. Weapon follows an anatomically continuous path with the right hand closed around the grip.')
left_walk=character('dave','walk','left','A','User continuation 2026-10-31; A2 native specification',10,20,
    'f0 passing; f1 first leg swing; f2 first CONTACT; f3 load; f4 push; f5 opposite passing; f6 opposite swing; f7 opposite CONTACT; f8 load; f9 push into f0. Walk west in place; no duplicate terminal frame.',
    loop='loop',size=(96,96),origin=(48,88),timing='contract walk count/rate; independent left authoring explicitly requested by user',
    extra='Attach art/source/dave/cardinal_batch_v001/dave_base_left_source_v001.png as the facing model. Far anatomical right hand holds sword; near left hand is empty. No full-sprite mirror. Contacts f2/f7.')
left_attack=character('dave','attack','left','A','User continuation 2026-10-31; A3 native specification',8,None,
    'ANTICIPATION f0-1; ACTIVE f2-4 with CONTACT f3 toward west; RECOVERY f5-7. Keep the far right-shoulder/elbow/wrist/grip chain; near left hand remains empty.',
    ticks=[3,3,3,3,3,4,4,4],timing='contract:27 game ticks at60Hz,450ms',
    extra='Attach the established authored-left base. Upper-left light stays fixed. Do not mirror the right attack; use the anatomical right arm. Slash FX separate.')
for authored_left in [left_walk,left_attack]:
    authored_left['id_status']='new stable authored-left ID under explicit user request; Claude resource registration pending'

fx('spr_fx_slash', 'A', 'A4', (128, 96), 4, 'A white-gold sword crescent growing from its pivot and sweeping toward east', origin=(16, 48), fps=20,
   facing='east', poses='f0 thin leading edge; f1 broad CONTACT crescent; f2 taper and split tail; f3 residual taper, mostly transparent.', timing='contract: 20 fps once; runtime gate conflict recorded in visual guide',
   extra='Only the arc, no sword or character. The pivot is at (16,48), positive x to the right. The engine rotates it toward the mouse and shows it only while the attack is active. Source duration 200 ms conflicts with 150 ms active window; do not silently retime it.')
material('tex_sand_light', 'A', 'A5', 'Pale warm beige desert sand with low-contrast fine grain, broad sparse shallow ripple clusters and restrained upper-left relief. Keep dark contours off flat terrain.',
         variants=[('ripples', 'Sparse broad wind ripples, no pebble objects.'), ('pebbles', 'Sparse tiny embedded ochre and cool-grey pebbles, below object-art contrast.'), ('cracks', 'Very sparse shallow hairline dry cracks, low contrast, no giant mud plates.')])
material('tex_sand_dark', 'A', 'A5', 'Muted medium warm ochre sand, same grain scale as tex_sand_light, gently compacted path material. No painted path edges or dark outline; engineering blends its irregular margins.')
material('tex_rock_top', 'A', 'A5', 'Desert canyon top rock: muted ochre-grey broad flat angular planes, occasional fine fissures. Match the template stone density and upper-left highlights without strong continuous diagonal stripes.')
material('tex_cliff_face', 'A', 'A5', 'Vertical front face of desert canyon rock with horizontal strata, broad ochre-brown slab faces, dark lower-right recesses and restrained top-left ledge light. No top cap, freestanding rock or horizon.', face=True)
character('undead', 'idle', 'down', 'A', 'A6', 6, 10, 'f0 baseline; f1-2 shoulders rise; f3 crest; f4-5 settle, grounded feet. A slow dry breathing sway.', loop='loop', timing='6 frames from A6; 10 fps from contract idle default')
for direction in ['down', 'side', 'up']:
    character('undead', 'walk', direction, 'A', 'A6', 8, 12, 'f0 drag; f1 approach; f2 first CONTACT; f3 load; f4 drag opposite; f5 approach; f6 opposite CONTACT; f7 load. Slow uneven gait without changing leg length.', loop='loop', timing='8 frames from A6; 12 fps and contacts f2/f6 are art recommendations (not Dave step indices)')
    character('undead', 'attack', direction, 'A', 'A6', 8, None, 'ANTICIPATION f0-3 shoulders rise and reaching arm pulls back; ACTIVE f4 reach begins, f5 CONTACT swipe; RECOVERY f6 decelerate, f7 return. Keep the planted foot anchor.',
              ticks=[6, 6, 6, 6, 4, 4, 7, 7], timing='frame ranges from A6; durations proposed for Claude enemy data')
character('undead', 'hurt', 'down', 'A', 'A6', 2, 12, 'f0 impact recoil with body compression; f1 guarded settle. No full-canvas white flash.', timing='contract default hurt playback')
character('undead', 'defeat', 'front', 'A', 'A6', 8, 12, 'f0 losing balance; f1-2 knees buckle; f3 ground CONTACT; f4-6 cloth and limbs settle; f7 still remains. No gore or full-screen flash.', loop='once_hold', timing='8 frames from A6; 12 fps chosen within contract range')
character('undead', 'rise', 'front', 'A', 'A6', 10, 12, 'f0 concealed below sand; f1-2 cloth and hand protrude; f3-5 shoulders and skull lift; f6-7 knees plant; f8 weight transfer; f9 baseline standing silhouette. Keep the same ground point.', timing='10 frames from A6; 12 fps proposed', extra='Only the undead body and attached loose sand; separate summoning cracks and sand-burst FX are supplied for the boss milestone.')
add('spr_chest_desert', 'A', 'A7', 'Treasure chest states', (64, 64), (32, 56), frames=6, fps=None, loop='state_driven',
    states=['closed: f0', 'opening: f1-4', 'open: f5'], footprint=(48, 20),
    subject='A squat desert treasure chest, warm weathered golden-brown planks, cool iron edge bands and a simple centred latch. Visible lid top and front in the template elevated camera, no elaborate emblem.',
    poses='f0 closed; f1 latch releases and lid cracks; f2 half open; f3 approaching full lift; f4 opening settles; f5 fully open and held. Base and hinge remain registered.',
    timing='states and counts from A7; opening proposed at 12 fps for four frames',
    checks=['All six frames use the same base and hinge location.', 'Footprint 48x20 is centred on (32,56).', 'Open lid fits inside 64x64 without shrinking the chest.', 'Closed/open are holds; opening is a four-frame one-shot.'])
fx('spr_checkpoint_star', 'A', 'A8', (64, 64), 8, 'A warm yellow five-point checkpoint star, small amber outline and gentle gold inner glow, hovering over its fixed anchor',
   origin=(32, 48), fps=10, loop='loop', poses='f0 low glow; f1-3 rise gently; f4 glow crest; f5-7 return. Star shape and location remain stable; pulse luminance gently, no flashing.', timing='contract',
   extra='The bottom hover anchor is (32,48). Glow must stay within bounds. Star core is opaque, outer glow can use graded alpha. No baked ground shadow, save text or pedestal.')
fx('spr_fx_sparkle', 'A', 'A8', (16, 16), 6, 'A tiny pale-gold four-point star glint', fps=24, poses='f0 point; f1-2 expand; f3 crest; f4 taper; f5 fade fully transparent.')

ICON_DESCRIPTIONS = {
    'potion_health': 'One squat clear glass flask, red healing liquid, cork stopper, simple brass neck band. No label or cross; broad soft shading, not faceted 3D.',
    'longsword': 'One straight silver longsword with a brass crossguard and brown grip, identical to Dave\'s base sword.',
    'bandit_scimitar': 'One worn curved iron scimitar with a brown grip and simple brass guard, matching the bandit weapon.',
    'sunsteel_blade': 'One straight sunsteel sword, warm pale gold blade with a small bright upper-left highlight, simple sun-shaped brass guard; no magical text.',
    'worn_tabard': 'One worn ivory tabard with muted brown edging, readable frayed hem and simple belt; clothing icon, no body.',
    'iron_tunic': 'One compact cool iron plated tunic with brown underlayer, clear shoulder openings and waist, no body.',
    'paladin_mail': 'One shining silver paladin mail cuirass with ivory layered cloth and restrained brass clasps, matching Dave, no head or body.',
    'wanderer_tunic': 'One muted ochre and brown desert travel tunic with a simple sash and hood folded at neck, no body.',
    'gold_coins': 'A small readable stack of three warm gold coins with plain stamped rims, no lettering.',
    'desert_rose': 'One desert rose mineral cluster, dusty rose and pale ochre gypsum petals, readable angular rosette.',
    'golden_scarab': 'One gold scarab amulet with a small muted lapis wing inset, clear beetle silhouette, no lettering.',
    'ancient_coin': 'One worn antique gold coin with a simple abstract radial stamp, no readable letters or numbers.',
    'pharaoh_ankh': 'One gold ankh with a small lapis inset and broad readable loop, matching the Pharaoh regalia. Boss reward, not a Grail.',
    'potion_greater': 'One larger double-shouldered glass flask with rich red healing liquid, brass neck band and cork. Distinguish by silhouette from potion_health, not by text.',
}
for item, description in ICON_DESCRIPTIONS.items():
    add('spr_icon_' + item, 'A' if item == 'potion_health' else 'B', 'A9' if item == 'potion_health' else 'B9',
        'Inventory item icon: ' + item, (64, 64), (0, 0), subject=description,
        kind='icon', priority='P0' if item == 'potion_health' else 'P1', states=['static'],
        checks=['At least 3 pixels of fully transparent padding on every side.', 'Centred visual mass; readable at 48x48.', 'No title, frame, cast shadow or white matte.', 'Weapon/costume silhouette matches its character reference.'],
        extra='Single inventory item, readable at 48 pixels, full silhouette contained inside x=3..60 and y=3..60. Natural glass translucency is allowed, but no opaque rectangle.')

for aid, size, desc in [
    ('spr_ui_hp_frame', (320, 32), 'Reuse the supplied UI health frame: dark ink well with cool grey rim, 8px cap/border scaling convention. It is an empty bar backing, with no baked text or health fill.'),
    ('spr_ui_hp_fill', (320, 32), 'Reuse the supplied full-size red health fill, no border, text, skull or heart. Source 320x32, same full dimensions as the frame; engine clips it to the destination track. Do not add a new 4px source inset.'),
    ('spr_ui_slot', (72, 72), 'Reuse the supplied empty square inventory slot, dark ink centre and cool grey rim. No icon, key glyph, equipment badge or text.'),
    ('spr_ui_slot_selected', (72, 72), 'Reuse the supplied selected-slot OVERLAY: transparent centre, gold outline, corners and selected marker aligned exactly to the base 72x72 slot. No icon or text.'),
    ('spr_ui_panel', (96, 96), 'Reuse the supplied nine-slice UI panel: calm dark ink centre, cool grey border. Exact 24px borders on all sides, stretchable 48x48 centre without motifs. No baked text.'),
]:
    add(aid, 'A', 'A10', 'Core HUD kit', size, (0, 0), kind='ui', states=['static'], subject=desc,
        checks=['Read at native 1280x720 GUI scale.', 'Bar fill and frame align pixel for pixel.', 'Selection reads through shape and value.', 'Panel corners survive nine-slice stretch tests at 320x160 and 760x300.'],
        extra='Screen-space UI, not a top-down world object. No baked letters, numbers, labels or item art; preserve border sizes exactly.')

# Milestone B: family-sized batches. Every action and facing gets its own prompt.
for direction in ['down', 'down_side', 'side', 'up_side', 'up']:
    character('dave', 'hurt', direction, 'B', 'B1', 3, 12, 'f0 impact compression; f1 short recoil, sword safely held; f2 guarded recovery toward idle. Feet remain on the fixed ground plane.', size=(96, 96), origin=(48, 88), timing='contract')
character('dave', 'death', 'front', 'B', 'B1', 10, 12, 'f0 struck; f1-2 losing balance; f3-4 knees buckle; f5 ground CONTACT; f6-8 cape/hair settle; f9 motionless, sword still identifiable on right side. Respectful, no gore.', loop='once_hold', size=(128, 96), origin=(64, 88), timing='10 frames from B1; 12 fps within contract range')
character('dave', 'potion', 'front', 'B', 'B1', 8, 16, 'f0 ready; f1-2 left hand raises red potion; f3-4 bottle reaches mouth and drinks; f5 lowers; f6 bottle returns; f7 returns neutral. Sword remains in right hand and points safely away.', size=(96, 96), origin=(48, 88), timing='contract')
for entity, request in [('skeleton_warrior', 'B2'), ('skeleton_archer', 'B3'), ('bandit', 'B4'), ('bandit_caster', 'B5')]:
    character(entity, 'idle', 'down', 'B', request, 6, 10, 'Six-pose subtle breathing or dry sway with grounded feet; f0 neutral, f3 crest, f5 settling into f0.', loop='loop', timing='A6 family coverage; B3/B5 support-state coverage proposed')
    for direction in ['down', 'side', 'up']:
        character(entity, 'walk', direction, 'B', request, 8, 16, 'f0 passing; f1 approach; f2 first CONTACT; f3 push; f4 passing opposite; f5 approach; f6 opposite CONTACT; f7 push into f0. Preserve weapon silhouette and head scale.', loop='loop', timing='8 frames from A6 family coverage; 16 fps and contacts f2/f6 proposed')
        if entity == 'skeleton_warrior':
            poses='ANTICIPATION f0-2 right-hand sword draw back; ACTIVE f3 begin strike, f4 CONTACT; RECOVERY f5-7 settle. Shield stays on left arm.'; ticks=[5,5,5,4,4,5,5,5]
        elif entity == 'bandit':
            poses='ANTICIPATION f0-1 crouch and right-hand scimitar windup; ACTIVE f2 launch cut, f3 CONTACT, f4 follow-through; RECOVERY f5-7 regain balance.'; ticks=[4,4,3,3,3,4,4,4]
        elif entity == 'skeleton_archer':
            poses='ANTICIPATION f0 reach to quiver, f1 nock, f2-4 draw bow; RELEASE f5 arrow leaves string at bow-hand nock line; RECOVERY f6-7 relax and reset. Never draw the bow in the wrong hand.'; ticks=[5,5,5,5,5,3,5,5]
        else:
            poses='ANTICIPATION f0-2 raise staff, f3-4 charge held tip; RELEASE f5 cast orb from staff tip; RECOVERY f6-7 lower staff. No orb baked into body frames.'; ticks=[5,5,5,5,5,3,5,5]
        a=character(entity, 'cast' if entity == 'bandit_caster' else 'attack', direction, 'B', request, 8, None, poses, ticks=ticks,
                    timing='active/release indices from requests; tick durations proposed for Claude data')
        if entity in ['skeleton_archer', 'bandit_caster']:
            a['release_frame']=5
            a['release_offset_px']=None
            a['additional_instructions'] += ' Measure a release offset from the fixed origin at frame 5 after export; record signed dx,dy in the sidecar. Do not guess coordinates from source resolution.'
            a['additional_instructions'] += ' The flying projectile is a separate sprite: do not bake projectile travel into the body frames. An arrow may be nocked before release; frame 5 shows the cleared string after release.' if entity=='skeleton_archer' else ' Keep the launched orb separate from the staff/body frames.'
    character(entity, 'hurt', 'down', 'B', request, 2, 12, 'f0 short impact recoil; f1 guarded recovery; weapon remains held.', timing='A6 family coverage; B3/B5 support states proposed')
    character(entity, 'defeat', 'front', 'B', request, 8, 12, 'f0 losing balance; f1-2 fold; f3 ground CONTACT; f4-6 cloth/bones settle; f7 still final remains. No gore.', loop='once_hold', timing='A6 family coverage; B3/B5 support states proposed')
fx('spr_arrow', 'B', 'B3', (32, 8), 1, 'One wooden arrow with dark shaft, small ivory-grey iron head and ochre fletching, pointing east', origin=(16,4), fps=None, loop='static', facing='east')
fx('spr_fx_arrow_hit', 'B', 'B3', (48,48), 6, 'A small pale sand/stone impact chip burst, readable and restrained', poses='f0 point; f1-2 contact burst; f3-4 outward chips; f5 fade.')
fx('spr_magic_orb', 'B', 'B5', (32,32), 4, 'A compact amber-white magic core with muted turquoise edge and a charcoal-readable perimeter', loop='loop', poses='Four gentle internal swirl phases, stable outer silhouette and luminance, last phase connects to first.')
fx('spr_fx_magic_launch', 'B', 'B5', (64,64), 6, 'A small turquoise-gold staff-tip launch flare with a short forward wisp', poses='f0 pinprick; f1-2 crest; f3-4 taper; f5 transparent.')
fx('spr_fx_magic_hit', 'B', 'B5', (64,64), 8, 'A turquoise-gold orb impact with a small radial ring and fragments', poses='f0 contact; f1-2 expansion; f3-5 scattered motes; f6-7 fade.')
character('bat', 'fly', 'front', 'B', 'B6', 6, 15, 'f0 wings raised; f1 downstroke; f2 lowest stroke; f3 folding recovery; f4 rising; f5 near raised, then f0. Body centre stays fixed, wing joints move naturally.', loop='loop', size=(64,64), origin=(32,32), timing='contract', extra='Existing spr_bat_fly is 200x200. This is the requested replacement delivery size, not authorization to overwrite that engine resource.')
character('bat', 'dive', 'front', 'B', 'B6', 4, 20, 'f0 tuck anticipation; f1 forward dive; f2 closest CONTACT silhouette; f3 spread wings for recovery. Runtime translation moves the bat; do not bake travel into the canvas.', size=(64,64), origin=(32,32), timing='4 frames from B6; 20 fps proposed')
character('bat', 'defeat', 'front', 'B', 'B6', 6, 12, 'f0 recoil; f1-2 wings fold; f3 downward curl; f4 settle; f5 still. Centre anchor maintained, engine handles falling movement.', loop='once_hold', size=(64,64), origin=(32,32), timing='6 frames from B6; 12 fps proposed')
for direction in ['down','side','up']:
    character('python','slither',direction,'B','B7',8,12,'Eight continuous S-curve phases propagating from neck to tail, f0 and f4 opposing bends; fixed head scale, body length and patch sequence. Last phase flows into first.',loop='loop',size=(128,96),origin=(64,72),timing='contract',priority='P1')
    character('python','lunge',direction,'B','B7',4,None,'ANTICIPATION f0 held coil; ACTIVE f1 neck extends, f2 CONTACT jaws forward; RECOVERY f3 recoil. Entire body stays inside the fixed canvas; runtime controls world movement.',size=(128,96),origin=(64,72),ticks=[4,3,3,6],timing='4 frames from B7; active f1-2 and durations proposed',priority='P1')
for action,frames,fps,poses,loop in [
    ('coil',6,12,'f0 low coil; f1-3 tighten readable concentric body; f4 head rises; f5 held pre-lunge warning. Maintain single continuous body.','once_hold'),
    ('hurt',2,12,'f0 impact bend; f1 coil recovery. No body severing.','once'),
    ('defeat',8,12,'f0 recoil; f1-3 body relaxes; f4 ground CONTACT; f5-6 settles; f7 still, intact serpent.','once_hold')]:
    character('python',action,'front','B','B7',frames,fps,poses,loop=loop,size=(128,96),origin=(64,72),timing='counts from B7; fps and front-only shared states proposed',priority='P1')
for action,frames,fps,loop,poses in [
    ('mound',6,10,'loop','f0 small raised sand mound; f1-2 rise and creep; f3 crest; f4-5 settle, visible warning immediately, no mouth yet.'),
    ('emerge',8,16,'once','f0 mound; f1-2 crown breaks through; f3-5 body rises; f6-7 settle into emerged silhouette.'),
    ('idle_up',6,10,'loop','Six slow front-facing upright sways, mouth and segment count fixed; suffix up means upright emerged pose, not a back-facing view.'),
    ('attack',8,None,'once','ANTICIPATION f0-3 rear and mouth opens; ACTIVE f4 bite begins, f5 CONTACT; RECOVERY f6-7 pull back.'),
    ('burrow',8,16,'once','f0 upright; f1-3 lower; f4-6 sinks; f7 mound-only handoff. Do not just reverse emerge if sand gravity would look wrong.'),
    ('hurt',2,12,'once','f0 segment recoil; f1 recover, mouth landmark unchanged.'),
    ('defeat',10,12,'once_hold','f0 recoil; f1-4 collapse; f5 ground CONTACT; f6-8 dust and segments settle; f9 still collapsed remains.')]:
    a=character('sandworm',action,'front','B','B8',frames,fps,poses,loop=loop,size=(192,192),origin=(96,176),ticks=[6,6,6,6,4,4,6,6] if action=='attack' else None,timing='counts and active f4-5 from B8; playback durations proposed',priority='P1')
    if action=='mound': a['additional_instructions']+=' This is the attack warning; make it recognizable within the first 250 ms without relying on a late bright flash.'
for aid,size,frames,desc,origin,loop in [
    ('spr_fx_hit',(64,64),6,'A restrained warm ivory contact spark with small ochre chips',(32,32),'once'),
    ('spr_fx_dust',(48,32),6,'A low pale ochre footstep dust puff lying on the ground plane',(24,24),'once'),
    ('spr_fx_poof',(96,96),8,'A compact muted sand-coloured disappearing puff with curling lobes',(48,72),'once'),
    ('spr_fx_heal_ring',(128,64),8,'A RED healing ground ellipse with warm red edge and clear transparent centre',(64,32),'once'),
    ('spr_fx_heal_particle',(16,16),6,'One small RED healing mote, soft red core and tapered upward glint',(8,8),'once'),
    ('spr_fx_levelup',(128,128),8,'A warm gold rising level-up halo and sparse gold motes, no text',(64,112),'once')]:
    fx(aid,'B','B10',size,frames,desc,origin=origin,loop=loop,priority='P1',poses='f0 onset; f1-2 expand; f3 crest; remaining frames taper and fade; last frame transparent.',extra='Colour remains red for healing; no green healing aura. Origins and level-up canvas not specified in B10 are proposed for integration.')

# Milestone C: ground and modular pieces.
for aid,description,face in [
    ('tex_grass','Sparse oasis grass, muted olive green short blades, small clusters, no black outlines around individual blades.',False),
    ('tex_water','Calm oasis water, muted turquoise, low-contrast broad ripples, no shoreline or floating objects. Four subtle phase variants, stable mean brightness.',False),
    ('tex_wet_sand','Darkened damp warm ochre sand, same grain scale as the light desert sand, no shore edge.',False),
    ('tex_paving','Worn pale warm stone paving blocks with modest irregular seams; no strong grid outlines.',False),
    ('tex_masonry_top','Warm grey-ochre ruined masonry top surface, broad worn block planes and shallow chips.',False),
    ('tex_masonry_face','Front face of ruined desert stone masonry, weathered ochre-grey bricks, continuous horizontal courses, upper-left relief.',True),
    ('tex_chasm_wall','Dark ochre-grey chasm inner wall, receding stone layers, dark recesses, no visible sky or props.',True),
    ('tex_chasm_void','A nearly black warm charcoal chasm floor/void with extremely subtle even texture, no stars, gradient or highlight.',False)]:
    a=material(aid,'C','C1',description,face=face)
    if aid=='tex_water':
        a['animation'].update(frame_count=4,fps=6,loop='loop',timing_status='optional 4 frames from C1; 6 fps proposed')
        a['animation']['pose_plan']='Four gentle ripple phases; no camera movement, stable shoreline-free material, spatial tiling on every frame and temporal f3-to-f0 seam required.'
add('ts_stairs','C','C2','Six-cell wide stairs source sheet',(192,128),(0,0),kind='modular',states=['left_top','mid_top','right_top','left_bottom','mid_bottom','right_bottom'],
    subject='Wide worn pale ochre stone stairs, elevated adventure view, three 64px cells wide and two cells tall. Broad risers with top-left highlights and darker front faces, no rails.',
    extra='EXACT SOURCE GRID: row 0 left_top, mid_top, right_top; row 1 left_bottom, mid_bottom, right_bottom. Middle column must repeat horizontally without discontinuity. No padding between source cells. All six source cells contain artwork; engine needs a separately reserved empty tile index 0, not deletion of left_top.',
    checks=['Verify 192x128, six exact 64px cells, no grid lines in artwork.', 'Join left + three mid + right columns and inspect riser continuity.', 'Ground entrances clear, step height and highlights match.', 'Confirm engine repacking reserves empty tile zero without losing a stair cell.'])
add('ts_bridge','C','C3','Bridge modular source sheet',(448,128),(0,0),kind='modular',naming='contract ID; proposed exact atlas layout',states=['E-W rope top/bottom/both/none','N-S rope left/right/both/none','broken E-W x2','post x2'],
    subject='Weathered warm wooden desert footbridges with muted brown ropes, broad readable planks and upper-left highlights. Elevated adventure camera. Fully transparent gaps between pieces.',
    extra='Proposed 7-column by 2-row 64px grid, row-major cells 0..13: 0 transparent; 1 E-W top rope; 2 E-W bottom rope; 3 E-W both; 4 E-W no rope; 5 N-S left rope; 6 N-S right rope; 7 N-S both; 8 N-S none; 9 broken E-W left end; 10 broken E-W right end; 11 left post 32x64 centred in cell; 12 right post 32x64 centred in cell; 13 transparent. E-W planks join on left/right, N-S on top/bottom. Side ropes never block entrances. Final atlas dimensions/layout are proposed because C3 gives no total canvas.',
    checks=['Verify each cell boundary and transparent reserved cells.', 'Test three-cell E-W and N-S runs for plank, rope and light continuity.', 'Broken ends expose a clear nonwalkable gap.', 'Post artworks are exactly 32x64 inside their 64x64 cells; no adjacent-cell bleed.'])
PROP_SPECS = [
    ('cactus_tall',(64,128),(32,120),(24,16),'A tall muted sage saguaro cactus, one upright trunk and two asymmetrical arms, sparse readable spines, broad light/shadow planes.'),
    ('cactus_small',(48,64),(24,56),(20,12),'A short rounded sage-green barrel cactus with a small arm and sparse spines.'),
    ('rock_small_01',(48,40),(24,34),(32,14),'A low angular warm grey-ochre rock with one broad top plane.'),
    ('rock_small_02',(48,40),(24,34),(30,14),'A low paired ochre rock cluster with two simple unequal masses.'),
    ('rock_small_03',(48,40),(24,34),(32,14),'A flat split grey-ochre desert rock, shallow readable fissure.'),
    ('boulder_01',(128,112),(64,100),(96,40),'A large broad warm ochre-grey boulder, visible upper planes and darker right face.'),
    ('boulder_02',(128,112),(64,100),(96,40),'A large broken ochre-grey boulder with an angled top and shallow notch, distinct from boulder_01.'),
    ('tree_desert',(160,160),(80,150),(24,14),'A sparse desert acacia, warm grey-brown twisting trunk, low muted olive umbrella canopy with gaps.'),
    ('tree_dead',(128,160),(64,150),(24,14),'A bare dead desert tree with grey-brown twisted trunk and sparse readable forked branches, no leaves.'),
    ('palm_01',(128,192),(64,182),(24,14),'A slightly leaning date palm, warm segmented brown trunk and broad sage-olive fronds, no tiny leaf noise.'),
    ('palm_02',(128,192),(64,182),(24,14),'A straight-trunk date palm with a distinct asymmetrical crown of broad olive fronds, same species as palm_01.'),
    ('bush',(64,48),(32,42),None,'A low oasis shrub with muted olive-green rounded clumps and a few clear leaves.'),
    ('bush_dead',(64,48),(32,42),None,'A low dry grey-ochre twig bush, readable airy clumps and broken branches.'),
    ('pebbles_01',(64,64),(32,32),None,'A flat sparse scatter of three tiny ochre pebbles, low contrast on sand.'),
    ('pebbles_02',(64,64),(32,32),None,'A flat sparse scatter of five small cool-grey pebbles, different spacing from pebbles_01.'),
    ('pebbles_03',(64,64),(32,32),None,'A flat sparse scatter of two ochre chips and one grey pebble.'),
    ('skull_01',(32,32),(16,24),None,'One small weathered ivory human skull, front three-quarter top-down, dark sockets, no gore.'),
    ('skull_02',(32,32),(16,24),None,'One small weathered ivory human skull lying on its side, different orientation, no gore.'),
    ('ruin_block_01',(64,64),(32,56),(48,24),'One worn pale ochre stone ruin brick with a visible top plane, chipped corners and simple mortar stain.'),
    ('ruin_block_02',(128,64),(64,56),(96,24),'Two joined worn pale ochre ruin blocks with a broken edge, low and broad.'),
    ('ruin_block_03',(64,96),(32,86),(48,24),'A short vertical two-brick broken ruin stack, visible top surface, chipped stone.'),
    ('wagon_wreck',(192,128),(96,116),(160,40),'A broken desert wooden wagon with one collapsed wheel, warm brown planks and dull iron fittings, no occupant.'),
    ('obelisk',(96,224),(48,214),(48,24),'A tall weathered pale ochre stone obelisk, simple unreadable shallow carved bands and chipped tip, no text.'),
    ('pharaoh_statue',(128,256),(64,244),(72,32),'A worn desert stone statue of the Undead Pharaoh regalia, lapis/gold shapes translated into carved pale ochre stone. No living body or recovered Grail.'),
    ('tumbleweed',(48,48),(24,24),None,'One airy near-spherical dry ochre tumbleweed, interwoven broad twig clusters, transparent gaps, weak ambient shading so rotation does not rotate a strong highlight. No baked shadow.'),
]
for key,size,origin,fp,desc in PROP_SPECS:
    add('spr_'+key,'C','C4','Desert prop: '+key,size,origin,kind='prop',subject=desc,footprint=fp,
        naming='proposed sprite ID for contract prop key '+key,priority='P1' if key in ['wagon_wreck','obelisk','pharaoh_statue'] else 'P0',states=['static'],
        extra='The requested prop key maps to this proposed sprite ID; engineering confirms registration. All C4 origins and footprints except explicitly requested sizes/footprints are proposed. ' +
              ('Flat decal with no collision; centre alignment is intentional.' if key.startswith('pebbles') or key.startswith('skull') else 'No baked ground shadow. ') +
              ('One static frame only, centred pivot; engine rotates it and handles travel, no baked spinning sheet.' if key=='tumbleweed' else ''),
        checks=['Match silhouette and colour at native scale on sand and ruins.', 'Verify base/trunk anchor and proposed footprint overlay.', 'No background, shadow rectangle or clipped branches.', 'Distinct variants keep material palette and light direction consistent.'])
fx('spr_healing_spring','C','C6',(128,96),4,'A small low oasis healing spring with pale stone rim, muted turquoise ripples and a subtle RED healing glimmer',origin=(64,80),fps=8,loop='loop',priority='P2',poses='Four quiet ripple phases, stable rim, no large luminance pulse.',extra='128x96 and four loop frames from C6; origin and fps proposed. Do not turn general oasis water red.')

# Milestone D UI art (normal, hover, pressed are engine-selected states).
for aid,size,desc in [
    ('spr_ui_save_card',(760,120),'Reuse the supplied occupied-save card prototype: dark ink centre, restrained cool grey rim, empty reserved thumb area on the left and clear editable text area on right. No baked screenshot, text or numbers.'),
    ('spr_ui_save_card_empty',(760,120),'Reuse the supplied empty-save card matching spr_ui_save_card exactly, quieter cool grey border and empty central text area; no text or icon.'),
    ('spr_ui_button',(64,64),'Reuse the supplied nine-slice button prototype: dark ink centre, cool grey rim with exact 16px borders; no text or icon.')]:
    add(aid,'D','D1','Save/load/menu UI',(size),(0,0),kind='ui',frames=3,loop='state_driven',priority='P1',states=['normal f0','hover f1','pressed f2'],
        subject=desc,poses='f0 normal; f1 clear warm gold hover rim; f2 darker inset centre and 1px depressed bevel, same outer dimensions.',
        extra='Screen-space GUI. Three discrete states, not an automatically playing animation. Match the existing UI handoff palette and preserve gold hover/focus and pressed inset states.',
        checks=['All states register at the same corners.', 'Button 16px nine-slice borders survive stretching.', 'No baked text; keep text areas calm and clear.'])

# Milestone E follows the original brief and the narrative art handoff.
add('spr_intro_wall','E','E2 + narrative art requests','Breached Holy City wall',(1920,640),(0,0),kind='scene',subject='A wide breached pale stone Holy City defensive wall, broad fractured blocks, warm sand dust, approx 400px breach spanning local x=760..1160, ruined banner attachment, same illustrated masonry as desert ruins, upper-left light. No characters, text, visible Grail or living person.',
    extra='Transparent sky/breach areas where appropriate for layered compositing. Stage top-left (0,0), noncolliding backdrop for the 1920x1080 intro stage; Dave is staged separately at ground (1040,790). Maintain elevated adventure camera and native-scale pans.',checks=['Verify 1920x640 and breach x=760..1160.', 'Test 1280x720 camera crops and parallax seams.', 'No invented story details or recovered Grail.'])
sky=add('spr_intro_sky','E','Narrative art requests','Dusty intro atmosphere',(1280,720),(0,0),kind='scene',priority='P1',subject='One restrained dusty warm sky/atmosphere backdrop behind the breached Holy City wall, no new landmark with story significance, no living figure, Grail, text or horizon incompatible with the established view.',extra='Opaque full backdrop; optional slow parallax only. Base renderer may use a flat muted backdrop instead.',checks=['Exact 1280x720 with alpha 255 everywhere.','Backdrop stays quiet behind wall and live text.'])
sky['transparency']='opaque 8-bit RGBA, alpha 255 throughout, sRGB'
for i,size in enumerate([(64,64),(96,96),(128,96),(160,128)],1):
    add(f'spr_intro_rubble_{i:02d}','E','E3 + narrative art requests','Aftermath rubble',size,(size[0]//2,size[1]-8),kind='prop',subject=f'One distinct cluster of fractured pale Holy City stone blocks, variant {i}, ochre dust, no bodies or gore.',checks=['Same wall material and light as intro_wall.','Base remains registered and all fragments fit.'])
for i in range(1,4):
    add(f'spr_intro_fallen_{i:02d}','E','E3 + narrative art requests','Respectful fallen defender',(128,64),(64,56),kind='prop',subject=f'One fallen armored Holy City defender, pose variant {i}, silver and muted ivory/brown clothing, face turned away, covered and respectful, no gore or exposed wounds. Identity is not Dave. No breathing, twitching, glow or ghost imagery.',checks=['Respectful anatomy and believable limb arrangement.','Distinct silhouette without confusing the body for Dave.'])
add('spr_intro_banner','E','Narrative art requests','Windblown torn city banner',(128,192),(64,176),kind='prop',frames=6,fps=8,loop='loop',subject='A torn muted crimson Holy City banner attached at the RIGHT, pulling WEST toward screen left, broad cloth folds, no readable heraldic text or new emblem.',poses='Six consistent cloth gust phases, right attachment fixed; screen-left hem billows and settles with a continuous f5-to-f0 seam.',extra='Cinematic decoration with no collision. Match wall palette and light. A static fallback is allowed if engineering supplies wind motion.',checks=['Fixed right attachment; wind always left.','128x192 every frame; no clipping of torn hem.','Inspect loop at 8fps.'])
add('spr_intro_spear','E','Narrative art requests','Broken spear aftermath prop',(128,64),(64,56),kind='prop',subject='One broken plain wooden spear with a dull iron head among small stone rubble, no body, gore, text or additional quest object.',checks=['Material and light match intro_wall.','All fragments fit; fixed base-centre origin.'])
character('dave','wind_idle','down','E','E4 + narrative art requests',12,12,'Dave is the sole standing survivor: sword lowered, head slightly bowed. Twelve subtle gust phases; body and boots stable; cape and long hair flow WEST, screen left, while clasps stay fixed. No sudden direction reversal.',loop='loop',size=(96,96),origin=(48,88),timing='contract')
character('dave','turn','front','E','E4 + narrative art requests',4,8,'f0 down; f1 slight down-right turn; f2 down_side; f3 side facing right. Feet pivot on same anchor, sword remains right-handed, head and shoulder turn precede cape.',size=(96,96),origin=(48,88),timing='narrative request: 4 poses at 8fps, 0.5 seconds')
character('dave','grief','down','E','Narrative art requests',1,None,'One still grief pose: head bowed, free left hand closed slowly at side, sword lowered in right hand. No stretching, crying exaggeration or cape attachment change.',loop='static',size=(96,96),origin=(48,88),timing='narrative request: one still pose',priority='P1')
character('dave','vow','down','E','Narrative art requests',1,None,'One still vow pose: head raised with steady resolve, free left hand rests at breastplate, sword remains lowered in right hand. Cape and hair still pull left.',loop='static',size=(96,96),origin=(48,88),timing='narrative request: one still pose',priority='P1')
for entity in ['dave','pharaoh']:
    moods=[('neutral',''),('solemn','_solemn'),('determined','_determined')] if entity=='dave' else [('menace',''),('rage','_rage')]
    for mood,suffix in moods:
        aid='spr_portrait_'+entity+suffix
        add(aid,'E','E5 + narrative art requests','Dialogue portrait',(512,512),(0,0),kind='portrait',priority='P0' if not suffix else ('P2' if entity=='pharaoh' else 'P1'),states=[mood],
            subject=(("Attach art/source/dave/dave_base_down_v002.png for Dave's identity: adult warm friendly resolute face, swept long golden-brown hair, shining cool silver rounded paladin shoulders, ivory layered tabard, brown undergarments and red cape held by two brass clasps. Translate the model into natural adult bust anatomy; do not copy chibi eye size or head-to-body ratio." if entity=='dave' else "Attach the established Pharaoh base model: regal emaciated adult mummy face, dark sockets with restrained amber light, ivory wraps, lapis-and-gold striped nemes, broad gold collar and ivory/lapis layered robes. Keep the identity and rod crown design coherent with the boss model.")+f' Mood: {mood}.'),
            extra='Deliberate hand-painted fantasy bust illustration, facing RIGHT toward dialogue text, three-quarter view, chest-up. Convincing adult skull, eye sockets, neck and shoulder anatomy; natural restrained eye size rather than enlarged sprite eyes. Preserve identity landmarks, hairline, costume, materials and upper-left light from the established game model. Brushwork and designed value masses, no plastic 3D, photoreal collage, warped jewelry, melted fingers or stock AI fantasy face. Transparent outside bust, shoulder edges contained with 16px safe padding; no baked frame or text. At 208x208 the face and gaze still read. Dave is warm, firm and battle-worn; solemn lowers the eyes, determined keeps a steady gaze. Pharaoh base is controlled menace, no Grail; optional rage is parked P2 and is not needed by the current script.',
            checks=['Natural adult cranial and neck anatomy, equal believable eyes and coherent gaze right.','Dave hairline, colour, clasps and armor match his model; Pharaoh regalia matches boss.','No asymmetrical melted collar, extra teeth, fingers or floating accessories.','Inspect at both 512 and GUI 208 pixels; mouth remains expressive and deliberate.'])

# Milestone F: boss and effects, one action per request.
for action,n,fps,loop,poses in [
    ('idle',8,10,'loop','Eight slow levitation poses, floating body shifts <=2px; fixed ground anchor and stable rod. No cape/hair swap.'),
    ('summon',10,12,'once','ANTICIPATION f0-3 raise free hand; f4-6 summon gesture crest; f7-9 lower hand and return. Summoning cracks are separate.'),
    ('laser_charge',8,12,'once','ANTICIPATION f0-2 raise laser rod; f3-5 lock aim; f6-7 hold charged pose. Keep rod crown measurable, no beam baked into body.'),
    ('laser_fire',4,12,'loop','Four restrained rod recoil/robe ripple poses around a stable firing stance. Laser beam separate; loop first/last body and rod pose carefully.'),
    ('thunder_cast',8,12,'once','ANTICIPATION f0-3 raise free arm and staff; f4 cast gesture crest; f5-7 recovery. Bolt and warning markers are separate.'),
    ('hurt',2,12,'once','f0 short torso recoil; f1 recover, crown/rod stable, no full-screen white flash.'),
    ('teleport_out',6,20,'once','f0 solid body; f1-2 edges disintegrate to warm sand; f3-4 thinning silhouette; f5 fully transparent. Ground anchor fixed.'),
    ('teleport_in',6,20,'once','f0 transparent; f1-2 sand assembles into silhouette; f3-4 robe and head form; f5 solid identity exactly matching idle.'),
    ('death',16,12,'once_hold','f0-2 stagger; f3-5 rod lowers and crown dims; f6-9 robes and body disintegrate into ochre sand from extremities inward; f10-13 dust settles; f14 near empty; f15 transparent. No Grail, full-screen flash or gore.')]:
    a=character('pharaoh',action,'front','F','F1',n,fps,poses,loop=loop,size=(192,192),origin=(96,176),timing='counts/loop from F1; fps chosen from contract default where applicable or proposed')
    if action in ['laser_charge','laser_fire']:
        a['rod_tip_offsets_px']=[None]*n
        a['additional_instructions']+=' After export measure the centre of the rod crown on EVERY frame and supply signed dx,dy from (96,176) in the sidecar. Laser fire tip tracking also proposed to prevent beam wobble. Null means unmeasured, never a zero offset.'
fx('spr_laser_beam','F','F2',(64,32),4,'A gold-white horizontal laser beam with amber edge, extending continuously left-to-right across the tile',fps=24,loop='loop',facing='east',poses='Four gentle internal energy phases; width and core brightness stable.',extra='Tile seamlessly along x on every frame. No end cap in repeating section. Preserve a readable outline and reduced-flash brightness; emission pivot (0,16) proposed.',origin=(0,16))
fx('spr_fx_laser_charge','F','F2',(64,64),8,'A restrained amber-gold rod-tip charge halo with small inward motes',poses='f0 faint readable halo; f1-5 grow steadily; f6-7 hold bright charged core. No whiteout.')
fx('spr_laser_aim','F','F2',(16,16),1,'One amber horizontal aim dash with dark rim and transparent padding, pointing east',fps=None,loop='static',facing='east',extra='Not the damaging beam; warning stays visible on pale sand. Engine repeats/rotates dashes.')
fx('spr_thunder_marker','F','F3',(128,64),4,'A warning ground ellipse with an amber-red rim and dark contour, clear hollow centre',fps=10,loop='loop',poses='Four gentle expanding/pulsing phases; visible rim from frame 0, no strobe.',extra='Communicate danger by shape and value as well as colour. Warning must read within 250ms, do not delay visibility.')
fx('spr_thunder_exclaim','F','F3',(32,48),1,'A large readable amber exclamation mark with charcoal outline and transparent background',fps=None,loop='static')
fx('spr_lightning_bolt','F','F3',(96,384),6,'A narrow descending pale gold-white lightning bolt with blue-grey edge and sparse branching',origin=(48,376),fps=24,poses='f0 narrow leader; f1 main connection; f2 strongest contact; f3-4 thinning forks; f5 faded tail.',extra='Ground contact at (48,376); the bolt rises upward from that anchor. Local effect only, no full-screen illumination or repeated bright-dark strobe.')
fx('spr_fx_thunder_impact','F','F3',(128,96),8,'A local amber-white lightning ground impact, elliptical dust and small sparks',origin=(64,80),poses='f0 contact; f1-2 ring expands; f3-5 dust and sparks; f6-7 fade.',extra='Origin proposed; reduced-flash version must preserve the dark ground ring and silhouette.')
fx('spr_summon_crack','F','F4',(96,48),6,'A dark branching summoning crack in the ground with restrained amber inner light',poses='f0 central readable fissure; f1-3 branches expand; f4-5 settle into final warning.',origin=(48,24),extra='Do not bake an undead body into the crack; final state hold proposed until rise handoff.')
fx('spr_fx_sand_burst','F','F4',(96,64),8,'An ochre sand emergence burst, low ground ellipse, outward small chunks and pale dust',origin=(48,48),poses='f0 contact; f1-3 burst; f4-6 dust falls; f7 fades.')
for aid,size,origin,n,states,desc in [
    ('spr_gate_arena',(192,192),(96,176),8,['closed f0','opening f0-7','open f7','closing reverse f7-0'],'A three-cell-wide desert arena gate, heavy warm sandstone posts, restrained iron/gold portcullis, clear 192px overall span. Raised bars retract without moving posts.'),
    ('spr_door_sealed',(192,224),(96,208),1,['sealed'],'A sealed heavy sandstone dungeon door with worn gold/ochre geometric trim and a dark seam, no readable text or recovered relic.'),
    ('spr_dungeon_entrance',(384,320),(192,304),1,['static threshold'],'A monumental ruined desert dungeon entrance, pale ochre stone facade, deep dark doorway exactly 128px wide, broken blocks and restrained Pharaoh-era geometric trim. No interior scene or Grail.')]:
    add(aid,'F','F5','Gate or dungeon threshold',size,origin,frames=n,fps=16 if n>1 else None,loop='state_driven' if n>1 else 'static',kind='prop',states=states,subject=desc,
        poses='Eight registered opening positions; reverse order for closing only if weight and mechanism read naturally.' if n>1 else 'Static single image.',
        timing='counts/sizes from F5; origins, 16fps and reversal proposal for integration',
        checks=['Exact frame canvas, fixed post/base registration.','Door opening width and three-cell gate span measured.','Pass-behind tops and foot-level collision evaluated by Claude.','No relic recovery or invented story text.'])
for aid,size,desc in [
    ('spr_title_bg',(1280,720),'A wide illustrated desert canyon and distant ruined Pharaoh-era masonry, pale warm sand and muted ochre cliffs, calm darkened centre reserved for title/menu text. No characters, logo or text.'),
    ('spr_title_logo',(640,240),'A deliberate fantasy adventure wordmark reading exactly "Dave’s & Enemies", warm pale stone and restrained brass, readable ampersand, no subtitle, no extra text.'),
    ('spr_ending_bg',(1280,720),'The desert dungeon threshold in quiet dusk light, deep doorway still unexplored, calm central negative space for later ending text. No recovered Grail or text.')]:
    add(aid,'F','F8','Title or ending presentation art',size,(0,0),kind='scene',priority='P2',subject=desc,
        extra='Keep ending composition restrained and the threshold dark, no playable dungeon interior. The ending title To Be Continued and its menu button are live text, not baked into spr_ending_bg. Title logo requires manual typography and spelling verification; do not rely on generated letterforms.',
        checks=['Native 1280x720 composition or exact logo canvas.','Title spelling, apostrophe and ampersand inspected character by character.','No recovered Grail; GUI text areas remain clear.'])


def prompt(a: dict, variant: tuple[str,str] | None = None) -> str:
    anim=a['animation']; w,h=a['target_dimensions_px']; n=anim['frame_count']
    lines=[f"Use case: {'identity-preserve' if a['kind']=='character' else 'stylized-concept'}.",
           f"Asset ID: {a['asset_id']}. Purpose: {a['purpose']}. Game: Dave's & Enemies, Chapter I Desert."]
    if a['kind']=='portrait':
        lines.append('Reference roles: attach the established character model for identity and costume. Render a deliberate HAND-PAINTED FANTASY ILLUSTRATION with natural adult anatomy, not an enlarged gameplay sprite.')
    elif a['kind']=='ui':
        lines.append('Reference roles: attach this component from art/reference/ui_handoff/assets/ as the authoritative geometry and palette reference. The prototype is already supplied; reuse it for the current milestone. This optional generation prompt is for later approved art polish only. Preserve the existing dark ink/cool grey/gold hierarchy. This is flat screen-space UI, no world camera foreshortening.')
    elif a['kind']=='material':
        lines.append('Reference roles: attach the original template floor/wall images for material density, broad shading and restrained contrast. Render an orthographic flat material sample, no perspective or vignette. Smooth illustrated game texture, not coarse pixel art.')
    else:
        style=STYLE.replace('text, watermark,','watermark,') if a['asset_id']=='spr_title_logo' else STYLE
        lines.append('Reference roles: attach art/reference/template_sprite_inspection.png as the authoritative style/density reference. '+style)
    if a['kind']=='character':
        lines.append('Production gate: run the animation request only after this character base and this facing pass native-size identity, perspective and alignment inspection. If that gate is pending, make only the neutral base/facing reference first, then stop before animation.')
    if a['kind']=='character' and not a['asset_id'].startswith('spr_dave_'):
        entity=next(k for k in sorted(ENTITIES,key=len,reverse=True) if a['asset_id'].startswith('spr_'+k+'_'))
        lines.append(f'Attach the established {entity} base model as the identity reference. If it has not been established, generate only its neutral base first and stop before animation. Do not invent a new design for each state.')
    lines.extend(['Subject: '+a['subject'], 'Direction: '+FACING[anim['direction']],
                  f'Final target: {w}x{h} native pixels PER FRAME; '+a['alignment'],
                  'Transparency: '+a['transparency']+'.'])
    if variant:
        lines.append(f'Material detail variant {variant[0]} ONLY: {variant[1]} Do not generate the other variants in the same image.')
    if n>1:
        if a['kind']=='material':
            lines.append(f'Deliver {n} consecutive material phases separately, each {w}x{h}. No sheet mixing other materials. Frame sequence: '+anim['pose_plan'])
        elif a['kind']=='ui':
            lines.append(f'Deliver {n} discrete registered UI states as separate images or one horizontal row of {n} equal cells. These are state-selected images, not a loop. '+anim['pose_plan'])
        else:
            lines.append(f'Generate ONLY this one asset/action/direction as {n} chronological frames in one horizontal row, equally sized cells, left to right, no labels or visible grid lines. Planned final strip is {w*n}x{h}, or individual fixed {w}x{h} frames. A generator may produce a larger source; exact grid and dimensions must be checked and exported afterward. No other characters, actions or directions.')
            lines.append('Pose plan, zero-based indices: '+anim['pose_plan'])
    else:
        lines.append('Generate one static asset only, no contact sheet or alternative views.')
        if anim['pose_plan']: lines.append('Pose: '+anim['pose_plan'])
    if anim['game_ticks_per_frame']:
        lines.append(f"Timing: at 60Hz hold frames 0..{n-1} for {anim['game_ticks_per_frame']} game ticks respectively; not uniform sprite fps. "+anim['timing_status']+'.')
    elif anim['fps']:
        lines.append(f"Playback specification: {anim['fps']} fps; {anim['loop']}. {anim['timing_status']}.")
    else:
        lines.append('Playback/state selection: '+anim['loop']+'. '+anim['timing_status']+'.')
    if a['footprint_px']:
        lines.append(f"Collision footprint reference (not painted into art): {a['footprint_px'][0]}x{a['footprint_px'][1]} pixels at the base.")
    if a['additional_instructions']: lines.append('Additional constraints: '+a['additional_instructions'])
    if a['kind'] not in ['material','scene','portrait','ui']:
        lines.append('Transparent outer canvas, no ground plane or baked ground shadow. Preserve solid interiors, clean straight alpha and no clipped silhouette. Source artwork is not an engine-ready export until measured and inspected.')
    lines.append('Inspection before acceptance: '+' '.join(a['inspection_checklist']))
    return '\n\n'.join(lines)+'\n'


def main():
    DOCS.mkdir(exist_ok=True)
    for milestone in 'ABCDEF': (ART/'prompts'/('milestone_'+milestone.lower())).mkdir(parents=True,exist_ok=True)
    for a in ASSETS:
        if a['kind']=='ui':
            names=([a['asset_id']+'.png'] if a['animation']['frame_count']==1 else [a['asset_id']+f'_{i:02d}.png' for i in range(a['animation']['frame_count'])])
            a['status']='prototype_supplied_in_UI_HANDOFF; engine_acceptance_pending'
            a['source_files']=['art/reference/ui_handoff/assets/'+n for n in names]
            a['available_delivery']={'archive':'docs/UI_HANDOFF.zip','entries':['ui/assets/'+n for n in names], 'route':'reuse prototype first; generation prompt is optional polish'}
        variations=a['variants'] or [None]
        a['prompt_files']=[]
        for variant in variations:
            suffix='.'+variant[0] if variant else ''
            p=ART/'prompts'/('milestone_'+a['milestone'].lower())/(a['asset_id']+suffix+'.txt')
            p.write_text(prompt(a,variant),encoding='utf-8')
            a['prompt_files'].append(p.relative_to(ROOT).as_posix())
        if a['asset_id']=='spr_dave_idle_down':
            a['status']='base_source_generated; eight-frame idle not produced'
            a['source_files']=['art/source/dave/dave_base_down_v001.png','art/source/dave/dave_base_down_v002.png']
        if a['asset_id']=='spr_icon_potion_health':
            a['status']='source_generated; native export and cleanup pending'
            a['source_files']=['art/source/icons/spr_icon_potion_health_source_v001.png']
        delivery_dir=next((ART/'exports/dave'/batch/a['asset_id'] for batch in ['down_v001','cardinal_v001']
                           if (ART/'exports/dave'/batch/a['asset_id']/(a['asset_id']+'.json')).is_file()),None)
        if delivery_dir is not None:
            sidecar_path=delivery_dir/(a['asset_id']+'.json')
            sidecar=json.loads(sidecar_path.read_text(encoding='utf-8'))
            n=sidecar['frame_count']
            a['status']=sidecar['status']
            a['source_files']=sorted({sidecar['source']}|{f.get('source',sidecar['source']) for f in sidecar['source_frames']})
            a['native_delivery']={
                'frames_directory':delivery_dir.relative_to(ROOT).as_posix(),
                'strip':(delivery_dir/(a['asset_id']+f'_strip{n}.png')).relative_to(ROOT).as_posix(),
                'sidecar':sidecar_path.relative_to(ROOT).as_posix(),
                'review_gif':'art/review/dave/'+delivery_dir.parent.name+'/'+a['asset_id']+'_preview.gif',
                'contact_sheet':'art/review/dave/'+delivery_dir.parent.name+'/'+a['asset_id']+'_contact.png',
                'validation':'art/review/dave/'+delivery_dir.parent.name+'/validation.json',
                'engine_preview_checked':False,
            }
            a['verified_engine_ready']=False
    ids=[a['asset_id'] for a in ASSETS]
    assert len(ids)==len(set(ids)), 'duplicate IDs'
    for a in ASSETS:
        n=a['animation']['frame_count']; ticks=a['animation']['game_ticks_per_frame']
        assert n>0 and all(x>0 for x in a['target_dimensions_px'])
        if ticks: assert len(ticks)==n
        for p in a['prompt_files']: assert (ROOT/p).is_file()
    bundle={'schema_version':1,'game':"Dave's & Enemies, Chapter I Desert",'date':'2026-10-31',
            'contract':'docs/PROJECT_CONTRACT.md','requests':'docs/ASSET_REQUESTS.md',
            'narrative_requests':'docs/NARRATIVE_ASSET_REQUESTS.md',
            'original_brief':'art/reference/original_game_brief.txt',
            'ui_handoff':'docs/UI_HANDOFF.zip',
            'scope':'art specifications and source generation only; no runtime integration',
            'asset_count':len(ASSETS),'assets':ASSETS}
    (ART/'asset_manifest.json').write_text(json.dumps(bundle,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    lines=['# Dave’s and Enemies art asset manifest','',
           'Art-only handoff for Claude. Exact contract IDs are preserved; proposed wildcard expansions and undefined layout choices are identified. Assets include planned artwork, generated sources and existing supplied UI prototypes; none is marked engine-verified. Timing and geometry marked proposed are art recommendations, not edits to engineering data.','',
           'The complete machine-readable specification is [asset_manifest.json](../art/asset_manifest.json). Every entry contains dimensions, origin, transparency, states, direction, frame count, timing, dependencies, inspection checklist and a complete copy-ready prompt file.','']
    for m in 'ABCDEF':
        group=[a for a in ASSETS if a['milestone']==m]
        lines += [f'## Milestone {m}','', '| Asset ID | Pri | Target per frame | Origin | States and playback | Prompt | Native delivery |','|---|---|---|---|---|---|---|']
        for a in group:
            an=a['animation']; playback=(str(an['fps'])+' fps') if an['fps'] else ('engine timed' if an['game_ticks_per_frame'] else 'state/static')
            if an['game_ticks_per_frame']:playback+=' '+str(an['game_ticks_per_frame'])+' ticks'
            pp=' · '.join(f'[prompt{(" "+str(i+1)) if len(a["prompt_files"])>1 else ""}](../{p})' for i,p in enumerate(a['prompt_files']))
            states='; '.join(a['required_states'])
            delivery=a.get('native_delivery')
            delivery_link=f'[strip](../{delivery["strip"]}) · [timing](../{delivery["sidecar"]}) · engine check pending' if delivery else ('existing UI prototype' if a['kind']=='ui' else 'planned/source only')
            lines.append(f'| `{a["asset_id"]}` | {a["priority"]} | {a["target_dimensions_px"][0]}×{a["target_dimensions_px"][1]} | {a["origin_px"]} | {an["frame_count"]} f; {playback}; {an["loop"]}; {states} | {pp} | {delivery_link} |')
        lines.append('')
    lines += ['## Scope and ID decisions','',
              'C4 names are prop keys in the requests rather than specified sprite IDs. Proposed `spr_<prop_key>` mappings are explicitly marked in the JSON. B10 unspecified canvas/origin choices and the C3 atlas layout also require registration by Claude. Narrative-specific IDs and corrected E3 sizes/turn timing follow NARRATIVE_ASSET_REQUESTS. Pharaoh rage is a parked P2 option, unnecessary for the current script. The requested `spr_bat_fly` ID already exists; no existing resource was overwritten.','',
              'A10 and D1 UI prototype PNG/SVG sources are already supplied in UI_HANDOFF.zip. The manifest links copied reference assets and marks their generation prompts optional polish; reuse and validate the prototypes before commissioning alternatives. Their schematic world/portrait art is not a style reference.','',
              'Audio, font licensing/installation, room layouts, story/dialogue data and cutscene implementation remain with Claude. A11/A12, B11, C5, E1/E6–E9 and F6/F7 are tracked by ASSET_REQUESTS and are outside this art production pack. The original game brief has been read from its source chat and saved verbatim under art/reference. Original template screenshots remain unavailable; actual template PNGs and metadata anchor this art direction.','']
    (DOCS/'ART_ASSET_MANIFEST.md').write_text('\n'.join(lines),encoding='utf-8')
    first=['# Dave’s and Enemies Milestone A art prompts','',
           'Copy-ready generation prompts for the next playable milestone. Run only one prompt at a time. Establish and inspect each character base before its animation prompts. All numeric sizes below are final export targets, not claims about generator output. Full inspection specifications are in the JSON manifest.','',
           'Recommended queue: Dave base reference → down idle → down walk → down attack → slash → other Dave facings one action at a time → undead base and its down-facing actions → remaining undead facings → materials one variant at a time → chest → checkpoint and sparkle → potion icon. Reuse the existing HUD prototype kit from UI_HANDOFF.zip; HUD prompts are optional later polish. Independent static assets may proceed while character cleanup is pending.','',
           'Dave v002 now has native down idle plus walk/attack for down, right, independently authored left, and up:80 animation frames total. See ART_DAVE_DOWN_HANDOFF.md and ART_DAVE_CARDINAL_HANDOFF.md before regenerating them. The latest batch adds54 frames. Native PNG/strip checks passed; engine acceptance remains with Claude. Left walk/attack IDs were added under the explicit user continuation; bind them for west without mirroring. Health-potion source v001 still needs export.','']
    for a in [x for x in ASSETS if x['milestone']=='A']:
        for variant in a['variants'] or [None]:
            label=a['asset_id']+(' '+variant[0] if variant else '')
            first += ['## '+label,'','```text',prompt(a,variant).rstrip(),'```','']
    (DOCS/'ART_MILESTONE_A_PROMPTS.md').write_text('\n'.join(first),encoding='utf-8')
    print(json.dumps({'assets':len(ASSETS),'by_milestone':dict(Counter(a['milestone'] for a in ASSETS)),
                      'prompt_files':sum(len(a['prompt_files']) for a in ASSETS)},indent=2))


if __name__=='__main__': main()
