from pathlib import Path
import ast
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
py_count = 0
vue_count = 0

for path in ROOT.rglob('*.py'):
    if any(part in {'.venv','node_modules','__pycache__'} for part in path.parts):
        continue
    py_count += 1
    try:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    except Exception as exc:
        errors.append(f'Python syntax: {path}: {exc}')

for path in ROOT.joinpath('frontend_vue/src').rglob('*.vue'):
    vue_count += 1
    text = path.read_text(encoding='utf-8', errors='replace')
    if '<template' in text and '</template>' not in text:
        errors.append(f'Vue template appears unclosed: {path}')

for path in ROOT.joinpath('frontend_vue/src').rglob('*.js'):
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
        if '\x00' in text:
            errors.append(f'Binary/null byte in JS: {path}')
    except OSError as exc:
        errors.append(str(exc))

for path in [ROOT/'frontend_vue/package.json']:
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'JSON: {path}: {exc}')

print(f'Python files checked: {py_count}')
print(f'Vue files checked: {vue_count}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('SOURCE_CHECK=PASS')
