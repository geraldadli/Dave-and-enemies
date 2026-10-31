"""Optional font-source rebuild. Requires fontTools; uses supplied local VF only."""
from pathlib import Path
import hashlib
import json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

root = Path(__file__).resolve().parents[1] / 'fonts'
result = []
for style, weight in [('Regular', 400), ('Bold', 700)]:
    f = TTFont(root / 'NotoSans-VF.ttf')
    f = instantiateVariableFont(f, {'wght': weight, 'wdth': 100}, inplace=True, updateFontNames=True)
    p = root / f'NotoSans-{style}.ttf'
    f.save(p)
    check = TTFont(p)
    required = set(range(32, 127)) | {ord(c) for c in '—…’“”×'}
    missing = sorted(required-set(check.getBestCmap()))
    assert not missing, missing
    assert 'fvar' not in check
    assert check['name'].getDebugName(2) == style
    result.append({'file':p.name, 'family':check['name'].getDebugName(1),
                   'style':check['name'].getDebugName(2), 'weight':check['OS/2'].usWeightClass,
                   'variable':False, 'required_glyphs_missing':missing,
                   'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(root / 'FONT_INFO.json').write_text(json.dumps({'upstream':'https://github.com/google/fonts/tree/main/ofl/notosans',
    'license':'OFL.txt', 'instances':result},indent=2),encoding='utf-8')
print('Verified static Regular/Bold names and required glyph coverage.')
