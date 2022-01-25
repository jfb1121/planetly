from flask_swagger_ui import get_swaggerui_blueprint


"""swagger specific"""
SWAGGER_URL = '/api/v1/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Planetly assignment"
    }
)
