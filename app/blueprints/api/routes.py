from flask import jsonify
from ...models import Artist, Venue
from . import api_bp

@api_bp.route('/artists')
def get_all_artists():
    """
    Retrieve a list of all artists.

    This endpoint returns a JSON array containing the ID and name of all artists in the database.

    Returns:
        JSON: A list of dictionaries, each containing:
            - id (int): The unique identifier of the artist.
            - name (str): The name of the artist.

    Example response:
        [
            {"id": 1, "name": "Artist 1"},
            {"id": 2, "name": "Artist 2"},
            ...
        ]
    """
    artists = Artist.query.all()
    return jsonify([{'id': artist.id, 'name': artist.name} for artist in artists])

@api_bp.route('/venues')
def get_venues():
    """
    Retrieve a list of all venues.

    This endpoint returns a JSON array containing the ID and name of all venues in the database.

    Returns:
        JSON: A list of dictionaries, each containing:
            - id (int): The unique identifier of the venue.
            - name (str): The name of the venue.

    Example response:
        [
            {"id": 1, "name": "Venue 1"},
            {"id": 2, "name": "Venue 2"},
            ...
        ]
    """
    venues = Venue.query.all()
    return jsonify([{'id': venue.id, 'name': venue.name} for venue in venues])

