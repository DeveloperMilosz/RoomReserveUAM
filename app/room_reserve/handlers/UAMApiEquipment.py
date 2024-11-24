import requests
from pydantic import BaseModel, ValidationError
from django.db import transaction
from room_reserve.models import Room, RoomAttribute
from typing import Optional, List
import logging


# Define Pydantic models
class AttributeDescription(BaseModel):
    pl: str
    en: str


class RoomAttributeIn(BaseModel):
    id: str
    description: AttributeDescription
    count: int


class RoomDataIn(BaseModel):
    id: int
    attributes: List[RoomAttributeIn]


# Configure logger
logger = logging.getLogger(__name__)

# API configuration
USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_ROOM = "/services/geo/rooms"

# Room IDs to retrieve
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
    354,
]


class UAMApiHandler:
    def __init__(self, room_ids: list):
        self.room_ids = room_ids

    def get_room_data(self, room_id: int) -> Optional[dict]:
        """Fetch room data from API using requests."""
        data = {"room_ids": str(room_id), "format": "json", "fields": "attributes"}
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

        try:
            # Make a POST request
            response = requests.post(f"{USOS_API_BASE_URL}{USOS_API_ROOM}", data=data, headers=headers)
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

    def save_room(self, room_id: int, room_data: dict):
        """Save room and attributes data to the database."""
        try:
            # Validate data using Pydantic
            if str(room_id) not in room_data:
                logger.warning(f"Room ID {room_id} not found in response.")
                return

            validated_data = RoomDataIn(id=room_id, **room_data[str(room_id)])

            # Save to database in a transaction
            with transaction.atomic():
                # Save room object
                room_obj, created = Room.objects.update_or_create(
                    id=validated_data.id,
                    defaults={"is_updated": True},
                )
                if created:
                    logger.info(f"Room {room_id} created.")
                else:
                    logger.info(f"Room {room_id} updated.")

                # Save attributes
                RoomAttribute.objects.filter(room=room_obj).delete()  # Clear existing attributes
                for attr in validated_data.attributes:
                    RoomAttribute.objects.create(
                        room=room_obj,
                        attribute_id=attr.id,
                        description_pl=attr.description.pl,
                        description_en=attr.description.en,
                        count=attr.count,
                    )
                logger.info(f"Attributes for room {room_id} saved.")

        except ValidationError as e:
            logger.error(f"Validation error for room ID {room_id}: {e.json()}")
        except Exception as e:
            logger.error(f"Error saving room {room_id}: {e}")

    def main(self):
        """Main method to fetch and save room data."""
        for room_id in self.room_ids:
            room_data = self.get_room_data(room_id)
            if room_data:
                self.save_room(room_id, room_data)


# Run the handler if script is executed directly
if __name__ == "__main__":
    handler = UAMApiHandler(room_ids=room_ids)
    handler.main()
