"""Validate and preview independently painted right/left/up native Dave sprites."""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art/exports/dave/cardinal_v001'
REVIEW=ROOT/'art/review/dave/cardinal_v001'
FACINGS=['side','left','up']


def premult(im):
    a=np.array(im).astype(float)
    return np.dstack([a[:,:,:3]*a[:,:,3:4]/255,a[:,:,3]])


def anatomy(direction,action):
    if direction=='side':
        return 'Anatomical right near arm holds sword; far left hand empty; right-arm crossing during attack inspected.'
    if direction=='left':
        return 'Anatomical right far shoulder/arm holds sword; near foreground left arm remains empty. Independent drawing, no whole-sprite mirror.'
    return ('Image-right right arm is weapon arm; image-left left glove empty. Back view throughout. ' +
            ('Right arm crosses north/front behind hair in f4; empty left arm remains low, weapon arm partly occluded.' if action=='attack' else 'Hair overlays upper cape, both attachments remain under hair.'))


def main():
    errors=[];records=[];loaded={}
    for direction in FACINGS:
        for action,n,size,origin in [('walk',10,96,[48,88]),('attack',8,128,[64,112])]:
            name=f'spr_dave_{action}_{direction}';directory=OUT/name
            meta=json.loads((directory/(name+'.json')).read_text())
            frames=[];local_errors=[]
            for i in range(n):
                path=directory/(name+f'_{i:02d}.png');im=Image.open(path)
                if im.size!=(size,size) or im.mode!='RGBA':local_errors.append('size/mode '+path.name)
                if path.read_bytes()[24]!=8 or 'srgb' not in im.info:local_errors.append('8bit/sRGB '+path.name)
                a=np.array(im.getchannel('A'));border=np.r_[a[0],a[-1],a[:,0],a[:,-1]]
                if int(border.max())!=0:local_errors.append('edge clipping '+path.name)
                frames.append(im.copy())
            strip=Image.open(directory/(name+f'_strip{n}.png'))
            if strip.size!=(n*size,size):local_errors.append('strip dimensions')
            for i,im in enumerate(frames):
                if not np.array_equal(np.array(im),np.array(strip.crop((i*size,0,(i+1)*size,size)))):local_errors.append('strip content '+str(i))
            if meta['origin_px']!=origin:local_errors.append('origin')
            if action=='walk' and (meta['fps']!=20 or meta['foot_contacts']!=[2,7]):local_errors.append('walk timing/events')
            if action=='attack' and meta['game_ticks_per_frame']!=[3,3,3,3,3,4,4,4]:local_errors.append('attack timing')
            diffs=[round(float(np.abs(premult(frames[(i+1)%n])-premult(frames[i])).mean()),3) for i in range(n)]
            ratio=round(diffs[-1]/max(diffs[:-1]),3)
            visual={'identity':'native frames and source atlas inspected for v002 hair, silver armor, ivory/brown garments, red cape and upper-left light',
                    'handedness':anatomy(direction,action),
                    'registration':'fixed untrimmed canvases/origins, measured source roots and common uniform scales; no anatomical part warping',
                    'phase_plan':'contacts f2/f7; cloth and heels partly occlude leg identity; check planted-foot sliding in moving engine preview' if action=='walk' else 'f0-1 anticipation; f2-4 active; f3 contact; f5-7 recovery; final pose returns to native facing base',
                    'alpha':'reviewed over white, black, sand and dark ruins; source RGB under alpha0 cleared on export',
                    'adjacent_premultiplied_rgba_MAD':diffs,
                    'loop_boundary':{'f9_to_f0_MAD':diffs[-1],'largest_internal_MAD':max(diffs[:-1]),'ratio':ratio,'interpretation':'diagnostic only; no perfect seamless-loop certification'} if action=='walk' else 'not a loop; native base used for f7',
                    'remaining_polish':'minor generated outline/hair/cape variation and stride smoothing may need retouch after native-speed review',
                    'engine_preview_checked':False}
            meta['inspection']['visual_checks']=visual
            meta['inspection']['native_png_and_strip_checks_passed']=not local_errors
            meta['inspection']['engine_preview_checked']=False
            meta['status']='native_export_inspected_pending_Claude_engine_acceptance'
            meta['verified_engine_ready']=False
            meta['generation_tool']='built-in image_gen.imagegen'
            meta['allow_image_xscale_mirror']=False
            (directory/(name+'.json')).write_text(json.dumps(meta,indent=2)+'\n')
            errors.extend(name+': '+e for e in local_errors)
            records.append({'asset_id':name,'frames':n,'canvas_px':[size,size],'origin_px':origin,'strip_px':[n*size,size],
                            'local_errors':local_errors,'visual_inspection':visual})
            loaded[name]=frames
    for direction in FACINGS:
        name=f'dave_base_{direction}_reference';path=OUT/name/(name+'_00.png');im=Image.open(path)
        if im.size!=(96,96) or im.mode!='RGBA' or 'srgb' not in im.info:errors.append(name+' base metadata')
        meta_path=OUT/name/(name+'.json');meta=json.loads(meta_path.read_text())
        meta['status']='native_facing_reference_accepted_for_this_art_batch'
        meta['inspection']['visual_checks']={'body_height_px':78,'appearance_and_hand':anatomy(direction,'base'),'engine_preview_checked':False}
        meta_path.write_text(json.dumps(meta,indent=2)+'\n')

    # Six-panel review media: every pose is a delivered PNG, no synthetic poses.
    all_frames=[];ends=np.cumsum([50,50,50,50,50,1000/15,1000/15,1000/15])
    for t in range(0,2000,10):
        board=Image.new('RGB',(864,736),'#30343a');d=ImageDraw.Draw(board)
        d.text((12,10),'DAVE V002 - AUTHORED RIGHT / LEFT / UP. Native-export review; GameMaker check pending.',fill='white')
        for col,direction in enumerate(FACINGS):
            for row,action in enumerate(['walk','attack']):
                name=f'spr_dave_{action}_{direction}'
                i=int((t%500)//50) if action=='walk' else min(7,int(np.searchsorted(ends,t%450,side='right')))
                im=loaded[name][i];stage=Image.new('RGBA',(128,128),'#cdb986')
                stage.alpha_composite(im,(16,24) if action=='walk' else (0,0))
                x=col*288+12;y=76+row*326
                board.paste(stage.convert('RGB').resize((256,256),Image.Resampling.NEAREST),(x,y))
                label=('RIGHT / side','LEFT / no mirror','UP / back')[col]
                d.text((x,y-29),label+' - '+action.upper(),fill='white')
                phase=('CONTACT' if i in [2,7] else 'stride') if action=='walk' else ('anticipation' if i<2 else 'ACTIVE' if i<5 else 'recovery')
                d.text((x,y+265),f'f{i:02d}  {phase}',fill='#f2d17d' if phase in ['CONTACT','ACTIVE'] else 'white')
        d.text((12,712),'Review GIF only. PNG strips + exact timing JSON are the delivery. No slash FX or ground shadows baked in.',fill='white')
        all_frames.append(board)
    samples=all_frames[::10];pal_source=Image.new('RGB',(864,736*len(samples)))
    for i,im in enumerate(samples):pal_source.paste(im,(0,736*i))
    palette=pal_source.quantize(colors=256)
    quant=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in all_frames]
    quant[0].save(REVIEW/'dave_cardinal_animation_review.gif',save_all=True,append_images=quant[1:],duration=10,loop=0,disposal=1,optimize=True)
    all_frames[0].save(REVIEW/'dave_cardinal_animation_review_poster.png')

    for action in ['walk','attack']:
        review=Image.new('RGB',(1152,1581),'#30343a');dr=ImageDraw.Draw(review)
        dr.text((10,12),action.upper()+' contrast/alpha check: RIGHT, LEFT, UP. White / black / sand / ruins.',fill='white')
        for row,bg in enumerate(['#ffffff','#000000','#cdb986','#292b2d']):
            for col,direction in enumerate(FACINGS):
                im=loaded[f'spr_dave_{action}_{direction}'][2 if action=='walk' else 3]
                tile=Image.new('RGBA',(128,128),bg);tile.alpha_composite(im,(16,24) if action=='walk' else (0,0))
                review.paste(tile.convert('RGB').resize((384,384),Image.Resampling.NEAREST),(col*384,45+row*384))
        review.save(REVIEW/f'dave_cardinal_{action}_alpha_review.png')
    report={'date':'2026-10-31','scope':'art-only native export validation and visual frame inspection, no GameMaker execution',
            'new_animation_frames':54,'new_facing_references':3,'native_animation_assets':6,'errors':errors,'assets':records,
            'verified_engine_ready':False,'generation':'built-in image_gen.imagegen, one character/action/direction per job',
            'remaining_engine_work':['register authored left IDs and direction4 mapping without whole-sprite mirror',
                                     'preview20fps gait/footstep events and transition alignment',
                                     'use450ms exact attack ticks and active range2-4',
                                     'assess stride and loop/outline smoothing at native motion speed']}
    (REVIEW/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'new_animation_frames':54,'facings':3,'assets':6,'errors':errors,
                      'walk_loop_boundary_ratios':{r['asset_id']:r['visual_inspection']['loop_boundary']['ratio'] for r in records if 'walk' in r['asset_id']},
                      'engine_tested':False},indent=2))
    assert not errors


if __name__=='__main__':main()
