"""An implementation of a hash table. Uses chaining to handle collisions."""


class HashTable:

    # initialize instance attributes
    def __init__(self, initial_size=10):

        # set the initial number of buckets
        # initially 10 by default, can be manually overridden
        self.size = initial_size
        self.table = [[] for _ in range(self.size)]

    # provide a custom string representation for printing
    def __repr__(self):
        
        return f"<HashTable size={self.size}>"

    def insert(self, key, val):
        """Insert the given key-value pair into the hash table."""

        bucket_index = hash(key) % self.size
        self.table[bucket_index].append(val)


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    # test hash table operations
    package_table = HashTable()
    print(package_table)
    print(package_table.table)

    package_table.insert("12", 42)
    package_table.insert("13", 100)
    package_table.insert("1123", 15)

    print(package_table.table)
