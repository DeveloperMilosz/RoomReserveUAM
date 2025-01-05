from room_reserve.models import Room, Event, Lecturers  # Import modeli
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import pandas as pd
from datetime import datetime

@login_required
def my_excel_import(request):
    data = []
    rooms = Room.objects.all()  # Pobieranie wszystkich pokoi
    events = Event.objects.all()  # Pobieranie wszystkich wydarzeń
    lecturers = [
        {"id": lecturer.id, "full_name": f"{lecturer.first_name} {lecturer.last_name}"}
        for lecturer in Lecturers.objects.all()
    ]  # Pobieranie wszystkich wykładowców z pełnym imieniem i nazwiskiem

    if request.method == "POST" and "excelfile" in request.FILES:
        # Przetwarzanie pliku Excel przy użyciu Pandas
        excel_file = request.FILES["excelfile"]
        df = pd.read_excel(excel_file)  # Wczytaj plik Excel do DataFrame

        # Konwersja danych do listy słowników
        for _, row in df.iterrows():
            # Obsługa konwersji godzin
            godzina_rozpoczecia = row.get("godzina_rozpoczecia", "")
            if pd.notnull(godzina_rozpoczecia):
                try:
                    # Jeśli wartość jest czasem w Pandas
                    if isinstance(godzina_rozpoczecia, pd.Timestamp):
                        godzina_rozpoczecia = godzina_rozpoczecia.strftime("%H:%M:%S")
                    else:
                        # Próba parsowania z ciągu
                        godzina_rozpoczecia = datetime.strptime(str(godzina_rozpoczecia), "%H:%M:%S").strftime("%H:%M:%S")
                except ValueError:
                    godzina_rozpoczecia = ""  # Jeśli nie można sparsować, pozostaw puste

            godzina_zakonczenia = row.get("godzina_zakonczenia", "")
            if pd.notnull(godzina_zakonczenia):
                try:
                    if isinstance(godzina_zakonczenia, pd.Timestamp):
                        godzina_zakonczenia = godzina_zakonczenia.strftime("%H:%M:%S")
                    else:
                        godzina_zakonczenia = datetime.strptime(str(godzina_zakonczenia), "%H:%M:%S").strftime("%H:%M:%S")
                except ValueError:
                    godzina_zakonczenia = ""

            data.append({
                "nazwa": row.get("nazwa", ""),
                "nazwa_ang": row.get("nazwa_ang", ""),
                "data": row.get("data", "").strftime("%Y-%m-%d") if pd.notnull(row.get("data")) else "",
                "godzina_rozpoczecia": godzina_rozpoczecia,
                "godzina_zakonczenia": godzina_zakonczenia,
                "nazwa_wydarzenia": row.get("nazwa_wydarzenia", ""),
                "meeting_type": row.get("meeting_type", ""),
                "room": row.get("room", ""),
                "lecturers": row.get("lecturers", ""),
                "color": row.get("color", ""),
            })

    elif request.method == "POST" and "save_data" in request.POST:
        # Zapisanie danych do bazy (bez zmian)
        pass

    return render(request, "pages/calendar/import_excel.html", {"data": data, "rooms": rooms, "events": events, "lecturers": lecturers})
