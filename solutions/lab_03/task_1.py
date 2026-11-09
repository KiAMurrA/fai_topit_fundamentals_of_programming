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


def main():
    score = int(input("Результат (0-100): "))
    work_type = input("Тип работы (exam/project/practice): ").strip()
    absences = int(input("Пропущено занятий (0-5): "))
    print(process_record(score, work_type, absences)[1])

    print("\n--- Обработка списка записей ---")
    process_list(RECORDS)


if __name__ == "__main__":
    main()