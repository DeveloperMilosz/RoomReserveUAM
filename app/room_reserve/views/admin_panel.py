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
        selected_ids = request.POST.getlist("selected_ids")

        if action in ["approve_selected", "reject_selected"]:
            if not selected_ids:
                messages.error(request, "No items selected.")
                return redirect("admin_panel")

            # Determine model type
            model = Event if item_type == "event" else Meeting if item_type == "meeting" else None
            if not model:
                messages.error(request, "Invalid item type.")
                return redirect("admin_panel")

            # Process selected items
            for item_id in selected_ids:
                item = get_object_or_404(model, id=item_id)
                item.is_approved = action == "approve_selected"
                item.is_rejected = action == "reject_selected"
                item.save()

            action_text = "approved" if action == "approve_selected" else "rejected"
            messages.success(request, f"Selected {item_type}s have been {action_text}.")
            return redirect("admin_panel")

        if action in ["accept_selected", "reject_selected_from_accepted"]:
            if not selected_ids:
                messages.error(request, "No items selected.")
                return redirect("admin_panel")

            # Determine model type
            model = Event if item_type == "event" else Meeting if item_type == "meeting" else None
            if not model:
                messages.error(request, "Invalid item type.")
                return redirect("admin_panel")

            # Accept or reject selected from accepted/rejected
            for item_id in selected_ids:
                item = get_object_or_404(model, id=item_id)
                if action == "accept_selected":
                    item.is_approved = True
                    item.is_rejected = False
                elif action == "reject_selected_from_accepted":
                    item.is_approved = False
                    item.is_rejected = True
                item.save()

            action_text = "accepted" if action == "accept_selected" else "rejected"
            messages.success(request, f"Selected {item_type}s have been {action_text}.")
            return redirect("admin_panel")

    return render(request, "pages/admin/admin_panel.html", {
        "pending_events": pending_events,
        "approved_events": approved_events,
        "rejected_events": rejected_events,
        "pending_meetings": pending_meetings,
        "approved_meetings": approved_meetings,
        "rejected_meetings": rejected_meetings,
    })
