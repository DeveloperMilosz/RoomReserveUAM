import httpx
from pydantic import ValidationError
from django.db import transaction
from room_reserve.models import Room
from typing import Optional
import logging
from room_reserve.serializers import RoomDataIn
logger = logging.getLogger(__name__)


# Konfiguracja API
USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_ROOM = "/services/geo/room"

# Lista room_id
room_ids = [
    2488,
    2489,
    2490,
    2684,
    2685,
    2686,
    2687,
    2688,
    2689,
    2690,
    2691,
    2692,
    2693,
    2694,
    2695,
    2696,
    2697,
    2698,
    2699,
    2700,
    2701,
    2702,
    2703,
    2704,
    2777,
]


class UAMApiHandler:
    def __init__(self, room_ids: list):
        self.room_ids = room_ids

    def get_room_data(self, room_id: int) -> Optional[RoomDataIn]:
        data = {"room_id": str(room_id), "format": "json"}
        r = httpx.post(f"{USOS_API_BASE_URL}{USOS_API_ROOM}", data=data)
        room = RoomDataIn(**room_id)
        return r.json(), room

    # TODO sprawdzic czy dostales 200, sprawdzic czy sa dane. try expect

    def save_room(self, room_data, room):
        try:

            with transaction.atomic():

                room_obj, created = Room.objects.update_or_create(
                    id=room_data,
                    room_number=room.number,
                    building_id=room.building_id,
                    defaults={
                        "room number": room.room_number,
                        "building id": room.building_id,
                        "building_name_pl": room.building_name.pl,
                        "building_name_en": room.building_name.en,
                        "is_updated": True,
                    },
                )
                if created:
                    logger.info(f"Room {room.number} created.")
                else:
                    logger.info(f"Room {room.number} updated.")

        except ValidationError as e:
            logger.error(f"Validation error for room ID {room_data.get('id')}: {e}")

    def main(self):
        for room_id in self.room_ids:
            room_data = get_room_data(room_id)
            save_room(room_data)


UAMApiHandler(room_ids=room_ids).main()
