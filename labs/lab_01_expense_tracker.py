import json
from datetime import date

current_year = date.today().year


def get_content(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
    except FileNotFoundError:
        print("Файл не найден! Актуальные данные - пустой список")
        content = []
    except json.decoder.JSONDecodeError:
        print("Невалидный JSON. Вместо записи и чтения данных выведется пустой список")
        content = []
    return content


def add_expense(path, expense, category, timestamp, comment=None):
    content = get_content(path)
    content.append({"expense": expense, "category": category, "date": timestamp, "comment": comment})
    for i in content:
        date_actual = i["date"]
        if date_actual[4] != "-" or date_actual[5] != "-" or date_actual[6] != "-" or date_actual[7] != "-":
            return False
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
        return True


def delete_expense(path, expense, category, timestamp):
    content = get_content(path)
    for i in content:
        if i["category"] == category and i["expense"] == expense and i["date"] == timestamp:
            content.remove(i)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            return True
    return False


def get_statistic(path, month, year, category=None):
    if month > 12 or month <= 0 or year > current_year:
        raise ValueError("Месяц должен быть от 1 до 12")
    content = get_content(path)
    sum_of_total_expense = 0
    list_of_total_expenses = []
    total_expense = {}
    try:
        for i in content:
            date_actual = i["date"]
            date_split = date_actual.split("-")
            if category is None:
                if month == int(date_split[1]) and year == int(date_split[0]):
                    total_expense[i["category"]] = total_expense.get(i["category"], 0) + i["expense"]
                    sum_of_total_expense += i["expense"]

            else:
                if month == int(date_split[1]) and year == int(date_split[0]) and i["category"] == category:
                    sum_of_total_expense += i["expense"]
                    list_of_total_expenses.append(i)
        if total_expense:
            list_of_total_expenses.append(total_expense)
        return list_of_total_expenses, round(sum_of_total_expense, 2)
    except ValueError as error:
        print(error)


