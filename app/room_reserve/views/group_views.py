from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from room_reserve.models import Group
from room_reserve.forms.groups import GroupForm

User = get_user_model()


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
    Widok edycji grupy z możliwością dodawania administratorów, członków i generowania linku zaproszenia.
    """
    group = get_object_or_404(Group, id=group_id)
    invite_link = None  # Domyślny link, jeśli nie zostanie wygenerowany

    # Sprawdzenie, czy użytkownik jest jednym z administratorów
    if request.user not in group.admins.all():
        messages.error(request, "Nie masz uprawnień do edycji tej grupy.")
        return redirect("group_detail", group_id=group.id)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)

        if "add_admin" in request.POST:
            # Dodanie administratora
            new_admin_email = request.POST.get("new_admin_email")
            try:
                new_admin = User.objects.get(email=new_admin_email)
                group.add_admin(new_admin)
                group.add_member(new_admin)  # Nowy administrator automatycznie staje się członkiem
                messages.success(request, f"Użytkownik {new_admin.email} został dodany jako administrator.")
            except User.DoesNotExist:
                messages.error(request, "Podany użytkownik nie istnieje.")

        elif "add_member" in request.POST:
            # Dodanie członka
            new_member_email = request.POST.get("new_member_email")
            try:
                new_member = User.objects.get(email=new_member_email)
                group.add_member(new_member)
                messages.success(request, f"Użytkownik {new_member.email} został dodany jako członek grupy.")
            except User.DoesNotExist:
                messages.error(request, "Podany użytkownik nie istnieje.")

        elif "generate_invite_link" in request.POST:
            # Generowanie nowego linku zaproszenia
            group.generate_invite_link()
            invite_link = request.build_absolute_uri(f"/join-group/{group.invite_link}/")
            messages.success(request, "Nowy link zaproszenia został wygenerowany.")

        elif form.is_valid():
            form.save()
            messages.success(request, "Grupa została pomyślnie zaktualizowana.")
            return redirect("group_detail", group_id=group.id)
        else:
            messages.error(request, "Wystąpił błąd podczas edycji grupy.")

    else:
        form = GroupForm(instance=group)
        if group.invite_link:
            invite_link = request.build_absolute_uri(f"/join-group/{group.invite_link}/")

    return render(request, "pages/groups/edit_group.html", {"form": form, "group": group, "invite_link": invite_link})


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


@login_required
def join_group_by_invite(request, invite_link):
    """
    Widok umożliwiający dołączenie do grupy za pomocą linku zaproszenia.
    """
    group = get_object_or_404(Group, invite_link=invite_link)

    # Dodaj użytkownika jako członka grupy
    if request.user not in group.members.all():
        group.members.add(request.user)
        messages.success(request, f"Dołączyłeś do grupy: {group.name}.")
    else:
        messages.info(request, "Jesteś już członkiem tej grupy.")

    return redirect("group_detail", group_id=group.id)


@login_required
def generate_invite_link(request, group_id):
    """
    Widok do generowania nowego linku zaproszenia dla grupy.
    """
    group = get_object_or_404(Group, id=group_id)

    # Sprawdzenie, czy użytkownik jest administratorem grupy
    if request.user not in group.admins.all():
        messages.error(request, "Nie masz uprawnień do zarządzania tą grupą.")
        return redirect("group_detail", group_id=group.id)

    # Wygenerowanie nowego linku zaproszenia
    group.generate_invite_link()

    # Generowanie pełnego linku
    invite_link = request.build_absolute_uri(f"/join-group/{group.invite_link}/")

    messages.success(request, f"Nowy link zaproszenia został wygenerowany: {invite_link}")
    return redirect("group_detail", group_id=group.id)
