import httpx

USOS_API_BASE_URL = "https://usosapps.amu.edu.pl"
USOS_API_ROOM = "/services/geo/rooms"

# Lista room_id
room_ids = [
    2488, 2489, 2490, 2684, 2685, 2686, 2687, 2688, 2689, 2690, 2691, 2692,
    2693, 2694, 2695, 2696, 2697, 2698, 2699, 2700, 2701, 2702, 2703, 2704,
    2777, 354
]

# Funkcja do wysyłania żądania POST dla danego room_id
def get_room_data(room_id):
    data = {
        "room_ids": str(room_id),  # Zmiana na "room_ids"
        "format": "json",
        "fields": "attributes"  # Dodano parametr "fields"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",  # Nagłówek do przekazania danych jako form-urlencoded
        "Accept": "application/json"  # Nagłówek oczekujący odpowiedzi JSON
    }
    response = httpx.post(USOS_API_BASE_URL + USOS_API_ROOM, data=data, headers=headers)
    return response.text

# Pętla po wszystkich room_id
for room_id in room_ids:
    room_data = get_room_data(room_id)
    print(f"Room ID: {room_id}, Data: {room_data}")
