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
    difference = get_days_between(first, last)
    return {"days": difference }, 200


@app.route("/weekday", methods= ["POST"])
def get_day_of_the_week():
    data = request.json
    day = convert_to_datetime(data.get("date"))
    day_of_week = get_day_of_week_on(day)
    return {"weekday": day_of_week}, 200


@app.route("/history", methods= ["POST", "DELETE"])
def get_history():
    pass


@app.route("/current_age", methods= ["GET"])
def get_birthday():
    args = request.args.to_dict()
    date_str = args.get("date")
    date_str_list = date_str.split("-")
    date_str_correct_format = ".".join([date_str_list[2], date_str_list[1], date_str_list[0]])
    current_age = get_current_age(convert_to_datetime(date_str_correct_format).date())
    return {"current_age": current_age}, 200



if __name__ == "__main__":
    app.run(port=8080, debug=True)
