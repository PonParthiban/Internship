#array 
arr = []

# Insert
def insert(value):
    arr.append(value)

# Delete
def delete(value):
    if value in arr:
        arr.remove(value)
    else:
        print("Value not found")

# Display
def display():
    print("Array:", arr)


# Example usage
insert(10)
insert(20)
insert(30)
display()

delete(20)
display()

#single linked list

class singlynode:
    def __init__(self,val,next=None):
        self.val = val
        self.next = next
    
    def __str__(self):
        return str(self.val)
    
head = singlynode(1)
a = singlynode(2)
b = singlynode(3)
c = singlynode(4)

head.next = a 
a.next = b 
b.next = c

def display(head):
    curr = head
    elements = []

    while curr:
        elements.append(str(curr.val))
        curr = curr.next
    print(' -> '.join(elements))

display(head)

def search(head,val):
    curr = head
    while curr:
        if val == curr.val:
           return True
        curr = curr.next
    return False

print(search(head,3))

#doubly linked list

class doublylinkedlist():

    def __init__(self,val,next=None,prev=None):
        self.val = val
        self.next = next
        self.prev = prev
    
    def __str__(self):
        return (str(self.val))
    
head = tail = doublylinkedlist(1)

def display(head):
     curr = head
     elements = []
     while curr:
         elements.append(str(curr.val))
         curr = curr.next

     print(" <-> ".join(elements))

display(head)

def insert_at_beginning(head,tail,val):
    new_node = doublylinkedlist(val,next = head)
    head.prev = new_node
    return new_node, tail
head,tail = insert_at_beginning(head, tail, 3)
display(head)