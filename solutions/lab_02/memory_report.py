# 1
import sys

empty_list = []
list_10 = list(range(10))
tuple_10 = tuple(range(10))
str_10 = "abcdefghij"
num = 42
none_obj = None

sizes = [
    {"scenario": "пустой список", "count": len(empty_list), "size": sys.getsizeof(empty_list)},
    {"scenario": "список из 10 чисел", "count": len(list_10), "size": sys.getsizeof(list_10)},
    {"scenario": "кортеж из 10 чисел", "count": len(tuple_10), "size": sys.getsizeof(tuple_10)},
    {"scenario": "строка из 10 символов", "count": len(str_10), "size": sys.getsizeof(str_10)},
    {"scenario": "целое число", "count": 1, "size": sys.getsizeof(num)},
    {"scenario": "None", "count": 1, "size": sys.getsizeof(none_obj)},
]

# 2
lst = []
last_size = sys.getsizeof(lst)
grow = [{'length': len(lst), 'size': last_size, 'diff': 0}]
for i in range(100):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != last_size:
        grow.append({'length': len(lst), 'size': size, 'diff': size - last_size})
        last_size = size

# 3
import tracemalloc

# Вариант 1: список
traced = []

tracemalloc.start()
numbers = list(range(100_000))
current, peak = tracemalloc.get_traced_memory()
traced.append({"scenario":'list(range(100_000))', "count":len(numbers), "size":sys.getsizeof(numbers), 'cur_b':current, 'peak_b':peak})
tracemalloc.stop()

tracemalloc.start()
numbers2 = range(100_000)
current2, peak2 = tracemalloc.get_traced_memory()
traced.append({"scenario":'range(100_000)', "count":len(numbers2), "size":sys.getsizeof(numbers2), 'cur_b':current2, 'peak_b':peak2})
tracemalloc.stop()

peak_ratio = traced[0]["peak_b"] / traced[1]["peak_b"]

# Вывод отчета

print("Часть 1. Размеры отдельных объектов")
for row in sizes:
    print(row["scenario"],'| элементов: ',  row["count"], '| размер в байтах: ', row["size"])

print()

print("Часть 2. Рост списка")
for row in grow:
    print('длина: ', row['length'], "| размер в байтах:", row['size'], '| разница с предыдущим:', row['diff'])

print()

print("Часть 3. Измерение через tracemalloc")

for row in traced:
    print(row['scenario'], '| элементов: ',  row["count"],'| размер в байтах: ', row["size"])
    print("Current memory: %.2f KB" % (row["cur_b"]/1024))
    print("Peak memory:    %.2f KB" % (row["peak_b"]/1024))
    print()
print("Отношение пиковых объемов (list / range): %.1f" % peak_ratio)

