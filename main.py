from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flights.FlightFinder import SearchFlights
from my_forms import AirplaneForm, StockForm
from stocks.Stocks import StocksInfo
import os

app = Flask(__name__)
key = os.environ.get('FLASK_KEY')
app.config['SECRET_KEY'] = key
Bootstrap5(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chess', methods=["GET", "POST"])
def chess():
    pieces = 'white'
    pieces = request.args.get('pieces')
    return render_template("chess.html", pieces=pieces)


@app.route('/thesis', methods=["GET", "POST"])
def thesis():
    return render_template("thesis.html")


@app.route('/stocks', methods=["GET", "POST"])
def stocks():
    flag = 0
    form = StockForm()
    if form.validate_on_submit():
        flag = 1

        stock = StocksInfo(form.stock_name.data)

        print(f"return = {vars(stock)}")
        return render_template("stocks.html", form=stock, flag=flag)
    return render_template("stocks.html", form=form, flag=flag)


@app.route('/flight-deals', methods=["GET", "POST"])
def flights():
    form = AirplaneForm()
    if form.validate_on_submit():
        flights_info = SearchFlights(form.origin.data, form.destination.data, form.max_price.data)
        if (flights_info.flights_found == None):
            flash("Invalid city entered")
        elif (len(flights_info.flights_found) == 0):
            flash("No flights under that price found")

        return render_template("flights.html", form=flights_info, flag=1)
    return render_template("flights.html", form=form, flag=0)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
