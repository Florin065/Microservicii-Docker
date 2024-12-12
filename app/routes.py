from flask import Blueprint, request, jsonify
from .models import Country, City, Temperature

api = Blueprint("api", __name__)

# Variabila globală pentru ID-ul țării
country_id = 0

@api.route('/api/countries', methods=['POST'])
def add_country():
    global country_id  # Declarăm că vom folosi variabila globală

    # Obținem datele din body-ul cererii
    data = request.get_json()

    # Creăm obiectul Country cu un ID incrementat
    country = Country(
        country_id=country_id,
        country_name=data["name"],
        country_lat=data["lat"],
        country_long=data["long"]
    )

    # Salvăm țara în baza de date
    country.save()

    # Incrementăm `country_id` pentru următoarea țară
    country_id += 1

    return jsonify({"message": "Country added", "id": country_id - 1}), 201



@api.route('/api/countries', methods=['GET'])
def get_countries():
    print("GET /api/countries was called")
    return jsonify([]), 200
