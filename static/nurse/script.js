function updateVitals(patientId) {
    Swal.fire({
        title: 'Update Patient Vitals',
        html: `
        
        <div class="input-group flex-nowrap">
            <span class="input-group-text" id="weightValue">Weight</span>
            <input type="range" onchange="weight()"  id="weight" class="form-range" min="0" max="1000" value="50" >
        </div>
        <div class="input-group flex-nowrap">
            <span class="input-group-text" id="bp">Blood Pressure</span>
            <input type="text" class="form-control" placeholder="120/80" aria-label="bp" aria-describedby="addon-wrapping">
        </div>
        <div class="input-group flex-nowrap">
            <span class="input-group-text" id="pulse">Pulse</span>
            <input type="text" class="form-control" placeholder="bpm" aria-label="bp" aria-describedby="addon-wrapping">
        </div>
        <div class="input-group flex-nowrap">
            <span class="input-group-text" id="date">Date</span>
            <input type="date" class="form-control" aria-label="date" aria-describedby="addon-wrapping">
        </div>
        <div class="input-group flex-nowrap">
            <span class="input-group-text">Time</span>
            <input type="time" id="time" class="form-control" onclick="time()" aria-label="time" aria-describedby="addon-wrapping">
        </div>



    `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: 'Update',
        preConfirm: () => {
            const weight = document.getElementById('weight').value;
            const bp = document.getElementById('bp').value;
            const temp = document.getElementById('pulse').value;

            if (!weight || !bp || !pulse) {
                Swal.showValidationMessage('All fields are required');
                return false;
            }

            return {
                patient_id: patientId,
                weight,
                bp,
                temp,
            };
        }
    }).then(async (result) => {
        if (result.isConfirmed) {
            let resp_promise = fetch('/nurse/update-vitals', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(result.value)
            })


            let resp_data = await resp_promise.json()

            if (resp_data['code'] == '200') { 
                Swal.fire('Success', 'Vitals updated successfully', 'success'); 
            }
            else {
                Swal.fire('Error', resp_data['msg'], 'error');
            }
        }
    });
}