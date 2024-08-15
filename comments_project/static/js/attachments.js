document.addEventListener('DOMContentLoaded', function() {
    const modal = new bootstrap.Modal(document.getElementById('attachmentModal'));
    const modalBody = document.getElementById('modal-body');

    document.querySelectorAll('.view-attachment').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const url = this.getAttribute('data-url');
            const filename = this.getAttribute('data-file-name');
            const extension = filename.split('.').pop().toLowerCase();

            console.log('File URL:', url);

            if (['jpg', 'jpeg', 'png', 'gif'].includes(extension)) {
                modalBody.innerHTML = `<img src="${url}" class="img-fluid" />`;
            } else if (['pdf'].includes(extension)) {
                modalBody.innerHTML = `<iframe src="${url}" style="width: 100%; height: 400px;" frameborder="0"></iframe>`;
            } else if (['txt'].includes(extension)) {

                fetch(url)
                    .then(response => response.text())
                    .then(text => {
                        modalBody.innerHTML = `<pre>${text}</pre>`;
                    })
                    .catch(error => {
                        modalBody.innerHTML = `<p>Error loading file</p>`;
                        console.error('Error loading text file:', error);
                    });
            } else {
                modalBody.innerHTML = `<a href="${url}" target="_blank">View file</a>`;
            }

            modal.show();
        });
    });
});
