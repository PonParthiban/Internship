#bubble sort
def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

# Example
arr = [64, 34, 25, 12, 22]
print("Bubble Sort:", bubble_sort(arr))

#quick sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)


# Example
arr = [64, 34, 25, 12, 22]
print("Quick Sort:", quick_sort(arr))