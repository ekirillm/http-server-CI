#!/usr/bin/env python3

import socket
import os
import redis
import json
import pickle
import pymongo
import logging
import logging.config
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
PORT = 65432

# connect to db
conn_db = pymongo.MongoClient('server-mongo', 27017)
db = conn_db['test-json']	


def put_value(key, value):
	# add key-value pair to cache
	cache = redis.Redis(host='host-redis', port=6379)
	cache.ping()
	cache.set(key, pickle.dumps(value))
	app.logger.debug('set value in cache for key [%s]', key)
	# add to db
	coll = db['messages']
	res = list(coll.find({'key':key}))
	if len(res) == 0:
		# key not exists
		coll.insert_one({'key':key, 'message':value})
		app.logger.info('key-value pair is created for key [%s]', key)
		return True
	elif len(res) == 1:
		# key exists
		coll.update_one({'key':key}, {"$set": {'message':value}})
		app.logger.info('value is updated for key [%s]', key)
		return False
	else:	
		# more then one value for key
		app.logger.error('there are more than one value for key [%s]', key)
		raise Exception()

@app.route('/<key>', methods=['POST'])
def handle_put(key):
	app.logger.debug('put for key [%s]', key)
	res = request.get_json()
	if res is None:
		app.logger.error('request data is not parsed')
		abort(400)
	
	if 'message' not in res.keys():
		app.logger.error('there are no message field in request data')
		abort(400)

	value = res['message']

	is_created = put_value(key, value)
	if is_created:
		return ('Created', 201)
	else:
		return ('Ok', 200)


@app.route('/<key>', methods=['GET'])
def handle_get(key):
	app.logger.debug('get for key [%s]', key)
	no_cache_str = request.args.get('no-cache', 'false')
	no_cache = False
	if no_cache_str == 'true':
		app.logger.info('no-cache is true for key [%s]', key)
		no_cache = True
	elif no_cache_str == 'false':
		app.logger.info('no-cache is false for key [%s]', key)
		no_cache = False
	else:
		app.logger.error('no-cache parameter is not correct for key [%s]', key)
		abort(400)

	if not no_cache:
		cache = redis.Redis(host='host-redis', port=6379)
		cache.ping()
		if cache.exists(key):
			app.logger.debug('get value from cache for key [%s]', key)
			return jsonify(message=pickle.loads(cache.get(key)))
		else:
			app.logger.warning('no data in cache for key [%s]', key)
	coll = db['messages']
	res = list(coll.find({'key':key}))
	if len(res) == 0:
		app.logger.error('no data in database for key [%s]', key)
		abort(404)
	elif len(res) == 1:
		if not no_cache:
			put_value(key, res[0]['message'])
		return jsonify(message=res[0]['message'])
	else:
		# more than one value for key
		app.logger.error('there are more than one value for key [%s]', key)
		abort(500)
		
@app.route('/<key>', methods=['DELETE'])
def handle_delete(key):
	app.logger.debug('delete for key [%s]', key)
	cache = redis.Redis(host='host-redis', port=6379)
	cache.ping()
	if cache.exists(key):
		app.logger.debug('value is deleted from cache for key [%s]', key)
		cache.delete(key)
	else:
		app.logger.warning('no data in cache for key [%s]', key)
	
	coll = db['messages']
	res = list(coll.find({'key':key}))
	if len(res) == 0:
		app.logger.warning('no data in database for key [%s]', key)
		return ('Ok', 200)
	elif len(res) == 1:
		coll.remove({'key':key})
		app.logger.debug('value is deleted from database for key [%s]', key)
		return ('Ok', 200)
	else:
		# more then one value for key
		app.logger.error('there are more than one value for key [%s]', key)
		abort(500)

@app.route('/')
def hello():
	app.logger.debug('index')
	return 'Hello! It is http-key-value-storage-server. Specify key in URL and use POST, GET and DELETE requests.'


if __name__ == '__main__':
	log_config_path = './log.config'
	logging.config.fileConfig(log_config_path)
	conf_logger = logging.getLogger('ServerLog')

	# Add handlers to default logger in order to log all requests
	default_logger = logging.getLogger('werkzeug')
	for handler in conf_logger.handlers:
		default_logger.addHandler(handler)
	app.logger = conf_logger
	app.run(host='0.0.0.0', port=PORT)



