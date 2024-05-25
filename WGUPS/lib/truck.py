"""Class definition of a truck. A truck holds packages and can deliver
packages to their addresses. The delivery route is plotted with the nearest
neighbor algorithm.
"""


class Truck:

    def __init__(self, id, address_list, distance_matrix):

        self.id = id

        # starting location is the HUB
        self.location = "4001 South 700 East, Salt Lake City, UT 84107"

        self.speed = 18  # avg 18 mph
        self.capacity = 16

        self.packages = []
        self.route = []

        self.address_list = address_list
        self.distance_matrix = distance_matrix

    def __repr__(self):

        return f"<Truck {self.id}, load={len(self.packages)}, cap={self.capacity}>"

    def load_package(self, package_id):
        """Load a package onto the truck for delivery."""

        if len(self.packages) <= self.capacity:
            self.packages.append(package_id)
        else:
            # truck is full; cannot load another package
            return False

    def lookup_distance(self, from_address, to_address):
        """Lookup the distance between the two addresses."""

        from_address_full = [addr for addr in self.address_list
                             if from_address in addr][0]
        to_address_full = [addr for addr in self.address_list
                             if to_address in addr][0]
        
        from_address_index = self.address_list.index(from_address_full)
        to_address_index = self.address_list.index(to_address_full)

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
            unvisited_addr.append(package.address)

        distance_traveled = 0

        location = self.location
        while len(unvisited_addr) > 0:
            next_address = None
            min_distance = float("inf")

            for address in unvisited_addr:
                distance = self.lookup_distance(location, address)
                if distance < min_distance:
                    min_distance = distance
                    next_address = address
            
            self.route.append(next_address)
            unvisited_addr.pop(
                unvisited_addr.index(next_address)
            )
            location = next_address
            distance_traveled += min_distance

        # return to hub after packages are delivered
        self.route.append("4001 South 700 East, Salt Lake City, UT 84107")
        distance_traveled += self.lookup_distance(
            location,
            "4001 South 700 East, Salt Lake City, UT 84107"
        )

        return distance_traveled


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    truck = Truck(id=1)
    another_truck = Truck(id=2)

    print(truck)
    print(another_truck)
