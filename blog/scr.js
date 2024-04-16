function openRespondersList(postId) {
    var url = document.getElementById('responders-list-button').getAttribute('data-url').replace('0', postId);
    var win = window.open(url, '_blank');
    win.focus(); // Попытайтесь фокусировать окно после открытия
}



// Сохранение информации об избранных элементах
let favorites = [];

// Функция для добавления элемента в избранное
function addToFavorites(item) {
    favorites.push(item);
}

// Функция для отображения избранных элементов на странице favorite.html
function displayFavorites() {
    let favoritesContainer = document.getElementById('favorites-container');
    
    favorites.forEach(item => {
        let itemElement = document.createElement('div');
        itemElement.textContent = item.name; // Предполагается, что у элемента есть свойство name
        favoritesContainer.appendChild(itemElement);
    });
}

// Пример использования функций
addToFavorites({ name: 'Элемент 1' });
addToFavorites({ name: 'Элемент 2' });

displayFavorites();
