import {authClient} from "./dependencies.js";

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('logout').addEventListener('click', async function () {
        await authClient.logout();
        window.location.replace('/');
    });
});
