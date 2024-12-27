document.addEventListener("DOMContentLoaded", function () {
  const noteElements = document.querySelectorAll(".note");
  const statusColumns = document.querySelectorAll(".status-column");
  const currentGroupId = CURRENT_GROUP_ID; // Zmienna przekazana z szablonu

  let draggedNote = null;

  noteElements.forEach((note) => {
      note.addEventListener("dragstart", (e) => {
          draggedNote = note;
          e.dataTransfer.effectAllowed = "move";
          setTimeout(() => {
              note.classList.add("dragging");
          }, 0);
      });

      note.addEventListener("dragend", () => {
          draggedNote.classList.remove("dragging");
          draggedNote = null;
      });
  });

  statusColumns.forEach((column) => {
      column.addEventListener("dragover", (e) => {
          e.preventDefault();

          const afterElement = getDragAfterElement(column, e.clientY);
          if (!afterElement) {
              column.querySelector(".note-container").appendChild(draggedNote);
          } else {
              column.querySelector(".note-container").insertBefore(draggedNote, afterElement);
          }
      });

      column.addEventListener("drop", (e) => {
          e.preventDefault();

          const newStatusId = column.getAttribute("data-status-id");
          const noteId = draggedNote.getAttribute("data-note-id");

          updateNoteStatus(noteId, newStatusId).then(() => {
              saveNoteOrder();
          });
      });
  });

  function getDragAfterElement(container, y) {
      const draggableElements = [
          ...container.querySelectorAll(".note:not(.dragging)"),
      ];

      return draggableElements.reduce(
          (closest, child) => {
              const box = child.getBoundingClientRect();
              const offset = y - box.top - box.height / 2;
              if (offset < 0 && offset > closest.offset) {
                  return { offset: offset, element: child };
              } else {
                  return closest;
              }
          },
          { offset: Number.NEGATIVE_INFINITY }
      ).element;
  }

  function updateNoteStatus(noteId, statusId) {
      return fetch("/api/update_note_status/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({
              note_id: noteId,
              status_id: statusId,
              group_id: currentGroupId,
          }),
      })
          .then((response) => response.json())
          .then((data) => {
              if (!data.success) {
                  console.error("Error updating note status:", data.error);
              }
          })
          .catch((err) => {
              console.error("AJAX error:", err);
          });
  }

  function saveNoteOrder() {
      const notesOrderData = [];

      document.querySelectorAll(".status-column").forEach((column) => {
          const statusId = column.getAttribute("data-status-id");
          const noteNodes = column.querySelectorAll(".note");

          noteNodes.forEach((note, index) => {
              notesOrderData.push({
                  id: note.getAttribute("data-note-id"),
                  status_id: statusId,
                  order: index,
              });
          });
      });

      fetch("/api/save_note_order/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({ notes: notesOrderData, group_id: currentGroupId }),
      })
          .then((resp) => resp.json())
          .then((data) => {
              if (!data.success) {
                  console.error("Error saving note order:", data.error);
              }
          })
          .catch((err) => {
              console.error("Error in saving note order:", err);
          });
  }

  const manageStatusesBtn = document.getElementById("manage-statuses-btn");
  const manageStatusesPopup = document.getElementById("manage-statuses-popup");
  const popupOverlay = document.getElementById("popup-overlay");
  const closePopupBtn = document.getElementById("close-popup-btn");

  manageStatusesBtn.addEventListener("click", () => {
      manageStatusesPopup.style.display = "block";
      popupOverlay.style.display = "block";
  });

  closePopupBtn.addEventListener("click", () => {
      manageStatusesPopup.style.display = "none";
      popupOverlay.style.display = "none";
  });

  const addStatusForm = document.getElementById("add-status-form");
  addStatusForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const statusNameInput = document.getElementById("status-name");
      const statusColorInput = document.getElementById("status-color");

      const name = statusNameInput.value.trim();
      const color = statusColorInput.value;

      if (!name) {
          alert("Nazwa statusu jest wymagana");
          return;
      }

      fetch("/api/add_status/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({ name, color, group_id: currentGroupId }),
      })
          .then((resp) => resp.json())
          .then((data) => {
              if (data.success) {
                  window.location.reload();
              } else {
                  console.error(data.error || "Nie można dodać statusu.");
              }
          })
          .catch((err) => {
              console.error("Error:", err);
          });
  });

  document.querySelectorAll(".btn-delete-status").forEach((btn) => {
      btn.addEventListener("click", function () {
          const statusId = this.getAttribute("data-status-id");
          const groupId = this.getAttribute("data-group-id");

          if (!confirm("Czy na pewno chcesz usunąć ten status?")) {
              return;
          }

          fetch(`/api/delete_status/${statusId}/`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": getCSRFToken(),
              },
              body: JSON.stringify({ status_id: statusId, group_id: groupId }),
          })
              .then((resp) => resp.json())
              .then((data) => {
                  if (data.success) {
                      window.location.reload();
                  } else {
                      console.error(data.error || "Nie można usunąć statusu.");
                  }
              })
              .catch((err) => {
                  console.error("Error:", err);
              });
      });
  });

  function getCSRFToken() {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, 10) === "csrftoken=") {
                  cookieValue = cookie.substring(10);
                  break;
              }
          }
      }
      return cookieValue;
  }
});