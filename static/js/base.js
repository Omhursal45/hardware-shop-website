    const menuBtn = document.getElementById('mobile-menu-btn');
    const navMenu = document.getElementById('nav-menu');

    if (menuBtn && navMenu) {
        menuBtn.addEventListener('click', (e) => {
            navMenu.classList.toggle('active');
            e.stopPropagation();
        });
        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target) && !menuBtn.contains(e.target)) {
                navMenu.classList.remove('active');
            }
        });
    }
    const searchInput = document.getElementById('search-input');
    const suggestionsBox = document.getElementById('search-suggestions');

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value.trim();
            if (query.length < 1) {
                suggestionsBox.innerHTML = '';
                suggestionsBox.style.display = 'none';
                return;
            }

            const url = searchInput.dataset.autocompleteUrl + '?q=' + encodeURIComponent(query);
            fetch(url)
                .then((res) => res.json())
                .then((data) => {
                    suggestionsBox.innerHTML = '';
                    if (data.length > 0) {
                        data.forEach((item) => {
                            const li = document.createElement('li');
                            li.textContent = item.name;
                            li.addEventListener('click', () => {
                                window.location.href = `/products/${item.slug}/`;
                            });
                            suggestionsBox.appendChild(li);
                        });
                        suggestionsBox.style.display = 'block';
                    } else {
                        suggestionsBox.style.display = 'none';
                    }
                })
                .catch((err) => {
                    console.error('Autocomplete fetch failed', err);
                });
        });
        document.addEventListener('click', (e) => {
            if (e.target !== searchInput && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = 'none';
            }
        });
    }
