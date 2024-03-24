from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database_name'
mongo = MongoClient(app.config['MONGO_URI'])

# Model for nutrition
class Nutrition:
    def __init__(self, serving_size, calories, fat, cholesterol, sodium, carbs, sugars, protein, ingredients, contains):
        self.serving_size = serving_size
        self.calories = calories
        self.fat = fat
        self.cholesterol = cholesterol
        self.sodium = sodium
        self.total_carbs = carbs
        self.sugars = sugars
        self.protein = protein
        self.ingredients = ingredients
        self.contains = contains

# Model for food items
class Food:
    def __init__(self, name, description, nutrition):
        self.name = name
        self.description = description
        self.nutrition = nutrition

# Model for stations
class Stations:
    def __init__(self, name, foods):
        self.name = name
        self.foods = foods

# Model for dining locations
class DiningLocation:
    def __init__(self, name, stations):
        self.name = name
        self.stations = stations

# Function to populate DiningLocation with a list of station names
def populate_dining_location_with_stations(dining_location, station_names):
    stations = []
    for name in station_names:
        station = Stations(name=name, foods=[])
        stations.append(station)
    dining_location.stations = stations

# Example usage
dining_location = DiningLocation(name='Example Dining Location', stations=[])
station_names = ['Station 1', 'Station 2', 'Station 3']
populate_dining_location_with_stations(dining_location, station_names)
# Route for adding foods to a station within a dining location
@app.route('/dining_locations/<location_id>/stations/<station_id>/foods', methods=['POST'])
def add_food_to_station(location_id, station_id):
    data = request.json
    nutrition_data = data['nutrition']
    nutrition = Nutrition(
        serving_size=nutrition_data['serving_size'],
        calories=nutrition_data['calories'],
        fat=nutrition_data['fat'],
        cholesterol=nutrition_data['cholesterol'],
        sodium=nutrition_data['sodium'],
        carbs=nutrition_data['carbs'],
        sugars=nutrition_data['sugars'],
        protein=nutrition_data['protein'],
        ingredients=nutrition_data['ingredients'],
        contains=nutrition_data['contains']
    )
    food = Food(
        name=data['name'],
        description=data['description'],
        nutrition=nutrition
    )
    station = mongo.db.dining_locations.find_one({'_id': location_id, 'stations._id': station_id}, {'stations.$': 1})['stations'][0]
    station['foods'].append(food.__dict__)
    mongo.db.dining_locations.update_one({'_id': location_id, 'stations._id': station_id}, {'$set': {'stations.$': station}})
    return jsonify({'message': 'Food added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
