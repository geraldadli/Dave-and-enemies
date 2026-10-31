"""Read-only source inspection plus explicitly labelled review thumbnails; no engine exports."""
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / 'art' / 'reference'
SOURCES = [
    'art/source/dave/dave_base_down_v001.png',
    'art/source/dave/dave_base_down_v002.png',
    'art/source/icons/spr_icon_potion_health_source_v001.png',
]

reports=[]
for filename in SOURCES:
    path=ROOT/filename
    with Image.open(path) as src:
        im=src.convert('RGBA')
        alpha=im.getchannel('A')
        hist=alpha.histogram()
        header=path.read_bytes()[:26]
        report={
            'file':filename, 'size_px':list(src.size), 'mode':src.mode,
            'png_channel_bit_depth':header[24],
            'png_colour_type':header[25],
            'embedded_icc':bool(src.info.get('icc_profile')),
            'srgb_chunk_present':'srgb' in src.info,
            'alpha_zero_pixels':hist[0], 'alpha_partial_pixels':sum(hist[1:255]),
            'alpha_opaque_pixels':hist[255],
            'alpha_nearly_opaque_250_255_pixels':sum(hist[250:]),
            'alpha_mode_counts':Counter(alpha.get_flattened_data()).most_common(6),
            'nonzero_alpha_bounds':list(alpha.getbbox()) if alpha.getbbox() else None,
            'alpha_128_bounds':list(alpha.point(lambda p:255 if p>=128 else 0).getbbox()),
            'status':'generated_source_not_engine_ready',
        }
        reports.append(report)
(REF/'generated_source_inspection.json').write_text(json.dumps(reports,indent=2)+'\n',encoding='utf-8')

# These are diagnostic resamples only. They are not deliverable sprite frames.
board=Image.new('RGB',(1120,440),'#bda77b')
draw=ImageDraw.Draw(board)
draw.text((20,14),'FIRST BATCH SOURCE REVIEW - thumbnails only; no engine-ready exports',fill='#171719')
for col,(name,height,label) in enumerate([
    (SOURCES[1],78,'Dave v002: 78px silhouette-height preview'),
    (SOURCES[2],58,'Potion v001: 58px silhouette-height preview'),
]):
    im=Image.open(ROOT/name).convert('RGBA'); mask=im.getchannel('A').point(lambda p:255 if p>=128 else 0)
    figure=im.crop(mask.getbbox()); factor=height/figure.height
    native=figure.resize((round(figure.width*factor),height),Image.Resampling.LANCZOS)
    x=20+col*550; draw.text((x,52),label,fill='#171719')
    for i,colour in enumerate(['#cdb986','#292b2d']):
        tile=Image.new('RGBA',(96,96),colour); tile.alpha_composite(native,((96-native.width)//2,88-height))
        board.paste(tile.convert('RGB').resize((192,192),Image.Resampling.NEAREST),(x+i*210,90))
    board.paste(native,(x+165,300),native)
draw.text((20,414),'Crops use alpha>=128 to isolate the main silhouette for QA. Faint stray alpha still needs cleanup.',fill='#171719')
board.save(REF/'first_batch_source_review.png')
print(json.dumps(reports,indent=2))
