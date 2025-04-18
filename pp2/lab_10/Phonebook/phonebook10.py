import psycopg2
import sys

def create_connection():
    """Создает соединение с базой данных"""
    try:
        # Подключение к базе данных PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            dbname="phonebook_db",
            user="postgres",
            password="123456"
        )
        return conn
    except psycopg2.Error as e:
        # Обработка ошибки подключения
        print(f"Ошибка подключения к базе данных: {e}")
        sys.exit(1)

def create_table(conn):
    """Создает таблицу phonebook, если она не существует"""
    try:
        cur = conn.cursor()
        # SQL-запрос для создания таблицы
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook(
                id SERIAL PRIMARY KEY,  # Уникальный идентификатор
                name VARCHAR(600),      # Имя контакта
                phone VARCHAR(20)       # Номер телефона
            )            
        """)
        conn.commit()  # Сохранение изменений
        cur.close()  # Закрытие курсора
    except psycopg2.Error as e:
        # Обработка ошибки при создании таблицы
        print(f"Ошибка при создании таблицы: {e}")

def add_contact_manual(conn):
    """Добавляет контакт вручную через ввод пользователя"""
    try:
        # Запрос имени и номера телефона у пользователя
        name = input("Введите имя: ")
        phone_n = input("Введите номер телефона: ")
        
        cur = conn.cursor()
        # SQL-запрос для добавления контакта
        cur.execute("INSERT INTO phonebook(name, phone) VALUES(%s, %s)", (name, phone_n))
        conn.commit()  # Сохранение изменений
        cur.close()  # Закрытие курсора
        
        print("Контакт успешно добавлен!")
    except psycopg2.Error as e:
        # Обработка ошибки при добавлении контакта
        print(f"Ошибка при добавлении контакта: {e}")

def add_contacts_from_file(conn):
    """Добавляет контакты из CSV файла"""
    try:
        # Запрос пути к CSV-файлу
        file_path = input("Введите путь к CSV файлу (формат: имя,телефон): ")
        
        cur = conn.cursor()
        # Открытие файла и чтение строк
        with open(file_path, "r") as file:
            for line in file:
                try:
                    # Разделение строки на имя и номер телефона
                    name, phone_n = line.strip().split(",")
                    cur.execute("INSERT INTO phonebook(name, phone) VALUES(%s, %s)", (name, phone_n))
                except ValueError:
                    # Обработка строки с неверным форматом
                    print(f"Пропущена строка с неверным форматом: {line.strip()}")
        
        conn.commit()  # Сохранение изменений
        cur.close()  # Закрытие курсора
        print("Контакты из файла успешно добавлены!")
    except FileNotFoundError:
        # Обработка ошибки, если файл не найден
        print("Файл не найден!")
    except psycopg2.Error as e:
        # Обработка ошибки при добавлении контактов
        print(f"Ошибка при добавлении контактов из файла: {e}")

def update_contact(conn):
    """Обновляет контакт в телефонной книге"""
    try:
        # Запрос действия от пользователя
        choice = input("Что вы хотите обновить? 'name' (имя) или 'phone' (телефон): ").lower()
        
        cur = conn.cursor()
        
        if choice == "name":
            # Обновление имени контакта
            cur_name = input("Введите текущее имя: ")
            new_name = input("Введите новое имя: ")
            cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, cur_name))
        elif choice == "phone":
            # Обновление номера телефона
            cur_phone = input("Введите текущий номер телефона: ")
            new_phone = input("Введите новый номер телефона: ")
            cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, cur_phone))
        else:
            # Обработка неверного выбора
            print("Неверный выбор. Попробуйте снова.")
            return
        
        conn.commit()  # Сохранение изменений
        print("Контакт успешно обновлен!")
        
        # Вывод обновленных данных
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        print("\nТекущие контакты:")
        for row in rows:
            print(row)
        
        cur.close()  # Закрытие курсора
    except psycopg2.Error as e:
        # Обработка ошибки при обновлении контакта
        print(f"Ошибка при обновлении контакта: {e}")

def search_contacts(conn):
    """Поиск контактов по различным критериям"""
    try:
        # Вывод вариантов поиска
        print("\nВарианты поиска:")
        print("1 - поиск по точному имени")
        print("2 - поиск по началу имени")
        print("3 - поиск по точному номеру телефона")
        print("4 - поиск по началу номера телефона")
        print("5 - показать все контакты")
        
        choice = input("Выберите вариант поиска (1-5): ")
        
        cur = conn.cursor()
        
        if choice == "1":
            # Поиск по точному имени
            name = input("Введите имя: ")
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
        elif choice == "2":
            # Поиск по началу имени
            name_st = input("Введите начало имени: ")
            cur.execute("SELECT * FROM phonebook WHERE name LIKE %s", (name_st + '%',))
        elif choice == "3":
            # Поиск по точному номеру телефона
            phone_n = input("Введите номер телефона: ")
            cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone_n,))
        elif choice == "4":
            # Поиск по началу номера телефона
            phone_st = input("Введите начало номера телефона: ")
            cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (phone_st + '%',))
        elif choice == "5":
            # Показать все контакты
            cur.execute("SELECT * FROM phonebook")
        else:
            # Обработка неверного выбора
            print("Неверный выбор. Попробуйте снова.")
            return
        
        rows = cur.fetchall()
        
        if not rows:
            # Если контакты не найдены
            print("Контакты не найдены.")
        else:
            # Вывод найденных контактов
            print("\nРезультаты поиска:")
            for row in rows:
                print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
        
        cur.close()  # Закрытие курсора
    except psycopg2.Error as e:
        # Обработка ошибки при поиске контактов
        print(f"Ошибка при поиске контактов: {e}")

def delete_contact(conn):
    """Удаляет контакт из телефонной книги"""
    try:
        # Запрос критерия удаления
        choice = input("По какому критерию удалить контакт? 'name' (имя) или 'phone' (телефон): ").lower()
        
        cur = conn.cursor()
        
        if choice == "name":
            # Удаление по имени
            name = input("Введите имя для удаления: ")
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        elif choice == "phone":
            # Удаление по номеру телефона
            phone = input("Введите номер телефона для удаления: ")
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        else:
            # Обработка неверного выбора
            print("Неверный выбор. Попробуйте снова.")
            return
        
        conn.commit()  # Сохранение изменений
        print("Контакт успешно удален!")
        
        # Вывод оставшихся контактов
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        print("\nТекущие контакты:")
        for row in rows:
            print(row)
        
        cur.close()  # Закрытие курсора
    except psycopg2.Error as e:
        # Обработка ошибки при удалении контакта
        print(f"Ошибка при удалении контакта: {e}")

def show_menu():
    """Отображает главное меню"""
    print("\nТелефонный справочник - Главное меню")
    print("1. Добавить контакт вручную")
    print("2. Добавить контакты из файла")
    print("3. Обновить контакт")
    print("4. Поиск контактов")
    print("5. Удалить контакт")
    print("6. Выход")
    return input("Выберите действие (1-6): ")

def main():
    """Основная функция программы"""
    # Создаем соединение с базой данных
    conn = create_connection()
    
    # Создаем таблицу, если она не существует
    create_table(conn)
    
    while True:
        # Отображение меню и выполнение выбранного действия
        choice = show_menu()
        
        if choice == "1":
            add_contact_manual(conn)
        elif choice == "2":
            add_contacts_from_file(conn)
        elif choice == "3":
            update_contact(conn)
        elif choice == "4":
            search_contacts(conn)
        elif choice == "5":
            delete_contact(conn)
        elif choice == "6":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")
    
    # Закрываем соединение с базой данных
    conn.close()

if __name__ == "__main__":
    main()