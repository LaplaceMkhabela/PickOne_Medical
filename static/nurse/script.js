function updateVitals(patientId) {
    Swal.fire({
        title: '',
        html: `
        
        <div class="dialog-container">
        <div class="dialog-header">
            <h1>Health Metrics</h1>
            <p>Update vital signs and health measurements</p>
        </div>
        
        <div class="dialog-body">
            <div class="input-group">
                <label for="systolic">
                    <span class="metric-indicator systolic-indicator"></span>
                    Blood Pressure - Systolic (mmHg)
                </label>
                <div class="blood-pressure-container">
                    <div>
                        <select id="systolic">
                            <option value="" disabled selected>Select systolic value</option>
                            <option value="90">90</option>
                            <option value="100">100</option>
                            <option value="110">110</option>
                            <option value="120">120 (Normal)</option>
                            <option value="130">130</option>
                            <option value="140">140 (High)</option>
                            <option value="150">150</option>
                            <option value="160">160</option>
                            <option value="170">170</option>
                            <option value="180">180</option>
                        </select>
                    </div>
                    <div>
                        <label for="diastolic">
                            <span class="metric-indicator diastolic-indicator"></span>
                            Diastolic (mmHg)
                        </label>
                        <select id="diastolic">
                            <option value="" disabled selected>Select diastolic value</option>
                            <option value="50">50</option>
                            <option value="60">60 (Normal)</option>
                            <option value="70">70</option>
                            <option value="80">80 (High)</option>
                            <option value="90">90</option>
                            <option value="100">100</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="input-group">
                <label for="temperature">
                    <span class="metric-indicator temp-indicator"></span>
                    Temperature (°C)
                </label>
                <input type="number" id="temperature" min="35" max="42" step="0.1" placeholder="Enter temperature in Celsius">
                <div class="metric-note">Normal body temperature is approximately 37°C</div>
            </div>
            
            <div class="input-group">
                <label class="w-top" for="weight">
                    <span class="metric-indicator weight-indicator"></span>
                    Weight (kg)
                </label>
                <div class="slider-info w-top">
                    
                    <span>Current: <span class="slider-value" id="current-weight">70</span> kg</span>
                    
                </div>
                <div class="range-slider-container">
                    <input type="range" style="width:100%" id="weight" min="5" max="180" value="70" step="0.5" onchange="weightValue()">
                </div>
                <div class="metric-note">Drag the slider to select your weight</div>
            </div>
        </div>
    </div>

    `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: 'Update',
        preConfirm: () => {
            const weight = document.getElementById('weight').value;
            const bp_systolic = document.getElementById('systolic').value;
            const bp_diastolic = document.getElementById('diastolic').value;
            const temp = document.getElementById('temperature').value;

            if (!weight || !bp_systolic || !bp_diastolic || !temp) {
                Swal.showValidationMessage('All fields are required');
                return false;
            }

            return {
                isConfirmed: true,
                id: patientId,
                weight,
                bp_systolic,
                bp_diastolic,
                temp,
            };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            update(result)
        }
    });
}


function weightValue() {
    document.getElementById('current-weight').textContent = document.getElementById('weight').value;
}

async function update(result) {
    let resp_promise = await fetch('/nurse/update/vitals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(result.value)
    })


    let resp_data = await resp_promise.json()

    if (resp_data['code'] == '200') {
        Swal.fire('Success', 'Vitals updated successfully', 'success');
        Swal.fire({
            title: "Success",
            text: "Vitals updated successfully",
            icon: "success",
            showCancelButton: false,
            confirmButtonText: "Ok"
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.reload()
            }
        });
    }
    else {
        Swal.fire('Error', resp_data['msg'], 'error');
    }
}
