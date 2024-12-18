from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room_reserve.models import Group
from room_reserve.forms.groups import GroupForm  # Zmiana tutaj


@login_required
def my_groups_view(request):
    """Widok wyświetlający grupy użytkownika."""
    user = request.user
    my_groups = user.group_memberships.all()
    admin_groups = user.administered_groups.all()
    return render(request, "pages/groups/my_groups.html", {"my_groups": my_groups, "admin_groups": admin_groups})


@login_required
def create_group_view(request):
    """
    Widok tworzenia nowej grupy.
    """
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)  # Tworzymy obiekt, ale jeszcze go nie zapisujemy
            group.save()  # Zapisujemy obiekt w bazie danych, aby uzyskał ID

            # Dodajemy relacje ManyToMany po zapisaniu obiektu
            group.admins.add(request.user)  # Dodaj użytkownika jako administratora
            group.members.add(request.user)  # Dodaj użytkownika jako członka

            messages.success(request, "Grupa została pomyślnie utworzona.")
            return redirect("my_groups")
        else:
            messages.error(request, "Wystąpił błąd podczas tworzenia grupy.")
    else:
        form = GroupForm()

    return render(request, "pages/groups/create_group.html", {"form": form})
