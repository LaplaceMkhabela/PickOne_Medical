document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. LOGIN FORM LOGIC ---
    const loginForm = document.getElementById('loginForm');

    // Only run this if we are on the login page
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const role = document.getElementById('role').value;
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (role && username && password) {
                // Simulate Login
                alert(`Logging you in as a: ${role.toUpperCase()}`);
                
                // Redirect logic
                if (role === 'doctor') {
                    window.location.href = "doctor_dashboard.html";
                } else if (role === 'patient') {
                    alert("Patient Dashboard coming soon!");
                } else {
                    alert("Nurse Dashboard coming soon!");
                }
            } else {
                alert("Please select a role and fill in all fields.");
            }
        });
    }

    // --- 2. PASSWORD TOGGLE LOGIC ---
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', () => {
            // Toggle type
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            // Toggle Image Icon
            if (type === 'password') {
                togglePassword.src = "https://i.ibb.co/TxrRMx5n/icons8-eye-50.png"; // Open Eye
            } else {
                togglePassword.src = "https://i.ibb.co/Mxm6yVVn/icons8-eye-50-1.png"; // Slash Eye
            }
        });
    }

    // --- 3. SIDEBAR TOGGLE LOGIC (MOBILE) ---
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebar = document.querySelector('.sidebar');

    if (menuToggle && sidebar) {
        
        // Open Sidebar
        menuToggle.addEventListener('click', () => {
            sidebar.classList.add('active');
        });

        // Close Sidebar (Click X)
        if (closeSidebar) {
            closeSidebar.addEventListener('click', () => {
                sidebar.classList.remove('active');
            });
        }

        // Close Sidebar (Click Outside)
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        });
    }
});

// --- 4. REGISTRATION FORM LOGIC ---
    const registerForm = document.getElementById('registerForm');

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const role = document.getElementById('reg-role').value;
            const fullname = document.getElementById('fullname').value;
            const pass1 = document.getElementById('reg-password').value;
            const pass2 = document.getElementById('confirm-password').value;

            // Simple Password Match Check
            if (pass1 !== pass2) {
                alert("Passwords do not match!");
                return;
            }

            if (pass1.length < 6) {
                alert("Password must be at least 6 characters long.");
                return;
            }

            // Success!
            alert(`Account created successfully for ${fullname} (${role.toUpperCase()})!\nRedirecting to login...`);
            window.location.href = "index.html"; // Send them back to login
        });
    }

    // --- 5. REGISTRATION PASSWORD TOGGLES ---
    // Function to make any password field toggleable
    function setupPasswordToggle(toggleId, inputId) {
        const toggleBtn = document.getElementById(toggleId);
        const inputField = document.getElementById(inputId);

        if (toggleBtn && inputField) {
            toggleBtn.addEventListener('click', () => {
                const type = inputField.getAttribute('type') === 'password' ? 'text' : 'password';
                inputField.setAttribute('type', type);
                
                // Toggle Icon
                if (type === 'password') {
                    toggleBtn.src = "https://i.ibb.co/TxrRMx5n/icons8-eye-50.png";
                } else {
                    toggleBtn.src = "https://i.ibb.co/Mxm6yVVn/icons8-eye-50-1.png";
                }
            });
        }
    }

    // Setup the two toggles on the registration page
    setupPasswordToggle('toggleRegPassword', 'reg-password');
    setupPasswordToggle('toggleConfirmPassword', 'confirm-password');