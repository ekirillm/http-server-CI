# http-key-value-storage-server
[![Build Status](https://travis-ci.org/ekirillm/http-server-CI.svg?branch=master)](https://travis-ci.org/ekirillm/http-server-CI)

HTTP server with Docker Compose, Redis and MongoDB. 
## Usage
* Start server: `docker-compose up`
* Stop server: `docker-compose down`

Data is saved in MongoDB container, cache is in Redis container.

Server port: `2000`.

URL: http://ip:2000/{key}?[no-cache=[true|false]]

Example requests using curl: 
* curl -X POST -H "Content-Type: application/json" -d '{"message": "aaa"}' localhost:2000/1
* curl -X GET localhost:2000/1
* curl -X GET localhost:2000/1?no-cache=true
* curl -X GET localhost:2000/1?no-cache=false
* curl -X DELETE localhost:2000/1
* curl -X POST -H "Content-Type: application/json" -d '{"message": {"ddd": "fff"}}' localhost:2000/1

`log.config` is a configuration file for logger.