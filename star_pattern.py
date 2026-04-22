
for i in range(1,6):
    print(" * "*i)

print()

for i in range(6,-1,-1):
    print(" * "*i)

print()

n=5
for i in range(n):
    for j in range(n-i-1):
        print(" ",end="")
    for j in range(i+1):
        print(" * ",end="")
    print()

print()

n=5
for i in range(n):
    for j in range(i):
        print(" ",end="")
    for j in range(n-i):
        print(" * ",end="")
    print()

print()

n=5
for i in range(n):
    for j in range(i,n):
       print(" ",end="")
    for j in range(i+1):
       print("*",end="")
    print()

print()

n=5
for i in range(n):
    for j in range(i+1):
       print(" ",end="")
    for j in range(i,n):
       print("*",end="")
    print()

print()

for i in range(5):
    for j in range(5):
        print(" * ",end="")
    print()

print()

n=5
for i in range(n):
    for j in range(n-i-1):
        print(" ",end="")
    for j in range(i+1):
        print(" * ",end="")
    print()
for i in range(n):
    for j in range(i+1):
        print(" ",end="")
    for j in range(n-i-1):
        print(" * ",end="")
    print()

print()

