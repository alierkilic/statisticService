import sys
from flask import Flask, Response, request
import requests
from csv import reader
import msgpack

# Read data
with open('events.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)

# used msgpack for serialization
#serializer encode for client
msg = msgpack.packb(list_of_rows)
# send data to server
r = requests.post("http://127.0.0.1:5000", data=msg)