
import csv
import time
# from memory_profiler import memory_usage

'''Перебор значений'''



start_time = time.time()                                                                           # Таймер2 старт

# открытие файла
file = 'Export.csv'

user = [-72.140337, 44.411036]


def content_list(name):
    '''Получение материала для перебора'''
    with open(name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        coord = {}
        for row in reader:
            key = row['FMID']
            columns = ['x', 'y']
            if key not in coord:
                coord[key] = []

            for n in columns:
                if row[n]!='':
                    coord[key].append(float(row[n]))

    return coord


# print(len(grid))


def check_dist(coords, user_pos):
    vertex_distances = {}

    for key, value in coords.items():

        distance = sum((vp - lp) ** 2 for vp, lp in zip(value, user_pos)) ** 0.5

        if round(distance, 2)<=2:
            vertex_distances[key] = value, round(distance, 2)

    return vertex_distances

coord = content_list(file)    
# for key, value in content_list(file).items():
#     print(key, value)


result = check_dist(coord, user)

sorted_data = dict(sorted(result.items(), key=lambda val: val[1][1]))



for key, val in sorted_data.items():                                                  # Вывод результата перебора
    if val[0]:
        print(f'{key:>10}  {val}')


end_time = time.time()                                                                                    # Таймер2 конец
execution_time = end_time - start_time 
 
print(f"Время простого перебора: {execution_time} секунд")

# print(memory_usage())