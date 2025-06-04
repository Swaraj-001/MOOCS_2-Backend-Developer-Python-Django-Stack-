from django.db import models

from db_connect import db

users_collection = db['users']

monuments_collection = db['monuments']

contributions_collection = db['contributions']

cities_collection = db['cities']