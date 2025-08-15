from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Avg

from courses.models import Course
from portfolio.models import Project
from challenges.models import Challenge, Submission

# Optional imports so the app works even if these models are not present
try:
    from courses.models import Enrollment  # type: ignore
except Exception:  # pragma: no cover
    Enrollment = None  # type: ignore

try:
    from portfolio.models import Review  # type: ignore
except Exception:  # pragma: no cover
    Review = None  # type: ignore


def home(request):
    # Featured = newest published courses
    featured_courses = (
        Course.objects.filter(is_published=True)
        .order_by("-created_at")[:4]
    )

    # Community = newest public projects (+rating & review count)
    community_projects = (
        Project.objects.filter(is_public=True)
        .annotate(
            reviews_count=Count("reviews", distinct=True),
            avg_rating=Avg("reviews__rating"),
        )
        .order_by("-created_at")[:4]
    )

    stats = {
        "published_courses": Course.objects.filter(is_published=True).count(),
        "challenges": Challenge.objects.count(),
        "submissions": Submission.objects.count(),
        "public_projects": Project.objects.filter(is_public=True).count(),
    }

    ctx = {
        "featured_courses": featured_courses,
        "community_projects": community_projects,
        "stats": stats,
    }
    return render(request, "core/home.html", ctx)


def about(request):
    return render(request, "core/about.html")


@login_required
def dashboard(request):
    """Personal dashboard with quick stats and recent activity."""
    user = request.user

    # --- counts for the header cards / checklist
    published_courses_count = Course.objects.filter(is_published=True).count()
    my_courses_count = (
        Enrollment.objects.filter(user=user).count() if Enrollment else 0
    )
    my_projects_count = Project.objects.filter(owner=user).count()
    my_submissions_count = Submission.objects.filter(author=user).count()
    my_reviews_count = (
        Review.objects.filter(reviewer=user).count() if Review else 0
    )

    # --- recent activity lists
    recent_projects = (
        Project.objects.filter(owner=user).order_by("-created_at")[:5]
    )
    recent_submissions = (
        Submission.objects.filter(author=user)
        .select_related("challenge")
        .order_by("-created_at")[:5]
    )
    recent_enrollments = (
        Enrollment.objects.filter(user=user)
        .select_related("course")
        .order_by("-joined_at")[:5]     # IMPORTANT: Enrollment has joined_at
        if Enrollment
        else []
    )

    ctx = {
        "stats": {
            "courses": published_courses_count,
            "my_courses": my_courses_count,
            "my_projects": my_projects_count,
            "my_submissions": my_submissions_count,
            "my_reviews": my_reviews_count,
        },
        "recent_projects": recent_projects,
        "recent_submissions": recent_submissions,
        "recent_enrollments": recent_enrollments,
    }
    return render(request, "core/dashboard.html", ctx)


# Async (bonus)
async def leaderboard(request):
    # ORM in async view will run in threadpool automatically
    top = list(
        Submission.objects.values("author__username")
        .annotate(n=Count("id"))
        .order_by("-n")[:10]
    )
    return render(request, "core/leaderboard.html", {"top": top})


# Error handlers
def bad_request(request, exception):  # 400
    return render(request, "400.html", status=400)

def permission_denied(request, exception):  # 403
    return render(request, "403.html", status=403)

def page_not_found(request, exception):  # 404
    return render(request, "404.html", status=404)

def server_error(request):  # 500
    return render(request, "500.html", status=500)

