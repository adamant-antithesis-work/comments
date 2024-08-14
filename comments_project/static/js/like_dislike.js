document.addEventListener('DOMContentLoaded', () => {
    const handleLikeDislike = (event) => {
        event.preventDefault();

        const form = event.target.closest('form');
        const url = form.action;
        const postId = form.getAttribute('data-id');
        const likeCounter = document.querySelector(`.like-counter[data-id="${postId}"]`);

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams(new FormData(form)).toString()
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                likeCounter.textContent = data.likes;
                likeCounter.style.color = data.likes < 0 ? 'red' : 'inherit';
            } else {
                console.error('Ошибка при обновлении лайков/дизлайков.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    };

    document.querySelectorAll('.like-form, .dislike-form').forEach(form => {
        form.addEventListener('submit', handleLikeDislike);
    });
});