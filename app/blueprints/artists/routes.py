
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import Artist, Availability
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

        search_term = request.form['search_term']
        artists = Artist.query.filter(
            Artist.name.ilike(f'%{search_term}%')).all()
        return render_template(
            'pages/search_artists.html',
            results=artists,
            search_term=request.form.get(
                'search_term',
                ''))

    except Exception as e:

        print(f'Error occured while searchig for specific artist : {e}')
        return render_template('500.html'), 500


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


@artists_bp.route('/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    try:
        record = Artist.query.get_or_404(artist_id)
        form = ArtistForm(obj=record)
        availabilities = Availability.query.filter_by(artist_id=artist_id).all()
        form.availabilities = availabilities
        
        return render_template('forms/edit_artist.html', form=form, artist=record)
    except Exception as e:
        print(f'Error occurred when retrieving artists with error {e}')
        return render_template('500.html'), 500


@artists_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    record = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=record)
    if form.validate():
        try:
            form.populate_obj(record)
            
            existing_availabilities = Availability.query.filter_by(artist_id=artist_id).all()
            for availability in existing_availabilities:
                db.session.delete(availability)
            
            for availability in form.availabilities:
                new_availability = Availability(
                    artist_id=artist_id,
                    working_period_start=availability.working_period_start.data,
                    working_period_end=availability.working_period_end.data
                )
                db.session.add(new_availability)
            
            new_starts = request.form.getlist('new_availability_start')
            new_ends = request.form.getlist('new_availability_end')
            new_availability = Availability(
                artist_id=artist_id,
                working_period_start=datetime.strptime(start, '%Y-%m-%dT%H:%M'),
                working_period_end=datetime.strptime(end, '%Y-%m-%dT%H:%M')
                    )
            db.session.add(new_availability)
            
            db.session.commit()
            flash(f'Artist {record.name} was updated successfully')
        except Exception as e:
            db.session.rollback()
            flash(f'Something went wrong with {record.name}: {str(e)}')
        finally:
            db.session.close()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}')

    return redirect(url_for('artist.show_artist', artist_id=artist_id))



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

