
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import Artist, Availability, Show
from ...forms import ArtistForm, AvailabilityForm
from ...extensions import db
from sqlalchemy.sql import desc 
from . import artists_bp
from datetime import datetime

@artists_bp.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@artists_bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    if form.validate_on_submit():
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=form.genres.data,
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data
            )
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist ' + new_artist.name + ' was successfully listed!')
            return redirect(url_for('artists.add_availability', artist_id=new_artist.id))
        except Exception as e:
            db.session.rollback()
            flash(
                'The error occurred. Artist ' +
                form.name.data +
                ' could not be listed.')
            print(f'Error is {e}')
        finally:
            db.session.close()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}')

    return render_template('pages/home.html')


@artists_bp.route('/artists')
def artists():
    try:
        data = Artist.query.order_by(desc(Artist.id)).limit(10).all()
        return render_template('pages/artists.html', artists=data)
    except Exception as e:
        print(f"Error retrieving artists: {e}")
        return render_template('errors/500.html'), 500


@artists_bp.route('/artists/search', methods=['POST'])
def search_artists():
    try:
        # Get the search term from the form
        search_term = request.form.get('search_term', '')

        # Perform a case-insensitive search using ilike
        artists = Artist.query.filter(
            Artist.name.ilike(f'%{search_term}%')
        ).all()

        # Prepare the response data
        response = {
            "count": len(artists),
            "data": [{
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": Show.query.filter(
                    Show.artist_id == artist.id,
                    Show.start_time > datetime.now()
                ).count()
            } for artist in artists]
        }

        # Render the search results page
        return render_template(
            'pages/search_artists.html',
            results=response,
            search_term=search_term
        )

    except Exception as e:
        # Log the error for debugging purposes
        print(f'Error occurred while searching for specific artist: {e}')
        
        # Render a 500 error page
        return render_template('errors/500.html'), 500


@artists_bp.route('/<int:artist_id>')
def show_artist(artist_id):
    try:

        artist = Artist.query.get_or_404(artist_id)
        artist.upcoming_shows = artist.get_upcoming_shows()
        artist.past_shows = artist.get_past_shows()
        return render_template('pages/show_artist.html', artist=artist)

    except Exception as e:

        print('Error occured while retrieving artists:{str(e)}')
        return render_template('500.html'), 500





@artists_bp.route('/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)

    if request.method == 'POST' and form.validate():
        try:
            form.populate_obj(artist)
            db.session.commit()
            flash(f'Artist {artist.name} was updated successfully')
            return redirect(url_for('artists.edit_artist_availability', artist_id=artist_id))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred. Artist {artist.name} could not be updated: {str(e)}')
        finally:
            db.session.close()

    return render_template('forms/edit_artist.html', form=form, artist=artist)

@artists_bp.route('/<int:artist_id>/edit/availability', methods=['GET', 'POST'])
def edit_artist_availability(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    availability = Availability.query.filter_by(artist_id=artist_id).first()
    
    if not availability:
        availability = Availability(artist_id=artist_id)

    form = AvailabilityForm(obj=availability)

    if request.method == 'POST' and form.validate():
        try:
            form.populate_obj(availability)
            db.session.add(availability)
            db.session.commit()
            flash('Availability was updated successfully')
            return redirect(url_for('artists.show_artist', artist_id=artist_id))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred. Availability could not be updated: {str(e)}')
        finally:
            db.session.close()

    return render_template('forms/edit_availability.html', form=form, artist=artist)


@artists_bp.route('/<int:artist_id>/availability/add', methods=["GET","POST"])
def add_availability(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = AvailabilityForm()

    if form.validate_on_submit():
        new_availability = Availability(
            working_period_start = form.working_period_start.data,
            working_period_end = form.working_period_end.data,
            artist_id=artist.id
        )

        db.session.add(new_availability)
        db.session.commit()
        flash(f"Availability for {artist.name} added successfully ")
        print(f"New availability added: {new_availability}")  # Debug print

        return redirect(url_for('artists.show_artist', artist_id=artist_id))
    else:
        print(f"Form errors: {form.errors}")  # Debug print
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'error')

    return render_template('forms/add_availability.html', form=form, artist=artist)

