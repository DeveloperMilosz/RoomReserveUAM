from django.urls import path

from room_reserve.views import home as home_views

urlpatterns = [
    # Home
    path("", home_views.HomeView.as_view(), name="home"),
]
