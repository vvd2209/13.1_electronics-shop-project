# -*- coding: utf-8 -*-
import csv
import os.path

from src.errors import InstantiateCSVError


class Item:
    """
    Класс для представления товара в магазине.
    """
    pay_rate = 1.0
    all = []
    CSV_PATH = os.path.join(os.path.dirname(__file__), "items.csv")  # путь к csv-файлу

    @classmethod
    def instantiate_from_csv(cls):
        """класс-метод, инициализирующий экземпляры класса `Item` данными из файла src/items.csv"""
        with open(cls.CSV_PATH, encoding='windows-1251') as csvfile:
            cls.all.clear()
            reader = csv.DictReader(csvfile)
            for attribute in reader:
                cls(attribute['name'], float(attribute['price']), int(attribute['quantity']))

        try:
            with open(cls.CSV_PATH, encoding='windows-1251') as csvfile:
                reader = csv.DictReader(csvfile)
                if reader.fieldnames != ['name', 'price', 'quantity']:
                    raise InstantiateCSVError
                cls.all.clear()
                for attribute in reader:
                    if any(value is None for value in attribute.values()):
                        raise InstantiateCSVError
                    cls(attribute['name'], float(attribute['price']), int(attribute['quantity']))
        except FileNotFoundError:
            raise FileNotFoundError('Отсутствует файл item.csv')


    @staticmethod
    def string_to_number(string):
        """статический метод, возвращающий число из числа-строки"""
        return int(float(string))

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Создание экземпляра класса item.
        :param name: Название товара.
        :param price: Цена за единицу товара.
        :param quantity: Количество товара в магазине.
        """
        self.__name = name
        self.price = price
        self.quantity = quantity
        self.all.append(self)

    def __repr__(self):
        """Отображает информацию об объекте класса в режиме отладки"""
        return f"{self.__class__.__name__}('{self.__name}', {self.price}, {self.quantity})"

    def __str__(self):
        """Отображает информацию об объекте класса для пользователей"""
        return f"{self.__name}"

    def __add__(self, other):
        """
        Складывает экземпляры класса `Phone` и `Item` (сложение по количеству товара в магазине)
        Проверяет, чтобы нельзя было сложить `Phone` или `Item` с экземплярами не `Phone` или `Item` классов.
        """
        if not issubclass(other.__class__, self.__class__):
            raise ValueError('Складывать можно только объекты Item и дочерние от них.')
        return self.quantity + other.quantity

    @property
    def name(self):
        """Возвращает имя"""
        return self.__name

    @name.setter
    def name(self, name):
        """Обрезает имя, если оно больше 10 символов"""
        if len(name) > 10:
            self.__name = name[0:10]
        else:
            self.__name = name


    def calculate_total_price(self) -> float:
        """
        Рассчитывает общую стоимость конкретного товара в магазине.

        :return: Общая стоимость товара.
        """
        self.total_price = self.price * self.quantity
        return self.total_price

    def apply_discount(self) -> None:
        """
        Применяет установленную скидку для конкретного товара.
        """
        self.price *= self.pay_rate