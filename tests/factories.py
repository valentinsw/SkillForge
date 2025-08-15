from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

from courses.models import Course, Lesson, Enrollment
from challenges.models import Challenge, Submission
from portfolio.models import Project, Review

User = get_user_model()


def _unique_username(base: str) -> str:
    """
    Ensure username is unique in the test DB.
    Keeps 'base' if free; otherwise appends a counter.
    """
    if not User.objects.filter(username=base).exists():
        return base
    i = 1
    while True:
        cand = f"{base}{i}"
        if not User.objects.filter(username=cand).exists():
            return cand
        i += 1


def create_user(username="user", password="pass1234", is_staff=False, is_superuser=False):
    uname = _unique_username(username)
    u = User.objects.create_user(
        username=uname,
        email=f"{uname}@example.com",
        password=password,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )
    return u


def create_course(title="REST APIs with DRF", created_by=None, is_published=True, slug=None):
    if created_by is None:
        created_by = create_user("author")
    if slug is None:
        slug = slugify(title)
    return Course.objects.create(
        title=title,
        slug=slug,
        short_description="Short",
        description="Long description",
        created_by=created_by,
        is_published=is_published,
    )


def add_lesson(course, title="Intro", order=1):
    return Lesson.objects.create(course=course, title=title, order=order, content="...")


def enroll(user, course):
    return Enrollment.objects.create(user=user, course=course)


def create_challenge(title="Blog Engine", course=None, prompt="Build a blog"):
    """
    Your Challenge model in this repo does not take 'due_date'.
    Also some projects use 'prompt' or 'description' – we set whichever exists.
    """
    if course is None:
        course = create_course()

    fields = {f.name for f in Challenge._meta.get_fields()}

    kwargs = {"title": title, "course": course}
    if "prompt" in fields:
        kwargs["prompt"] = prompt
    elif "description" in fields:
        kwargs["description"] = prompt

    return Challenge.objects.create(**kwargs)


def submit(author=None, challenge=None, score=None, status="submitted"):
    if author is None:
        author = create_user("student")
    if challenge is None:
        challenge = create_challenge()
    return Submission.objects.create(
        author=author,
        challenge=challenge,
        score=score,
        status=status,
    )


def create_project(owner=None, title="My Project", is_public=True):
    if owner is None:
        owner = create_user("owner")
    return Project.objects.create(
        owner=owner,
        title=title,
        description="Project description",
        is_public=is_public,
    )


def review(project=None, reviewer=None, rating=5, comment="Nice job!"):
    if project is None:
        project = create_project()
    if reviewer is None:
        reviewer = create_user("reviewer")
    return Review.objects.create(
        project=project,
        reviewer=reviewer,
        rating=rating,
        comment=comment,
    )
