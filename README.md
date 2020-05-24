# Comics publisher

## Описание
Скрипт скачивает случаные комиксы с [сайта](https://xkcd.com/) и публикует их в группе [ВК](https://vk.com).

## Требования к окружению
Разработка велась на Python 3.7.3 + IDE PyCharm.

## Как установить
Скачайте и установите зависимости `requirements.txt`

    pip install -r requirements.txt

Создайте группу в ВК, потом `standalone` [приложение](https://vk.com/dev) и привяжите к нему
созданную группу.

Также надо создать `.env` файл рядом со скритом и прописать следующие переменные:

    access_token
    group_id

`access_token` - ключ доступа пользователя. Права нужны такие: `photos`, `groups`, `wall` и `offline`.
Полную инструкцию смотреть [тут](https://vk.com/dev/implicit_flow_user).

`group_id` - айди вашей созданной группы. Узнать айди если что можно [тут](https://regvk.com/id/).

## Примеры запуска

    python script.py
