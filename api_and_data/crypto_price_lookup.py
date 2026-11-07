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


# Функция для проверки работоспособности запроса https://api.coinlore.net/api/assets/
def check_request(URL_TO_FIND_ID):  # -> на вход дается обычная URL_TO_FIND_ID
    try:
        response = requests.get(URL_TO_FIND_ID, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка в передаче запроса. Код ошибки: {response.status_code}")
            return False
        return response.json()  # -> Возвращает Данные если запрос прошел успешно
    except requests.exceptions.RequestException:
        print('Ошибка запроса')
        return False


# Функция, которая ищет введенную пользователем криптовалюту среди данных в def check_request(URL_TO_FIND_ID)::
def find_id_in_information(actual_crypto_name, result):
    if not result:
        return False
    id_of_users_coin = None
    for coin in result[
        "data"]:
        if coin["symbol"] == actual_crypto_name:
            id_of_users_coin = coin["id"]
            break
    if id_of_users_coin is None:
        print("Ошибка! Монета не нашлась. Перепроверьте название")
        return False
    return id_of_users_coin  # -> Возвращает id монеты (тип - строка)


# Функция для проверки валидности запросов по ссылке для получения информации о конкретной монете
def check_url_to_get_information(URL_TO_GET_INFORMATION, id_of_users_coin):  # -> На вход id монеты и ссылка
    try:
        response = requests.get(f"{URL_TO_GET_INFORMATION}", params={"id": id_of_users_coin}, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка получения данных о монете. Код ошибки: {response.status_code}")
            return False
        return response.json()
    except requests.exceptions.RequestException:
        print('Ошибка запроса')
        return False


def main():
    result = check_request(URL_TO_FIND_ID)
    if not result:
        print("Не удалось загрузить базу монет.")
        return
    while True:
        crypto_name = input(
            "Введите название криптовалюты в трехбуквенном формате (BTC, ETH, BNB и т.д) для получения статистики\n-> ")
        actual_crypto_name = validation_of_crypto_name(crypto_name)
        if not actual_crypto_name:
            continue
        id_of_users_coin = find_id_in_information(actual_crypto_name, result)
        if id_of_users_coin:
                break

    data = check_url_to_get_information(URL_TO_GET_INFORMATION, id_of_users_coin)
    if data and isinstance(data, list) and len(data) > 0:
        coin_info = data[0]
        print(f"МОНЕТА: {coin_info.get('name', 'Неизвестно')}")
        print("----------")
        print(f"Ранг по рыночной капитализации: {coin_info.get('rank', 'Неизвестно')}\nТекущая цена в USD: {coin_info.get('price_usd', 'Неизвестно')}")
        print(
            f"Изменение цены в % за последние 24 часа: {coin_info.get('percent_change_24h', 'Неизвестно')}\nОбъём торгов за 24ч в USD: {coin_info.get('volume24', 'Неизвестно')}")
    else:
        print("Не удалось получить данные монеты")

if __name__ == "__main__":
    main()
