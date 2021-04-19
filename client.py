import requests
import data_gen
import time
from threading import Timer
import socketio
import eventlet, random

url = "http://127.0.0.1:8000/"
eventlet.monkey_patch()
sio = socketio.Client()
sio.connect('http://localhost:8000', namespaces=['/communication'])


@sio.event(namespace='/communication')
def message(data):
    print("End com: ", data)
    d = {"driver": data[1], "rating": random.randint(1, 5), "number": 1}
    r = requests.post(url + "/rating", json=d)
    # write to db


def driver_request():
    driver = data_gen.get_random_driver()
    print("Driver:", driver)
    r = requests.post(url + "/driver", json=driver)


def rider_request():
    rider = data_gen.get_random_rider()
    print("Rider:", rider)
    r = requests.post(url + "/rider", json=rider)


for i in range(100):
    print("Case:", i + 1)
    flag = random.randint(0, 9)
    # arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19]
    # arr = random.shuffle(arr)
    # arr = random.shuffle(arr)
    # arr = random.shuffle(arr)
    # arr = [1, 10, 20]
    # flag = arr[i % len(arr)]
    if flag < 6:
        Timer(1.0, driver_request).start()
    else:
        Timer(1.0, rider_request).start()

    time.sleep(1)
time.sleep(1000)
