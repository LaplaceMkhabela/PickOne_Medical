function buildForm(user) {
    let form = `

<div class="form-overlay">
    <div class="form-card">
        <div class="form-header">
            <p>Please ensure your contact details are up to date for medical correspondence.</p>
        </div>

        <form action="#" method="POST">
            <div class="form-grid">
                <div class="form-group full-width">
                    <label for="full-name">Full Name</label>
                    <input type="text" id="name" name="full-name" value="${user['name']}" required>
                </div>

                <div class="form-group">
                    <label for="dob">Date of Birth</label>
                    <input type="date" id="dob" name="dob" required>
                </div>

                <div class="form-group">
                    <label for="gender">Gender</label>
                    <select id="gender" name="gender">
                        <option value="">Select...</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                        <option value="prefer-not-to-say">Prefer not to say</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email" value="${user['email']}" required>
                </div>

                <div class="form-group">
                    <label for="phone">Phone Number</label>
                    <input type="tel" id="phone" name="phone" placeholder="+27 81 533 5675" required>
                </div>

                <div class="form-group full-width">
                    <label for="address">Home Address</label>
                    <textarea id="address" name="address" rows="3" placeholder="Street address, City, Postal code"></textarea>
                </div>
            </div>
        </form>
    </div>
</div>
`

    return form
}

async function update(form) {
    let resp_promise = await fetch('patient/update/profile', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
    let resp_data = resp_promise.json()

    if (resp_data['code'] == '200') {
        Swal.fire({
            title: "Success",
            text: resp_data['msg'],
            icon: "success"
        });
    }
    else {
        Swal.fire({
            title: "Unsuccessful",
            text: resp_data['msg'],
            icon: "error"
        });
    }
}

function update_profile(user) {
    let updateForm = buildForm(user)
    Swal.fire({
        title: 'Personal Information',
        html: `${updateForm}`,
        showCancelButton: true,
        confirmButtonText: 'Update',
        preConfirm: () => {
            const id = user['id'];
            const name = document.getElementById('name').value;
            const dob = document.getElementById('dob').value;
            const gender = document.getElementById('gender').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const address = document.getElementById('address').value;

            if (!dob || !gender || !phone || !address) {
                Swal.showValidationMessage('All fields are required');
                return false;
            }

            return { isConfirmed: true, "name": name, "dob": dob, "gender": gender, "email": email, "phone": phone, "address": address,"id":id }
        }
    }).then((result) => {
        if (result.isConfirmed) {
            update(result.value)
        }
    });
}

