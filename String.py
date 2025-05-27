str = "Welcome to Python!"

print(str[:7])
print(str[7:])
print(str[:-7])
print(str[-7:])
print(str[0:7])
print(str[::2])

str1 = "Hello World!"
print(str1.upper())
print(str1.lower())
print(str1.capitalize())
print(str1.split())
print(str1.replace("World!","Friends!"))
print(str1.find("World!"))

message = '''Hello Sir,
Good Afternoon,
Hope you find this message well.'''

print(message)

name = "Decode with Saksham!"
subscribers = 79

str2 = f"Our channel name is: {name} and current subscribers are: {subscribers}"
print(str2)