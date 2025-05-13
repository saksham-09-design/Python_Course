num1 = 245

rev = 0

rem = num1 % 10
rev = rev * 10 + rem
num1 //= 10

rem = num1 % 10
rev = rev * 10 + rem
num1 //= 10

rem = num1 % 10
rev = rev * 10 + rem
num1 //= 10

print("The reverse of the number is: "+ str(rev))