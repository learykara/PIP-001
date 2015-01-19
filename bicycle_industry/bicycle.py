# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# models the bicycle industry
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

from collections import defaultdict




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


