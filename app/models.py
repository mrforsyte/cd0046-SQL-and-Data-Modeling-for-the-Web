from .extensions import db
from sqlalchemy import func, and_
from datetime import datetime


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
    seeking_talent = db.Column(db.Boolean, default=False,nullable=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String(50)))
    shows = db.relationship('Show', back_populates='venue',lazy='dynamic')
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now())

    def __repr__(self):
        return f'<Vanue {self.id} {self.name}>'
    
    def get_past_shows(self):
        """Retrieve all past shows for this venue."""
        return db.session.query(Show).join(Venue).filter(
            Show.venue_id == self.id,
            Show.start_time < datetime.now()
        ).all()

    def get_upcoming_shows(self):
        """Retrieve all upcoming shows for this venue."""
        return db.session.query(Show).join(Venue).filter(
            Show.venue_id == self.id,
            Show.start_time >= datetime.now()
        ).all()

    @property
    def past_shows_count(self):
        return len(self.get_past_shows())
    
    @property
    def upcoming_shows_count(self):
        return len(self.get_upcoming_shows())


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(50)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', back_populates='artist', lazy='dynamic')
    availabilities = db.relationship('Availability', back_populates='artist')


    def __repr__(self):
        return f'< Artist is {self.name} {self.id}>'
    

    def get_past_shows(self):
        """Retrieve all past shows for this artist."""
        return db.session.query(Show).join(Artist).filter(
            Show.artist_id == self.id,
            Show.start_time < datetime.now()
        ).all()

    def get_upcoming_shows(self):
        """Retrieve all upcoming shows for this artist."""
        return db.session.query(Show).join(Artist).filter(
            Show.artist_id == self.id,
            Show.start_time >= datetime.now()
        ).all()

    @property
    def upcoming_shows_count(self):
        return self.shows.filter(Show.start_time > datetime.now()).count()

    @property
    def past_shows_count(self):
        return self.shows.filter(Show.start_time <= datetime.now()).count()

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, index=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    venue = db.relationship('Venue', back_populates ='shows')
    artist = db.relationship('Artist', back_populates ='shows')

    def __repr__(self):
        return f'<Show {self.id}: {self.name}>'


class Availability(db.Model):

    __tablename__ = 'availability'

    id = db.Column(db.Integer, primary_key=True)
    working_period_start = db.Column(db.DateTime)
    working_period_end = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    artist = db.relationship('Artist', back_populates ='availabilities')

    def __repr__(self):
        return f'<Availability {self.id}: {self.working_period_start} -> {self.working_period_end}>'