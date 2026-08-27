# A+ cleanup unresolved matches

## Master Piercer
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:12:    'Master Piercer': 'Professional Piercer',

## Master Body Piercer
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:11:    'Master Body Piercer': 'Professional Piercer',

## McCarran
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:15:    'McCarran International Airport': 'Harry Reid International Airport',
./tools/a_plus_cleanup.py:16:    'McCarran Airport': 'Harry Reid International Airport',
./tools/a_plus_cleanup.py:17:    'McCarran': 'Harry Reid International Airport',

## 480+
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do

## 323
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:52:    s = re.sub(r'\b(?:323|350|400|480)\+?\s+(Google\s+)?reviews\b', 'hundreds of Google reviews', s, flags=re.I)
./tools/a_plus_cleanup.py:53:    s = re.sub(r'\b(?:323|350|400|480)\+\b', 'hundreds', s)

## 350+
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do

## 400+
./walk_in_tattoos_las_vegas_authority_guide/code.html:1622:<span class="font-label-caps text-[10px] text-on-surface-variant uppercase">Google Reviews (2,400+)</span>
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./skipped_upload_build/walk_in_tattoos_las_vegas_nap_corrected.html:1547:<span class="font-label-caps text-[10px] text-on-surface-variant uppercase">Google Reviews (2,400+)</span>
./skipped_pages_clipboard.html:872:<span class="font-label-caps text-[10px] text-on-surface-variant uppercase">Google Reviews (2,400+)</span>

## masculine, honest shop talk
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:18:    'That is masculine, honest shop talk — no shame, no sales pitch.': "That’s honest shop talk — no shame and no sales pitch.",
./tools/a_plus_cleanup.py:19:    'That is masculine, honest shop talk - no shame, no sales pitch.': "That’s honest shop talk — no shame and no sales pitch.",

## cabin pressure
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:59:    s = re.sub(r'(?is)cabin pressure and dry airplane air change aftercare timing\.?', 'Long sitting, friction, dry cabin air, and limited washing access can make aftercare less convenient when you fly soon after a tattoo.', s)

## starter jewelry
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:24:    (r'(?is)We use starter jewelry([^<\n]{0,260})', r'We use properly fitted initial jewelry selected for the placement and your anatomy.'),
./tools/a_plus_cleanup.py:25:    (r'(?is)We never use [“\"]starter jewelry[”\"]([^<\n]{0,260})', r'We choose initial jewelry for fit, material, swelling room, and the placement being performed.'),

## premier authority
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:26:    (r'(?i)premier authority', 'professional piercer'),

## Best Body Piercer in Las Vegas
./.github/workflows/a-plus-factual-cleanup.yml:43:            for term in 'Master Piercer' 'Master Body Piercer' 'McCarran' '480+' '323' '350+' '400+' 'masculine, honest shop talk' 'cabin pressure' 'starter jewelry' 'premier authority' 'Best Body Piercer in Las Vegas'; do
./tools/a_plus_cleanup.py:28:    (r'(?i)Best Body Piercer in Las Vegas', 'Professional Piercer in Las Vegas'),

