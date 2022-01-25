from flask import abort, jsonify, make_response


def error_func(message: str, status: int):
    """
    returns json response with given status code
    """
    abort(make_response(jsonify(success=False,
                                message=message), status))