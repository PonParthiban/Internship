class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]   # list of buckets

    # Hash function
    def hash_function(self, key):
        return key % self.size

    # Insert
    def insert(self, key):
        index = self.hash_function(key)
        if key not in self.table[index]:   # avoid duplicates
            self.table[index].append(key)

    # Search
    def search(self, key):
        index = self.hash_function(key)
        return key in self.table[index]

    # Delete
    def delete(self, key):
        index = self.hash_function(key)
        if key in self.table[index]:
            self.table[index].remove(key)
        else:
            print("Key not found")

    # Display
    def display(self):
        for i, bucket in enumerate(self.table):
            print(i, ":", bucket)


# Example usage
ht = HashTable(5)

ht.insert(10)
ht.insert(15)
ht.insert(20)
ht.insert(7)

ht.display()

print("Search 15:", ht.search(15))

ht.delete(15)
ht.display()