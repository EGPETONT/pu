import argparse
from tabulate import tabulate

class DataClass:
    def get_data(self):
        raise NotImplementedError("Subclass must implement this method")

class DerivedDataClass1(DataClass):
    def __init__(self, data_list):
        self.data_list = data_list

    def get_data(self):
        return self.data_list

class DerivedDataClass2(DataClass):
    def __init__(self, data_list):
        self.data_list = data_list

    def get_data(self):
        return self.data_list

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
        for data in self.caller_class.call_data_classes():
            table_data.append([type(data).__name__] + data)

        headers = ["Class Name"] + [f"Attribute {i+1}" for i in range(len(data))]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def __call__(self):
        self.print_table()

def parse_args():
    parser = argparse.ArgumentParser(description="Print data from DataClass instances.")
    # Добавьте здесь аргументы, если нужно
    return parser.parse_args()

def main():
    args = parse_args()

    # Создаем экземпляры производных классов с списками атрибутов
    data_class1 = DerivedDataClass1(["Data 1-1", "Data 1-2"])
    data_class2 = DerivedDataClass2(["Data 2-1", "Data 2-2", "Data 2-3", "1", "2", "3", "4"])

    caller_class = CallerClass()

    # Добавляем экземпляры производных классов в CallerClass
    caller_class.add_data_class(data_class1)
    caller_class.add_data_class(data_class2)

    # Создаем экземпляр TablePrinter и выводим таблицу
    table_printer = TablePrinter(caller_class)
    table_printer()

if __name__ == "__main__":
    main()