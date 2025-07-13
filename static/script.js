document.addEventListener('keydown', function (event) {
    const activeElement = document.activeElement;
    if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA') {
        return;
    }

    if (event.key.toLowerCase() === 'a' && window.location.pathname === '/') {
        event.preventDefault();

        const modalElement = document.getElementById('addDeckModal');
        const isVisible = modalElement.classList.contains('show');

        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);

        if (isVisible) {
            modalInstance.hide();
        } else {
            modalInstance.show();
        }
    }


    if (event.key.toLowerCase() === 'a' && window.location.pathname.startsWith('/deck_view')) {
        event.preventDefault();

        const modalElement = document.getElementById('addCardModal');
        const isVisible = modalElement.classList.contains('show');

        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);

        if (isVisible) {
            modalInstance.hide();
        } else {
            modalInstance.show();
        }
    }

    if (event.key.toLowerCase() === 'p' && window.location.pathname.startsWith('/deck_view')) {
        event.preventDefault();

        const modalElement = document.getElementById('practiceModal');
        const isVisible = modalElement.classList.contains('show');

        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);

        if (isVisible) {
            modalInstance.hide();
        } else {
            modalInstance.show();
        }
    }
});
