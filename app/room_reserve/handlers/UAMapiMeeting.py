import requests
from pydantic import BaseModel, ValidationError
from django.db import transaction
from room_reserve.models import Meeting
from typing import Optional, List, Dict
import logging
from requests_oauthlib import OAuth1
#from room_reserve.serializers import MeetingDataIn

# Konfiguracja loggera
logger = logging.getLogger(__name__)

# Klucze do uwierzytelniania OAuth
consumer_key = "N7AhjH9YPUVKN6ft3zfU"
consumer_secret = "29Xd3aDwKGePMaVrXvpdWCq2y274dauwf7xX2rBy"
auth = OAuth1(consumer_key, consumer_secret)

# URL API
USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_MEETING = "/services/tt/room"

# Lista ID spotkań do pobrania
meeting_ids = [
    2488, 2489, 2490, 2684, 2685, 2686, 2687, 2688, 2689,
    2690, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698,
    2699, 2700, 2701, 2702, 2703, 2704, 2777,
]


class MeetingData(BaseModel):
    start_time: str
    end_time: str
    name: Dict[str, str]

class UAMApiHandler:
    def __init__(self, meeting_ids: List[int]):
        self.meeting_ids = meeting_ids

    def get_meeting_data(self, meeting_id: int) -> Optional[List[dict]]:
        """Pobieranie danych o spotkaniach z API."""
        data = {"room_id": str(meeting_id), "format": "json"}  # Parametry requesta

        try:
            r = requests.post(f"{USOS_API_BASE_URL}{USOS_API_MEETING}", data=data, auth=auth)
            r.raise_for_status()  # Sprawdzenie, czy odpowiedź jest poprawna

            meeting_data = r.json()  # Konwersja odpowiedzi na format JSON
            logger.debug(f"Data received for meeting ID {meeting_id}: {meeting_data}")

            if meeting_data:
                return meeting_data
            else:
                logger.warning(f"No data returned for meeting ID {meeting_id}")
                return None

        except requests.RequestException as e:
            logger.error(f"An error occurred while requesting meeting {meeting_id}: {e}")
            return None

    def save_meeting(self, meeting_data: dict):
        """Zapis danych spotkania do bazy."""
        try:
            # Walidacja danych za pomocą Pydantic
            meeting = MeetingData(**meeting_data)

            with transaction.atomic():
                meeting_obj, created = Meeting.objects.update_or_create(
                    id=meeting_data.get('id'),  # Zakładając, że ID jest dostępne w danych API
                    defaults={
                        "start_time": meeting.start_time,
                        "end_time": meeting.end_time,
                        "name_pl": meeting.name.get('pl'),  # Zabezpieczenie przed KeyError
                        "name_en": meeting.name.get('en'),
                        "is_updated": True,
                    },
                )
                if created:
                    logger.info(f"Meeting {meeting.name.get('pl')} created.")
                else:
                    logger.info(f"Meeting {meeting.name.get('pl')} updated.")

        except ValidationError as e:
            logger.error(f"Validation error for meeting data: {e.json()}")
        except Exception as e:
            logger.error(f"Error saving meeting: {e}")

    def main(self):
        """Główna metoda do pobierania i zapisywania danych o spotkaniach."""
        for meeting_id in self.meeting_ids:
            meeting_data_list = self.get_meeting_data(meeting_id)

            if meeting_data_list:
                # Iteracja po liście spotkań zwróconych dla danego room_id
                for meeting_data in meeting_data_list:
                    self.save_meeting(meeting_data)


if __name__ == "__main__":
    handler = UAMApiHandler(meeting_ids=meeting_ids)
    handler.main()
