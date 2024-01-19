import itertools as itr


class grid_search:

    '''Конструктор'''

    def __init__(self, file_data) -> None:
        self.radius = 3
        self.grid_borders = {}
        self.filled_map = {}
        self.every_dot = []
        self.user_square = 0
        self.period_len = 0
        self.first_square_coords = 0
        self.closest_points = {}

        self.file_data = file_data
        # в классе храним информацию о сетке по которой ее можно будет запросить и воспроизвести
        # все точки на плоскости(комбинации), список рассортированных 


    '''Сортировка и работа с данными'''

    def content_list(self, dict):
        '''
        Преобразование  и сортировка данных
        '''
        coord = {}
        for row in dict:
            key = row['FMID']
            columns = ['x', 'y']
            for n in columns:
                if row[n]!='':
                    if key not in coord:
                        coord[key] = []
                    coord[key].append(float(row[n]))
        return coord

    def min_max(self, coord):
        '''
        Sort and display the _minimum and _maximum of the specified dictionary based on data base
        '''
        x_val = []
        for x, y in coord.values():
            x_val.append(x)
        y_val = []
        for x, y in coord.values():
            y_val.append(y)

        x_val = sorted(x_val)
        y_val = sorted(y_val)

        x_min_max = x_val[0], x_val[-1]
        y_min_max = y_val[0], y_val[-1]

        return x_min_max, y_min_max
    

    '''Подготовка к построению сетки'''


    def period_and_1square_points(self, points):
        return len(points), [0, 1, len(points), len(points)+1]
    

    def divide_into_parts(self, coord__min, coord__max):
        '''
        Divide x and y lines by equal parts. Takes _minimum and _maximum x or y value as args
        '''
        temp_list = []
        tenth = (coord__max - coord__min) / 7
        def counter(list, coord__min, coord__max):
            while coord__max > coord__min:
                coord = coord__min + tenth
                list.append(coord)
                coord__min = coord  # исправлено: обновляем начальное значение для следующей итерации
        counter(temp_list, coord__min, coord__max)
        return [coord__min] + temp_list


    def combine(self, x_list, y_list):
        '''
        Combinations of points for grid building
        '''
        comb = list(itr.product(x_list, y_list))
        return comb


    '''Стройка'''

    def build_grid(self, combinations, first_sq_points, row_len):
        '''
        Form squares. Takes combinations of points as arg
        '''
        grid = {}
        c = 1
        def filler(sq_name, points, c):
            try:
                fin_point = combinations[points[0]], combinations[points[3]]

                if sq_name not in grid:
                    grid[sq_name] = []

                for i in fin_point:
                    grid[sq_name].append(i)

                # Условие выхода из рекурсии: если следующий индекс выходит за пределы
                if points[3] + 1 >= len(combinations):
                    return

                # Рекурсивный вызов с новыми значениями
                new_sq_name = 'square' + str(c)
                new_points = [i + 1 for i in points]
                filler(new_sq_name, new_points, c+1)
            except IndexError:
                # Если мы вышли за пределы списка, выходим из рекурсии
                return
        # Начальные значения для первого вызова
        filler('square0', first_sq_points, c)

        del_indx = len(grid)                                             # костыль.... убираем лишние квадраты
        del_list = []
        for _ in range(0, row_len):
            del_indx -= row_len
            del_list.append(del_indx)

        for i in del_list:
            if i>0:
                del grid['square'+str(i)]


        return grid

    '''ПРЕДВАРИТЕЛЬНЫЙ ПОИСК'''

    '''Делим сетку пополам'''

    def div_half(self, combinations):   
        if len(combinations)%2==0:
            x = len(combinations)//2
            first_half, second_half = combinations[:x], combinations[x:]

        first_half = first_half[0], first_half[-1]
        second_half = second_half[0], second_half[-1]

        return first_half, second_half


    '''Принадлежность точки к области'''

    def is_in(self, point, square):
        try:
            _min, _max = square[0], square[1]
            x, y = point[0], point[1]
            # print(x, y)
            if _min[0]<=x and _max[0]>=x and _min[1]<=y and _max[1]>=y:
                return x, y
        except IndexError:
            pass

    '''Заполнение сетки'''

    def fill_grid(self, content, grid):
        filled_grid = {}
        for key, value in grid.items():
            for id, point in content.items():
                # print('point', point)
                # print('value', value)
                point_pos = self.is_in(point, value)
                if point_pos:
                    if key not in filled_grid:
                        filled_grid[key] = []
                    point_id = point_pos, id
                    filled_grid[key].append(point_id)
        return filled_grid


    '''Поисковики'''

    def find_neibours(self, sq_name, period_and_1square_points):
        square_number = int(sq_name.replace('square', ''))
        x = period_and_1square_points-1
        neibour_indx = [
            (square_number - x + 1), (square_number + 1), (square_number + x + 1),
            (square_number - x), square_number, (square_number + x),
            (square_number - x - 1), (square_number - 1), (square_number + x - 1)
        ]

        neibours = ['square'+str(i) for i in neibour_indx if i>=0]

        return neibours

    def half_search(self, user):
        '''
        Сужаем поиск до половины
        
        '''
        first_half, second_half = self.div_half(self.every_dot)
        half = len(self.filled_map)//2
        if self.is_in(user, first_half):
            search_field = dict(list(self.grid_borders.items())[:half])
            # print(search_field, self.grid_borders)
            for key, value in search_field.items():
                if self.is_in(user, value):
                    self.user_square = key


            print(f'User position found in the first half,  {self.user_square}')
        elif self.is_in(user, second_half):
            search_field = dict(list(self.grid_borders.items())[half:])
            # print(search_field, self.grid_borders)
            for key, value in search_field.items():
                if self.is_in(user, value):
                    self.user_square = key

            print(f'User position found in the second half,  {self.user_square}')
        else:
            raise ValueError('User position is out of range!\nPlease, try again.')
        return self.user_square

    def radius_search(self, user):
        '''
        Финальный поиск по радиусу
        
        '''
        square_range = self.find_neibours(self.user_square, self.period_len)
        # print(square_range)

        position_list = {}

        for square in square_range:
            try:
                dots_list = self.filled_map[square]

                for dot in dots_list:
                    dot_id = dot[1]
                    dot_coord = dot[0]
                    distance = sum((vp - lp) ** 2 for vp, lp in zip(dot_coord, user)) ** 0.5

                    if round(distance, 2)<=self.radius:
                        position_list[dot_id] = dot_coord, round(distance, 2)
            except KeyError:
                pass
        self.closest_points = dict(sorted(position_list.items(), key=lambda val: val[1][1]))

        return self.closest_points


    '''Вызывающие функции'''

    def map_builder(self):
        '''
        Строит сетку
        
        '''
        coord = self.content_list(self.file_data)
        x_min_max, y_min_max = self.min_max(coord)
        border_x = self.divide_into_parts(*x_min_max)
        border_y = self.divide_into_parts(*y_min_max)
        self.every_dot = self.combine(border_x, border_y)
        self.period_len, self.first_square_coords = self.period_and_1square_points(border_x)
        self.grid_borders = self.build_grid(self.every_dot, self.first_square_coords, self.period_len)
        self.filled_map = self.fill_grid(coord, self.grid_borders)  
        print('Сетка успешно построена!')
        return self.every_dot, self.period_len, self.first_square_coords, self.filled_map, self.grid_borders


    def search(self, user):
        '''
        Поиск по готовой сетке
        '''
        self.user_square = self.half_search(user)
        self.closet_points = self.radius_search(user)
        return self.closest_points



if __name__ == '__main__':
    import server
    # from memory_profiler import memory_usage
    import time

    db = server.Database()
    db.open_database('Export.csv')
    file = db.data
    user = (-72.140337, 44.411036)
    srch = grid_search(file)

    start_time = time.time()  # Таймер1 старт
    srch.map_builder()

    end_time = time.time()
    execution_time = end_time - start_time                                  
    
    print(f"Время создания сетки: {execution_time} секунд")

    start_time = time.time()

    res = srch.search(user)
    chk = 0
    for index, coordinates in res.items():                                          # Вывод результата на консоль
        if coordinates[0]:
            x = coordinates[0][0]
            y = coordinates[0][1]
            dist = coordinates[1]
            print(f'{chk:<5} Индекс: {index} x: {x:<5}  y: {y:<5} Расстояние: {dist:<5} миль')
            chk +=1

    end_time = time.time()
    execution_time = end_time - start_time 
 
    print(f"Время перебора по сетке: {execution_time} секунд")    

    # print(f'Memory usage: {memory_usage()}')
