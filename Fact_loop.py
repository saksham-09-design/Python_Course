num = int(input("Enter a Number: "))
fact = 1

while(num > 0):
    fact = fact * num
    num = num -1

print(f"The Factorial is {fact}")