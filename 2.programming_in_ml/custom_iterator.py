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
