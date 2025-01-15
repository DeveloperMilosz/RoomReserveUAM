from django.shortcuts import render
from room_reserve.models import Meeting, Event, Room, Group, RoomAttribute
from room_reserve.filters import MeetingFilter, EventFilter, RoomFilter, FreeRoomFilter, GroupFilter
from django.http import JsonResponse
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
import json
from django.conf import settings
from django.db.models import Prefetch
from django.db.models import Q


def search_meetings(request):
    """Wyszukaj spotkania."""
    if request.GET:
        meeting_filter = MeetingFilter(request.GET, queryset=Meeting.objects.all().order_by("start_time"))
    else:
        meeting_filter = MeetingFilter(queryset=Meeting.objects.none())

    return render(request, "pages/search/search_meetings.html", {"filter": meeting_filter})


def search_events(request):
    """Wyszukaj wydarzenia."""
    if request.GET:
        event_filter = EventFilter(request.GET, queryset=Event.objects.all())
    else:
        event_filter = EventFilter(queryset=Event.objects.none())

    # Dodaj URL do logo
    for event in event_filter.qs:
        event.logo_url = event.logo.url if event.logo else None

    return render(request, "pages/search/search_events.html", {"filter": event_filter})


def search_rooms(request):
    """Wyszukaj sale."""
    # Ścieżka do pliku JSON
    json_path = settings.BASE_DIR / "static" / "data" / "punkty.json"

    # Wczytanie danych z pliku JSON
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            points_data = json.load(file)
    except FileNotFoundError:
        return JsonResponse({"error": "Plik punkty.json nie został znaleziony."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Błąd w odczycie pliku punkty.json."}, status=500)

    # Filtrowanie danych na podstawie kryteriów
    if request.GET:
        room_filter = RoomFilter(
            request.GET,
            queryset=Room.objects.prefetch_related(
                Prefetch("attributes", queryset=RoomAttribute.objects.all())
            ).distinct(),
        )
    else:
        room_filter = RoomFilter(queryset=Room.objects.none())

    # Obsługa zapytań AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Pobierz przefiltrowane numery sal i atrybuty z bazy danych
        filtered_rooms = room_filter.qs
        filtered_room_numbers = filtered_rooms.values_list("room_number", flat=True)
        selected_attributes = request.GET.getlist("attribute")  # Pobierz wybrane atrybuty z formularza

        # Filtruj dane JSON
        filtered_data = [
            point
            for point in points_data
            if point["room_number"] in filtered_room_numbers
            and (
                "attributes" not in point
                or (selected_attributes and all(attr in point.get("attributes", []) for attr in selected_attributes))
            )
        ]

        return JsonResponse(filtered_data, safe=False)

    # Renderowanie strony HTML dla standardowego żądania GET
    return render(request, "pages/search/search_rooms.html", {"filter": room_filter})


def search_free_rooms(request):
    """Wyszukaj wolne sale."""
    if request.GET:
        room_filter = FreeRoomFilter(request.GET, queryset=Room.objects.prefetch_related("attributes").distinct())
    else:
        room_filter = FreeRoomFilter(queryset=Room.objects.none())
    return render(request, "pages/search/search_free_rooms.html", {"filter": room_filter})


def search_groups(request):
    if request.GET:
        group_filter = GroupFilter(request.GET, queryset=Group.objects.all())
    else:
        group_filter = GroupFilter(queryset=Group.objects.none())
    return render(request, "pages/search/search_groups.html", {"filter": group_filter})


def api_search_meetings(request):
    meeting_filter = MeetingFilter(
        request.GET,
        queryset=Meeting.objects.select_related("room", "event")
        .prefetch_related("lecturers")
        .filter(is_approved=True)
        .order_by("start_time"),
    )
    data = [
        {
            "id": meeting.id,
            "start_time": meeting.start_time.isoformat(),
            "end_time": meeting.end_time.isoformat(),
            "title": meeting.name_pl,
            "color": meeting.color,
            "room": meeting.room.room_number if meeting.room else None,
            "logo": (
                request.build_absolute_uri(meeting.event.logo.url) if meeting.event and meeting.event.logo else None
            ),
            "lecturers": [f"{lecturer.first_name} {lecturer.last_name}" for lecturer in meeting.lecturers.all()],
            "event_name": meeting.event.name if meeting.event else None,
            "event_id": meeting.event.id if meeting.event else None,
        }
        for meeting in meeting_filter.qs
    ]
    return JsonResponse(data, safe=False)


@api_view(["GET"])
def room_status(request, room_id):
    """
    API endpoint zwracający status sali: czy odbywa się spotkanie.
    """
    try:
        # Pobierz salę po jej ID
        room = Room.objects.get(id=room_id)

        # Sprawdź czy aktualnie odbywa się spotkanie
        current_meeting = Meeting.objects.filter(
            room=room, start_time__lte=now(), end_time__gte=now(), is_approved=True
        ).exists()

        # Przygotuj odpowiedź
        data = {
            "room_id": room.id,
            "room_number": room.room_number,
            "has_meeting_now": current_meeting,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


class RoomPointsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        json_path = settings.BASE_DIR / "static" / "data" / "punkty.json"

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                points_data = json.load(file)

            # Opcjonalne filtrowanie sal na podstawie istniejących w bazie
            room_numbers = Room.objects.values_list("room_number", flat=True)
            filtered_data = [point for point in points_data if point["room_number"] in room_numbers]

            return JsonResponse(filtered_data, safe=False)
        except FileNotFoundError:
            return JsonResponse({"error": "Plik punkty.json nie został znaleziony."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Błąd w odczycie pliku punkty.json."}, status=500)






class FreeRoomsAPIView(APIView):
    """
    API endpoint zwracający wolne sale z numerem i wyposażeniem.
    """

    def get(self, request):
        start_date = request.GET.get("start_date")
        start_time = request.GET.get("start_time")
        end_date = request.GET.get("end_date")
        end_time = request.GET.get("end_time")
        attribute = request.GET.get("attribute")

        if not (start_date and start_time and end_date and end_time):
            return Response(
                {"error": "Wymagane są parametry start_date, start_time, end_date oraz end_time."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_datetime = f"{start_date}T{start_time}"
        end_datetime = f"{end_date}T{end_time}"

        # Pobieranie zajętych sal
        busy_rooms = Meeting.objects.filter(
            Q(start_time__lt=end_datetime) & Q(end_time__gt=start_datetime)
        ).values_list("room_id", flat=True)

        # Filtracja wolnych sal
        rooms = Room.objects.exclude(id__in=busy_rooms)

        if attribute:
            rooms = rooms.filter(attributes__attribute_id=attribute)

        free_rooms = [
            {
                "room_number": room.room_number,
                "has_attribute": attribute in [attr.attribute_id for attr in room.attributes.all()]
            }
            for room in rooms.prefetch_related("attributes")
        ]

        return Response(free_rooms, status=status.HTTP_200_OK)




    class RoomEquipmentAPIView(APIView):
    """
    API endpoint zwracający numer sali i informację o posiadaniu określonego wyposażenia.
    """

    def get(self, request):
        attribute = request.GET.get("attribute")

        if not attribute:
            return Response(
                {"error": "Parametr 'attribute' jest wymagany."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Pobieranie wszystkich sal
        rooms = Room.objects.prefetch_related("attributes").all()

        room_list = [
            {
                "room_number": room.room_number,
                "has_attribute": attribute in [attr.attribute_id for attr in room.attributes.all()]
            }
            for room in rooms
        ]

        return Response(room_list, status=status.HTTP_200_OK)
