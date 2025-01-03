from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
from room_reserve.models import Event  # Import modelu Event

@login_required
def my_excel_import(request):
    data = []

    if request.method == "POST" and "excelfile" in request.FILES:
        # Przetwarzanie pliku Excel przy użyciu Pandas
        excel_file = request.FILES["excelfile"]
        df = pd.read_excel(excel_file)  # Wczytaj plik Excel do DataFrame

        # Konwersja danych do listy słowników
        for _, row in df.iterrows():
            data.append({
                "nazwa": row.get("nazwa", ""),
                "nazwa_ang": row.get("nazwa_ang", ""),
                "data": row.get("data", "").strftime("%Y-%m-%d") if pd.notnull(row.get("data")) else "",
                "godzina_rozpoczecia": row.get("godzina_rozpoczecia", "").strftime("%H:%M:%S") if pd.notnull(row.get("godzina_rozpoczecia")) else "",
                "godzina_zakonczenia": row.get("godzina_zakonczenia", "").strftime("%H:%M:%S") if pd.notnull(row.get("godzina_zakonczenia")) else "",
                "nazwa_wydarzenia": row.get("nazwa_wydarzenia", ""),
            })

    elif request.method == "POST" and "save_data" in request.POST:
        # Zapisanie danych do bazy
        rows = zip(
            request.POST.getlist("nazwa"),
            request.POST.getlist("nazwa_ang"),
            request.POST.getlist("data"),
            request.POST.getlist("godzina_rozpoczecia"),
            request.POST.getlist("godzina_zakonczenia"),
            request.POST.getlist("nazwa_wydarzenia"),
        )

        for row in rows:
            Event.objects.create(
                nazwa=row[0],
                nazwa_ang=row[1],
                data=row[2],
                godzina_rozpoczecia=row[3],
                godzina_zakonczenia=row[4],
                nazwa_wydarzenia=row[5],
            )

        return redirect("my_excel_import")

    return render(request, "pages/calendar/import_excel.html", {"data": data})
