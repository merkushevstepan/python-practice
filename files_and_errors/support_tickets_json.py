import json


def check_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
    except json.decoder.JSONDecodeError:
        print("Невалидный JSON. Вместо записи и чтения данных выведется пустой список")
        content = []
    except FileNotFoundError:
        print("Ошибка! Файл не найден. Файл будет создан со значением []")
        content = []
    return content


def add_ticket(path, title, priority):
    content = check_file(path)
    maximum = 0
    for i in content:
        if i["id"] > maximum:
            maximum = i["id"]
    content.append({"id": maximum + 1, "title": title, "priority": priority, "status": "open"})
    identity = content[-1]["id"]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
        return identity


def close_ticket(path, ticket_id):
    content = check_file(path)
    if ticket_id <= 0:
        print("ID не может быть <= 0")
        return False
    for i in content:
        if i["id"] == ticket_id:
            if i["status"] == "closed":
                return False
            i["status"] = "closed"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
                return True
    return False


def get_open_tickets(path, priority=None):
    content = check_file(path)
    all_tickets = []
    if priority is None:
        for i in content:
            if i["status"] == "open":
                all_tickets.append(i)
    else:
        for i in content:
            if i["priority"] == priority:
                if i["status"] == "open":
                    all_tickets.append(i)
    return all_tickets
