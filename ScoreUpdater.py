import json
from DataHandler import DataHandler

__author__ = 'Thomas'

with open('test.json') as data_file:
    data = json.load(data_file)

data_handler = DataHandler(usr=data["usr"], table=data["table"], url=data["url"], pwd=data["pwd"])


