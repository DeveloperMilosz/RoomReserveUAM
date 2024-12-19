from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room_reserve.models import Group
from room_reserve.forms.groups import GroupForm
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def group_detail_view(request, group_id):
    """
    Widok szczegółowy grupy.
    """
    group = get_object_or_404(Group, id=group_id)
    return render(request, "pages/groups/group_detail.html", {"group": group})


@login_required
def edit_group_view(request, group_id):
    """
    Widok edycji grupy.
    """
    group = get_object_or_404(Group, id=group_id)

    # Upewnij się, że tylko administrator grupy może ją edytować
    if group.admin != request.user:
        messages.error(request, "Nie masz uprawnień do edycji tej grupy.")
        return redirect("group_detail", group_id=group.id)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupa została pomyślnie zaktualizowana.")
            return redirect("group_detail", group_id=group.id)
        else:
            messages.error(request, "Wystąpił błąd podczas edycji grupy.")
    else:
        form = GroupForm(instance=group)

    return render(request, "pages/groups/edit_group.html", {"form": form, "group": group})


@login_required
def add_admin_view(request, group_id):
    """
    Widok dodawania administratorów do grupy.
    """
    group = get_object_or_404(Group, id=group_id)

    # Sprawdzenie, czy aktualny użytkownik jest jednym z administratorów
    if request.user not in group.admins.all():
        messages.error(request, "Nie masz uprawnień do zarządzania tą grupą.")
        return redirect("group_detail", group_id=group.id)

    if request.method == "POST":
        new_admin_email = request.POST.get("new_admin_email")
        try:
            new_admin = User.objects.get(email=new_admin_email)
            group.add_admin(new_admin)
            group.add_member(new_admin)  # Nowy administrator automatycznie staje się członkiem
            messages.success(request, f"Użytkownik {new_admin.email} został dodany jako administrator.")
        except User.DoesNotExist:
            messages.error(request, "Podany użytkownik nie istnieje.")

    return redirect("group_detail", group_id=group.id)
