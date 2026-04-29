from datetime import datetime, timedelta


class Task:
    def __init__(
        self,
        description,
        task_type,
        time,
        pet_name,
        recurrence=None,
        priority=1,
        duration=15,
    ):
        self.description = description
        self.task_type = task_type
        self.time = time
        self.pet_name = pet_name
        self.recurrence = recurrence
        self.priority = priority
        self.duration = duration
        self.completed = False

    def mark_complete(self):
        self.completed = True

        if self.recurrence == "daily":
            return self.create_next_occurrence(days=1)

        if self.recurrence == "weekly":
            return self.create_next_occurrence(days=7)

        return None

    def create_next_occurrence(self, days):
        base_time = datetime.strptime(self.time, "%H:%M")
        next_time = base_time + timedelta(days=days)

        return Task(
            description=self.description,
            task_type=self.task_type,
            time=next_time.strftime("%H:%M"),
            pet_name=self.pet_name,
            recurrence=self.recurrence,
            priority=self.priority,
            duration=self.duration,
        )

    def to_dict(self):
        return {
            "pet_name": self.pet_name,
            "description": self.description,
            "task_type": self.task_type,
            "time": self.time,
            "recurrence": self.recurrence,
            "priority": self.priority,
            "duration": self.duration,
            "completed": self.completed,
        }


class Pet:
    def __init__(self, name, species="unknown", age=None):
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks

    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }


class Owner:
    def __init__(self, name="Pet Owner", email="default@email.com"):
        self.name = name
        self.email = email
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def get_pet(self, pet_name):
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def list_pets(self):
        return self.pets

    def get_all_tasks(self):
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "pets": [pet.to_dict() for pet in self.pets],
        }


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def get_all_tasks(self):
        return self.owner.get_all_tasks()

    def sort_tasks_by_time(self):
        tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda task: task.time or "99:99")

    def filter_by_pet(self, pet_name):
        return [
            task
            for task in self.get_all_tasks()
            if task.pet_name.lower() == pet_name.lower()
        ]

    def filter_by_status(self, completed=False):
        return [task for task in self.get_all_tasks() if task.completed == completed]

    def detect_conflicts(self):
        tasks = self.sort_tasks_by_time()
        conflicts = []

        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                first = tasks[i]
                second = tasks[j]

                if first.time and second.time and first.time == second.time:
                    conflicts.append(
                        {
                            "time": first.time,
                            "message": f"{first.pet_name} has '{first.description}' and {second.pet_name} has '{second.description}' at the same time.",
                            "tasks": [first.to_dict(), second.to_dict()],
                        }
                    )

        return conflicts

    def generate_daily_schedule(self):
        return [task.to_dict() for task in self.sort_tasks_by_time()]

    def complete_task(self, task):
        next_task = task.mark_complete()
        if next_task:
            pet = self.owner.get_pet(task.pet_name)
            if pet:
                pet.add_task(next_task)
        return next_task