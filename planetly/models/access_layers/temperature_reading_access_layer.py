from datetime import datetime
from typing import Sequence

from planetly.exceptions import AccessLayerException
from planetly.models.temperature_reading import TemperatureReading
from mongoengine.errors import NotUniqueError, DoesNotExist
from mongoengine.errors import ValidationError


class TemperatureReadingAccessLayer:
    """
    Class responsible to abstract all the database logic with regards to the
    temperature reading model in the database.
    """

    def get_unique_cities(self, from_date=None, to_date=None) -> Sequence:
        """
        returns unique cities, for which at least one temperature is recorded.
        """
        query = self._apply_from_to_filter(from_date=from_date,
                                           to_date=to_date)
        cities = TemperatureReading.objects(query).distinct("city_name")
        if len(cities) == 0:
            return []

        return cities

    def create_temperature_reading(
        self,
        city_name: str,
        recording_date: str,
        average_temperature: float,
        average_temperature_uncertainty: float
    ):
        try:
            TemperatureReading(
                city_name=city_name,
                recording_date=recording_date,
                average_temperature=average_temperature,
                average_temperature_uncertainty=average_temperature_uncertainty
            ).save()
        except NotUniqueError:
            raise AccessLayerException('Record already exists for this data,'
                                       'Maybe you want to update.')

    def get_records_by_city_name(self, city_name, from_date=None, to_date=None):
        query = {'city_name': city_name}
        query = self._apply_from_to_filter(query,
                                           from_date,
                                           to_date)

        records = TemperatureReading.objects(**query)

        return records

    def get_records_by_name_date(self, city_name, recording_date):
        try:
            return TemperatureReading.objects.get(city_name=city_name,
                                          recording_date=recording_date)
        except DoesNotExist:
            raise AccessLayerException

    def update_document(self, document):
        document.updated_at = datetime.utcnow()
        document.save()

    def get_records(self, from_date, to_date, limit=None, city_name=None):
        """
        query's the database for records
        applies filters if any.
        """
        query = self._apply_from_to_filter(
            from_date=from_date, to_date=to_date)
        if city_name is not None:
            query['city_name'] = city_name
        records = TemperatureReading.objects(**query).limit(limit)

        return records

    def get_average_temperature_ordered(self, from_date, to_date, limit, order):
        """
        query the data base for highest average temperature, orders by highest.

        returns query result.  
        """
        query = self._apply_from_to_filter(
            from_date=from_date,
            to_date=to_date)
        records = TemperatureReading.objects(
            **query).order_by(f'{order}average_temperature').limit(limit)

        return records

    def _apply_from_to_filter(self, query={}, from_date=None, to_date=None):
        if from_date is not None:
            query['recording_date__gte'] = from_date
        if to_date is not None:
            query['recording_date__lte'] = to_date

        return query
