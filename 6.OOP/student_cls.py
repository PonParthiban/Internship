class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def display_person(self):
        print(f"name: {self.name}")
        print(f"age: {self.age}")

class student(person):
    def __init__(self,name,age,dept,roll_no):
        super().__init__(name,age)
        self.dept = dept
        self.roll_no = roll_no
    
    def display_student(self):
        self.display_person()
        print(f"Department: {self.dept}")
        print(f"Roll Number: {self.roll_no}")

s = student("parthi",19,"cs",104)
s.display_student() 