#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTS = {'.html','.htm','.md','.txt','.json','.jsonld','.js','.ts','.tsx','.jsx','.py','.xml'}
SELF = Path(__file__).resolve()

LITERAL_REPLACEMENTS = {
    'Master Body Piercer': 'Professional Piercer',
    'Master Piercer': 'Professional Piercer',
    'master body piercer': 'professional piercer',
    'master piercer': 'professional piercer',
    'McCarran International Airport': 'Harry Reid International Airport',
    'McCarran Airport': 'Harry Reid International Airport',
    'McCarran': 'Harry Reid International Airport',
    'That is masculine, honest shop talk — no shame, no sales pitch.': "That’s honest shop talk — no shame and no sales pitch.",
    'That is masculine, honest shop talk - no shame, no sales pitch.': "That’s honest shop talk — no shame and no sales pitch.",
    'calm, calm': 'calm',
}

REGEX_REPLACEMENTS = [
    (r'(?is)We use starter jewelry([^<\n]{0,260})', r'We use properly fitted initial jewelry selected for the placement and your anatomy.'),
    (r'(?is)We never use [“\"]starter jewelry[”\"]([^<\n]{0,260})', r'We choose initial jewelry for fit, material, swelling room, and the placement being performed.'),
    (r'(?i)premier authority', 'professional piercer'),
    (r'(?i)pioneered Anatomical Ear Curation', 'focuses on anatomy-aware ear curation'),
    (r'(?i)Best Body Piercer in Las Vegas', 'Professional Piercer in Las Vegas'),
    (r'(?i)surgical precision', 'careful placement'),
    (r'(?i)intensive clinical training', 'professional piercing training'),
    (r'(?i)clinical training', 'professional piercing training'),
    (r'(?i)global conferences', 'continuing education'),
    (r'(?i)clients travel from across the country', 'clients visit from Las Vegas and beyond'),
    (r'(?i)exceeds state health requirements', 'follows Southern Nevada body-art health requirements and studio sanitation protocols'),
]


def rewrite_file(path: Path) -> bool:
    if path.resolve() == SELF or '.github' in path.parts:
        return False
    try:
        s = path.read_text(encoding='utf-8')
    except Exception:
        return False
    old = s

    for a,b in LITERAL_REPLACEMENTS.items():
        s = s.replace(a,b)
    for pat, repl in REGEX_REPLACEMENTS:
        s = re.sub(pat, repl, s)

    s = re.sub(r'\b(?:323|350|400|480)\+?\s+(Google\s+)?reviews\b', 'hundreds of Google reviews', s, flags=re.I)
    s = re.sub(r'\b(?:323|350|400|480)\+\b', 'hundreds', s)

    s = re.sub(r'(?i)\b(?:4|6|8|10)\s*minutes?\s+from\s+Caesars\b', 'a short drive from Caesars; check live traffic for timing', s)
    s = re.sub(r'(?i)\b(?:4|6|8|10)\s*minutes?\s+from\s+Resorts World\b', 'a short drive from Resorts World; check live traffic for timing', s)

    s = re.sub(r'(?i)a straight shot east on Tropicana', 'a short drive from LAS using airport connectors toward Tropicana', s)
    s = re.sub(r'(?is)cabin pressure and dry airplane air change aftercare timing\.?', 'Long sitting, friction, dry cabin air, and limited washing access can make aftercare less convenient when you fly soon after a tattoo.', s)

    s = re.sub(r'(?i)Do not use tea tree oil[^.<]{0,180}unless your piercer tells you otherwise\.?', 'Do not use tea tree oil on a healing piercing.', s)
    s = re.sub(r'(?i)tea tree oil[^.<]{0,120}unless your piercer tells you otherwise\.?', 'tea tree oil on a healing piercing.', s)

    s = re.sub(
        r'(?is)Too shallow\s*\([^)]*\)\s*:\s*blowouts?\s*,\s*rapid fade\s*,\s*patchy heal\.?',
        'Too shallow: pigment may heal faint, patchy, or fall out because too much ink was placed in tissue that continually renews.', s)
    s = re.sub(
        r'(?is)Too shallow\s*:\s*blowouts?\s*,\s*rapid fade\s*,\s*patchy heal\.?',
        'Too shallow: pigment may heal faint, patchy, or fall out because too much ink was placed in tissue that continually renews.', s)
    s = re.sub(
        r'(?is)Too deep\s*([^<\n]{0,180})',
        'Too deep: pigment can spread beyond the intended line, increasing the risk of blurred edges or tattoo blowout and causing unnecessary tissue trauma.', s)
    s = re.sub(
        r'(?i)(upper\s+to\s+mid\s+reticular\s+dermis|1\.5\s*[–-]\s*2\s*mm)',
        'the dermis, with exact working depth varying by body site, skin thickness, technique, and individual anatomy', s)

    rel = path.relative_to(ROOT).as_posix().lower()
    if any(k in rel for k in ('dermis', 'epidermis', 'hypodermis', 'skin_science', 'skin-science')):
        s = re.sub(r'(?is)<section\b[^>]*>.*?Real ear piercing work from our studio[^<]*.*?</section>', '', s)
        s = re.sub(r'(?is)<section\b[^>]*>.*?ear piercing work[^<]*not stock photos.*?</section>', '', s)

    if path.suffix.lower() in {'.html', '.htm', '.json', '.xml', '.md', '.jsonld'} and 'tools' not in path.parts:
        s = s.replace('kmorgen14@gmail.com', 'booking@workofarttattoo.com')
        s = s.replace('thewhiteknight702@gmail.com', 'booking@workofarttattoo.com')

    if s != old:
        path.write_text(s, encoding='utf-8')
        return True
    return False


def main() -> int:
    changed=[]
    for p in ROOT.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXTS:
            continue
        if any(part in {'.git','node_modules','.venv','venv','.github'} for part in p.parts):
            continue
        if rewrite_file(p):
            changed.append(p.relative_to(ROOT).as_posix())

    gitignore = ROOT/'.gitignore'
    existing = gitignore.read_text(encoding='utf-8') if gitignore.exists() else ''
    wanted = ['.DS_Store','__pycache__/','*.pyc']
    add = [x for x in wanted if x not in existing.splitlines()]
    if add:
        gitignore.write_text(existing.rstrip()+('\n' if existing.strip() else '')+'\n'.join(add)+'\n', encoding='utf-8')
        changed.append('.gitignore')

    print('Changed files:', len(changed))
    for x in changed:
        print(x)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
