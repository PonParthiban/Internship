#function dividing numbers and handle divide-by-zero exception
def division(a , b):
    try:
     result = a / b
     print(f"Result:{result}")
    except ZeroDivisionError:
     return "Zero can't be divided by zero"
division(10,0)