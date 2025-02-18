
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Artist
from forms import ArtistForm
from extensions import db

artist_bp = Blueprint('artists', __name__)


@artist_bp.route('/artists')
def artists():
    try:
        data = Artist.query.all()
        return render_template('pages/artists.html', artists=data)
    except Exception as e:
        print(f"Error retrieving artists: {e}")
        return render_template('errors/500.html'), 500


@artist_bp.route('/artists/search', methods=['POST'])
def search_artists():
    try:

        search_term = request.form['search_term']
        artists = Artist.query.filter(
            Artist.namename.ilike(f'%{search_term}%')).all()
        return render_template(
            'pages/search_artists.html',
            results=artists,
            search_term=request.form.get(
                'search_term',
                ''))

    except Exception as e:

        print(f'Error occured while searchig for specific artist : {e}')
        return render_template('500.html'), 500


@artist_bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:

        data = Show.query.get(artist_id)
        return render_template('pages/show_artist.html', artist=data)

    except Exception as e:

        print('Error occured while retrieving artists:{e}')
        return render_template('500.html'), 500

#  Update
#  ----------------------------------------------------------------


@artist_bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    try:

        record = Artist.query.get_or_404(artist_id)
        form = ArtistForm(obj=record)
        return render_template(
            'forms/edit_artist.html',
            form=form,
            artist=record)

    except Exception as e:

        print('Error occured when retrieving artists with error" {e}')
        return render_template('500.html'), 500


@artist_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    record = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=record)
    if form.validate():
        try:
            form.populate_obj(record)
            db.session.commit()
            flash(f'Artist {record.name} was updated successfully')
        except Exception as e:
            db.session.rollback()
            flash(f'something went wrong with {record.name}')
        finally:
            db.session.close()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}')

    return redirect(url_for('show_artist', artist_id=artist_id))


