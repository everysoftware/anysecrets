import {authClient} from './dependencies.js';

async function onRegisterFormSubmit(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }
    const response = await authClient.register(name, email, password);
    if (response) {
        alert('You are successfully registered. Please log in.');
        window.location.assign('/login');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('registerForm').addEventListener('submit', onRegisterFormSubmit)
});
