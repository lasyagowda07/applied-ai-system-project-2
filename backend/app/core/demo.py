from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner()

dog = Pet("Bruno", "dog")
cat = Pet("Luna", "cat")

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Feed", "feeding", "08:00", "Bruno"))
dog.add_task(Task("Walk", "walking", "18:00", "Bruno"))
cat.add_task(Task("Medicine", "medication", "08:00", "Luna"))

scheduler = Scheduler(owner)

print("=== SCHEDULE ===")
for task in scheduler.generate_schedule():
    print(task)

print("\n=== CONFLICTS ===")
for c in scheduler.detect_conflicts():
    print(c)