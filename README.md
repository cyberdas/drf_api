# API для системы опроса пользователей

## Разворачивание проекта локально

- Скопируйте репозиторий
```
git clone https://github.com/cyberdas/fabrique_test.git
```
- Установите зависимости
```
pip install -r requirements.txt
```
- Примените миграции
```
- Создайте файл .env с переменными

python manage.py makemigrations
python manage.py migrate
```
- Создайте суперпользователя с неограниченными правами
```
python manage.py createsuperuser
```
- Запустите проект
```
python manage.py runserver
```

## Разворачивание в Docker
- Создать образ:
```
    docker build -t <image name> .
```
- Создать и запустить контейнер из образа:
```
    docker run --name <container name> -d -p <host port>:8000 <image name>
```
- Зайти в запущенный контейнер:
```
    docker exec -it <container name> /bin/bash
    python manage.py createsuperuser 
```
## Функционал администора
- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)
- Эндпоинты
```
/api-auth/ - авторизация в системе
/api/polls/ - доступ ко всем опросам + создание нового
/api/polls/<id>/questions/ - доступ ко всем вопросам опроса + создание нового
/api/polls/<id>/questions/<id>/choices/ - создание вариантов ответа для вопроса
/api/polls/<id>/questions/<id>/choices/<id>/ - измение варианта
```
- Также доступна панель администратора
```
/admin/
```
## Фунционал пользователя(регистрация не нужна)
- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя
## Документация API
Api доступен по адресу /api/
- Эндпоинты
Для доступа к методам необходимо передать user_id
```
/api/polls-active/ - Все активные опросы
/api/polls-finished/ - Пройденные опросы
```
## Для ответа используйте подходящий путь
- Ответ текстом - api/text-answer/
- Выбор одного варианта - api/choice-answer/
- Выбор нескольких вариантов - api/multi-choice-answer/ 
```
{
" choices": [<id варианта>, <id вариант>, ]
}
```