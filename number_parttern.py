
n=5
for i in range(n):
    for j in range(i+1):
        print(j+1,end=" ")
    print()

print()

n=5
for i in range(n):
    for j in range(i,-1,-1):
        print(j+1,end=" ")
    print()

print()

n=5
for i in range(n):
    for j in range(i,-1,-1):
        print(i+1,end=" ")
    print()

print()

n=5
for i in range(n):
    for j in range(n-i):
        print(i+1,end=" ")
    print()

print()

n=5
for i in range(n):
    for j in range(i+1):
        print(n-i,end=" ")
    print()

print()

n=5
for i in range(n):
    for j in range(i+1):
        print(n-j,end=" ")
    print()

print()

n=5
for i in range(n):
    for j in range(i,-1,-1):
        print(n-j,end=" ")
    print()

print()

n=5
for i in range(n):
    for j in range(n-i-1):
        print(" ",end="")
    for j in range(i+1):
        print(n-i,end="")
    print()

print()

