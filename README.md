### Статус workflow

![foodgram_workflow](https://github.com/Fr33vvay/foodgram-project/workflows/foodgram_workflow/badge.svg)

### [Пример сайта](http://freeway-foodgram.tk/recipe/)
# Foodgram. Рецепты с фоточками

Сайт рецептов. Пользователи могут публиковать свои рецепты, просматривать и 
сохранять в Избранном чужие рецепты, подписываться на страницы любимых авторов.
Функция "Список покупок" позволяет добавить один или несколько рецептов и
затем скачать общий список покупок в формате txt.

## Начало

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере в целях разработки и тестирования.

### Предварительные условия

Для установки программного обеспечения понадобятся

* [docker 19.03+](https://www.docker.com/get-started)
* [docker-compose 1.25.0+](https://docs.docker.com/compose/)
* [git](https://github.com/)


### Установка

Для установки необходимо: 
* склонировать репозиторий и создать файл .env с настройками в корневой папке проекта
* создать докер-контейнер, запустить приложение
* открыть консоль для ввода последующих команд 
* накатить миграции
* собрать статические файлы
* при необходимости загрузить список ингредиентов и единиц измерения в БД
* при необходимости создать суперпользователя
* зайти в админ-панель django (your_dns/admin) и создать теги

```
git clone https://github.com/Fr33vvay/foodgram-project
cd foodgram-project/
touch .env
docker-compose up -d
docker exec -it django bash
python manage.py migrate
python manage.py collectstatic
python manage.py load_ingredients_data
python manage.py createsuperuser
```

Для проверки работы откройте в своем браузере: [localhost/recipe](http://localhost/recipe)

Если вы хотите локально вносить изменения в проект, то в файле
docker-compose.yaml закомментируйте строку image: fr33vvay/foodgram:latest
и раскомментируйте build: .
## Пример настроек окружения

Пример файла .env можно найти здесь [.env.template](.env.template).
## Создано при помощи
* [Python 3.8](https://www.python.org/downloads/)
* [Django 3.0](https://docs.djangoproject.com/en/3.1/)
* [Django-REST-Framework 3.11](https://www.django-rest-framework.org/)
* [Docker-compose](https://docs.docker.com/compose/)
