a = 10
b = 20

print("The numbers are: " + str(a) + " "+ str(b))

a = a ^ b
b = a ^ b
a = a ^ b

print("The numbers are: " + str(a) + " "+ str(b))