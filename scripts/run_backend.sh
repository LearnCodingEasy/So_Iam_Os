#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../backend_django"
python manage.py check
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
