#single 
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

print("======================================================================================")

#hiearchical
class Animal:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(f"Name: {self.name}")


class Dog(Animal):
    def speak(self):
        print("Barks")


class Cat(Animal):
    def speak(self):
        print("Meows")
d = Dog("Tom")
c = Cat("Kitty")
d.display()
d.speak()
c.display()
c.speak()

print("======================================================================================")

#multi-level
class college:
    def __init__(self, dept, section):
        self.dept = dept
        self.section = section

    def display_college(self):
        print(f"Department: {self.dept}")
        print(f"Section: {self.section}")


class classes(college):
    def __init__(self, roll_no, dept, section):
        super().__init__(dept, section)
        self.roll_no = roll_no
    
    def display_classes(self):
        self.display_college()
        print(f"Roll Number: {self.roll_no}")


class student(classes):
    def __init__(self, name, age, dept, section, roll_no):
        super().__init__(roll_no, dept, section)
        self.name = name
        self.age = age
    
    def display_student(self):
        self.display_classes()
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")


s = student("parthi", 19, "CS", "B", 144)
s.display_student()

print("======================================================================================")

#method overriding
class Animal:
    def speak(self):
        print("Animal sound")


class Dog(Animal):
    def speak(self):
        print("Bark")


d = Dog()
d.speak()   

print("======================================================================================")

#multiple

class Father:
    def skills(self):
        print("Gardening, Driving")

class Mother:
    def skills(self):
        print("Cooking, Painting")

class Child(Father, Mother):
    def show(self):
        print("Child inherits from both parents")

c = Child()
c.show()
c.skills()  