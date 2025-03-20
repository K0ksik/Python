from User import User

class Customer(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, role="cust")
        self.purchase_history = []

    def __json__(self):
        data = super().__json__()
        data["purchase_history"] = self.purchase_history
        return data

    @classmethod
    def from_dict(cls, data: dict):
        customer = cls(username=data["username"], password=data["password"])
        customer.purchase_history = data.get("purchase_history", [])
        return customer

    def menu(self, store):
        while True:
            action = input(
                "\nВыберите действие:\n"
                "1. Просмотреть инструменты\n"
                "2. Купить инструмент\n"
                "3. Поиск инструмента\n"
                "4. Просмотреть историю покупок\n"
                "5. Фильтровать инструменты\n"
                "6. Сортировать инструменты\n"
                "0. Выйти\n"
            )
            if action == '1':
                self.view_instruments(store)
            elif action == '2':
                self.buy_instrument(store)
            elif action == '3':
                self.search_instrument(store)
            elif action == '4':
                self.view_purchase_history()
            elif action == '5':
                self.filter_instruments_menu(store)
            elif action == '6':
                self.sort_instruments_menu(store)
            elif action == '0':
                break
            else:
                print("Некорректный ввод")

    def view_instruments(self, store):
        store.view_instruments()

    def buy_instrument(self, store):
        name = input("Введите название инструмента для покупки: ")
        store.buy_instrument(name, self)

    def search_instrument(self, store):
        search_name = input("Введите название инструмента для поиска: ")
        found_instruments = store.search_instruments(search_name)
        if found_instruments:
            print("Найденные инструменты:")
            for instrument in found_instruments:
                print(instrument)
        else:
            print("Инструменты не найдены")

    def view_purchase_history(self):
        if not self.purchase_history:
            print("История покупок пуста")
        else:   
            print("История покупок:")
            for purchase in self.purchase_history:
                print(purchase)

    def filter_instruments_menu(self, store):
        category = input("Введите категорию (оставьте пустым, чтобы пропустить): ")
        color = input("Введите цвет (оставьте пустым, чтобы пропустить): ")
        price_range = input("Введите диапазон цен (например, 1000-5000, оставьте пустым, чтобы пропустить): ")

        price_range_tuple = None
        if price_range:
            try:
                min_price, max_price = map(float, price_range.split("-"))
                price_range_tuple = (min_price, max_price)
            except ValueError:
                print("Некорректный формат диапазона цен")
                return
        filtered_instruments = store.filter_instruments(
            category=category if category else None,
            color=color if color else None,
            price_range=price_range_tuple if price_range else None
        )
        if filtered_instruments:
            print("\nОтфильтрованные инструменты:")
            for instrument in filtered_instruments:
                print(instrument)
        else:
            print("Инструменты не найдены")

    def sort_instruments_menu(self, store):
        print("\nСортировка инструментов:")
        order = input("Сортировать по возрастанию (1) или убыванию (2)? ")
        if order == '1':
            sorted_instruments = store.sort_instruments(reverse=False)
        elif order == '2':
            sorted_instruments = store.sort_instruments(reverse=True)
        else:
            print("Некорректный ввод")
            return   
        if sorted_instruments:
            print("\nОтсортированные инструменты:")
            for instrument in sorted_instruments:
                print(instrument)
        else:
            print("Инструменты не найдены")