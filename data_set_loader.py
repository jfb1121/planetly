from datetime import datetime
from typing import Collection
import click
from pymongo import MongoClient
from scripts.settings import DB_USER_NAME, DB_PASSWORD, DB_URL

import pandas as pd
import numpy as np

"""
This script is intended to be run only once. 
It deletes all records existing in the database, before creating new ones.

* Loads the input csv (assumes you give the right one).
* cleans up data by filling nan's through imputed values.
* splits the data frame into a strict batch (based on the data set).
* loads it into the database using pymongo.
    * pymongo doesn't validate the documents on the basis of the model defined.
    so, we drop columns and rename them to match the model defined in the 
    application. 
"""


def establish_connection() -> Collection:
    uri = f"mongodb://{DB_USER_NAME}:{DB_PASSWORD}@{DB_URL}:27017/assignment?\
    authSource=admin"
    client = MongoClient(uri)
    db = client.assignment
    collection = db.temperature_reading
    # deletes all records.
    collection.delete_many({})

    return collection


def clean_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    replaces nan values in the data set by taking a mean of the same month
    for the same city.
    """
    # remove duplicate records for the same city and recording_date
    # this is necessary as our application depends on the uniqueness of this
    # combination.
    data_frame = data_frame.sort_values("AverageTemperatureUncertainty",
                                        ascending=False).drop_duplicates(
        ["City", "dt"], keep="last"
    )
    # add a int based month column
    data_frame['month'] = pd.DatetimeIndex(data_frame['dt']).month
    # take a subset for filling nan in AverageTemperature
    subset_data_avg_temp = data_frame[['City', 'month', 'AverageTemperature']]
    subset_data_avg_temp['AverageTemperature'] = \
        compute_fill_na(subset_data_avg_temp)

    data_frame['AverageTemperature'] = compute_fill_na(subset_data_avg_temp)

    subset_data_avg_temp_uncertanity = \
        data_frame[['City', 'month', 'AverageTemperatureUncertainty']]

    data_frame['AverageTemperatureUncertainty'] = \
        compute_fill_na(subset_data_avg_temp_uncertanity)

    return data_frame


def compute_fill_na(subset_data):
    return subset_data.groupby(['City', 'month']
                               ).transform(lambda group: group.fillna(group.mean()))


@click.command()
@click.argument('file', type=click.Path(exists=True))
def load_data(file):
    collection = establish_connection()
    data_frame = preprocess_data(file)
    # hard coded based on the data set
    df_split = np.array_split(data_frame, 80)
    for frame in df_split:
        write_to_mongo(frame, collection)


def write_to_mongo(data_frame: pd.DataFrame, collection: Collection):
    records = data_frame.to_dict(orient="records")
    collection.insert_many(records)


def preprocess_data(file):
    data_frame = pd.read_csv(file)
    data_frame = clean_data(data_frame)
    data_frame = drop_unwanted_columns(data_frame)
    data_frame = rename_columns(data_frame)
    data_frame = convert_to_date_time(data_frame)
    add_required_columns(data_frame)

    return data_frame


def convert_to_date_time(data_frame):
    data_frame['recording_date'] = pd.to_datetime(
        data_frame['recording_date'], format="%Y-%m-%d")

    return data_frame


def add_required_columns(data_frame):
    data_frame['created_at'] = datetime.utcnow()


def rename_columns(data_frame):
    old_to_new_mapping = {
        'dt': 'recording_date',
        'City': 'city_name',
        'AverageTemperature': 'average_temperature',
        'AverageTemperatureUncertainty': 'average_temperature_uncertainty'
    }
    df = data_frame.rename(columns=old_to_new_mapping)

    return df


def drop_unwanted_columns(data_frame):
    df = data_frame.drop(columns=['Country', 'Latitude', 'Longitude', 'month'])

    return df


if __name__ == "__main__":
    load_data()
