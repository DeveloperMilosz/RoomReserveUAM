async function fetchMeetingsFromAPI() {
    let meetings;
    const currentURL = window.location.href;

        const apiEndpoint = '/get_meetings/';
        const response = await fetch(apiEndpoint);
        meetings = await response.json();

    return meetings;
}
