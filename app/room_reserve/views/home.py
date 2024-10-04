from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Widok strony głównej, który wymaga logowania
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"  # Wskazujesz na swój szablon w 'templates/pages/home.html'
    login_url = "account_login"  # Strona logowania
