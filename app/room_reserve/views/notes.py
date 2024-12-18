from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room_reserve.models import Note, Status
from room_reserve.forms.calendar import NoteForm
from django.http import JsonResponse
import json

from django.utils import timezone

def notes_list(request):
    notes = Note.objects.filter(owner=request.user).order_by("deadline")
    statuses = Status.objects.filter(created_by=request.user)
    return render(request, "pages/notes/notes.html", {
        "notes": notes,
        "statuses": statuses,
        "now": timezone.now(),  # Aktualny czas
    })


@login_required
def add_or_edit_note(request, note_id=None):
    note = None
    if note_id:  # Jeśli edytujemy notatkę
        note = get_object_or_404(Note, id=note_id, owner=request.user)

    if request.method == "POST":  # Obsługa formularza
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.owner = request.user
            new_note.save()
            messages.success(request, "Notatka została zapisana.")
            return redirect("notes_list")
    else:  # Wstępne wypełnienie formularza
        form = NoteForm(instance=note)

    # Pobranie dostępnych statusów stworzonych przez użytkownika
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

            # Ensure note belongs to the logged-in user
            note = Note.objects.get(id=note_id, owner=request.user)
            status = Status.objects.get(id=status_id, created_by=request.user)

            # Update note status
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