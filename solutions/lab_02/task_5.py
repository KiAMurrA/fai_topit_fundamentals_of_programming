# Часть 1
import sys

empty_list = []
list_10 = list(range(10))
tuple_10 = tuple(range(10))
str_10 = "abcdefghij"
num = 42
none_obj = None

print("Пустой список: ", sys.getsizeof(empty_list))
print("Список из 10 int: ", sys.getsizeof(list_10))
print("Кортеж из 10 int: ", sys.getsizeof(tuple_10))
print("Строка из 10 симв.: ", sys.getsizeof(str_10))
print("Целое число: ", sys.getsizeof(num))
print("None: ", sys.getsizeof(none_obj))

# Часть 2
import sys

lst = []
last_size = sys.getsizeof(lst)
print(f"len={len(lst):3d}  size={last_size:4d}  (ёмкость ≈ {(last_size - 56) // 8})")

for i in range(100):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != last_size:
        print(f"len={len(lst):3d}  size={size:4d}  (ёмкость ≈ {(size - 56) // 8})")
        last_size = size

# Часть 3
import tracemalloc

# Вариант 1: список
tracemalloc.start()
numbers = list(range(100_000))
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print("list(range(100_000)):")
print("  текущая:", current / 1024, "КБ")
print("  пиковая:", peak / 1024, "КБ")

# Вариант 2: range
tracemalloc.start()
numbers = range(100_000)
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print("range(100_000):")
print("  текущая:", current / 1024, "КБ")
print("  пиковая:", peak / 1024, "КБ")