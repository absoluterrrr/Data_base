import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# Змінна для збереження id обраного користувача
select_user_id = None


# =========================
# Робота з базою даних
# =========================

def initdb():
    conn = sqlite3.connect("My_project.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            location TEXT NOT NULL,
            birth_city TEXT NOT NULL,
            telegram TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    # Перевіряємо, чи існують усі необхідні стовпці
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if "location" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN location TEXT NOT NULL DEFAULT ''"
        )

    if "birth_city" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN birth_city TEXT NOT NULL DEFAULT ''"
        )

    if "telegram" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN telegram TEXT NOT NULL DEFAULT ''"
        )

    if "phone" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN phone TEXT NOT NULL DEFAULT ''"
        )

    conn.commit()
    conn.close()


def add_user_db(name, age, location, birth_city, telegram, phone):
    conn = sqlite3.connect("My_project.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (name, age, location, birth_city, telegram, phone)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, age, location, birth_city, telegram, phone)
    )

    conn.commit()
    conn.close()


def choose_user_db():
    conn = sqlite3.connect("My_project.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()

    return rows


def update_user_db(
    user_id,
    name,
    age,
    location,
    birth_city,
    telegram,
    phone
):
    conn = sqlite3.connect("My_project.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET name = ?,
            age = ?,
            location = ?,
            birth_city = ?,
            telegram = ?,
            phone = ?
        WHERE id = ?
        """,
        (
            name,
            age,
            location,
            birth_city,
            telegram,
            phone,
            user_id
        )
    )

    conn.commit()
    conn.close()


def delete_user_db(user_id):
    conn = sqlite3.connect("My_project.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()


# =========================
# Перевірка введених даних
# =========================

def validate_input():
    name = entry_name.get().strip()
    age_str = entry_age.get().strip()
    location = entry_location.get().strip()
    birth_city = entry_birth_city.get().strip()
    telegram = entry_telegram.get().strip()
    phone = entry_phone.get().strip()

    if (
        not name
        or not age_str
        or not location
        or not birth_city
        or not telegram
        or not phone
    ):
        messagebox.showwarning(
            "Помилка",
            "Будь ласка, заповніть всі поля!"
        )
        return None, None, None, None, None, None

    if not age_str.isdigit():
        messagebox.showwarning(
            "Помилка!",
            "Вік повинен бути цілим числом!"
        )
        return None, None, None, None, None, None

    age = int(age_str)

    if age <= 0:
        messagebox.showwarning(
            "Помилка!",
            "Вік повинен бути більше 0!"
        )
        return None, None, None, None, None, None

    return (
        name,
        age,
        location,
        birth_city,
        telegram,
        phone
    )


# =========================
# Оновлення таблиці
# =========================

def load_users():
    for item in tree.get_children():
        tree.delete(item)

    rows = choose_user_db()

    for row in rows:
        tree.insert(
            "",
            "end",
            values=row
        )


# =========================
# Додавання користувача
# =========================

def add_user():
    (
        name,
        age,
        location,
        birth_city,
        telegram,
        phone
    ) = validate_input()

    if name is not None:
        add_user_db(
            name,
            age,
            location,
            birth_city,
            telegram,
            phone
        )

        messagebox.showinfo(
            "Успіх!",
            "Дані користувача були додані."
        )

        clear_fields()
        load_users()


# =========================
# Оновлення користувача
# =========================

def update_user():
    global select_user_id

    if select_user_id is None:
        messagebox.showwarning(
            "Помилка!",
            "Оберіть користувача з таблиці для оновлення."
        )
        return

    (
        name,
        age,
        location,
        birth_city,
        telegram,
        phone
    ) = validate_input()

    if name is not None:
        update_user_db(
            select_user_id,
            name,
            age,
            location,
            birth_city,
            telegram,
            phone
        )

        messagebox.showinfo(
            "Успіх!",
            "Дані користувача були оновлені."
        )

        clear_fields()
        load_users()

        select_user_id = None


# =========================
# Видалення користувача
# =========================

def Delete():
    global select_user_id

    if select_user_id is None:
        messagebox.showwarning(
            "Помилка!",
            "Оберіть користувача з таблиці для видалення."
        )
        return

    answer = messagebox.askyesno(
        "Підтвердження",
        "Ви дійсно хочете видалити цього користувача?"
    )

    if answer:
        delete_user_db(select_user_id)

        messagebox.showinfo(
            "Успіх!",
            "Користувача було видалено."
        )

        clear_fields()
        load_users()

        select_user_id = None


# =========================
# Вибір користувача
# =========================

def on_select_user(event):
    global select_user_id

    selected = tree.selection()

    if not selected:
        return

    item = tree.item(selected[0])
    values = item["values"]

    if values:
        select_user_id = values[0]

        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[1])

        entry_age.delete(0, tk.END)
        entry_age.insert(0, values[2])

        entry_location.delete(0, tk.END)
        entry_location.insert(0, values[3])

        entry_birth_city.delete(0, tk.END)
        entry_birth_city.insert(0, values[4])

        entry_telegram.delete(0, tk.END)
        entry_telegram.insert(0, values[5])

        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, values[6])


# =========================
# Очищення полів
# =========================

def clear_fields():
    global select_user_id

    select_user_id = None

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_location.delete(0, tk.END)
    entry_birth_city.delete(0, tk.END)
    entry_telegram.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

    tree.selection_remove(tree.selection())


# =========================
# Запуск бази
# =========================

initdb()


# =========================
# Головне вікно
# =========================

root = tk.Tk()
root.title("База даних")
root.geometry("1000x600")
root.resizable(False, False)


# =========================
# Поля введення
# =========================

frame_inputs = ttk.LabelFrame(
    root,
    text="Дані користувача",
    padding=(10, 10)
)

frame_inputs.pack(
    fill="x",
    padx=15,
    pady=10
)


ttk.Label(
    frame_inputs,
    text="Ім'я:"
).grid(
    row=0,
    column=0,
    pady=5,
    padx=5
)

entry_name = ttk.Entry(
    frame_inputs,
    width=35
)

entry_name.grid(
    row=0,
    column=1,
    pady=5
)


ttk.Label(
    frame_inputs,
    text="Вік:"
).grid(
    row=1,
    column=0,
    pady=5,
    padx=5
)

entry_age = ttk.Entry(
    frame_inputs,
    width=35
)

entry_age.grid(
    row=1,
    column=1,
    pady=5
)


ttk.Label(
    frame_inputs,
    text="Місце проживання:"
).grid(
    row=2,
    column=0,
    pady=5,
    padx=5
)

entry_location = ttk.Entry(
    frame_inputs,
    width=35
)

entry_location.grid(
    row=2,
    column=1,
    pady=5
)


ttk.Label(
    frame_inputs,
    text="Місто народження:"
).grid(
    row=3,
    column=0,
    pady=5,
    padx=5
)

entry_birth_city = ttk.Entry(
    frame_inputs,
    width=35
)

entry_birth_city.grid(
    row=3,
    column=1,
    pady=5
)


ttk.Label(
    frame_inputs,
    text="Telegram користувача:"
).grid(
    row=4,
    column=0,
    pady=5,
    padx=5
)

entry_telegram = ttk.Entry(
    frame_inputs,
    width=35
)

entry_telegram.grid(
    row=4,
    column=1,
    pady=5
)


ttk.Label(
    frame_inputs,
    text="Номер телефону:"
).grid(
    row=5,
    column=0,
    pady=5,
    padx=5
)

entry_phone = ttk.Entry(
    frame_inputs,
    width=35
)

entry_phone.grid(
    row=5,
    column=1,
    pady=5
)


# =========================
# Кнопки
# =========================

frame_buttons = ttk.Frame(
    root,
    padding=(10, 5)
)

frame_buttons.pack(
    fill="x",
    padx=15
)


btn_add = ttk.Button(
    frame_buttons,
    text="Додати",
    command=add_user
)

btn_add.grid(
    row=0,
    column=0,
    padx=10
)


btn_update = ttk.Button(
    frame_buttons,
    text="Оновити",
    command=update_user
)

btn_update.grid(
    row=0,
    column=1,
    padx=10
)


btn_delete = ttk.Button(
    frame_buttons,
    text="Видалити",
    command=Delete
)

btn_delete.grid(
    row=0,
    column=2,
    padx=10
)


btn_clear = ttk.Button(
    frame_buttons,
    text="Очистити",
    command=clear_fields
)

btn_clear.grid(
    row=0,
    column=3,
    padx=10
)


# =========================
# Таблиця
# =========================

frame_table = ttk.Frame(
    root,
    padding=(10, 10)
)

frame_table.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


columns = (
    "Id",
    "Name",
    "Age",
    "Location",
    "BirthCity",
    "Telegram",
    "Phone"
)


tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings",
    height=10
)


tree.heading("Id", text="Id")
tree.heading("Name", text="Ім'я")
tree.heading("Age", text="Вік")
tree.heading("Location", text="Місце проживання")
tree.heading("BirthCity", text="Місто народження")
tree.heading("Telegram", text="Telegram")
tree.heading("Phone", text="Номер телефону")


tree.column("Id", width=40)
tree.column("Name", width=120)
tree.column("Age", width=50)
tree.column("Location", width=160)
tree.column("BirthCity", width=160)
tree.column("Telegram", width=150)
tree.column("Phone", width=140)


scroll_bar_y = ttk.Scrollbar(
    frame_table,
    orient="vertical",
    command=tree.yview
)

scroll_bar_x = ttk.Scrollbar(
    frame_table,
    orient="horizontal",
    command=tree.xview
)


tree.configure(
    yscrollcommand=scroll_bar_y.set,
    xscrollcommand=scroll_bar_x.set
)


tree.pack(
    side="top",
    fill="both",
    expand=True
)

scroll_bar_y.pack(
    side="right",
    fill="y"
)

scroll_bar_x.pack(
    side="bottom",
    fill="x"
)


# Вибір користувача з таблиці
tree.bind(
    "<<TreeviewSelect>>",
    on_select_user
)


# Завантаження існуючих даних
load_users()


# Запуск програми
root.mainloop()
