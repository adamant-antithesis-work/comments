// Объект для хранения состояния сортировки по каждому посту
const sortStates = {};

function toggleCommentTable(postId) {
    var table = document.getElementById('comment-table-' + postId);
    if (table.style.display === 'none') {
        table.style.display = 'table';
    } else {
        table.style.display = 'none';
    }
}

function sortTable(postId, columnIndex) {
    var table = document.getElementById('comment-table-' + postId);
    if (!table) return;

    if (!sortStates[postId]) {
        sortStates[postId] = {};
    }

    const currentState = sortStates[postId][columnIndex] || 'asc';
    const newState = currentState === 'asc' ? 'desc' : 'asc';
    sortStates[postId][columnIndex] = newState;

    var rows = Array.from(table.querySelectorAll('tbody > tr'));
    var sortedRows = rows.sort((a, b) => {
        var cellA = a.querySelectorAll('td')[columnIndex].textContent.trim();
        var cellB = b.querySelectorAll('td')[columnIndex].textContent.trim();

        if (newState === 'asc') {
            return cellA.localeCompare(cellB, undefined, { numeric: true });
        } else {
            return cellB.localeCompare(cellA, undefined, { numeric: true });
        }
    });

    var tbody = table.querySelector('tbody');
    sortedRows.forEach(row => tbody.appendChild(row));
}


document.addEventListener('DOMContentLoaded', function() {
    var modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            var postId = this.id.split('-')[1];
            var links = this.querySelectorAll('th a');
            links.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    var index = Array.from(this.parentElement.parentElement.children).indexOf(this.parentElement);
                    sortTable(postId, index);
                });
            });
        });
    });
});
