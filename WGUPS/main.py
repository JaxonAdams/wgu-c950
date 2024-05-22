# JAXON ADAMS -- STUDENT ID: 011441603

"""C950 - Data Structures & Algorithms II - Performance Assessment

WGUPS Routing Program implementation. Uses a hash table as the self-adjusting
data structure required for storing package data. The algorithm used to plot
truck delivery routes is a greedy algorithm called the "nearest neighbor"
algorithm.

Author: Jaxon Adams
Student ID: 011441603
"""


import csv

from lib.package import Package
from lib.hash_table import HashTable


class Simulation:
    """Creates and manages the simulation of a package delivery routing
    program. Run the simulation by invoking the "run" method.
    """

    def __init__(self, packages_path=None, distances_path=None):
    
        # load data files
        self.distance_matrix = self._load_distance_matrix(distances_path)
        self.packages = self._load_packages(packages_path)

    def _load_distance_matrix(self, filepath):
        """Read the given file for a matrix of distances between delivery
        locations. Return a two-dimensional array of distances.
        """

        distance_matrix = []
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)

            next(reader)  # remove the header row -- we don't need it processed

            distance_matrix.extend(row[1:] for row in reader)

        return distance_matrix

    def _load_packages(self, filepath):
        """Read the given file for a list of packages to be delivered, and
        load each package into a hash table.
        """

        package_hash = HashTable()
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                package = Package(
                    row["Package ID"],
                    row["Address"],
                    "UT",
                    row["Zip"],
                    row["Weight KILO"],
                    row["Delivery Deadline"],
                )

                package_hash.insert(package.id, package)

        return package_hash

    def run(self):

        print("Hello, world!")
        # print(self.distance_matrix)

        # print("HUB DISTANCE FROM HUB:", end=" ")
        # print(self.distance_matrix[0][0])  # 0

        # print("ROW 4 DISTANCE FROM HUB:", end=" ")
        # print(self.distance_matrix[3][0])  # 11

        # print("ROW 12 DISTANCE FROM ROW 7:", end=" ")
        # print(self.distance_matrix[11][6])  # 6.9

        print(self.packages)

        print("Package 1: ", self.packages.lookup("1"))
        print("    Address: ", self.packages.lookup("1").address)
        print("Package 12:", self.packages.lookup("12"))
        print("    Address: ", self.packages.lookup("12").address)


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    program = Simulation(
        distances_path="./data/distances.csv",
        packages_path="./data/packages.csv",
    )

    program.run()
