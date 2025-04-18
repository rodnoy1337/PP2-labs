import psycopg2
import csv

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host = "localhost",
    dbname = "phonebook_db",
    user = "postgres",
    password = "123456"
)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Функция для ввода данных вручную
def inputData():
    name = input("Hello input your name: ")  # Запрос имени пользователя
    number = input("Input your phone number: ")  # Запрос номера телефона
    # Вставка данных в таблицу phone_book
    cur.execute(' INSERT INTO postgres.public.phone_book("PersonName", "PhoneNumber") VALUES( %s, %s); ', (name, number))

# Функция для импорта данных из CSV-файла
def importFromCSV():
    with open("info.csv", 'r') as file:  # Открытие CSV-файла
        reader = csv.reader(file)
        for row in reader:
            personName, phoneNumber = row  # Чтение имени и номера телефона из строки
            # Вставка данных в таблицу phone_book
            cur.execute(' INSERT INTO postgres.public.phone_book("PersonName", "PhoneNumber") VALUES( %s, %s); ', (personName, phoneNumber))

# Функция для обновления номера телефона по имени
def update_contact(personName, phoneNumber):
    # Обновление записи в таблице phone_book
    cur.execute(' UPDATE postgres.public.phone_book SET "PhoneNumber" = %s WHERE "PersonName" = %s ', (phoneNumber, personName))

# Функция для запроса всех данных из таблицы и записи их в файл
def queryData():
    cur.execute(' SELECT * FROM postgres.public.phone_book ')  # Запрос всех данных из таблицы
    data = cur.fetchall()  # Получение всех строк результата
    path = r"queredData.txt"  # Путь к файлу для записи данных

    f = open(path, "w")  # Открытие файла для записи
    for row in data:
        # Запись данных в файл
        f.write("Name: " + str(row[1]) + "\n" + "Number: " + str(row[2]) + "\n")
    f.close()

# Функция для удаления записи по имени
def deleteData():
    print("Which name do ypu want to delete?\n")  # Запрос имени для удаления
    personName = input()
    # Удаление записи из таблицы phone_book
    cur.execute(f''' DELETE FROM postgres.public.phone_book WHERE "PersonName"='{personName}' ''')

# Функция для удаления всех данных из таблицы
def deleteAllData():
    # Удаление всех записей из таблицы phone_book
    cur.execute(' DELETE FROM postgres.public.phone_book ')

# Основной цикл программы
done = False
while not done:
    # Вывод меню действий
    print("What do you want to do?\n\
          1. Input data from console\n\
          2. Upload form csv file\n\
          3. Update existing contact\n\
          4. Query data from the table\n\
          5. Delete data from table by person name\n\
          6. Delete all data from table\n\
          7. Exit")
    x = int(input("Enter number 1-5\n"))  # Запрос выбора действия
    if(x == 1):
        inputData()  # Ввод данных вручную
    elif(x == 2):
        importFromCSV()  # Импорт данных из CSV
    elif(x == 3):
        print("Which number do you want to update? Enter name and new number: ")
        name = input()  # Запрос имени
        newNumber = input()  # Запрос нового номера
        update_contact(name, newNumber)  # Обновление контакта
    elif(x == 4):
        queryData()  # Запрос данных из таблицы
    elif(x == 5):
        deleteData()  # Удаление записи по имени
    elif(x == 6):
        deleteAllData()  # Удаление всех данных
    elif(x == 7):
        done = True  # Завершение программы
    conn.commit()  # Сохранение изменений в базе данных

# Закрытие курсора и соединения с базой данных
cur.close()
conn.close()


