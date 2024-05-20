"""An implementation of a hash table. Uses chaining to handle collisions."""


class HashTable:

    # initialize instance attributes
    def __init__(self, initial_size=10):

        # set the initial number of buckets
        # 10 by default, can be manually overridden
        self.size = initial_size

    # provide a custom string representation for printing
    def __repr__(self):
        
        return f"<HashTable size={self.size}>"


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    # test hash table operations
    package_table = HashTable()
    print(package_table)
