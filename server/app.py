import time

import eventlet
import requests
from flask import Flask, request
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import os

eventlet.monkey_patch()
app = Flask(__name__)
scheduler = APScheduler()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
region = os.environ.get('REGION')
# region = "wololo"

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


@app.route('/driver', methods=['POST'])
def driver():
    data = request.json
    drivers.append(data)
    return data


@app.route('/rider', methods=['POST'])
def rider():
    data = request.json
    riders.append(data)
    return data


@app.route('/try', methods=['GET'])
def baka():
    return "Sussy Baka\n"


@app.route('/')
def index():
    print("Received request!!!!!!!!!!")
    return 'Hellodd!'


@app.route('/d')
def index2():
    print("Received request!!!!!!!!!!")
    return 'DIE DIE DIE!'


def find_a_driver():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    if len(drivers) > 0 and len(riders) > 0:
        data, distance = rider_services(riders[0])
        js = {"0": riders[0]['name'], "1": data['name'], "2": round(distance * 2)}
        print("Trying request")
        print("http://" + region + ".communication.com:5500/")
        requests.post("http://" + region + ".communication.com:5500/", json=js)
        # requests.post("http://dinajpur.communication.com:5500/", json=js)
        # requests.post("http://127.0.0.1:5500/", json=js)
        # socketio.emit('message', [riders[0]['name'], data['name'], round(distance * 2)], namespace='/communication')
        riders.pop(0)

    # elif len(riders) > 1:
    #     riders[0], riders[len(riders)-1] = riders[len(riders)-1], riders[0]


if __name__ == '__main__':
    # scheduler.add_job(id='Schedule task', func=find_a_driver, trigger='interval', seconds=5)
    # scheduler.start()
    # # app.run(port=8000)
    # socketio.run(app, port=8000)

    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(func=find_a_driver, trigger="interval", seconds=5)
    scheduler.start()
    socketio.run(app, port=8000, host="0.0.0.0")
