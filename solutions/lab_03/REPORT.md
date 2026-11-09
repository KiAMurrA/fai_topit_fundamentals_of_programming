## Задание 1. Условия и классификация данных
_Листинг кода:_
```python
LEVELS = ("недостаточный", "удовлетворительный", "хороший", "отличный")


def check_ranges(score, absences):
    if not 0 <= score <= 100:
        return "Ошибка: результат должен быть от 0 до 100."
    elif not 0 <= absences <= 5:
        return "Ошибка: число пропусков должно быть от 0 до 5."
    else:
        return None


def get_level(score, absences):
    if score >= 90:
        index = 3
    elif score >= 75:
        index = 2
    elif score >= 60:
        index = 1
    else:
        index = 0

    if absences > 3:
        index = max(index - 1, 0)
    return LEVELS[index]


def describe_work(work_type):
    match work_type:
        case "exam":
            return "экзаменационная работа"
        case "project":
            return "проектная работа"
        case "practice":
            return "практическая работа"
        case _:
            return "неизвестный тип работы"


def process_record(score, work_type, absences):
    error = check_ranges(score, absences)
    if error is not None:
        return None, error
    level = get_level(score, absences)
    line = (f"результат {score}, {describe_work(work_type)}, "
            f"пропусков {absences} -> уровень: {level}")
    return level, line

def main():
    score = int(input("Результат (0-100): "))
    work_type = input("Тип работы (exam/project/practice): ").strip()
    absences = int(input("Пропущено занятий (0-5): "))
    print(process_record(score, work_type, absences)[1])

    print("\n--- Обработка списка записей ---")
    process_list(RECORDS)


if __name__ == "__main__":
    main()
```
_Таблица результатов и ожиданий:_
 
| № | Результат | Тип | Пропуски | Ожидаемо | Фактически |
|---|-----------|-----|----------|----------|------------|
| 1 | 0 | exam | 0 | недостаточный | недостаточный |
| 2 | 59 | project | 0 | недостаточный | недостаточный |
| 3 | 60 | practice | 0 | удовлетворительный | удовлетворительный |
| 4 | 74 | exam | 3 | удовлетворительный | удовлетворительный |
| 5 | 75 | project | 0 | хороший | хороший |
| 6 | 89 | practice | 4 | удовлетворительный (понижение с «хорошего») | удовлетворительный |
| 7 | 90 | exam | 0 | отличный | отличный |
| 8 | 100 | exam | 5 | хороший (понижение с «отличного») | хороший |
| 9 | 62 | project | 4 | недостаточный (понижение с «удовлетворительного») | недостаточный |
| 10 | 30 | practice | 5 | недостаточный (нижняя граница, не понижается) | недостаточный |
| 11 | 101 | exam | 0 | сообщение об ошибке результата | Ошибка: результат должен быть от 0 до 100. |
| 12 | -1 | exam | 0 | сообщение об ошибке результата | Ошибка: результат должен быть от 0 до 100. |
| 13 | 80 | exam | 6 | сообщение об ошибке пропусков | Ошибка: число пропусков должно быть от 0 до 5. |
| 14 | 70 | essay | 0 | удовлетворительный, «неизвестный тип работы» | удовлетворительный, неизвестный тип работы |

_Недостижимые ветви:_
- При корректных данных (как гарантирует условие задачи) ветка `case _` в `describe_work` недостижима. Она достижима 
только при некорректном типе работы (сценарий 14), поэтому оставлена как защитная.
- В `get_level` отдельные условия вида `score < 0` или `score > 100` не нужны и были бы недостижимы: такие значения 
отсекаются раньше, в `check_ranges`. Ветка `else` в цепочке уровней срабатывает только для 0–59.
- В `check_ranges` ветка `else` (данные корректны) достигается, только если обе предыдущие проверки не сработали, а 
проверка пропусков выполняется, только если результат уже корректен.
- Понижение уровня: если порядок проверки `>= 90 → >= 75 → >= 60` изменить на обратный, первая же ветка `>= 60` 
«перехватывала» бы все большие значения, и ветки для 75 и 90 стали бы недостижимыми. Поэтому порядок от большего к меньшему принципиален.

__Практическое расширение:__
```python
RECORDS = (
    (95, "exam", 0),
    (89, "project", 4),
    (75, "practice", 3),
    (60, "exam", 5),
    (59, "project", 0),
    (0, "practice", 2),
    (100, "exam", 5),
    (74, "project", 4),
    (82, "practice", 1),
    (67, "exam", 0),
    (45, "project", 5)
)
```
```python
def process_list(records):
    counts = {level: 0 for level in LEVELS}
    invalid = 0
    print("Индивидуальные результаты:")
    for number, (score, work_type, absences) in enumerate(records, start=1):
        level, line = process_record(score, work_type, absences)
        print(f"{number:2}. {line}")
        if level is None:
            invalid += 1
        else:
            counts[level] += 1

    print("\nИтоговая сводка:")
    for level in reversed(LEVELS):
        print(f"  {level}: {counts[level]}")
    print(f"  некорректных записей: {invalid}")
```
_Фрагмент вывода:_
 
```
Итоговая сводка:
  отличный: 1
  хороший: 3
  удовлетворительный: 2
  недостаточный: 5
  некорректных записей: 1
```

## Задание 2. Циклы и базовые алгоритмические схемы
_Листинг кода без практического расширения:_
```python
measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]

def first_pass(data):
    summ = 0
    mini = 10000
    maxi = 0
    chet = 0
    for item in data:
        summ += item
        if item > maxi:
            maxi = item
        if item < mini:
            mini = item
        if item % 2 == 0:
            chet += 1
    return summ, mini, maxi, chet

def second_pass(data, average):
    count = 0
    for item in data:
        if item > average:
            count += 1
    return count

def line_search(data, number):
    compare = 0
    for item in data:
        compare += 1
        if item == number:
            return data.index(item), compare
    return -1, compare

def prost(num):
    if num <= 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def selection_sort(data):
    result = list(data)
    comparisons = 0
    n = len(result)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            comparisons += 1
            if result[j] < result[min_index]:
                min_index = j
        result[i], result[min_index] = result[min_index], result[i]
    return result, comparisons

def binary_search(sorted_data, target):
    low, high = 0, len(sorted_data) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if sorted_data[mid] == target:
            return mid, comparisons
        elif sorted_data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons
```
_Сложность алгоритмов_
 
| Алгоритм | Время | От чего зависит | Доп. память |
|----------|-------|-----------------|-------------|
| Статистика (первый и второй проход) | O(n) | n — длина списка; каждый элемент обрабатывается константное число раз (два прохода дают 2n, то есть O(n)) | O(1): несколько переменных-счётчиков |
| Линейный поиск | O(n) | n — длина списка; в худшем случае (элемента нет или он последний) просматриваются все элементы | O(1) |
| Проверка простоты | O(√n) | значение числа n (не длина записи): делители перебираются от 2 до √n | O(1) |
| Сортировка выбором | O(n²) | n — длина списка; число сравнений всегда n(n−1)/2 независимо от порядка данных | O(n) в моей реализации, так как сортируется копия (сама сортировка — O(1) дополнительной памяти, если сортировать на месте) |
| Бинарный поиск | O(log n) | n — длина отсортированного списка; каждое сравнение уменьшает диапазон вдвое | O(1) (итеративная версия) |

__Практическое расширение__

_Листинг кода:_
```python
def experiment():
    print(f"{'n':>5} | {'линейный: средн.':>16} | {'линейный: худш.':>15} | "
          f"{'бинарный: средн.':>16} | {'бинарный: худш.':>15} | {'сорт. выбором':>13}")
    print("-" * 97)
    for n in (10, 100, 1000):
        rng = random.Random(n)  # фиксированное зерно: повторяемость
        data = rng.sample(range(10 * n), n)  # одинаковый набор для обоих алгоритмов
        sorted_data, sort_cmp = selection_sort(data)
        absent = -1  # заведомо отсутствует

        lin_total = bin_total = 0
        lin_worst = bin_worst = 0
        for target in data:  # ищем каждый элемент набора
            _, c1 = line_search(data, target)
            _, c2 = binary_search(sorted_data, target)
            lin_total += c1
            bin_total += c2
            if c1 > lin_worst:
                lin_worst = c1
            if c2 > bin_worst:
                bin_worst = c2
        _, c1 = line_search(data, absent)  # отсутствующее значение
        _, c2 = binary_search(sorted_data, absent)
        if c1 > lin_worst:
            lin_worst = c1
        if c2 > bin_worst:
            bin_worst = c2

        print(f"{n:>5} | {lin_total / n:>16.1f} | {lin_worst:>15} | "
              f"{bin_total / n:>16.1f} | {bin_worst:>15} | {sort_cmp:>13}")
```
_Таблица сревнений:_

| n | Линейный, среднее число сравнений | Линейный, худший случай | Бинарный, среднее число сравнений | Бинарный, худший случай | Сортировка выбором, сравнений |
|------|-------|------|------|----|--------|
| 10   | 5.5   | 10   | 2.9  | 4  | 45     |
| 100  | 50.5  | 100  | 5.8  | 7  | 4950   |
| 1000 | 500.5 | 1000 | 9.0  | 10 | 499500 |

## Задаание 3. Коллекции и выбор структуры данных
_Листинг кода:_
```python
submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]

students = set()  # 1. все студенты
labs = set()  # 2. все сданные работы
attempts_by_student = {}  # 3. студент -> список попыток [(работа, результат), ...]
best_scores = {}  # 4. (студент, работа) -> лучший результат
attempt_counts = {}  # 5. (студент, работа) -> число попыток
completed_by_lab = {}  # дополнительно: работа -> множество студентов (для запросов)


def add_submission(student, lab, score):
    key = (student, lab)
    students.add(student)
    labs.add(lab)
    attempts_by_student.setdefault(student, []).append((lab, score))
    if key not in best_scores or score > best_scores[key]:
        best_scores[key] = score
    attempt_counts[key] = attempt_counts.get(key, 0) + 1
    completed_by_lab.setdefault(lab, set()).add(student)


def build(records):
    for student, lab, score in records:
        add_submission(student, lab, score)


def students_with_all_labs():
    sets = list(completed_by_lab.values())
    if not sets:
        return set()
    return set.intersection(*sets)


def print_structures():
    print("Студенты:", sorted(students))
    print("Работы:", sorted(labs))
    print("Попытки по студентам:", attempts_by_student)
    print("Лучшие результаты:", best_scores)
    print("Число попыток:", attempt_counts)

def main():
    build(submissions)
    print("=== Построенные структуры ===")
    print_structures()

    print("\nСдавали все работы:", sorted(students_with_all_labs()))

    print("\n=== Добавляем запись ('daria', 'lab_02', 4) ===")
    add_submission("daria", "lab_02", 4)
    print_structures()
    print("\nСдавали все работы:", sorted(students_with_all_labs()))

    print("\n=== Список как ключ словаря ===")
    try:
        {["anna", "lab_01"]: 5}
    except TypeError as error:
        print("TypeError:", error)
```

_Ответы на вопросы:_

**Множество подходит для уникальных значений.** Множество хранит каждый элемент не более одного раза, а повторное `add` 
существующего значения ничего не меняет. Поэтому имя `anna`, встречающееся трижды, попадёт в `students` один раз, и дубликаты 
не нужно отфильтровывать вручную. Проверка принадлежности и операции над множествами (пересечение, объединение, разность) 
тоже эффективны, так как множество устроено как хеш-таблица.
 
**Кортеж можно использовать как ключ.** Ключ словаря должен быть хешируемым, то есть иметь значение хеша, которое не меняется
за время жизни объекта. Кортеж неизменяем, поэтому его хеш вычисляется по элементам и остаётся постоянным (при условии, 
что элементы кортежа тоже хешируемы: строки в `(student, lab)` — хешируемы).
 
**Список нельзя использовать как ключ.** Список изменяем: если бы его хеш считался по содержимому, то после изменения 
списка хеш поменялся бы, и словарь не смог бы найти ключ в том месте, где его положил. Поэтому у списков хеш не определён. 
В программе это показано: `{["anna", "lab_01"]: 5}` вызывает `TypeError: unhashable type: 'list'`.
 
**Словарь предпочтительнее списка для поиска по составному ключу.** В списке записей результат для `(anna, lab_01)`
пришлось бы искать перебором: O(n) сравнений. В словаре по хеш-таблице поиск выполняется в среднем за O(1) независимо от числа записей.
 
_Средняя сложность операций_
 
| Коллекция | Добавление | Поиск / проверка принадлежности | Замечание |
|-----------|-----------|----------------------------------|-----------|
| `set` | O(1) | O(1) | в худшем случае (много коллизий) O(n) |
| `dict` | O(1) | O(1) по ключу | в худшем случае O(n) |
| `list` | `append` — O(1) амортизированно | по значению — O(n); по индексу — O(1) | вставка в начало — O(n) |
| `tuple` | создаётся за O(k), k — число элементов | по значению — O(k) | неизменяем; хеш считается за O(k), для коротких ключей — константа |

__Практическое расширение:__

_Листинг кода:_
```python
def handle_query(line):
    parts = line.split()
    match parts:
        case []:
            return ""
        case ["student", name]:
            if name not in attempts_by_student:
                return f"Студент {name} не найден."
            items = ", ".join(f"{lab}={score}" for lab, score in attempts_by_student[name])
            return f"{name}: {items}"
        case ["best", name, lab]:
            key = (name, lab)
            if key not in best_scores:
                return f"Нет данных для ({name}, {lab})."
            return f"Лучший результат {name} по {lab}: {best_scores[key]}"
        case ["attempts", name, lab]:
            key = (name, lab)
            if key not in attempt_counts:
                return f"Нет данных для ({name}, {lab})."
            return f"Попыток {name} по {lab}: {attempt_counts[key]}"
        case ["completed", lab]:
            if lab not in completed_by_lab:
                return f"Работа {lab} никем не сдавалась."
            return f"{lab} сдавали: {', '.join(sorted(completed_by_lab[lab]))}"
        case ["student" | "best" | "attempts" | "completed", *_]:
            return ("Неверное число аргументов. Формат: student <имя> | "
                    "best <имя> <работа> | attempts <имя> <работа> | completed <работа>")
        case [command, *_]:
            return f"Неизвестная команда: {command}"

def main():
    print("\n=== Запросы (exit — выход) ===")
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if line.strip() == "exit":
            break
        print(handle_query(line))
```

Пример запуска:
 
```
> student anna
anna: lab_01=5, lab_02=5, lab_01=4
> best anna lab_01
Лучший результат anna по lab_01: 5
> attempts boris lab_02
Попыток boris по lab_02: 1
> completed lab_01
lab_01 сдавали: anna, boris, daria
> student igor
Студент igor не найден.
> best anna lab_09
Нет данных для (anna, lab_09).
> hello world
Неизвестная команда: hello
```

## Задание 4. Функции, параметры и области видимости
_Исследование LEGB_
 
Python ищет имя по порядку: Local → Enclosing → Global → Built-in. Поиск останавливается на первой найденной области.
 
_Схема областей видимости_
 
```
┌─ Built-in ─────────────────────────────────────────────┐
│  len, print, max, ...                                  │
│  ┌─ Global (модуль task_4.py) ──────────────────────┐  │
│  │  course = "Основы программирования"              │  │
│  │  outer, inner не здесь: inner живет в outer      │  │
│  │  ┌─ Enclosing (функция outer) ───────────────┐   │  │
│  │  │  module = "Функции"                       │   │  │
│  │  │  ┌─ Local (функция inner) ─────────────┐  │   │  │
│  │  │  │  local_note = "изучаем ..."         │  │   │  │
│  │  │  │  nonlocal module  → ссылка наружу   │  │   │  │
│  │  │  └─────────────────────────────────────┘  │   │  │
│  │  └───────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```
 
_Порядок поиска каждого имени в `inner()`_
 
| Имя | Где найдено | Как искали |
|---|---|---|
| `local_note` | Local | Сразу найдено в `inner`, так как там присваивается |
| `module` | Enclosing | В `inner` нет своего `module` (из-за `nonlocal`), поэтому имя привязано к переменной `outer`. Присваивание меняет именно её |
| `course` | Global | Нет в Local и Enclosing → найдено в модуле. Только читается, поэтому `global` не нужен и глобальное имя не меняется |
| `len` | Built-in | Нет в Local, Enclosing, Global → найдено во встроенных |
 
`nonlocal module` без объявления привело бы к `UnboundLocalError`: присваивание `module = ...` создало бы новую локальную переменную, и чтение `module` справа стало бы чтением ещё не заданной локальной.
 
Результат запуска подтверждает: после `inner()` значение `module` в `outer` изменилось, а `course` осталось прежним.
 
_Ошибка изменяемого значения по умолчанию_
 
```python
def add_result(value, results=[]):
    results.append(value)
    return results
```
 
```
add_result(1)  # [1]
add_result(2)  # [1, 2]  — ожидали [2]
```
 
_Объяснение через жизненный цикл объекта_
 
1. Выражение `def` выполняется один раз, когда Python создаёт функцию.
2. В этот момент вычисляется значение по умолчанию: создаётся один объект-список `[]`, он сохраняется в `add_result.__defaults__`.
3. При каждом вызове без второго аргумента `results` связывается с этим же списком, а не с новым.
4. `append` изменяет объект на месте, поэтому изменения накапливаются между вызовами. Проверка: `add_result.__defaults__` → `([1, 2],)`.
Значение по умолчанию живёт столько же, сколько сама функция. Для неизменяемых значений (`int`, `str`, `None`) проблемы нет, так как их нельзя изменить на месте.

__Практическое расширение:__

_Листинг кода:_
```python
def apply_to_results(operation: Callable, values: Iterable) -> list:
    return [operation(value) for value in values]


def to_percent(score: int) -> float:
    return score / 5 * 100


def make_threshold_checker(threshold: float) -> Callable[[float], bool]:

    def check(result: float) -> bool:
        return result >= threshold  # threshold берется из замыкания

    return check


print("\n=== apply_to_results и замыкания ===")
scores = [3, 4, 5, 2]
print(apply_to_results(to_percent, scores))  # именованная функция
print(apply_to_results(lambda x: x * 2, scores))  # lambda

passed_3 = make_threshold_checker(3)
passed_5 = make_threshold_checker(5)
print(apply_to_results(passed_3, scores))  # [True, True, True, False]
print(apply_to_results(passed_5, scores))  # [False, False, True, False]
print(passed_3.__closure__[0].cell_contents, passed_5.__closure__[0].cell_contents)  # 3 5

assert apply_to_results(to_percent, [5]) == [100.0]
assert apply_to_results(lambda x: x + 1, [1, 2]) == [2, 3]
assert passed_3(3) is True and passed_5(4) is False
assert scores == [3, 4, 5, 2]
```
_Замыкание в `make_threshold_checker`_

_Листнг кода:_
```python
def make_threshold_checker(threshold):
    def check(result):
        return result >= threshold
    return check
```
 
```
passed_3 = make_threshold_checker(3)
passed_5 = make_threshold_checker(5)
```
 
Каждый вызов фабрики создаёт новую область Enclosing со своим `threshold` и новую функцию `check`. Вложенная функция 
«захватывает» ячейку (cell) с этим значением, и оно сохраняется после завершения фабрики.
 
- `passed_3` хранит `threshold = 3`, `passed_5` хранит `threshold = 5`.
- Проверка: `passed_3.__closure__[0].cell_contents` → `3`, `passed_5.__closure__[0].cell_contents` → `5`.
- Проверки независимы: на оценках `[3, 4, 5, 2]` получаем `[True, True, True, False]` и `[False, False, True, False]`.
В замыкании сохраняется значение параметра `threshold` из конкретного вызова фабрики.

## Задание 5. Анализатор учебных результатов

_Листинг кода:_
```python
import copy

students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}

NO_DATA = "Нет данных"

CATEGORIES = (
    (90, "Отлично"),
    (75, "Хорошо"),
    (60, "Удовлетворительно"),
    (0, "Неудовлетворительно"),
)


def mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def minimum(values: list[float]) -> float | None:
    if not values:
        return None
    result = values[0]
    for value in values:
        if value < result:
            result = value
    return result


def maximum(values: list[float]) -> float | None:
    if not values:
        return None
    result = values[0]
    for value in values:
        if value > result:
            result = value
    return result


def classify(score: float | None) -> str:
    if score is None:
        return NO_DATA
    if not 0 <= score <= 100:
        raise ValueError(f"Результат должен быть в диапазоне 0..100, получено {score}")
    for lower_bound, label in CATEGORIES:
        if score >= lower_bound:
            return label
    return NO_DATA



def student_summary(name: str, results: list[int]) -> dict:
    average = mean(results)
    return {
        "name": name,
        "count": len(results),
        "mean": average,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(average),
    }


def build_rating(students: dict[str, list[int]]) -> list[tuple[str, float]]:
    ranked = [
        (name, mean(results))
        for name, results in students.items()
        if results
    ]
    return sorted(ranked, key=lambda pair: (-pair[1], pair[0]))


def _leaders_from_rating(rating: list[tuple[str, float]]) -> list[str]:
    if not rating:
        return []
    best = rating[0][1]
    leaders = []
    for name, average in rating:
        if average != best:
            break
        leaders.append(name)
    return leaders


def find_top_students(students: dict[str, list[int]]) -> list[str]:
    return _leaders_from_rating(build_rating(students))


def group_summary(students: dict[str, list[int]]) -> dict:
    category_counts = {label: 0 for _, label in CATEGORIES}
    category_counts[NO_DATA] = 0

    total_sum = 0
    total_count = 0
    with_results = 0

    for name, results in students.items():
        summary = student_summary(name, results)
        category_counts[summary["category"]] += 1
        if results:
            with_results += 1
            total_sum += sum(results)
            total_count += len(results)

    rating = build_rating(students)
    return {
        "students_total": len(students),
        "students_with_results": with_results,
        "average": total_sum / total_count if total_count else None,
        "category_counts": category_counts,
        "leaders": _leaders_from_rating(rating),
        "rating": rating,
    }


def _fmt(value: float | None, precision: int = 2) -> str:
    """Число с округлением или прочерк для None."""
    if value is None:
        return "—"
    return f"{value:.{precision}f}"


def format_report(student_data: list[dict], group_data: dict) -> str:
    """Итоговый текстовый отчет.

    Вход: список результатов student_summary и словарь результата group_summary.
    Результат: многострочная строка.
    Особый случай: пустой student_data -> строка "Студентов нет".
    """
    lines = ["ОТЧЕТ ПО ГРУППЕ", "=" * 60, "", "Студенты:"]

    if not student_data:
        lines.append("  Студентов нет")
    for item in student_data:
        lines.append(
            f"  {item['name']}: результатов {item['count']}, "
            f"среднее {_fmt(item['mean'])}, "
            f"мин {_fmt(item['min'], 0)}, макс {_fmt(item['max'], 0)}, "
            f"категория: {item['category']}"
        )

    lines += ["", "Группа:"]
    lines.append(
        f"  Студентов: {group_data['students_total']} "
        f"(с результатами: {group_data['students_with_results']})"
    )
    lines.append(f"  Общий средний результат: {_fmt(group_data['average'])}")

    leaders = group_data["leaders"]
    if not leaders:
        lines.append("  Лидеров нет")
    elif len(leaders) == 1:
        lines.append(f"  Лидер: {leaders[0]}")
    else:
        lines.append(f"  Лидеры: {', '.join(leaders)}")

    lines.append("  Студентов по категориям:")
    for label, count in group_data["category_counts"].items():
        lines.append(f"    {label}: {count}")

    lines += ["", "Рейтинг:"]
    if not group_data["rating"]:
        lines.append("  Рейтинг пуст")
    for place, (name, average) in enumerate(group_data["rating"], start=1):
        lines.append(f"  {place}. {name} — {_fmt(average)}")

    return "\n".join(lines)


def run_tests() -> None:
    # --- базовые функции -------------------------------------------------
    assert mean([1, 2, 3]) == 2
    assert mean([5]) == 5
    assert mean([]) is None
    assert minimum([3, 1, 2]) == 1
    assert minimum([-1, -5, 0]) == -5
    assert minimum([7]) == 7
    assert minimum([]) is None
    assert maximum([3, 1, 2]) == 3
    assert maximum([-1, -5, -3]) == -1
    assert maximum([7]) == 7
    assert maximum([]) is None

    # --- сценарий 1: обычный набор данных --------------------------------
    original = copy.deepcopy(students)
    assert student_summary("Анна", students["Анна"]) == {
        "name": "Анна", "count": 4, "mean": 85.25,
        "min": 78, "max": 91, "category": "Хорошо",
    }
    group = group_summary(students)
    assert group["students_total"] == 4
    assert group["students_with_results"] == 4
    assert abs(group["average"] - 1032 / 13) < 1e-9
    assert group["category_counts"] == {
        "Отлично": 1, "Хорошо": 1, "Удовлетворительно": 1,
        "Неудовлетворительно": 1, NO_DATA: 0,
    }
    assert group["leaders"] == ["Дарья"]
    assert [name for name, _ in group["rating"]] == ["Дарья", "Анна", "Борис", "Илья"]
    assert find_top_students(students) == ["Дарья"]
    assert students == original  # исходный словарь и списки не изменены

    # --- сценарий 2: один студент ----------------------------------------
    solo = {"Ольга": [100]}
    solo_group = group_summary(solo)
    assert solo_group["students_total"] == 1
    assert solo_group["average"] == 100
    assert solo_group["leaders"] == ["Ольга"]
    assert solo_group["category_counts"]["Отлично"] == 1
    assert student_summary("Ольга", [100])["min"] == student_summary("Ольга", [100])["max"] == 100

    # --- сценарий 3: несколько лидеров -----------------------------------
    tie = {"Глеб": [85, 85], "Вера": [80, 90], "Дима": [70]}
    assert find_top_students(tie) == ["Вера", "Глеб"]  # оба 85.0, по алфавиту
    assert group_summary(tie)["leaders"] == ["Вера", "Глеб"]
    assert [name for name, _ in build_rating(tie)] == ["Вера", "Глеб", "Дима"]

    # --- сценарий 4: пустая группа ---------------------------------------
    empty_group = group_summary({})
    assert empty_group["students_total"] == 0
    assert empty_group["average"] is None
    assert empty_group["leaders"] == []
    assert empty_group["rating"] == []
    assert find_top_students({}) == []
    assert "Студентов нет" in format_report([], empty_group)

    # --- сценарий 5: студент без результатов -----------------------------
    assert student_summary("Ева", []) == {
        "name": "Ева", "count": 0, "mean": None,
        "min": None, "max": None, "category": NO_DATA,
    }
    mixed = {"Ева": [], "Фёдор": [70]}
    mixed_group = group_summary(mixed)
    assert mixed_group["students_total"] == 2
    assert mixed_group["students_with_results"] == 1
    assert mixed_group["average"] == 70
    assert mixed_group["category_counts"][NO_DATA] == 1
    assert mixed_group["leaders"] == ["Фёдор"]
    assert mixed_group["rating"] == [("Фёдор", 70.0)]
    only_empty = group_summary({"Ева": []})
    assert only_empty["average"] is None and only_empty["leaders"] == []

    # --- сценарий 6: граничные значения категорий ------------------------
    assert classify(100) == "Отлично"
    assert classify(90) == "Отлично"
    assert classify(89.99) == "Хорошо"
    assert classify(75) == "Хорошо"
    assert classify(74.99) == "Удовлетворительно"
    assert classify(60) == "Удовлетворительно"
    assert classify(59.99) == "Неудовлетворительно"
    assert classify(0) == "Неудовлетворительно"
    assert classify(None) == NO_DATA
    for bad in (-1, 100.5):
        try:
            classify(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"classify({bad}) должен вызывать ValueError")

    # --- формат отчета ----------------------------------------------------
    text = format_report(
        [student_summary(n, r) for n, r in students.items()], group
    )
    assert "Лидер: Дарья" in text
    assert "Общий средний результат: 79.38" in text
    assert "1. Дарья — 93.75" in text

    print("Все проверки пройдены.\n")


def main() -> None:
    student_data = [student_summary(name, results) for name, results in students.items()]
    group_data = group_summary(students)
    print(format_report(student_data, group_data))


if __name__ == "__main__":
    run_tests()
    main()
```
_Входные данные:_
```
students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}
```
_Вывод:_
```
ОТЧЕТ ПО ГРУППЕ
============================================================

Студенты:
  Анна: результатов 4, среднее 85.25, мин 78, макс 91, категория: Хорошо
  Борис: результатов 3, среднее 66.67, мин 60, макс 72, категория: Удовлетворительно
  Дарья: результатов 4, среднее 93.75, мин 90, макс 97, категория: Отлично
  Илья: результатов 2, среднее 58.00, мин 55, макс 61, категория: Неудовлетворительно

Группа:
  Студентов: 4 (с результатами: 4)
  Общий средний результат: 79.38
  Лидер: Дарья
  Студентов по категориям:
    Отлично: 1
    Хорошо: 1
    Удовлетворительно: 1
    Неудовлетворительно: 1
    Нет данных: 0

Рейтинг:
  1. Дарья — 93.75
  2. Анна — 85.25
  3. Борис — 66.67
  4. Илья — 58.00
```
_Декомпозиция_
 
Программа разбита на уровни, каждый использует только нижележащий
 
_Принципы:_
 
1. **Одна функция — одна задача.** Подсчёт, отбор лидеров и вывод разделены, поэтому каждую часть можно проверить отдельным `assert`.
2. **Вычисления отделены от вывода.** `format_report` не обращается к исходным данным, только к словарям-итогам; формат отчёта можно менять, не трогая расчёты.
3. **Данные не изменяются.** Везде создаются новые структуры (`sorted`, списковые включения, новые словари); проверка в тесте: `students == original` после всех расчётов.
4. **Особые случаи решены в нижних функциях** (`None` для пустых списков), а верхние лишь учитывают их через `if results`, `if not rating`.

_Сложность построения общей статистики_
 
Обозначим: **S** — число студентов, **n** — общее число результатов, **kᵢ** — число результатов i-го студента (n = Σkᵢ).
 
| Этап | Сложность |
|---|---|
| `student_summary` одного студента: `mean`, `minimum`, `maximum`, `len` | O(kᵢ) (три прохода, константа 3) |
| Цикл по студентам в `group_summary` (итоги, счётчики, накопление суммы) | O(n) суммарно |
| `build_rating`: средние + сортировка S элементов | O(n + S log S) |
| `_leaders_from_rating`: проход по началу рейтинга | O(S) в худшем случае |
| `format_report` | O(S) |
 
**Итого: O(n + S log S)** по времени. Линейная часть — один проход по всем результатам; `S log S` добавляет только сортировка для рейтинга. Так как обычно S ≪ n, на практике это близко к линейной.
 
**Память:** O(S) дополнительно (словари итогов, рейтинг, счётчики). Общий средний считается через накопление `total_sum` и `total_count`, без копирования всех результатов в один список.
 
Замечание о константе: средний результат каждого студента считается дважды (в `student_summary` и в `build_rating`), но это не меняет оценку O(n + S log S).

