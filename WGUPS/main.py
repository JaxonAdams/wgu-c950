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

from lib.truck import Truck
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

        # trucks -- three available in this project
        self.truck1 = Truck(id=1)
        self.truck2 = Truck(id=2)
        self.truck3 = Truck(id=3)

        # package load order -- hardcoded for this project
        # first 16 is picked up by the first truck; second 16 by
        #   the second truck, etc.
        self.package_load_order = [
            '1', '4', '11', '14', '15', '16', '17', '19', '20', '21', '22',
            '24', '26', '31', '34', '40', '2', '3', '5', '7', '8', '10',
            '13', '18', '27', '29', '30', '35', '36', '37', '38', '39', '6',
            '9', '12', '23', '25', '28', '32', '33',
        ]


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

    def load_truck(self, truck, package_list):
        """Load the given truck with a group of packages."""

        for package_id in package_list:
            truck.load_package(package_id)

    def run(self):

        # load trucks
        self.load_truck(self.truck1, self.package_load_order[:16])
        del self.package_load_order[:16]

        self.load_truck(self.truck2, self.package_load_order[:16])
        del self.package_load_order[:16]

        # plot truck delivery routes
        self.truck1.plot_delivery_route(self.packages)
        self.truck2.plot_delivery_route(self.packages)


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    program = Simulation(
        distances_path="./data/distances.csv",
        packages_path="./data/packages.csv",
    )

    program.run()
