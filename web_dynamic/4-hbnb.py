#!/usr/bin/python3
"""Script that starts a Flask web application
listening on 0.0.0.0:5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
import uuid
app = Flask(__name__)


@app.route("/4-hbnb/", strict_slashes=False)
def hbnb():
    """Display an HTML page with filters for states, amenities, and places"""
    states = storage.all(State)
    sorted_states_list = sorted(states.values(), key=lambda state: state.name)
    amenities = storage.all(Amenity)
    sorted_amenities_list = sorted(amenities.values(), key=lambda amenity: amenity.name)
    places = storage.all(Place)
    sorted_places_list = sorted(places.values(), key=lambda place: place.name)

    users = storage.all(User)
    for place in sorted_places_list:
        place.user = users.get('User.' + place.user_id)

    return render_template('4-hbnb.html',
                           states=sorted_states_list,
                           amenities=sorted_amenities_list,
                           places=sorted_places_list,
                           cache_id=str(uuid.uuid4()))


@app.teardown_appcontext
def close_storage(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
