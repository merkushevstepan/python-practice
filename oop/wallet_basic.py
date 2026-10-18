class Wallet:


    def __init__(self, owner):
        self.owner = owner
        self._balance = 0


    def deposit(self, amount):
        if amount <= 0:
            return False
        self._balance += amount
        return True


    def withdraw(self, amount):
        if amount > self._balance or amount <= 0:
            return False
        self._balance -= amount
        return True

    @property
    def get_balance(self):
        return self._balance


anna = Wallet("Анна")
anna.deposit(100)
anna.withdraw(50)
print(anna.get_balance)

petya = Wallet("Петя")
petya.deposit(1000)
petya.withdraw(2000)
petya.withdraw(100)
print(petya.get_balance)


