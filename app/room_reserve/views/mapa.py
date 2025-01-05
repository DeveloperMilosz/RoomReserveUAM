from django.shortcuts import render
from room_reserve.models import RoomPlan, Meeting
from django.utils.timezone import now
from django.db.models import Exists, OuterRef, Subquery


def building_plan_view(request, building_name, floor):
    current_time = now()

    # Podzapytanie, które znajduje aktualne spotkanie dla pokoju
    current_meeting_query = Meeting.objects.filter(
        room=OuterRef("room"), start_time__lte=current_time, end_time__gte=current_time
    ).values("id")[:1]

    plans = (
        RoomPlan.objects.filter(building_name=building_name, floor=floor)
        .select_related("room")
        .annotate(is_busy=Exists(current_meeting_query), current_meeting_id=Subquery(current_meeting_query))
    )

    # Pobranie aktualnych spotkań
    current_meetings = Meeting.objects.filter(
        start_time__lte=current_time, end_time__gte=current_time, room__in=[plan.room for plan in plans if plan.room]
    ).select_related("room")

    # Oblicz współrzędne etykiet
    for plan in plans:
        label_positions = plan.calculate_label_position()
        for i, shape in enumerate(plan.svg_points):
            try:
                if i < len(label_positions):
                    shape["label_x"] = label_positions[i]["label_x"]
                    shape["label_y"] = label_positions[i]["label_y"]
                    shape["label_x_text"] = label_positions[i]["label_x"] + 10  # Przesunięcie w prawo
                    shape["label_y_text"] = label_positions[i]["label_y"] + 10  # Przesunięcie w dół
                    shape["room_number"] = plan.room.room_number  # Dodano nazwę sali
                else:
                    shape["label_x"] = 0  # Domyślna wartość w przypadku braku współrzędnych
                    shape["label_y"] = 0
                    shape["label_x_text"] = 10
                    shape["label_y_text"] = 10
                    shape["room_number"] = "Brak nazwy"  # Domyślna nazwa sali
            except KeyError as e:
                print(f"Brak klucza {e} w danych SVG dla kształtu: {shape}")

    plan_image = plans.first().plan_image.url if plans.exists() and plans.first().plan_image else None

    return render(
        request,
        "pages/building_plan.html",
        {
            "plans": plans,
            "plan_image": plan_image,
            "building_name": building_name,
            "floor": floor,
            "current_meetings": current_meetings,
        },
    )
