"""Validate native art deliveries and assemble review media from painted exports."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art/exports/dave/down_v001'
REVIEW=ROOT/'art/review/dave/down_v001'
ASSETS=[('spr_dave_idle_down',8,96,96,[48,88]),
        ('spr_dave_walk_down',10,96,96,[48,88]),
        ('spr_dave_attack_down',8,128,128,[64,112])]


def premult(im):
    a=np.array(im).astype(float)
    return np.dstack((a[:,:,:3]*(a[:,:,3:4]/255),a[:,:,3]))


def main():
    errors=[];records=[];loaded={}
    for name,n,w,h,origin in ASSETS:
        directory=OUT/name;sidecar=json.loads((directory/(name+'.json')).read_text())
        frames=[]
        for i in range(n):
            p=directory/(name+f'_{i:02d}.png');im=Image.open(p)
            if im.size!=(w,h) or im.mode!='RGBA':errors.append(str(p)+' canvas/mode')
            if 'srgb' not in im.info:errors.append(str(p)+' missing sRGB')
            a=np.array(im.getchannel('A'));border=np.r_[a[0],a[-1],a[:,0],a[:,-1]]
            if border.max()!=0:errors.append(str(p)+' nontransparent border')
            frames.append(im.copy())
        strip=Image.open(directory/(name+f'_strip{n}.png'))
        if strip.size!=(w*n,h):errors.append(name+' strip dimensions')
        for i,im in enumerate(frames):
            if not np.array_equal(np.array(im),np.array(strip.crop((i*w,0,(i+1)*w,h)))):errors.append(name+' strip frame '+str(i))
        if sidecar['origin_px']!=origin:errors.append(name+' origin')
        if name.endswith('attack_down') and (sidecar['game_ticks_per_frame']!=[3,3,3,3,3,4,4,4] or sum(sidecar['game_ticks_per_frame'])!=27):errors.append(name+' timing')
        diffs=[round(float(np.abs(premult(frames[(i+1)%n])-premult(frames[i])).mean()),3) for i in range(n)]
        visual={
            'identity_and_right_hand':'all native frames and painted sources inspected; sword anatomical right throughout',
            'costume':'silver plate, ivory tabard, golden-brown hair, brown garments, two shoulder cape attachments retained; normal occlusion during attacks',
            'lighting':'upper-left highlight convention preserved; no mirrored figures',
            'ground':'fixed native origin and canvases; locomotion knee/foot projection varies through stride',
            'adjacent_premultiplied_rgba_mean_absolute_difference':diffs,
            'loop_seam':('f7/f0 subtle silhouette settling remains; seam difference '+str(diffs[-1])+' versus largest internal '+str(max(diffs[:-1])) if 'idle' in name else
                         'f9/f0 passing-to-push-off continuity inspected; no duplicate end pose' if 'walk' in name else 'not a loop; f7 returns to exact checked base registration'),
            'remaining_engine_check':'Claude: preview native speed, transition alignment, footstep events and active hitbox timing in GameMaker',
        }
        if 'walk' in name:visual['contacts']='f2 anatomical right foot/viewer left; f7 anatomical left foot/viewer right, corrected and inspected'
        if 'attack' in name:visual['poses']='f0-1 anticipation, f2-4 active, f3 contact, f5-7 recovery; shortened inconsistent blades; final pose reuses base'
        sidecar['inspection']['visual_checks']=visual
        sidecar['inspection']['engine_preview_checked']=False
        sidecar['inspection']['native_png_and_strip_checks_passed']=not errors
        sidecar['status']='native_export_inspected_pending_Claude_engine_acceptance'
        sidecar['verified_engine_ready']=False
        (directory/(name+'.json')).write_text(json.dumps(sidecar,indent=2)+'\n')
        records.append({'asset_id':name,'frame_count':n,'canvas_px':[w,h],'origin_px':origin,
                        'strip_px':[w*n,h],'fps':sidecar['fps'],
                        'game_ticks_per_frame':sidecar.get('game_ticks_per_frame'),
                        'loop':sidecar['loop'],'visual_inspection':visual})
        loaded[name]=frames
    # Review animation: three native-aligned stages, not engine sprite data.
    # Attack is selected from exact 60Hz frame boundaries at a 10ms GIF sampling
    # interval. The JSON tick schedule remains authoritative for integration.
    rendered=[]
    attack_ends=np.cumsum([50,50,50,50,50,1000/15,1000/15,1000/15])
    for t in range(0,2400,10):
        frame=Image.new('RGB',(1248,530),'#30343a');draw=ImageDraw.Draw(frame)
        draw.text((14,10),'DAVE DOWN - native export review. Ground crosses align at each origin. GameMaker preview pending.',fill='white')
        indices=[int((t%800)//100),int((t%500)//50),int(np.searchsorted(attack_ends,t%450,side='right'))]
        for col,(spec,index) in enumerate(zip(ASSETS,indices)):
            name,n,w,h,origin=spec;index=min(n-1,index);im=loaded[name][index]
            stage=Image.new('RGBA',(128,128),'#cdb986')
            pos=(64-origin[0],112-origin[1]);stage.alpha_composite(im,pos)
            x=col*416+16;y=70
            frame.paste(stage.convert('RGB').resize((384,384),Image.Resampling.NEAREST),(x,y))
            draw.line((x+64*3-8,y+112*3,x+64*3+8,y+112*3),fill='#705e43')
            label='IDLE 10 fps' if col==0 else 'WALK 20 fps' if col==1 else 'ATTACK 450 ms / exact ticks in JSON'
            draw.text((x,42),label,fill='white')
            phase=('contact' if index in (2,7) else 'stride') if col==1 else ('anticipation' if index<2 else 'ACTIVE' if index<5 else 'recovery') if col==2 else 'breath / cape'
            draw.text((x,468),f'frame {index:02d}  {phase}',fill='#f2d17d' if phase in ('contact','ACTIVE') else 'white')
        draw.text((16,506),'Preview GIF uses a fixed shared palette; PNG frames retain full RGBA colour. No slash FX is baked into the attack.',fill='white')
        rendered.append(frame)
    palette=Image.new('RGB',(1248,530*len(rendered[::10])))
    for i,fr in enumerate(rendered[::10]):palette.paste(fr,(0,i*530))
    palette=palette.quantize(colors=256)
    quant=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in rendered]
    quant[0].save(REVIEW/'dave_down_animation_review.gif',save_all=True,append_images=quant[1:],duration=10,loop=0,disposal=1,optimize=True)
    rendered[0].save(REVIEW/'dave_down_animation_review_poster.png')
    # Straight-alpha fringe review on four contrasting backgrounds.
    chosen=[loaded[ASSETS[0][0]][0],loaded[ASSETS[1][0]][2],loaded[ASSETS[1][0]][7],loaded[ASSETS[2][0]][1],loaded[ASSETS[2][0]][3],loaded[ASSETS[2][0]][4]]
    board=Image.new('RGB',(128*3*len(chosen),128*3*4+45),'#30343a');d=ImageDraw.Draw(board)
    d.text((10,10),'Alpha and contour review: idle0, walk2, walk7, attack1, attack3, attack4. White / black / sand / ruins.',fill='white')
    for row,bg in enumerate(['#ffffff','#000000','#cdb986','#292b2d']):
        for col,im in enumerate(chosen):
            tile=Image.new('RGBA',(128,128),bg);tile.alpha_composite(im,((128-im.width)//2,112-(88 if im.width==96 else 112)))
            board.paste(tile.convert('RGB').resize((384,384),Image.Resampling.NEAREST),(col*384,45+row*384))
    board.save(REVIEW/'dave_down_alpha_review.png')
    report={'date':'2026-10-31','scope':'native art exports only; no GameMaker execution or integration',
            'exported_animation_frames':26,'base_reference_frames':1,'errors':errors,'assets':records,
            'verified_engine_ready':False,'source_prompts':'art/source/dave/down_batch_v001/*.prompt.txt',
            'optional_art_polish':['Minor generated outline/face variation between poses.','Idle f7-to-f0 has a small visible silhouette settle; no perfect seamless-loop claim.']}
    (REVIEW/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'animation_frames':26,'assets':len(records),'errors':errors,'engine_tested':False},indent=2))
    assert not errors


if __name__=='__main__':main()
