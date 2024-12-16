from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room_reserve.models import Note, Status
from room_reserve.forms.calendar import NoteForm
from django.http import JsonResponse
import json

@login_required
def notes_list(request):
    """
    Display a list of notes for the logged-in user.
    Supports filtering by status if a `status_id` is passed as a query parameter.
    """
    status_id = request.GET.get("status_id")
    if status_id:
        notes = Note.objects.filter(owner=request.user, status_id=status_id).order_by("deadline")
    else:
        notes = Note.objects.filter(owner=request.user).order_by("deadline")

    statuses = Status.objects.filter(created_by=request.user)

    context = {
        "notes": notes,
        "statuses": statuses,
    }
    return render(request, "pages/notes/notes.html", context)


@login_required
def add_note(request):
    """
    Handle creating a new note.
    """
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            messages.success(request, "Note created successfully!")
            return redirect("notes_list")
    else:
        form = NoteForm()

    context = {
        "form": form,
    }
    return render(request, "pages/notes/new_note.html", context)


@login_required
def edit_note(request, note_id):
    """
    Handle editing an existing note.
    """
    note = get_object_or_404(Note, id=note_id, owner=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully!")
            return redirect("notes_list")
    else:
        form = NoteForm(instance=note)

    context = {
        "form": form,
        "note": note,
    }
    return render(request, "pages/notes/edit_note.html", context)

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