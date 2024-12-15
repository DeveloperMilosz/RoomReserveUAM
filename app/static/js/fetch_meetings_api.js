async function fetchMeetings() {
    const apiEndpoint = '/get_meetings/';

    try {
        // Fetch meetings from the API
        const response = await fetch(apiEndpoint);
        const meetings = await response.json();
        return meetings;
    } catch (error) {
        console.error('Error fetching meetings:', error);
        return [];
    }
}

function filterMeetingsByRoom(meetings) {
    const roomNumberElement = document.querySelector('#filter_room_number');
    if (!roomNumberElement) {
        return meetings;
    }

    const roomNumber = roomNumberElement.innerHTML;
    console.log(roomNumber)

    // Filter meetings by the specified room number
    return meetings.filter(meeting => meeting.room === roomNumber);
}

async function importMeetings() {
    const meetings = await fetchMeetings();
    return filterMeetingsByRoom(meetings);
}
