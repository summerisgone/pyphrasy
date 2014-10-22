# pyphrasy - Склонение по падежам русских словосочетаний.

Мы долго искали способ, как просклонять сложные названия в проекте. Нашли платную библиотеку,
но тем интереснее стало написать своё открытое решение.

Всё просто:

    import pymorphy2
    from inflect import PhraseInflector, GRAM_CHOICES

    morph = pymorphy2.MorphAnalyzer()
    inflector = PhraseInflector(morph)
    form = 'gent'
    print inflector.inflect(phrase, form)


Вся работа основана на библиотеке [pymorpy2](https://pymorphy2.readthedocs.org), которая, в свою очередь,
активно использует словари [OpenCorpora](http://opencorpora.org/).

Если вам нравится проделанная работа и вы хотите внести свою лепту - помогите проекту OpenCorpora,
это совсем не сложно.

# Веб-сервис


Проект [запущен на Heroku](http://pyphrasy.herokuapp.com/), и имеет API на http://pyphrasy.herokuapp.com/inflect.
Ожидаю запрос с двумя параметрами:

* phrase - что склонять
* forms - один элемент или список падежей или/и чисел по сокращениям в pymorphy2, разделённые запятой

Например: http://pyphrasy.herokuapp.com/inflect?phrase=склонятор%20словосочетаний&forms=gent,plur&forms=datv
