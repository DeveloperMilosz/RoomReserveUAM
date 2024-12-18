let currentView = 'monthly';
let currentDate = new Date();

const daysOfWeek = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'];

const getMondayFirstDay = weekday => (weekday + 6) % 7;

const formatDate = date =>
    `${String(date.getDate()).padStart(2, '0')}.${String(date.getMonth() + 1).padStart(2, '0')}.${date.getFullYear()}`;

const timeToPosition = (start, end) => {
    const startHour = start.getUTCHours() + start.getUTCMinutes() / 60;
    const endHour = end.getUTCHours() + end.getUTCMinutes() / 60;
    return {
        top: startHour * 60,
        height: (endHour - startHour) * 60
    };
};

const updateDateRange = () => {
    const dateRangeEl = document.getElementById('dateRange');
    if (currentView === 'monthly') {
        dateRangeEl.textContent = currentDate.toLocaleDateString('pl-PL', { year: 'numeric', month: 'long' });
    } else {
        const weekStart = new Date(currentDate);
        weekStart.setDate(currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6);
        dateRangeEl.textContent = `${formatDate(weekStart)} - ${formatDate(weekEnd)}`;
    }
};

const updateWeekdaysWithDates = () => {
    const weekdaysEl = document.querySelector('.weekdays');
    weekdaysEl.innerHTML = '';
    const weekStart = new Date(currentDate);
    weekStart.setDate(currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));

    for (let i = 0; i < 7; i++) {
        const currentDay = new Date(weekStart);
        currentDay.setDate(weekStart.getDate() + i);
        const dayEl = document.createElement('div');
        dayEl.innerHTML = `<strong>${daysOfWeek[i]}</strong> ${formatDate(currentDay)}`;
        weekdaysEl.appendChild(dayEl);
    }
};

const generateMonthlyCalendar = () => {
    const calendarEl = document.getElementById('calendar');
    calendarEl.innerHTML = '';
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = getMondayFirstDay(new Date(year, month, 1).getDay());

    for (let i = 0; i < firstDay; i++) {
        calendarEl.appendChild(document.createElement('div')).classList.add('day');
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayEl = document.createElement('div');
        dayEl.classList.add('day');
        dayEl.dataset.day = day;
        dayEl.innerHTML = `<strong>${day}</strong><div class="events"></div>`;
        calendarEl.appendChild(dayEl);
    }
};

function generateWeeklyCalendar(year, month, day) {
    const calendarEl = document.getElementById('calendar');
    calendarEl.innerHTML = '';
    const currentDate = new Date(year, month, day);
    const startOfWeek = currentDate.getDate() - getMondayFirstDay(currentDate.getDay());

    const hourColumn = document.createElement('div');
    hourColumn.classList.add('hour');
    
    // Pętla od 0 do 23.5 (0.5 oznacza pół godziny)
    for (let i = 0; i < 24; i += 0.5) {
        const timeLabel = document.createElement('div');
        timeLabel.classList.add('time-label');
    
        // Jeśli i jest liczbą całkowitą, dodaj ":00", w przeciwnym razie dodaj ":30"
        const hour = Math.floor(i); // Całkowita część godziny
        const minutes = (i % 1 === 0) ? '00' : '30'; // Dodanie minut
    
        timeLabel.textContent = `${String(hour).padStart(2, '0')}:${minutes}`;
        hourColumn.appendChild(timeLabel);
    }
    
    calendarEl.appendChild(hourColumn);

    for (let i = 0; i < 7; i++) {
        const weekDay = new Date(year, month, startOfWeek + i - 1);
        const dayEl = document.createElement('div');
        dayEl.classList.add('day', 'weekly');
        const formattedDate = weekDay.toLocaleDateString('pl-PL').replace(/\//g, '.');
        dayEl.innerHTML = `<strong>${formattedDate}</strong>`;
        calendarEl.appendChild(dayEl);
    }
}

const displayMeetings = meetings => {
    const calendarEl = document.getElementById('calendar');

    if (currentView === 'monthly') {
        const days = calendarEl.querySelectorAll('.day');
        days.forEach(day => {
            const eventsContainer = day.querySelector('.events');
            if (eventsContainer) eventsContainer.innerHTML = '';
        });

        meetings.forEach(meeting => {
            const startDate = new Date(meeting.start_time);
            if (startDate.getMonth() === currentDate.getMonth() && startDate.getFullYear() === currentDate.getFullYear()) {
                const dayIndex = startDate.getDate();
                const firstDayOffset = getMondayFirstDay(new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay());

                const dayEl = calendarEl.querySelector(`.day:nth-child(${dayIndex + firstDayOffset})`);

                if (dayEl) {
                    let eventsContainer = dayEl.querySelector('.events');
                    if (!eventsContainer) {
                        eventsContainer = document.createElement('div');
                        eventsContainer.classList.add('events');
                        dayEl.appendChild(eventsContainer);
                    }

                    const eventEl = document.createElement('a');
                    eventEl.href = `/meeting/${meeting.id}`;
                    eventEl.classList.add('event');
                    eventEl.style.backgroundColor = meeting.color;
                    eventEl.textContent = meeting.title;
                    eventsContainer.appendChild(eventEl);
                }
            }
        });
    } else if (currentView === 'weekly') {
        displayWeeklyMeetings(meetings);
    }
};

const displayWeeklyMeetings = meetings => {
    const calendarEl = document.getElementById('calendar');
    const dayColumns = Array.from(calendarEl.querySelectorAll('.day.weekly'));

    const meetingsByDay = {};
    meetings.forEach(meeting => {
        const startDate = new Date(meeting.start_time);
        const endDate = new Date(meeting.end_time);
        const dayIndex = getMondayFirstDay(startDate.getDay());

        if (!meetingsByDay[dayIndex]) {
            meetingsByDay[dayIndex] = [];
        }

        meetingsByDay[dayIndex].push({
            ...meeting,
            start: startDate,
            end: endDate
        });
    });

    Object.keys(meetingsByDay).forEach(dayIndex => {
        const dayEl = dayColumns[parseInt(dayIndex)];
        if (!dayEl) return;

        const meetingsForDay = meetingsByDay[dayIndex];

        meetingsForDay.sort((a, b) => a.start - b.start);

        const overlappingGroups = [];
        meetingsForDay.forEach(meeting => {
            let addedToGroup = false;

            for (const group of overlappingGroups) {
                if (group.some(other => other.end > meeting.start && other.start < meeting.end)) {
                    group.push(meeting);
                    addedToGroup = true;
                    break;
                }
            }

            if (!addedToGroup) {
                overlappingGroups.push([meeting]);
            }
        });

        overlappingGroups.forEach(group => {
            const columns = [];
            group.forEach(meeting => {
                let placed = false;
                for (let col = 0; col < columns.length; col++) {
                    if (columns[col].every(otherMeeting => otherMeeting.end <= meeting.start || otherMeeting.start >= meeting.end)) {
                        columns[col].push(meeting);
                        placed = true;
                        break;
                    }
                }
                if (!placed) {
                    columns.push([meeting]);
                }
            });

            const totalColumns = columns.length;
            columns.forEach((col, colIndex) => {
                col.forEach(meeting => {
                    const eventEl = document.createElement('a');
                    eventEl.href = `/meeting/${meeting.id}`;
                    eventEl.title = `${meeting.title}`
                    eventEl.classList.add('event', 'weekly');
                    eventEl.textContent = meeting.title;

                    const position = timeToPosition(meeting.start, meeting.end);
                    eventEl.style.backgroundColor = meeting.color;
                    eventEl.style.position = 'absolute';
                    eventEl.style.top = position.top + 'px';
                    eventEl.style.height = position.height + 'px';

                    eventEl.style.width = `${100 / totalColumns}%`;
                    eventEl.style.left = `${(colIndex * 100) / totalColumns}%`;

                    dayEl.appendChild(eventEl);
                });
            });
        });
    });
};


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
            name_en: title,
            color: color
        });
    });
    
    return result;
}

async function processAndDisplayMeetings() {
    const meetings = await importMeetings();
    console.log(meetings);

    if (currentView === 'monthly') {
        displayMeetings(meetings);
    } else if (currentView === 'weekly') {
        const weekStart = new Date(currentDate);
        weekStart.setDate(currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6);

        const weeklyMeetings = meetings.filter(meeting => {
            const startDate = new Date(meeting.start_time);
            return startDate >= weekStart && startDate <= weekEnd;
        });

        displayMeetings(weeklyMeetings);
    }
}


document.getElementById('toggleView').addEventListener('click', () => {
    currentView = currentView === 'monthly' ? 'weekly' : 'monthly';
    if (currentView === 'monthly') {
        generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
    } else {
        generateWeeklyCalendar(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            currentDate.getDate()
        );
    }
    updateDateRange();
    processAndDisplayMeetings();
});

document.getElementById('goToToday').addEventListener('click', function () {
    currentDate = new Date();
    if (currentView === 'monthly') {
        generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
    } else {
        generateWeeklyCalendar(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            currentDate.getDate()
        );
    }
    updateDateRange();
    processAndDisplayMeetings();
});

document.getElementById('arrow-left').addEventListener('click', function () {
    if (currentView === 'monthly') {
        currentDate.setMonth(currentDate.getMonth() - 1);
        generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
    } else {
        currentDate.setDate(currentDate.getDate() - 7);
        generateWeeklyCalendar(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            currentDate.getDate()
        );
    }
    updateDateRange();
    processAndDisplayMeetings();
});

document.getElementById('arrow-right').addEventListener('click', function () {
    if (currentView === 'monthly') {
        currentDate.setMonth(currentDate.getMonth() + 1);
        generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
    } else {
        currentDate.setDate(currentDate.getDate() + 7);
        generateWeeklyCalendar(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            currentDate.getDate()
        );
    }
    updateDateRange();
    processAndDisplayMeetings();
});

updateDateRange();
generateMonthlyCalendar();
processAndDisplayMeetings();