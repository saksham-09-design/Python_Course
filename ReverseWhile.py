num1 = int(input("Enter a number: "))
rev = 0

while(num1 > 0):
    rem = num1 % 10
    rev = rev * 10 + rem
    num1 = num1 // 10

print("The reverse of number is: " + str(rev))