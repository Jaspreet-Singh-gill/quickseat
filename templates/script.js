async function registerUser() {
    const email = document.getElementById("reg-email").value;
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;
    const messageBox = document.getElementById("message");
    const loginButton = document.getElementById("login-btn");

    if (!email || !username || !password) {
        messageBox.textContent = "Please fill in all fields!";
        messageBox.style.color = "red";
        messageBox.classList.remove("hidden");
        return;
    }

    const data = { email:email, 
                username:username,
                password: password };

    try {
        const response = await fetch("http://127.0.0.1:8000/user_create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            messageBox.textContent = "You have been registered successfully!";
            messageBox.style.color = "green";
            loginButton.classList.remove("hidden"); // Show Login Button
        } else {
            messageBox.textContent = "Please enter your details correctly!";
            messageBox.style.color = "red";
        }

        messageBox.classList.remove("hidden");
    } catch (error) {
        messageBox.textContent = "An error occurred. Please try again!";
        messageBox.style.color = "red";
        messageBox.classList.remove("hidden");
    }
}

// Redirect to Login Page
function goToLogin() {
    window.location.href = "login.html";
}

async function loginUser() {
    const identifier = document.getElementById("login-identifier").value;
    const password = document.getElementById("login-password").value;
    const messageBox = document.getElementById("login-message");

    if (!identifier || !password) {
        messageBox.textContent = "Please enter your username/email and password!";
        messageBox.style.color = "red";
        messageBox.classList.remove("hidden");
        return;
    }

    // Prepare form data (OAuth2 expects 'username' instead of 'identifier')
    const formData = new URLSearchParams();
    formData.append("username", identifier);  // OAuth2 requires "username"
    formData.append("password", password);

    try {
        const response = await fetch("http://127.0.0.1:8000/user_login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.access_token) {
            localStorage.setItem("jwt_token", result.access_token); // Store JWT token
            messageBox.textContent = "Login successful! Redirecting...";
            messageBox.style.color = "green";
            setTimeout(() => {
                window.location.href = "dashboard.html"; // Redirect after login
            }, 1500);
        } else {
            messageBox.textContent = "Invalid username/email or password!";
            messageBox.style.color = "red";
        }

        messageBox.classList.remove("hidden");
    } catch (error) {
        messageBox.textContent = "An error occurred. Please try again!";
        messageBox.style.color = "red";
        messageBox.classList.remove("hidden");
    }
}
