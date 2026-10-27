import gc

gc.collect()

first = []
second = []

first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)

# Состояние сборщика мусора
print("\nАвтоматический сборщик включён:", gc.isenabled())
print("Пороги поколений:", gc.get_threshold())
print("Текущие счётчики поколений:", gc.get_count())
print("Статистика поколений:")
for number, stats in enumerate(gc.get_stats()):
    print(f"  поколение {number}: {stats}")

# 1. Запоминаем идентификаторы
first_id = id(first)
second_id = id(second)
print("\nid(first):", first_id)
print("id(second):", second_id)


def alive(object_id):
    return any(id(obj) == object_id for obj in gc.get_objects()) # Проверяет, есть ли объект с таким id среди объектов, отслеживаемых gc.


# 2. Удаляем имена
del first
del second
print("\nИмена first и second удалены")
print("Список first ещё в памяти:", alive(first_id))
print("Список second ещё в памяти:", alive(second_id))

# 3. Запускаем сборщик
collected = gc.collect()
print("\ngc.collect() вернул:", collected)
print("Список first ещё в памяти:", alive(first_id))
print("Список second ещё в памяти:", alive(second_id))

print('=' * 20)
print('Эксперимент')
# Эксперимент
import gc
import weakref


class Node:
    def __init__(self):
        self.other = None


# WeakSet не удерживает объекты, поэтому по его размеру
# видно, сколько узлов реально ещё существует
alive = weakref.WeakSet()


def make_cycle():
    a = Node()
    b = Node()
    a.other = b
    b.other = a
    alive.add(a)
    alive.add(b)
    return a, b


gc.collect()  # чистим мусор, накопившийся до эксперимента

print("Автоматический сборщик включён:", gc.isenabled())
gc.disable()
try:
    print("Автоматический сборщик отключён:", not gc.isenabled())

    # Создаём 5 циклов и сразу теряем внешние ссылки
    # (функция возвращает пару, но мы её не сохраняем)
    for _ in range(5):
        make_cycle()

    print("\nЦиклов создано: 5, узлов должно быть 10")
    print("Узлов в памяти после удаления внешних ссылок:", len(alive))

    collected = gc.collect()
    print("\ngc.collect() вернул:", collected)
    print("Узлов в памяти после gc.collect():", len(alive))
finally:
    # Автоматическая сборка восстанавливается, даже если произошла ошибка
    gc.enable()

print("\nАвтоматический сборщик снова включён:", gc.isenabled())

print('=' * 20)
print('Практическое задание')
# Практическое задание
gc.collect()
gc.disable()

print("Собрано до создания графа:", gc.collect())

a = {"name": "A", "links": []}
b = {"name": "B", "links": []}
c = {"name": "C", "links": []}
d = {"name": "D", "links": []}

a["links"].append(b)  # A -> B
b["links"].append(c)  # B -> C
c["links"].append(a)  # C -> A

for node in (a, b, c, d):
    print(node["name"], "->", [n["name"] for n in node["links"]])

del a, b, c
print("Собрано после удаления графа:", gc.collect())

print("D доступен:", d["name"], d["links"])

gc.enable()