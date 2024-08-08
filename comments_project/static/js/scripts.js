document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.reply-button').forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault();
            const targetSelector = button.getAttribute('data-target');
            const form = document.querySelector(targetSelector);

            if (form) {
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            }
        });
    });
});