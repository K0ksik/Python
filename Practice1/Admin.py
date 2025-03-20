from User import User
from Instrument import Instrument
from Export_Import import Export_Import

class Admin(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, role="adm")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            username=data["username"],
            password=data["password"],
        )

    def menu(self, store):
        while True:
            action = input(
                "\nВыберите действие:\n"
                "1. Добавить инструмент\n"
                "2. Удалить инструмент\n"
                "3. Просмотреть инструменты\n"
                "4. Просмотреть пользователей\n"
                "5. Экспорт данных\n"
                "6. Импорт данных\n"
                "0. Выйти\n"
            )
            if action == '1':
                self.add_instrument(store)
            elif action == '2':
                self.remove_instrument(store)
            elif action == '3':
                self.view_instruments(store)
            elif action == '4':
                self.view_users(store)
            elif action == '5':
                self.export_data(store)
            elif action == '6':
                self.import_data(store)
            elif action == '0':
                break
            else:
                print("Некорректный ввод.")

    def add_instrument(self, store):
        name = input("Название инструмента: ")
        price = float(input("Цена: "))
        stock = int(input("Количество: "))
        color = input("Цвет инструмента: ")
        category = input("Категория инструмента: ")
        instrument = Instrument(name, price, stock, color, category)
        store.add_instrument(instrument)

    def remove_instrument(self, store):
        name = input("Название инструмента для удаления: ")
        store.remove_instrument(name)

    def view_instruments(self, store):
        store.view_instruments()

    def view_users(self, store):
        store.view_users()

    def export_data(self, store):
        print("\nЭкспорт данных:")
        data_type = input("Что экспортировать? (inst - инструменты, user - пользователей): ").lower()
        if data_type == "inst":
            store.export_instruments()  
        elif data_type == "user":
            store.export_users()  
        else:  
            print("Некорректный тип данных")

    def import_data(self, store):
        print("\nИмпорт данных:")
        data_type = input("Что импортировать? (inst - инструменты, user - пользователей): ").lower()
        if data_type == "inst":
            imported_data = store.import_instruments()  
            if imported_data:
                print("\nИмпортированные инструменты:")
                for instrument in imported_data:
                    print(instrument)
        elif data_type == "user":
            imported_data = store.import_users()  
            if imported_data:
                print("\nИмпортированные пользователи:")
                for user_data in imported_data:
                    print(f"{user_data.username} - {user_data.role}")
        else:
            print("Некорректный тип данных")