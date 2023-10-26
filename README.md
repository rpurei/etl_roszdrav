# ETL Росминздрав
Система ETL для обновления НСИ информационной системы медицинской организации.

Представляет собой веб-приложение, через интерфейс которого есть возможность выбора справочников для обновления. Предусмотрена возможность работы в режимме DEV - когда обновляются справочники тестовой информационной системы, переключение в PROD режим происходит через подтверждение путем ручного ввода отображенного на экране числа.

Обновление происходит в максимально безопасном режиме - сначала загружаются все данные, потом происходит переименование таблиц справочников НСИ, причем есть возможность отката к предыдущей версии.

## Запуск
Для запуска необходим установленный Docker, приложение упаковано в контейнер.

Перед запуском необходимо указать настройки:
- настройки собственной базы данных приложения **tasks/config.py** - словарь **db_nsi** (пароль root должен совпадать с паролем в docker-compose.yml, параметр **MYSQL_ROOT_PASSWORD**)
- настройки DEV базы данных **tasks/config.py** - словарь **db_mm**
- настройки PROD базы данных **tasks/config.py** - словарь **db_mm_master**:

Для запуска из каталога приложения выполнить:
```sh
docker-compose up -d
```
Веб-интерфейс будет доступен по адресу <http://localhost:5000>
Имя пользователя и пароль по умолчанию:

**admin admin**
