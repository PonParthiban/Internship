def decor(func):
    def wrapper(*args, **kwargs):
        print("====== Before the function call ======")
        result = func(*args, **kwargs)
        print("====== After the function call ======")
        return result
    return wrapper

@decor
def say_hello(name):
    print(f"Hello, {name}!")
say_hello("Alice")

@decor
def add(a, b):
    return a + b
result = add(5, 3)
print(f"Result of add: {result}")

