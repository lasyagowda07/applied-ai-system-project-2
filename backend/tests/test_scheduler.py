from app.core.pawpal_system import Owner, Pet, Task, Scheduler


def test_scheduler_sorts_tasks_by_time():
    owner = Owner()
    pet = Pet("Bruno", "dog")

    pet.add_task(Task("Evening walk", "walking", "18:00", "Bruno"))
    pet.add_task(Task("Morning food", "feeding", "08:00", "Bruno"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_time()

    assert sorted_tasks[0].time == "08:00"
    assert sorted_tasks[1].time == "18:00"


def test_scheduler_detects_same_time_conflicts():
    owner = Owner()
    pet = Pet("Bruno", "dog")

    pet.add_task(Task("Food", "feeding", "08:00", "Bruno"))
    pet.add_task(Task("Medicine", "medication", "08:00", "Bruno"))

    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0]["time"] == "08:00"