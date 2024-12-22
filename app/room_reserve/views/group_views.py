from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from room_reserve.models import Group, Meeting, Event
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
    Widok edycji grupy z przypisywaniem spotkań i wydarzeń.
    """
    group = get_object_or_404(Group, id=group_id)
    invite_link = None  # Domyślny link, jeśli nie zostanie wygenerowany
    available_meetings = Meeting.objects.exclude(assigned_groups=group)  # Spotkania nieprzypisane do grupy
    available_events = Event.objects.exclude(assigned_groups=group).distinct()  # Wydarzenia nieprzypisane do grupy

    # Sprawdzenie, czy użytkownik jest jednym z administratorów
    if request.user not in group.admins.all():
        messages.error(request, "Nie masz uprawnień do edycji tej grupy.")
        return redirect("group_detail", group_id=group.id)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)

        if "assign_meeting" in request.POST:
            # Przypisanie spotkania
            meeting_id = request.POST.get("meeting_id")
            try:
                meeting = Meeting.objects.get(id=meeting_id)
                group.meetings.add(meeting)
                messages.success(request, f"Spotkanie '{meeting.name_pl}' zostało przypisane do grupy.")
            except Meeting.DoesNotExist:
                messages.error(request, "Wybrane spotkanie nie istnieje.")

        elif "assign_event" in request.POST:
            # Przypisanie wydarzenia i jego spotkań
            event_id = request.POST.get("event_id")
            try:
                event = Event.objects.get(id=event_id)
                group.events.add(event)  # Przypisz wydarzenie do grupy
                group.meetings.add(*event.meetings.all())  # Dodaj wszystkie spotkania z wydarzenia
                messages.success(request, f"Wydarzenie '{event.name}' i jego spotkania zostały przypisane do grupy.")
            except Event.DoesNotExist:
                messages.error(request, "Wybrane wydarzenie nie istnieje.")

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

    return render(
        request,
        "pages/groups/edit_group.html",
        {
            "form": form,
            "group": group,
            "invite_link": invite_link,
            "available_meetings": available_meetings,
            "available_events": available_events,
        },
    )


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


@login_required
def request_join_group(request, group_id):
    """
    Widok składania prośby o dołączenie do grupy.
    """
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        group.add_join_request(request.user)
        messages.success(request, "Twoja prośba o dołączenie do grupy została wysłana.")
    else:
        messages.info(request, "Jesteś już członkiem tej grupy.")
    return redirect("group_detail", group_id=group.id)


@login_required
def handle_join_request(request, group_id, user_id, action):
    """
    Widok obsługi próśb o dołączenie do grupy.
    """
    group = get_object_or_404(Group, id=group_id)
    user = get_object_or_404(User, id=user_id)

    # Sprawdzenie, czy użytkownik jest administratorem grupy
    if request.user not in group.admins.all():
        messages.error(request, "Nie masz uprawnień do zarządzania tą grupą.")
        return redirect("group_detail", group_id=group.id)

    if action == "accept":
        group.accept_join_request(user)
        messages.success(request, f"Prośba użytkownika {user.email} została zaakceptowana.")
    elif action == "reject":
        group.reject_join_request(user)
        messages.info(request, f"Prośba użytkownika {user.email} została odrzucona.")

    return redirect("group_detail", group_id=group.id)


@login_required
def remove_member(request, group_id, user_id):
    """
    Widok usuwania członka z grupy.
    """
    group = get_object_or_404(Group, id=group_id)
    member = get_object_or_404(User, id=user_id)

    # Sprawdzenie, czy użytkownik ma uprawnienia do usuwania członków
    if request.user not in group.admins.all() and request.user.user_type != "Admin":
        messages.error(request, "Nie masz uprawnień do usuwania członków z tej grupy.")
        return redirect("group_detail", group_id=group.id)

    # Usunięcie członka
    if member in group.members.all():
        group.remove_member(member)
        messages.success(request, f"Użytkownik {member.email} został usunięty z grupy.")
    else:
        messages.error(request, "Ten użytkownik nie jest członkiem tej grupy.")

    return redirect("group_detail", group_id=group.id)


@login_required
def remove_meeting(request, group_id, meeting_id):
    """
    Widok usuwania spotkania z grupy.
    """
    group = get_object_or_404(Group, id=group_id)
    meeting = get_object_or_404(Meeting, id=meeting_id)

    # Sprawdzenie, czy użytkownik ma uprawnienia do usuwania spotkań
    if request.user not in group.admins.all() and request.user.user_type != "Admin":
        messages.error(request, "Nie masz uprawnień do usuwania spotkań z tej grupy.")
        return redirect("group_detail", group_id=group.id)

    # Usunięcie spotkania
    if meeting in group.meetings.all():
        group.meetings.remove(meeting)
        messages.success(request, f"Spotkanie '{meeting.name_pl}' zostało usunięte z grupy.")
    else:
        messages.error(request, "Wybrane spotkanie nie jest przypisane do tej grupy.")

    return redirect("group_detail", group_id=group.id)


@login_required
def remove_event(request, group_id, event_id):
    """
    Widok usuwania wydarzenia z grupy.
    """
    group = get_object_or_404(Group, id=group_id)
    event = get_object_or_404(Event, id=event_id)

    # Sprawdzenie, czy użytkownik ma uprawnienia do usuwania wydarzeń
    if request.user not in group.admins.all() and request.user.user_type != "Admin":
        messages.error(request, "Nie masz uprawnień do usuwania wydarzeń z tej grupy.")
        return redirect("group_detail", group_id=group.id)

    # Usunięcie wydarzenia
    if event in group.events.all():
        group.events.remove(event)
        group.meetings.remove(*event.meetings.all())  # Usunięcie wszystkich powiązanych spotkań
        messages.success(request, f"Wydarzenie '{event.name}' oraz jego spotkania zostały usunięte z grupy.")
    else:
        messages.error(request, "Wybrane wydarzenie nie jest przypisane do tej grupy.")

    return redirect("group_detail", group_id=group.id)
