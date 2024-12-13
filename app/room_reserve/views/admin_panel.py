from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from room_reserve.models import Event, Meeting

@login_required
@staff_member_required
def admin_panel(request):
    # Query categorized events and meetings
    pending_events = Event.objects.filter(is_approved=False, is_rejected=False)
    approved_events = Event.objects.filter(is_approved=True, is_rejected=False)
    rejected_events = Event.objects.filter(is_approved=False, is_rejected=True)

    pending_meetings = Meeting.objects.filter(is_approved=False, is_rejected=False)
    approved_meetings = Meeting.objects.filter(is_approved=True, is_rejected=False)
    rejected_meetings = Meeting.objects.filter(is_approved=False, is_rejected=True)

    if request.method == "POST":
        item_type = request.POST.get("type")
        action = request.POST.get("action")

        # Approve or reject all items
        if action in ["approve_all", "reject_all"]:
            if item_type == "event":
                items = pending_events
            elif item_type == "meeting":
                items = pending_meetings
            else:
                messages.error(request, "Invalid item type.")
                return redirect("admin_panel")

            for item in items:
                item.is_approved = action == "approve_all"
                item.is_rejected = action == "reject_all"
                item.save()

            action_text = "approved" if action == "approve_all" else "rejected"
            messages.success(request, f"All {item_type}s have been {action_text}.")
            return redirect("admin_panel")

        # Approve or reject a single item
        item_id = request.POST.get("id")
        if item_id:
            if item_type == "event":
                item = get_object_or_404(Event, id=item_id)
            elif item_type == "meeting":
                item = get_object_or_404(Meeting, id=item_id)
            else:
                messages.error(request, "Invalid item type.")
                return redirect("admin_panel")

            if action == "approve":
                item.is_approved = True
                item.is_rejected = False
                messages.success(request, f"{item} approved successfully.")
            elif action == "reject":
                item.is_approved = False
                item.is_rejected = True
                messages.success(request, f"{item} rejected successfully.")
            else:
                messages.error(request, "Invalid action.")
            item.save()
            return redirect("admin_panel")

    return render(request, "pages/admin/admin_panel.html", {
        "pending_events": pending_events,
        "approved_events": approved_events,
        "rejected_events": rejected_events,
        "pending_meetings": pending_meetings,
        "approved_meetings": approved_meetings,
        "rejected_meetings": rejected_meetings,
    })
