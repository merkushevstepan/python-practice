class User:


    def __init__(self, name, age):
        result = self.set_age(age)
        if result == True:
            self._age = age
        else:
            self._age = 0
        self.name = name


    def set_age(self, new_age):
        if new_age < 0 or new_age > 120:
            return False
        self._age = new_age
        return True


    def get_age(self):
        return self._age




anna = User("Анна", 25)
print(anna.get_age())

print(anna.set_age(30))
print(anna.get_age())

print(anna.set_age(200))
print(anna.get_age())

print(anna.set_age(0))
print(anna.set_age(120))
print(anna.set_age(-1))
print(anna.set_age(121))

vasya = User("Вася", 500)
print(vasya.get_age())

print(anna.name)