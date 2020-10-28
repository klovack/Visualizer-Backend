""" Only run this script once, to initialize the database """

from visualizer.models.journey import Journey
from visualizer.models.vendor import Vendor
from visualizer import db, create_app

if __name__ == "__main__":
    db.create_all(app=create_app())
    print(f"Database {Journey} and {Vendor} is created")
