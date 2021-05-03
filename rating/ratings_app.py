from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import json

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'ratings',
    'host': 'mongodb',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Rating(db.Document):
    driver_name = db.StringField()
    rating = db.StringField()
    def to_json(self):
        return {"driver_name": self.driver_name,
                "rating": self.rating}


@app.route('/api/rating', methods=['POST'])
def ratings():
    data = request.json
    x = json.loads(data)
    rat = Rating(driver_name=x['driver_name'],
                rating=str(x['rating']))
    rat.save()
    print('doneeeee')
    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)
