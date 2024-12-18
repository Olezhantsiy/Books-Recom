function updateSelectedCheckboxes() {
    const selectedContainer = document.getElementById('selected-author-checkboxes');
    const allCheckboxes = document.querySelectorAll('#author-checkboxes .form-check-input');

    // Очищаем контейнер выбранных чекбоксов перед добавлением новых
    selectedContainer.innerHTML = '';

    allCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            // Создаем новый чекбокс в контейнере для выбранных
            const selectedCheckbox = document.createElement('div');
            selectedCheckbox.classList.add('form-check', 'selected-author-checkbox');
            const label = document.createElement('label');
            label.classList.add('form-check-label');
            label.textContent = checkbox.nextElementSibling.textContent;

            const input = document.createElement('input');
            input.type = 'checkbox';
            input.classList.add('form-check-input');
            input.checked = true;
            input.value = checkbox.value;
            input.id = checkbox.id;

            // Добавляем обработчик для снятия отметки
            input.addEventListener('change', () => {
                checkbox.checked = input.checked;
                updateSelectedCheckboxes();
            });

            selectedCheckbox.appendChild(input);
            selectedCheckbox.appendChild(label);

            selectedContainer.appendChild(selectedCheckbox);
        }
    });
}

// Функция для поиска чекбоксов
function filterCheckboxes(inputId, checkboxesContainerId) {
    const input = document.getElementById(inputId);
    const container = document.getElementById(checkboxesContainerId);
    const checkboxes = container.querySelectorAll('.form-check');

    input.addEventListener('input', () => {
        const query = input.value.toLowerCase();

        checkboxes.forEach((checkbox, index) => {
            const label = checkbox.querySelector('label').textContent.toLowerCase();

            // Если запрос пустой, скрываем чекбоксы начиная с 6-го
            if (query === '') {
                if (index >= 5) {
                    checkbox.style.display = 'none';
                } else {
                    checkbox.style.display = 'block';
                }
            } else {
                if (label.includes(query)) {
                    checkbox.style.display = 'block';
                } else {
                    checkbox.style.display = 'none';
                }
            }
        });
    });
}

// Ограничение на количество отображаемых чекбоксов (не больше 5)
function limitCheckboxesDisplay() {
    const checkboxes = document.querySelectorAll('#author-checkboxes .form-check');
    checkboxes.forEach((checkbox, index) => {
        if (index >= 5) {
            checkbox.style.display = 'none'; // Скрываем чекбоксы начиная с 6-го
        }
    });
}

// Инициализация
document.querySelectorAll('.form-check-input').forEach(checkbox => {
    checkbox.addEventListener('change', updateSelectedCheckboxes);
});

// Инициализация фильтрации
filterCheckboxes('author-search', 'author-checkboxes');
updateSelectedCheckboxes();

// Ограничение на количество чекбоксов
limitCheckboxesDisplay();


function updateSelectedGenreCheckboxes() {
    const selectedContainer = document.getElementById('selected-genre-checkboxes');
    const allCheckboxes = document.querySelectorAll('#genre-checkboxes .form-check-input');

    // Очищаем контейнер выбранных чекбоксов перед добавлением новых
    selectedContainer.innerHTML = '';

    allCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            // Создаем новый чекбокс в контейнере для выбранных
            const selectedCheckbox = document.createElement('div');
            selectedCheckbox.classList.add('form-check', 'selected-genre-checkbox');
            const label = document.createElement('label');
            label.classList.add('form-check-label');
            label.textContent = checkbox.nextElementSibling.textContent;

            const input = document.createElement('input');
            input.type = 'checkbox';
            input.classList.add('form-check-input');
            input.checked = true;
            input.value = checkbox.value;
            input.id = checkbox.id;

            // Добавляем обработчик для снятия отметки
            input.addEventListener('change', () => {
                checkbox.checked = input.checked;
                updateSelectedGenreCheckboxes();
            });

            selectedCheckbox.appendChild(input);
            selectedCheckbox.appendChild(label);

            selectedContainer.appendChild(selectedCheckbox);
        }
    });
}

// Функция для поиска чекбоксов жанров
function filterGenreCheckboxes(inputId, checkboxesContainerId) {
    const input = document.getElementById(inputId);
    const container = document.getElementById(checkboxesContainerId);
    const checkboxes = container.querySelectorAll('.form-check');

    input.addEventListener('input', () => {
        const query = input.value.toLowerCase();

        checkboxes.forEach((checkbox, index) => {
            const label = checkbox.querySelector('label').textContent.toLowerCase();

            // Если запрос пустой, скрываем чекбоксы начиная с 6-го
            if (query === '') {
                if (index >= 5) {
                    checkbox.style.display = 'none';
                } else {
                    checkbox.style.display = 'block';
                }
            } else {
                if (label.includes(query)) {
                    checkbox.style.display = 'block';
                } else {
                    checkbox.style.display = 'none';
                }
            }
        });
    });
}

// Ограничение на количество отображаемых чекбоксов жанров (не больше 5)
function limitGenreCheckboxesDisplay() {
    const checkboxes = document.querySelectorAll('#genre-checkboxes .form-check');
    checkboxes.forEach((checkbox, index) => {
        if (index >= 5) {
            checkbox.style.display = 'none'; // Скрываем чекбоксы начиная с 6-го
        }
    });
}

// Инициализация
document.querySelectorAll('.form-check-input').forEach(checkbox => {
    checkbox.addEventListener('change', updateSelectedGenreCheckboxes);
});

// Инициализация фильтрации жанров
filterGenreCheckboxes('genre-search', 'genre-checkboxes');
updateSelectedGenreCheckboxes();

// Ограничение на количество чекбоксов жанров
limitGenreCheckboxesDisplay();

function updateSelectedPublisherCheckboxes() {
    const selectedContainer = document.getElementById('selected-publisher-checkboxes');
    const allCheckboxes = document.querySelectorAll('#publisher-checkboxes .form-check-input');

    // Очищаем контейнер выбранных чекбоксов перед добавлением новых
    selectedContainer.innerHTML = '';

    allCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            // Создаем новый чекбокс в контейнере для выбранных
            const selectedCheckbox = document.createElement('div');
            selectedCheckbox.classList.add('form-check', 'selected-publisher-checkbox');
            const label = document.createElement('label');
            label.classList.add('form-check-label');
            label.textContent = checkbox.nextElementSibling.textContent;

            const input = document.createElement('input');
            input.type = 'checkbox';
            input.classList.add('form-check-input');
            input.checked = true;
            input.value = checkbox.value;
            input.id = checkbox.id;

            // Добавляем обработчик для снятия отметки
            input.addEventListener('change', () => {
                checkbox.checked = input.checked;
                updateSelectedPublisherCheckboxes();
            });

            selectedCheckbox.appendChild(input);
            selectedCheckbox.appendChild(label);

            selectedContainer.appendChild(selectedCheckbox);
        }
    });
}

// Функция для поиска чекбоксов издательств
function filterPublisherCheckboxes(inputId, checkboxesContainerId) {
    const input = document.getElementById(inputId);
    const container = document.getElementById(checkboxesContainerId);
    const checkboxes = container.querySelectorAll('.form-check');

    input.addEventListener('input', () => {
        const query = input.value.toLowerCase();

        checkboxes.forEach((checkbox, index) => {
            const label = checkbox.querySelector('label').textContent.toLowerCase();

            // Если запрос пустой, скрываем чекбоксы начиная с 6-го
            if (query === '') {
                if (index >= 5) {
                    checkbox.style.display = 'none';
                } else {
                    checkbox.style.display = 'block';
                }
            } else {
                if (label.includes(query)) {
                    checkbox.style.display = 'block';
                } else {
                    checkbox.style.display = 'none';
                }
            }
        });
    });
}

// Ограничение на количество отображаемых чекбоксов издательств (не больше 5)
function limitPublisherCheckboxesDisplay() {
    const checkboxes = document.querySelectorAll('#publisher-checkboxes .form-check');
    checkboxes.forEach((checkbox, index) => {
        if (index >= 5) {
            checkbox.style.display = 'none'; // Скрываем чекбоксы начиная с 6-го
        }
    });
}

// Инициализация
document.querySelectorAll('.form-check-input').forEach(checkbox => {
    checkbox.addEventListener('change', updateSelectedPublisherCheckboxes);
});

// Инициализация фильтрации издательств
filterPublisherCheckboxes('publisher-search', 'publisher-checkboxes');
updateSelectedPublisherCheckboxes();

// Ограничение на количество чекбоксов издательств
limitPublisherCheckboxesDisplay();



// Открытие/закрытие боковой панели
const filterToggleBtn = document.getElementById('filter-toggle-btn');
const sidebar = document.getElementById('sidebar');
const filterCloseBtn = document.getElementById('filter-close-btn');

filterToggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
});

filterCloseBtn.addEventListener('click', () => {
    sidebar.classList.remove('open');
});