from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"


def manual_view(request):
    return render(request, "pages/manual.html")
