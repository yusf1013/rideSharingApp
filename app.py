import time
from flask_socketio import SocketIO
from flask import Flask, request
from threading import Timer
from flask_apscheduler import APScheduler
import eventlet
import database

import atexit

app = Flask(__name__)
eventlet.monkey_patch()
scheduler = APScheduler()
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


@socketio.on('message')
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


@app.route('/rating', methods=['POST'])
def rating():
    data = request.json

    handle_rating(data)
    # try:
    #     handle_rating(data)
    # except:
    #     print("Error!", data)

    return "Done!"


def handle_rating(data):
    print("Rating:", data)
    to_find = {'driver': data['driver']}
    db_driver = database.find_from_database("ride_sharing_app", "ratings", to_find)
    if db_driver is None:
        print("In if: ", data)
        database.insert_into_database("ride_sharing_app", "ratings", data)

    else:
        print("In else: ", data)
        print(type(db_driver['number']))
        n = db_driver['number'] + 1
        rate = (db_driver['number'] * db_driver['rating'] + data['rating']) / n
        data['number'] = n
        data['rating'] = rate
        print("End else: ", data)
        database.update_database("ride_sharing_app", "ratings", to_find, data)
    return data


@app.route('/')
def index():
    print("Received request!!!!!!!!!!")
    socketio.emit('message', ["HI", "Bye"], namespace='/communication')
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
    scheduler.add_job(id='Schedule task', func=find_a_driver, trigger='interval', seconds=5)
    scheduler.start()
    socketio.run(app, port=8000)
