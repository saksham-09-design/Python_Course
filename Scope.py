x = 20
y = 30


def temp():
    x = 30
    z = 70
    print(f"In Local Level: {x} {y} {z}")

    if x == 30:
        a = 10
        x = 40
        print(f"In Block Level: {x} {y} {z} {a}")

print(f"In Global Level: {x}")
temp()