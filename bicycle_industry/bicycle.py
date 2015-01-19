# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# models the bicycle industry
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~


model_information = {
    'cruiser': {'weight': 100, 'production_cost': 150},
    'racer': {'weight': 80, 'production_cost': 250},
    'mountain': {'weight': 120, 'production_cost': 200},
    'huffy': {'weight': 90, 'production_cost': 125},
    'tandem': {'weight': 150, 'production_cost': 210},
    'schwinn': {'weight': 110, 'production_cost': 175}
}


class Bicycle(object):
    """Models a bicycle object"""
    def __init__(self, name):
        self.name = name
        self.weight = model_information[name]['weight']
        self.production_cost = model_information[name]['production_cost']


class BikeShop(object):
    """Models a bike shop"""
    def __init__(self, name, margin):
        self.name = name
        self.margin = margin
        self.profit = 0
        self.inventory = {}


class Customer(object):
    """Models a customer"""
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.bikes = {}

