# Emphasoft
<h1> Тестовое задание </h1>

Реализация авторизации пользователей через Google на Flask

`app.py` - основоной файл с функциями представления \
`oauth1.py` - реализация получения и отправления запросов провайдерам OAuth \
`config.py` - настройи приложения(база и ключи) 
<h3>Развертывание на римере heroku</h3>
Установка Heroku CLI 
После установки нужно войти в аккаунт

```sh
$ heroku login
```

Далее с помощью git клонируем приложение:
```sh
$ git clone https://github.com/nailprik/Emphasoft
$ cd Emphasoft
```
Создаем приложение Heroku
```sh
$ heroku apps:create emphasoft101
Creating ⬢ emphasoft101... done
https://emphasoft101.herokuapp.com/ | https://git.heroku.com/emphasoft101.git
```
Переносим приложение в гланую ветвь репозитория Heroku git
```sh
$ git checkout -b deploy
$ git push heroku deploy:master
```

Приложение будет развернуто по ссылке в ввыводе консоли
