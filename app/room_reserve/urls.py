# from http.client import NotConnected
from django.urls import include, path
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
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
from room_reserve.views import notifications_history
from room_reserve.views import notes as notes_views
from room_reserve.views import group_views
from room_reserve.views import my_excel as excel_views
from room_reserve.views import mapa as mapa_views
from room_reserve.views import mappa as mappa_views

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
    path("edit-event/<int:event_id>/", event_meeting.edit_event_with_meetings, name="edit_event_with_meetings"),
    path("room/<str:room_number>/schedule/", rosberrypi_views.room_schedule_view, name="room_schedule"),
    path("create-event/", event_meeting.create_event_with_meetings, name="create_event_with_meetings"),
    path("get_meetings/", calendar_views.get_meetings, name="get_meetings"),
    path("editmeeting/<int:meeting_id>/", calendar_views.edit_meeting, name="edit_meeting"),
    path("delete_meeting/<int:meeting_id>/", calendar_views.delete_meeting, name="delete_meeting"),
    path("new_meeting/", calendar_views.new_meeting, name="new_meeting"),
    path("new_event/", calendar_views.new_event, name="new_event"),
    path("meeting/<int:meeting_id>/", calendar_views.meeting_details, name="meeting_details"),
    path("event/<int:event_id>/", calendar_views.event_details, name="event_details"),
    path("room/<str:room_number>/", calendar_views.room_details, name="room_details"),
    path("search/", calendar_views.search_view, name="search_view"),
    path("profil/", profile_views.my_profile_view, name="my_profile"),
    path("reservation/", profile_views.my_reservations, name="my_reservations"),
    path("search/meetings/", search_views.search_meetings, name="search_meetings"),
    path("search/events/", search_views.search_events, name="search_events"),
    path("search/rooms/", search_views.search_rooms, name="search_rooms"),
    path("search/free-rooms/", search_views.search_free_rooms, name="search_free_rooms"),
    path("search/groups/", search_views.search_groups, name="search_groups"),
    path("api/search/meetings/", search_views.api_search_meetings, name="api_search_meetings"),
    path("meeting/<int:meeting_id>/cancel/", calendar_views.cancel_meeting, name="cancel_meeting"),
    # odwolanie spotkan
    path("meeting/<int:meeting_id>/cancel/", calendar_views.cancel_meeting, name="cancel_meeting"),
    path("meeting/<int:meeting_id>/restore/", calendar_views.restore_meeting, name="restore_meeting"),
    path("meeting/<int:meeting_id>/edit/", calendar_views.edit_meeting, name="edit_meeting"),
    # notifications
    path("notifications/mark-read/", mark_views.mark_notifications_as_read, name="mark_notifications_as_read"),
    path("notifications/messages/", notifications_history.message_history, name="message_history"),
    path("notifications/alerts/", notifications_history.alert_history, name="alert_history"),
    path("notifications/send/", notifications_history.send_notification, name="send_notification"),
    path("notifications/history/", notifications_history.alert_history, name="notification_history"),  # Dodano tutaj
    # test notifications
    path("test_notification/", test_views.test_notifications, name="test_notification"),
    path("about/", calendar_views.about_view, name="about"),
    # notes
    path("notes/", notes_views.notes_list, name="notes_list"),
    path("notes/add/", notes_views.add_or_edit_note, name="add_note"),
    path("notes/edit/<int:note_id>/", notes_views.add_or_edit_note, name="edit_note"),
    path("api/update_note_status/", notes_views.update_note_status, name="update_note_status"),
    path("api/add_status/", notes_views.add_status, name="add_status"),
    path("api/delete_status/<int:status_id>/", notes_views.delete_status, name="delete_status"),
    path("api/save_note_order/", notes_views.save_note_order, name="save_note_order"),
    # grupy
    path("my-groups/", group_views.my_groups_view, name="my_groups"),
    path("create-group/", group_views.create_group_view, name="create_group"),
    path("group/<int:group_id>/", group_views.group_detail_view, name="group_detail"),
    path("group/<int:group_id>/edit/", group_views.edit_group_view, name="edit_group"),
    path("group/<int:group_id>/add-admin/", group_views.add_admin_view, name="add_admin"),
    path("join-group/<uuid:invite_link>/", group_views.join_group_by_invite, name="join_group"),
    path("group/<int:group_id>/generate-invite/", group_views.generate_invite_link, name="generate_invite_link"),
    path("group/<int:group_id>/request-join/", group_views.request_join_group, name="request_join_group"),
    path(
        "group/<int:group_id>/handle-request/<int:user_id>/<str:action>/",
        group_views.handle_join_request,
        name="handle_join_request",
    ),
    path("group/<int:group_id>/remove-member/<int:user_id>/", group_views.remove_member, name="remove_member"),
    path("group/<int:group_id>/remove-meeting/<int:meeting_id>/", group_views.remove_meeting, name="remove_meeting"),
    path("group/<int:group_id>/remove-event/<int:event_id>/", group_views.remove_event, name="remove_event"),
    path("admin-panel/", admin_views.admin_panel, name="admin_panel"),
    # regulamin
    path("regulamin/", profile_views.terms_conditions_view, name="terms_conditions"),
    path("import_excel/", excel_views.my_excel_import, name="my_excel_import"),
    path("building/<str:building_name>/<int:floor>/", mapa_views.building_plan_view, name="building_plan_view"),
    path("api/room-status/<int:room_id>/", search_views.room_status, name="room_status"),
    path("mapa/1pietro/", mappa_views.mapa_pietro1, name="mapa_pietro1"),
    path("manual/", home_views.manual_view, name="manual"),
    path("api/room-statuses/", mappa_views.RoomStatusesAPIView.as_view(), name="room_statuses"),
    path("mapa/pietro1/", mappa_views.pietro1, name="mapa_pietro1"),
    path("mapa/pietro2/", mappa_views.pietro2, name="mapa_pietro2"),
    path("mapa/parter/", mappa_views.parter, name="mapa_parter"),
    path("api/room-points/", search_views.RoomPointsAPIView.as_view(), name="room_points"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
