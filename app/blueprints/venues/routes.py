from flask import render_template, request, flash, redirect, url_for, abort, current_app
from ...models import Venue,Show
from ...forms import VenueForm
from ...extensions import db
from sqlalchemy.sql import func, desc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from . import venues_bp



@venues_bp.route('/venues')
def venues():
    """ Shows all current venues in database and groups them by city and state. """
    try:
        locations = db.session.query(Venue.city, Venue.state).distinct().all()

        areas = []
        for city, state in locations:
            venues = Venue.query.filter(Venue.city == city, Venue.state == state).all()
            if venues:  
                venue_data = []
                for venue in venues:
                   
                    past_shows = venue.get_past_shows()
                    upcoming_shows = venue.get_upcoming_shows()

                    venue_data.append({
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": len(upcoming_shows),
                        "num_past_shows": len(past_shows)
                    })

                areas.append({
                    "city": city,
                    "state": state,
                    "venues": venue_data
                })

        return render_template('pages/venues.html', areas=areas)

    except Exception as e:
        print(f"Error retrieving venues: {e}")
        return render_template('errors/500.html'), 500
    



@venues_bp.route('/search', methods=['POST'])
def search_venues():
    """ Searches for venues. """

    search_term = request.form.get('search_term', '')
    current_time = datetime.now()

    venues = Venue.query.filter(
        func.lower(Venue.name).contains(func.lower(search_term))
    ).all()

    response = {
        "count": len(venues),
        "data": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": Show.query.filter(
                Show.venue_id == venue.id,
                Show.start_time > current_time
            ).count()
        } for venue in venues]
    }

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=search_term
    )


@venues_bp.route('/<int:venue_id>')
def show_venue(venue_id):
    """ Shows specific venue with a given id """

    try:

        data = Venue.query.get(venue_id)
        return render_template('pages/show_venue.html', venue=data)
    except Exception as e:

        print(f"Error retrieving venue with {venue_id} id: {e}")
        return render_template('errors/500.html'), 500



@venues_bp.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@venues_bp.route('/create', methods=['POST'])
def create_venue_submission():
    """ Creates a venue """
    venue_form = VenueForm()
    if venue_form.validate_on_submit():
        try:
            new_venue = Venue(
                name=venue_form.name.data,
                city=venue_form.city.data,
                state=venue_form.state.data,
                address=venue_form.address.data,
                phone=venue_form.phone.data,
                genres=venue_form.genres.data,
                facebook_link=venue_form.facebook_link.data,
                image_link=venue_form.image_link.data,
                website=venue_form.website_link.data
            )
            db.session.add(new_venue)
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully listed!')

        except Exception as e:
            db.session.rollback()
            flash(
                'An error occurred. Venue ' +
                request.form['name'] +
                ' could not be listed.')
            print(e)
        finally:
            db.session.close()
    else:
        for field, errors in venue_form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}")

    return render_template('pages/home.html')


@venues_bp.route('/venues/<venue_id>', methods=['POST', 'DELETE'])
def delete_venue(venue_id):
    """ Delets a venue"""
    try:

        item_to_delete = db.session.query(Venue).get(venue_id)

        if not item_to_delete:
            abort(404)

        db.session.delete(item_to_delete)
        db.session.commit()
        flash('Venue successfully deleted!')

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error deleting venue: {str(e)}', 'error')
        abort(500)

    return redirect(url_for('venues.venues'))



@venues_bp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """ Edits a venue with given id. """
    record = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=record)

    return render_template('forms/edit_venue.html', form=form, venue=record)


@venues_bp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(request.form)

    if form.validate():
        try:
            form.populate_obj(venue)
            db.session.commit()
            flash(f'Venue {venue.id}:{venue.name} was successfully updated!')
        except Exception as e:
            db.session.rollback()
            flash(
                f'The error occurred. Venue {venue.name} could not be updated.')
            print(e)
        finally:
            db.session.close()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}')

    return redirect(url_for('venues.show_venue', venue_id=venue_id))
