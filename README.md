# SkillForge

Micro-learning platform built with Django. Public can browse courses; authenticated users enroll, do challenges, submit solutions, and maintain a portfolio with projects & reviews.

## Quickstart (Local venv)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Demo Roles (optional fixtures)

You can create users in admin and place "staff" users into the **Staff** group created by `python manage.py seed_roles`.

## Tech & Structure

- Django 5, DRF (read-only sample), Bootstrap 5
- Apps: core, accounts, courses, challenges, portfolio, api
- Authentication: login/register/logout
- Public: Home, About, Courses (list/detail)
- Private: Dashboard, Lessons (detail), Challenges (list/detail), Submissions CRUD, Portfolio (Projects CRUD, Reviews CRUD)
- Admin: Customized lists, filters, ordering, inlines, etc.
- Error pages: 400/403/404/500

## Tests

Run tests:

```bash
python manage.py test
```

## Environment

`.env.example` contains development defaults. For deploy, set `DEBUG=0`, proper `ALLOWED_HOSTS` and a `DATABASE_URL` if using PostgreSQL.
