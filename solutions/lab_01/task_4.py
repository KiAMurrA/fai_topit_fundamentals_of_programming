student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10

print(f'1) {student[0]}, {student[-1]}') # Первый и последний элемент имени
print(f'2) {student[:4]}, {student[5:]}') # Срез имени и фамилии
print(f'3) {student.upper()}, {student.lower()}') # Имя и фамилия верхнем и нижнем регистрах
print(f'4) {student[0]}.{student[5]}.') # Инициалы
print(f'5) {course[::-1]}')

# 1. Оператор %
res_percent = "%s — %s: %d/%d (%.1f%%)" % (
    student,
    course,
    completed,
    total,
    (completed / total) * 100,
)

# 2. Метод .format()
res_format = "{0} — {1}: {2}/{3} ({4:.1%})".format(
    student, course, completed, total, completed / total
)

# 3. f-строка
res_fstring = f"{student} — {course}: {completed}/{total} ({completed / total:.1%})"

print(res_percent)
print(res_format)
print(res_fstring)

symbol = "Я"

code_point = ord(symbol)
restored_char = chr(code_point)
utf8_encoded = symbol.encode("utf-8")
byte_length = len(utf8_encoded)

print(f"Исходный символ: {symbol}")
print(f"Кодовая позиция (ord): {code_point}")
print(f"Восстановленный символ: {restored_char}")
print(f"Результат кодирования UTF-8: {utf8_encoded}")
print(f"Длина в байтах: {byte_length}")

# s = 'Привет'
# s[0] = 'п'
# Traceback (most recent call last):
#   File "C:\Users\user\PycharmProjects\topit_fundamentals_of_programming\lab_01\task_4.py", line 47, in <module>
#     s[0] = 'п'
#     ~^^^
# TypeError: 'str' object does not support item assignment
