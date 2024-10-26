import requests
from requests_oauthlib import OAuth1

# Twoje dane uwierzytelniające
consumer_key = "N7AhjH9YPUVKN6ft3zfU"
consumer_secret = "29Xd3aDwKGePMaVrXvpdWCq2y274dauwf7xX2rBy"

# Tworzymy obiekt OAuth1
auth = OAuth1(consumer_key, consumer_secret)

USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_ROOM = "/services/tt/room"

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


def get_room_data(room_id):
    params = {"room_id": str(room_id), "format": "json"}
    r = requests.post(USOS_API_BASE_URL + USOS_API_ROOM, params=params, auth=auth)
    return r.text

for room_id in room_ids:
    room_data = get_room_data(room_id)
    print(f"Room ID: {room_id}, Data: {room_data}")
