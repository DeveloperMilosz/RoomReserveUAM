from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from room_reserve.notifications import notify_user

User = get_user_model()


def test_notifications(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        message = request.POST.get("message")
        if user_id and message:
            user = User.objects.get(id=user_id)
            notify_user(user=user, message=message, submitted_by=request.user)
        return redirect("test_notification")  # Po wysłaniu przekierowanie na tę samą stronę

    users = User.objects.all()
    return render(request, "test_notification.html", {"users": users})
