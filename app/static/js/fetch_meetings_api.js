async function fetchMeetings() {
    const apiEndpoint = '/get_meetings/';

    try {
        const response = await fetch(apiEndpoint);
        const meetings = await response.json();
        return meetings;
    } catch (error) {
        console.error('Błąd podczas pobierania API:', error);
        return [];
    }
}

function filterMeetingsByRoom(meetings) {
    const roomNumberElement = document.querySelector('#filter_room_number');
    if (!roomNumberElement) {
        return meetings;
    }

    const roomNumber = roomNumberElement.innerHTML;
    return meetings.filter(meeting => meeting.room === roomNumber);
}

async function importMeetings() {
    const meetings = await fetchMeetings();
    return filterMeetingsByRoom(meetings);
}
