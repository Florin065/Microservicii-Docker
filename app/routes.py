from bson import ObjectId, errors as bson_errors
from flask import jsonify, request
from app import app, db
import cerberus

country_schema = {
    'nume': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'lat': {
        'type': 'float',
        'required': True,
    },
    'lon': {
        'type': 'float',
        'required': True,
    }
}

city_schema = {
    'idTara': {
        'type': 'integer',
        'required': True
    },
    'nume': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'lat': {
        'type': 'float',
        'required': True,
    },
    'lon': {
        'type': 'float',
        'required': True,
    }
}

temperature_schema = {
    'idOras': {
        'type': 'integer',
        'required': True
    },
    'value': {
        'type': 'float',
        'required': True
    },
    'timestamp': {
        'type': 'datetime',
        'required': True
    }
}

validator_countries = cerberus.Validator(country_schema)
validator_cities = cerberus.Validator(city_schema)
validator_temperatures = cerberus.Validator(temperature_schema)


def validate_objectid(id_str):
    try:
        return ObjectId(id_str)
    except bson_errors.InvalidId:
        return None


def validate_country_input(data, schema):
    if not validator_countries.validate(data, schema):
        return False, validator_countries.errors
    return True, None


def validate_city_input(data, schema):
    if not validator_cities.validate(data, schema):
        return False, validator_cities.errors
    return True, None


@app.route('/api/countries', methods=['POST'])
def add_country():
    data = request.json

    is_valid, errors = validate_country_input(data, country_schema)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    country = {
        '_id': ObjectId(),
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    try:
        result = db.countries.insert_one(country)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': f"Database conflict: {str(e)}"}), 409


@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = list(db.countries.find())
    for country in countries:
        country['id'] = str(country['_id'])
        del country['_id']
    return jsonify(countries), 200


@app.route('/api/countries/<string:id>', methods=['PUT'])
def update_country(id):
    data = request.json

    obj_id = validate_objectid(id)
    is_valid, errors = validate_country_input(data, country_schema)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    update_data = {
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    result = db.countries.update_one({'_id': obj_id}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'Country not found'}), 404
    return jsonify({'message': 'Country updated successfully'}), 200


@app.route('/api/countries/<string:id>', methods=['DELETE'])
def delete_country(id):
    obj_id = validate_objectid(id)
    result = db.countries.delete_one({'_id': obj_id})
    if result.deleted_count == 0:
        return jsonify({'error': 'Country not found'}), 404

    if not obj_id:
        return jsonify({'error': 'Invalid ID format'}), 400

    return jsonify({'message': 'Country deleted successfully'}), 200


@app.route('/api/cities', methods=['POST'])
def add_city():
    data = request.json

    is_valid, errors = validate_city_input(data, city_schema)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    city = {
        '_id': ObjectId(),
        'idTara': data['idTara'],
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    try:
        result = db.cities.insert_one(city)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': f"Database conflict: {str(e)}"}), 409


@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = list(db.cities.find())
    for city in cities:
        city['id'] = str(city['_id'])
        del city['_id']
    return jsonify(cities), 200


@app.route('/api/cities/country/<int:id_Tara>', methods=['GET'])
def get_cities_by_country(id_Tara):
    exist = db.countries.find_one({'_id': id_Tara})
    if not exist:
        return jsonify([]), 200

    cities = list(db.cities.find({'idTara': id_Tara}))
    for city in cities:
        city['id'] = str(city['_id'])
        del city['_id']
    return jsonify(cities), 200


@app.route('/api/cities/<string:id>', methods=['PUT'])
def update_city(id):
    data = request.json

    obj_id = validate_objectid(id)
    is_valid, errors = validate_city_input(data, city_schema)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    update_data = {
        'idTara': data['idTara'],
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    result = db.cities.update_one({'_id': obj_id}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'message': 'City updated successfully'}), 200


@app.route('/api/cities/<string:id>', methods=['DELETE'])
def delete_city(id):
    obj_id = validate_objectid(id)
    result = db.cities.delete_one({'_id': obj_id})
    if result.deleted_count == 0:
        return jsonify({'error': 'City not found'}), 404

    if not obj_id:
        return jsonify({'error': 'Invalid ID format'}), 400

    return jsonify({'message': 'City deleted successfully'}), 200
