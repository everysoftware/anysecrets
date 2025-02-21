function searchPasswords() {
    const search = document.getElementById('search')
    const query = search.value;

    if (query) {
        window.location.assign('/passwords?q=' + encodeURIComponent(query));
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('search').addEventListener("keydown", function (e) {
        if (e.code === "Enter") {
            searchPasswords();
        }
    });
    document.getElementById('searchButton').addEventListener("click", function () {
        searchPasswords();
    });
});
