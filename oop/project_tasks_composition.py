class Task:

    def __init__(self, title, hours):
        self.title = title
        self.hours = hours


class Project:
    def __init__(self):
        self._tasks = []

    def add_task(self, task):
        self._tasks.append(task)

    def remove_task(self, title):
        for task in self._tasks:
            if task.title == title:
                self._tasks.remove(task)
                return True
        return False

    def get_total_hours(self):
        count = 0
        for task in self._tasks:
            count += task.hours

        return count

    def count_tasks(self):
        return len(self._tasks)


# Сценарий 1: пустой проект
empty_project = Project()
print(empty_project.get_total_hours())
print(empty_project.count_tasks())

# Сценарий 2: три задачи
project = Project()
project.add_task(Task("Дизайн экрана входа", 5))
project.add_task(Task("API регистрации", 8))
project.add_task(Task("Тесты", 3))
print(project.get_total_hours())
print(project.count_tasks())

# Сценарий 3: убрать существующую задачу
print(project.remove_task("Тесты"))
print(project.get_total_hours())
print(project.count_tasks())

# Сценарий 4: убрать несуществующую задачу
print(project.remove_task("Деплой"))
print(project.get_total_hours())