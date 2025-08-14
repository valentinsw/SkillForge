# core/management/commands/seed_demo.py
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db import transaction

from courses.models import Course, Lesson
try:
    from courses.models import Enrollment
except Exception:
    Enrollment = None

from portfolio.models import Project, Review
from challenges.models import Challenge
try:
    from challenges.models import Submission
except Exception:
    Submission = None


class Command(BaseCommand):
    help = (
        "Seed demo data: users, courses/lessons, challenges(+submissions), "
        "portfolio(+reviews). Safe & idempotent; run with --reset to re-seed."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete demo-owned objects before seeding again.",
        )

    @staticmethod
    def _set(obj, **fields):
        """Assign only existing attributes, staying compatible with your schema."""
        for k, v in fields.items():
            if hasattr(obj, k):
                setattr(obj, k, v)

    @transaction.atomic
    def handle(self, *args, **opts):
        User = get_user_model()

        # --- Users & roles ---------------------------------------------------
        staff_group, _ = Group.objects.get_or_create(name="Staff")

        demo, _ = User.objects.get_or_create(
            username="demo", defaults={"email": "demo@example.com"}
        )
        demo.set_password("DemoPass123!")
        demo.is_active = True
        demo.save()

        staff, _ = User.objects.get_or_create(
            username="staff", defaults={"email": "staff@example.com"}
        )
        staff.is_staff = True
        staff.set_password("StaffPass123!")
        staff.is_active = True
        staff.save()
        staff.groups.add(staff_group)

        if opts["reset"]:
            # Clean only demo/staff data in safe dependency order
            if Submission:
                Submission.objects.filter(author__username__in=["demo", "staff"]).delete()

            Review.objects.filter(reviewer__username__in=["demo", "staff"]).delete()
            Project.objects.filter(owner__username__in=["demo", "staff"]).delete()

            chal_titles = [
                "Blog Engine (CRUD + Auth)",
                "CSV Importer (Validation + Report)",
                "Image Gallery (Uploads + Thumbnails)",
                "JWT Todo API (DRF + Tests)",
            ]
            Challenge.objects.filter(title__in=chal_titles).delete()

            if Enrollment:
                Enrollment.objects.filter(user__username__in=["demo", "staff"]).delete()

            course_slugs = ["django-fundamentals", "python-oop", "rest-apis-with-drf"]
            Lesson.objects.filter(course__slug__in=course_slugs).delete()
            Course.objects.filter(slug__in=course_slugs).delete()

            self.stdout.write(self.style.WARNING("Previous demo data removed."))

        # --- Courses & Lessons ----------------------------------------------
        courses_data = [
            {
                "title": "Django Fundamentals",
                "slug": "django-fundamentals",
                "short_description": "Build a mini study tracker while learning MVT, URLs, views, templates, models, forms, and auth.",
                "description": (
                    "A practical intro to Django 5: project/app layout, URL routing, CBVs, "
                    "template inheritance, ORM relations, forms/validation, messages, and admin."
                ),
                "lessons": [
                    ("Project Setup & MVT", "Create a Django 5 project/app, MVT flow, first view/template."),
                    ("URLs, Views & Templates", "Paths, converters, CBVs vs FBVs, inheritance, static."),
                    ("Models, Migrations & Admin", "FK/M2M, migrations, customizing admin."),
                    ("Forms & Validation", "ModelForm vs Form, server-side validation, CSRF, messages."),
                    ("Auth & Permissions", "Login/register/logout, @login_required, staff checks."),
                ],
            },
            {
                "title": "Python OOP Essentials",
                "slug": "python-oop",
                "short_description": "Classes, inheritance, composition, dataclasses, and SOLID in Django-style examples.",
                "description": (
                    "Encapsulation, inheritance vs composition, dataclasses/value objects, "
                    "and applying SOLID in web apps."
                ),
                "lessons": [
                    ("Classes & Encapsulation", "Constructors, properties, invariants."),
                    ("Inheritance vs Composition", "When to subclass vs delegate; testing."),
                    ("Dataclasses & Value Objects", "Lightweight immutable configs/DTOs."),
                    ("SOLID in Practice", "Refactors reducing coupling, improving maintainability."),
                ],
            },
            {
                "title": "REST APIs with DRF",
                "slug": "rest-apis-with-drf",
                "short_description": "Production-ready APIs: serializers, viewsets, auth, permissions, pagination, tests.",
                "description": (
                    "Serializers, viewsets, routers, filtering, pagination, authentication/permissions, "
                    "OpenAPI schema, and testing."
                ),
                "lessons": [
                    ("Serializers, ViewSets & Routers", "From models to JSON; nested serializers; routing."),
                    ("Auth & Permissions", "Session/Token/JWT; custom permissions; common pitfalls."),
                    ("Filtering & Pagination", "Query params, filter backends, page/cursor pagination."),
                    ("Testing & Schema", "APITestCase, OpenAPI schema, docs & versioning."),
                ],
            },
        ]

        for c in courses_data:
            course, created = Course.objects.get_or_create(
                slug=c["slug"],
                defaults={
                    "title": c["title"],
                    "short_description": c["short_description"],
                    "description": c["description"],
                    "created_by": staff,   # satisfy NOT NULL
                    "is_published": True,
                },
            )
            if not created:
                self._set(
                    course,
                    title=c["title"],
                    short_description=c["short_description"],
                    description=c["description"],
                    is_published=True,
                )
                course.save()

            for idx, (ltitle, lcontent) in enumerate(c["lessons"], start=1):
                lesson, _ = Lesson.objects.get_or_create(course=course, title=ltitle)
                self._set(lesson, content=lcontent, body=lcontent, order=idx)
                lesson.save()

            if Enrollment:
                Enrollment.objects.get_or_create(user=demo, course=course)

        def course_or_fallback(slug):
            obj = Course.objects.filter(slug=slug).first()
            return obj or Course.objects.first()

        # --- Challenges (+ optional Submission) ------------------------------
        challenges_data = [
            {
                "title": "Blog Engine (CRUD + Auth)",
                "prompt": (
                    "Build a basic blog with public post listing and private author CRUD.\n\n"
                    "Requirements:\n"
                    "• Public: post list (paginated), detail, author, created date.\n"
                    "• Private: authors can create/edit/delete their own posts.\n"
                    "• Auth: login/register/logout; @login_required for create/edit/delete.\n"
                    "• Validation: title ≥ 5 chars; body ≥ 50 chars; friendly errors.\n"
                    "• Security: CSRF; object-level permission checks.\n\n"
                    "Acceptance:\n"
                    "1) Anonymous: view only.\n"
                    "2) Owner-only edits/deletes.\n"
                    "3) Tests: list, create, permission denial."
                ),
                "deadline_days": 14,
                "course_slug": "django-fundamentals",
            },
            {
                "title": "CSV Importer (Validation + Report)",
                "prompt": (
                    "CSV importer for Contact(name,email,age) with validation & report.\n\n"
                    "Requirements:\n"
                    "• Upload CSV; parse server-side; limit ≤2MB.\n"
                    "• Validate: email format; age 0–120; name non-empty.\n"
                    "• Show summary and per-row errors; only valid rows create objects.\n\n"
                    "Acceptance:\n"
                    "1) Invalid rows skipped & reported.\n"
                    "2) CSRF + size limit enforced.\n"
                    "3) Tests: valid import; invalid row reported."
                ),
                "deadline_days": 10,
                "course_slug": "python-oop",
            },
            {
                "title": "Image Gallery (Uploads + Thumbnails)",
                "prompt": (
                    "Image gallery with upload, listing, detail, and thumbnails.\n\n"
                    "Requirements:\n"
                    "• Model: Image(title, file, uploaded_by, created_at, is_public).\n"
                    "• Validate file types (PNG/JPG/WebP). Create 400x400 thumbnail.\n"
                    "• Public listing shows public images; private view for owner.\n\n"
                    "Acceptance:\n"
                    "1) Non-owners cannot access private images.\n"
                    "2) Thumbnails on listing, full image on detail.\n"
                    "3) Tests: permission check; thumbnail exists."
                ),
                "deadline_days": 21,
                "course_slug": "django-fundamentals",
            },
            {
                "title": "JWT Todo API (DRF + Tests)",
                "prompt": (
                    "Todo REST API with DRF + JWT.\n\n"
                    "Requirements:\n"
                    "• /todos/ list/create; /todos/<id>/ retrieve/update/delete.\n"
                    "• Per-user data isolation; title ≥3 chars; completed bool.\n"
                    "• Pagination 10; filter completed=true/false.\n\n"
                    "Acceptance:\n"
                    "1) Auth required to create.\n"
                    "2) User cannot access another user's todo.\n"
                    "3) Tests for create/auth, isolation, filter."
                ),
                "deadline_days": 12,
                "course_slug": "rest-apis-with-drf",
            },
        ]

        for ch in challenges_data:
            course_fk = course_or_fallback(ch["course_slug"])
            chal, created = Challenge.objects.get_or_create(
                title=ch["title"],
                defaults={
                    "prompt": ch["prompt"],
                    "deadline": timezone.now() + timedelta(days=ch["deadline_days"]),
                    "course": course_fk,  # satisfy NOT NULL
                },
            )
            if not created:
                self._set(
                    chal,
                    prompt=ch["prompt"],
                    deadline=timezone.now() + timedelta(days=ch["deadline_days"]),
                    course=course_fk,
                )
                chal.save()

            if Submission:
                sub, _ = Submission.objects.get_or_create(author=demo, challenge=chal)
                self._set(
                    sub,
                    text_answer=(
                        "Initial demo submission.\n"
                        "Repo: https://example.com/demo/repo\n"
                        "Notes: meets acceptance criteria."
                    ),
                )
                sub.save()

        # --- Portfolio & Reviews --------------------------------------------
        projects_data = [
            {
                "title": "SkillForge Portal",
                "description": (
                    "Learning portal with courses, coding challenges, and a personal portfolio. "
                    "Includes auth, role-based permissions, Bootstrap UI, REST API, and tests."
                ),
                "repo_url": "https://github.com/valentinsw/SkillForge",
                "live_url": "http://127.0.0.1:8000/",
                "is_public": True,
            },
            {
                "title": "DRF Todo API",
                "description": "JWT-protected Todo backend with filtering, pagination, and tests.",
                "repo_url": "https://example.com/demo/todo-api",
                "live_url": "",
                "is_public": True,
            },
            {
                "title": "Image Gallery",
                "description": "Uploads + thumbnails; public/private visibility; responsive grid.",
                "repo_url": "https://example.com/demo/image-gallery",
                "live_url": "",
                "is_public": True,
            },
        ]

        for p in projects_data:
            proj, _ = Project.objects.get_or_create(owner=demo, title=p["title"])
            self._set(
                proj,
                description=p["description"],
                repo_url=p.get("repo_url"),
                live_url=p.get("live_url"),
                is_public=p.get("is_public", True),
            )
            proj.save()

            # IMPORTANT: supply defaults so NOT NULL fields are set during creation
            rev, created = Review.objects.get_or_create(
                project=proj,
                reviewer=staff,  # your model uses 'reviewer'
                defaults={
                    "rating": 5,
                    "comment": "Solid work. Consider adding CI and badges.",
                },
            )
            if not created:
                self._set(rev, rating=5, comment="Solid work. Consider adding CI and badges.")
                rev.save()

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write(self.style.SUCCESS("Users: demo / DemoPass123!   staff / StaffPass123!"))

