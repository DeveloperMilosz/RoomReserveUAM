from socket import IP_DROP_MEMBERSHIP
import pandas as pd
import json
from datetime import datetime
from room_reserve.models import Meeting, Room, Event, User, Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def my_excel_import(request):
    data = []
    rooms = Room.objects.all()
    events = Event.objects.all()
    lecturers = User.objects.filter(user_type__in=["Organizer", "Lecturer"])
    groups = Group.objects.all()  # Pobierz wszystkie grupy

    if request.method == "POST" and "excelfile" in request.FILES:
        excel_file = request.FILES["excelfile"]
        try:
            # Wczytanie pliku Excel do DataFrame
            df = pd.read_excel(excel_file)

            # Parsowanie dat i godzin z obsługą różnych formatów
            if "data" in df.columns:
                df["data"] = pd.to_datetime(df["data"], errors="coerce")
            if "godzina rozpoczecia" in df.columns:
                df["godzina rozpoczecia"] = pd.to_datetime(
                    df["godzina rozpoczecia"], format="%H:%M:%S", errors="coerce"
                ).dt.time
            if "godzina zakończenia" in df.columns:
                df["godzina zakończenia"] = pd.to_datetime(
                    df["godzina zakończenia"], format="%H:%M:%S", errors="coerce"
                ).dt.time

            # Usunięcie duplikatów w danych
            df = df.drop_duplicates()

            # Przygotowanie danych do wyświetlenia
            for index, row in df.iterrows():

                data.append(
                    {
                        "index": index,
                        "nazwa": row.get("nazwa", ""),
                        "nazwa_ang": row.get("nazwa_ang", ""),
                        "data": row["data"].strftime("%Y-%m-%d") if pd.notnull(row["data"]) else "",
                        "godzina_rozpoczecia": (
                            row["godzina rozpoczecia"].strftime("%H:%M:%S")
                            if pd.notnull(row["godzina rozpoczecia"])
                            else ""
                        ),
                        "godzina_zakonczenia": (
                            row["godzina zakończenia"].strftime("%H:%M:%S")
                            if pd.notnull(row["godzina zakończenia"])
                            else ""
                        ),
                        "nazwa_wydarzenia": row.get("nazwa_wydarzenia", ""),
                        "meeting_type": row.get("meeting_type", ""),
                        "room": row.get("room", ""),
                        "lecturers": row.get("lecturers", ""),
                        "color": row.get("color", ""),
                        "groups": row.get("groups", ""),  # Dodane pole dla grup
                        "description": row.get("description", ""),  # Dodane pole dla opisu
                    }
                )

        except Exception as e:
            messages.error(request, f"Błąd podczas przetwarzania pliku: {str(e)}")
            return redirect("import_excel")

    elif request.method == "POST" and "save_data" in request.POST:

        try:
            # Zapisanie danych do bazy
            grouped_data = {}

            for key, value in request.POST.items():
                if key.startswith("nazwa_"):
                    index = key.split("_")[-1]
                    grouped_data[index] = {
                        "nazwa": request.POST.get(f"nazwa_{index}"),
                        "nazwa_ang": request.POST.get(f"nazwa_ang_{index}"),
                        "data": request.POST.get(f"data_{index}"),
                        "godzina_rozpoczecia": request.POST.get(f"godzina_rozpoczecia_{index}"),
                        "godzina_zakonczenia": request.POST.get(f"godzina_zakonczenia_{index}"),
                        "nazwa_wydarzenia": request.POST.get(f"nazwa_wydarzenia_{index}"),
                        "meeting_type": request.POST.get(f"meeting_type_{index}"),
                        "room": request.POST.get(f"room_{index}"),
                        "lecturers": request.POST.get(f"lecturers_{index}", ""),
                        "groups": request.POST.get(f"groups_{index}", ""),
                        "color": request.POST.get(f"color_{index}", "#2873FF"),
                        "description": request.POST.get(f"description_{index}", ""),
                    }

            for index, meeting_data in grouped_data.items():
                room = Room.objects.filter(id=meeting_data["room"]).first() if meeting_data["room"] else None
                event = (
                    Event.objects.filter(id=meeting_data["nazwa_wydarzenia"]).first()
                    if meeting_data["nazwa_wydarzenia"]
                    else None
                )

                # Tworzenie obiektu Meeting
                meeting = Meeting.objects.create(
                    name_pl=meeting_data["nazwa"],
                    name_en=meeting_data["nazwa_ang"],
                    start_time=f"{meeting_data['data']} {meeting_data['godzina_rozpoczecia']}",
                    end_time=f"{meeting_data['data']} {meeting_data['godzina_zakonczenia']}",
                    meeting_type=meeting_data["meeting_type"],
                    room=room,
                    event=event,
                    color=meeting_data["color"],
                    description=meeting_data["description"],
                    is_rejected=False,
                    is_excel=True,
                )

                # Dodanie wykładowców (ManyToMany)
                if meeting_data["lecturers"]:
                    lecturer_ids = [id.strip() for id in meeting_data["lecturers"].split(",") if id.strip().isdigit()]
                    lecturers = User.objects.filter(id__in=lecturer_ids)
                    meeting.lecturers.set(lecturers)

                # Dodanie grup (ManyToMany)
                if meeting_data["groups"]:
                    group_ids = [id.strip() for id in meeting_data["groups"].split(",") if id.strip().isdigit()]
                    groups = Group.objects.filter(id__in=group_ids)
                    meeting.assigned_groups.set(groups)

                meeting.save()

            messages.success(request, "Dane zostały pomyślnie zapisane.")
            return redirect("import_excel")

        except Exception as e:
            messages.error(request, f"Błąd podczas zapisywania danych: {str(e)}")
            return redirect("import_excel")

    return render(
        request,
        "pages/calendar/import_excel.html",
        {"data": data, "rooms": rooms, "events": events, "lecturers": lecturers, "groups": groups},
    )
