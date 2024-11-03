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
    const topPosition = startHour * 60;
    const eventHeight = (endHour - startHour) * 60;

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

        const formattedStart = `${String(weekStart.getDate()).padStart(2, '0')}.${String(weekStart.getMonth() + 1).padStart(2, '0')}.${weekStart.getFullYear()}`;
        const formattedEnd = `${String(weekEnd.getDate()).padStart(2, '0')}.${String(weekEnd.getMonth() + 1).padStart(2, '0')}.${weekEnd.getFullYear()}`;
        
        dateRangeEl.textContent = `${formattedStart} - ${formattedEnd}`;
    }
}

function updateWeekdaysWithDates() {
    const weekdaysEl = document.querySelector('.weekdays');
    weekdaysEl.innerHTML = '';

    const weekStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));

    const daysOfWeek = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'];

    for (let i = 0; i < 7; i++) {
        const dayEl = document.createElement('div');
        const currentDay = new Date(weekStart);
        currentDay.setDate(weekStart.getDate() + i);

        const formattedDate = `${String(currentDay.getDate()).padStart(2, '0')}.${String(currentDay.getMonth() + 1).padStart(2, '0')}.${currentDay.getFullYear()}`;

        dayEl.innerHTML = `<strong>${daysOfWeek[i]}</strong> ${formattedDate}`;
        weekdaysEl.appendChild(dayEl);
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
        const formattedDate = date.toLocaleDateString('pl-PL').replace(/\//g, '.');
        
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
        

        const formattedDate = weekDay.toLocaleDateString('pl-PL').replace(/\//g, '.');
        dayEl.innerHTML = `<strong>${formattedDate}</strong>`;
        calendarEl.appendChild(dayEl);
    }
}

function displayMeetingsInWeek(meetings) {
    const dayMeetings = {};

    meetings.forEach(meeting => {
        const startDate = new Date(meeting.start_time);
        const endDate = new Date(meeting.end_time);

        const currentWeekStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - getMondayFirstDay(currentDate.getDay()));
        const currentWeekEnd = new Date(currentWeekStart);
        currentWeekEnd.setDate(currentWeekStart.getDate() + 6);

        if (startDate >= currentWeekStart && startDate <= currentWeekEnd) {
            const dayIndex = getMondayFirstDay(startDate.getDay());

            if (!dayMeetings[dayIndex]) {
                dayMeetings[dayIndex] = [];
            }

            dayMeetings[dayIndex].push({

                id: meeting.id,
                start_time: startDate,
                end_time: endDate,
                title: meeting.title,
                color: meeting.color
            });
        }
    });

    Object.keys(dayMeetings).forEach(dayIndex => {
        const dayEl = document.querySelector(`#calendar .day.weekly:nth-child(${parseInt(dayIndex) + 2})`);

        if (dayEl) {
            const meetingsForDay = dayMeetings[dayIndex];

            meetingsForDay.forEach((meeting, index) => {
                const overlappingMeetings = meetingsForDay.filter(otherMeeting => {
                    return (
                        otherMeeting.start_time < meeting.end_time &&
                        otherMeeting.end_time > meeting.start_time
                    );
                });

                const overlapCount = overlappingMeetings.length;
                const meetingWidth = 100 / overlapCount;

                const eventEl = document.createElement('a');
                eventEl.href="/meeting/"+meeting.id;
                eventEl.classList.add('event', 'weekly');
                eventEl.textContent = meeting.title;

                const position = timeToPosition(meeting.start_time, meeting.end_time);
                eventEl.style.backgroundColor = meeting.color;
                eventEl.style.position = "absolute";
                eventEl.style.top = position.top + 'px';
                eventEl.style.height = position.height + 'px';
                eventEl.style.width = meetingWidth + '%';
                eventEl.style.left = (index * meetingWidth) + '%';
                
                dayEl.appendChild(eventEl);
            });
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
        console.error('Error while getting events', error);
    }
}

document.getElementById('toggleView').addEventListener('click', function () {
    const calendarEl = document.getElementById('calendar');

    if (currentView === 'monthly') {
        currentView = 'weekly';
        calendarEl.classList.remove('monthly');
        calendarEl.classList.add('weekly');
        generateWeeklyCalendar(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
    } else {
        currentView = 'monthly';
        calendarEl.classList.remove('weekly');
        calendarEl.classList.add('monthly');
        generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
    }
    updateDateRange();
    fetchMeetings();
});

document.getElementById('arrow-left').addEventListener('click', function () {
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

document.getElementById('arrow-right').addEventListener('click', function () {
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
                let eventsContainer = dayEl.querySelector('.events');
                if (!eventsContainer) {
                    eventsContainer = document.createElement('a');
                    eventsContainer.href="/meeting/"+meeting.id;
                    eventsContainer.classList.add('events');
                    dayEl.appendChild(eventsContainer);
                }

                const eventEl = document.createElement('div');
                eventEl.style.backgroundColor = meeting.color;
                eventEl.classList.add('event');
                eventEl.textContent = meeting.title;
                eventsContainer.appendChild(eventEl);
            }
        }
    });
}


updateDateRange();
generateMonthlyCalendar(currentDate.getFullYear(), currentDate.getMonth());
fetchMeetings();