#!/usr/bin/env python3

import socket
import os
import redis
import json
import pickle
import requests
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
PORT = 2000
servers_address = ['http://server1:2001', 'http://server2:2002']

def balance(key):
	return servers_address[key % len(servers_address)]

@app.route('/<key>', methods=['POST'])
def handle_put(key):
	int_key = 0
	try:
		int_key = int(key)
	except:
		abort(400)
	server_address = balance(int_key)
	resp = requests.post(server_address + '/' + str(int_key), data=request.data, headers=request.headers)
	return resp.content, resp.status_code, resp.headers.items()


@app.route('/<key>', methods=['GET'])
def handle_get(key):
	int_key = 0
	try:
		int_key = int(key)
	except:
		abort(400)

	no_cache_str = request.args.get('no-cache', 'false')
	no_cache = False
	if no_cache_str == 'true':
		no_cache = True
	elif no_cache_str == 'false':
		no_cache = False
	else:
		abort(400)

	if not no_cache:
		cache = redis.Redis(host='cache-redis', port=6379)
		cache.ping()
		if cache.exists(int_key):
			return jsonify(message=pickle.loads(cache.get(int_key)))

	server_address = balance(int_key)
	resp = requests.get(server_address + '/' + str(int_key), headers=request.headers, params=request.args)
	return resp.content, resp.status_code, resp.headers.items()

@app.route('/<key>', methods=['DELETE'])
def handle_delete(key):
	int_key = 0
	try:
		int_key = int(key)
	except:
		abort(400)

	cache = redis.Redis(host='cache-redis', port=6379)
	cache.ping()
	if cache.exists(int_key):
		cache.delete(int_key)
	server_address = balance(int_key)
	resp = requests.delete(server_address + '/' + str(int_key), headers=request.headers)
	return resp.content, resp.status_code, resp.headers.items()

@app.route('/')
def hello():
	return 'Hello! It is http-key-value-storage-server. Specify key in URL and use POST, GET and DELETE requests.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT) 



