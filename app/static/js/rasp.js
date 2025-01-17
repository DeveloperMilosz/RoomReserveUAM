//pogoda
'use strict'
const monthNames = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
    "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
];

let dateObj = new Date();
let month = monthNames[dateObj.getUTCMonth()];
let day = dateObj.getUTCDate();
let year = dateObj.getUTCFullYear();

let newdate = `${month} ${day}, ${year}`;

const app = document.querySelector('.weather');

fetch('https://api.openweathermap.org/data/2.5/weather?id=3089033&APPID=2d48b1d7080d09ea964e645ccd1ec93f&units=metric&lang=pl')
    .then(response => response.json())
    .then(data => {
        console.log(data)

        app.insertAdjacentHTML('afterbegin', `<div class="titlebar">
    <div class="clock" id="clock"></div>
    <p class="date">${newdate}</p>
    <h4 class="city">${data.name}</h4>
    <p class="description">${data.weather[0].description}</p>
</div>
<div class="temperature">
    <img src="http://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png" />
    <h2>${Math.round(data.main.temp)}°C</h2>
</div>
<div class="extra">
    <div class="info">
        <h5>Wiatr</h5>
        <p>${data.wind.speed}mps</p>
    </div>
    <div class="info">
        <h5>Wilgotność</h5>
        <p>${data.main.humidity}%</p>
    </div>
</div>`)
});

// zegar na pogodzie
function updateClock() {
  const clockElement = document.getElementById('clock');
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  clockElement.textContent = `${hours}:${minutes}:${seconds}`;
}
setInterval(updateClock, 1000);
window.onload = updateClock;

document.addEventListener('DOMContentLoaded', function() {
  function parseDateString(dateString) {
      const [datePart, timePart] = dateString.trim().split(' ');
      const [day, month, year] = datePart.split('.');
      const [hour, minute] = timePart.split(':');
      return new Date(year, month - 1, day, hour, minute);
  }
  function msToDHMS(ms) {
      ms = Math.floor(ms / 1000);
      let d = Math.floor(ms / 86400);
      ms %= 86400;
      let h = Math.floor(ms / 3600);
      ms %= 3600;
      const m = Math.floor(ms / 60);
      const s = ms % 60;
      if (d > 0) {
          h += d * 24;
          d = 0;
      }
      let parts = [];
      if (h) parts.push(h + "g");
      if (m) parts.push(m + "m");
      parts.push(s + "s");
      return parts.join(" ");
  }
  function updateTimers() {
      const meetings = document.querySelectorAll('.meeting');
      const now = new Date();
      meetings.forEach(meeting => {
          const startTimeP = meeting.querySelector('.extra .info:nth-of-type(1) p');
          const endTimeP = meeting.querySelector('.extra .info:nth-of-type(2) p');
          const timer = meeting.querySelector('.timer');
          if (!startTimeP || !endTimeP || !timer) return;
          const startTime = parseDateString(startTimeP.textContent);
          const endTime = parseDateString(endTimeP.textContent);
          const timeToStart = startTime - now;
          const timeToEnd = endTime - now;
          let message = '';
          if (now >= startTime && now < endTime) {
              message = 'Spotkanie skończy się za: <strong>' + msToDHMS(timeToEnd) + '</strong>';
          } else if (now < startTime) {
              message = 'Spotkanie zacznie się za: <strong>' + msToDHMS(timeToStart) + '</strong>';
          } else {
              message = 'Spotkanie już się zakończyło.';
          }
          timer.innerHTML = message;
      });
  }
  updateTimers();
  setInterval(updateTimers, 1000);
});