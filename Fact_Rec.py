def factorial(num):
    if num > 0:
        return num * factorial(num-1)
    else:
        return 1

num = int(input("Enter a Number: "))
fact = factorial(num)
print(f"The Factorial is: {fact}")