# Purpose

Create a REST endpoint that return the sum of a list of numbers e.g. [1,2,3] => 1+2+3 = 6

We hard code the list using the following line: 
```numbers_to_add = list(range(10000001))```

The url of the endpoint and the sample response is as follows:


```
Request: http://localhost:5000/total
Response:
{
    "total": 6
}
```

# Installation

You can easily install the app with Docker in the app's root directory:

```
docker-compose -d up --build
```
This will build the docker and as soon as it finishes the build it will start listening on port 5000. For stopping it
 just type 
```docker-compose down```

# Requests
The GET method is used for requests. The main reason is the idempotent property:
 if the requests are made with the same data, the response will always be the same. Another interesting point is that,
  in addition, GET requests are cached by browsers (browser caches url) so the response will be much faster when we 
  make the same requests. In order to do this we must use query strings. This is an example of a request: 
  ```
curl --location --request GET 'http://127.0.0.1:5000/total?list=[0,1,2,3]'
```
The problem with using query string parameters is that they are built into the url itself and there is a maximum limit 
on the number of characters a url can use: 2048. So the solution to send a very big list of numbers would be to use 
request body. The requests will not be cached but we will be able to send them. An example of a request with 
request body would be the one below:
```
curl --location --request GET 'http://127.0.0.1:5000/total' \
--header 'Content-Type: text/plain' \
--data-raw '[1, 2, 3]'
```
This is totally correct according to RFCs 7230-7237 of 2014. In fact ElasticSearch makes a very strong use of this 
type of requests. So we have the possibility to send data in both the query string and the request body. In this 
case the data will be taken from the query string as the url caching can make that the response of the server after 
a request. Here an example:

```
curl --location --request GET 'http://127.0.0.1:5000/total?list=[0,1,2,3,4]' \
--header 'Content-Type: text/plain' \
--data-raw '[1, 2, 3]'
```
In this case the response will be: ```{"total": 10}```

The reason why I have added these two options is because I don't have information about the process that makes 
the requests. Of course it is not the best idea to be able to send data from two different sources since this 
can produce errors.  As this is an exercise, it is a small demonstration that it is possible and depending on which 
process is sending the data, one of the two options should be eliminated.

# Error codes

### 200
Everything is ok. It will send back a response with the result in json format.

### 400
Invalid input. It sends back information about the error in plain text: no data, no list or empty list. 
Examples included on ```openapi.yaml``` file.

### 416
At least one value in the list is out of range.

# Tests

Edge cases and regular cases are included in both: unittests and pytests. Create a virtualenv and install dependencies 
(```pip install -r requirements.txt```) and run tests on your favourite IDE

### Unittest

  You can run unittest tests inside the docker by executing ```docker exec -it dlg_dlg_1 python tests/test_app.py```

### Pytest

  You can run pytest tests inside the docker by executing ```docker exec -it dlg_dlg_1 pytest tests/```
