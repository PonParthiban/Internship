class car:
    def __init__(self, make , model):
        self.make = make
        self.model = model
    
    def display(self):
        print(f"Car: {self.make}, {self.model}")

c1 = car("swift","desire")
c1.display()
