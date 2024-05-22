"""An implementation of a hash table. This implementation uses chaining to
handle collisions.
"""


class HashTable:

    # initialize instance attributes
    def __init__(self, initial_size=10):

        # set the initial number of buckets
        # initially 10 by default, can be manually overridden
        self.size = initial_size
        self.table = [[] for _ in range(self.size)]

        # resizing-related attributes
        self._resize_threshold = 0.7
        self._num_of_elements = 0

    # provide a custom string representation for printing
    def __repr__(self):
        
        return f"<HashTable size={self.size}>"

    # calculate the hash table's load factor
    def _load_factor(self):

        return self._num_of_elements / self.size

    # resize the hash table
    def _resize(self, new_size):

        stored_elements = []
        for bucket in self.table:
            for element in bucket:
                stored_elements.append(element)
        
        self.table = [[] for _ in range(new_size)]
        self.size = new_size
        self._num_of_elements = 0

        for element in stored_elements:
            self.insert(element.id, element)

    # insert function -- takes a package id as the key and a package instance
    #   as a value
    def insert(self, key, val):
        """Insert the given key-value pair into the hash table."""

        bucket_index = hash(key) % self.size
        self.table[bucket_index].append(val)

        # hash table upkeep -- determine if resize needed
        self._num_of_elements += 1
        if self._load_factor() >= self._resize_threshold:
            self._resize(self.size * 2)

    # lookup function -- takes a package id as input and returns the package
    def lookup(self, key):
        """Lookup the entry associated with the given key."""

        bucket_index = hash(key) % self.size
        # run a linear search on the bucket's list
        for package in self.table[bucket_index]:
            if package.id == key:
                return package
        
        return False  # not found


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    # test hash table operations
    package_table = HashTable()
    print(package_table)
    print(package_table.table)
