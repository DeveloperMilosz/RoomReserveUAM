import requests
from pydantic import BaseModel, ValidationError
from django.db import transaction
from room_reserve.models import Room  # Zakładamy, że model nazywa się Room
from typing import Optional, List, Dict
import logging
from requests_oauthlib import OAuth1

# Konfiguracja loggera
logger = logging.getLogger(__name__)

# Dane uwierzytelniające OAuth
consumer_key = "N7AhjH9YPUVKN6ft3zfU"
consumer_secret = "29Xd3aDwKGePMaVrXvpdWCq2y274dauwf7xX2rBy"
auth = OAuth1(consumer_key, consumer_secret)

# URL API
USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_ROOM = "/services/tt/room"

# Lista ID pokoi do pobrania
room_ids = [
    2488, 2489, 2490, 2684, 2685, 2686, 2687, 2688, 2689,
    2690, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698,
    2699, 2700, 2701, 2702, 2703, 2704, 2777,
]

class RoomData(BaseModel):
    """Model danych pokoju zgodny z odpowiedzią API."""
    id: int
    attributes: List[Dict[str, str]]

class UAMApiHandler:
    def __init__(self, room_ids: List[int]):
        self.room_ids = room_ids

    def get_room_data(self, room_id: int) -> Optional[dict]:
        """Pobieranie danych o pokoju z API."""
        params = {"room_id": str(room_id), "format": "json"}  # Parametry zapytania

        try:
            response = requests.post(f"{USOS_API_BASE_URL}{USOS_API_ROOM}", params=params, auth=auth)
            response.raise_for_status()  # Sprawdzenie, czy odpowiedź jest poprawna

            room_data = response.json()  # Konwersja odpowiedzi na format JSON
            logger.debug(f"Data received for room ID {room_id}: {room_data}")

            if room_data:
                return room_data
            else:
                logger.warning(f"No data returned for room ID {room_id}")
                return None

        except requests.RequestException as e:
            logger.error(f"An error occurred while requesting room {room_id}: {e}")
            return None

    def save_room(self, room_data: dict):
        """Zapis danych pokoju do bazy."""
        try:
            # Walidacja danych za pomocą Pydantic
            room = RoomData(**room_data)

            with transaction.atomic():
                room_obj, created = Room.objects.update_or_create(
                    id=room.id,  # Zakładając, że pole ID jest dostępne w modelu Room
                    defaults={
                        "attributes": room.attributes,
                    },
                )
                if created:
                    logger.info(f"Room {room.id} created.")
                else:
                    logger.info(f"Room {room.id} updated.")

        except ValidationError as e:
            logger.error(f"Validation error for room data: {e.json()}")
        except Exception as e:
            logger.error(f"Error saving room: {e}")

    def main(self):
        """Główna metoda do pobierania i zapisywania danych o pokojach."""
        for room_id in self.room_ids:
            room_data = self.get_room_data(room_id)

            if room_data:
                self.save_room(room_data)


if __name__ == "__main__":
    handler = UAMApiHandler(room_ids=room_ids)
    handler.main()
