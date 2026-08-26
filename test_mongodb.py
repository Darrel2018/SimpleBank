import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config.database.mongodb import db

print("Database:", db.name)
print("Collections:", db.list_collection_names())