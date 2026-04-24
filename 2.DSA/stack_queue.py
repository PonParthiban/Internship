# Stack implementation
stack = []

# Push (insert)
def push(x):
    stack.append(x)

# Pop (remove)
def pop():
    if len(stack) == 0:
        print("Stack is empty")
    else:
        return stack.pop()

# Display
def display_stack():
    print("Stack:", stack)


# Example
push(10)
push(20)
push(30)
display_stack()

print("Popped:", pop())
display_stack()

# Queue implementation
queue = []

# Enqueue (insert)
def enqueue(x):
    queue.append(x)

# Dequeue (remove)
def dequeue():
    if len(queue) == 0:
        print("Queue is empty")
    else:
        return queue.pop(0)

# Display
def display_queue():
    print("Queue:", queue)


# Example
enqueue(10)
enqueue(20)
enqueue(30)
display_queue()

print("Dequeued:", dequeue())
display_queue()

