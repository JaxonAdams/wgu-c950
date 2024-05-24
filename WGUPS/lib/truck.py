"""Class definition of a truck. A truck holds packages and can deliver
packages to their addresses. The delivery route is plotted with the nearest
neighbor algorithm.
"""


class Truck:

    def __init__(self, id):

        self.id = id

        self.speed = 18  # avg 18 mph
        self.capacity = 16
    
    def __repr__(self):

        return f"<Truck {self.id}>"


# !---------------------------------------------------------------------------
if __name__ == "__main__":

    truck = Truck(id=1)
    another_truck = Truck(id=2)

    print(truck)
    print(another_truck)
