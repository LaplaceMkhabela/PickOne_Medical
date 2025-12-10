document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const role = document.getElementById('role').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (role && username && password) {
            // This is just for testing to see if it works
            alert(`Logging you in as a: ${role.toUpperCase()}\nUsername: ${username}`);
            
        } else {
            alert("Please select a role and fill in all fields.");
        }
    });
});