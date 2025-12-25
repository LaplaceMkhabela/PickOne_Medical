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