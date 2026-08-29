from back import Habit, HabitStore

def test_correct_habit_add():
    habit = Habit("Trening", None, 0, 0, 0)
    habit_methods = HabitStore()
    result_add = habit_methods.add(habit)
    assert result_add is True

def test_is_habit_present_after_remove():
    habit = Habit("Trening", None, 0, 0, 0)
    habit_methods = HabitStore()
    habit_methods.add(habit)
    result_remove =  habit_methods.remove("Trening")
    assert result_remove is True
    assert habit_methods.find("Trening") is None

def test_habit_find():
    habit = Habit("Trening", None, 0, 0, 0)
    habit_methods = HabitStore()
    habit_methods.add(habit)
    result_find = habit_methods.find("Trening")
    assert result_find is not None
    assert result_find.name == "Trening"

def test_find_empty_habit():
    habit = Habit("Trening", None, 0, 0, 0)
    habit_methods = HabitStore()
    habit_methods.add(habit)
    habit_methods.remove("Trening")
    assert habit_methods.find("Trening") is None

def test_remove_empty_habit():
    habit_methods = HabitStore()
    result = habit_methods.remove("Trening")
    assert result is False

def test_habit_duplicates():
    habit = Habit("Trening", None, 0, 0, 0)
    habit2 = Habit("Trening", None, 0, 0, 0)
    habit_methods = HabitStore()
    habit_methods.add(habit)
    assert habit_methods.add(habit2) is False

def test_find_empty_habit():
    habit_methods = HabitStore()
    assert habit_methods.find("Trening") is False

def test_habit_name_letter_size():
    habit = Habit("Trening", None, 0, 0, 0)
    habit_methods = HabitStore()
    result = habit_methods.find("tRENING")
    assert result is not None
    assert habit.name == "Trening"
