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

        # trucks -- three available in this project; only two will be used in the simulation
        self.truck1 = Truck(id=1, address_list=self.addresses, distance_matrix=self.distance_matrix)
        self.truck2 = Truck(id=2, address_list=self.addresses, distance_matrix=self.distance_matrix)
        self.truck3 = Truck(id=3, address_list=self.addresses, distance_matrix=self.distance_matrix)

        # package load order -- hardcoded for this project
        # first 16 is picked up by the first truck; second 16 by
        #   the second truck, etc.
        self.package_load_order = [
            '1', '6', '11', '14', '15', '16', '17', '19', '20', '21', '22', '24', '26', '31', '34', '40',  # trip 1
            '2', '3', '5', '7', '8', '10', '13', '18', '27', '29', '30', '35', '36', '37', '38', '39',     # trip 2
            '4', '12', '23', '25', '28', '32', '33', None, None, None, None, None, None, None, None, None, # trip 3
            '9',                                                                                           # trip 4
        ]

        # a priority queue will hold the simulation events; i.e. truck leaves HUB or truck delivers package
        # priority queue will be ordered by the simulation time, or how many minutes since the start of the day
        self.events = queue.PriorityQueue()

        # set the simulation start and end times
        self.simulation_start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        self.simulation_end_time = self._prompt_for_end_time()


    def _load_distance_matrix(self, filepath):
        """Read the given file for a matrix of distances between delivery
        locations. Return a two-dimensional array of distances.
        """

        # distance matrix will be implemented as a list of lists, or a 2d array
        distance_matrix = []
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)

            # package addresses are taken from the CSV's first row, ignoring the first field
            self.addresses = next(reader)[1:]

            # for every row after the header, append a list of values excluding the first value (address)
            distance_matrix.extend(row[1:] for row in reader)

        return distance_matrix

    def _load_packages(self, filepath):
        """Read the given file for a list of packages to be delivered, and
        load each package into a hash table.
        """

        # package data will be stored in our custom hash table
        package_hash = HashTable()
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # create a Package instance to store in the hash table
                package = Package(
                    row["Package ID"],
                    row["Address"],
                    "UT",
                    row["Zip"],
                    row["Weight KILO"],
                    row["Delivery Deadline"],
                )

                # the package ID serves as the hash table entry's key
                package_hash.insert(package.id, package)

        return package_hash
    
    def _prompt_for_end_time(self):
        """Prompt the user for the time the simulation should end. 5:00pm by default."""

        print("Enter simulation stop time [5:00 PM]", end=" >> ")
        user_input = input()

        # set time to 5:00 PM by default
        if user_input == "":
            stop_time = datetime.strptime("5:00 PM", "%I:%M %p")
        else:
            # create a datetime instance from the user's input
            try:
                stop_time = datetime.strptime(user_input, "%I:%M %p")
            except ValueError:  # invalid input time
                print("\nInvalid format: please use the format '%I:%M %p', like 10:35 AM\n")
                return self._prompt_for_end_time()

        stop_datetime = datetime.today().replace(
            hour=stop_time.hour,
            minute=stop_time.minute,
            second=0,
            microsecond=0,
        )

        # make sure the end time is on or after the start time
        if stop_datetime < self.simulation_start_time:
            print("\nPlease enter a time after 8:00 AM\n")
            return self._prompt_for_end_time()

        print("\n")
        return stop_datetime

    def load_truck(self, truck, package_list):
        """Load the given truck with a group of packages."""

        # logic for loading a single package onto a truck is contained
        #   in the Truck class definition
        for package_id in package_list:
            truck.load_package(package_id, self.packages)

    def prep_delivery(self, truck):
        """Prepare a delivery trip by loading packages onto a truck and
        plotting the delivery route.
        """

        # clear out the previous route and list of loaded packages
        truck.route = []
        truck.packages = []

        # load the first 16 packages from our package load order
        # 16 = truck maximum capacity
        self.load_truck(truck, self.package_load_order[:16])
        # remove these packages from our load order
        del self.package_load_order[:16]

        # plot the route that should be taken to deliver all loaded packages
        truck.plot_delivery_route(self.packages)

    def run(self):

        # prepare a new delivery for each of our available trucks
        self.prep_delivery(self.truck1)
        self.prep_delivery(self.truck2)

        # an active delivery is a Truck.deliver_packages() coroutine
        active_deliveries = []

        # starting the day at 8:00 AM
        start_time = self.simulation_start_time

        # append package delivery coroutines to our list of active deliveries
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

        # queue up the first event in each of our active delivery coroutines
        for delivery_proc in active_deliveries:
            self.events.put(next(delivery_proc))

        # simulation event loop -- processes events queued up in our events priority queue
        total_distance_traveled = 0
        simulation_time = start_time
        while simulation_time < self.simulation_end_time:

            # no more events; simulation finished before EOD (5:00 PM)
            if self.events.empty():
                break

            # pop an event from our events priority queue to be processed
            current_event = self.events.get()
            
            # add the distance traveled in this event to our running total
            simulation_time, truck_id, distance, previous_action = current_event
            total_distance_traveled += distance

            # print(f"Truck: {truck_id} -- {current_event}")

            # determine which truck this delivery event belongs to
            if truck_id == 1:
                active_truck = self.truck1
                active_delivery = active_deliveries[0]
            elif truck_id == 2:
                active_truck = self.truck2
                active_delivery = active_deliveries[1]

            # if a truck has returned to the HUB and there are still packages
            #   which need to be delivered, load up the packages and start a
            #   new delivery
            if (previous_action == "Returned to the HUB"
                and not len(active_truck.packages)
                and len(self.package_load_order)):

                # prepare a new delivery with our active truck
                self.prep_delivery(active_truck)

                # create a new active delivery coroutine
                new_delivery = active_truck.deliver_packages(
                    self.packages,
                    start_time=simulation_time,
                )

                if truck_id == 1:
                    delivery_index = 0
                elif truck_id == 2:
                    delivery_index = 1

                # queue up the new delivery coroutine's first event
                active_deliveries[delivery_index] = new_delivery
                self.events.put(next(new_delivery))

            # try to get a new event from our active delivery and queue it up
            # also, send the current simulation time to the delivery coroutine
            try:
                next_event = active_delivery.send(simulation_time)
            except StopIteration:
                pass
            else:
                self.events.put(next_event)

        # print the total milage traveled by all trucks
        end_time = max([simulation_time, self.simulation_end_time]).strftime("%I:%M %p")

        print("Simulation ended at:", end_time)
        print(f"Distance travelled: {total_distance_traveled:.2f} mi")

        # print the status of all packages
        print("\nAll packages:")
        self.packages.print_all()


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    # ascii art from https://ascii-generator.site/t/
    # font: "slant"
    title = """
 _       __   ______   __  __    ____    _____
| |     / /  / ____/  / / / /   / __ \  / ___/
| | /| / /  / / __   / / / /   / /_/ /  \__ \ 
| |/ |/ /  / /_/ /  / /_/ /   / ____/  ___/ / 
|__/|__/   \____/   \____/   /_/      /____/  
                                              
    """

    print(title)

    program = Simulation(
        distances_path="./data/distances.csv",
        packages_path="./data/packages.csv",
    )

    program.run()
