import requests
from pydantic import ValidationError
from django.db import transaction
from room_reserve.models import Lecturers
from typing import Optional
import logging
from pydantic import BaseModel


# Define Pydantic models for lecturer data
class LecturerDataIn(BaseModel):
    id: str
    first_name: str
    last_name: str


# Configure logger
logger = logging.getLogger(__name__)

# API configuration
USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_LECTURER = "/services/users/staff_index"

# List of lecturer IDs to retrieve (example)
lecturer_ids = [
    "33136",
    "1941",
    "552272",
    "471597",
    "5592",
    "551394",
    "469848",
    "1963",
    "475646",
]


class UAMLecturerApiHandler:
    def __init__(self, lecturer_ids: List[str]):
        self.lecturer_ids = lecturer_ids

    def get_lecturer_data(self, lecturer_id: str) -> Optional[dict]:
        """Fetch lecturer data from API using requests."""
        data = {"user_id": lecturer_id, "format": "json"}  # Request parameters

        try:
            # Make a POST request
            response = requests.post(f"{USOS_API_BASE_URL}{USOS_API_LECTURER}", data=data)
            response.raise_for_status()  # Raise an error for bad responses

            lecturer_data = response.json()  # Parse JSON response

            if lecturer_data:
                return lecturer_data
            else:
                logger.warning(f"No data returned for lecturer ID {lecturer_id}")
                return None

        except requests.RequestException as e:
            logger.error(f"An error occurred while requesting lecturer {lecturer_id}: {e}")
            return None

    def save_lecturer(self, lecturer_data: dict):
        """Save lecturer data to the database."""
        try:
            # Validate data using Pydantic
            lecturer = LecturerDataIn(**lecturer_data)

            # Save to database in a transaction
            with transaction.atomic():
                # Only save 'first_name' and 'last_name'
                lecturer_obj, created = Lecturers.objects.update_or_create(
                    id=lecturer.id,
                    defaults={
                        "first_name": lecturer.first_name,
                        "last_name": lecturer.last_name,
                    },
                )
                if created:
                    logger.info(f"Lecturer {lecturer.first_name} {lecturer.last_name} created.")
                else:
                    logger.info(f"Lecturer {lecturer.first_name} {lecturer.last_name} updated.")

        except ValidationError as e:
            logger.error(f"Validation error for lecturer ID {lecturer_data.get('id')}: {e.json()}")
        except Exception as e:
            logger.error(f"Error saving lecturer {lecturer_data.get('id')}: {e}")

    def main(self):
        """Main method to fetch and save lecturer data."""
        for lecturer_id in self.lecturer_ids:
            lecturer_data = self.get_lecturer_data(lecturer_id)
            if lecturer_data:
                self.save_lecturer(lecturer_data)


# Run the handler if script is executed directly
if __name__ == "__main__":
    handler = UAMLecturerApiHandler(lecturer_ids=lecturer_ids)
    handler.main()
