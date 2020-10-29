"""
Class for journey model
"""

from .. import db, marshmallow


class Journey(db.Model):
    """
    Journey represents the pickup and dropoff location. It also has other helper properties
    """

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey(
        'vendor.id'), nullable=False)

    passenger_count = db.Column(db.Integer, nullable=False)
    pickup_latitude = db.Column(db.Float)
    pickup_longitude = db.Column(db.Float)
    dropoff_latitude = db.Column(db.Float)
    dropoff_longitude = db.Column(db.Float)

    total_fare_amount = db.Column(db.Float)

    pickup_time = db.Column(db.DateTime, nullable=False)
    dropoff_time = db.Column(db.DateTime, nullable=False)

    distance = db.Column(db.Float)

    def __init__(
        self,
        vendor_id=None,
        passenger_count=1,
        pickup_latitude=None,
        pickup_longitude=None,
        dropoff_latitude=None,
        dropoff_longitude=None,
        total_fare_amount=None,
        pickup_time=None,
        dropoff_time=None,
        distance=None,
    ):
        self.vendor_id = vendor_id
        self.passenger_count = passenger_count
        self.pickup_latitude = pickup_latitude
        self.pickup_longitude = pickup_longitude
        self.dropoff_latitude = dropoff_latitude
        self.dropoff_longitude = dropoff_longitude
        self.total_fare_amount = total_fare_amount
        self.pickup_time = pickup_time
        self.dropoff_time = dropoff_time
        self.distance = distance

    def save(self):
        """ Shorthand function to save the instance """
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """ Shorthand function to update the instance """
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        """ Shorthand function to delete the instance """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """ Returns all instances in the database """
        return Journey.query.all()

    @staticmethod
    def get_one(search_id):
        """ Returns one by id """
        return Journey.query.get(search_id)

    def __repr__(self):
        return (
            f"Journey('{self.pickup_time} - "
            f"{self.dropoff_time}. {self.distance}/{self.total_fare_amount}')")


class JourneySchema(marshmallow.Schema):
    """ Journey marshmallow schema """
    class Meta:
        """ A meta description for marshmallow integration """
        fields = ('vendor_id', 'id', 'passenger_count',
                  'pickup_latitude', 'pickup_longitude',
                  'dropoff_latitude', 'dropoff_longitude',
                  'total_fare_amount', 'pickup_time', 'dropoff_time',
                  'distance')

journey_schema = JourneySchema()
journeys_schema = JourneySchema(many=True)
