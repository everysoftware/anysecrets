document.addEventListener('DOMContentLoaded', function () {
    for (const field of document.getElementsByClassName('password')) {
        const toggleButton = document.querySelector('.toggle-visibility');
        const copyButton = document.querySelector('.copy');

        toggleButton.addEventListener('click', function () {
            if (field.type === 'password') {
                field.type = 'text';
                toggleButton.textContent = 'visibility_off';
            } else {
                field.type = 'password';
                toggleButton.textContent = 'visibility';
            }
        });

        copyButton.addEventListener('click', function () {
            navigator.clipboard.writeText(field.value)
                .catch((error) => {
                    console.error('Failed to copy: ', error);
                    alert('Failed to copy');
                });
        });
    }
});
