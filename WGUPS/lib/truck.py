"""Class definition of a truck. A truck holds packages and can deliver
packages to their addresses. The delivery route is plotted with the nearest
neighbor algorithm.
"""


class Truck:

    def __init__(self, id):

        self.id = id

        self.speed = 18  # avg 18 mph
        self.capacity = 16

        self.packages = []
        self.route = []

    def __repr__(self):

        return f"<Truck {self.id}, load={len(self.packages)}, cap={self.capacity}>"

    def load_package(self, package_id):
        """Load a package onto the truck for delivery."""

        if len(self.packages) <= self.capacity:
            self.packages.append(package_id)
        else:
            # truck is full; cannot load another package
            return False

    def plot_delivery_route(self, package_table):
        """Plot a delivery route to deliver all loaded packages."""

        # load addresses which we'll deliver to
        unvisited_addr = []
        for pkg_id in self.packages:
            
            package = package_table.lookup(pkg_id)
            unvisited_addr.append(package.address)

        print(unvisited_addr)


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    truck = Truck(id=1)
    another_truck = Truck(id=2)

    print(truck)
    print(another_truck)
