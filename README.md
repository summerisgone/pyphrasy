# pyphrasy - Склонение по падежам русских словосочетаний.

Мы долго искали способ, как просклонять сложные названия в проекте. Нашли платную библиотеку,
но тем интереснее стало написать своё открытое решение.

Всё просто: устанавливаете пакет ``pyphrasy`` и:

    import pymorphy2
    from pyphrasy.inflect import PhraseInflector

    morph = pymorphy2.MorphAnalyzer()
    inflector = PhraseInflector(morph)
    form = 'gent'
    print inflector.inflect(phrase, form)


Вся работа основана на библиотеке [pymorpy2](https://pymorphy2.readthedocs.org), которая, в свою очередь,
активно использует словари [OpenCorpora](http://opencorpora.org/).

Если вам нравится проделанная работа и вы хотите внести свою лепту - помогите проекту OpenCorpora,
это совсем не сложно.

## Веб-сервис

Проект [запущен на Heroku](http://pyphrasy.herokuapp.com/), и имеет API на http://pyphrasy.herokuapp.com/inflect.
Ожидаю запрос с двумя параметрами:

* phrase - что склонять
* forms - один элемент или список падежей или/и чисел по сокращениям в pymorphy2, разделённые запятой

Например: http://pyphrasy.herokuapp.com/inflect?phrase=склонятор%20словосочетаний&forms=gent,plur&forms=datv


# Как запустить на своем хостинге

Веб-сервис написан на python и испольузет фреймворк Flask. Для работы потребуется установка пакетов, указаных в requirements.txt.

По желанию можно использовать [virtualenv](http://www.unix-lab.org/posts/virtualenv/).

Инструкция для чайников:

1. Скопировать исходный код с github

1.1. Создать и активировать окружение virtualenv (необязательно)


    $ virtualenv .env
    $ source .env/bin/activate

2. Установить зависимости

    $ pip install -r requirements.txt

3. Запустить сервис


        $ python app.py

4. Проверить работоспособность


        $ curl "http://localhost:8000/inflect?phrase=%D1%80%D0%B0%D0%B1%D0%BE%D1%87%D0%B0%D1%8F%20%D0%BA%D0%BE%D0%BF%D0%B8%D1%8F&cases=accs&cases=datv"

## Changelog

### 0.1

начальный релиз

### 0.2.0

- [исправлен](https://github.com/summerisgone/pyphrasy/pull/13) `pip install`
- настроен CI
- обновлены зависимости

### 1.0.0

- Переход на python3
- Замена Flask + gunicorn на aiohttp