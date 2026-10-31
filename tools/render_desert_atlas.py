"""Render design schematics from exported room data; no game artwork is edited."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"design"/"desert"
PREVIEW=BASE/"previews"
COLORS={".":"#e8cf91",",":"#b99a62",";":"#7eaa69","~":"#4d9fbd","#":"#755746","M":"#77736b","_":"#c7bca0","^":"#d79c55","C":"#302c3c","=":"#b5763d","|":"#b5763d","x":"#744449"}


def font(size,bold=False):
    path=Path("C:/Windows/Fonts")/("segoeuib.ttf" if bold else "segoeui.ttf")
    return ImageFont.truetype(str(path),size) if path.exists() else ImageFont.load_default(size=size)


def render(ids,path,tile,cols):
    specs=json.loads((BASE/"gameplay_specs.json").read_text(encoding="utf-8"))
    panelw=40*tile+30;panelh=24*tile+84;rows=(len(ids)+cols-1)//cols
    im=Image.new("RGB",(cols*panelw+24,rows*panelh+100),"#18202b")
    d=ImageDraw.Draw(im,"RGBA")
    d.text((20,12),"DAVE'S & ENEMIES / DESERT CHAPTER",font=font(23,True),fill="#f7ecd0")
    d.text((20,43),"Original gameplay schematics | provisional 18 main + 6 optional rooms | decoration omitted",font=font(15),fill="#b7c4d1")
    for index,rid in enumerate(ids):
        room=json.loads((BASE/"rooms"/(rid+".json")).read_text(encoding="utf-8"));s=specs[rid]
        ox=14+(index%cols)*panelw;oy=84+(index//cols)*panelh
        label=rid.split("_")[1].upper()
        d.text((ox,oy),f"{label}  {room['display_name']}",font=font(16,True),fill="#fff4d8")
        d.text((ox,oy+23),f"{room['size_cells'][0]}x{room['size_cells'][1]} tiles / {s['intensity']}",font=font(13),fill="#aebcca")
        gx,gy=ox,oy+45
        for y,row in enumerate(room["terrain"]):
            for x,ch in enumerate(row):
                r=[gx+x*tile,gy+y*tile,gx+(x+1)*tile-1,gy+(y+1)*tile-1]
                d.rectangle(r,fill=COLORS[ch])
                if tile>=12:d.rectangle(r,outline=(12,16,20,30),width=1)
                if ch=="^":
                    d.line([r[0]+1,r[1]+tile//3,r[2]-1,r[1]+tile//3],fill="#74522f")
                    d.line([r[0]+1,r[1]+2*tile//3,r[2]-1,r[1]+2*tile//3],fill="#74522f")
                if ch=="x":d.line([r[0],r[1],r[2],r[3]],fill="#edb5b1",width=1)
        for group in s["encounters"]:
            x1,y1,x2,y2=group["combat_rect"]
            d.rectangle([gx+x1*tile,gy+y1*tile,gx+(x2+1)*tile-1,gy+(y2+1)*tile-1],outline="#b64942",width=1)
        for arrival in s["arrivals"]:
            x,y=arrival["cell"];cx=gx+(x+.5)*tile;cy=gy+(y+.5)*tile
            r=max(2,tile//4);d.ellipse([cx-r,cy-r,cx+r,cy+r],fill="#28e3df",outline="#174c5a")
        for obj in room["objects"]:
            x,y=obj["cell"];cx=gx+(x+.5)*tile;cy=gy+(y+.5)*tile;r=max(2,tile//3)
            kind=obj["type"]
            if kind=="enemy":d.ellipse([cx-r,cy-r,cx+r,cy+r],fill="#b32535",outline="#fff0d5")
            elif kind=="chest":d.rectangle([cx-r,cy-r,cx+r,cy+r],fill="#ffd141",outline="#5b4310")
            elif kind=="checkpoint":
                pts=[(cx,cy-r-1),(cx+r+1,cy),(cx,cy+r+1),(cx-r-1,cy)]
                d.polygon(pts,fill="#fff143",outline="#745b05")
            else:d.rectangle([cx-r,cy-r,cx+r,cy+r],fill="#4d3d2d",outline="#dfbd81")
        if "boss" in s:
            x1,y1,x2,y2=s["boss"]["entrance_gate_rect"]
            d.rectangle([gx+x1*tile,gy+y1*tile,gx+(x2+1)*tile-1,gy+(y2+1)*tile-1],fill="#ab66c5")
        d.text((ox,oy+24*tile+49),f"Batch {s['batch']:02} | {len(s['chests'])} chest(s)",font=font(12),fill="#b7c4d1")
    y=im.height-24
    d.text((20,y),"Red: enemy/pad  |  Gold square: chest  |  Yellow diamond: save  |  Cyan: arrival  |  Purple: boss gate",font=font(13),fill="#d8e1e8")
    path.parent.mkdir(parents=True,exist_ok=True);im.save(path)


if __name__=="__main__":
    manifest=json.loads((BASE/"chapter_manifest.json").read_text(encoding="utf-8"))
    # Batches put their attached optional room beside the relevant main-route segment.
    render([rid for batch in manifest["batches"] for rid in batch["rooms"]],PREVIEW/"chapter_atlas.png",8,4)
    render(manifest["batches"][0]["rooms"],PREVIEW/"batch_01_opening.png",14,2)
    print(f"Rendered chapter atlas and opening-batch preview in {PREVIEW}")
