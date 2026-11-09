import math
from typing import Callable, Iterable


def arithmetic_mean(values: list[float]) -> float:
    """Возвращает среднее арифметическое непустого списка."""
    if not values:
        return float("nan")
    return sum(values) / len(values)


def normalize_name(name: str) -> str:
    """Удаляет лишние пробелы и приводит каждую часть имени к нужному регистру."""
    parts = name.split()
    if not parts:
        return ""
    normalized = [
        "-".join(piece.capitalize() for piece in part.split("-"))
        for part in parts
    ]
    return " ".join(normalized)


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    """Формирует строковый отчет о результатах студента."""
    name = normalize_name(student)
    if not results:
        return f"{prefix}: {name} — результатов нет"
    mean = arithmetic_mean(results)  # results не изменяем, только читаем
    return (
        f"{prefix}: {name} — работ: {len(results)}, "
        f"среднее: {mean:.{precision}f}, "
        f"максимум: {max(results)}, минимум: {min(results)}"
    )


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов."""
    seen: set[str] = set()
    cleaned: list[str] = []
    for tag in tags:
        tag = tag.strip()
        if lowercase:
            tag = tag.lower()
        if not tag or tag in seen:
            continue
        seen.add(tag)
        cleaned.append(tag)
    return tuple(cleaned)


# arithmetic_mean
assert arithmetic_mean([1, 2, 3]) == 2
assert arithmetic_mean([5]) == 5
assert math.isclose(arithmetic_mean([1.5, 2.5, 3.5, 4.5]), 3.0)
assert math.isnan(arithmetic_mean([]))
_src = [4, 5]
arithmetic_mean(_src)
assert _src == [4, 5]

# normalize_name
assert normalize_name("  иВАН   пЕТРОВ ") == "Иван Петров"
assert normalize_name("анна-мария   сидорова") == "Анна-Мария Сидорова"
assert normalize_name("") == ""
assert normalize_name("   ") == ""

# build_report
assert build_report("иван петров", [5, 4, 3]) == (
    "Результат: Иван Петров — работ: 3, среднее: 4.00, максимум: 5, минимум: 3"
)
assert "4.3333" in build_report("Иван", [4, 4, 5], precision=4)
assert build_report("Иван", [5], prefix="Итог").startswith("Итог:")
assert build_report("Иван", []).endswith("результатов нет")
_res = [3, 4]
build_report("Иван", _res)
assert _res == [3, 4]  # results не изменен

# collect_tags
assert collect_tags(" Python ", "python", "", "Flask") == ("python", "flask")
assert collect_tags("A", "a", lowercase=False) == ("A", "a")
assert collect_tags() == ()
assert collect_tags("  ", "") == ()

# precision и prefix — только именованные параметры
try:
    build_report("Иван", [5], 3)  # type: ignore[misc]
except TypeError:
    pass
else:
    raise AssertionError("precision не должен приниматься позиционно")


print("=== Позиционные и именованные аргументы ===")
print(arithmetic_mean([4, 5, 5]))
print(normalize_name("  мАРИЯ   иванова "))
print(build_report("петров пётр", [5, 4, 4]))
print(build_report("петров пётр", [5, 4, 4], precision=0, prefix="Итог"))
print(build_report(student="сидоров", results=[3, 3, 4], precision=1))
print(collect_tags("Python", "python", " OOP ", ""))
print(collect_tags("Python", "python", lowercase=False))

print("\n=== Распаковка * и ** ===")
raw_tags = ["Python", " git ", "PYTHON", "", "Git"]
print(collect_tags(*raw_tags))  # список -> позиционные аргументы

report_options = {"precision": 1, "prefix": "Зачет"}
print(build_report("козлова анна", [5, 5, 4], **report_options))  # словарь -> именованные

args = ("иванов иван", [4, 4, 5])
print(build_report(*args, **report_options))  # вместе



course = "Основы программирования"  # Global


def outer() -> str:
    module = "Функции"

    def inner() -> str:
        nonlocal module
        local_note = "изучаем области видимости"
        module = module + " и области видимости"
        # course -> Global, len -> Built-in, local_note -> Local, module -> Enclosing
        return f"{course}: {module} ({local_note}, символов: {len(module)})"

    result = inner()
    return f"{result} | после inner: {module}"


print("\n=== LEGB ===")
print(outer())
print("course не изменился:", course)
assert course == "Основы программирования"


def add_result_buggy(value, results=[]):
    results.append(value)
    return results


def add_result(value, results=None):
    if results is None:
        results = []
    results.append(value)
    return results


print("\n=== Изменяемый аргумент по умолчанию ===")
print(add_result_buggy(1))  # [1]
print(add_result_buggy(2))  # [1, 2]
print(add_result_buggy.__defaults__)  # ([1, 2],)
print(add_result(1))  # [1]
print(add_result(2))  # [2]
assert add_result(1) == [1]
assert add_result(2) == [2]
assert add_result(3, [1, 2]) == [1, 2, 3]



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