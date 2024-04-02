import argparse
from tabulate import tabulate
import socket


class DataClass:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        raise NotImplementedError("Subclass must implement this method")

class DerivedDataClass1(DataClass):
    def __init__(self, name):
        super().__init__(name)
        self.data_list = self.get_data()

    def get_data(self):
        return self.get_ports_info()

    def get_ports_info(self):
        open_ports = []
        for port in range(1, 65536):  # диапазон портов от 1 до 65535
            try:
                # Создаем сокет TCP
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # Устанавливаем тайм-аут на небольшое время, чтобы не ждать бесконечно
                    s.settimeout(0.1)
                    # Пытаемся подключиться к порту
                    result = s.connect_ex(('localhost', port))
                    if result == 0:
                        open_ports.append(port)
            except socket.error:
                continue
        return open_ports
        
class DerivedDataClass2(DataClass):
    def __init__(self, name):
        super().__init__(name)
        self.data_list = self.get_data()

    def get_data(self):
        # Предполагаем, что этот метод возвращает список данных
        return [6, 7, 8, 9, 10]

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
            yield data_class.get_data()

class TablePrinter:
    def __init__(self, caller_class):
        self.caller_class = caller_class

    def print_table(self):
        table_data = []
        headers = []
        for data_class in self.caller_class.data_classes:
            headers.append(data_class.name)
            table_data.append(data_class.get_data())

        # Транспонирование таблицы для правильного отображения столбцов
        table_data = list(map(list, zip(*table_data)))

        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def __call__(self):
        self.print_table()

def parse_args():
    parser = argparse.ArgumentParser(description="Print data from DataClass instances.")
    # Добавьте здесь аргументы, если нужно
    return parser.parse_args()

def main():
    args = parse_args()

    # Создаем экземпляры производных классов с указанием имени
    data_class1 = DerivedDataClass1(name="Class1")
    data_class2 = DerivedDataClass2(name="Class2")

    caller_class = CallerClass()

    # Добавляем экземпляры производных классов в CallerClass
    caller_class.add_data_class(data_class1)
    caller_class.add_data_class(data_class2)

    # Создаем экземпляр TablePrinter и выводим таблицу
    table_printer = TablePrinter(caller_class)
    table_printer()

if __name__ == "__main__":
    main()