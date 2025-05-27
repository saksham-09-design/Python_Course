def fibo(a, b, num):
    c = a + b
    print(f"{c} ", end=" ")
    num = num - 1
    if num > 0:
        a = b
        b = c
        fibo(a, b, num)


num = int(input("Enter the Number of Elements: "))
a = 0
b = 1
print(f"{a} {b} ", end=" ")
num = num - 2
fibo(a, b, num)