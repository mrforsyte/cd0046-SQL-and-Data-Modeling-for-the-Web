from .extensions import db
from sqlalchemy import func

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String(50)))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now())

    def __repr__(self):
        return f'<Vanue {self.id} {self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    def __repr__(self):
        return f'< Artist is {self.name} {self.id}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, index=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    venue = db.relationship('Venue', backref='shows')
    artist = db.relationship('Artist', backref='shows')

    def __repr__(self):
        return f'<Show {self.id}: {self.name}>'


class Availability(db.Model):

    __tablename__ = 'availability'

    id = db.Column(db.Integer, primary_key=True)
    working_period_start = db.Column(db.DateTime)
    working_period_end = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    artist = db.relationship('Artist', backref='avialabilities')

    def __repr__(self):
        return f'<Availability {self.id}: {self.working_period_start} -> {self.working_period_end}>'
