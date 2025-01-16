document.addEventListener('DOMContentLoaded', function() {
  /* 1. Ukrywamy wszystkie mapy i pokazujemy mapę parteru */
  const allMapContainers = document.querySelectorAll('.map-container');
  allMapContainers.forEach(container => {
    container.style.display = 'none';
  });
  // Domyślnie pokaż parter
  const parterMap = document.querySelector('.map0');
  if (parterMap) {
    parterMap.style.display = 'block';
  }

  /* 2. Pobranie listy sal z #rooms_table i nadanie .occupied */
  const roomsTableElement = document.getElementById('rooms_table');
  if (roomsTableElement) {
    let roomsList = [];
    try {
      roomsList = JSON.parse(roomsTableElement.textContent);
    } catch (error) {
      console.error('Nie można sparsować JSON z #rooms_table:', error);
    }
    // Dla każdej sali typu "0.35" => #room-0\.35 => dodajemy klasę .occupied
    roomsList.forEach(function(roomNumber) {
      const selector = '#room-' + roomNumber.replace('.', '\\.');
      const roomElement = document.querySelector(selector);
      if (roomElement) {
        roomElement.classList.add('occupied');
      }
    });
  }

  /* 3. Reagowanie na zmianę w select (bez submit) - przełączanie map */
  const floorSelect = document.getElementById('floor');
  if (floorSelect) {
    floorSelect.addEventListener('change', function() {
      // Ukryj wszystkie mapy
      allMapContainers.forEach(container => {
        container.style.display = 'none';
      });
      // Wyświetl tylko mapę zgodną z wybraną opcją
      const selectedFloor = floorSelect.value;
      switch (selectedFloor) {
        case 'parter':
          document.querySelector('.map0').style.display = 'block';
          break;
        case 'pietro1':
          document.querySelector('.map1').style.display = 'block';
          break;
        case 'pietro2':
          document.querySelector('.map2').style.display = 'block';
          break;
      }
    });
  }
});