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
import queue
from datetime import datetime, timedelta

from lib.truck import Truck
from lib.package import Package
from lib.hash_table import HashTable


class Simulation:
    """Creates and manages the simulation of a package delivery routing
    program. Run the simulation by invoking the "run" method.
    """

    def __init__(self, packages_path=None, distances_path=None):
    
        # load data files
        self.addresses = []
        self.distance_matrix = self._load_distance_matrix(distances_path)
        self.packages = self._load_packages(packages_path)

        # trucks -- three available in this project
        self.truck1 = Truck(id=1, address_list=self.addresses, distance_matrix=self.distance_matrix)
        self.truck2 = Truck(id=2, address_list=self.addresses, distance_matrix=self.distance_matrix)
        self.truck3 = Truck(id=3, address_list=self.addresses, distance_matrix=self.distance_matrix)

        # package load order -- hardcoded for this project
        # first 16 is picked up by the first truck; second 16 by
        #   the second truck, etc.
        self.package_load_order = [
            '1', '6', '11', '14', '15', '16', '17', '19', '20', '21', '22',
            '24', '26', '31', '34', '40', '2', '3', '5', '7', '8', '10',
            '13', '18', '27', '29', '30', '35', '36', '37', '38', '39', '4',
            '12', '23', '25', '28', '32', '33', None, None, None, None, None,
            None, None, None, None, '9',
        ]

        self.events = queue.PriorityQueue()


    def _load_distance_matrix(self, filepath):
        """Read the given file for a matrix of distances between delivery
        locations. Return a two-dimensional array of distances.
        """

        distance_matrix = []
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)

            self.addresses = next(reader)[1:]

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

    def prep_delivery(self, truck):
        """Prepare a delivery trip by loading packages onto a truck and
        plotting the delivery route.
        """

        truck.route = []
        truck.packages = []

        self.load_truck(truck, self.package_load_order[:16])
        del self.package_load_order[:16]

        truck.plot_delivery_route(self.packages)

    def run(self):

        # load trucks
        self.prep_delivery(self.truck1)
        self.prep_delivery(self.truck2)

        active_deliveries = []
        # self.load_truck(self.truck1, self.package_load_order[:16])
        # del self.package_load_order[:16]

        # self.load_truck(self.truck2, self.package_load_order[:16])
        # del self.package_load_order[:16]

        # # plot truck delivery routes
        # self.truck1.plot_delivery_route(self.packages)
        # self.truck2.plot_delivery_route(self.packages)

        start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

        # truck1_delivery = self.truck1.deliver_packages(
        #     self.packages,
        #     start_time=start_time,
        # )
        # truck2_delivery = self.truck2.deliver_packages(
        #     self.packages,
        #     start_time=start_time + timedelta(minutes=26),
        # )

        active_deliveries.append(
            self.truck1.deliver_packages(
                self.packages,
                start_time=start_time,
            )
        )

        active_deliveries.append(
            self.truck2.deliver_packages(
                self.packages,
                start_time=start_time + timedelta(minutes=26),
            )
        )

        # t1_first_event = next(truck1_delivery)
        # t2_first_event = next(truck2_delivery)
        
        # self.events.put(t1_first_event)
        # self.events.put(t2_first_event)

        for delivery_proc in active_deliveries:
            self.events.put(next(delivery_proc))

        total_distance_traveled = 0
        simulation_time = start_time
        while simulation_time < datetime.now().replace(hour=17, minute=0):
            if self.events.empty():
                print("End of events.")
                print(f"Distance travelled: {total_distance_traveled:.2f} mi")
                print("Simulation end time:", simulation_time.strftime("%H:%M"))
                print("\n\n")
                self.packages.print_all()
                break

            current_event = self.events.get()
            simulation_time, truck_id, distance, previous_action = current_event
            total_distance_traveled += distance
            print(f"Truck: {truck_id} -- {current_event}")
                
            if truck_id == 1:
                active_truck = self.truck1
                active_delivery = active_deliveries[0]
            elif truck_id == 2:
                active_truck = self.truck2
                active_delivery = active_deliveries[1]

            if (previous_action == "Returned to the HUB"
                and not len(active_truck.packages)
                and len(self.package_load_order)):
                self.prep_delivery(active_truck)
                new_delivery = active_truck.deliver_packages(
                    self.packages,
                    start_time=simulation_time,
                )
                if truck_id == 1:
                    delivery_index = 0
                elif truck_id == 2:
                    delivery_index = 1
                active_deliveries[delivery_index] = new_delivery
                self.events.put(next(new_delivery))

            try:
                next_event = active_delivery.send(simulation_time)
            except StopIteration:
                pass
            else:
                self.events.put(next_event)


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    program = Simulation(
        distances_path="./data/distances.csv",
        packages_path="./data/packages.csv",
    )

    program.run()
