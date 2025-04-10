# from users import Users
# from cipher import Cipher
# from use_threads import UseThreads

# def main():
#     users = Users()
#     cipher = Cipher()
#     use_threads = UseThreads()

#     while True:
#         print("1. Регистрация")
#         print("2. Авторизация")
#         print("3. Выйти")
#         choice = input("Выберите действие: ")

#         if choice == "1":
#             username = input("Введите имя пользователя: ")
#             password = input("Введите пароль: ")
#             users.register_user(username, password)
#         elif choice == "2":
#             username = input("Введите имя пользователя: ")
#             password = input("Введите пароль: ")
#             if users.login_user(username, password):
#                 print("Авторизация успешна!")
#                 use_threads.start_saving_thread(username, users)

#                 while True:
#                     print("1. Добавить заметку")
#                     print("2. Просмотреть заметки")
#                     print("3. Выйти из аккаунта")
#                     user_choice = input("Выберите действие: ")

#                     if user_choice == "1":
#                         print("1. Ввести текст вручную")
#                         print("2. Указать путь к файлу")
#                         encryption_choice = input("Выберите способ ввода текста: ")

#                         text = None  

#                         if encryption_choice == "1":
#                             text = input("Введите текст для заметки: ")
#                         elif encryption_choice == "2":
#                             file_path = input("Введите путь к файлу: ")
#                             try:
#                                 with open(file_path, "r", encoding="utf-8") as file:
#                                     text = file.read()
#                             except FileNotFoundError:
#                                 print("Файл не найден")
#                                 continue
#                         else:
#                             print("Неверный выбор")
#                             continue  

#                         if text is None:
#                             print("Текст не был введен")
#                             continue

#                         shift = int(input("Введите сдвиг для шифра Цезаря: "))
#                         encrypted_text = cipher.encrypt(text, shift)
#                         print("Зашифрованный текст:", encrypted_text)

#                         users.add_note(username, encrypted_text)
#                     elif user_choice == "2":
#                         notes = users.get_notes(username)
#                         print("Ваши заметки:")
#                         for note in notes:
#                             print(note)
#                     elif user_choice == "3":
#                         use_threads.stop_saving_thread()
#                         break
#             else:
#                 print("Неверное имя пользователя или пароль")
#         elif choice == "3":
#             break

# if __name__ == "__main__":
#     main()
# main.py
from users import Users
from cipher import Cipher
from use_threads import UseThreads
import queue

def main():
    users = Users()
    cipher = Cipher()
    use_threads = UseThreads()

    while True:
        print("1. Регистрация")
        print("2. Авторизация")
        print("3. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            users.register_user(username, password)
        elif choice == "2":
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            if users.login_user(username, password):
                print("Авторизация успешна!")
                use_threads.start_saving_thread(username, users)

                while True:
                    print("1. Добавить заметку")
                    print("2. Просмотреть заметки")
                    print("3. Выйти из аккаунта")
                    user_choice = input("Выберите действие: ")

                    if user_choice == "1":
                        print("1. Ввести текст вручную")
                        print("2. Указать путь к файлу")
                        encryption_choice = input("Выберите способ ввода текста: ")

                        text = None

                        if encryption_choice == "1":
                            text = input("Введите текст для заметки: ")
                        elif encryption_choice == "2":
                            file_path = input("Введите путь к файлу: ")
                            try:
                                with open(file_path, "r", encoding="utf-8") as file:
                                    text = file.read()
                            except FileNotFoundError:
                                print("Файл не найден")
                                continue
                        else:
                            print("Неверный выбор")
                            continue

                        if text is None:
                            print("Текст не был введен")
                            continue

                        shift = int(input("Введите сдвиг для шифра Цезаря: "))

                        result_queue = queue.Queue()
                        cipher.encrypt(text, shift, result_queue)
                        encrypted_text = result_queue.get()
                        print("Зашифрованный текст:", encrypted_text)

                        users.add_note(username, encrypted_text)
                    elif user_choice == "2":
                        notes = users.get_notes(username)
                        print("Ваши заметки:")
                        for note in notes:
                            print(note)
                    elif user_choice == "3":
                        use_threads.stop_saving_thread()
                        break
            else:
                print("Неверное имя пользователя или пароль")
        elif choice == "3":
            break

if __name__ == "__main__":
    main()