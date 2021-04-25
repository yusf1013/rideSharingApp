from flask import Flask, request
import database

app = Flask(__name__)


@app.route('/rating', methods=['POST'])
def rating():
    data = request.json
    handle_rating(data)
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
    return 'Ratings page'


if __name__ == '__main__':
    app.run(port=5000)
