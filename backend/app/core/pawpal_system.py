from datetime import datetime, timedelta


class Task:
    def __init__(self, description, task_type, time, pet_name, recurrence=None, priority=1):
        self.description = description
        self.task_type = task_type
        self.time = time  # string "HH:MM"
        self.pet_name = pet_name
        self.recurrence = recurrence  # None, "daily", "weekly"
        self.priority = priority
        self.completed = False

    def mark_complete(self):
        self.completed = True

        # handle recurrence
        if self.recurrence == "daily":
            next_time = self._next_day(self.time)
            return Task(
                self.description,
                self.task_type,
                next_time,
                self.pet_name,
                self.recurrence,
                self.priority,
            )
        return None

    def _next_day(self, time_str):
        t = datetime.strptime(time_str, "%H:%M")
        t = t + timedelta(days=1)
        return t.strftime("%H:%M")

    def __repr__(self):
        return f"{self.pet_name} | {self.task_type} | {self.time} | Completed: {self.completed}"


class Pet:
    def __init__(self, name, species, age=None):
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks


class Owner:
    def __init__(self, name="Pet Owner", email="default@email.com"):
        self.name = name
        self.email = email
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def get_all_tasks(self):
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def get_all_tasks(self):
        return self.owner.get_all_tasks()

    def sort_tasks_by_time(self):
        tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda x: x.time)

    def filter_by_pet(self, pet_name):
        return [t for t in self.get_all_tasks() if t.pet_name == pet_name]

    def filter_by_status(self, completed=False):
        return [t for t in self.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self):
        tasks = self.sort_tasks_by_time()
        conflicts = []

        for i in range(len(tasks) - 1):
            if tasks[i].time == tasks[i + 1].time:
                conflicts.append((tasks[i], tasks[i + 1]))

        return conflicts

    def generate_schedule(self):
        return self.sort_tasks_by_time()