fetch('/api/free-rooms/')
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  console.log(response.json)
  return response.json();
})