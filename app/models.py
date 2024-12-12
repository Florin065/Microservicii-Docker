from mongoengine import Document, StringField, FloatField, IntField, ReferenceField, DateTimeField


class Country(Document):
    country_id = IntField(primary_key=True)
    country_name = StringField(required=True, unique=True)
    country_lat = FloatField(required=True)
    country_long = FloatField(required=True)


class City(Document):
    city_id = IntField(primary_key=True, required=True)
    city_name = StringField(required=True, unique=True)
    city_lat = FloatField(required=True)
    city_long = FloatField(required=True)
    country_id = ReferenceField(Country, required=True, unique=True)


class Temperature(Document):
    temperature_id = IntField(required=True, primary_key=True)
    value = FloatField(required=True)
    timestamp = DateTimeField(required=True, unique=True)
    city_id = ReferenceField(City, required=True, unique=True)
