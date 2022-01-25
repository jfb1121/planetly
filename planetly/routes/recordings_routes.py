from flask import Blueprint, jsonify, request
from planetly.exceptions import AccessLayerException, ServiceException
from planetly.modules.response_utils import error_func
from planetly.services.temperature_recording_service import \
    TemperatureRecordingService


recordings_urls = Blueprint(
    "monthly_average_temperatures",
    __name__,
    url_prefix="/temperatures")

service = TemperatureRecordingService()


@recordings_urls.route('/', methods=["GET"])
def list_all_records():
    """
    List all function for the resource, allows filtering using query string 
    parameters.
    """

    from_date = request.args.get("fromDate", None)
    to_date = request.args.get("toDate", None)
    record_limit = int(request.args.get("limit", None)) if request.args.get(
        "limit", None) is not None else None
    records = service.get_avg_temperature_readings(
        from_date,
        to_date,
        record_limit,
    )

    return jsonify(records), 200


@recordings_urls.route('/', methods=["post"])
def create_record():
    """
    This function allows to create a new record.

    returns 200: if a record was created.

    returns 422: if record creation failed because a resource already exists. 
    """
    data = request.get_json(force=True)
    try:
        service.add_temperature_reading(**data)

        return {"success": True}, 200
    except AccessLayerException:
        error_func("resource already exists", 422)


@recordings_urls.route('/ChasingSummer', methods=["GET"])
def list_hottest():
    """
    List all function for the resource, allows filtering using query string 
    parameters.
    """
    from_date = request.args.get("fromDate", None)
    to_date = request.args.get("toDate", None)
    record_limit = int(request.args.get("limit", None)) if request.args.get(
        "limit", None) is not None else None
    try:
        records = service.get_avg_temperature_readings(
            from_date=from_date,
            to_date=to_date,
            limit=record_limit,
            order="hottest"
        )
        return jsonify(records), 200
    except ServiceException:
        error_func("Invalid query", 405)



@recordings_urls.route('/<city_name>/<recording_date>', methods=["GET"])
def get_record(city_name, recording_date):
    """
    returns a single record for the given city name and recording date.
    status code 200: success
    status code 404: no record exists for the given combination of input.
    """
    try:
        record = service.get_recorded_avg_temp(city_name, recording_date)
        return record
    except AccessLayerException:
        error_func("Record for the given city and date doesn't exist", 404)


@recordings_urls.route('/<city_name>/<recording_date>', methods=["POST"])
def create_record_by_name_date(city_name, recording_date):
    """
    Allows creating a new single record.    

    status code 200: success
    status code 405: failure, record already exists / input data is incorrect.
    """
    data = request.get_json(force=True)
    data['city_name'] = city_name
    data['recording_date'] = recording_date
    try:
        service.add_temperature_reading(**data)

        return {"success": True}, 200
    except AccessLayerException:
        error_func("resource already exists", 422)
    except ServiceException:
        error_func("Invalid input", 405)


@recordings_urls.route('/<city_name>/<recording_date>', methods=["PUT"])
def update_record_by_name_date(city_name, recording_date):
    """
    Allows updating a single record for the combination of city name and
    recording date.

    status code 200: success
    status code 400: no updatable fields in the request
    status code 404: the record being updated does not exist. 
    """
    data = request.get_json(force=True)
    try:
        service.update_temperature_reading(city_name, recording_date, **data)
        return jsonify({"success": True}), 200
    except ServiceException:
        error_func("Nothing to update", 400)
    except AccessLayerException:
        error_func("The resource you are trying to update, does not exist", 404)
