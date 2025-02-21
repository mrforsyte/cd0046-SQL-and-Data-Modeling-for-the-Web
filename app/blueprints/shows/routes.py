from flask import render_template, request, flash, redirect, url_for, current_app
from ...models import Show, Artist,Venue
from ...forms import ShowForm
from ...extensions import db
from . import shows_bp
from sqlalchemy import SQLAlchemyError





@shows_bp.route('/shows')
def shows():
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


@shows_bp.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()

    return render_template('forms/new_show.html', form=form)


@shows_bp.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    if form.validate_on_submit():
        try:
            artist = Artist.query.get(form.artist_id.data)
            venue = Venue.query.get(form.venue_id.data)
            if not artist or not venue:
                flash('Invalid artist or venue ID.')
                return render_template('forms/new_show.html', form=form)

            new_show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=form.start_time.data
            )
            db.session.add(new_show)
            db.session.commit()
            flash(
                f'Show was successfully listed for {artist.name} at {venue.name}!')
            return redirect(url_for('shows'))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error creating show: {str(e)}")
            flash('An error occurred. Show could not be listed due to a database issue.')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error creating show: {str(e)}")
            flash('An unexpected error occurred. Show could not be listed.')
        finally:
            db.session.close()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}")
    return render_template('forms/new_show.html', form=form)

