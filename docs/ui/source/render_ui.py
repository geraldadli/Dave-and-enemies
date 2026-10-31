"""Rebuild design references, editable SVGs, prototype frame kit, and static QA.

Requires Python 3 + Pillow. Run from any directory. No GameMaker files are edited.
FontTools was used once to make the supplied static Noto Sans instances; not needed here.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from functools import lru_cache
import csv
import hashlib
import html
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'mockups'
ASSETS = ROOT / 'assets'
FONT = ROOT / 'fonts'
S = 2
C = dict(ink='#171B27', raised='#242A39', well='#101521', edge='#747F95',
         gold='#EAC477', text='#F6EBDD', muted='#B9C3D3', disabled='#929DAF',
         health='#C14F5C', boss='#A663C1', xp='#6FB8C9', error='#FFAC9F',
         success='#A5D6A0', sand='#D8BB87', path='#B79567', rock='#82695D')
TEXT_CHECKS = []
PNG_INFO = PngImagePlugin.PngInfo()
PNG_INFO.add(b'sRGB', b'\x00')


@lru_cache(None)
def font(size=23, bold=False, scale=S):
    return ImageFont.truetype(str(FONT / ('NotoSans-Bold.ttf' if bold else 'NotoSans-Regular.ttf')), size*scale)


def measure(t, size=23, bold=False):
    return font(size, bold, 1).getlength(t)


def wrap(t, width, size=23, bold=False):
    lines = []
    for para in t.split('\n'):
        line = ''
        for word in para.split(' '):
            candidate = (line+' '+word).strip()
            if measure(candidate, size, bold) <= width:
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word
                while measure(line, size, bold) > width:
                    i = 1
                    while i < len(line) and measure(line[:i+1], size, bold) <= width:
                        i += 1
                    lines.append(line[:i])
                    line = line[i:]
        lines.append(line)
    return lines


class Canvas:
    def __init__(self, w=1280, h=720, transparent=False):
        self.w, self.h = w, h
        self.im = Image.new('RGBA', (w*S, h*S), (0, 0, 0, 0) if transparent else C['ink'])
        self.d = ImageDraw.Draw(self.im)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
                    '<defs><style>@font-face{font-family:NotoUI;src:url(../fonts/NotoSans-Regular.ttf)}'
                    '@font-face{font-family:NotoUI;src:url(../fonts/NotoSans-Bold.ttf);font-weight:700}'
                    'text{font-family:NotoUI,"Noto Sans",sans-serif}</style></defs>']
        if not transparent:
            self.rect(0, 0, w, h, C['ink'])

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1, radius=0):
        kw = dict(fill=fill, outline=stroke, width=round(sw*S))
        box = (round(x*S), round(y*S), round((x+w)*S), round((y+h)*S))
        if radius:
            self.d.rounded_rectangle(box, radius=round(radius*S), **kw)
        else:
            self.d.rectangle(box, **kw)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')

    def line(self, points, fill, width=1):
        self.d.line([(round(x*S), round(y*S)) for x, y in points], fill=fill, width=round(width*S))
        pts = ' '.join(f'{x},{y}' for x, y in points)
        self.svg.append(f'<polyline points="{pts}" fill="none" stroke="{fill}" stroke-width="{width}"/>')

    def poly(self, pts, fill, stroke=None, sw=1):
        p = [(round(x*S), round(y*S)) for x, y in pts]
        self.d.polygon(p, fill=fill)
        if stroke:
            self.d.line(p+[p[0]], fill=stroke, width=round(sw*S), joint='curve')
        ps = ' '.join(f'{x},{y}' for x, y in pts)
        self.svg.append(f'<polygon points="{ps}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')

    def ellipse(self, x, y, w, h, fill, stroke=None, sw=1):
        self.d.ellipse((round(x*S), round(y*S), round((x+w)*S), round((y+h)*S)), fill, stroke, round(sw*S))
        self.svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')

    def text(self, x, y, t, size=23, color=None, bold=False, align='left', width=None, lh=None):
        color = color or C['text']
        lh = lh or {18:24, 23:30, 28:36, 46:58}.get(size, size*1.3)
        f = font(size, bold)
        a, desc = f.getmetrics()
        baseline = y*S+(lh*S-a-desc)/2+a
        tw = f.getlength(t)/S
        if width is not None:
            TEXT_CHECKS.append(dict(text=t, width=width, measured=round(tw, 2), size=size, pass_fit=tw <= width+0.5))
        dx = x-(tw/2 if align == 'center' else tw if align == 'right' else 0)
        self.d.text((dx*S, baseline), t, fill=color, font=f, anchor='ls')
        anchor = {'left':'start', 'center':'middle', 'right':'end'}[align]
        self.svg.append(f'<text x="{x}" y="{baseline/S}" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{color}">{html.escape(t)}</text>')

    def paragraph(self, x, y, t, width, size=23, color=None, bold=False, max_lines=None):
        lines = wrap(t, width, size, bold)
        if max_lines is not None and len(lines) > max_lines:
            raise ValueError(f'Text overflows {max_lines} lines: {t}')
        lh = 36 if size == 28 else 30 if size == 23 else 24
        for i, tline in enumerate(lines):
            self.text(x, y+lh*i, tline, size, color, bold, width=width)
        return lines

    def dim(self, alpha=0.45):
        overlay = Image.new('RGBA', self.im.size, C['ink'])
        overlay.putalpha(round(alpha*255))
        self.im = Image.alpha_composite(self.im, overlay)
        self.d = ImageDraw.Draw(self.im)
        self.svg.append(f'<rect width="{self.w}" height="{self.h}" fill="{C["ink"]}" opacity="{alpha}"/>')

    def save(self, stem, folder=OUT):
        folder.mkdir(parents=True, exist_ok=True)
        png = self.im.resize((self.w, self.h), Image.Resampling.LANCZOS)
        png.save(folder / f'{stem}.png', pnginfo=PNG_INFO)
        (folder / f'{stem}.svg').write_text('\n'.join(self.svg+['</svg>']), encoding='utf-8')
        return png


def panel(c, x, y, w, h, fill=None, border=None):
    c.rect(x+3, y+5, w, h, C['well'], radius=12)
    c.rect(x, y, w, h, fill or C['ink'], border or C['edge'], 2, 12)
    c.line([(x+16, y+2), (x+w-16, y+2)], '#9098A6', 1)
    for xx, yy, sx, sy in [(x+9,y+9,1,1),(x+w-9,y+9,-1,1),(x+9,y+h-9,1,-1),(x+w-9,y+h-9,-1,-1)]:
        c.line([(xx+sx*6,yy),(xx,yy),(xx,yy+sy*6)], C['gold'], 1)


def focus(c, x, y, w, h, col=None):
    col = col or C['gold']
    c.rect(x+1,y+1,w-2,h-2,None,col,2,8)
    for xx, yy, sx, sy in [(x,y,1,1),(x+w,y,-1,1),(x,y+h,1,-1),(x+w,y+h,-1,-1)]:
        c.line([(xx+sx*10,yy),(xx,yy),(xx,yy+sy*10)],col,3)


def button(c, x, y, w, h, label, state='normal', small=False):
    fill = C['raised'] if state in ('hover','pressed','focus') else C['ink']
    border = C['gold'] if state in ('focus','selected') else C['error'] if state == 'danger' else C['edge']
    c.rect(x,y,w,h,fill,border,2,8)
    if state == 'focus':
        focus(c,x,y,w,h)
    if state == 'selected':
        c.rect(x+w/2-10,y+h-4,20,3,C['gold'])
    color = C['disabled'] if state == 'disabled' else C['text']
    fs = 18 if small else 23
    if label:
        c.text(x+w/2,y+(h-(24 if small else 30))/2+(1 if state=='pressed' else 0),label,fs,color,align='center',width=w-24)
    if state == 'disabled':
        c.line([(x+12,y+h-6),(x+28,y+h-6)], C['disabled'],2)


def icon(c, x, y, kind, size=48):
    # Explicitly schematic art placeholders; not the production item-icon delivery.
    s = size/48
    def r(a,b,w,h,col,stroke=None): c.rect(x+a*s,y+b*s,w*s,h*s,col,stroke,2*s,3*s)
    def p(pts,col): c.poly([(x+a*s,y+b*s) for a,b in pts],col,C['well'],2*s)
    if 'potion' in kind:
        r(18,1,12,10,'#BEA27A',C['well'])
        r(16,10,16,9,'#DBD2BF',C['well'])
        r(10,17,28,28,C['health'],C['well'])
        r(15,21,5,14,'#F4B3A2')
    elif kind in ('longsword','bandit_scimitar','sunsteel_blade'):
        p([(26,3),(35,4),(22,31),(16,27)], '#DCE4ED')
        p([(8,27),(13,23),(29,33),(26,37)], C['gold'])
        p([(13,31),(19,35),(12,46),(6,43)], '#7D5949')
    elif kind in ('worn_tabard','iron_tunic','paladin_mail','wanderer_tunic'):
        p([(13,7),(20,3),(28,3),(35,7),(45,18),(35,24),(34,44),(14,44),(13,24),(3,18)], '#9BA8B8')
        r(20,8,8,29,'#963F4D')
        c.line([(x+16*s,y+34*s),(x+32*s,y+34*s)], C['gold'],2*s)
    elif 'coin' in kind or 'scarab' in kind or 'ankh' in kind:
        c.ellipse(x+7*s,y+6*s,34*s,34*s,C['gold'],C['well'],2*s)
        c.ellipse(x+13*s,y+12*s,22*s,22*s,'#BD8C45',C['well'],1*s)
    elif 'rose' in kind:
        for a in range(5):
            c.ellipse(x+(15+8*math.cos(a*1.26))*s,y+(15+8*math.sin(a*1.26))*s,18*s,18*s,'#C5847D',C['well'],s)
        c.ellipse(x+20*s,y+20*s,8*s,8*s,C['gold'])


def slot(c, x, y, item=None, qty=1, key=None, state='normal', equipped=False):
    c.rect(x,y,72,72,C['raised'] if state=='hover' else C['well'],C['edge'],2,8)
    if item:
        icon(c,x+12,y+8,item)
    else:
        c.line([(x+30,y+36),(x+42,y+36)],'#566176',2)
    if key:
        c.rect(x+3,y+2,22,24,C['ink'],radius=3)
        c.text(x+7,y+2,str(key),18)
    if qty > 1:
        text = f'×{qty}'
        tw = measure(text,18)
        c.rect(x+64-tw-3,y+47,tw+7,23,C['ink'],radius=3)
        c.text(x+64,y+47,text,18,align='right')
    if equipped:
        c.rect(x+47,y+2,22,24,C['ink'],radius=3)
        c.text(x+58,y+2,'E',18,C['gold'],align='center')
    if state in ('selected','focus'):
        focus(c,x,y,72,72)
        if state == 'selected': c.rect(x+26,y+67,20,3,C['gold'])
    if state == 'invalid':
        focus(c,x,y,72,72,C['error'])
    if state == 'carry':
        for yy in (y+5,y+64):
            for xx in range(int(x+8),int(x+64),12):
                c.line([(xx,yy),(xx+6,yy)],C['gold'],2)


def world(c, boss=False):
    c.rect(0,0,1280,720,C['sand'])
    c.poly([(0,464),(310,366),(622,396),(924,254),(1280,310),(1280,442),(920,402),(644,526),(310,502),(0,602)],C['path'])
    c.poly([(0,0),(1280,0),(1280,130),(1140,112),(1080,192),(936,156),(844,112),(730,140),(624,112),(480,164),(296,100),(156,144),(0,112)],C['rock'])
    c.poly([(0,0),(1280,0),(1280,82),(1120,66),(1050,140),(928,112),(830,60),(730,92),(620,64),(480,112),(296,48),(144,92),(0,64)],'#A1886B')
    # Ruined gateway and scattered masonry keep the mockup scene readable.
    for xx in (918,1100):
        c.rect(xx,110,68,158,'#9F8A72',C['rock'],3,5)
        for yy in range(130,260,32): c.line([(xx+2,yy),(xx+66,yy)],C['rock'],2)
    c.rect(904,88,280,48,'#AD967B',C['rock'],3,4)
    for xx,yy in [(120,244),(190,552),(788,566),(1140,380),(432,210)]:
        c.ellipse(xx,yy,56,22,'#B49A74')
        c.poly([(xx+4,yy+12),(xx+12,yy-6),(xx+40,yy-14),(xx+52,yy+8)],'#9F8970',C['rock'],2)
    for xx,yy in [(184,190),(762,210),(1120,546)]:
        c.rect(xx,yy,18,76,'#70846A',C['well'],2,8)
        c.line([(xx+2,yy+38),(xx-14,yy+38),(xx-14,yy+18)],'#536C55',10)
    for i in range(35):
        xx=60+(i*197)%1160; yy=140+(i*131)%448
        c.line([(xx,yy),(xx+10,yy-2)],'#C3A576',2)
    # Tiny Dave silhouette: current art is not a replacement for the contracted sprites.
    c.ellipse(586,416,70,22,'#9C835F')
    c.poly([(606,356),(634,356),(646,418),(594,418)],'#9F3E48',C['well'],2)
    c.ellipse(603,328,34,42,'#BD9258',C['well'],2)
    c.rect(603,370,34,37,'#D2D8DF',C['well'],2,7)
    c.line([(610,407),(608,423)],C['well'],9)
    c.line([(630,407),(632,423)],C['well'],9)
    c.line([(642,386),(671,357)],'#E8E9E5',7)
    if boss:
        c.ellipse(925,321,96,26,'#92764F')
        c.poly([(952,214),(987,214),(1008,315),(928,315)],'#5B5879',C['well'],3)
        c.ellipse(949,188,40,48,'#A79980',C['well'],2)
        c.poly([(942,200),(952,176),(984,176),(1000,222),(981,214),(970,191),(956,214)],C['gold'],C['well'],2)
        c.line([(1008,222),(1010,316)],C['gold'],6)
        c.ellipse(999,207,22,22,C['boss'],C['well'],2)


def health(c, boss=False):
    c.rect(24,24,320,56,C['ink'],radius=8)
    c.text(32,24,'HP',18,bold=True)
    c.text(336,24,'104 / 140',18,align='right')
    c.rect(24,48,320,32,C['well'],C['edge'],2,8)
    c.rect(32,56,304*104/140,16,C['health'],radius=4)
    if boss:
        # Opaque name plate so the label reads against either sand or ruins.
        c.rect(384,24,512,32,C['ink'],radius=8)
        c.text(640,24,'The Undead Pharaoh',23,align='center',width=480)
        c.rect(384,56,512,32,C['well'],C['edge'],2,8)
        c.rect(392,64,496*.72,16,C['boss'],radius=4)


MAIN = [('longsword',1),('potion_health',5),('potion_greater',2),('worn_tabard',1),('ancient_coin',3),(None,1),(None,1),(None,1)]


def hotbar(c, selected=1):
    for i,(it,q) in enumerate(MAIN):
        slot(c,324+80*i,624,it,q,i+1,'selected' if i==selected else 'normal',i in (0,3))


def portrait(c,x,y,who):
    c.rect(x,y,208,208,C['well'],C['edge'],2,8)
    c.ellipse(x+21,y+10,166,180,'#293445')
    if who=='dave':
        c.poly([(x+20,y+206),(x+34,y+140),(x+78,y+122),(x+144,y+124),(x+187,y+161),(x+199,y+206)],'#A33F4F',C['well'],3)
        c.poly([(x+41,y+206),(x+48,y+153),(x+80,y+137),(x+140,y+145),(x+169,y+182),(x+174,y+206)],'#A9B6C7',C['well'],3)
        c.ellipse(x+61,y+30,94,116,'#BC975B',C['well'],3)
        c.poly([(x+92,y+46),(x+133,y+42),(x+150,y+72),(x+147,y+112),(x+127,y+134),(x+103,y+120),(x+91,y+88)],'#C99D7C',C['well'],2)
        c.poly([(x+59,y+73),(x+66,y+30),(x+117,y+22),(x+148,y+41),(x+111,y+48),(x+90,y+80),(x+87,y+142),(x+65,y+137)],'#C69A54',C['well'],3)
        c.line([(x+124,y+78),(x+138,y+78)],C['well'],3)
        c.line([(x+133,y+108),(x+146,y+105)],'#65443B',2)
        c.line([(x+63,y+168),(x+143,y+184)],'#E3D8BC',3)
    else:
        c.poly([(x+30,y+206),(x+51,y+145),(x+94,y+124),(x+137,y+127),(x+178,y+159),(x+195,y+206)],'#57526B',C['well'],3)
        c.poly([(x+87,y+44),(x+134,y+42),(x+154,y+74),(x+147,y+116),(x+118,y+138),(x+91,y+110)],'#AC9A79',C['well'],3)
        c.poly([(x+30,y+140),(x+52,y+38),(x+94,y+12),(x+143,y+26),(x+183,y+145),(x+152,y+132),(x+126,y+53),(x+91,y+48),(x+70,y+141)],C['gold'],C['well'],3)
        for xx in range(48,72,10): c.line([(x+xx,y+66),(x+xx-12,y+126)],'#40506C',5)
        for xx in range(150,174,10): c.line([(x+xx-13,y+66),(x+xx+7,y+129)],'#40506C',5)
        c.line([(x+116,y+81),(x+139,y+78)],C['well'],5)
        c.line([(x+121,y+113),(x+144,y+108)],C['well'],3)
        c.poly([(x+90,y+145),(x+136,y+145),(x+157,y+174),(x+114,y+192),(x+73,y+173)],C['gold'],C['well'],3)


def inventory(full=False):
    c=Canvas(); world(c); c.dim(.45); panel(c,56,40,1168,560)
    c.text(80,64,'Inventory',28,bold=True)
    button(c,1160,56,40,40,'X',small=True)
    c.text(80,116,'Storage',23)
    c.text(712,116,'Full / 32' if full else '13 / 32',18,C['error'] if full else C['muted'],align='right')
    choices=['potion_health','longsword','gold_coins','iron_tunic','ancient_coin','desert_rose','potion_greater','golden_scarab']
    for r in range(4):
        for col in range(8):
            n=r*8+col
            item=choices[n%8] if full or n<13 else None
            slot(c,80+80*col,152+80*r,item,9 if full and item and ('potion' in item or 'coin' in item) else 2 if n in (0,4,8) else 1,
                 state='focus' if n==0 else 'normal')
    c.text(752,64,'Dave / Level 6',23)
    c.rect(752,104,376,16,C['well'],C['edge'],1,4)
    c.rect(752,104,376*.6,16,C['xp'],radius=4)
    c.text(752,128,'XP 240 / 400',18,C['muted'])
    for x,label,it,name,stat in [(752,'Weapon','longsword','Longsword','Damage 6'),(984,'Armor','worn_tabard','Worn tabard','Defense 2')]:
        c.rect(x,160,216,96,C['raised'],C['edge'],1,8)
        icon(c,x+12,172,it)
        c.text(x+72,170,label,18,C['muted'])
        c.text(x+72,198,name,18,width=132)
        c.text(x+24,228,stat,18,C['muted'])
    c.rect(752,280,448,296,C['well'],C['edge'],1,8)
    c.text(776,304,'Health Potion',23,width=400)
    c.text(776,368,'Consumable / Restores 30 HP',18,C['xp'],width=400)
    c.paragraph(776,400,'Restores 30 health.\nA small comfort for the road.',400,23,max_lines=3)
    button(c,776,528,192,40,'Use'); button(c,984,528,192,40,'Move')
    if full:
        c.paragraph(80,492,'Inventory full. Loot remains here.',632,23,C['error'],max_lines=2)
        for i in range(8): slot(c,324+80*i,624,choices[i],9 if 'potion' in choices[i] or 'coin' in choices[i] else 1,i+1)
    else:
        c.text(80,492,'Select an item to inspect it.',23,C['muted'],width=632)
        hotbar(c)
    c.text(80,556,'Enter Action   M Move   F6 Area   I / Tab Close',18,C['muted'],width=1120)
    return c


def dialogue(who):
    c=Canvas(); world(c,True); health(c)
    panel(c,24,440,1232,256); portrait(c,48,464,who)
    c.text(280,464,'Dave' if who=='dave' else 'The Undead Pharaoh',28,bold=True,width=928)
    t='Step aside.' if who=='dave' else 'You shall not pass. This desert will be your grave.'
    c.paragraph(280,512,t,928,28,max_lines=2)
    c.text(280,648,'Enter / Space / LMB  Continue',18,C['muted'])
    return c


def saves(load=False):
    c=Canvas(); world(c); c.dim(.65); panel(c,208,72,864,600)
    c.text(232,96,'Load Game' if load else 'Save Game',46,bold=True)
    button(c,752,112,132,36,'Save','disabled' if load else 'selected',True)
    button(c,896,112,132,36,'Load','selected' if load else 'normal',True)
    for i in range(3):
        y=192+128*i
        c.rect(260,y,760,120,C['raised'] if i==0 else C['well'],C['gold'] if i==0 else C['edge'],2,12)
        if i==0: focus(c,260,y,760,120)
        c.text(284,y+18,str(i+1),28,bold=True)
        c.text(332,y+16,["Pharaoh’s Gate",'Oasis Refuge','Empty slot'][i],23,C['disabled'] if load and i==2 else C['text'],width=664)
        c.text(332,y+56,['Level 6 / 01:42:18 / 31 Oct 2026 13:05','Level 3 / 00:38:04 / 31 Oct 2026 11:58','No saved journey' if load else 'Start a new save here'][i],18,C['muted'],width=664)
        c.text(332,y+88,'Selected' if i==0 else 'Unavailable in Load mode' if load and i==2 else '',18,C['gold'] if i==0 else C['disabled'],width=664)
    c.text(232,584,'Select a journey to load.' if load else 'Saving at a checkpoint restores health.',18,C['muted'],width=632)
    button(c,232,608,160,40,'Back'); button(c,888,608,160,40,'Load' if load else 'Save')
    return c


def overwrite():
    c=saves(); c.dim(.60); panel(c,384,216,512,288)
    c.text(408,240,'Overwrite slot 1?',28,bold=True,width=464)
    c.paragraph(408,288,'This will replace your save at\nPharaoh’s Gate.',464,23,max_lines=2)
    c.text(408,376,'Saved 31 Oct 2026 13:05',18,C['muted'],width=464)
    button(c,408,432,216,48,'Cancel','focus'); button(c,648,432,224,48,'Overwrite','danger')
    return c


def pause():
    c=Canvas(); world(c); c.dim(.65); panel(c,440,88,400,544)
    c.text(464,112,'Paused',46,bold=True,width=352)
    labels=['Resume','Settings','Save Game','Load Game','Main Menu','Quit Game']
    for i,label in enumerate(labels):
        button(c,464,200+60*i,352,48,label,'focus' if i==0 else 'disabled' if i==2 else 'normal')
    c.text(464,580,'Save at a checkpoint.',18,C['disabled'],width=352)
    return c


def settings():
    c=Canvas(); world(c); c.dim(.65); panel(c,208,72,864,600)
    c.text(232,96,'Settings',46,bold=True)
    for i,(label,val) in enumerate([('Music',70),('Sound effects',80),('Dialogue blips',65)]):
        y=188+64*i
        c.text(232,y+8,label,23,width=280)
        if i==0: focus(c,526,y-4,372,56)
        c.rect(536,y+14,352,20,C['well'],C['edge'],1,6)
        c.rect(536,y+14,352*val/100,20,C['gold'],radius=6)
        c.rect(536+352*val/100-12,y+8,24,32,C['text'],C['well'],2,5)
        c.text(1048,y+8,f'{val}%',23,align='right')
    for i,(label,val) in enumerate([('Reduced flash','Off'),('Screen shake','On'),('Window mode','Windowed')]):
        y=380+64*i
        c.text(232,y+8,label,23,width=280)
        button(c,536,y,352,48,val)
        c.text(552,y+12,'<',18,C['muted']); c.text(872,y+12,'>',18,C['muted'],align='right')
    c.text(232,608,'Left/Right Adjust   Enter Toggle',18,C['muted'],width=632)
    button(c,888,608,160,40,'Back')
    return c


def game_over():
    c=Canvas(); world(c); c.dim(.88)
    c.text(640,152,'Game Over',46,bold=True,align='center')
    c.text(640,220,'The sands keep their secrets.',23,C['muted'],align='center')
    c.text(640,268,'Last checkpoint: Pharaoh’s Gate',18,C['muted'],align='center')
    for i,label in enumerate(['Return to Last Checkpoint','Load Game','Main Menu']):
        button(c,384,328+72*i,512,56,label,'focus' if i==0 else 'normal')
    return c


def ending():
    c=Canvas()
    c.poly([(0,580),(256,534),(488,572),(800,548),(1060,574),(1280,520),(1280,720),(0,720)],'#252735')
    c.poly([(0,644),(300,610),(600,640),(1010,600),(1280,640),(1280,720),(0,720)],'#34303B')
    # Low-contrast arch silhouette is a background placeholder for spr_ending_bg.
    c.rect(934,200,84,374,'#282A38',radius=4)
    c.rect(1140,200,84,374,'#282A38',radius=4)
    c.rect(918,168,322,64,'#30313F',radius=8)
    for xx in (950,1156):
        for yy in (260,340,420,500): c.line([(xx,yy),(xx+50,yy)],'#373847',2)
    c.line([(448,140),(832,140)],C['gold'],1)
    c.text(640,168,'CHAPTER I',18,C['gold'],align='center')
    c.text(640,216,'To Be Continued',46,bold=True,align='center',width=1104)
    c.text(640,296,'Beyond the desert, the search goes on.',23,C['muted'],align='center',width=1104)
    button(c,448,432,384,56,'Main Menu','focus')
    c.text(640,520,'Your journey continues in the next chapter.',18,C['muted'],align='center')
    return c


def states():
    c=Canvas(); c.text(48,32,'One component language',46,bold=True)
    c.text(48,104,'72 px slots / 48 px icons / 18 px keycaps and quantities',23,C['muted'])
    entries=[('Normal','normal'),('Hover','hover'),('Selected','selected'),('Keyboard focus','focus'),('Move source','carry'),('Invalid target','invalid')]
    for i,(label,state) in enumerate(entries):
        x=48+200*i
        slot(c,x,176,'potion_health',5,state=state)
        c.text(x,264,label,18,C['muted'],width=180)
    slot(c,48,336,key=8); c.text(144,352,'Empty / retains the same hit area',23,width=1000)
    slot(c,48,432,'longsword',equipped=True); c.text(144,448,'Equipped / references one of the 40 storage entries',23,width=1000)
    button(c,48,568,216,48,'Normal'); button(c,288,568,216,48,'Focused','focus')
    button(c,528,568,216,48,'Pressed','pressed'); button(c,768,568,216,48,'Disabled','disabled')
    c.text(48,648,'Disabled controls keep a readable label and a reason; they never activate.',18,C['disabled'],width=1184)
    return c


SCREENS = [
    ('01_gameplay','Gameplay / quiet HUD',lambda: gameplay(False),[
        'A  HP group (24,24), 320 × 56. No XP, level, coins, or quest widgets.',
        'B  Eight 72 px main slots at y=624. 8 px gaps; complete row width 632 px.',
        'C  Left-click selects a slot; Q uses a consumable. I / Tab or right-click opens inventory.']),
    ('02_boss','Boss encounter',lambda: gameplay(True),[
        'A  Boss name and health centered at the top; HP and eight main slots remain visible.',
        'B  Boss frame (384,56), 512 × 32. Fill tint differs from Dave HP; no new permanent meters.',
        'C  No dialogue panel during combat. Defeat holds zero, hides UI during the slow fade.']),
    ('03_inventory','Inventory / 32 additional slots',lambda: inventory(False),[
        'A  Panel (56,40), 1168 × 560; 8 × 4 storage grid at (80,152), not including the hotbar.',
        'B  Level, XP, equipment, description, and contextual actions live inside inventory.',
        'C  Main row stays at (324,624); combat pauses. Keyboard F6 changes focus area.']),
    ('04_inventory_full','Inventory / full feedback',lambda: inventory(True),[
        'A  Full means all 40 entries occupied with no compatible stack capacity.',
        'B  Feedback names the outcome: Inventory full. Loot remains here. No item is discarded.',
        'C  Rearranging, equipping, consuming, and closing stay available when full.']),
    ('05_dialogue_dave','Dialogue / Dave',lambda: dialogue('dave'),[
        'A  Panel (24,440), 1232 × 256. Portrait at (48,464), exactly 208 × 208.',
        'B  28 px dialogue in 928 × 80 viewport. First press reveals; next press advances.',
        'C  Hotbar is hidden and has no input. Portrait shown is a schematic placeholder.']),
    ('06_dialogue_pharaoh','Dialogue / The Undead Pharaoh',lambda: dialogue('pharaoh'),[
        'A  Same left portrait position for every speaker. Source portrait faces right toward text.',
        'B  Exact boss_intro text is drawn as editable text; no words baked into portrait art.',
        'C  Combat and boss health activate only after the completed or safely skipped exchange.']),
    ('07_save','Save / three slots',lambda: saves(False),[
        'A  Exactly three 760 × 120 cards. Locations, level, playtime, and local save date stay editable.',
        'B  Select a card, then Save. Occupied slot opens a separate overwrite confirmation.',
        'C  Save available at checkpoints. Successful save restores health; busy write locks controls.']),
    ('08_load','Load / empty slot disabled',lambda: saves(True),[
        'A  Same three-slot layout. Empty and invalid saves show readable status and cannot load.',
        'B  Load from an active session confirms unsaved progress loss; failure preserves menu focus.',
        'C  With no valid saves, focus Back and disable Load. No automatic deletion or fourth slot.']),
    ('09_overwrite','Confirmation / safe default',overwrite,[
        'A  Confirmation (384,216), 512 × 288, traps input over its dimmed caller.',
        'B  Cancel receives first focus. Opening Enter must be released before either action fires.',
        'C  Overwrite uses an explicit destructive label. Esc / right-click cancels; outside-click does nothing.']),
    ('10_pause','Pause / contextual disabled control',pause,[
        'A  Panel (440,88), 400 × 544. World simulation and playtime stop; all HUD is hidden.',
        'B  Save Game is disabled outside a checkpoint; footer explains why.',
        'C  Child menus return to pause first. Resume requires release before combat accepts input.']),
    ('11_settings','Settings / one hierarchy',settings,[
        'A  Volumes for music, effects, and dialogue blips; sliders support mouse and keyboard.',
        'B  Reduced flash and Screen shake are independent controls; warnings remain readable.',
        'C  Window mode is disabled with a reason if unsupported. Preferences persist independently.']),
    ('12_game_over','Game Over / restore a snapshot',game_over,[
        'A  Three actions: Return to Last Checkpoint, Load Game, Main Menu.',
        'B  Without a checkpoint snapshot, primary label becomes Restart Chapter.',
        'C  No automatic death save. Wait 600 ms and for controls to release before accepting input.']),
    ('13_component_states','Components / interaction states',states,[
        'A  Shared outlines, spacing, and type. Focus differs from persistent selected-slot state.',
        'B  Empty slots keep geometry. Equipped badge references storage rather than adding capacity.',
        'C  Icons are schematic; final item art is 64 px RGBA, drawn at 48 px.']),
    ('14_to_be_continued','Chapter end / To Be Continued',ending,[
        'A  46 px title, restrained hierarchy, one clear Main Menu action.',
        'B  Background is a design placeholder for spr_ending_bg; the Grail is not shown recovered.',
        'C  Fade in for 800 ms, then accept a fresh press. Do not claim a save occurred.']),
]


def gameplay(boss=False):
    c=Canvas(); world(c,boss); health(c,boss); hotbar(c); return c


def annotations(im, title, lines, stem):
    sheet=Image.new('RGBA',(1280,916),C['ink']); sheet.alpha_composite(im,(0,0))
    d=ImageDraw.Draw(sheet)
    d.line([(0,720),(1280,720)],fill=C['gold'],width=2)
    def tx(x,y,t,fs,color,bold=False):
        f=font(fs,bold,1); d.text((x,y),t,font=f,fill=color)
    tx(24,734,title+' / 1280 × 720 GUI',23,C['text'],True)
    for i,t in enumerate(lines):
        if measure(t,18)>1232: raise ValueError('Annotation overflow: '+t)
        tx(24,776+32*i,t,18,C['muted'])
    tx(24,884,'Design reference. All game text stays editable. Scene / portrait / item illustrations are placeholders.',18,C['disabled'])
    sheet.convert('RGB').save(OUT/f'{stem}_annotated.png')


def build_assets():
    # Source art intentionally contains no labels. This is a prototype frame kit, not final painted UI.
    for name,w,h,kind in [
        ('spr_ui_panel',96,96,'panel'),('spr_ui_hp_frame',320,32,'hp'),
        ('spr_ui_hp_fill',320,32,'fill'),('spr_ui_slot',72,72,'slot'),
        ('spr_ui_slot_selected',72,72,'selected'),
        ('spr_ui_save_card',760,120,'card'),('spr_ui_save_card_empty',760,120,'empty'),
        ('spr_ui_button',64,64,'button')]:
        nstates=3 if kind in ('card','empty','button') else 1
        for state in range(nstates):
            c=Canvas(w,h,True)
            fill=C['raised'] if state==1 else C['ink']
            if kind=='panel':
                # 24 px slice-safe border; no corner decoration enters stretchable center.
                c.rect(0,0,w-1,h-1,C['ink'],C['edge'],2,12)
                c.line([(24,2),(w-24,2)],'#9098A6',1)
            elif kind=='hp': c.rect(0,0,w-1,h-1,C['well'],C['edge'],2,8)
            elif kind=='fill': c.rect(0,0,w-1,h-1,C['health'],radius=4)
            elif kind=='slot': c.rect(0,0,71,71,C['well'],C['edge'],2,8)
            elif kind=='selected':
                focus(c,1,1,69,69); c.rect(26,67,20,3,C['gold'])
            elif kind in ('card','empty'):
                c.rect(0,0,w-1,h-1,C['well'] if kind=='empty' and state==0 else fill,C['edge'],2,12)
            else: c.rect(0,0,w-1,h-1,fill,C['edge'],2,8)
            if state==2: c.line([(8,h-3),(w-8,h-3)],C['well'],3)
            c.save(name+(f'_{state:02}' if nstates>1 else ''),ASSETS)


LAYOUT = {
    'metadata': {'canvas':[1280,720], 'safe_margin':24,'coordinate_system':'top-left logical GUI px; rectangles x,y,w,h',
                 'contract':'docs/PROJECT_CONTRACT.md','date':'2026-10-31','kind':'design specification, not runtime schema'},
    'colors':C,
    'fonts': {'family':'Noto Sans','meta':{'px':18,'line':24,'weight':400},'body':{'px':23,'line':30,'weight':400},
              'heading':{'px':28,'line':36,'weight':700},'dialogue':{'px':28,'line':36,'weight':400},'title':{'px':46,'line':58,'weight':700}},
    'sources': {'spr_ui_panel':{'size':[96,96],'nine_slice':[24,24,24,24]},'spr_ui_button':{'size':[64,64],'nine_slice':[16,16,16,16]},
                'spr_ui_hp_frame':{'size':[320,32],'nine_slice':[8,8,8,8]},'spr_ui_hp_fill':{'size':[320,32]},
                'spr_ui_slot':{'size':[72,72]},'spr_ui_slot_selected':{'size':[72,72]},
                'spr_ui_save_card':{'size':[760,120]},'spr_ui_save_card_empty':{'size':[760,120]},
                'spr_portrait_dave':{'size':[512,512],'delivered':False},'spr_portrait_pharaoh':{'size':[512,512],'delivered':False}},
    'rects': {
        'ui.hp.group':[24,24,320,56], 'ui.hp.frame':[24,48,320,32], 'ui.hp.fill':[32,56,304,16],
        'ui.boss.group':[384,24,512,64],'ui.boss.frame':[384,56,512,32],'ui.boss.fill':[392,64,496,16],
        'ui.hotbar':[324,624,632,72], 'ui.feedback':[384,568,512,40],
        'ui.inventory.panel':[56,40,1168,560],'ui.inventory.grid':[80,152,632,312],
        'ui.inventory.close':[1160,56,40,40],'ui.inventory.xp':[752,104,376,16],
        'ui.inventory.weapon':[752,160,216,96],'ui.inventory.armor':[984,160,216,96],
        'ui.inventory.detail':[752,280,448,296],'ui.inventory.description':[776,400,400,114],
        'ui.inventory.primary':[776,528,192,40],'ui.inventory.move':[984,528,192,40],
        'ui.inventory.status':[80,492,632,60],
        'ui.dialogue.panel':[24,440,1232,256],'ui.dialogue.portrait':[48,464,208,208],
        'ui.dialogue.text':[280,512,928,80],'ui.dialogue.narration':[48,496,1160,108],
        'ui.save.panel':[208,72,864,600], 'ui.save.tab_save':[752,112,132,36],'ui.save.tab_load':[896,112,132,36],
        'ui.save.back':[232,608,160,40],'ui.save.primary':[888,608,160,40],
        'ui.confirm.panel':[384,216,512,288],'ui.confirm.cancel':[408,432,216,48],'ui.confirm.accept':[648,432,224,48],
        'ui.pause.panel':[440,88,400,544],'ui.settings.panel':[208,72,864,600],
        'ui.settings.back':[888,608,160,40],'ui.ending.main_menu':[448,432,384,56]},
    'repeated': {
        'hotbar':{'count':8,'start':[324,624],'cell':[72,72],'pitch':[80,0],'item_indices':[0,7]},
        'storage':{'rows':4,'columns':8,'start':[80,152],'cell':[72,72],'pitch':[80,80],'item_indices':[8,39]},
        'save_cards':{'count':3,'start':[260,192],'cell':[760,120],'pitch':[0,128]},
        'pause_buttons':{'count':6,'start':[464,200],'cell':[352,48],'pitch':[0,60]},
        'game_over_buttons':{'count':3,'start':[384,328],'cell':[512,56],'pitch':[0,72]},
        'settings_rows':{'count':6,'start':[232,188],'cell':[816,48],'pitch':[0,64]}},
    'state_notes': {'inventory':'32 extra + same 8 main slots, world paused','dialogue':'hotbar hidden and input disabled',
                    'normal_gameplay':'HP and 8 slots only','boss_combat':'adds boss health only'},
}


def contrast(a,b):
    def lum(x):
        vals=[int(x[i:i+2],16)/255 for i in (1,3,5)]
        vals=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
        return sum(v*w for v,w in zip(vals,[.2126,.7152,.0722]))
    aa,bb=sorted([lum(a),lum(b)])
    return (bb+.05)/(aa+.05)


def qa(images):
    rects=dict(LAYOUT['rects'])
    for name,v in LAYOUT['repeated'].items():
        rows=v.get('rows',1); cols=v.get('columns',v.get('count',1))
        for r in range(rows):
            for col in range(cols):
                rects[f'{name}[{r},{col}]']=[v['start'][0]+col*v['pitch'][0],v['start'][1]+(r if rows>1 else col)*v['pitch'][1],*v['cell']]
    bounds=[]
    for name,(x,y,w,h) in rects.items():
        if not (x>=24 and y>=24 and x+w<=1256 and y+h<=696): bounds.append(name)
    pairs={}
    for fg in ['text','muted','disabled','gold','error','success']:
        for bg in ['ink','raised','well']:
            pairs[f'{fg}_on_{bg}']=round(contrast(C[fg],C[bg]),2)
    # Dave HP labels on the brightest mockup sand are also measured separately.
    pairs['ink_on_sand']=round(contrast(C['ink'],C['sand']),2)
    dialogue_tests=['Step aside.','You shall not pass. This desert will be your grave.','W'*140]
    pages={t:[wrap(t,928,28)[i:i+2] for i in range(0,len(wrap(t,928,28)),2)] for t in dialogue_tests}
    failed=[x for x in TEXT_CHECKS if not x['pass_fit']]
    assets=[]
    for p in sorted(ASSETS.glob('*.png')):
        im=Image.open(p)
        assets.append({'file':p.name,'size':list(im.size),'mode':im.mode,'srgb':im.info.get('srgb')==0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    report={'scope':'Static design checks only. No engine compilation, runtime input, save I/O, or gameplay checks performed.',
            'bounds_checked':len(rects),'bounds_failures':bounds,'text_fit_checks':len(TEXT_CHECKS),'text_fit_failures':failed,
            'contrast_ratios':pairs,'minimum_text_contrast':min(v for k,v in pairs.items() if k!='ink_on_sand'),
            'storage_count':32,'main_count':8,'total_item_entries':40,'save_slots':3,
            'dialogue_wrapping_pages':pages,'mockup_count':len(images),'mockup_sizes':sorted(set(str(i.size) for i in images)),
            'prototype_assets':assets,'scaled_reference_sizes':{'1600x900':[1600,900],'1920x1080':[1920,1080],'2560x1440':[2560,1440],
                                                               '3440x1440':{'content':[2560,1440],'offset':[440,0]},'1280x800':{'content':[1280,720],'offset':[0,40]}}}
    (ROOT/'QA_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    assert not bounds, bounds
    assert not failed, failed
    assert min(pairs.values())>=4.5, pairs
    assert all(x['mode']=='RGBA' for x in assets)
    assert all(x['srgb'] for x in assets)
    print(f'PASS: {len(images)} layouts, {len(rects)} rectangles, {len(TEXT_CHECKS)} text-fit checks, {len(assets)} RGBA prototype sources.')


def asset_manifest():
    rows=[
        ['spr_ui_panel','panel','96x96','0,0','24 all sides','1','P0','supplied prototype','Opaque panel; transparent rounded corners; no labels'],
        ['spr_ui_hp_frame','border','320x32','0,0','8 all sides','1','P0','supplied prototype','Dave bar native; boss destination 512x32; preserve caps'],
        ['spr_ui_hp_fill','bar','320x32','0,0','none','1','P0','supplied prototype','Tint red/purple; clip to destination track; contains no numbers'],
        ['spr_ui_slot','slot border','72x72','0,0','none','1','P0','supplied prototype','Shared by 8 main and 32 extra; icon/key/count drawn separately'],
        ['spr_ui_slot_selected','selection overlay','72x72','0,0','none','1','P0','supplied prototype','Transparent center; gold outline/corners/selected marker'],
        ['spr_ui_button','button','64x64','0,0','16 all sides','3 normal hover pressed','P1','supplied prototype','Individual _00/_01/_02 frames; final default height 48; labels separate'],
        ['spr_ui_save_card','save card','760x120','0,0','none; native destination','3 normal hover pressed','P1','supplied prototype','Never bake location, slot number, metadata, or Selected label'],
        ['spr_ui_save_card_empty','empty save card','760x120','0,0','none; native destination','3 normal hover pressed','P1','supplied prototype','Empty/invalid text remains editable; disabled state via code'],
        ['spr_portrait_dave','portrait','512x512','0,0','draw at 208x208','1 neutral; determined optional','P0','art request; not delivered','Facing right; paladin armor, red cape, long golden-brown hair; bust; 16 px safe source padding'],
        ['spr_portrait_pharaoh','portrait','512x512','0,0','draw at 208x208','1 menace; rage optional','P0','art request; not delivered','Facing right; undead ruler, regal headdress; bust; consistent top-left light; 16 px safe padding'],
        ['spr_icon_potion_health','item icon','64x64','0,0','draw at 48x48','1','P0','art request; not delivered','Red potion; 3 px padding; no baked stack quantity'],
    ]
    for item in ['longsword','bandit_scimitar','sunsteel_blade','worn_tabard','iron_tunic','paladin_mail','wanderer_tunic','gold_coins','desert_rose','golden_scarab','ancient_coin','pharaoh_ankh','potion_greater']:
        rows.append([f'spr_icon_{item}','item icon','64x64','0,0','draw at 48x48','1','P1','art request; not delivered','Contract B9 identifier; centered, 3 px source padding; no text'])
    rows += [
        ['spr_ending_bg','background','1280x720','0,0','native GUI plane','1','P2','art request; not delivered','Low contrast arch/ruin; no title, labels, or recovered Grail'],
        ['NotoSans-Regular.ttf','font','pixel sizes 18,23,28','font metrics','font; never image-scale','Regular','P0','supplied static TTF','OFL.txt included; derived from official variable font wght400 wdth100'],
        ['NotoSans-Bold.ttf','font','pixel sizes 28,46','font metrics','font; never image-scale','Bold','P0','supplied static TTF','Same family, wght700 wdth100; headings and major titles'],
        ['code:portrait_border','drawn border','208x208','GUI top-left','2 px inset','normal','P0','specified; no separate asset ID','Reuse panel edge colors; no baked name'],
        ['code:focus_ring','drawn border','component rectangle','GUI top-left','2 px ring + 4 px ticks','focused','P0','specified; no separate asset ID','Gold with corners; distinct from selected bottom marker'],
        ['code:close','drawn control','40x40','GUI top-left','fixed','normal hover pressed disabled','P0','specified; no separate asset ID','Editable X, 18 px; no sprite necessary'],
        ['code:empty_slot','empty indicator','12x2','slot center','fixed','empty','P0','specified; no separate asset ID','Muted horizontal dash; does not count as an item'],
        ['code:equipment_badge','drawn indicator','22x24','slot local 47,2','fixed','equipped','P1','specified; no separate asset ID','Editable E at 18 px; outline and text, no new storage'],
        ['code:slider','drawn control','352x20 track;24x32 thumb','GUI top-left','fixed','normal focus drag disabled','P1','specified; no separate asset ID','Tinted fill, readable percentage separate'],
    ]
    with (ROOT/'UI_ASSETS.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['asset_id','category','source_size','origin','scaling_or_slice','states','priority','delivery_status','notes']);w.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True); ASSETS.mkdir(exist_ok=True)
    images=[]
    for stem,title,fn,notes in SCREENS:
        im=fn().save(stem); images.append(im)
        annotations(im,title,notes,stem)
    # Overview is a contact sheet only; native/annotated layouts are authoritative for text legibility.
    cols=3; cellw=512; cellh=328
    sheet=Image.new('RGB',(cols*cellw,96+math.ceil(len(images)/cols)*cellh),C['ink'])
    d=ImageDraw.Draw(sheet)
    d.text((20,14),'Dave’s & Enemies / UI design handoff',font=font(28,True,1),fill=C['text'])
    d.text((20,54),'14 layouts / 1280 × 720 reference / open individual annotated PNGs for dimensions',font=font(18,False,1),fill=C['muted'])
    for n,(im,(_,title,_,_)) in enumerate(zip(images,SCREENS)):
        x=(n%cols)*cellw;y=96+(n//cols)*cellh
        sheet.paste(im.resize((512,288),Image.Resampling.LANCZOS).convert('RGB'),(x,y))
        d.text((x+10,y+296),title,font=font(18,False,1),fill=C['text'])
    sheet.save(ROOT/'UI_OVERVIEW.png')
    # Full-size scaling samples for one detailed panel and one ultrawide output.
    images[2].resize((1920,1080),Image.Resampling.LANCZOS).save(OUT/'scaling_inventory_1920x1080.png')
    ultra=Image.new('RGB',(3440,1440),'black')
    ultra.paste(images[0].resize((2560,1440),Image.Resampling.LANCZOS).convert('RGB'),(440,0))
    ultra.save(OUT/'scaling_gameplay_3440x1440.png')
    build_assets(); asset_manifest()
    (ROOT/'UI_LAYOUTS.json').write_text(json.dumps(LAYOUT,ensure_ascii=False,indent=2),encoding='utf-8')
    qa(images)


if __name__=='__main__': main()
