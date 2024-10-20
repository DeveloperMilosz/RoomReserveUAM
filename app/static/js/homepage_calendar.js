let currentView = 'monthly';
let currentDate = new Date();

function getMondayFirstDay(weekday) {
    return (weekday + 6) % 7;
}

function timeToPosition(start, end) {
    const startTime = new Date(start);
    const endTime = new Date(end);
    const startHour = startTime.getUTCHours() + startTime.getUTCMinutes() / 60;
    const endHour = endTime.getUTCHours() + endTime.getUTCMinutes() / 60;

    const eventDuration = endHour - startHour;
    const topPosition = startHour * 60;
    const eventHeight = eventDuration * 60;

    return {
        top: topPosition,
        height: eventHeight
    };
}

function updateDateRange() {
    const dateRangeEl = document.getElementById('dateRange');
    
    if (currentView === 'monthly') {
        const options = { year: 'numeric', month: 'long' };
        const formattedMonth = currentDate.toLocaleDateString('pl-PL', options);
        dateRangeEl.textContent = formattedMonth;
    } else if (currentView === 'weekly') {
        const weekStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6);

        const options = { day: 'numeric', month: 'long', year: 'numeric' };
        const formattedStart = weekStart.toLocaleDateString('pl-PL', options);
        const formattedEnd = weekEnd.toLocaleDateString('pl-PL', options);
        
        dateRangeEl.textContent = `${formattedStart} - ${formattedEnd}`;
    }
}

function generateMonthlyCalendar(year, month) {
    const calendarEl = document.getElementById('calendar');
    calendarEl.innerHTML = '';
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = getMondayFirstDay(new Date(year, month, 1).getDay());

    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.classList.add('day');
        calendarEl.appendChild(emptyDay);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(year, month, day);
        const dayEl = document.createElement('div');
        dayEl.classList.add('day');
        
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = date.toLocaleDateString('pl-PL', options);
        
        dayEl.innerHTML = `<strong>${formattedDate}</strong>`;
        calendarEl.appendChild(dayEl);
    }
}

function generateWeeklyCalendar(year, month, day) {
    const calendarEl = document.getElementById('calendar');
    calendarEl.innerHTML = '';
    const currentDate = new Date(year, month, day);
    const startOfWeek = currentDate.getDate() - getMondayFirstDay(currentDate.getDay()) + 1;

    const hourColumn = document.createElement('div');
    hourColumn.classList.add('hour');
    for (let i = 0; i < 24; i++) {
        const timeLabel = document.createElement('div');
        timeLabel.classList.add('time-label');
        timeLabel.textContent = `${String(i).padStart(2, '0')}:00`;
        hourColumn.appendChild(timeLabel);
    }
    calendarEl.appendChild(hourColumn);

    for (let i = 0; i < 7; i++) {
        const weekDay = new Date(year, month, startOfWeek + i - 1);
        const dayEl = document.createElement('div');
        dayEl.classList.add('day', 'weekly');
        
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = weekDay.toLocaleDateString('pl-PL', options);
        
        dayEl.innerHTML = `<strong>${formattedDate}</strong>`;
        calendarEl.appendChild(dayEl);
    }
}

function displayMeetingsInWeek(meetings) {
    meetings.forEach(meeting => {
        const startDate = new Date(meeting.start_time);
        const endDate = new Date(meeting.end_time);

        const currentWeekStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));
        const currentWeekEnd = new Date(currentWeekStart);
        currentWeekEnd.setDate(currentWeekStart.getDate() + 6);

        if (startDate >= currentWeekStart && startDate <= currentWeekEnd) {
            const dayIndex = getMondayFirstDay(startDate.getDay());

            const dayEl = document.querySelector(`#calendar .day.weekly:nth-child(${dayIndex + 2})`);

            if (dayEl) {
                const eventEl = document.createElement('div');
                eventEl.classList.add('event', 'weekly');
                eventEl.textContent = meeting.title;

                const position = timeToPosition(meeting.start_time, meeting.end_time);
                eventEl.style.position = "absolute";
                eventEl.style.top = position.top + 'px';
                eventEl.style.height = position.height + 'px';

                dayEl.appendChild(eventEl);
            }
        }
    });
}

async function fetchMeetings() {
    try {
        const response = await fetch('/get-meetings/');
        const meetings = await response.json();

        if (currentView === 'monthly') {
            displayMeetingsInMonth(meetings);
        } else {
            displayMeetingsInWeek(meetings);
        }
    } catch (error) {
        console.error('Błąd podczas pobierania wydarzeń:', error);
    }
}

document.getElementById('toggleView').addEventListener('click', function () {
    const calendarEl = document.getElementById('calendar');
    // const weekdaysEl = document.querySelector('.weekdays');

    if (currentView === 'monthly') {
        currentView = 'weekly';
        calendarEl.classList.remove('monthly');
        calendarEl.classList.add('weekly');
        // weekdaysEl.classList.add('weekly');
        // weekdaysEl.classList.remove('monthly');
        generateWeeklyCalendar(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
    } else {
        currentView = 'monthly';
        calendarEl.classList.remove('weekly');
        calendarEl.classList.add('monthly');
        // weekdaysEl.classList.add('monthly');
        // weekdaysEl.classList.remove('weekly');
        generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
    }
    updateDateRange();
    fetchMeetings();
});

document.getElementById('prev').addEventListener('click', function () {
    if (currentView === 'monthly') {
        currentDate.setMonth(currentDate.getMonth() - 1);
        generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
    } else {
        currentDate.setDate(currentDate.getDate() - 7);
generateWeeklyCalendar(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
}
updateDateRange();
fetchMeetings();
});

document.getElementById('next').addEventListener('click', function () {
if (currentView === 'monthly') {
    currentDate.setMonth(currentDate.getMonth() + 1);
    generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
} else {
    currentDate.setDate(currentDate.getDate() + 7);
    generateWeeklyCalendar(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
}
updateDateRange();
fetchMeetings();
});

function displayMeetingsInMonth(meetings) {
meetings.forEach(meeting => {
    const startDate = new Date(meeting.start_time);
    const meetingMonth = startDate.getMonth();
    const meetingDay = startDate.getDate();

    if (meetingMonth === currentDate.getMonth()) {
        const dayEl = document.querySelector(`#calendar .day:nth-child(${meetingDay + new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay() - 1})`);
        
        if (dayEl) {
            const eventEl = document.createElement('div');
            eventEl.classList.add('event');
            eventEl.textContent = meeting.title;
            dayEl.appendChild(eventEl);
        }
    }
});
}

updateDateRange();
generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
fetchMeetings();