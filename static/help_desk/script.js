function time() {
    const now = new Date();
    let time_now = now.toTimeString().slice(0, 5);
    document.getElementById('time').value = time_now
}

async function new_appointment(result) {
    let url = window.location.href + "/appointments/new"
    let resp = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(result.value) })
    data = await resp.json()

    if (data["code"] == "200") {
        Swal.fire({
            title: 'Success',
            text: data['msg'],
            icon: 'success',
            showCancelButton: false,
            confirmButtonText: 'Ok'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.reload();
            }
        });
    }
    else {
        Swal.fire({
            title: 'Failure',
            text: data['msg'],
            icon: 'error',
            showCancelButton: false,
            confirmButtonText: 'Ok'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.reload();
            }
        });
    }
}

function newAppointmentDialog() {
    Swal.fire({
        title: 'Patient Appointment',
        html: `
                <div class="input-group flex-nowrap my-2">
                    <span class="input-group-text">Patient Name</span>
                    <input id="patientName" type="text" class="form-control" placeholder="Nikola Tesla" aria-label="bp" aria-describedby="addon-wrapping">
                </div>
                <div class="input-group flex-nowrap my-2">
                    <span class="input-group-text">Patient Id</span>
                    <input id="patientId" type="text" class="form-control" placeholder="Pat001" aria-label="bp" aria-describedby="addon-wrapping">
                </div>
                <div class="input-group flex-nowrap my-2">
                    <span class="input-group-text" >Time</span>
                    <input id="time" type="time" onclick="time()" class="form-control" aria-label="time" aria-describedby="addon-wrapping">
                </div>
                <div class="input-group flex-nowrap my-2">
                    <span class="input-group-text">Date</span>
                    <input id="date" type="date" class="form-control" aria-label="date" aria-describedby="addon-wrapping">
                </div>
            `,
        showCancelButton: true,
        confirmButtonText: 'Add',
        preConfirm: () => {
            const id = document.getElementById('patientId').value;
            const name = document.getElementById('patientName').value;
            const time = document.getElementById('time').value;
            const date = document.getElementById('date').value;

            if (!id || !time || !date || !name) {
                Swal.showValidationMessage('All fields are required');
                return false;
            }

            return { isConfirmed: true, "id": id, "name": name, "date": date, "time": time }
        }
    }).then((result) => {
        if (result.isConfirmed) {
            new_appointment(result)
        }
    });
}

const monthYear = document.getElementById("monthYear");
  const daysEl = document.getElementById("days");
  let current = new Date()
  let selectedDay = current.getDay();

  function renderCalendar() {
    daysEl.innerHTML = "";

    const year = current.getFullYear();
    const month = current.getMonth();

    monthYear.textContent = current.toLocaleString("default", {
      month: "long",
      year: "numeric"
    });

    const firstDay = new Date(year, month, 1);
    const startDay = (firstDay.getDay() + 6) % 7; 
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();

    // Previous month filler
    for (let i = startDay - 1; i >= 0; i--) {
      const d = document.createElement("div");
      d.textContent = daysInPrevMonth - i;
      d.className = "outside";
      daysEl.appendChild(d);
    }

    // Current month days
    for (let d = 1; d <= daysInMonth; d++) {
      const day = document.createElement("div");
      day.textContent = d;

      if (d === selectedDay &&
          month === 1 &&
          year === 2024) {
        day.classList.add("selected");
      }

      day.onclick = () => {
        selectedDay = d;
        renderCalendar();
      };

      daysEl.appendChild(day);
    }

    // Next month filler
    const totalCells = daysEl.children.length;
    const remaining = 42 - totalCells;

    for (let i = 1; i <= remaining; i++) {
      const d = document.createElement("div");
      d.textContent = i;
      d.className = "outside";
      daysEl.appendChild(d);
    }
  }

  document.getElementById("prev").onclick = () => {
    current.setMonth(current.getMonth() - 1);
    selectedDay = null;
    renderCalendar();
  };

  document.getElementById("next").onclick = () => {
    current.setMonth(current.getMonth() + 1);
    selectedDay = null;
    renderCalendar();
  };


  function parsePythonListString(str) {
  // 1. Decode HTML entities
  const decoded = str
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"');

  // 2. Convert Python list syntax to JS/JSON
  const jsonLike = decoded.replace(/'/g, '"');

  // 3. Parse into JS array
  return JSON.parse(jsonLike);
}


  renderCalendar();