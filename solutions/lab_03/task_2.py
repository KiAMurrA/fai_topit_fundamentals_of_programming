import random

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

def main():
    print('=~' * 5, 'Статистика (первый проход + второй проход)', '=~' * 5)
    summ, mini, maxi, chet = first_pass(measurements)
    average = summ / len(measurements)
    above = second_pass(measurements, average)
    print(f"Сумма: {summ}")
    print(f"Минимум: {mini}")
    print(f"Максимум: {maxi}")
    print(f"Чётных значений: {chet}")
    print(f"Среднее: {average}")
    print(f"Значений выше среднего: {above}")

    print()
    print('=~' * 5, 'Линейный поиск', '=~' * 5)
    number = int(input("Введите число для поиска: "))
    index, compare = line_search(measurements, number)
    print(f'Индекс числа: {index}')
    print(f'Сравнений: {compare}')

    print()
    print('=~' * 5, 'Проверка на простоту', '=~' * 5)
    num = int(input("Введите положительное целое число: "))
    print("простое" if prost(num) else "составное (или меньше 2)")

    print()
    print('=~' * 5, "Сравнение поисков (число сравнений)", '=~' * 5)
    experiment()


if __name__ == "__main__":
    main()












