fetch('/api/room-statuses/')
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
})
.then(data => {
  const meetingsList = document.getElementById('current-meetings');

  data.forEach(room => {
    const roomElement = document.getElementById(`room-${room.room_number}`);
    if (roomElement) {
      if (room.has_meeting_now) {
        roomElement.classList.remove('gray');
        roomElement.classList.add('occupied');

        const meetingItem = document.createElement('li');
        meetingItem.innerHTML = `
          <strong>Sala: ${room.room_number}</strong>
          <span>${room.meeting_details?.meeting_name || 'Brak nazwy'}</span>
          <span>${room.meeting_details?.lecturers.join(', <br>') || 'Brak danych'}</span>
          <span>Czas: ${room.meeting_details?.start_time || ''} - ${room.meeting_details?.end_time || ''}</span>
        `;
        meetingsList.appendChild(meetingItem);
      }
    }
  });
})
.catch(error => console.error('Błąd przy pobieraniu statusów sal:', error));

const redirectMap = {
    "{% url 'mapa_parter' %}": "{% url 'mapa_pietro1' %}",
    "{% url 'mapa_pietro1' %}": "{% url 'mapa_pietro2' %}",
    "{% url 'mapa_pietro2' %}": "{% url 'mapa_parter' %}",
};

const redirectToNextPage = () => {
    const currentUrl = window.location.pathname;
    const nextUrl = redirectMap[currentUrl];
    if (nextUrl) {
    window.location.href = nextUrl;
    } else {
    console.error('Nie znaleziono URL do przekierowania:', currentUrl);
    }
};

setTimeout(redirectToNextPage, 15000);