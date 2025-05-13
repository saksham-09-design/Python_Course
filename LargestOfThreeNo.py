num1 = int(input("Enter one number: "))
num2 = int(input("Enter second number: "))
num3 = int(input("Enter third number: "))

if num1 == num2 and num2 == num3:
    print("All three numbers are equal.")
elif num1 == num2:
    if num1 > num3:
        print("Number 1 and 2 are largest and equal.")
    else:
        print("Number three is largest.")
elif num1 == num3:
    if num1 > num2: 
        print("Number 1 and 3 are largest and equal")
    else:
        print("Number 2 is largest")
elif num2 == num3:
    if num2 > num1:
        print("Number 2 and 3 are largest and eqal")
    else:
        print("Number 1 is largest")
elif num1 > num2:
    if num1 > num3:
        print("Number 1 is largest")
    else:
        print("Number 3 is largest")
else:
    if num2 > num3:
        print("Number 2 is largest")
    else:
        print("Number 3 is largest")
        