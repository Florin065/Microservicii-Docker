import requests

BASE_URL = "http://localhost:5000/api"


def test_add_country():
    response = requests.post(
        f"{BASE_URL}/countries",
        json={"name": "Romania", "lat": 45.9432, "long": 24.9668},
    )
    assert response.status_code == 201


def test_get_countries():
    response = requests.get(f"{BASE_URL}/countries")
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())  # Parsează și afișează conținutul JSON
    assert response.status_code == 200


    # data = response.json()
    # assert any(country["name"] == "Romania" for country in data)
