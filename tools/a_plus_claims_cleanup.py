#!/usr/bin/env python3
"""Second-pass claim cleanup for customer-facing/source content."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
EXT={'.html','.htm','.md','.txt','.json','.js','.py'}
LITERAL={
 'medical-grade hygiene':'studio sanitation','medical-grade safety':'professional piercing practices','medical-grade piercing':'professional piercing','medical-grade ear piercing':'professional ear piercing','medical-grade sterilization':'sterilization protocols','medical-grade disinfectants':'professional surface disinfectants','medical-grade infrastructure':'professional sanitation infrastructure','hospital-grade protocols':'studio sterilization protocols','hospital-grade sterilization':'autoclave sterilization','hospital-grade antiseptic':'cleaning chemicals','specific medical-grade options':'specific topical products','medical-grade surgical steel and implant-grade titanium':'quality jewelry selected for fresh-piercing suitability and fit','Sterile Medical Grade Tattoo Station':'Clean Tattoo Station','sterile-medical-grade-tattoo-station':'clean-tattoo-station','precision ear curation and medical-grade piercing':'ear curation and professional piercing'}
PARAGRAPHS=[
(r'(?is)A premium studio invests tens of thousands of dollars in (?:medical-grade|professional sanitation) infrastructure\..*?molecular integrity of the pigments used\.', 'A professional studio invests in cleanable surfaces, hand-washing facilities, single-use supplies, sterilization equipment where reusable instruments are processed, and documented sanitation procedures. The important question is whether the shop can explain its process clearly.'),
(r'(?is)Cheap Strip shops often prioritize turnover over sanitation\..*?walk out immediately\.', 'A low price or busy location does not tell you whether a studio is clean. Look for fresh single-use needles, clean work surfaces, proper barriers, hand hygiene, and clear answers about sterilization and aftercare.'),
(r'(?is)In an industry where safety standards can vary wildly, Katelyn has set a new benchmark for studio sanitation in Las Vegas\..*?(?:Anatometal\.|</p>)', 'Katelyn uses single-use piercing needles and follows the studio’s normal sterilization, surface-disinfection, and jewelry-handling procedures. Placement and initial jewelry are planned around the piercing and the client’s anatomy.</p>')]

def main():
 changed=[]
 for p in ROOT.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in EXT or any(x in p.parts for x in ('.git','.github','node_modules','tools')): continue
  try:s=p.read_text(encoding='utf-8')
  except:continue
  old=s
  for pat,repl in PARAGRAPHS:s=re.sub(pat,repl,s)
  for a,b in LITERAL.items():s=s.replace(a,b).replace(a.title(),b.title())
  if 'katelyn' in p.as_posix().lower():
   s=s.replace("Las Vegas's premier expert in anatomical ear curation, fine line tattoos, and professional piercing","Las Vegas piercer focused on anatomy-aware ear curation, facial and body piercing")
   s=s.replace('specializing in bespoke anatomical ear curation and delicate fine line tattoos','specializing in anatomy-aware ear curation, facial piercing, and body piercing')
   s=s.replace('a sterile environment that exceeds studio sterilization protocols','a clean studio setup using established sterilization and surface-disinfection procedures')
   s=re.sub(r'<span class="material-symbols-outlined[^>]*">(?:earbuds|face_5|vaccines)</span>','',s)
  if s!=old:p.write_text(s,encoding='utf-8');changed.append(p.relative_to(ROOT).as_posix())
 print('Claim-cleanup changed:',len(changed))
 for x in changed:print(x)
 return 0
if __name__=='__main__':raise SystemExit(main())
