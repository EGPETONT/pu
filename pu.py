import argparse
from tabulate import tabulate


class DataClass:
    def get_data(self):
        raise NotImplementedError("Subclass must implement this method")

class DerivedDataClass1(DataClass):
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return f"Data from DerivedDataClass1: {self.data}"

class DerivedDataClass2(DataClass):
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return f"Data from DerivedDataClass2: {self.data}"

class CallerClass:
    def __init__(self):
        self.data_classes = []

    def add_data_class(self, data_class):
        if isinstance(data_class, DataClass):
            self.data_classes.append(data_class)
        else:
            raise ValueError("Object must be an instance of DataClass or its subclasses")

    def call_data_classes(self):
        for data_class in self.data_classes:
            print(data_class.get_data())

class TablePrinter:
    def __init__(self, caller_class):
        self.caller_class = caller_class

    def print_table(self):
        table_data = []
        for data_class in self.caller_class.data_classes:
            table_data.append([type(data_class).__name__, data_class.get_data()])

        print(tabulate(table_data, headers=["Class Name", "Data"], tablefmt="grid"))

    def __call__(self):
        self.print_table()

# Функция для обработки аргументов командной строки
def parse_args():
    parser = argparse.ArgumentParser(description="Print data from DataClass instances.")
    # Добавьте здесь аргументы, если нужно
    return parser.parse_args()

# Главная функция, которая будет вызвана при запуске скрипта
def main():
    # Обработка аргументов командной строки
    args = parse_args()

    # Создаем экземпляры производных классов
    data_class1 = DerivedDataClass1("Data 1")
    data_class2 = DerivedDataClass2("Data 2")

    caller_class = CallerClass()

    # Добавляем экземпляры производных классов в CallerClass
    caller_class.add_data_class(data_class1)
    caller_class.add_data_class(data_class2)

    # Создаем экземпляр TablePrinter и выводим таблицу
    table_printer = TablePrinter(caller_class)
    table_printer()  # Вызываем экземпляр как функцию

# Проверяем, запущен ли скрипт напрямую, а не импортирован
if __name__ == "__main__":
    main()

# # Создаем экземпляры производных классов
# data_class1 = DerivedDataClass1("Data 1")
# data_class2 = DerivedDataClass2("Data 2")

# caller_class = CallerClass()

# # Добавляем экземпляры производных классов в CallerClass
# caller_class.add_data_class(data_class1)
# caller_class.add_data_class(data_class2)

# # Вызываем метод caller_class, который вызывает метод get_data у всех производных классов
# caller_class.call_data_classes()