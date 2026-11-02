import json
from datetime import date

current_year = date.today().year


def check_data(timestamp):
    try:
        d = date.fromisoformat(timestamp)
        return d
    except (ValueError, TypeError):
        print("Ошибка в обработке даты")
        return None


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
    d = check_data(timestamp)
    if d is None:
        return False
    if isinstance(expense, (int, float)) == False:
        return False
    if expense <= 0:
        return False
    content = get_content(path)
    try:
        content.append({"expense": expense, "category": category.lower(), "date": timestamp, "comment": comment})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
            return True
    except (ValueError, TypeError, SyntaxError):
        print("Ошибка в передаче даты")
        return False


def delete_expense(path, expense, category, timestamp):
    content = get_content(path)
    for i in content:
        if i["category"] == category.lower() and i["expense"] == expense and i["date"] == timestamp:
            content.remove(i)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            return True
    return False


def get_statistic(path, month, year, category=None):
    if month > 12 or month <= 0:
        raise ValueError("Месяц должен быть от 1 до 12")
    content = get_content(path)
    sum_of_total_expense = 0
    total_expense = {}
    try:
        for i in content:
            d = check_data(i["date"])
            if d is None:
                raise ValueError("Некорректная дата")
            if category is None:
                if d.month == month and d.year == year:
                    total_expense[i["category"]] = total_expense.get(i["category"], 0) + i["expense"]
                    sum_of_total_expense += i["expense"]

            else:
                if d.month == month and d.year == year and i["category"] == category.lower():
                    total_expense[i["category"]] = total_expense.get(i["category"].lower(), 0) + i["expense"]
                    sum_of_total_expense += i["expense"]
        for name, value in total_expense.items():
            total_expense[name] = round(value, 2)
        return total_expense, round(sum_of_total_expense, 2), True
    except (ValueError, IndexError) as error:
        print(error)
        return total_expense, round(sum_of_total_expense, 2), False


