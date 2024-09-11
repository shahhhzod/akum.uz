$(document).ready(function () {
    // Обработка ввода текста и автозаполнение
    $('#search-input').on('input', function () {
        var query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: "{% url 'autocomplete' %}",
                data: { 'term': query },
                success: function (data) {
                    $('#suggestions').empty();
                    if (data.length > 0) {
                        data.forEach(function (suggestion) {
                            $('#suggestions').append('<li class="list-group-item">' + suggestion + '</li>');
                        });
                    } else {
                        $('#suggestions').append('<li class="list-group-item">Ничего не найдено</li>');
                    }
                }
            });
        } else {
            $('#suggestions').empty();
        }
    });

    // Определение местоположения пользователя
    fetch('http://ip-api.com/json/')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                document.getElementById('user-city').innerText = data.city;
            } else {
                document.getElementById('user-city').innerText = "Неизвестен";
            }
        })
        .catch(error => {
            console.error('Error fetching location:', error);
            document.getElementById('user-city').innerText = "Неизвестен";
        });

    // Инициализация состояния кнопок
    document.addEventListener('DOMContentLoaded', updateAddToCartButton);
});

function increment() {
    let quantityInput = document.getElementById('quantity');
    let currentValue = parseInt(quantityInput.value);
    let maxValue = parseInt(quantityInput.getAttribute('data-max'));

    if (currentValue < maxValue) {
        quantityInput.value = currentValue + 1;
    }

    updateAddToCartButton();
}

function decrement() {
    let quantityInput = document.getElementById('quantity');
    let currentValue = parseInt(quantityInput.value);

    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }

    updateAddToCartButton();
}

function updateAddToCartButton() {
    let quantityInput = document.getElementById('quantity');
    let currentValue = parseInt(quantityInput.value);
    let maxValue = parseInt(quantityInput.getAttribute('data-max'));
    let addToCartButton = document.getElementById('addToCartButton');

    if (currentValue >= maxValue) {
        addToCartButton.disabled = true;
    } else {
        addToCartButton.disabled = false;
    }
}

function validateSearch() {
    var query = document.getElementById('search-input').value.trim();
    if (query === "") {
        var toastEl = document.getElementById('searchToast');
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
        return false;
    }
    return true;
}


function validateSearch() {
    var query = document.getElementById('search-input').value;
    return query.trim().length > 0;  // Проверяем, чтобы поле не было пустым
}

$(document).ready(function () {
    $("#search-input").on('keyup', function () {
        var query = $(this).val();

        if (query.length > 2) {  // Начинаем поиск, если длина строки больше 2 символов
            $.ajax({
                url: "{% url 'products:autocomplete_search' %}",
                data: {'term': query},
                dataType: 'json',
                success: function (data) {
                    var autocompleteList = $("#autocomplete-list");
                    autocompleteList.empty();  // Очищаем предыдущие результаты

                    // Добавляем новые результаты в список
                    data.forEach(function (item) {
                        autocompleteList.append('<li class="list-group-item" onclick="selectAutocompleteItem(\'' + item.name + '\')">' + item.name + '</li>');
                    });
                }
            });
        } else {
            $("#autocomplete-list").empty();  // Очищаем результаты, если строка меньше 3 символов
        }
    });
});

function selectAutocompleteItem(name) {
    $("#search-input").val(name);  // Заполняем поле ввода выбранным элементом
    $("#autocomplete-list").empty();  // Очищаем список автозаполнения
    document.forms[0].submit();  // Отправляем форму
}


document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl, { delay: 3000 });
    });
    toastList.forEach(toast => toast.show());
});


document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl, { delay: 3000 });
    });
    toastList.forEach(toast => toast.show());
});