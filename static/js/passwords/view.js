import {passwordClient} from "./dependencies.js";

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('editPasswordForm').addEventListener('submit', async function (event) {
        event.preventDefault();
        const passwordId = document.getElementById('passwordId').value;
        const data = {
            name: document.getElementById('title').value,
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            url: document.getElementById('url').value,
            note: document.getElementById('note').value
        };
        const response = await passwordClient.editPassword(passwordId, data);
        if (response) {
            window.location.assign('/passwords');
        }
    });

    document.getElementById('deletePasswordButton').addEventListener('click', async function () {
        const passwordId = document.getElementById('passwordId').value;
        const confirmation = confirm('Are you sure you want to delete this password?');
        if (confirmation) {
            const response = await passwordClient.deletePassword(passwordId);
            if (response) {
                window.location.assign('/passwords');
            }
        }
    });
});
