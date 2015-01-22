
from bicycle import Bicycle, BikeShop, Customer, bicycle_model_information


# Instantiate Bicycle Objects
cruiser = Bicycle('cruiser')
racer = Bicycle('racer')
mountain = Bicycle('mountain')
huffy = Bicycle('huffy')
tandem = Bicycle('tandem')
schwinn = Bicycle('schwinn')


# Instantiate Bike Shop Object and fill inventory
bike_shop = BikeShop('Mike\'s Bikes', 20)

bike_shop_inventory = {
    cruiser: 2,
    racer: 4,
    mountain: 3,
    huffy: 6,
    tandem: 1,
    schwinn: 2
}

for model in bike_shop_inventory:
    bike_shop.stock_inventory(model, bike_shop_inventory[model])


# Instantiate Customers
customer_1 = Customer('Joe', 200)
customer_2 = Customer('Jane', 500)
customer_3 = Customer('John', 1000)

customers = [customer_1, customer_2, customer_3]


# Print customer name and affordable bikes
print 'Printing customers and purchasable bikes'
for customer in customers:
    print customer.name, customer.affordable_bikes(bike_shop)


# Print the initial inventory of the bike shop
print "Initial inventory of {}".format(bike_shop.name)
print [
    "Model: {}, Count: {}".format(bike.name, bike_shop.inventory[bike])
    for bike in bike_shop.inventory]

customer_1.purchase_bike(cruiser, bike_shop)
customer_2.purchase_bike(racer, bike_shop)
customer_3.purchase_bike(tandem, bike_shop)


# Print the remaining inventory and profit of the bike shop
print '{}\'s remaining inventory:'.format(bike_shop.name)
print [(bike.name, bike_shop.inventory[bike]) for bike in bike_shop.inventory]

print '{}\'s profit:'.format(bike_shop.name)
print '${}'.format(bike_shop.profit)

