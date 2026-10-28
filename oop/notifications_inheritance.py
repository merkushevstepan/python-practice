class Notification:
    def __init__(self, recipient, text):
        self.recipient = recipient
        self.text = text

    def get_message(self):
        return f"[{self.recipient}] {self.text}"

    def is_valid(self):
        if len(self.text.split()) == 0:
            return False
        return True


class EmailNotification(Notification):
    def __init__(self, recipient, text, subject):
        super().__init__(recipient, text)
        self.subject = subject

    def get_message(self):
        return f"[{self.recipient}] Тема: {self.subject} | {self.text}"


class SmsNotification(Notification):
    def get_message(self):
        if len(self.text) > 10:
            formatted_text = self.text[:10] + '...'
            return f"[{self.recipient}] {formatted_text}"
        return f"[{self.recipient}] {self.text}"


# 1. Базовый класс
base = Notification("anna@mail.ru", "Ваш платёж принят")
print(base.get_message())

# 2. Почта
email = EmailNotification("anna@mail.ru", "Ваш платёж принят", "Платёж")
print(email.get_message())

# 3. SMS, длинный текст
sms_long = SmsNotification("+79001234567", "Привет, мир! Это тест")
print(sms_long.get_message())

# 4. SMS, короткий текст
sms_short = SmsNotification("+79001234567", "Привет")
print(sms_short.get_message())

# 5. Проверка текста
print(Notification("a@b.ru", "   ").is_valid())
print(EmailNotification("a@b.ru", "", "Тема").is_valid())
print(SmsNotification("+7900", "Привет").is_valid())

# 6. Отношение «является видом»
print(isinstance(email, Notification))

# Дополнительно: граница в SMS (ровно 10 символов)
print(SmsNotification("+7900", "1234567890").get_message())
