import {authClient} from './dependencies.js';

async function onLoginFormSubmit(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const response = await authClient.login(email, password);
    if (response) {
        window.location.assign('/passwords');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginForm').addEventListener('submit', onLoginFormSubmit);
});
