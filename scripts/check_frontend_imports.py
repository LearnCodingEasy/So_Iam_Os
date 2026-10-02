from pathlib import Path
import re, sys
root=Path('frontend_vue/src').resolve()
errors=[]
pat=re.compile(r"(?:from\s+|import\s*\(\s*|import\s+)[\"'](@/[^\"']+|\.\.?/[^\"']+)[\"']")

def candidates(base):
    vals=[base, base.with_suffix('.js'), base.with_suffix('.vue'), base.with_suffix('.json'), base/'index.js', base/'index.vue']
    return vals
for p in root.rglob('*'):
    if p.suffix not in {'.js','.vue'}: continue
    text='\n'.join(line for line in p.read_text(encoding='utf-8',errors='replace').splitlines() if not line.lstrip().startswith('//'))
    for spec in pat.findall(text):
        if spec.startswith('@/'): target=root/spec[2:]
        else: target=(p.parent/spec).resolve()
        if not any(x.exists() for x in candidates(target)):
            errors.append(f'{p.relative_to(root)} -> {spec}')
if errors:
    print('UNRESOLVED_LOCAL_IMPORTS')
    print('\n'.join(errors[:100]))
    sys.exit(1)
print('FRONTEND_LOCAL_IMPORTS=PASS')
