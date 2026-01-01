document.addEventListener('DOMContentLoaded', () => {
    
    // =========================================================
    // 1. LOGIN PAGE LOGIC (index.html)
    // =========================================================
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const role = document.getElementById('role').value;
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (role && username && password) {
                // SAVE DATA: We store the name and role in the browser's memory
                localStorage.setItem('currentUser', username);
                localStorage.setItem('currentRole', role);

                // REDIRECT: Go to the loading page first!
                window.location.href = "loading.html"; 
            } else {
                alert("Please select a role and fill in all fields.");
            }
        });
    }

    // =========================================================
    // 2. LOADING PAGE LOGIC (loading.html)
    // =========================================================
    // We check if the "welcomeText" element exists (meaning we are on the loading page)
    const welcomeText = document.getElementById('welcomeText');

    if (welcomeText) {
        // RETRIEVE DATA: Get the name we saved earlier
        const user = localStorage.getItem('currentUser');
        const role = localStorage.getItem('currentRole');

        // Update the text on screen
        if (user) {
            welcomeText.innerText = `Welcome, ${user}`;
        }

        // WAIT 3 SECONDS, THEN GO TO DASHBOARD
        setTimeout(() => {
            if (role === 'doctor') {
                window.location.href = "doctor_dashboard.html";
            } else if (role === 'patient') {
                // We haven't built this yet, so maybe send to error for now?
                alert("Patient Dashboard under construction!"); 
                window.location.href = "index.html";
            } else {
                alert("Nurse Dashboard under construction!");
                window.location.href = "index.html";
            }
        }, 3000); // 3000 milliseconds = 3 seconds
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
            window.location.href = "login.html"; // Send them back to login
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

    // =========================================================
    // 5. ERROR PAGE LOGIC (Auto-Redirect)
    // =========================================================
    const countdownElement = document.getElementById('countdown');

    if (countdownElement) {
        let timeLeft = 10;

        const timer = setInterval(() => {
            timeLeft--; 
            countdownElement.innerText = timeLeft; 

            if (timeLeft <= 0) {
                clearInterval(timer); 
                window.location.href = "welcome-page.html"; 
            }
        }, 1000); 
    }
});