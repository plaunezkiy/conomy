# Conomy

###Тестовое задание для conomy.ru

### Запуск
* Создать виртуальную среду и установить зависимости
    * ```python -m venv venv```
    * ```source venv/scripts/activate```
    * ```pip install -r requirements.txt```
* Применить миграции и запустить сервер
    * ```./manage.py migrate```
    * ```./manage.py runserver```

# Конечные адреса API

* **Получение токена авторизации**
    * ```api/v1/token/```

* **Обновление токена авторизации**
    * ```api/v1/token/refresh/```

* **Список кошельков**
    * ```api/v1/wallets/```

* **Один кошелек**
    * ```api/v1/wallets/{id}/```

* **Транзакции одного кошелька**
    * ```api/v1/wallets/{id}/transactions/```

* **Список транзакций всех кошельков**
    * GET ```api/v1/transactions/```

* **Создание тразакции**
    * POST ```api/v1/transactions/```

* **Одна транзакция**
    * ```api/v1/transactions/{id}/```

