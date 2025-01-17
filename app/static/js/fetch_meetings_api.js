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

function filterMeetingsByEvent(meetings) {
    const eventNameElement = document.querySelector('#filter_event');
    if (!eventNameElement) {
        return meetings;
    }

    const eventName = eventNameElement.innerHTML.trim();
    return meetings.filter(meeting => meeting.event_name == eventName);
}

async function importMeetings() {
    let meetings = await fetchMeetings();
    meetings = filterMeetingsByRoom(meetings);
    meetings = filterMeetingsByEvent(meetings);
    if (window.filterMeetingsByUserEmail) {
        meetings = filterMeetingsByUserEmail(meetings);
    }
    
    return meetings;
}
