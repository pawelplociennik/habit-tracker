from pathlib import Path
import json
from datetime import date
import smtplib
from email.message import EmailMessage
from functools import partial

def today() -> str:
    return date.today().isoformat()

class Habit:
    def __init__(self, name: str, last_done: str | None, points_per_done: int, total_points: int, streak: int):
        self.name = name                  # nazwa nawyku (np. "Trening")
        self.last_done = last_done        # ostatnia data wykonania w formacie "YYYY-MM-DD" albo None
        self.points_per_done = points_per_done  # ile punktów za jedno odhaczenie
        self.total_points = total_points  # suma punktów
        self.streak = streak              # aktualna passa

    def mark_done(self, today_str: str) -> bool:
        if today_str == self.last_done:
            return False
        if self.last_done is None:
            self.streak = 1
        else:
            last_date = date.fromisoformat(self.last_done)
            today_date = date.fromisoformat(today_str)
            if (today_date - last_date).days == 1:
                self.streak += 1
            else:
                self.streak = 1
        self.last_done = today_str
        self.total_points += self.points_per_done
        return True

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "last_done": self.last_done,
            "points_per_done": self.points_per_done,
            "total_points": self.total_points,
            "streak": self.streak,
        }

    @classmethod
    def from_dict(cls, habit_data: dict):
        return cls(
            habit_data["name"],
            habit_data["last_done"],
            habit_data["points_per_done"],
            habit_data["total_points"],
            habit_data["streak"],
    )

def autosave(func):
    def functionWithWrapper(self,*args, **kwargs):
        result = func(self,*args, **kwargs)
        if result:
            self.save()
        return result
    return functionWithWrapper

class HabitStore:

    def __init__(self, *habits, filename="habits.json"):
        self.habits = list(habits)  # lista obiektów Habit
        self.filename = filename

    def find(self, name: str):
        name = name.strip().lower()
        for habit in self.habits:
            if habit.name.lower() == name:
                return habit
        return None

    @autosave
    def add(self, habit: Habit) -> bool:
        selection = self.find(habit.name)  # (string)
        if selection is None:
            self.habits.append(habit)
            return True
        return False

    @autosave
    def mark_habit_done(self, name: str, today_str: str) -> bool:
        habit_find = self.find(name)
        if habit_find is None:
            return False
        return habit_find.mark_done(today_str)

    @autosave
    def remove(self, name: str) -> bool:
        habit = self.find(name)
        if habit is not None:
            self.habits.remove(habit)
            return True
        return False

    def save(self) -> None:
        file = Path(self.filename)
        json_data = [habit.to_dict() for habit in self.habits]
        json_text = json.dumps(json_data,ensure_ascii=False,indent = 2)
        file.write_text(json_text,encoding="utf-8")

    def load(self) -> None:
        file = Path(self.filename)
        if not file.exists():
            self.habits =[]
            return
        readfile = file.read_text(encoding="utf-8")
        if readfile.strip() == "":
            self.habits = []
            return
        data = json.loads(readfile)
        self.habits = [Habit.from_dict(habit) for habit in data]

    @autosave
    def name_update(self, oldname: str,newname: str)-> bool:
        newname = newname.strip()
        habit_find_old = self.find(oldname)
        habit_find_new = self.find(newname)
        if habit_find_old is None:
            return False
        if newname == "":
            return False
        if habit_find_new is not None and habit_find_new != habit_find_old:
            return False
        habit_find_old.name = newname
        return True

def sort_by_name(self):
    self.habits.sort(key=lambda habit_find:habit_find.name)
    return self.habits

def email_reminder(self,user,password,to,subject="Przypomnienie"):
    body="Zrób trening!"
    message = EmailMessage()
    message["From"] = user
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(user,password)
            smtp.send_message(message)

    except Exception as e:
        print(f"błąd - {e}")


def email_reminder_with_date(self, habit:Habit):
    date_today = date.today()
    if habit.last_done is None:
        print("wyślij przypomnienie!")
        return

    last_done = date.fromisoformat(habit.last_done)

    email = email_reminder()

    if (date_today - last_done).days > 0:
        print("wyślij przypomnienie!")


if __name__ == "__main__":
    store = HabitStore()
    store.load()
    main(store)
'''
