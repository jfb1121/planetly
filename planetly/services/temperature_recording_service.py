from datetime import datetime
from dateutil import parser

from typing import Any, Mapping, Sequence, Union

import json
from planetly.exceptions import ServiceException
from planetly.models.access_layers.temperature_reading_access_layer import\
    TemperatureReadingAccessLayer


class TemperatureRecordingService:
    """
    This service contains all the business logic for temperature related
    operations.
    """

    def __init__(self) -> None:
        self.access_layer = TemperatureReadingAccessLayer()

    def get_recorded_avg_temp(self,
                              city_name,
                              recording_date) -> Mapping:
        """
        returns a single record for the given city on a date, if it exists.
        """
        rec = self.access_layer.get_records_by_name_date(city_name,
                                                         recording_date)

        return json.loads(rec.to_json())

    def get_avg_temperature_readings(self,
                                     from_date=None,
                                     to_date=None,
                                     limit=None,
                                     order=None,
                                     city_name=None
                                     ) -> Sequence:
        """
        returns the records, applies filters if applicable
        """
        if from_date is not None and to_date is not None:
            from_date = self.date_helper(from_date).date()
            to_date = self.date_helper(to_date).date()
            if to_date < from_date:
                raise ServiceException("Expected to date to be less than from")

        if order is None:
            records = self.access_layer.get_records(
                from_date,
                to_date,
                limit,
                city_name
            )

            reocrds = [json.loads(rec.to_json()) for rec in records]

            return reocrds
        else:
            return self.get_avg_temperatures_recorded_ordered(
                from_date,
                to_date,
                limit,
                order)

    def add_temperature_reading(
        self,
        city_name: str,
        recording_date: str,
        average_temperature: Union[float, str],
        average_temperature_uncertainty: Union[float, str]
    ) -> None:
        """
        creates a new record

        raises ServiceException in case of incorrect / incomplete data
        """
        if average_temperature_uncertainty is None or \
                average_temperature is None or \
                average_temperature_uncertainty == '' or \
                average_temperature == '':
            raise ServiceException
        try:
            average_temperature_uncertainty = float(
                average_temperature_uncertainty)
            average_temperature = float(average_temperature)
        except ValueError:
            raise ServiceException
        recording_date = self.date_helper(recording_date).date()
        self.access_layer.create_temperature_reading(
            city_name,
            recording_date,
            average_temperature,
            average_temperature_uncertainty
        )

    def get_avg_temperatures_recorded_ordered(self,
                                              from_date=None,
                                              to_date=None,
                                              limit=None,
                                              order=None):
        """
        returns top n average hottest/coldest temperatures recorded.
        """
        if order == "hottest":
            order = '-'
        elif order == "coldest":
            order = '+'
        else:
            raise ServiceException(
                "Expected order to be by hottest or coldest")

        records = self.access_layer.get_average_temperature_ordered(
            from_date,
            to_date,
            limit,
            order
        )

        return [json.loads(rec.to_json()) for rec in records]

    def update_temperature_reading(
        self,
        city_name: str,
        recording_date: str,
        average_temperature: Union[float, str] = None,
        average_temperature_uncertainty: Union[float, str] = None
    ):
        """
        updates the avg temperature and/or avg temperature uncertainty.
        """
        if average_temperature is None and average_temperature_uncertainty is\
                None:
            raise ServiceException("Expected something to update")

        doc = self.access_layer.get_records_by_name_date(
            city_name, recording_date)

        if average_temperature is not None:
            doc.average_temperature = average_temperature

        if average_temperature_uncertainty is not None:
            doc.average_temperature_uncertainty = \
                average_temperature_uncertainty

        self.access_layer.update_document(doc)

    def date_helper(self, date: str) -> datetime:
        return parser.parse(date)
        
        
