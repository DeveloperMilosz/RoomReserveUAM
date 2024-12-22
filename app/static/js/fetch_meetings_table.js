async function fetchMeetings() {
    const apiURL = "/api/search/meetings/";
    const params = new URLSearchParams(window.location.search);

    try {
        const response = await fetch(`${apiURL}?${params}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const meetings = await response.json();
        return meetings;
    } catch (error) {
        console.error("Wystąpił błąd podczas pobierania danych z API:", error);
        return [];
    }
}

async function importMeetings() {
    try {
        const meetings = await fetchMeetings();
        renderMeetingsTable(meetings);
        return meetings;
    } catch (error) {
        console.error("Wystąpił błąd podczas importowania spotkań:", error);
    }
}

function renderMeetingsTable(meetings) {
    const tableBody = document.querySelector("table.data-table tbody");

    tableBody.innerHTML = "";

    if (!meetings || meetings.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="7">Brak wyników.</td></tr>`;
        return;
    }

    meetings.forEach((meeting) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td><a href="/meeting/${meeting.id}/">${meeting.title || "Brak nazwy"}</a></td>
            <td>${meeting.lecturers.join(", ") || "Brak prowadzącego"}</td>
            <td>${meeting.room || "Brak sali"}</td>
            <td>${new Date(meeting.start_time).toLocaleDateString()}</td>
            <td>${new Date(meeting.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
            <td>${new Date(meeting.end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
            <td>
                ${
                    meeting.event_name && meeting.event_id
                        ? `<a href="/event/${meeting.event_id}/">${meeting.event_name}</a>`
                        : "Nieprzypisane"
                }
            </td>
        `;

        tableBody.appendChild(row);
    });
}
