from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import path, re_path

from random import choice
from string import ascii_letters
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.messages.middleware import MessageMiddleware

stats_db = {}




# Задание 3. URL shortener
#
# Реализуйте сервис для сокращения ссылок. Примеры таких сервисов:
# http://bit.ly, http://t.co, http://goo.gl
# Пример ссылки: http://bit.ly/1qJYR0y
#
# Вам понадобится шаблон с формой для отправки ссылки (файл index.html),
# и две функции, одна для обработки запросов GET и POST для сабмита URL
# и отображения результата, и вторая для редиректа с короткого URL на исходный.
# Для хранения соответствий наших коротких ключей и полных URL мы будем
# использовать кеш Django, django.core.cache
# Экземпляр cache уже импортирован, и используется следующим образом.
# Сохранить значение:
#
#  cache.add(key, value)
#
# Извлечь значение:
#
#  cache.get(key, default_value)
#
# Второй аргумент метода get - значение по умолчанию,
# если ключ не найден в кеше.
#
# Вы можете запустить сервер для разработки, и посмотреть
# ответы ваших функций в браузере:
#
# python homework03.py runserver


# Конфигурация, не нужно редактировать
if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['']
        }]
    )


def random_key(key = ""):
    """
    Случайный короткий ключ, состоящий из цифр и букв.
    Минимальная длина ключа - 5 символов. Для генерации случайных
    последовательностей вы можете воспользоваться библиотекой random.
    """
    return key.join(choice(ascii_letters) for i in range(5))
# map(обьект,(єлементы обрабатываемые им))   !!!

def index(request):
    """
    При запросе методом GET, отдаем HTML страницу (шаблон index.html) с формой
    с одним полем url типа text (отредактируйте шаблон, дополните форму).

    При отправке формы методом POST извлекаем url из request.POST и
    делаем следующее:

    1. Проверяем URL. Допускаются следующие схемы: http, https, ftp

    Если URL не прошел проверку - отобразите на нашей странице с формой
    сообщение о том, какие схемы поддерживаются.

    Если URL прошел проверку:

    2. Создаем случайный короткий ключ, состоящий из цифр и букв
    (функция random_key).

    3. Сохраняем URL в кеш со сгенерированным ключом:

    cache.add(key, url)

    4. Отдаем ту же страницу с формой и дополнительно отображаем на ней
    кликабельную короткую ссылку (HTML тег 'a') вида
    http://localhost:8000/<key>
    """
#GET
    if request.method == 'GET':
        return render(request, 'index.html')
#POST
    if request.method == 'POST':
        val = URLValidator()
        url = request.POST.get('url')
        try:
            val(url)
            key = random_key()
            cache.add(key, url)
            return render(request, 'index.html', {'form':key})
        except ValidationError:
            return render(request, 'index.html', {'form_message': url})


def redirect_view(request, key):
    """
    Функция обрабатывает сокращенный URL вида http://localhost:8000/<key>
    Ищем ключ в кеше (cache.get). Если ключ не найден,
    редиректим на главную страницу (/). Если найден,
    редиректим на полный URL, сохраненный под данным ключом.
    """
    global stats_db
    url = cache.get(key, 'None')
    if url == 'None':
        return redirect(to='/')
    try:
        stats_db[key] += 1
    except:
        stats_db[key] = 1
    return redirect(to=url)


def stats(request, key):
    """
    Статистика кликов на сокращенные ссылки.
    В теле ответа функция возращает количество
    переходов по данному коду.
    """
    if request.method == "GET":
        global stats_db
        count = stats_db[key]
    else:
        count = 0
    return render(request, 'index.html', {'form_count': count})


urlpatterns = [
    path('', index),
    re_path(r'^(?P<key>\w+)$', redirect_view),
    re_path(r'^(?P<key>\w+)/stats$', stats),
]


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
