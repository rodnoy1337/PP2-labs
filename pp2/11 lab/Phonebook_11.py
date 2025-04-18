import psycopg2
import sys
import json

def create_connection():
    """Создает соединение с базой данных"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="phonebook_db",
            user="postgres",
            password="123456"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        sys.exit(1)

def create_table(conn):
    """Создает таблицу phonebook, если она не существует"""
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook(
                id SERIAL PRIMARY KEY,
                name VARCHAR(600),
                phone VARCHAR(20)
            )            
        """)
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблицы: {e}")

def add_contact_manual(conn):
    """Добавляет контакт вручную через ввод пользователя"""
    try:
        name = input("Введите имя: ")
        phone_n = input("Введите номер телефона: ")
        
        cur = conn.cursor()
        cur.execute("INSERT INTO phonebook(name, phone) VALUES(%s, %s)", (name, phone_n))
        conn.commit()
        cur.close()
        
        print("Контакт успешно добавлен!")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении контакта: {e}")

def add_contacts_from_file(conn):
    """Добавляет контакты из CSV файла"""
    try:
        file_path = input("Введите путь к CSV файлу (формат: имя,телефон): ")
        
        cur = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                try:
                    name, phone_n = line.strip().split(",")
                    cur.execute("INSERT INTO phonebook(name, phone) VALUES(%s, %s)", (name, phone_n))
                except ValueError:
                    print(f"Пропущена строка с неверным форматом: {line.strip()}")
        
        conn.commit()
        cur.close()
        print("Контакты из файла успешно добавлены!")
    except FileNotFoundError:
        print("Файл не найден!")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении контактов из файла: {e}")

def update_contact(conn):
    """Обновляет контакт в телефонной книге"""
    try:
        choice = input("Что вы хотите обновить? 'name' (имя) или 'phone' (телефон): ").lower()
        
        cur = conn.cursor()
        
        if choice == "name":
            cur_name = input("Введите текущее имя: ")
            new_name = input("Введите новое имя: ")
            cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, cur_name))
        elif choice == "phone":
            cur_phone = input("Введите текущий номер телефона: ")
            new_phone = input("Введите новый номер телефона: ")
            cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, cur_phone))
        else:
            print("Неверный выбор. Попробуйте снова.")
            return
        
        conn.commit()
        print("Контакт успешно обновлен!")
        
        # Показываем обновленные данные
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        print("\nТекущие контакты:")
        for row in rows:
            print(row)
        
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении контакта: {e}")

def search_contacts(conn):
    """Поиск контактов по различным критериям"""
    try:
        print("\nВарианты поиска:")
        print("1 - поиск по точному имени")
        print("2 - поиск по началу имени")
        print("3 - поиск по точному номеру телефона")
        print("4 - поиск по началу номера телефона")
        print("5 - показать все контакты")
        
        choice = input("Выберите вариант поиска (1-5): ")
        
        cur = conn.cursor()
        
        if choice == "1":
            name = input("Введите имя: ")
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
        elif choice == "2":
            name_st = input("Введите начало имени: ")
            cur.execute("SELECT * FROM phonebook WHERE name LIKE %s", (name_st + '%',))
        elif choice == "3":
            phone_n = input("Введите номер телефона: ")
            cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone_n,))
        elif choice == "4":
            phone_st = input("Введите начало номера телефона: ")
            cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (phone_st + '%',))
        elif choice == "5":
            cur.execute("SELECT * FROM phonebook")
        else:
            print("Неверный выбор. Попробуйте снова.")
            return
        
        rows = cur.fetchall()
        
        if not rows:
            print("Контакты не найдены.")
        else:
            print("\nРезультаты поиска:")
            for row in rows:
                print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
        
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при поиске контактов: {e}")

def delete_contact(conn):
    """Удаляет контакт из телефонной книги"""
    try:
        choice = input("По какому критерию удалить контакт? 'name' (имя) или 'phone' (телефон): ").lower()
        
        cur = conn.cursor()
        
        if choice == "name":
            name = input("Введите имя для удаления: ")
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        elif choice == "phone":
            phone = input("Введите номер телефона для удаления: ")
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        else:
            print("Неверный выбор. Попробуйте снова.")
            return
        
        conn.commit()
        print("Контакт успешно удален!")
        
        # Показываем оставшиеся контакты
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        print("\nТекущие контакты:")
        for row in rows:
            print(row)
        
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка при удалении контакта: {e}")
    
def new_validate_phone(phone: str) -> bool:
    """Проверяет, что телефон содержит только цифры (10-15 символов)"""
    return phone.isdigit() and 10 <= len(phone) <= 15

def new_upsert_contact(conn):
    """Добавляет или обновляет контакт (с проверкой телефона)"""
    try:
        name = input("Введите имя: ")
        phone = input("Введите телефон (10-15 цифр): ")
        
        if not new_validate_phone(phone):
            print("Ошибка: неверный формат телефона")
            return
            
        cur = conn.cursor()
        # Используем ON CONFLICT для upsert
        cur.execute("""
            INSERT INTO phonebook (name, phone) 
            VALUES (%s, %s)
            ON CONFLICT (phone) 
            DO UPDATE SET name = EXCLUDED.name
        """, (name, phone))
        
        conn.commit()
        print("Успешно: контакт добавлен/обновлен")
    except psycopg2.Error as e:
        print(f"Ошибка базы данных: {e}")

def new_paginated_search(conn):
    """Поиск с пагинацией"""
    try:
        page = int(input("Номер страницы: "))
        limit = 5
        offset = (page - 1) * limit
        
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM phonebook 
            ORDER BY name
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        rows = cur.fetchall()
        print(f"\nСтраница {page}:")
        for row in rows:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
            
    except ValueError:
        print("Ошибка: введите число")
    except psycopg2.Error as e:
        print(f"Ошибка базы данных: {e}")

def new_add_from_json(conn):
    """Добавляет контакты из JSON-файла"""
    try:
        file_path = input("Введите путь к JSON-файлу: ")
        
        with open(file_path, 'r') as f:
            contacts = json.load(f)
            
            valid = 0
            invalid = 0
            
            cur = conn.cursor()
            for contact in contacts:
                if not new_validate_phone(contact['phone']):
                    print(f"Пропущен: {contact['name']} - неверный телефон")
                    invalid += 1
                    continue
                    
                cur.execute("""
                    INSERT INTO phonebook (name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                """, (contact['name'], contact['phone']))
                valid += 1
                
            conn.commit()
            print(f"Добавлено: {valid}, Пропущено: {invalid}")
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка файла: {e}")
    except psycopg2.Error as e:
        print(f"Ошибка базы данных: {e}")

def new_export_to_csv(conn):
    """Экспортирует все контакты в CSV"""
    try:
        file_path = input("Введите путь для сохранения (например: contacts.csv): ")
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        
        with open(file_path, 'w') as f:
            f.write("ID,Name,Phone\n")
            for row in rows:
                f.write(f"{row[0]},{row[1]},{row[2]}\n")
                
        print(f"Экспортировано {len(rows)} контактов в {file_path}")
    except Exception as e:
        print(f"Ошибка: {e}")

def new_advanced_menu(conn):
    while True:
        print("\nДополнительные функции:")
        print("1. Умное добавление (с проверкой)")
        print("2. Поиск с пагинацией")
        print("3. Импорт из JSON")
        print("4. Экспорт в CSV")
        print("5. Вернуться в главное меню")
        
        choice = input("Выберите действие (1-5): ")
        
        if choice == "1":
            new_upsert_contact(conn)
        elif choice == "2":
            new_paginated_search(conn)
        elif choice == "3":
            new_add_from_json(conn)
        elif choice == "4":
            new_export_to_csv(conn)
        elif choice == "5":
            break
        else:
            print("Неверный выбор")


def show_menu():
    print("\nТелефонный справочник - Главное меню")
    print("1. Добавить контакт вручную")  
    print("2. Добавить контакты из файла (CSV)")  
    print("3. Обновить контакт")  
    print("4. Поиск контактов")  
    print("5. Удалить контакт")  
    print("6. Дополнительные функции ")  
    print("7. Выход")  
    return input("Выберите действие (1-7): ")



def main():
    """Основная функция программы"""
    conn = create_connection()
    create_table(conn)
    
    while True:
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
            new_advanced_menu(conn)  
        elif choice == "7":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 7.")
    
    conn.close()



if __name__ == "__main__":
    main()