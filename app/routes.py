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

country_schema_update = {
    'id': {
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

city_schema_update = {
    'id': {
        'type': 'integer',
        'required': True
    },
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

temperature_schema_update = {
    'id': {
        'type': 'integer',
        'required': True
    },
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
validator_countries_update = cerberus.Validator(country_schema_update)
validator_cities = cerberus.Validator(city_schema)
validator_cities_update = cerberus.Validator(city_schema_update)
validator_temperatures = cerberus.Validator(temperature_schema)
validator_temperatures_update = cerberus.Validator(temperature_schema_update)


def generate_sequence(collection_name):
    sequence = db.counters.find_one_and_update(
        {'_id': collection_name},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=True
    )
    return sequence['seq']


# ------------- ROUTE: /api/countries ----------------


@app.route('/api/countries', methods=['POST'])
def add_country():
    data = request.json

    is_valid = validator_countries.validate(data)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': validator_countries.errors}), 400

    country = {
        '_id': generate_sequence('countries'),
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    try:
        db.countries.insert_one(country)
        return jsonify({'id': country['_id']}), 201
    except Exception as e:
        return jsonify({'error': f"Database conflict: {str(e)}"}), 409


@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = list(db.countries.find())

    for country in countries:
        country['id'] = country['_id']
        del country['_id']

    return jsonify(countries), 200


@app.route('/api/countries/<int:id>', methods=['PUT'])
def update_country(id):
    data = request.json

    is_valid = validator_countries_update.validate(data)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': validator_countries_update.errors}), 400

    update_data = {
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    try:
        result = db.countries.update_one({'_id': id}, {'$set': update_data})
        if result.matched_count == 0:
            return jsonify({'error': 'Country not found'}), 404
        return jsonify({'message': 'Country updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': f"Database conflict: {str(e)}"}), 409


@app.route('/api/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
    if id <= 0:
        return jsonify({'error': 'Invalid ID format. ID must be a positive integer'}), 400

    result = db.countries.delete_one({'_id': id})
    if result.deleted_count == 0:
        return jsonify({'error': 'Country not found'}), 404

    return jsonify({'message': 'Country deleted successfully'}), 200


# ------------- ROUTE: /api/cities ----------------


@app.route('/api/cities', methods=['POST'])
def add_city():
    data = request.json

    is_valid = validator_cities.validate(data)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': validator_cities.errors}), 400

    country_exists = db.countries.find_one({'_id': data['idTara']})
    if not country_exists:
        return jsonify({'error': 'Country not found'}), 404

    city = {
        '_id': generate_sequence('cities'),
        'idTara': data['idTara'],
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    try:
        db.cities.insert_one(city)
        return jsonify({'id': city['_id']}), 201
    except Exception as e:
        return jsonify({'error': f"Database conflict: {str(e)}"}), 409


@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = list(db.cities.find())

    for city in cities:
        city['id'] = city['_id']
        del city['_id']

    return jsonify(cities), 200


@app.route('/api/cities/country/<int:id_Tara>', methods=['GET'])
def get_cities_by_country(id_Tara):
    if not db.countries.find_one({'_id': id_Tara}):
        return jsonify([]), 200

    cities = list(db.cities.find({'idTara': id_Tara}))
    for city in cities:
        city['id'] = city['_id']
        del city['_id']
    return jsonify(cities), 200


@app.route('/api/cities/<int:id>', methods=['PUT'])
def update_city(id):
    data = request.json

    is_valid = validator_cities_update.validate(data)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': validator_cities_update.errors}), 400

    update_data = {
        'idTara': data['idTara'],
        'nume': data['nume'],
        'lat': data['lat'],
        'lon': data['lon']
    }

    try:
        result = db.cities.update_one({'_id': id}, {'$set': update_data})
        if result.matched_count == 0:
            return jsonify({'error': 'City not found'}), 404
        return jsonify({'message': 'City updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': f"Database conflict: {str(e)}"}), 409


@app.route('/api/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    if id <= 0:
        return jsonify({'error': 'Invalid ID format. ID must be a positive integer'}), 400

    result = db.cities.delete_one({'_id': id})
    if result.deleted_count == 0:
        return jsonify({'error': 'City not found'}), 404

    return jsonify({'message': 'City deleted successfully'}), 200


# ------------- ROUTE: /api/temperatures ----------------


@app.route('/api/temperatures', methods=['POST'])
def add_temperature():
    data = request.json

    is_valid, errors = validate_temperature_input(data, temperature_schema)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    city_exists = db.cities.find_one({'_id': data['idOras']})
    if not city_exists:
        return jsonify({'error': 'City not found'}), 404

    temperature = {
        '_id': ObjectId(),
        'idOras': data['idOras'],
        'value': data['value'],
        'timestamp': data['timestamp']
    }

    try:
        result = db.temperatures.insert_one(temperature)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': f"Database conflict: {str(e)}"}), 409


@app.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    from_date = request.args.get('from')
    until_date = request.args.get('until')

    query = {}
    if lat:
        query['lat'] = lat
    if lon:
        query['lon'] = lon
    if from_date and until_date:
        query['timestamp'] = {'$gte': from_date, '$lte': until_date}
    elif from_date:
        query['timestamp'] = {'$gte': from_date}
    elif until_date:
        query['timestamp'] = {'$lte': until_date}

    temperatures = list(db.temperatures.find(query))
    for temperature in temperatures:
        temperature['id'] = str(temperature['_id'])
        del temperature['_id']
    return jsonify(temperatures), 200


@app.route('/api/temperatures/cities/<int:id_oras>', methods=['GET'])
def get_temperatures_by_city(id_oras):
    from_date = request.args.get('from')
    until_date = request.args.get('until')

    query = {'idOras': id_oras}
    if from_date and until_date:
        query['timestamp'] = {'$gte': from_date, '$lte': until_date}
    elif from_date:
        query['timestamp'] = {'$gte': from_date}
    elif until_date:
        query['timestamp'] = {'$lte': until_date}

    temperatures = list(db.temperatures.find(query))
    for temperature in temperatures:
        temperature['id'] = str(temperature['_id'])
        del temperature['_id']
    return jsonify(temperatures), 200


@app.route('/api/temperatures/countries/<int:id_tara>', methods=['GET'])
def get_temperatures_by_country(id_tara):
    from_date = request.args.get('from')
    until_date = request.args.get('until')

    cities = list(db.cities.find({'idTara': id_tara}))
    query = {'idOras': {'$in': [city['_id'] for city in cities]}}
    if from_date and until_date:
        query['timestamp'] = {'$gte': from_date, '$lte': until_date}
    elif from_date:
        query['timestamp'] = {'$gte': from_date}
    elif until_date:
        query['timestamp'] = {'$lte': until_date}

    temperatures = list(db.temperatures.find(query))
    for temperature in temperatures:
        temperature['id'] = str(temperature['_id'])
        del temperature['_id']
    return jsonify(temperatures), 200


@app.route('/api/temperatures/<string:id>', methods=['PUT'])
def update_temperature(id):
    data = request.json

    obj_id = validate_objectid(id)
    is_valid, errors = validate_temperature_input(data, temperature_schema_update)
    if not is_valid:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    update_data = {
        'idOras': data['idOras'],
        'value': data['value'],
        'timestamp': data['timestamp']
    }

    result = db.temperatures.update_one({'_id': obj_id}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'Temperature not found'}), 404
    return jsonify({'message': 'Temperature updated successfully'}), 200


@app.route('/api/temperatures/<string:id>', methods=['DELETE'])
def delete_temperature(id):
    obj_id = validate_objectid(id)
    result = db.temperatures.delete_one({'_id': obj_id})
    if result.deleted_count == 0:
        return jsonify({'error': 'Temperature not found'}), 404

    if not obj_id:
        return jsonify({'error': 'Invalid ID format'}), 400

    return jsonify({'message': 'Temperature deleted successfully'}), 200
