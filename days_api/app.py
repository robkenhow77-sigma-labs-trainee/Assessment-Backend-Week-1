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


def get_difference(data: dict) -> int:
    first = convert_to_datetime(data.get("first"))
    last = convert_to_datetime(data.get("last"))
    difference = get_days_between(first, last)
    return difference


def validate_between_post(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    if len(data) != 2:
        return False
    for key in data.keys():
        if key not in ["first", "last"]:
            return False
    return True

@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({ "message": "Welcome to the Days API." })


@app.route("/between", methods= ["POST"])
def get_days_between_two_dates():
    data = request.json
    if validate_between_post(data):
        difference = get_difference(data)
        add_to_history(request)
        return {"days": difference }, 200
    return {"Bad request LOOK AT TEST"}, 400


@app.route("/weekday", methods= ["POST"])
def get_day_of_the_week():
    data = request.json
    day = convert_to_datetime(data.get("date"))
    day_of_week = get_day_of_week_on(day)
    add_to_history(request)

    return {"weekday": day_of_week}, 200


@app.route("/history", methods= ["GET", "DELETE"])
def get_history():
    args = request.args.to_dict()
    add_to_history(request)

    number = args.get("number")
    if number:
        if number.isnumeric():
            number = int(number)
            if number >= 1 and number <= 20:
                if len(app_history) > 20:
                    return app_history[:20], 200
                return app_history[:number], 200
            
    if len(app_history) > 5:
        return app_history[:5], 200
    return app_history, 200


@app.route("/current_age", methods= ["GET"])
def get_birthday():
    args = request.args.to_dict()
    date_str = args.get("date")
    date_str_list = date_str.split("-")
    date_str_correct_format = ".".join([date_str_list[2], date_str_list[1], date_str_list[0]])
    current_age = get_current_age(convert_to_datetime(date_str_correct_format).date())
    add_to_history(request)

    return {"current_age": current_age}, 200



if __name__ == "__main__":
    app.run(port=8080, debug=True)
