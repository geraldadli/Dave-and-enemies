"""Mechanical alpha cleanup, registration and packing of imagegen-painted Dave art.

No poses are synthesized here. Source cell crops/ground anchors are measured in
the export plan. A single uniform scale is used for each action, with fixed output
canvases. GameMaker resource files are never touched.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, PngImagePlugin
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / 'art/source/dave/down_batch_v001'
OUT = ROOT / 'art/exports/dave/down_v001'
REVIEW = ROOT / 'art/review/dave/down_v001'


def save_png(im, path):
    info = PngImagePlugin.PngInfo()
    info.add(b'sRGB', b'\x00')
    im.save(path, pnginfo=info)


def clean_alpha(im):
    """Remove disconnected alpha noise; retain 3px antialiased source perimeter."""
    arr=np.array(im.convert('RGBA'))
    alpha=arr[:,:,3]
    labels,n=ndimage.label(alpha>=16)
    sizes=np.bincount(labels.ravel()); sizes[0]=0
    # Main body and physically separate painted fragments may be legitimate on
    # attack poses. Keep substantial components, report counts for inspection.
    keep_ids=np.flatnonzero(sizes>=max(40,int(sizes.max()*0.0003)))
    keep=np.isin(labels,keep_ids)
    keep=ndimage.binary_dilation(keep,iterations=3)
    old=alpha.copy()
    alpha=np.where(keep,np.minimum(255,np.rint(alpha.astype(float)*255/253)),0).astype('uint8')
    arr[:,:,3]=alpha
    arr[alpha==0,:3]=0
    return Image.fromarray(arr,'RGBA'), {'discarded_nonzero_pixels':int(np.count_nonzero((old>0)&(alpha==0))),
                                        'substantial_components':len(keep_ids),
                                        'alpha_gain':255/253}


def isolate(im, component_label):
    """Separate overlapping source-cell bounding boxes by actual connected art."""
    arr=np.array(im.convert('RGBA'))
    labels,_=ndimage.label(arr[:,:,3]>=128)
    keep=ndimage.binary_dilation(labels==component_label,iterations=3)
    arr[~keep,3]=0
    return Image.fromarray(arr,'RGBA')


def register(im, canvas, anchor, origin, scale):
    # Filter associated-alpha RGBa then restore straight alpha to avoid black
    # fringes from interpolating transparent RGB. No opaque matte is introduced.
    coefficients=(1/scale,0,anchor[0]-origin[0]/scale,
                  0,1/scale,anchor[1]-origin[1]/scale)
    return im.convert('RGBa').transform(tuple(canvas),Image.Transform.AFFINE,
        coefficients,Image.Resampling.BICUBIC).convert('RGBA')


def frame_report(im):
    a=np.array(im.getchannel('A'))
    nz=np.argwhere(a>0); solid=np.argwhere(a>=128)
    bounds=lambda pts:[int(pts[:,1].min()),int(pts[:,0].min()),int(pts[:,1].max()+1),int(pts[:,0].max()+1)] if len(pts) else None
    border=np.r_[a[0,:],a[-1,:],a[:,0],a[:,-1]]
    return {'canvas_px':list(im.size),'alpha_bounds':bounds(nz),'solid_bounds':bounds(solid),
            'border_alpha_max':int(border.max()),'transparent_pixels':int(np.count_nonzero(a==0)),
            'opaque_pixels':int(np.count_nonzero(a==255))}


def review_frames(frames, asset, durations):
    w,h=frames[0].size
    cols=min(5,len(frames)); rows=(len(frames)+cols-1)//cols
    cellw=max(w*3,300); cellh=h*3+40
    sheet=Image.new('RGB',(cols*cellw,rows*cellh+45),'#393d43'); draw=ImageDraw.Draw(sheet)
    draw.text((10,10),asset+' - native export frames enlarged 3x; 0-based indices',fill='white')
    for i,im in enumerate(frames):
        x=(i%cols)*cellw; y=45+(i//cols)*cellh
        bg=Image.new('RGBA',(w,h),'#cdb986');bg.alpha_composite(im)
        sheet.paste(bg.convert('RGB').resize((w*3,h*3),Image.Resampling.NEAREST),(x,y))
        draw.text((x+5,y+h*3+8),f'f{i:02d}  {durations[i]} ms',fill='white')
    save_png(sheet,REVIEW/(asset+'_contact.png'))
    # GIF is review media only; delivered frames retain RGBA alpha.
    rendered=[]
    for im in frames:
        tile=Image.new('RGBA',(w,h),'#cdb986');tile.alpha_composite(im)
        rendered.append(tile.convert('RGB').resize((w*4,h*4),Image.Resampling.NEAREST))
    rendered[0].save(REVIEW/(asset+'_preview.gif'),save_all=True,append_images=rendered[1:],
                     duration=durations,loop=0,disposal=2)


def export(name):
    plan=json.loads((BATCH/'export_plan.json').read_text(encoding='utf-8'))[name]
    source=ROOT/plan['source']; im=Image.open(source).convert('RGBA')
    sources={plan['source']:im}
    frames=[]; reports=[]
    directory=OUT/name;directory.mkdir(parents=True,exist_ok=True)
    for i,frame in enumerate(plan['source_frames']):
        src=frame.get('source',plan['source'])
        if src not in sources:sources[src]=Image.open(ROOT/src).convert('RGBA')
        original=sources[src]
        if 'component_label' in frame:original=isolate(original,frame['component_label'])
        crop=original.crop(tuple(frame['box']))
        cleaned,cleanup=clean_alpha(crop)
        native=register(cleaned,plan['canvas_px'],frame['anchor'],plan['origin_px'],frame.get('scale',plan['scale']))
        save_png(native,directory/(name+f'_{i:02d}.png'))
        frames.append(native);reports.append({**frame_report(native),'cleanup':cleanup,'painted_source':src})
    strip=Image.new('RGBA',(frames[0].width*len(frames),frames[0].height))
    for i,frame in enumerate(frames):strip.paste(frame,(i*frame.width,0))
    save_png(strip,directory/(name+f'_strip{len(frames)}.png'))
    sidecar={**plan,'asset_id':name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
             'frame_count':len(frames),'delivery':'individual PNG frames and horizontal strip; 8-bit RGBA sRGB straight alpha',
             'source_frames_are_measured':True,'inspection':{'frames':reports,'mechanical_checks_passed':all(r['border_alpha_max']==0 for r in reports),
             'visual_checks':'pending','engine_preview_checked':False},'verified_engine_ready':False}
    (directory/(name+'.json')).write_text(json.dumps(sidecar,indent=2)+'\n',encoding='utf-8')
    durations=plan.get('review_durations_ms',[100]*len(frames))
    review_frames(frames,name,durations)
    print(json.dumps({'asset':name,'frames':len(frames),'reports':reports},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('asset');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
    export(args.asset)
