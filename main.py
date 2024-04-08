from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flights.FlightFinder import SearchFlights
from forms.airplane_form import AirplaneForm
import os


app = Flask(__name__)
key = os.environ.get('FLASK_KEY')
app.config['SECRET_KEY'] = key
Bootstrap5(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chess', methods = ["GET","POST"])
def chess():

    pieces = 'white'
    pieces = request.args.get('pieces')
    return render_template("chess.html", pieces = pieces)

@app.route('/flight-deals', methods=["GET","POST"])
def flights():
    form = AirplaneForm()
    if form.validate_on_submit():
        flights_info = SearchFlights(form.origin.data, form.destination.data, form.max_price.data)
        if (flights_info.flights_found == None ):
            flash("Invalid city entered")
        elif (len(flights_info.flights_found) == 0):
            flash("No flights under that price found")

        return render_template("flights.html", form = flights_info, flag=1)
    return render_template("flights.html", form = form, flag = 0)



if __name__ == "__main__":
    app.run(debug=False, port=5001)
