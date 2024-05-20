"""Class definition of a package. A package object contains fields relevent to
the package delivery; i.e. delivery address, package weight, etc.
"""


class Package:

    # initialize instance attributes
    def __init__(self, package_id, address, city, zip, weight, deadline):

        self.id = package_id

        # delivery location
        self.address = address
        self.city = city
        self.zip = zip

        # other delivery information
        self.weight = weight
        self.deadline = deadline
        self.status = "AT THE HUB"

    
# !---------------------------------------------------------------------------
if __name__ == "__main__":

    pkg = Package(1, "123 Sesame Street", "Eagle Mountain", 84005, "3lbs", "12:30")
    print(pkg.address)
    print(pkg.deadline)
