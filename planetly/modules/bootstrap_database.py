from mongoengine import connect


def connect_to_mongo(
    db_user_name,
    db_password,
    db_url,
    alias="default",
    host="mongodb"
):
    """
    establishes a connection to the database.
    """
    uri = f"{host}://{db_user_name}:{db_password}@{db_url}:27017/assignment?\
authSource=admin"
    connect(host=uri, alias=alias)
