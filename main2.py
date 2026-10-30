
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")
conn.commit()


# Добавление пользователя
def add_user():
    name = input("Имя: ").strip()

    try:
        age = int(input("Возраст: "))
    except ValueError:
        print("Возраст должен быть числом!")
        return

    email = input("Email: ").strip()

    if not name or not email or age < 0:
        print("Некорректные данные!")
        return

    try:
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            (name, age, email)
        )
        conn.commit()
        print("Пользователь добавлен!")
    except sqlite3.IntegrityError:
        print("Такой email уже существует!")


# Просмотр пользователей
def show_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if not users:
        print("База данных пуста!")
        return

    for user in users:
        print(
            f"ID: {user[0]} | "
            f"Имя: {user[1]} | "
            f"Возраст: {user[2]} | "
            f"Email: {user[3]}"
        )


# Поиск пользователя
def search_user():
    name = input("Введите имя: ")

    cursor.execute(
        "SELECT * FROM users WHERE name LIKE ?",
        (f"%{name}%",)
    )

    users = cursor.fetchall()

    if users:
        for user in users:
            print(user)
    else:
        print("Пользователь не найден!")


# Изменение пользователя
def update_user():
    try:
        user_id = int(input("ID пользователя: "))
        new_name = input("Новое имя: ").strip()

        if not new_name:
            print("Имя не может быть пустым!")
            return

        cursor.execute(
            "UPDATE users SET name = ? WHERE id = ?",
            (new_name, user_id)
        )
        conn.commit()

        if cursor.rowcount:
            print("Данные обновлены!")
        else:
            print("Пользователь не найден!")
    except ValueError:
        print("ID должен быть числом!")


# Удаление пользователя
def delete_user():
    try:
        user_id = int(input("ID пользователя: "))

        cursor.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        conn.commit()

        if cursor.rowcount:
            print("Пользователь удалён!")
        else:
            print("Пользователь не найден!")
    except ValueError:
        print("ID должен быть числом!")


# Главное меню
def main():
    while True:
        print("\n===== SQLITE DATABASE =====")
        print("1. Добавить пользователя")
        print("2. Показать пользователей")
        print("3. Найти пользователя")
        print("4. Изменить пользователя")
        print("5. Удалить пользователя")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            show_users()
        elif choice == "3":
            search_user()
        elif choice == "4":
            update_user()
        elif choice == "5":
            delete_user()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверная команда!")


try:
    main()
finally:
    conn.close()
