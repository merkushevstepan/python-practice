import requests

# Принцип работы кода: пользователь вводит три буквы названия монеты
# Далее скрипт отправляет запрос на https://api.coinlore.net/api/assets/ (там данные всех криптовалют что только есть)
# Далее идем циклом по выгруженным данным и достаем инфу про введенную пользователем монету
# Скрипт достает id монеты и достает данные по ссылке https://api.coinlore.net/api/ticker/?id=ВВЕДЕННОЕ IP
# Показывает красивую статистику
URL_TO_FIND_ID = "https://api.coinlore.net/api/assets/"
URL_TO_GET_INFORMATION = "https://api.coinlore.net/api/ticker/"


# функция проверяющая валидность введенного имя монеты
def validation_of_crypto_name(crypto_name):  # -> на вход дается строка, например "BTC"
    if type(crypto_name) != str:
        print("Ошибка в передаче названии монеты")
        return False
    for word in crypto_name:
        if word.isalpha() == False:
            print("Ошибка в передаче названии монеты. Вероятно вы передали символы, не являющиеся буквами")
            return False
    if len(crypto_name) == 0 or len(crypto_name) == 1:
        print("Ошибка! Вы ввели пустую строку или название монеты длиной в одну букву")
        return False
    actual_crypto_name = crypto_name.upper()
    return actual_crypto_name  # -> Возвращает название монеты в стандартном виде BTC. ETH и т.д


# Функция для проверки работоспособности запроса
def check_request(url):  # -> на вход дается обычная ссылка из переменных URL_TO_GET_INFORMATION либо URL_TO_FIND_ID
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка в передаче запроса. Код ошибки: {response.status_code}")
            return False  # -> Возвращает False, если запрос оказался с ошибкой
        return True  # -> Возвращает True, если запрос прошел успешно
    except requests.exceptions.RequestException:
        print('Ошибка запроса')
        return False


# Функция, выгружающая данные с запроса по ссылке URL_TO_FIND_ID = "https://api.coinlore.net/api/assets/"
def download_information_for_find_id():
    result = check_request(URL_TO_FIND_ID)
    if result != True:  # -> Если запрос оказался с ошибкой - возвращает False
        return result
    response = requests.get(URL_TO_FIND_ID, timeout=10)
    information = response.json()
    return information  # -> Возвращает объем данных {"data": [{"id": "90","symbol": "BTC","name": "Bitcoin","nameid": "bitcoin","rank": 1},{"id": "80","symbol": "ETH","name": "Ethereum","nameid": "ethereum","rank": 2 И Т.Д


# #Функция, которая ищет введенную пользователем криптовалюту среди данных в information из download_information_for_find_id():
def find_id_in_information(crypto_name):
    total_information = download_information_for_find_id() # -> Выгружаем данные {"data": [{"id": "90","symbol": "BTC"} из def download_information_for_find_id()
    if not total_information:
        return False  # -> Проверяем название монеты на валидность через написанную функцию
    actual_crypto_name = validation_of_crypto_name(crypto_name)
    if actual_crypto_name == False:
        return False
    id_of_users_coin = None
    for coin in total_information["data"]:  # -> Получается coin = {'id': '295', 'symbol': 'DGC', 'name': 'DigitalCoin', 'nameid': 'digitalcoin', 'rank': 4053}
        if coin["symbol"] == actual_crypto_name:
            id_of_users_coin = coin["id"]
            break
    if id_of_users_coin is None:
        print("Ошибка! Монета не нашлась. Перепроверьте название")
        return False  # -> Возвращаем False, если пользователь ввел ошибочное название и монета не нашлась
    return id_of_users_coin  # -> Возвращает id монеты (тип - строка)


# Функция для проверки валидности запросов по ссылке для получения информации о конкретной монете
def check_url_to_get_information(URL_TO_GET_INFORMATION, crypto_name): # -> На вход монета и ссылка
    if not find_id_in_information(crypto_name):
        return False
    id_of_users_coin = find_id_in_information(crypto_name)
    try:
        response = requests.get(f"{URL_TO_GET_INFORMATION}", params={"id": id_of_users_coin}, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка получения данных о монете. Код ошибки: {response.status_code}")
            return False  # -> Возвращает False если произошла ошибка в запросе
        return response.json()  # -> Возвращает данные, если запрос успешен | [{'id': '90', 'symbol': 'BTC', 'name': 'Bitcoin', 'nameid': 'bitcoin', 'rank': 1, 'price_usd': '75644.24', 'percent_change_24h': '-6.00', 'percent_change_1h': '0.06', 'percent_change_7d': '-6.22', 'price_btc': '1.00', 'market_cap_usd': '1510679848115.70', 'volume24': 124679217964.9128, 'volume24a': 123370898601.19148, 'csupply': '19970852.00', 'tsupply': '19970852', 'msupply': '21000000'}]
    except requests.exceptions.RequestException:
        print('Ошибка запроса')
        return False  # -> Возвращает False если произошла ошибка в запросе


# Функция, достающая актуальные данные для монеты, которую ввел пользователь. Для нее нужно вызвать все преждевременные проверки
def get_data_with_crypto_id(crypto_name):
    data = check_url_to_get_information(URL_TO_GET_INFORMATION, crypto_name)
    return data



def main():
    while True:
        crypto_name = input("Введите название криптовалюты в трехбуквенном формате (BTC, ETH, BNB и т.д) для получения статистики\n-> ")
        if validation_of_crypto_name(crypto_name) and find_id_in_information(crypto_name):
            break
    data = get_data_with_crypto_id(crypto_name)
    if find_id_in_information(crypto_name):
        print(f"МОНЕТА: {data[0]["name"]}")
        print("----------")
        print(f"Ранг по рыночной капитализации: {data[0]["rank"]}\nТекущая цена в USD: {data[0]["price_usd"]}")
        print(f"Изменение цены в % за последние 24 часа: {data[0]["percent_change_24h"]}\nОбъём торгов за 24ч в USD: {data[0]["volume24"]}")
main()
# ПЛАН НА ЗАВТРА:
# 1) Сократить запросы: сейчас 9 за один запуск, нужно 2 (check_request + get дублируются, find_id вызывается 4 раза)
# 2) В main проверять data, а не find_id_in_information; кавычки в f-строках (работают только на Python 3.12+)
# 3) По желанию: кэш "тикер -> id" в JSON-файле