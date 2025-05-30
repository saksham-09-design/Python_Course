class Person:
    name = ""
    age = 0
    gender = ""
    school = "ABC Public School"

    def getPerson(self, n, a, g):
        self.name = n
        self.age = a
        self.gender = g
    
    def printDetails(self):
        print("Personal Details:")
        print(f"Name = {self.name}")
        print(f"Age = {self.age}")
        print(f"Gender = {self.gender}")
        print("-----------------------------")

class student(Person):
    clas = ""
    rollNo = 0

    def getStudent(self, c, r):
        self.clas = c
        self.rollNo = r

    def printDetails(self):
        print(f"Name = {self.name}")
        print(f"Age = {self.age}")
        print(f"Gender = {self.gender}")
        print(f"School Name = {self.school}")
        print(f"Class = {self.clas}")
        print(f"Roll Number = {self.rollNo}")
        print("-----------------------------")

class Teacher(Person):
    subject = ""

    def getTeacher(self, sub):
        self.subject = sub

    def printDetails(self):
        print(f"Name = {self.name}")
        print(f"Age = {self.age}")
        print(f"Gender = {self.gender}")
        print(f"School Name = {self.school}")
        print(f"Subject = {self.subject}")
        print("-----------------------------")


p1 = Person()

t1 = Teacher()
t1.getPerson("XYZ","29","Male")
t1.getTeacher("Science")
p1 = t1
p1.printDetails()

s1 = student()
s1.getPerson("DFG", 14, "Female")
s1.getStudent("10Th", 1)
p1 = s1
p1.printDetails()