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

    for (let i = 0; i < 24; i += 0.5) {
        const timeLabel = document.createElement('div');
        timeLabel.classList.add('time-label');

        const hour = Math.floor(i);
        const minutes = (i % 1 === 0) ? '00' : '30';
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

    // --- Widok miesięczny ---
    if (currentView === 'monthly') {
        const days = calendarEl.querySelectorAll('.day');
        days.forEach(day => {
            const eventsContainer = day.querySelector('.events');
            if (eventsContainer) {
                eventsContainer.innerHTML = '';
            }
        });

        meetings.forEach(meeting => {
            const startDate = new Date(meeting.start_time);
            if (
                startDate.getMonth() === currentDate.getMonth() &&
                startDate.getFullYear() === currentDate.getFullYear()
            ) {
                const dayIndex = startDate.getDate();
                const firstDayOffset = getMondayFirstDay(
                    new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay()
                );

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
                    eventEl.textContent = meeting.title;

                    eventEl.style.boxShadow = `inset 0 0 0 2px ${meeting.color}`;

                    if (meeting.logo) {
                        eventEl.style.backgroundImage = `url(${meeting.logo})`;
                        eventEl.style.backgroundPosition = 'center center';
                        eventEl.style.backgroundRepeat = 'no-repeat';
                        eventEl.style.backgroundSize = 'cover';

                        eventEl.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
                        eventEl.style.backgroundBlendMode = 'lighten';
                    } else {
                        eventEl.style.backgroundColor = meeting.color;
                    }

                    eventsContainer.appendChild(eventEl);
                }
            }
        });

    // --- Widok tygodniowy ---
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
                    if (
                        columns[col].every(otherMeeting => otherMeeting.end <= meeting.start || otherMeeting.start >= meeting.end)
                    ) {
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
                    eventEl.title = `${meeting.title}`;
                    eventEl.classList.add('event', 'weekly');
                    eventEl.textContent = meeting.title;

                    const position = timeToPosition(meeting.start, meeting.end);
                    eventEl.style.position = 'absolute';
                    eventEl.style.top = position.top + 'px';
                    eventEl.style.height = position.height + 'px';

                    eventEl.style.width = `${100 / totalColumns}%`;
                    eventEl.style.left = `${(colIndex * 100) / totalColumns}%`;

                    eventEl.style.boxShadow = `inset 0 0 0 2px ${meeting.color}`;

                    if (meeting.logo) {
                        eventEl.style.backgroundImage = `url(${meeting.logo})`;
                        eventEl.style.backgroundPosition = 'center center';
                        eventEl.style.backgroundRepeat = 'no-repeat';
                        eventEl.style.backgroundSize = 'cover';

                        eventEl.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
                        eventEl.style.backgroundBlendMode = 'lighten';

                    } else {
                        eventEl.style.backgroundColor = meeting.color;
                    }

                    dayEl.appendChild(eventEl);
                });
            });
        });
    });
};

async function processAndDisplayMeetings() {
    const meetings = await importMeetings();  // z fetch.js
    console.log(meetings);

    if (currentView === 'monthly') {
        displayMeetings(meetings);
    } else if (currentView === 'weekly') {
        // Wyliczamy zakres tygodnia
        const weekStart = new Date(currentDate);
        weekStart.setDate(currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6);

        // Filtrujemy spotkania, aby wczytać tylko z aktualnego tygodnia
        const weeklyMeetings = meetings.filter(meeting => {
            const startDate = new Date(meeting.start_time);
            return startDate >= weekStart && startDate <= weekEnd;
        });
        displayMeetings(weeklyMeetings);
    }
}

document.getElementById('toggleView').addEventListener('click', () => {
    currentView = (currentView === 'monthly') ? 'weekly' : 'monthly';

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

// Inicjalizacja widoku na starcie
updateDateRange();
generateMonthlyCalendar();
processAndDisplayMeetings();