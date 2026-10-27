import copy


def print_info(step_name, structures):
    print(f"\n{'=' * 20} {step_name} {'=' * 20}")
    for name, obj in structures.items():
        ext_id = id(obj)
        nested_id = id(obj[0]) if len(obj) > 0 else "N/A"
        grade_id = id(obj[0][1]) if len(obj) > 0 and len(obj[0]) > 1 else "N/A"

        print(f"\n[{name.upper()}]: {obj}")
        print(f"  • id внешнего списка:          {ext_id}")
        print(f"  • id первого вложенного списка: {nested_id}")
        print(f"  • id первой оценки (obj[0][1]): {grade_id}")


# 1. Инициализация исходных структур
original = [
    ["Python", 5],
    ["Algorithms", 4],
]
alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

structures = {
    "original": original,
    "alias": alias,
    "shallow": shallow,
    "deep": deep,
}

print_info("Исходное состояние", structures)

# 2. Первое изменение: добавление элемента во внешний список
original.append(["Databases", 5])
print_info("После: original.append(['Databases', 5])", structures)

# 3. Второе изменение: модификация вложенного изменяемого объекта
original[0][1] = 3
print_info("После: original[0][1] = 3", structures)


wrong_matrix = [[0] * 3] * 3
wrong_matrix[0][0] = 1
print(f"wrong_matrix:   {wrong_matrix}")
print(f"id строк wrong_matrix:   {[id(row) for row in wrong_matrix]} (все id совпадают)")

correct_matrix = [[0] * 3 for _ in range(3)]
correct_matrix[0][0] = 1
print(f"correct_matrix: {correct_matrix}")
print(f"id строк correct_matrix: {[id(row) for row in correct_matrix]} (каждая строка уникальна)")