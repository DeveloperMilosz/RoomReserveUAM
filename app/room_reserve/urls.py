# from http.client import NotConnected
from django.urls import include, path
from django.urls import re_path

from room_reserve.views import home as home_views
from room_reserve.views import auth as auth_views
from room_reserve.views import calendar as calendar_views
from room_reserve.views import rosberrypi_viewer as rosberrypi_views
from room_reserve.views import event_meeting as event_meeting
from room_reserve.views import profile_views
from room_reserve.views import search as search_views
from room_reserve.views import admin_panel as admin_views
from room_reserve.views import test as test_views
from room_reserve.views import mark_notifications as mark_views
from room_reserve.views import notifications_history as history_views

urlpatterns = [
    # Home
    path("", home_views.HomeView.as_view(), name="home"),
    path("accounts/", include("allauth.urls")),
    # Login & Logout
    path("login/", auth_views.login, name="account_login"),
    path("logout/", auth_views.logout, name="account_logout"),
    # Signup
    path("signup/", auth_views.signup, name="account_signup"),
    # Email verification
    path(
        "confirm-email/",
        auth_views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    path(
        "new-confirm-email/",
        auth_views.new_email_verification_sent,
        name="account_new_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        auth_views.confirm_email,
        name="account_confirm_email",
    ),
    # Password reset
    path("password/reset/", auth_views.password_reset, name="account_reset_password"),
    path(
        "password/reset/done/",
        auth_views.password_reset_done,
        name="account_reset_password_done",
    ),
    path("password/change/", auth_views.password_change, name="account_password_change"),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        auth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        auth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
    path("room/<str:room_number>/schedule/", rosberrypi_views.room_schedule_view, name="room_schedule"),
    path("create-event/", event_meeting.create_event_with_meetings, name="create_event_with_meetings"),
    path("get_meetings/", calendar_views.get_meetings, name="get_meetings"),
    path("editmeeting/<int:meeting_id>/", calendar_views.edit_meeting, name="edit_meeting"),
    path("delete_meeting/<int:meeting_id>/", calendar_views.delete_meeting, name="delete_meeting"),
    path("new_meeting/", calendar_views.new_meeting, name="new_meeting"),
    path("new_event/", calendar_views.new_event, name="new_event"),
    path("meeting/<int:meeting_id>/", calendar_views.meeting_details, name="meeting_details"),
    path("event/<int:event_id>/", calendar_views.event_details, name="event_details"),
    path("search/", calendar_views.search_view, name="search_view"),
    path("profil/", profile_views.my_profile_view, name="my_profile"),
    path("reservation/", profile_views.my_reservations, name="my_reservations"),
    path("search/meetings/", search_views.search_meetings, name="search_meetings"),
    path("search/events/", search_views.search_events, name="search_events"),
    path("search/rooms/", search_views.search_rooms, name="search_rooms"),
    path("search/free-rooms/", search_views.search_free_rooms, name="search_free_rooms"),
    path("admin-panel/", admin_views.admin_panel, name="admin_panel"),
    # notifications
    path("notifications/mark-read/", mark_views.mark_notifications_as_read, name="mark_notifications_as_read"),
    path("notifications/history/", history_views.notification_history, name="notification_history"),
    # test notifications
    path("test_notification/", test_views.test_notifications, name="test_notification"),
    path("test-notify-admin/", test_views.test_notify_admin, name="test_notify_admin"),
    path("test-notify-event-approval/", test_views.test_notify_event_approval, name="test_notify_event_approval"),
]
