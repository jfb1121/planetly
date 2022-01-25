import datetime
import mongoengine_goodjson as gj
from mongoengine import StringField, DateField, DateTimeField, FloatField


class TemperatureReading(gj.Document):
    city_name = StringField(required=True)
    recording_date = DateField(required=True)
    average_temperature = FloatField(reqired=True)
    average_temperature_uncertainty = FloatField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField()
    meta = {
        'indexes': [
            {'fields': ('city_name', 'recording_date'), 'unique': True}
        ]
    }
