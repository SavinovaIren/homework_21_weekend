from abc import ABC, abstractmethod


class Storage(ABC):

    def __init__(self, items, capacity):
        self.capacity = capacity  # целое число
        self.items = items  # словарь название:количество

    @abstractmethod
    def add(self, title, quantity: int):  # `add`(<название>, <количество>)  - увеличивает запас items
        pass

    @abstractmethod
    def remove(self, title, quantity: int):  # `remove`(<название>, <количество>) - уменьшает запас items
        pass

    @abstractmethod
    def get_free_space(self):  # вернуть количество свободных мест
        pass

    @abstractmethod
    def get_items(self):  # возвращает сожержание склада в словаре {товар: количество}
        pass

    @abstractmethod
    def get_unique_items_count(self):  # возвращает количество уникальных товаров
        pass


class Store(Storage):

    def __init__(self, items: dict, capacity: int = 100):
        self.__items = items
        self.__capacity = capacity

    def __str__(self):
        list = ""
        for k, v in self.__items.items():
            list += f"{k}:{v}\n"
        return list

    def get_free_space(self):  # вернуть количество свободных мест
        current_space = 0
        for value in self.__items.values():
            current_space += value
        return self.__capacity - current_space

    def add(self, title, quantity: int):  # увеличивает запас items с учетом лимита capacity
        if title in self.__items.keys():
            if self.get_free_space() >= int(quantity):
                self.__items[title] += int(quantity)
                return True
            else:
                print("Места на складе недостаточно")
                return False
        else:
            if self.get_free_space() >= int(quantity):
                self.__items[title] = int(quantity)
                return True
            else:
                print("Места на складе недостаточно")
                return False

    def remove(self, title, quantity: int):  # уменьшает запас items но не ниже 0
        if self.__items[title] > int(quantity):
            self.__items[title] -= int(quantity)
            return True
        else:
            print("На складе недостаточно товара")
            return False

    def get_items(self):  # возвращает содержание склада в словаре {товар: количество}
        return f"{self.items}"

    def get_unique_items_count(self):  # возвращает количество уникальных товаров.
        return len(self.__items.keys())


class Shop(Store):

    def __init__(self, items, capacity: int = 20):
        super().__init__(items, capacity)

    def add(self, title, quantity: int):
        if self.get_unique_items_count() >= 5:
            print("Магазин переполнен, уникальных товаров должно быть не более 5")
            return False
        else:
            super().add(title, quantity)
            return True


class Request:

    def __init__(self, request_str):
        """Доставить 3 печеньки из склад в магазин"""
        req_str = request_str.split()
        action = req_str[0]
        self.__count = req_str[1]
        self.__product = req_str[2]
        if action == "Добавить":
            self.__from = req_str[4]
            self.__to = req_str[6]
        elif action == "Забрать":
            self.__from = req_str[4]
            self.__to = None
        elif action == "Привезти":
            self.__to = req_str[4]
            self.__from = None

    def move(self):
        if self.__to and self.__from:
            if eval(self.__to).add(self.__product, self.__count):
                eval(self.__from).remove(self.__product, self.__count)
        elif self.__to:
            eval(self.__to).add(self.__product, self.__count)
        elif self.__from:
            eval(self.__to).remove(self.__product, self.__count)


storage_1 = Store(items={"яблоко": 10, "слива": 20, "банан": 30})
storage_2 = Store(items={"ананас": 15, "слива": 20, "арбуз": 30, "груша": 30})
shop_1 = Shop(items={"арбуз": 2, "ананас": 3, "яблоко": 1, "груша": 1})

print("Привет!")

while True:
    user_input = input("Введите запрос:\n")

    if user_input == "стоп":
        break
    else:
        req = Request(user_input)
        req.move()
print(storage_1)
print(shop_1)
