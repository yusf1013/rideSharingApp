import random
import string
import string_utils

titles = ["Mr.", "Mrs.", "Ms.", "Dr.", "Miss", "Master", "Madam", "Sir", "Prof."]
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
               "Louise", "Rose", "Grace", "Jane", "Elizabeth", "Anne"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
              "Martinez", "Anserson", "Taylor", "Yeats", "Moore"]


def get_random_point():
    a = str(random.randint(0, 1000))
    b = str(random.randint(0, 1000))
    return a + "," + b


def get_random_rider():
    rider = {'name': get_random_name(), 'source': get_random_point(), 'destination': get_random_point()}
    return rider


def get_random_name():
    return random.choice(titles) + " " + random.choice(first_names) + " " + random.choice(
        string.ascii_uppercase) + ". " + random.choice(last_names)


def get_random_car_number():
    number = "ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789"
    number = string_utils.shuffle(number)
    return number[:5]


def get_random_driver():
    driver = {'name': get_random_name(), 'carNumber': get_random_car_number(), "location": get_random_point()}
    return driver
