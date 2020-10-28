"""
Models which are schema for the database
"""

from .. import db, marshmallow

class Vendor(db.Model):
    """
    Vendor has id, name, and journey
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    journeys = db.relationship('Journey', backref='vendor', lazy=True)

    def __init__(self, name=None):
        self.name = name

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
        return Vendor.query.all()

    @staticmethod
    def get_one(search_id):
        """ Returns one by id """
        return Vendor.query.get(search_id)

    def __repr__(self):
        return f"Vendor('{self.name}')"


class VendorSchema(marshmallow.SQLAlchemySchema):
    """ A marshmallow schema for vendor model """
    class Meta:
        """ A meta description for VendorSchema """
        model = Vendor

    id = marshmallow.auto_field()
    name = marshmallow.auto_field()
    journeys = marshmallow.auto_field()


vendor_schema = VendorSchema()
vendors_schema = VendorSchema(many=True)
