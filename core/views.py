from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from challenges.models import Submission

def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")

@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")

# Async (bonus)
async def leaderboard(request):
    # ORM in async view will run in threadpool automatically
    top = list(Submission.objects.values("author__username")
               .annotate(n=Count("id")).order_by("-n")[:10])
    return render(request, "core/leaderboard.html", {"top": top})

# Error handlers
def bad_request(request, exception): return render(request, "400.html", status=400)
def permission_denied(request, exception): return render(request, "403.html", status=403)
def page_not_found(request, exception): return render(request, "404.html", status=404)
def server_error(request): return render(request, "500.html", status=500)
