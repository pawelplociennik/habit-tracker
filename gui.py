import datetime
import tkinter as tk
from tkinter import ttk
from back import Habit, HabitStore
from back import today
from tkinter import messagebox

def handle_choices(event=None):

    selection = list_box.curselection()
    if not selection:
        return

    index = selection[0]
    habit_name = list_box.get(index)  # nazwa nawyku kliknięta w Listbox

    habit = tracker_store.find(habit_name)  # bierzemy obiekt Habit z backendu
    if habit is None:
        messagebox.showinfo("Błąd", "Nie znaleziono nawyku")
        return

    # Aktualizujemy panel szczegółów (StringVar -> automatycznie odświeża labelki)
    name.set(habit.name)
    streak.set(str(habit.streak))
    points.set(str(habit.total_points))

def clear_details():
    name.set("-")
    streak.set("-")
    points.set("-")

def list_refresh():
    habit_names =[habit.name for habit in tracker_store.habits]
    list_str.set(habit_names)

def habit_add():
    habit_name = entry_var.get().strip()

    if habit_name == "":
        messagebox.showerror("Brak nawyku","Wpisz nowy nawyk i zatwierdź klawiszem 'dodaj'")
        return

    habit = Habit(habit_name, None, 1, 0, 0)

    if tracker_store.add(habit):
        list_refresh()
    else:
        messagebox.showinfo("Duplikat", "Wprowadź inny nawyk")

    entry_var.set("")

tracker_store = HabitStore()


def habit_remove():
    selection = list_box.curselection()
    if not selection:
        messagebox.showwarning("Brak wyboru", "Zaznacz nawyk do usunięcia.")
        return
    index = selection[0]
    habit_list = list_box.get(index)
    if tracker_store.remove(habit_list):
        list_refresh()
    entry_var.set("")

def habit_done():
    selection = list_box.curselection()
    if not selection:
        messagebox.showwarning("Brak wyboru", "Zaznacz nawyk do odznaczenia")
        return
    index = selection[0]
    habit_name = list_box.get(index)

    if habit_name is None:
        messagebox.showinfo("Brak nawyku", "Nie znaleziono nawyku.")
        return

    done = tracker_store.mark_habit_done(habit_name, today())
    if done:
        list_refresh()
        handle_choices()
    else:
        messagebox.showinfo("Już odhaczone", "Ten nawyk został już dziś odhaczony.")   # odświeża szczegóły po praweej

def habit_edit():
    selection = list_box.curselection()
    if not selection:
        messagebox.showwarning("Nie zaznaczono nawyku", "Zaznacz nawyk")
        return
    old_habit = list_box.get(selection[0])
    new_habit = entry_var.get().strip()
    if tracker_store.name_update(old_habit, new_habit):
        list_refresh()
        handle_choices()
    entry_var.set('')

def tick():
    # odświeża tekst co 1 sekundę
    date_time.set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    root.after(1000, tick)

root = tk.Tk()
root.title("Habit Tracker")
root.geometry("400x600")
root.bind("<Return>",lambda event: habit_add())
root.bind("<Delete>",lambda event: habit_remove())
root.bind("<space>",lambda event: habit_done())
root.bind("<F2>",lambda event: habit_edit())

date_time = tk.StringVar(value="")

#top header line
header_frame = ttk.Frame(root, padding = 20)
header_frame.pack()
header_label = ttk.Label(header_frame, text = "Habit Tracker")
header_label.config(font = ("ArialBlack", 20))
header_label.pack()

# middle frame

content_frame = ttk.Frame(root, padding = 20)
content_frame.pack(fill = "both", expand = True)
content_frame.columnconfigure([0], weight=1)
content_frame.columnconfigure([1], weight=1)


# middle left list

content_label = ttk.Label(content_frame, text = "Lista nawyków:")
content_label.config(font = ("TimesNewRoman", 18))
content_label.grid(row = 0, column = 0, sticky="w", pady=(0,10))

entry_var = tk.StringVar(value="")
list_str = tk.StringVar(value=[])
list_box = tk.Listbox(content_frame,
            height = 10,
            width = 20,
            listvariable = list_str)
list_box.grid(column=0, row=1, sticky="nsew")  # rozciąga w pionie i poziomie
content_frame.rowconfigure(1, weight=1)        # już masz, ale tu pasuje logicznie
content_frame.columnconfigure(0, weight=1)
list_box.bind("<<ListboxSelect>>", handle_choices)

habit_name_label = ttk.Label(content_frame, text = "wprowadź nazwę nawyku")
habit_name_label.config(font = ("TimesNewRoman", 16))
habit_name_label.grid(column=0, row=2, sticky="nsew", pady=(20,0))

#middle right frame
details_frame = ttk.Frame(content_frame, padding = 20)
details_frame.grid(row = 1, column = 1, sticky="nsew")

content_frame.rowconfigure(1, weight=1)
details_frame.columnconfigure(0, weight=2)
details_frame.columnconfigure(1, weight=1)

#middle right
name = tk.StringVar(value="-")
streak = tk.StringVar(value="-")
points = tk.StringVar(value="-")

details_label = ttk.Label(content_frame, text = "Szczegóły:")
details_label.config(font = ("TimesNewRoman", 18))
details_label.grid(row = 0, column = 0, columnspan=2, sticky="e", pady=(0,10))



ttk.Label(details_frame, text = "Nazwa").grid(row = 1, column = 0,padx=(0,10),sticky="w")
ttk.Label(details_frame, textvariable =name).grid(row = 1, column = 1,sticky="w")

ttk.Label(details_frame, text = "Streak").grid(row = 2, column = 0,padx=(0,10,),sticky="w")
ttk.Label(details_frame, textvariable=streak).grid(row = 2, column = 1,sticky="w")

ttk.Label(details_frame, text = "Points").grid(row = 3, column = 0,padx=(0,10),sticky="w")
ttk.Label(details_frame, textvariable=points).grid(row = 3, column = 1,sticky="w")

#buttons
buttons_frame = ttk.Frame(root)
buttons_frame.pack(fill="x")

input_entry = ttk.Entry(buttons_frame, textvariable=entry_var)
input_entry.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,10))
input_entry.focus_set()

buttons_frame.columnconfigure(0, weight=1)
buttons_frame.columnconfigure(1, weight=1)

add_button = tk.Button(buttons_frame, command = habit_add)
add_button.config(font = ("TimesNewRoman", 18),text="Dodaj")
add_button.grid(row = 1, column = 0,padx=(0,10),sticky="ew")

delete_button = tk.Button(buttons_frame, command=habit_remove)
delete_button.config(font = ("TimesNewRoman", 18), text="Usuń")
delete_button.grid(row=1, column = 1,padx=(0,10),sticky="ew")

mark_button = tk.Button(buttons_frame, command=habit_done)
mark_button.config(font = ("TimesNewRoman", 18), text="Odznacz")
mark_button.grid(row=2, column = 0,padx=(0,10),sticky="ew")

edit_button = tk.Button(buttons_frame, command=habit_edit)
edit_button.config(font = ("TimesNewRoman", 18), text="Edytuj")
edit_button.grid(row=2, column = 1,padx=(0,10),sticky="ew")


bottom_frame = ttk.Frame(root)
bottom_frame.pack()

date_label = ttk.Label(bottom_frame, textvariable = date_time)
date_label.config(font = ("TimesNewRoman", 12))
date_label.grid(row = 2, column = 1,padx=(0,10), pady=(10,10),sticky="w")

tick()
tracker_store.load()
list_refresh()

root.mainloop()