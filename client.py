import sys
from flask import Flask, Response, request
import requests
from csv import reader
import msgpack

# Read data
with open('events.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    data = list(csv_reader)

# Send data
# used msgpack for serialization
start = 0
lines_to_send = 100
while(True):
    if(lines_to_send>len(data)):
        lines_to_send = len(data)
        # serializer encode for client
        msg = msgpack.packb(data[start:lines_to_send])
        # send data to server
        r = requests.post("http://127.0.0.1:5000", data=msg)
        break
    # serializer encode for client
    msg = msgpack.packb(data[start:lines_to_send])
    # send data to server
    r = requests.post("http://127.0.0.1:5000", data=msg)
    lines_to_send += 100
    start += 100
