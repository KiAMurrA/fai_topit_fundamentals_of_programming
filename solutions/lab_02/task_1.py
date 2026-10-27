# Эксперимент А
# a = 10
# b = a
#
# print(a, b)
# print(id(a), id(b))
#
# a += 1
#
# print(a, b)
# print(id(a), id(b))

# Эксперимент В
# first = [10, 20]
# second = first
#
# print(first, second)
# print(id(first), id(second))
#
# second.append(30)
#
# print(first, second)
# print(id(first), id(second))
# # Дополнение
# second = [10, 20, 30]
# print(first, second)
# print(first == second)
# print(first is second)
# second.append(40)
# print(first, second)

# Практическое задание

conf1 = ['Проект', ['Сергей', 'Егор'], [100, 0]]
conf2 = conf1

print('До изменения:')
print('conf1 = ', conf1)
print('conf2 = ', conf2)

conf2[1].append('Влад')
conf2[2][0] = 200

print('\nПосле изменения:')
print('conf1 = ', conf1)
print('conf2 = ', conf2)

conf3 = ['Проект', ['Сергей', 'Егор'], [100, 0]]
conf1[1].append("Лиза")
conf1[2][0] = 200

assert conf1 is not conf3
assert conf1[1] is not conf3[1]
assert conf1[2] is not conf3[2]
assert "Лиза" not in conf3[1]
assert conf1[2][0] == 200
assert conf3[2][0] == 100
print("\nПервая конфигурация (зависимая с conf2): ", conf1)
print("Независимая конфигурация: ", conf3)