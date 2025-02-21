import {passwordClient} from './dependencies.js';

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('createPasswordForm').addEventListener('submit', async function (event) {
        event.preventDefault();
        const data = {
            name: document.getElementById('title').value,
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            url: document.getElementById('url').value,
            note: document.getElementById('note').value
        };
        const response = await passwordClient.createPassword(data);
        if (response) {
            window.location.assign('/passwords');
        }
    });

    document.getElementById('generatePasswordButton').addEventListener('click', function () {
        document.getElementById('password').value = passwordClient.generatePassword();
    });
});
