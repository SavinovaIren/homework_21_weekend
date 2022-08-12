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
        super().__init__(items, capacity)

    def __str__(self):
        list_ = ""
        for k, v in self.items.items():
            list_ += f"{k}:{v}\n"
        return list_

    def get_free_space(self):  # вернуть количество свободных мест
        current_space = 0
        for value in self.items.values():
            current_space += value
        return self.capacity - current_space

    def add(self, title, quantity: int):  # увеличивает запас items с учетом лимита capacity
        if title in self.items.keys():
            if self.get_free_space() >= int(quantity):
                self.items[title] += int(quantity)
                return True
            else:
                print("Места на складе недостаточно")
                return False
        else:
            if self.get_free_space() >= int(quantity):
                self.items[title] = int(quantity)
                return True
            else:
                print("Места на складе недостаточно")
                return False

    def remove(self, title, quantity: int):  # уменьшает запас items но не ниже 0
        if self.items[title] > int(quantity):
            self.items[title] -= int(quantity)
            return True
        else:
            print("На складе недостаточно товара")
            return False

    def get_items(self):  # возвращает содержание склада в словаре {товар: количество}
        return f"{self.items}"

    def get_unique_items_count(self):  # возвращает количество уникальных товаров.
        return len(self.items.keys())


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

    def __init__(self, request_str: str):

        """Доставить 3 яблоко из склад-2 в магазин"""
        self.request_str = request_str
        request_list = self.request_str.split()
        self.__count = int(request_list[1])
        self.__product = request_list[2]
        self.__from = request_list[4]
        self.__to = request_list[6]

    @property
    def from_(self):
        return self.__from

    @from_.setter
    def from_(self, value):
        self.__from = value

    @property
    def to_(self):
        return self.__to

    @to_.setter
    def to_(self, value):
        self.__to = value

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, value):
        self.__product = value

    def __repr__(self):
        return f"Доставить {self.__count} {self.__product} из {self.__from} в {self.__to}"


storage_1 = Store(items={"яблоко": 10, "слива": 20, "банан": 30})
storage_2 = Store(items={"ананас": 15, "слива": 20, "арбуз": 30, "груша": 30})
shop_1 = Shop(items={"арбуз": 2, "ананас": 3, "яблоко": 1, "груша": 1})


def move():
    name_storage_1 = "склад-1"
    name_storage_2 = "склад-2"
    shop = "магазин"
    print("Программа для логистики товара между складами и магазинами запущена")
    while True:
        user_input = input("Нажмите 'ок', чтобы продолжить, если желаете завершить - 'стоп':\n")
        if user_input == "стоп":
            break
        elif user_input == 'ок':
            print("Количество и вид товара:")
            print(f"Склад-1:\n{storage_1}")
            print(f"Склад-2:\n{storage_2}")
            print(f"Магазин:\n{shop_1}")
            us_input = input("Доставить ___ __ из __ в ___:\n")
            us = us_input.split()
            user_req = f"Доставить {us[1]} {us[2]} из {us[4]} в {us[6]}"
            req = Request(user_req)
            if req.from_.lower() == name_storage_1:
                if storage_1.remove(req.product, req.count):
                    print("Нужное количество есть на складе")
                    if shop_1.add(req.product, req.count) == True:
                        print(f"Доставить {req.count} {req.product} с {req.from_} в {req.to_}")
                        print(f"Успешно доставлено в {req.to_}")
                        print(f"{name_storage_1.title()}\n{storage_1}")
                        print(f"{shop.title()}\n{shop_1}")
                    else:
                        print("В магазине недостаточно места, попробуйте что-то другое")
                        storage_1.add(req.product, req.count)
                else:
                    print("На складе нет нужного количества товара или нет такого наименования товара")
            elif req.from_.lower() == name_storage_2:
                if storage_2.remove(req.product, req.count):
                    print("Нужное количество есть на складе")
                    if shop_1.add(req.product, req.count):
                        print(f"Доставить {req.count} {req.product} с {req.from_} в {req.to_}")
                        print(f"Успешно доставлено в {req.to_}")
                        print(f"{name_storage_2.title()}\n{storage_2}")
                        print(f"{shop.title()}\n{shop_1}")
                    else:
                        print("В магазине недостаточно места, попробуйте что-то другое")
                        storage_1.add(req.product, req.count)
                else:
                    print("На складе нет нужного количества товара или нет такого наименования товара")
            elif req.from_.lower() == shop:
                if req.to_.lower() == name_storage_1:
                    if shop_1.remove(req.product, req.count):
                        print("Нужное количество есть в магазине")
                        if storage_1.add(req.product, req.count):
                            print(f"Доставить {req.count} {req.product} с {req.from_} в {req.to_}")
                            print(f"Успешно доставлено в {req.to_}")
                            print(f"{name_storage_1.title()}\n{storage_1}")
                            print(f"{shop.title()}\n{shop_1}")
                        else:
                            print("В магазине недостаточно места, попробуйте что-то другое")
                            shop_1.add(req.product, req.count)
                    else:
                        print("В магазине нет нужного количества товара или нет такого наименования товара")
                elif req.to_.lower() == name_storage_2:
                    if shop_1.remove(req.product, req.count):
                        print("Нужное количество есть в магазине")
                        if storage_2.add(req.product, req.count):
                            print(f"Доставить {req.count} {req.product} с {req.from_} в {req.to_}")
                            print(f"Успешно доставлено в {req.to_}")
                            print(f"{name_storage_2.title()}\n{storage_2}")
                            print(f"{shop.title()}\n{shop_1}")
                        else:
                            print("В магазине недостаточно места, попробуйте что-то другое")
                            shop_1.add(req.product, req.count)
                    else:
                        print("В магазине нет нужного количества товара или нет такого наименования товара")
            else:
                print(f"Такого склада нет в списке либо название склада введено не корректно")

if __name__ == "__main__":
    move()
