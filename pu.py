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

# Создаем экземпляры производных классов
data_class1 = DerivedDataClass1("Data 1")
data_class2 = DerivedDataClass2("Data 2")

caller_class = CallerClass()

# Добавляем экземпляры производных классов в CallerClass
caller_class.add_data_class(data_class1)
caller_class.add_data_class(data_class2)

# Вызываем метод caller_class, который вызывает метод get_data у всех производных классов
caller_class.call_data_classes()