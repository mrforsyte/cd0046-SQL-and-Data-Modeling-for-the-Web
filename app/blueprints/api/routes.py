from flask import jsonify
from ...models import Artist,Venue
from . import api_bp



@api_bp.route('/artists')
def get_all_artists():
    artists = Artist.query.all()
    return jsonify([{'id': artist.id,'name':artist.name} for artist in artists])

@api_bp.route('/venues')
def get_venues():
    venues = Venue.query.all()
    return jsonify([{'id': venue.id, 'name': venue.name} for venue in venues])


