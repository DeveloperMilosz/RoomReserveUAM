function getMeetingFromTable() {
    const table = document.querySelector('.tabela');
    const rows = table.querySelectorAll('tbody tr');

    const result = [];

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
        
        result.push({
            id: id,
            title: title,
            start_time: start_time,
            end_time: end_time,
            name_en: title,
            color: color
        });
    });
    
    return result;
}

async function importMeetings() {
    let meetings = getMeetingFromTable();
    return meetings;
}