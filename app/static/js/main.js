  document.addEventListener('DOMContentLoaded', function() {
    var currentMonday = getMonday(new Date());
    var selectedCell = null;
    renderWeek(currentMonday);
  
    document.getElementById('today').addEventListener('click', function() {
      currentMonday = getMonday(new Date());
      renderWeek(currentMonday);
    });
  
    document.getElementById('prev-week').addEventListener('click', function() {
      var prevMonday = new Date(currentMonday);
      prevMonday.setDate(prevMonday.getDate() - 7);
      currentMonday = prevMonday;
      renderWeek(currentMonday);
    });
  
    document.getElementById('next-week').addEventListener('click', function() {
      var nextMonday = new Date(currentMonday);
      nextMonday.setDate(nextMonday.getDate() + 7);
      currentMonday = nextMonday;
      renderWeek(currentMonday);
    });
  
    document.getElementById('cancel-event').addEventListener('click', function() {
      hideEventForm();
    });
  
    document.getElementById('save-event').addEventListener('click', function() {
      var eventTitle = document.getElementById('event-title').value;
      var eventStartTime = document.getElementById('event-start-time').value;
      var eventEndTime = document.getElementById('event-end-time').value;
  
      if (selectedCell && eventTitle && eventStartTime && eventEndTime) {
        var eventDisplay = document.createElement('div');
        eventDisplay.textContent = `${eventTitle} (${eventStartTime} - ${eventEndTime})`;
        eventDisplay.classList.add('event-entry');
  
        // Oblicz pozycję i wysokość w minutach
        var startMinutes = getMinutesFromTime(eventStartTime);
        var endMinutes = getMinutesFromTime(eventEndTime);
        var duration = endMinutes - startMinutes;
  
        eventDisplay.style.top = (startMinutes - 360) + "px"; // od godziny 6:00 (360 minut od północy)
        eventDisplay.style.height = duration + "px";
  
        selectedCell.appendChild(eventDisplay);
        hideEventForm();
      }
    });
  
    function renderWeek(monday) {
      var tableBody = document.querySelector('#calendar tbody');
      var tableHead = document.querySelector('#calendar thead tr');
      tableBody.innerHTML = '';
      tableHead.innerHTML = '';
  
      // Dodaj kolumnę godzin po lewej stronie
      var timeColumn = document.createElement('th');
      timeColumn.textContent = 'Godzina';
      tableHead.appendChild(timeColumn);
  
      // Renderuj dni tygodnia
      for (var i = 0; i < 7; i++) {
        var currentDay = new Date(monday);
        currentDay.setDate(monday.getDate() + i);
  
        // Nagłówek dnia
        var dayOfWeek = currentDay.toLocaleDateString('pl-PL', { weekday: 'long' });
        var dayOfMonth = currentDay.getDate();
        var month = currentDay.getMonth() + 1;
        var year = currentDay.getFullYear();
  
        var columnHeader = document.createElement('th');
        columnHeader.textContent = `${dayOfWeek} (${dayOfMonth}.${month}.${year})`;
        tableHead.appendChild(columnHeader);
      }
  
      // Renderuj godziny i dni w tabeli
      for (var hour = 6; hour <= 21; hour++) {
        var row = document.createElement('tr');
  
        // Kolumna z godzinami
        var timeCell = document.createElement('td');
        timeCell.textContent = `${hour}:00`;
        timeCell.classList.add('calendar-time');
        row.appendChild(timeCell);
  
        // Kolumny dla dni tygodnia
        for (var i = 0; i < 7; i++) {
          var dayCell = document.createElement('td');
          dayCell.classList.add('calendar-day');
          dayCell.addEventListener('click', function() {
            selectedCell = this;
            showEventForm();
          });
          row.appendChild(dayCell);
        }
  
        tableBody.appendChild(row);
      }
    }
  
    function getMonday(date) {
      var day = date.getDay() || 7;
      if (day !== 1) {
        date.setHours(-24 * (day - 1));
      }
      return date;
    }
  
    function showEventForm() {
      document.getElementById('event-form').style.display = 'block';
    }
  
    function hideEventForm() {
      document.getElementById('event-form').style.display = 'none';
      document.getElementById('event-title').value = '';
      document.getElementById('event-start-time').value = '';
      document.getElementById('event-end-time').value = '';
    }
  
    function getMinutesFromTime(time) {
      var [hours, minutes] = time.split(':').map(Number);
      return hours * 60 + minutes;
    }

    
  });