# SO_IAM_OS — Local Run & Verification

## 1. Backend

```bash
cd backend_django
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r ../requirements.txt
copy ..\\.env.example ..\\.env.local  # Windows
# or: cp ../.env.example ../.env.local
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver 127.0.0.1:8000
```

Health endpoint:

`GET http://127.0.0.1:8000/api/core/health/`

## 2. Frontend

```bash
cd frontend_vue
npm ci
npm run build
npm run test:unit -- --run
npm run dev
```

The frontend reads:

- `VITE_API_URL` for the Django origin.
- `VITE_API_BASE_URL` for `/api` requests.

## 3. Redis / Celery

For the full background-processing stack, start Redis and then:

```bash
cd backend_django
celery -A backend_django worker -l info
celery -A backend_django beat -l info
```

The local project can still start with SQLite and Django's in-memory Channels layer; production should use PostgreSQL + Redis.

## 4. Production prerequisites

- PostgreSQL
- Redis
- HTTPS reverse proxy
- Environment variables from `.env.example`
- `DATABASE_ENGINE=postgresql`
- `DJANGO_ENV=production`
- `DEBUG=false`
- secure cookies and trusted HTTPS origins

## 5. Validation performed on the packaged source

- Python compilation of the complete Django tree: PASS.
- Secret-file cleanup: PASS.
- Hard-coded frontend LAN API URL removed: PASS.
- Router dashboard path normalized: PASS.
- Automation routes protected by authentication metadata: PASS.
- PrimeVue ConfirmDialog registration corrected: PASS.
- Frontend dependency installation/build could not be executed in the isolated environment because external npm registry access is unavailable. Run the commands above on the development machine before publishing.
- Django runtime tests could not be executed in the isolated environment because Django dependencies are not preinstalled and external PyPI access is unavailable. Run the commands above after dependency installation.
