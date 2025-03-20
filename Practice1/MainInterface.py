from MusicStore import MusicStore
from Admin import Admin
from Customer import Customer

def main():
    store = MusicStore()

    while True:
        print("\nДобро пожаловать в музыкальный магазин!")
        action = input( 
            "Выберите действие:\n"
            "1. Вход\n"
            "2. Регистрация\n"
            "0. Выход\n"
        )
        if action == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            user = store.login(username, password)
            if user:
                user.menu(store)
        elif action == '2':
            role = input("Введите роль (adm - админ, cust - покупатель): ").lower()
            username = input("Введите имя пользователя: ")  
            password = input("Введите пароль: ")
            if role == "adm":
                user = Admin(username, password)
            elif role == "cust":
                user = Customer(username, password)
            else:
                print("Недопустимое значение")
                continue
            store.add_user(user)
        elif action == '0':
            print("Выход")
            break
        else:
            print("Некорректный ввод")

if __name__ == "__main__":
    main()