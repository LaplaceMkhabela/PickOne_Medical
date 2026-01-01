document.addEventListener('DOMContentLoaded', () => {
    
    // =========================================================
    // 1. LOGIN PAGE LOGIC (login-page.html)
    // =========================================================
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const role = document.getElementById('role').value;
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (role && username && password) {
                // SAVE DATA
                localStorage.setItem('currentUser', username);
                localStorage.setItem('currentRole', role);

                // REDIRECT: Fixed filename
                window.location.href = "loading-page.html"; 
            } else {
                alert("Please select a role and fill in all fields.");
            }
        });
    }

    // =========================================================
    // 2. LOADING PAGE LOGIC (loading-page.html)
    // =========================================================
    const welcomeText = document.getElementById('welcomeText');

    if (welcomeText) {
        // RETRIEVE DATA
        const user = localStorage.getItem('currentUser');
        const role = localStorage.getItem('currentRole');

        if (user) {
            welcomeText.innerText = `Welcome, ${user}`;
        }

        // WAIT 3 SECONDS, THEN REDIRECT
        setTimeout(() => {
            if (role === 'doctor') {
                // Fixed filename (assuming you named the file doctor-dashboard.html)
                window.location.href = "doctor-dashboard.html";
            } else if (role === 'patient') {
                alert("Patient Dashboard coming soon!"); 
                window.location.href = "login-page.html";
            } else {
                alert("Nurse Dashboard coming soon!");
                window.location.href = "login-page.html";
            }
        }, 3000); 
    }

    // =========================================================
    // 3. REGISTRATION LOGIC (registration-page.html)
    // =========================================================
    const registerForm = document.getElementById('registerForm');

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const role = document.getElementById('reg-role').value;
            const fullname = document.getElementById('fullname').value;
            const pass1 = document.getElementById('reg-password').value;
            const pass2 = document.getElementById('confirm-password').value;

            if (pass1 !== pass2) {
                alert("Passwords do not match!");
                return;
            }

            if (pass1.length < 6) {
                alert("Password must be at least 6 characters long.");
                return;
            }

            alert(`Account created successfully for ${fullname}! Redirecting to login...`);
            // Fixed filename
            window.location.href = "login-page.html"; 
        });
    }

    // =========================================================
    // 4. ERROR PAGE LOGIC (error-page.html)
    // =========================================================
    const countdownElement = document.getElementById('countdown');

    if (countdownElement) {
        let timeLeft = 10;
        const timer = setInterval(() => {
            timeLeft--; 
            countdownElement.innerText = timeLeft; 

            if (timeLeft <= 0) {
                clearInterval(timer); 
                // Fixed filename
                window.location.href = "welcome-page.html"; 
            }
        }, 1000); 
    }

    // =========================================================
    // 5. GLOBAL TOOLS (Password Toggle & Mobile Sidebar)
    // =========================================================
    
    // -- Password Toggle (Works for Login & Register) --
    const toggleIcons = document.querySelectorAll('.toggle-icon');

    toggleIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            const wrapper = icon.parentElement;
            const input = wrapper.querySelector('input');

            if (input) {
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);

                if (type === 'password') {
                    icon.src = "https://i.ibb.co/TxrRMx5n/icons8-eye-50.png";
                } else {
                    icon.src = "https://i.ibb.co/Mxm6yVVn/icons8-eye-50-1.png";
                }
            }
        });
    });

    // -- Sidebar Logic --
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebar = document.querySelector('.sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.add('active');
        });

        if (closeSidebar) {
            closeSidebar.addEventListener('click', () => {
                sidebar.classList.remove('active');
            });
        }

        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        });
    }
});