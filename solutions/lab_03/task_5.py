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