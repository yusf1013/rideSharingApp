import time

import eventlet
from flask import Flask, request
# from flask_apscheduler import APScheduler
from flask_socketio import SocketIO

eventlet.monkey_patch()
app = Flask(__name__)
# scheduler = APScheduler()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

drivers = []
riders = []


def dist(p1, p2):
    p1 = str(p1).split(",")
    p2 = str(p2).split(",")
    return pow(pow(int(p1[0]) - int(p2[0]), 2) + pow(int(p1[1]) - int(p2[1]), 2), 0.5)


def find_best_driver(rider):
    selected_driver = None
    selected_dist = 10000000

    for driver in drivers:
        this_dist = dist(driver['location'], rider['source'])
        if this_dist < selected_dist:
            selected_driver = driver
            selected_dist = this_dist

    return selected_driver, selected_dist


def rider_services(data):
    selected_driver, distance = find_best_driver(data)
    return selected_driver, distance


@app.route('/try', methods=['GET'])
def baka():
    return "Sussy Baka com\n"


@app.route('/', methods=['POST', 'GET'])
def index():
    data = request.json
    print("Data: ", data)
    socketio.emit('message', [data["0"], data["1"], data["2"]], namespace='/communication')
    return 'Hellodd!'


def find_a_driver():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    if len(drivers) > 0 and len(riders) > 0:
        data, distance = rider_services(riders[0])
        socketio.emit('message', [riders[0]['name'], data['name'], round(distance * 2)], namespace='/communication')
        riders.pop(0)

    # elif len(riders) > 1:
    #     riders[0], riders[len(riders)-1] = riders[len(riders)-1], riders[0]


if __name__ == '__main__':
    socketio.run(app, port=5500, host="0.0.0.0")
