const APIURL = 'https://github.com';

const main = document.getElementById('main');
const form = document.getElementById('form');
const search = document.getElementById('search');

/**
 * Получение данных профиля
 */
async function getUser(username) {
    // 1. Валидация имени (латиница, цифры, дефисы, до 39 символов)
    const usernameRegex = /^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i;
    
    if (!usernameRegex.test(username)) {
        createErrorCard('Некорректный формат имени пользователя');
        return;
    }

    try {
        const response = await fetch(APIURL + username);

        // 2. Обработка специфических статусов
        if (response.status === 403) {
            createErrorCard('Лимит запросов API исчерпан. Попробуйте позже.');
            return;
        }
        
        if (response.status === 404) {
            createErrorCard('Пользователь с таким именем не найден');
            return;
        }

        if (!response.ok) {
            throw new Error(`Ошибка: ${response.status}`);
        }

        // 3. Обработка ошибок парсинга JSON
        const data = await response.json().catch(() => {
            throw new Error('Ошибка обработки данных от сервера');
        });

        createUserCard(data);
        getRepos(username);
        
    } catch (err) {
        createErrorCard(err.message || 'Произошла непредвиденная ошибка');
    }
}

/**
 * Получение репозиториев
 */
async function getRepos(username) {
    try {
        const response = await fetch(APIURL + username + '/repos?sort=created');
        
        if (!response.ok) return; // Ошибки профиля важнее, тут просто игнорируем

        const data = await response.json().catch(() => []);
        addReposToCard(data);
    } catch (err) {
        console.error('Ошибка при загрузке репозиториев');
    }
}

/**
 * Создание карточки пользователя
 */
function createUserCard(user) {
    const cardHTML = `
    <div class="card">
        <div>
          <img src="${user.avatar_url}" alt="${user.name}" class="avatar">
        </div>
        <div class="user-info">
          <h2>${user.name || user.login}</h2>
          <p>${user.bio || 'Описание профиля отсутствует'}</p>
          <ul>
            <li>${user.followers} <strong>Followers</strong></li>
            <li>${user.following} <strong>Following</strong></li>
            <li>${user.public_repos} <strong>Repos</strong></li>
          </ul>
          <div id="repos"></div>
        </div>
    </div>
    `;
    main.innerHTML = cardHTML;
}

/**
 * Вывод сообщения об ошибке
 */
function createErrorCard(msg) {
    const cardHTML = `
        <div class="card">
            <h1>${msg}</h1>
        </div>
    `;
    main.innerHTML = cardHTML;
}

/**
 * Добавление репозиториев в карточку
 */
function addReposToCard(repos) {
    const reposEl = document.getElementById('repos');

    repos
        .slice(0, 5)
        .forEach(repo => {
            const repoEl = document.createElement('a');
            repoEl.classList.add('repo');
            repoEl.href = repo.html_url;
            repoEl.target = '_blank';
            repoEl.innerText = repo.name;

            reposEl.appendChild(repoEl);
        });
}

/**
 * Слушатель событий формы
 */
form.addEventListener('submit', (e) => {
    e.preventDefault();

    const user = search.value.trim();

    if (user) {
        getUser(user);
        search.value = '';
    }
});

