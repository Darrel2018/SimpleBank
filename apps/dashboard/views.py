from django.shortcuts import render
from apps.authentication.permissions import login_required

@login_required
def dashboard_home(request):
    return render(request, "dashboard/home.html")