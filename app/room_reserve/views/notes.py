from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room_reserve.models import Note, Status
from room_reserve.forms.calendar import NoteForm
from django.http import JsonResponse
import json

from django.utils import timezone


def notes_list(request):
    status_id = request.GET.get("status_id")
    statuses = Status.objects.filter(created_by=request.user)
    notes = Note.objects.filter(owner=request.user).order_by("status", "order")

    context = {
        "notes": notes,
        "statuses": statuses,
        "now": timezone.now(),
    }
    return render(request, "pages/notes/notes.html", context)


@login_required
def add_or_edit_note(request, note_id=None):
    note = None
    if note_id:
        note = get_object_or_404(Note, id=note_id, owner=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.owner = request.user
            new_note.save()
            messages.success(request, "Notatka została zapisana.")
            return redirect("notes_list")
    else:
        form = NoteForm(instance=note)

    statuses = Status.objects.filter(created_by=request.user)

    return render(request, "pages/notes/new_note.html", {
        "form": form,
        "note": note,
        "statuses": statuses,
    })

def update_note_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            note_id = data.get("note_id")
            status_id = data.get("status_id")

            note = Note.objects.get(id=note_id, owner=request.user)
            status = Status.objects.get(id=status_id, created_by=request.user)

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
        data = json.loads(request.body)
        name = data.get("name")
        color = data.get("color")
        if name and color:
            Status.objects.create(name=name, color=color, created_by=request.user)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid data"}, status=400)

def delete_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        status_id = data.get("status_id")
        try:
            status = Status.objects.get(id=status_id, created_by=request.user)
            status.delete()
            return JsonResponse({"success": True})
        except Status.DoesNotExist:
            return JsonResponse({"success": False, "error": "Status not found"}, status=404)
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