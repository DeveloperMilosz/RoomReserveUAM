from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room_reserve.models import Note, Status, Group
from room_reserve.forms.calendar import NoteForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import json

from django.utils import timezone


def notes_list(request):
    group_id = request.GET.get("group_id")
    if group_id:
        group = get_object_or_404(Group, id=group_id, members=request.user)
    else:
        group = Group.objects.filter(members=request.user).first()

    if not group:
        messages.info(request, "Nie należysz do żadnej grupy.")
        return redirect("home")  # Zamień na odpowiednią stronę

    statuses = Status.objects.filter(group=group)
    notes = Note.objects.filter(owner=request.user, group=group).order_by("status", "order")

    user_groups = Group.objects.filter(members=request.user)

    context = {
        "notes": notes,
        "statuses": statuses,
        "now": timezone.now(),
        "groups": user_groups,
        "current_group": group,
    }
    return render(request, "pages/notes/notes.html", context)


def add_or_edit_note(request, note_id=None):
    group_id = request.GET.get("group_id")
    group = get_object_or_404(Group, id=group_id, members=request.user) if group_id else None

    if not group:
        messages.error(request, "Grupa nie została określona.")
        return redirect("notes_list")

    note = get_object_or_404(Note, id=note_id, owner=request.user, group=group) if note_id else None

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.owner = request.user
            new_note.group = group
            new_note.save()
            messages.success(request, "Notatka została zapisana.")
            url = reverse('notes_list') + f'?group_id={group.id}'
            return HttpResponseRedirect(url)
    else:
        form = NoteForm(instance=note)

    statuses = Status.objects.filter(group=group)

    return render(request, "pages/notes/new_note.html", {
        "form": form,
        "note": note,
        "statuses": statuses,
        "group": group,
    })


def update_note_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            note_id = data.get("note_id")
            status_id = data.get("status_id")
            group_id = data.get("group_id")

            group = get_object_or_404(Group, id=group_id, members=request.user)
            note = Note.objects.get(id=note_id, owner=request.user, group=group)
            status = Status.objects.get(id=status_id, group=group)

            note.status = status
            note.save()

            return JsonResponse({"success": True})
        except Note.DoesNotExist:
            return JsonResponse({"success": False, "error": "Note not found."}, status=404)
        except Status.DoesNotExist:
            return JsonResponse({"success": False, "error": "Status not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request."}, status=400)


def add_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            color = data.get("color")
            group_id = data.get("group_id")

            group = get_object_or_404(Group, id=group_id, members=request.user)

            if name and color:
                Status.objects.create(name=name, color=color, created_by=request.user, group=group)
                return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid data"}, status=400)

def delete_status(request, status_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            group_id = data.get("group_id")
            status = Status.objects.get(id=status_id, created_by=request.user, group_id=group_id)
            
            Note.objects.filter(status=status).delete()
            status.delete()
            
            return JsonResponse({"success": True})
        except Status.DoesNotExist:
            return JsonResponse({"success": False, "error": "Status not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

 
def save_note_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            notes = data.get("notes", [])
            for note_data in notes:
                note_id = note_data.get("id")
                status_id = note_data.get("status_id")
                order = note_data.get("order")
                note = Note.objects.get(id=note_id, owner=request.user)
                note.status_id = status_id
                note.order = order
                note.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)