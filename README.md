# SkillForge

A small learning portal built with **Django 5**. It includes:

- Courses (list/detail, optional lessons)
- Coding challenges (list/detail, optional submissions)
- Personal portfolio (projects & reviews)
- Auth (login/register/logout), a simple dashboard, Bootstrap 5 UI
- Read‑only sample REST API (Django REST Framework)
- Basic tests

---

## Quickstart (local)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env               # then edit if you like
python manage.py migrate
python manage.py seed_roles        # create 'Staff' group & sync perms
python manage.py runserver
```

Open: <http://127.0.0.1:8000>

### Optional: demo users & sample content

This creates two users and a handful of courses, challenges, projects, lessons, etc.

```bash
# Add demo content
python manage.py seed_demo

# Or reset and re‑seed safely (idempotent)
python manage.py seed_demo --reset
```

**Demo credentials**

- `demo / DemoPass123!` (regular user)
- `staff / StaffPass123!` (is_staff, in the “Staff” group)

> If you already created a different superuser, you can still log in with that
> account. Demo users are just for quick exploration.

---

## App URLs (high level)

- `/` — Home
- `/about/` — About
- `/dashboard/` — User dashboard (login required)
- `/courses/` — Course list (+ detail)
- `/challenges/` — Challenge list (+ detail; submissions if supported)
- `/portfolio/` — Public projects
- `/portfolio/create/` — Create a project (login required)
- `/api/` — Sample DRF endpoints (read‑only)

---

## Project structure

```
accounts/      # auth views, forms, profile model
api/           # DRF serializers & read-only API views
challenges/    # challenges (+ optional submissions)
config/        # settings, urls, wsgi/asgi
core/          # pages, dashboard, template tags, mgmt commands
courses/       # courses (+ optional lessons, enrollments)
portfolio/     # projects & reviews
static/        # css/js/img
templates/     # django templates
tests/         # basic test suite
manage.py
requirements.txt
```

---

## Environment

`./.env.example` contains sensible development defaults. For production, set:

- `DEBUG=0`
- `ALLOWED_HOSTS=yourdomain.com,localhost`
- Database settings (e.g. `DATABASE_URL`) if using Postgres

Static files are served by Django in development; use a proper server or CDN for production.

---

## Tests

```bash
python manage.py test
```

---

## Notes

- The code is intentionally small and approachable so learners can scan it quickly.
- Some models have optional fields; the seeders only set attributes that exist in your schema.
- If you rename URL names or models, tweak the templates/seeders accordingly.
