function validateForm(event) {
    event.preventDefault()
    const form = document.getElementById('signUpForm');
    const inputs = form.querySelectorAll('input');

    for (let input of inputs) {
        if (!input.value.trim()) {
            alert('Please fill in all the fields');
            return false;
        }
    }
    addUser();
    return false;
}

function validateLoginForm(event) {
    event.preventDefault();
    const name = document.getElementById('loginName').value.trim();
    const password = document.getElementById('loginPassword').value.trim();
    if (!name || !password) {
        alert('Please fill in all required fields');
        console.log('Invalid login form');
        return false;
    }
    login();
    return false;
}

function clearLoginFields() {
    document.getElementById('loginName').value = "";
    document.getElementById('loginPassword').value = "";
}

async function login() {
    const name = document.getElementById('loginName').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    const response = await fetch('http://127.0.0.1:5000/auth/getUser', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            password: password
        })
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Logged in successfully:', data);
        localStorage.setItem('token', data.token);
        window.location.href = 'pages/main.html';
        document.getElementById('loginForm').reset();
    } else {
        console.log('Failed to log in:', response.statusText);
        const loginModal = document.getElementById('loginModal');
        const modalInstance = bootstrap.Modal.getInstance(loginModal);
        modalInstance.hide();
        clearLoginFields()
        const signUpModal = new bootstrap.Modal(document.getElementById('signUpModal'));
        signUpModal.show();
    }
}

async function addUser() {
    const user = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        city: document.getElementById('city').value,
        phone: document.getElementById('phone').value,
        password: document.getElementById('password').value
    };
    try {
        const response = await fetch('http://localhost:5000/auth/addUser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (response.ok) {
            const loginResponse = await fetch('http://127.0.0.1:5000/auth/getUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: user.name,
                    password: user.password
                })
            });

            if (loginResponse.ok) {
                const data = await loginResponse.json();
                console.log('Logged in successfully:', data);
                localStorage.setItem('token', data.token);
                window.location.href = 'pages/main.html';
            } else {
                console.log('Failed to log in:', loginResponse.statusText);
            }

            document.getElementById('signUpForm').reset();
            closesignUpModal();
        } else {
            const errorData = await response.json();
            if (errorData.error === "Password already exists") {
                alert("The password already exists. Please choose another one.");
            } else {
                console.log('Failed to add user:', response.statusText);
            }
        }
    } catch (error) {
        console.error('Error occurred:', error);
    }
}

function handleGoogleResponse(response) {
    console.log("Google Response:", response);

    // בדיקה אם לא קיבלנו את ה-credential מהתגובה של Google
    if (!response || !response.credential) {
        console.error("Google token is missing.");
        alert("Something went wrong with Google authentication.");
        return;
    }
    console.log("Sending Google token to server:", response.credential);

    // שליחת בקשה לשרת עם הטוקן של Google
    axios.post('http://127.0.0.1:5000/auth/googleLogin', {
        googleToken: response.credential
    })
        .then(serverResponse => {
            // בדיקה אם התגובה של השרת תקינה
            if (serverResponse.status === 200) {
                const token = serverResponse.data.token;
                console.log("Server Response:", serverResponse.data);
                localStorage.setItem('token', token);
                console.log("Login successful!", serverResponse.data.user);
                window.location.href = 'pages/main.html';  // דף הבית לאחר התחברות
            } else {
                console.error("Unexpected server response:", serverResponse);
                alert("Server returned an error, please try again later.");
            }
        })
        .catch(error => {
            if (error.response) {
                console.error("Server error:", error.response);
            } else if (error.request) {
                console.error("Network error:", error.request);
            } else {
                console.error("Error during request setup:", error.message);
            }
            alert("An error occurred. Please try again later.");
        });
}

window.onload = function () {
    console.log("Page Loaded");  // הדפסת לוג כאשר הדף נטען

    // הוספת מאזין לכפתור התחברות
    const loginButton = document.getElementById("googleLoginBtn");
    if (loginButton) {
        console.log("Google login button found.");
    } else {
        console.error("Google login button not found.");
    }

    loginButton.addEventListener("click", function () {
        console.log("Google login button clicked now!!");  // הדפסת לוג אם הכפתור נלחץ
        // הפעלת ה-prompt להתחברות עם גוגל
        console.log("Initializing Google OAuth...");
        google.accounts.id.initialize({
            client_id: "625165215188-nc3v63edv5th9498g0en3jjk9h03p07u.apps.googleusercontent.com",
            callback: handleGoogleResponse
        });
        console.log("Google OAuth initialized");
        google.accounts.id.prompt();
        console.log("Google sign-in prompt opened");
    });
};
