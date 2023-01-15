# Парсер конфигураций ФПСУ-IP

Программа (скрипт) предназнаена для получения следующей информации из текстового фалйа конфигурации ПАК ФПСУ-IP (Амикон):

1. Получение состояния IPFIX-серверов (Да(настроен)/Нет (не настроен).
2. Получение состояния МСЭ ФПСУ-IP (Да/Нет/Строка состояния не найдена в КФГ).
3. Получение информации о первом правиле в МСЭ ФПСУ-IP (Название первого правила в МСЭ).
4. Получение информации о количестве правил в МСЭ ФПСУ-IP (Количество правил в МСЭ ФПСУ-IP).
5. Получение информации об адресах ФПСУ-IP на портах (Все IP адреса на 1 и 2 порту ФПСУ-IP).
6. Получение информации об абонентах на LAN порту ФПСУ-IP (Сеть и маска/Хост).
7. Получение информации об абонентах на WAN порту ФПСУ-IP (Сеть и маска/Хост).


## Подготовка к запуску скрипта:

Устанавливаем  3 библиотеки:
    pytz-2021.3-py2.py3-none-any.whl
    zope.interface-5.4.0.tar.gz
    DateTime-4.3-py2.py3-none-any.whl

## Использование

Если python не установлен в path, команда превращается в /путь/до/папки/где/лежит/python название_скрипта.py

Для удобства меняем рабочую папку в терминале, на папку, где лежит Питон.
Пример команды:	cd "C:\ProgramFiles\Python310\"
Чтобы скрипт отрабатывал быстро, папка с конфигами должна быть на той же тачке, откуда запускается скрипт. С шары будет дольше.

Пример команды после изменения рабочего каталога:
python.exe C:\Users\user\Documents\Parser_FPSU-IP_v0.3.7.py

Далее следуем инструкциям скрипта.

---------------------------------------------------
Примечание: файлы конфигурация для парсинга должны лежать в папке "CFG", расположенной рядом со скриптом.
То есть, елси скрипт у нас расположен по пути: C:\Users\user\Documents\
То, файлы с текстовыми конфигами должны быть в каталоге: C:\Users\user\Documents\CFG\
---------------------------------------------------

Для Python 3.10 и выше:
    
    $ python Parser_FPSU-IP_v1.0.0.py
    

Для Python версии выше 3.6:
    
    $ python Parser_FPSU-IP_v0.3.7.py
