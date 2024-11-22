import requests
from pydantic import ValidationError
from django.db import transaction
from room_reserve.models import Room
from typing import Optional
import logging
from pydantic import BaseModel

# Define Pydantic models
class BuildingNameIn(BaseModel):
    pl: str
    en: str

class RoomDataIn(BaseModel):
    id: int
    number: str
    building_id: int
    building_name: BuildingNameIn

# Configure logger
logger = logging.getLogger(__name__)

# API configuration
USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_ROOM = "/services/geo/room"

# Room IDs to retrieve
room_ids = [
    2488, 2489, 2490, 2684, 2685, 2686, 2687, 2688, 2689,
    2690, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698,
    2699, 2700, 2701, 2702, 2703, 2777,
]

class UAMApiHandler:
    def __init__(self, room_ids: list):
        self.room_ids = room_ids

    def get_room_data(self, room_id: int) -> Optional[dict]:
        """Fetch room data from API using requests."""
        data = {"room_id": str(room_id), "format": "json"}  # Request parameters

        try:
            # Make a POST request
            response = requests.post(f"{USOS_API_BASE_URL}{USOS_API_ROOM}", data=data)
            response.raise_for_status()  # Raise an error for bad responses

            room_data = response.json()  # Parse JSON response

            if room_data:
                return room_data
            else:
                logger.warning(f"No data returned for room ID {room_id}")
                return None

        except requests.RequestException as e:
            logger.error(f"An error occurred while requesting room {room_id}: {e}")
            return None

    def save_room(self, room_data: dict):
        """Save room data to the database."""
        try:
            # Validate data using Pydantic
            room = RoomDataIn(**room_data)

            # Save to database in a transaction
            with transaction.atomic():
                room_obj, created = Room.objects.update_or_create(
                    id=room.id,
                    defaults={
                        "room_number": room.number,
                        "building_id": room.building_id,
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
            logger.error(f"Validation error for room ID {room_data.get('id')}: {e.json()}")
        except Exception as e:
            logger.error(f"Error saving room {room_data.get('id')}: {e}")

    def main(self):
        """Main method to fetch and save room data."""
        for room_id in self.room_ids:
            room_data = self.get_room_data(room_id)
            if room_data:
                self.save_room(room_data)

# Run the handler if script is executed directly
if __name__ == "__main__":
    handler = UAMApiHandler(room_ids=room_ids)
    handler.main()
