from Export_Import import Export_Import
from Instrument import Instrument

class MusicStore:
    def __init__(self):
        self.instruments = [
            Instrument("Гитара", 30000.0, 10, "Красный", "Струнные"),
            Instrument("Барабаны", 40000.0, 5, "Черный", "Ударные"),
            Instrument("Пианино", 30000.0, 3, "Белый", "Клавишные"),
            Instrument("Скрипка", 35000.0, 7, "Коричневый", "Струнные"),
            Instrument("Саксофон", 25000.0, 4, "Золотой", "Духовые"),
        ]
        self.users = []

    def login(self, username: str, password: str):
        for user in self.users:
            if user.username == username and user.password == password:
                print(f"Вход выполнен. Добро пожаловать, {username}!")
                return user
        print("Неверное имя пользователя или пароль.")
        return None


    def add_instrument(self, instrument):
        self.instruments.append(instrument)
        print("Инструмент успешно добавлен")

    def remove_instrument(self, name: str):
        self.instruments = [instrument for instrument in self.instruments if instrument.name != name]
        print("Инструмент успешно удален")

    def add_user(self, user):
        self.users.append(user)
       

    def view_instruments(self):
        if not self.instruments:
            print("Инструменты отсутствуют.")
        else:
            print("Список инструментов:")
            for instrument in self.instruments:
                print(instrument)

    def view_users(self):
        if not self.users:
            print("Пользователи отсутствуют.")
        else:
            print("Список пользователей:")
            for user in self.users:
                print(f"{user.username} - {user.role}")

    def buy_instrument(self, name: str, customer):
        for instrument in self.instruments:
            if instrument.name == name:
                if instrument.stock > 0:
                    instrument.stock -= 1
                    customer.purchase_history.append(f"{instrument.name} - {instrument.price} руб.")
                    return
                else:
                    print("Инструмент отсутствует на складе")
                    return
        print("Инструмент не найден")

    def search_instruments(self, query: str):
        query = query.lower()
        return [instrument for instrument in self.instruments if query in instrument.name.lower()]

    def filter_instruments(self, category=None, color=None, price_range=None):
        filtered_instruments = self.instruments

        if category:
            filtered_instruments = list(filter(lambda x: category.lower() in x.category.lower(), filtered_instruments))
        if color:
            filtered_instruments = list(filter(lambda x: color.lower() in x.color.lower(), filtered_instruments))
        if price_range:
            min_price, max_price = price_range
            filtered_instruments = list(filter(lambda x: min_price <= x.price <= max_price, filtered_instruments))

        return filtered_instruments

    def sort_instruments(self, reverse=False):
        return sorted(self.instruments, key=lambda x: x.price, reverse=reverse)


    def export_instruments(self, filename: str = "inst.json"):
        Export_Import.export_data(self.instruments, filename)

    def export_users(self, filename: str = "users.json"):
        Export_Import.export_data(self.users, filename)

    def import_instruments(self, filename: str = "inst.json"):
        imported_data = Export_Import.import_data(filename, "inst")
        if imported_data:
            self.instruments = imported_data
            return imported_data
        return []

    def import_users(self, filename: str = "users.json"):
        imported_data = Export_Import.import_data(filename, "user")
        if imported_data:
            self.users = imported_data
            return imported_data
        return []
    