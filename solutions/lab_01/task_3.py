import math
x = 17
y = 5
print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x // y)
print(x % y)
print(x ** y)

print(2 ** 1000)

result = 0.1 + 0.2
print(result)
print(result == 0.3)
print(result - 0.3)
print(math.isclose(result, 0.3))

a = int("42")
b = float("3.14")
c = str(2026)
d = bool(0)
e = bool(-1)
f = bool("")
g = bool("False")
h = complex(2, -3)
print(a, type(a))
print(b, type(b))
print(c, type(c))
print(d, type(d))
print(e, type(e))
print(f, type(f))
print(g, type(g))
print(h.real, h.imag, type(h))

print(int(42.9))

print(13.6 // 7)