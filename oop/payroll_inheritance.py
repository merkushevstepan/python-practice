class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_salary(self):
        return self.salary

    def get_info(self):
        return f"{self.name}: {self.get_salary()}"


class Developer(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def get_salary(self):
        return self.salary + self.bonus


class Manager(Employee):
    def __init__(self, name, salary, team_members):
        super().__init__(name, salary)
        self.team_members = team_members

    def get_salary(self):
        return self.salary + 5000 * self.team_members


class Intern(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)

    def get_salary(self):
        return self.salary // 2


def total_payroll(employees):
    summ_salary = 0
    for worker in employees:
        summ_salary += worker.get_salary()
    return summ_salary


anna = Employee("Анна", 1000)
petya = Developer("Петя", 1000, 500)
egor = Manager("Егор", 1000, 1)
vasya = Intern("Вася", 1000)

total = total_payroll([anna, petya, egor, vasya])
print(total)
