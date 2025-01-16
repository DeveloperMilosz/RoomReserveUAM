document.addEventListener('DOMContentLoaded', function() {
  const allMapContainers = document.querySelectorAll('.map-container');
  allMapContainers.forEach(container => {
    container.style.display = 'none';
  });
  const parterMap = document.querySelector('.map0');
  if (parterMap) {
    parterMap.style.display = 'block';
  }

  const roomsTableElement = document.getElementById('rooms_table');
  if (roomsTableElement) {
    let roomsList = [];
    try {
      roomsList = JSON.parse(roomsTableElement.textContent);
    } catch (error) {
      console.error('Nie można sparsować JSON z #rooms_table:', error);
    }
    roomsList.forEach(function(roomNumber) {
      const selector = '#room-' + roomNumber.replace('.', '\\.');
      const roomElement = document.querySelector(selector);
      if (roomElement) {
        roomElement.classList.add('occupied');
      }
    });
  }

  const floorSelect = document.getElementById('floor');
  if (floorSelect) {
    floorSelect.addEventListener('change', function() {
      allMapContainers.forEach(container => {
        container.style.display = 'none';
      });
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