// in case href(the page loaded) from reset password
document.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('reset') === '1') {
        const uidb64 = params.get('uidb64');
        const token = params.get('token');
        showResetPasswordForm(uidb64, token);
    } else {
        showLogin();
    }
});

function goToHome() {
    window.location.href = '/';
}

function showLogin() {
    document.getElementById('content-area').innerHTML = `
        <form id="login-form">
            <h2>Login</h2>
            <input type="text" id="username" placeholder="Username or Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Login</button>
            <p id="error-message"></p>
        </form>
    `;

    document.getElementById("login-form").addEventListener("submit", function(event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch("/api/users/login/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                identifier: username, 
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {  
                localStorage.setItem("token", data.token); 
                localStorage.setItem("username", username); 
                window.location.href = "/dashboard/";
            } else {
                document.getElementById("error-message").innerText = data.error || "Invalid credentials.";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("error-message").innerText = "Something went wrong. Please try again.";
        });
    });
}

function showRegister() {
    document.getElementById('content-area').innerHTML = `
        <form id="register-form">
            <h2>Register</h2>
            <input type="text" id="new-username" placeholder="Choose Username" required>
            <input type="email" id="email" placeholder="Email" required>
            <input type="password" id="new-password" placeholder="Password" required>
            <p id="register-error-message"></p>
            <button type="submit">Create Account</button>
        </form>
    `;

    document.getElementById("register-form").addEventListener("submit", function(event) {
        event.preventDefault();

        const username = document.getElementById("new-username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("new-password").value;

        fetch("/api/users/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) { 
                alert("Account created successfully! Please login.");
                showLogin(); 
            } else {
                document.getElementById("register-error-message").innerText = data.error || "Registration failed.";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("register-error-message").innerText = "Something went wrong. Please try again.";
        });
    });
}

function showForgotPassword() {
    document.getElementById('content-area').innerHTML = `
        <form id="forgot-password-form">
            <h2>Forgot Password</h2>
            <input type="email" id="forgot-email" placeholder="Enter your email" required>
            <button type="submit">Send Reset Link</button>
            <p id="forgot-error-message"></p>
        </form>
    `;

    document.getElementById('forgot-password-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const email = document.getElementById('forgot-email').value;

        fetch('/api/users/forgot-password/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Check email for reset link (this simulates email).');
                showLogin(); 
            } else {
                document.getElementById('forgot-error-message').innerText = data.error || 'Failed to process request.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('forgot-error-message').innerText = 'Something went wrong.';
        });
    });
}

function showResetPasswordForm(uidb64, token) {
    document.getElementById('content-area').innerHTML = `
        <form id="reset-password-form">
            <h2>Reset Password</h2>
            <input type="password" id="new-password" placeholder="Enter new password" required>
            <button type="submit">Reset</button>
            <p id="reset-error-message"></p>
        </form>
    `;

    document.getElementById('reset-password-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const newPassword = document.getElementById('new-password').value;

        fetch(`/api/users/reset-password/${uidb64}/${token}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: newPassword })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert("Password reset successfully! Please login.");
                showLogin(); 
            } else {
                document.getElementById('reset-error-message').innerText = data.error || 'Failed to reset password.';
            }
        })
        .catch(err => {
            console.error(err);
            document.getElementById('reset-error-message').innerText = "Something went wrong.";
        });
    });
}