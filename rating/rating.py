import json

from flask import Flask, request
import database

app = Flask(__name__)


@app.route('/rating', methods=['POST'])
def rating():
    print("YOYOYO in")
    data = request.json
    r = handle_rating(data)
    return r


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

    print(db_driver)
    if data and '_id' in data.keys():
        del data['_id']

    if db_driver and '_id' in db_driver.keys():
        del db_driver['_id']

    dic = '{ "Old data": ' + json.dumps(db_driver) + ', "New data": ' + json.dumps(data) + ' }'
    response = app.response_class(
        response=dic,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/')
def index():
    print("Received request!!!!!!!!!!")
    return 'Ratings page'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
