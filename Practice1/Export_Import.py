import json
from CustomEncoder import CustomEncoder

class Export_Import:
    @staticmethod
    def export_data(data: list, filename: str):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, cls=CustomEncoder, ensure_ascii=False, indent=4)
            print(f"Данные успешно экспортированы в файл {filename}.")
        except Exception as e:
            print(f"Ошибка при экспорте данных: {e}")

    @staticmethod
    def import_data(filename: str, class_type):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if class_type == "inst":
                    from Instrument import Instrument
                    return [Instrument.from_dict(item) for item in data]
                elif class_type == "user":
                    from Admin import Admin
                    from Customer import Customer
                    return [
                        Admin.from_dict(item) if item["role"] == "adm"
                        else Customer.from_dict(item)
                        for item in data
                    ]
                else:
                    print("Некорректный тип данных для импорта.")
                    return []
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return []
        except Exception as e:
            print(f"Ошибка при импорте данных: {e}")
            return []