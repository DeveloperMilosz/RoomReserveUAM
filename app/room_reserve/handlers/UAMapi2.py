from pydantic import BaseModel
import httpx

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
import httpx
from pydantic import BaseModel

USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_ROOM = "/services/geo/room"

data = {"room_id": str(2488), "format": "json"}
r = httpx.post(USOS_API_BASE_URL + USOS_API_ROOM, data=data)
data = r.json()


class BuildingNameIn(BaseModel):
    pl: str
    en: str


class RoomDataIn(BaseModel):
    id: int
    number: str
    building_id: int
    building_name: BuildingNameIn


for RoomDataIn in data:
    model = RoomDataIn(**data)
    print(model)
