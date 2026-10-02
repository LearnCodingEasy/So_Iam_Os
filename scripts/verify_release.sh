#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python scripts/verify_source.py
python scripts/check_frontend_imports.py
python -m compileall -q backend_django
if command -v npm >/dev/null 2>&1; then
  if [ -d frontend_vue/node_modules ]; then
    npm --prefix frontend_vue run build
    npm --prefix frontend_vue run test:unit -- --run
  else
    echo "SKIP_FRONTEND_RUNTIME=dependencies-not-installed"
  fi
fi
if python - <<'PY'
import importlib.util
mods=['django','rest_framework','channels','celery']
raise SystemExit(0 if all(importlib.util.find_spec(m) for m in mods) else 1)
PY
then
  (cd backend_django && python manage.py check && python manage.py test)
else
  echo "SKIP_DJANGO_RUNTIME=dependencies-not-installed"
fi
