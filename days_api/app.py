"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({ "message": "Welcome to the Days API." })


@app.route("/between", methods= ["POST"])
def get_days_between_two_dates():
    data = request.json
    first = convert_to_datetime(data.get("first"))
    last = convert_to_datetime(data.get("last"))
    return get_days_between(first, last)

@app.route("/weekday", methods= ["POST"])
def get_day_of_the_week():
    pass


@app.route("/history", methods= ["POST", "DELETE"])
def get_history():
    pass


@app.route("/current_age", methods= ["GET"])
def get_birthday():
    pass




if __name__ == "__main__":
    app.run(port=8080, debug=True)
