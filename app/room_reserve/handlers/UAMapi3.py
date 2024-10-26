import requests
from pydantic import ValidationError
from django.db import transaction
from room_reserve.models import Meeting
from typing import Optional
import logging
from room_reserve.serializers import MeetingDataIn
from requests_oauthlib import OAuth1

logger = logging.getLogger(__name__)

consumer_key = "N7AhjH9YPUVKN6ft3zfU"
consumer_secret = "29Xd3aDwKGePMaVrXvpdWCq2y274dauwf7xX2rBy"

auth = OAuth1(consumer_key, consumer_secret)

USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_MEETING = "/services/tt/room"

meeting_ids = [
    2488, 2489, 2490, 2684, 2685, 2686, 2687, 2688, 2689,
    2690, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698,
    2699, 2700, 2701, 2702, 2703, 2704, 2777,
]


class UAMApiHandler:
    def __init__(self, meeting_ids: list):
        self.meeting_ids = meeting_ids

    def get_meeting_data(self, meeting_id: int) -> Optional[dict]:
        # Zmiana formatu danych: zróbmy debug, żeby upewnić się, jakie dane są wysyłane
        data = {"meeting_id": str(meeting_id), "format": "json"}
        logger.debug(f"Wysyłanie zapytania z danymi: {data}")

        try:
            r = requests.post(f"{USOS_API_BASE_URL}{USOS_API_MEETING}", data=data, auth=auth)
            r.raise_for_status()

            # Sprawdzenie odpowiedzi API
            meeting_data = r.json()

            if meeting_data:
                logger.info(f"Odebrano dane spotkania dla ID {meeting_id}: {meeting_data}")
                return meeting_data
            else:
                logger.warning(f"Brak danych dla spotkania o ID {meeting_id}")
                return None

        except requests.HTTPError as e:
            logger.error(f"Błąd HTTP przy pobieraniu spotkania {meeting_id}: {e}, Response: {r.text}")
            return None
        except requests.RequestException as e:
            logger.error(f"Błąd sieci przy pobieraniu spotkania {meeting_id}: {e}")
            return None

    def save_meeting(self, meeting_data: dict):
        try:
            # Walidacja danych wejściowych za pomocą Pydantic
            meeting = MeetingDataIn(**meeting_data)

            with transaction.atomic():
                meeting_obj, created = Meeting.objects.update_or_create(
                    id=meeting_data.get('id'),
                    defaults={
                        "start_time": meeting.start_time,
                        "end_time": meeting.end_time,
                        "name_pl": meeting.name.pl,
                        "name_en": meeting.name.en,
                        "is_updated": True,
                    },
                )
                if created:
                    logger.info(f"Utworzono spotkanie: {meeting.name.pl}.")
                else:
                    logger.info(f"Zaktualizowano spotkanie: {meeting.name.pl}.")

        except ValidationError as e:
            logger.error(f"Błąd walidacji dla spotkania ID {meeting_data.get('id')}: {e}")
        except Exception as e:
            logger.error(f"Błąd przy zapisie spotkania {meeting_data.get('id')}: {e}")

    def main(self):
        for meeting_id in self.meeting_ids:
            meeting_data = self.get_meeting_data(meeting_id)
            if meeting_data:
                self.save_meeting(meeting_data)
            else:
                logger.warning(f"Pominięto zapis dla spotkania o ID {meeting_id} ze względu na brak danych.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Ustawienie poziomu logowania na DEBUG
    handler = UAMApiHandler(meeting_ids=meeting_ids)
    handler.main()
