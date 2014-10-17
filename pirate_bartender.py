from random import choice


questions = {
    "strong": "Do ye like yer drinks strong?",
    "salty": "Do ye like it with a salty tang?",
    "bitter": "Are ye a lubber who likes it bitter?",
    "sweet": "Would ye like a bit of sweetness with yer poison?",
    "fruity": "Are ye one for a fruity finish?"
}

ingredients = {
    "strong": ["glug of rum", "slug of whisky", "splash of gin"],
    "salty": ["olive on a stick", "salt-dusted rim", "rasher of bacon"],
    "bitter": ["shake of bitters", "splash of tonic", "twist of lemon peel"],
    "sweet": ["sugar cube", "spoonful of honey", "spash of cola"],
    "fruity": ["slice of orange", "dash of cassis", "cherry on top"]
}

drink_nouns = [
    'booty',
    'buccaneer',
    'kraken',
    'parrot',
    'seadog',
    'swabbie',
    'treasure'
]

def valid_response(resp):
    """Validates the response entered
    
    :param resp: the response entered in the console
    """
    if resp.lower() in ('y', 'yes'):
        return True
    elif resp.lower() in ('n', 'no'):
        return False
    return None

def get_customer_tastes():
    """Returns a ``dict`` indicating a customer's tastes"""
    tastes = {} 
    for question in questions:
        response = valid_response(raw_input(questions[question] + ': '))
        while response is None:
            print('Please enter a valid response (y/yes, n/no)')
            response = valid_response(raw_input(questions[question] + ': '))
        tastes[question] = response
    return tastes

def construct_drink(tastes):
    """Returns a ``list`` representing a drink
    
    :param tastes: a ``dict`` indicating the customer's tastes
    """
    drink = [
        choice(
            ingredients[item]) for item in tastes if tastes[item] is True]
    return drink

def construct_drink_name(tastes):
    """Return the name of a drink, based on preferred tastes and a 
    random noun
    
    :param tastes: a ``dict`` indicateing the customer's tastes
    """
    noun = choice(drink_nouns)
    adj = choice([k for k in tastes if tastes[k] is True])
    return adj + ' ' + noun


if __name__ == '__main__':
    have_another = True
    while have_another:
        tastes = get_customer_tastes()
        drink = construct_drink(tastes)
        drink_name = construct_drink_name(tastes)
        print 'You get the {} (ingredients: {}). Enjoy!'.format(
            drink_name, drink)
        have_another = valid_response(raw_input('Would you like another?: '))

