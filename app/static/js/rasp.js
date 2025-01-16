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

//czas do spotkania
function parseDateTime(dateString) {
    const [datePart, timePart] = dateString.split(' ');
    const [day, month, year] = datePart.split('.');
    const [hour, minute] = timePart.split(':');
    return new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute));
  }
  
  function pad(num) {
    return num < 10 ? '0' + num : num;
  }
  
  function updateCountdown(start, end, elementId) {
    const now = new Date();
    let text = '';
    if (now >= start && now < end) {
      const diff = end - now;
      const totalHours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff / (1000 * 60)) % 60);
      const seconds = Math.floor((diff / 1000) % 60);
      text = `Czas do końca spotkania:<br>${pad(totalHours)}h ${pad(minutes)}m ${pad(seconds)}s`;
    } else if (now < start) {
      const diff = start - now;
      const totalHours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff / (1000 * 60)) % 60);
      const seconds = Math.floor((diff / 1000) % 60);
      text = `Spotkanie rozpocznie się za:<br>${pad(totalHours)}h ${pad(minutes)}m ${pad(seconds)}s`;
    } else {
      text = 'Spotkanie się zakończyło';
    }
    const countdownElement = document.getElementById(elementId);
    if (countdownElement) {
      countdownElement.innerHTML = text;
    }
  }
  
  function initCountdown() {
    const currentEl = document.querySelector('.meeting-time-current');
    const nextEl = document.querySelector('.meeting-time-next');
    if (currentEl) {
      const text = currentEl.textContent.trim();
      const [startStr, endStr] = text.split(' - ');
      const start = parseDateTime(startStr);
      const end = parseDateTime(endStr);
      setInterval(() => {
        updateCountdown(start, end, 'countdown-current');
      }, 1000);
    }
    if (nextEl) {
      const text = nextEl.textContent.trim();
      const [startStr, endStr] = text.split(' - ');
      const start = parseDateTime(startStr);
      const end = parseDateTime(endStr);
      setInterval(() => {
        updateCountdown(start, end, 'countdown-next');
      }, 1000);
    }
  }
  
  document.addEventListener('DOMContentLoaded', initCountdown);