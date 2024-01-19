import csv
import math


class Database:
    # filename = 'Export.csv'

    def __init__(self):
        self.sheet = {}  # Атрибут для хранения содержимого страницы (метод show_sheet)
        self.sheet_size = 10  # Атрибут для задания величины страницы
        self.data = {}  # Атрибут содержит в себе преобразованные данные из csv

    def show_filtered_markets(self, list_reader, tuple_filter):
        """
        Метод фильтрует данные таблицы по одному заданному одному параметру
        :param list_reader: передается либо объект DictReader, либо список - результат предыдущей фильтрации
        :param tuple_filter: key - наименование столбца, value - значение, по которому фильтруем
        :return: list отфильтрованных магазинов(dict)
        """
        key, value = tuple_filter

        def filter_function(dict_filter):
            """
            Метод задает функцию для фильтрации магазинов
            :param dict_filter: данные магазина в виде dict
            :return: Bool
            """
            return dict_filter.get(key) == value

        result_generator = filter(filter_function, list_reader)
        return list(result_generator)

    def show_filtered_markets_city_state(self, list_reader, city, state):
        """
        Метод фильтраует данные таблицы по заданному city и state
        :param list_reader: принимает объет DictReader, когда у класса будет атрибут DictReader этот параметр надо будет
                            убрать!
        :param city: задает значение столбца city
        :param state: задает значение столбца state
        :return: list отфильтрованных данных
        """
        filtered_markets_state = self.show_filtered_markets(list_reader, ('State', state))
        filtered_markets_city_state = self.show_filtered_markets(filtered_markets_state, ('city', city))
        return list(filtered_markets_city_state)

    def show_sheet(self, sheet_number):
        """
        Метод разбивает массив данных на страницы и возвращает
        данные с указанной пользователем страницы. Размер страницы
        по умолчанию составляет 10 строк.
        :param sheet_number: задаёт значение страницы для вывода
        :return: list данных, если страница существует, и False, если её нет
        Для изменения размера страницы используйте атрибут sheet_size
        """
        self.num_of_sheets = math.ceil(len(self.data) / self.sheet_size)  # Вычисляем общее количество страниц
        if sheet_number != 0 and sheet_number < self.num_of_sheets:  # Если введённая страница входит в диапазон
            self.start_index = (sheet_number - 1) * self.sheet_size  # Вычисляем стартовый индекс страницы
            self.end_index = min(sheet_number * self.sheet_size, len(self.data))  # Вычисляем конечный индекс страницы
            self.sheet = self.data[self.start_index:self.end_index]  # Выполняем срез списка, чтобы получить содержимое страницы
            return self.sheet  # Возвращаем срез
        else:
            return False

    def open_database(self, filename):
        """
        Метод открывает базу данных, хранящуюся в .csv файле
        :param filename: принимает имя файла для открытия
        :return: True, если файл открыт успешно, или False, если открыть файл не удалось
        """
        try:
            with open(filename, 'r', encoding='UTF-8') as self.file:  # Открытие файла
                self.reader = csv.DictReader(self.file)  # Читаем данные в виде списка
                self.data = list(self.reader)  # Преобразуем данные в список
                return True  # Возвращаем True
        except FileNotFoundError:  # Если ошибка
            return False  # Возвращаем False
            
    def return_frame(self):
        """
        Возвращаем все данные
        """
        return self.data

    def return_headers(self):
        """
        Возвращаем заголовки
        """
        return self.data[0].keys()

if __name__ == '__main__':
    # with open(Database.filename, 'r', encoding="utf-8") as file:
    #    reader = csv.DictReader(file)
    #    database = Database()
    #    for i in database.show_filtered_markets_city_state(reader, 'Highlands', 'New Jersey'):
    #        print(i.get('MarketName'))
    database = Database()
    if database.open_database('Export.csv'):
        print("База данных открыта успешно.")
        print("Выполняем поиск по городу и штату:")
        for i in database.show_filtered_markets_city_state(database.data, 'Highlands', 'New Jersey'):
            print(i.get('MarketName'))
        print("Выводим содержимое пятой страницы:")
        sheet = database.show_sheet(5)
        for i in sheet:
            print(i)
    else:
        print("Базу данных открыть не удалось.")

