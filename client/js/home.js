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
