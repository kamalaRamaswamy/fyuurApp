#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    website_link = db.Column(db.String(120))
    looking_for_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))
    shows = db.relationship('Show', backref='venue', lazy=True)

def __repr__(self):
        return '<Venue name %r>' %self.name


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_for_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(1000))
    shows = db.relationship('Show', backref='artist', lazy=True)

def __repr__(self):
    return '<Artist name %r>' %self.name

class Show(db.Model):
    __tablename__ = 'show'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    
def __repr__(self):
    return 'Show %r%r'.format(self.artist_id, self.venue_id)


# with app.app_context():
#     db.create_all()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  states = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  response = []
  print(states)
  for state in states:
    venues = Venue.query.filter_by(state=state.state).filter_by(city=state.city).all()
    print(venues)
    location = []
    for venue in venues:
      location.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
            })
    response.append({
                'city': state.city,
                'state': state.state,
                'venues': location
            })
  
  return render_template('pages/venues.html', areas=response);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  term = request.form.get("search_term", "")
  result = Venue.query.filter(Venue.name.ilike(f"%{term}%")).all()
  data = []
  for venue in result:
    data.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
    })
  print(data)

  response = {
      "count": len(result),
      "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  if data is None:
        abort(404)

  print(data)
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website_link = request.form['website_link']
    looking_for_talent = True if 'looking_for_talent' in request.form else False 
    seeking_description = request.form['seeking_description']

    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, looking_for_talent=looking_for_talent, seeking_description=seeking_description)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] +' was successfully listed!')
  
  except Exception as ex:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
# TODO
# 
#   try:
#     venue = Venue.query.get(venue_id)
#     db.session.delete(venue)
#     db.session.commit()
#     flash('Venue ' + request.form['name'] +' was successfully deleted!')

#   except Exception as ex:
#     flash('An error occurred. Venue ' + request.form['name'] + ' could not be deleted.')
  
  return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = db.session.query(Artist).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  term = request.form.get("search_term", "")
  result = Artist.query.filter(Artist.name.ilike(f"%{term}%")).all()
  data = []
  for artist in result:
    data.append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
    })
  print(data)

  response = {
      "count": len(result),
      "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get(artist_id)
  if data is None:
        abort(404)

  print(data)
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------

# TODO
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try: 
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres'),
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website_link = request.form['website_link']
    looking_for_venue = True if 'looking_for_venue' in request.form else False
    seeking_description = request.form['seeking_description']

    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, looking_for_venue=looking_for_venue, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except Exception as ex:
    flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
