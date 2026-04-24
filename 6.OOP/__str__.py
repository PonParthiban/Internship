class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

class student(person):
    def __init__(self,name,age,dept,roll_no):
        super().__init__(name,age)
        self.dept = dept
        self.roll_no = roll_no
    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Department: {self.dept}, Roll Number: {self.roll_no}"


s = student("parthi",19,"cs",104)
print(s)
