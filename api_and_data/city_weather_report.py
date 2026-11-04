import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def check_city(city):
    if city == True or city == False:
        print("В списке есть некорректное название города")
        return False
    if len(city) > 1:
        if city.count(" ") > 0 and city.count("-") > 0:
            print("Ошибка. Некорректное название города. Вероятнее всего вы указали и тире, и пробел как разделитель")
            return False
        if city.count(" ") > 0:
            city_split = city.split()
            for i in city_split:
                if i.isalpha() != True and i != " ":
                    print("В списке есть некорректное название города")
                    return False
        if city.count("-") > 0:
            city_split = city.split("-")
            for i in city_split:
                if i.isalpha() != True and i != "-":
                    print("В списке есть некорректное название города")
                    return False
    return True


def get_coordinates(cities):
    if type(cities) != list:
        print("Ошибка в передаче данных. Введите список городов, например ['Moscow', 'Berlin']")
        return False
    cities = list(set(cities))
    all_cities = []
    unique_cities = []
    for city in cities:
        if check_city(city) == False:
            print(f"пропускаю некорректный город {city}")
            continue
        try:
            response = requests.get(GEO_URL, params={"name": city, "count": 1, "language": "en", "format": "json"},
                                    timeout=10)
            if response.status_code == 200:
                result = response.json()
                if len(result) <= 1:
                    print("Вы ввели несуществующий город")
                    continue

                all_cities.append({"city": result['results'][0]['name'], 'latitude': result['results'][0]['latitude'],
                                       'longitude': result['results'][0]['longitude']})
        except requests.exceptions.RequestException:
            print("Ошибка запроса")
            return False
    for result in all_cities:
        if result not in unique_cities:
            unique_cities.append(result)
    return unique_cities


def get_weather(cities):
    all_cities = get_coordinates(cities)
    if all_cities == False:
        return False
    users_cities = []
    cities = list(set(cities))
    for name_city in cities:
        try:
            for i in all_cities:
                if i['city'].lower() == name_city.lower():
                    response = requests.get(WEATHER_URL, params={"latitude": i['latitude'], "longitude": i['longitude'],
                                                                 "current": "temperature_2m,wind_speed_10m"})
                    if response.status_code == 200:
                        result = response.json()
                        users_cities.append([name_city, result])
        except requests.exceptions.RequestException:
            print("Ошибка запроса")
            return False
    return users_cities


def beautiful_answer(cities):
    total_statistic = []
    users_cities = get_weather(cities)
    most_warms = []
    most_warms_cities = []
    if not users_cities:
        return False
    for city in users_cities:
        statistic = {"City": city[0], "Temperature": city[1]['current']['temperature_2m'],
                     "Wind Speed": city[1]['current']['wind_speed_10m']}
        total_statistic.append(statistic)

    for statistics in total_statistic:
        most_warms.append(statistics["Temperature"])

    most_warms.sort()
    while len(most_warms) > 0:
        for city in total_statistic:
            if city['Temperature'] == most_warms[0]:
                most_warms_cities.append([city["City"], city['Temperature'], city['Wind Speed']])
                most_warms.remove(city['Temperature'])
                total_statistic.remove(city)
                break
        most_warms.sort()
    return most_warms_cities


def main():
    cities = []
    while True:
        choice = input(f"Введите название города, напишите 'стоп', чтобы прекратить\n-> ")
        if choice.lower().strip() == "стоп":
            break

        cities.append(choice)
    try:
        most_warms_cities = beautiful_answer(cities)
        most_warms_cities = most_warms_cities[::-1]
        print(
            f"----------ОТЧЕТ----------\nСамый теплый город: {most_warms_cities[0][0]} | Температура: {most_warms_cities[0][1]}°C | Скорость ветра: {most_warms_cities[0][2]}\n")
        print(f"Остальные города:")
        for i in most_warms_cities[1:]:
            print(f"Город: {i[0]} | Температура: {i[1]}°C | Скорость ветра: {i[2]}")
    except (TypeError, IndexError):
        print("Ошибка в передаче Городов, попробуйте еще раз")


main()
