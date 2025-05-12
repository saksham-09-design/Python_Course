num1 = 1234
total = 0

rem = num1 % 10
total += rem
num1 //= 10

rem = num1 % 10
total += rem
num1 //= 10

rem = num1 % 10
total += rem
num1 //= 10

rem = num1 % 10
total += rem
num1 //= 10

print("The sum of digits of number is: " + str(total))