from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"  # Podaj nazwę szablonu dla strony głównej
    login_url = "account_login"  # Ustawienia strony logowania
