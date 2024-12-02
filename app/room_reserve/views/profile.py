from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def my_profile_view(request):
    return render(request, "pages/profile/my_profile.html")


@login_required
def my_reservations_view(request):
    return render(request, "pages/profile/my_reservations.html")
