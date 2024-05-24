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
    
        # trucks will make three trips total
        self.first_trip = []
        self.second_trip = []
        self.third_trip = []

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

                if row["Trip"] == "1":
                    self.first_trip.append(package.id)
                elif row["Trip"] == "2":
                    self.second_trip.append(package.id)
                elif row["Trip"] == "3":
                    self.third_trip.append(package.id)

        return package_hash

    def run(self):

        print(self.first_trip, len(self.first_trip))
        print(self.second_trip, len(self.second_trip))
        print(self.third_trip, len(self.third_trip))


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    program = Simulation(
        distances_path="./data/distances.csv",
        packages_path="./data/packages.csv",
    )

    program.run()
