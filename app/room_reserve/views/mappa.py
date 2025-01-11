from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from room_reserve.models import Room, Meeting


def mapa_pietro1(request):
    return render(request, "pages/mapy/mapka1pietro.html")


def pietro1(request):
    return render(request, "pages/mapy/pietro1.html")


def pietro2(request):
    return render(request, "pages/mapy/pietro2.html")


def parter(request):
    # Pobierz wszystkie pokoje na parterze (lub według innych kryteriów)
    rooms = Room.objects.filter(building_name_pl="Parter")  # Zakładam, że tak identyfikujesz budynek
    return render(request, "pages/mapy/parter.html", {"rooms": rooms})


class RoomStatusesAPIView(APIView):
    """
    API endpoint zwracający status wszystkich sal z dodatkowymi informacjami o aktualnych spotkaniach.
    """

    def get(self, request):
        rooms = Room.objects.all()
        room_statuses = []

        for room in rooms:
            # Pobierz aktualne spotkanie dla sali, jeśli istnieje
            current_meeting = Meeting.objects.filter(
                room=room,
                start_time__lte=now(),
                end_time__gte=now(),
                is_approved=True,
            ).first()

            if current_meeting:
                # Jeśli jest aktywne spotkanie, dodaj szczegóły spotkania
                meeting_details = {
                    "meeting_name": current_meeting.name_pl,
                    "lecturers": [
                        f"{lecturer.first_name} {lecturer.last_name}" for lecturer in current_meeting.lecturers.all()
                    ],
                    "start_time": current_meeting.start_time.strftime("%H:%M"),
                    "end_time": current_meeting.end_time.strftime("%H:%M"),
                }
            else:
                # Jeśli brak aktywnego spotkania, ustaw szczegóły jako `None`
                meeting_details = None

            room_statuses.append(
                {
                    "room_id": room.id,
                    "room_number": room.room_number,
                    "has_meeting_now": bool(current_meeting),
                    "meeting_details": meeting_details,
                }
            )

        return Response(room_statuses, status=status.HTTP_200_OK)
