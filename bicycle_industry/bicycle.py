# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# models the bicycle industry
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

from collections import defaultdict


bicycle_model_information = {
    'cruiser': {
        'weight': 120,
        'production_cost': 140,
        'wheel_model_name': 'standard',
        'frame_model_name': 'carbon'},
    'racer': {
        'weight': 80,
        'production_cost': 250,
        'wheel_model_name': 'racing',
        'frame_model_name': 'aluminum'},
    'mountain': {
        'weight': 140,
        'production_cost': 200,
        'wheel_model_name': 'mountain',
        'frame_model_name': 'steel'},
    'huffy': {
        'weight': 130,
        'production_cost': 180,
        'wheel_model_name': 'standard',
        'frame_model_name': 'steel'},
    'tandem': {
        'weight': 190,
        'production_cost': 210,
        'wheel_model_name': 'standard',
        'frame_model_name': 'tandem'},
    'schwinn': {
        'weight': 110,
        'production_cost': 240,
        'wheel_model_name': 'racing',
        'frame_model_name': 'steel'}
}

wheel_information = {
    'racing': {'weight': 20, 'production_cost': 60},
    'mountain': {'weight': 35, 'production_cost': 40},
    'standard': {'weight': 30, 'production_cost': 30}
}

frame_information = {
    'aluminum': {'weight': 40, 'production_cost': 130},
    'carbon': {'weight': 60, 'production_cost': 80},
    'steel': {'weight': 70, 'production_cost': 120},
    'tandem': {'weight': 130, 'production_cost': 150}
}


def valid_bicycle_spec(model_name, property):
    """Validates that the `property` of the bicycle is the sum of its parts

    :param model_name: a ``string`` representing the name of the bike model_name
    :param property: the property to be checked (weight or production_cost)
    """
    wheel_model = bicycle_model_information.get(
        model_name).get('wheel_model_name')
    frame_model = bicycle_model_information.get(
        model_name).get('frame_model_name')
    return (bicycle_model_information.get(model_name).get(property) ==
        wheel_information.get(wheel_model).get(property) * 2 +
        frame_information.get(frame_model).get(property))


class Bicycle(object):
    """Models a bicycle object"""
    def __init__(self, name):
        self.name = name
        self.weight = bicycle_model_information[name]['weight']
        self.production_cost = bicycle_model_information[name]['production_cost']


class BikeShop(object):
    """Models a bike shop"""
    def __init__(self, name, margin):
        self.name = name
        self.margin = margin
        self.profit = 0
        self.inventory = defaultdict(int)

    def stock_inventory(self, bike, num):
        """Add bikes to the store's inventory
        :param bike_model: the bicycle model to be added
        :param num: the number of bikes to be added
        """
        self.inventory[bike] += num

    def calc_sale_price(self, bike):
        return bike.production_cost*(1 + self.margin/100)


class Customer(object):
    """Models a customer"""
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.bikes = defaultdict(int)

    def affordable_bikes(self, bike_shop):
        return [
            bike.name for bike in bike_shop.inventory if
            bike_shop.calc_sale_price(bike) <= self.money]

    def purchase_bike(self, bike, bike_shop):
        sale_price = bike_shop.calc_sale_price(bike)
        if sale_price > self.money:
            print 'Failed transaction: {} cannot afford a {} bike'.format(
                self.name, bike.name)
            return
        if bike_shop.inventory[bike] < 1:
            print 'Failed transaction: bike {} is out of stock'.format(
                bike.name)
            return
        print 'Customer {} purchasing a {} bicycle for ${} from {}'.format(
            self.name, bike.name, sale_price, bike_shop.name)
        self.bikes[bike] += 1
        self.money -= sale_price
        bike_shop.inventory[bike] -= 1
        bike_shop.profit += sale_price
        print 'Transaction successful.'


class Wheel(object):
    """Models the bicycle wheels"""
    def __init__(self, model):
        self.model = model
        self.weight = wheel_information[model]['weight']
        self.production_cost = wheel_information[model]['production_cost']


class Frame(object):
    """Models the bicycle frame"""
    def __init__(self, material):
        self.material = material
        self.weight = frame_information[material]['weight']
        self.production_cost = frame_information[material]['production_cost']
