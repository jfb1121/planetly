
<!-- ABOUT THE PROJECT -->
## About The Project


This is a simple REST API built with flask and MongoDB.

### Infrastructure decisions
  * Options considered:
    * SQL (any flavor)
    * NoSql databases
      * MongoDb
      * Cassandra
      * DynamoDB
  * SQL:
    * Great database for ACID compliance. (we don't need it for this application)
    * Vertical scaling 
    * This limits regional availability and requires replication of the database which is complex
    * Some flavors have inbuilt support for NoSql storage.
  * NoSql
    * MongoDb
      * Acid properties across documents.
      * Easy modelling and querying.
      * Horizontal scaling, with high availability.
      * Platform-agnostic (self hosted and managed).
      * Supports joins, multiple ranges etc .
      * Json based storage
    * Cassandra
      * Read optimized database.
      * Strict query first approach, to support additional queries a new model and rebuild is required.
      * Extremely high availability is possible with the right configurations for the right use cases.
      * Platform-agnostic (self hosted and managed)
      * Key-value storage.
    * DynamoDB
      * Heavy dependencies on AWS.(vendor locked)
      * Strict key-value store
      * Could become very expensive relatively soon
      * Not a lot of room for optimization, too few metrics.

  #### Decision
  I decided to use mongoDb as a backend store for multiple reasons, it provided an easy interface to work with.
  It's extremely flexible for any other use cases that might come in the future, which on production it always does.
  I have prior experience with it. 

  P.S: Any SQL database would have been a strong second with regards to other NoSql databases considered as most of them are key-value based strict databases. 

  #### Code base structure
  The code base tries to follow a strict separation of concerns principal.
  The system is divided into 3 layers:
    * View layer: responsible for dealing with request and response logic
    * Service layer: complex business logic goes here, although there were not a lot
    * I/O layer: Abstracts away any database or other form of I/O from the rest of the system.
      * This allows us to change the database / models while maintaining the same interface to the service layer

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://python.org)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [MongoDb](https://www.mongodb.com)
* [Swagger](https://swagger.io)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To test this application, you should run the following commands.


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* docker
  ```
  docker-compose up -d 
  ```
* load data from csv (please ensure to run in a virtual env)
  ```
  pip install -r requirements.txt
  python data_set_loader.py <path-to-csv> 
  ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- EXAMPLES -->
## EXAMPLES

please refer to the docs hosted at localhost:5000/api/v1/docs/
* 3.a:
  * Request:
    * curl
      ```
      curl --location --request GET 'localhost:5000/temperatures/ChasingSummer?fromDate=2000-01-01&toDate=2023-01-01&limit=1'
      ```
    * 3.a: python
      ```
      import http.client

      conn = http.client.HTTPSConnection("localhost", 5000)
      payload = ''
      headers = {}
      conn.request("GET", "/temperatures/ChasingSummer?fromDate=2000-01-01&toDate=2023-01-01&limit=1", payload, headers)
      res = conn.getresponse()
      data = res.read()
      print(data.decode("utf-8"))
      ```
  * Response:
    ```
    [
      {
          "average_temperature": 39.15600000000001,
          "average_temperature_uncertainty": 0.37,
          "city_name": "Ahvaz",
          "created_at": "2022-01-25T17:33:32.099000",
          "id": "61f034f78b21775609c9f01d",
          "recording_date": "2013-07-01T00:00:00"
      }
    ]
    ```

* 3.b:
  * Request:
    * curl
    ```
      curl --location --request POST 'localhost:5000/temperatures/Ahvaz/2021-12-01' --header 'Content-Type: application/json' --data-raw '{
      "average_temperature": 39.25600000000001,
      "average_temperature_uncertainty": 0.37
      }'
    ```
    * python
    ```
    import http.client
    import json

    conn = http.client.HTTPSConnection("localhost", 5000)
    payload = json.dumps({
      "average_temperature": 39.25600000000001,
      "average_temperature_uncertainty": 0.37
    })
    headers = {
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/temperatures/Ahvaz/2021-12-01", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    ```
  * Response:
  ```
  {
    "success": true
  }
  ```
* 3.c:
  * Request:
    * curl
    ```
    curl --location --request PUT 'localhost:5000/temperatures/Ahvaz/2013-07-01' --header 'Content-Type: application/json' --data-raw '{
    "average_temperature": 36.65600000000001}'
    ```
    * python
    ```
    import http.client
    import json

    conn = http.client.HTTPSConnection("localhost", 5000)
    payload = json.dumps({
      "average_temperature": 36.65600000000001
    })
    headers = {
      'Content-Type': 'application/json'
    }
    conn.request("PUT", "/temperatures/Ahvaz/2013-07-01", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    ```
  * Response:
  ```
  {
    "success": true
  }
  ```



<p align="right">(<a href="#top">back to top</a>)</p>



