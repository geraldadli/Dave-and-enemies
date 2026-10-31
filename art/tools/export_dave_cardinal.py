"""Art export wrapper for the authored right/left/up Dave batch."""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

import export_dave_down as core

ROOT=Path(__file__).resolve().parents[2]
core.BATCH=ROOT/'art/source/dave/cardinal_batch_v001'
core.OUT=ROOT/'art/exports/dave/cardinal_v001'
core.REVIEW=ROOT/'art/review/dave/cardinal_v001'


def components(path,rows=2):
    im=Image.open(ROOT/path).convert('RGBA');a=np.array(im);labels,_=ndimage.label(a[:,:,3]>=128)
    sizes=np.bincount(labels.ravel());items=[]
    r,g,b=[a[:,:,i].astype(float) for i in range(3)]
    yy=np.indices(labels.shape)[0]
    for label,s in enumerate(ndimage.find_objects(labels),1):
        if sizes[label]<2000:continue
        box=[s[1].start,s[0].start,s[1].stop,s[0].stop]
        brown=(labels==label)&(a[:,:,3]>200)&(r>35)&(r<170)&(g>20)&(g<125)&(b<100)&(r>g*1.15)&(g>b*1.1)&(yy>box[1]+.82*(box[3]-box[1]))
        by,bx=np.where(brown)
        item={'label':int(label),'bounds':box,'area':int(sizes[label])}
        if len(bx):item['boot_root_candidate']=[round(float((bx.min()+bx.max()+1)/2),1),int(by.max()+4)]
        items.append(item)
    items.sort(key=lambda i:(min(rows-1,int(i['bounds'][1]/(im.height/rows))),i['bounds'][0]))
    return im,items


def measured_frames(path,anchors,scale,rows=2):
    im,items=components(path,rows)
    if len(items)!=len(anchors):raise ValueError(f'Expected {len(anchors)} bodies, found {len(items)} in {path}')
    out=[]
    for item,anchor in zip(items,anchors):
        b=item['bounds'];box=[max(0,b[0]-5),max(0,b[1]-5),min(im.width,b[2]+5),min(im.height,b[3]+5)]
        out.append({'component_label':item['label'],'box':box,'anchor':[anchor[0]-box[0],anchor[1]-box[1]],'scale':scale})
    return out


def inspect(path,rows=2):
    im,items=components(path,rows)
    print(json.dumps({'source':path,'size_px':list(im.size),'significant_components':items},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['inspect','export']);p.add_argument('name');p.add_argument('--rows',type=int,default=2);args=p.parse_args()
    if args.action=='inspect':inspect(args.name,args.rows)
    else:
        core.OUT.mkdir(parents=True,exist_ok=True);core.REVIEW.mkdir(parents=True,exist_ok=True)
        core.export(args.name)
