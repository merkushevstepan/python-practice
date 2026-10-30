import json


def save_subscribers(subscribers, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(subscribers, f, ensure_ascii=False, indent=2)


def load_subscribers(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
            return content
    except json.decoder.JSONDecodeError:
        print("Невалидный JSON. Вместо данных файла выведен пустой список")
        content = []
        return content
    except FileNotFoundError:
        print("Файла нет, актуальные данные - пустой список")
        content = []
        return content


def count_by_plan(subscribers):
    plans = {}
    for i in subscribers:
        plans[i["plan"]] = plans.get(i['plan'], 0) + 1
    return plans




