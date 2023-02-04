# Проект №1   
## Telegram-bot конвертер валюты. 

## Оглавление  
[1. Постановка задачи](https://github.com/olpachino/Project_BGG_rating/blob/master/README.md#Постановка-задачи)  
[2. Содержание и результаты работы](https://github.com/olpachino/Project_BGG_rating/blob/master/README.md#Содержание-и-результаты-работы)   

### Постановка задачи  

**Задача:** Напишите _Telegram-бота_, в котором будет реализован следующий функционал:

1. Бот возвращает цену на определённое количество валюты (евро, доллар или рубль). 
2. При написании бота необходимо использовать библиотеку `pytelegrambotapi`. 
3. Человек должен отправить сообщение боту в виде `<имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>`. 
4. При вводе команды **/start** или **/help** пользователю выводятся инструкции по применению бота. 
5. При вводе команды **/values** должна выводиться информация о всех доступных валютах в читаемом виде. 
6. Для получения курса валют необходимо использовать любое удобное API и отправлять к нему запросы с помощью библиотеки `Requests`. 
7. Для парсинга полученных ответов использовать библиотеку `JSON`. 
8. При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число) вызывать собственно написанное исключение `APIException` с текстом пояснения ошибки. 
9. Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения. 
10. Для отправки запросов к API описать класс со статическим методом `get_price()`, который принимает три аргумента и возвращает нужную сумму в валюте: 
 - имя валюты, цену на которую надо узнать, — `base`;
 - имя валюты, цену в которой надо узнать, — `quote`; 
 - количество переводимой валюты — `amount`. 
11. Токен Telegram-бота хранить в специальном конфиге (можно использовать .py файл). 
12. Все классы спрятать в файле `extensions.py`.
  
:arrow_up:[к оглавлению](https://github.com/olpachino/Project_BGG_rating/blob/master/README.md#Оглавление)

### Содержание и результаты работы
1. Реаллизован _Telegram-bot_ [@ConvertCoin_bot](https://t.me/ConvertCoin_bot) для конвертации валюты. Исходный код бота [тут](https://github.com/olpachino/SkillFactory-FPW/blob/main/Projects/Telegram_bot/CoinConvert_bot.py)
2. ПО и библиотеки, используемые для реализации  
<p align="center">
<img src="https://img.shields.io/badge/Visual Studio Code- -blue.svg">    <img src="https://img.shields.io/badge/Telegram- -blue.svg">
</p>
<p align="center">
<img src="https://img.shields.io/badge/python-3.9.13-green.svg">    <img src="https://img.shields.io/badge/pyTelegramBotAPI-4.9.0-green.svg">    <img src="https://img.shields.io/badge/requests-2.28.1-green.svg">    <img src="https://img.shields.io/badge/JSON-1.3.0-green.svg">
 </p>   
 
3. Данные о курсе валют собираются через [API](https://www.cbr.ru/lk_uio/guide/rest_api/) с [сайта Центрального Банка РФ](https://www.cbr.ru/). Реализация выполнена в статическом методе `get_price` в файле [extensions.py](https://github.com/olpachino/SkillFactory-FPW/blob/main/Projects/Telegram_bot/extensions.py)
4. Все классы вынесены в отдельный файл [extensions.py](https://github.com/olpachino/SkillFactory-FPW/blob/main/Projects/Telegram_bot/extensions.py)
5. Все константы описаны в файле [config.py](https://github.com/olpachino/SkillFactory-FPW/blob/main/Projects/Telegram_bot/config.py)
6. Команды для работы с ботом:
    * `/start` и `/help` - подсказывают как оформить запрос для корректной работы бота
    * `/values` - описаны доступные валюты для конвертации
7. Реализован класс исключений `APIException`, для выявления ошибок.

:arrow_up:[к оглавлению](https://github.com/olpachino/Project_BGG_rating/blob/master/README.md#Оглавление)
