#custom iterator
class myiterator:
    def __init__(self,limit):
        self.limit = limit
        self.current = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= self.limit:
          value = self.current
          self.current += 1
          return value
        else:
          raise StopIteration
        
for i in myiterator(5):
   print(i)

print("\n")
class even_no():
    def __iter__(self):
        self.n = 2  
        return self

    def __next__(self):
        x = self.n
        self.n += 2  
        return x

even = even_no()
it = iter(even)

print(next(it))  
print(next(it)) 
print(next(it))  
print(next(it)) 
print(next(it))
    