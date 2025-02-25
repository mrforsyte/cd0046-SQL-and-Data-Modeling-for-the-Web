from flask import render_template, request, flash, redirect, url_for, current_app
from ...models import Show, Artist,Venue, Availability
from ...forms import ShowForm
from ...extensions import db
from . import shows_bp
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

@shows_bp.route('/')
def shows():
    """ Shows all current shows on the page """
    shows = db.session.query(Show, Venue, Artist).join(
        Venue).join(Artist).all()
    data = []
    for show, venue, artist in shows:
        data.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.isoformat()
        })
    return render_template('pages/shows.html', shows=data)


@shows_bp.route('/create')
def create_shows():
    form = ShowForm()

    return render_template('forms/new_show.html', form=form)


@shows_bp.route('/create', methods=['POST'])
def create_show_submission():
    """ Creates a show checking against availability of the artists. """
    form = ShowForm()
    if form.validate_on_submit():
        try:
            artist = Artist.query.get(form.artist_id.data)
            venue = Venue.query.get(form.venue_id.data)

            requested_start_time = form.start_time.data
            availability = Availability.query.filter(
                and_(
                    Availability.artist_id == artist.id,
                    Availability.working_period_start <= requested_start_time,
                    Availability.working_period_end >= requested_start_time
                )
            ).first()

            if not availability:
                flash(f'{artist.name} is not available at the requested time.')
                return render_template('forms/new_show.html', form=form)
            
            existing_show = Show.query.filter(
                and_(
                    Show.artist_id == artist.id,
                    Show.venue_id==venue.id,
                    Show.start_time == requested_start_time
                )
            ).first()

            if existing_show:
                flash(f'{artist.name} is alas busy at this time')
                return render_template('forms/new_show.html',form=form)

            new_show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=form.start_time.data
            )
            db.session.add(new_show)
            db.session.commit()
            return redirect(url_for('shows.shows'))
        
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error creating show: {str(e)}")
            return render_template('forms/new_show.html', form=form)
        finally:
            db.session.close()
    