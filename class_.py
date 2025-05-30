class car:
    company = ""
    model = ""
    year = 0

    def __init__(self, c="Tata", m="Harier", y=2025):
        self.company = c
        self.model = m
        self.year = y
    
    def printCar(self):
        print(f"Company: {self.company}")
        print(f"Model: {self.model}")
        print(f"Year: {self.year}")

c1 = car("Hyundai", "XYZ", 2025)
c1.printCar()

c2 = car()
c2.printCar()