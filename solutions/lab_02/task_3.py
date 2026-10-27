import sys

data = [1, 2, 3]
print("После создания:", sys.getrefcount(data))

alias = data
print("После создания alias:", sys.getrefcount(data))

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data))

del alias
print("После del alias:", sys.getrefcount(data))

container.clear()
print("После очистки контейнера:", sys.getrefcount(data))

print('=' * 20)
# Дополнительная программа со слабой ссылкой
import weakref

class Record:
    pass

record = Record()
weak_record = weakref.ref(record)

print(weak_record())
del record
print(weak_record())

print('=' * 20)
# Практическая задача
class Record:
    def __init__(self, name):
        self.name = name


registry = weakref.WeakValueDictionary()

r1 = Record("первая")
r2 = Record("вторая")
temp = Record("третья")

registry["r1"] = r1
registry["r2"] = r2
registry["r3"] = temp

print("Сначала:", sorted(registry.keys()))

del temp
print("После del temp:", sorted(registry.keys()))

del r2
print("После del r2:", sorted(registry.keys()))