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

    print("\n=== Запросы (exit — выход) ===")
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if line.strip() == "exit":
            break
        print(handle_query(line))


if __name__ == "__main__":
    main()
