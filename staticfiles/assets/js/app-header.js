    function deleteCookie(name) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;

        window.location.href = 'signin';
    }
    const logoutButton = document.getElementById('logoutButton'); 

    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            deleteCookie('jwtToken');
        });
    }
