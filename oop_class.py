class student:
    name = ""
    clss = ""
    school = "ABC Sen. Sec. School"
    def __init__(self, name, clas):
        self.name = name
        self.clss = clas
    def printDetails(self):
        print(f"Your name is {self.name}, class is {self.clss} and school is {self.school}")

s1 = student("Ashu","9th")
print(s1.name + s1.clss)
s1.printDetails()

s2 = student("Aashta", "10th")
s2.printDetails()