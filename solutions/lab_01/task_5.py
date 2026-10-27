# В данной программе я получаю переменные от пользователся с помощью input, а после вывожу их с помощью f-строк для того,
# чтобы можно было провести различные действия над переменными
user_name = input('Введите имя исследователя: ')
task_name = input('Введите название эксперимента: ')
number_of_launches = int(input('Введите количество выполненных запусков (целое число): '))
length_of_launch = float(input('Введите длительность одного запуска в секундах (вещественное число): '))
print('Введите действительную и мнимую части комплексного числа')
real_part = float(input('Введите действительную часть: '))
imag_part = float(input('Введите мнимую часть: '))
complex_number = complex(real_part, imag_part)

print('=' * 40)
print(f'ЭКСПЕРИМЕНТ: {task_name}')
print(f'Исследователь: {user_name}')
print(f'Запуски: {number_of_launches}')
print(f'Общее время: {length_of_launch * number_of_launches: .2f} с ({length_of_launch * number_of_launches / 60: .2f} мин)')
print(f'Коэффициент: {complex_number}')
print(f'Квадрат модуля: {real_part ** 2 + imag_part ** 2}')
print(f'Есть выполненные запуски: {bool(number_of_launches)}')
print('=' * 40)

print('Диагностическая строки')
print(f'Тип значения имени и названия эксперимента: {type(user_name)}, {type(task_name)}')
print(f'Тип значения количества запусков: {type(number_of_launches)}')
print(f'Тип значения длительности запуска: {type(length_of_launch)}')
print(f'Тип значения комплексного числа: {type(complex_number)}')



