function getMeetingFromTable() {
    // Znajdź tabelę HTML na podstawie klasy
    const table = document.querySelector('.tabela');
    const rows = table.querySelectorAll('tbody tr');
    // Tablica, która przechowa wyniki
    const result = [];

    // Iteruj przez każdy wiersz tabeli
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        
        const title = cells[0].querySelector('.link').textContent.trim();

        const startDate = cells[3].textContent.trim();
        const startTime = cells[4].textContent.trim();
        const endDate = cells[5].textContent.trim();
        const endTime = cells[6].textContent.trim();
        const id = parseInt(cells[8].textContent.trim(), 10);
        const color = cells[9].textContent.trim();
        cells[5].style.display="none";
        cells[8].style.display="none";
        cells[9].style.display="none";
        const start_time = `${startDate}T${startTime}:00+00:00`;
        const end_time = `${endDate}T${endTime}:00+00:00`;
        
        // Dodaj obiekt do wyników
        result.push({
            id: id,
            title: title,
            start_time: start_time,
            end_time: end_time,
            name_en: title, // Zakładam, że tytuł w języku angielskim jest taki sam
            color: color // Domyślny kolor, jeśli nie jest dostarczony w tabeli
        });
    });
    
    return result;
}

// async function fetchMeetings() {
//         let meetings;
//         currentURL = window.location.href
//         if (currentURL === 'http://0.0.0.0:8000/') {
//             apiEndpoint = '/get_meetings/';
//             const response = await fetch(apiEndpoint);
//             meetings = await response.json();
//         }  else {
//             meetings = getMeetingFromTable()
//         }

//         console.log(meetings)

//         if (currentView === 'monthly') {
//             displayMeetings(meetings);
//         } else if (currentView === 'weekly') {
//             const weekStart = new Date(currentDate);
//             weekStart.setDate(currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));
//             const weekEnd = new Date(weekStart);
//             weekEnd.setDate(weekStart.getDate() + 6);

//             const weeklyMeetings = meetings.filter(meeting => {
//                 const startDate = new Date(meeting.start_time);
//                 return startDate >= weekStart && startDate <= weekEnd;
//             });

//             displayMeetings(weeklyMeetings);
//         }
// }

async function fetchMeetingsFromAPI() {
    let meetings = getMeetingFromTable();
    return meetings;
}