"""Class definition of a truck. A truck holds packages and can deliver
packages to their addresses. The delivery route is plotted with the nearest
neighbor algorithm.
"""


import collections
from datetime import datetime, timedelta


Event = collections.namedtuple("Event", "time truck_id dist_travelled action")


class Truck:

    def __init__(self, id, address_list, distance_matrix):

        self.id = id

        # starting location is the HUB
        self.hub_address = "4001 South 700 East, Salt Lake City, UT 84107"
        self.location = "4001 South 700 East, Salt Lake City, UT 84107"

        self.speed = 18  # avg 18 mph
        self.capacity = 16

        self.packages = []
        self.route = []

        self.address_list = address_list
        self.distance_matrix = distance_matrix

    def __repr__(self):

        return f"<Truck {self.id}, load={len(self.packages)}, cap={self.capacity}>"

    def load_package(self, package_id, package_table, trip_num):
        """Load a package onto the truck for delivery."""

        if len(self.packages) <= self.capacity and package_id is not None:
            self.packages.append(package_id)
            
            # update package status
            package = package_table.lookup(package_id)
            package.status = f"EN ROUTE"
            package.truck = self.id
            package.trip_number = trip_num

            # package #9 (incorrect address) -- update to correct address when loaded
            if package_id == "9":
                package.address = "410 S State St"
        else:
            # truck is full; cannot load another package
            return False

    def lookup_distance(self, from_address, to_address):
        """Lookup the distance between the two addresses."""

        # fetch the full addresses from our address list
        from_address_full = [addr for addr in self.address_list
                             if from_address in addr][0]
        to_address_full = [addr for addr in self.address_list
                           if to_address in addr][0]

        # get the index of each address
        from_address_index = self.address_list.index(from_address_full)
        to_address_index = self.address_list.index(to_address_full)

        # lookup the distance between the two addresses in our distance matrix
        distance = self.distance_matrix[from_address_index][to_address_index]
        if distance == "":
            distance = self.distance_matrix[to_address_index][from_address_index]

        return float(distance)

    def plot_delivery_route(self, package_table):
        """Plot a delivery route to deliver all loaded packages."""

        # load addresses which we'll deliver to
        unvisited_addr = []
        for pkg_id in self.packages:
            package = package_table.lookup(pkg_id)
            unvisited_addr.append((pkg_id, package.address))

        # we'll use this to calculate a running total of miles traveled
        distance_traveled = 0

        # start at the current location; usually the HUB
        location = self.location

        # run as long as there are addresses to visit
        while len(unvisited_addr) > 0:
            next_address = None
            min_distance = float("inf")
            next_pkg_id = None

            # check each unvisited address for the closest one to the current location
            for pkg_id, address in unvisited_addr:
                distance = self.lookup_distance(location, address)
                if distance < min_distance:
                    min_distance = distance
                    next_address = address
                    next_pkg_id = pkg_id
            
            # add the closest address to the route
            self.route.append((next_address, min_distance, next_pkg_id))
            unvisited_addr.pop(
                unvisited_addr.index((next_pkg_id, next_address))
            )

            # travel to the closest address and begin again
            location = next_address
            distance_traveled += min_distance

        # return to hub after packages are delivered
        dist_to_hub = self.lookup_distance(
            location,
            self.hub_address,
        )
        distance_traveled += dist_to_hub

        # return the calculated distance traveled
        # the truck hasn't actually dropped off any packages, this is just a prediction for testing purposes
        return distance_traveled

    def deliver_packages(self, package_table, start_time=datetime.now().replace(hour=8, minute=0)):
        """Deliver packages by visiting each address in the plotted route.
        Yield to the simulator issuing events to allow other trucks to deliver
        packages as well.
        """

        # this function is a coroutine; it pauses and resumes to allow other processes
        #   to run concurrently. It is driven by the Simulation class in main.py.

        # each time execution pauses, we send out a new Event (i.e. delivering a package at a certain time).
        # we get back the current simulation time when execution resumes.

        # first event: starting our route by leaving the HUB once packages are loaded
        time = yield Event(start_time, self.id, 0, "Leaving the HUB")

        # follow the route plotted by the plot_delivery_route() method
        for address, distance, pkg_id in self.route:

            # calculate the time it takes to drive to the next address
            time_to_address =  timedelta(minutes=(distance / self.speed * 60))
            
            # advance simulation time to when we reach the new address
            new_sim_time = time + time_to_address
            self.location = address

            # if we're dropping off a package at this new address...
            if pkg_id is not None:

                # handle package delivery by updating the package status and removing it
                #   from the truck's list of loaded packages
                pkg = package_table.lookup(pkg_id)
                pkg.status = f"DELIVERED {datetime.strftime(new_sim_time, '%H:%M %p')}"
                
                self.packages.pop(
                    self.packages.index(pkg_id)
                )
            
            # yield a new Event representing the truck dropping off a package
            time = yield Event(new_sim_time, self.id, distance, f"Dropped off package {pkg_id} at {address}")

        # return to the HUB
        dist_to_hub = self.lookup_distance(self.location, self.hub_address)
        time_to_hub = timedelta(minutes=(dist_to_hub / self.speed * 60))
        self.location = self.hub_address
        
        # yield a new Event representing returning to the HUB
        time = yield Event(time + time_to_hub, self.id, dist_to_hub, "Returned to the HUB")


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    truck = Truck(id=1)
    another_truck = Truck(id=2)

    print(truck)
    print(another_truck)
