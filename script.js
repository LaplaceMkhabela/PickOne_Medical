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