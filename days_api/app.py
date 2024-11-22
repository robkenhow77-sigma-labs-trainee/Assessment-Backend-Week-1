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
        return False, {"error": "Missing required data."}
    
    if len(data) != 2:
        return False, {"error": "Missing required data."}
    
    for key in data.keys():
        if key not in ["first", "last"]:
            return False, {"error": "Missing required data."}

    for key in data.keys():
        try:
            valid_date = datetime.strptime(data.get(key), "%d.%m.%Y")
        except ValueError:
            return False, {"error": "Unable to convert value to datetime."}

    return True, None


def validate_weekday_post(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    
    if len(data) != 1:
        return False
    
    for key in data.keys():
        if key not in ["date"]:
            return False
        
    for key in data.keys():
        try:
            convert_to_datetime(data.get(key))
        except ValueError:
            return False
        
    return True


def validate_birthday(date_str: str) -> bool:
    try:
        date_str_list = date_str.split("-")
        date_str_correct_format = ".".join([date_str_list[2], date_str_list[1], date_str_list[0]])
        current_age = get_current_age(convert_to_datetime(date_str_correct_format).date())
    except ValueError:
        return False
    return True


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({ "message": "Welcome to the Days API." })


@app.route("/between", methods= ["POST"])
def get_days_between_two_dates():
    data = request.json
    error, message = validate_between_post(data)
    if error:
        difference = get_difference(data)
        add_to_history(request)
        return {"days": difference }, 200
    return message, 400


@app.route("/weekday", methods= ["POST"])
def get_day_of_the_week():
    data = request.json
    if validate_weekday_post(data):
        day = convert_to_datetime(data.get("date"))
        day_of_week = get_day_of_week_on(day)
        add_to_history(request)
        return {"weekday": day_of_week}, 200
    return{"error": "Missing required data."}, 400


@app.route("/history", methods= ["GET", "DELETE"])
def get_history():
    args = request.args.to_dict()
    if request.method == "POST":
        number = args.get("number")
        if number:
            if number.isnumeric():
                number = int(number)
                if number >= 1 and number <= 20:
                    add_to_history(request)
                    if len(app_history) > 20:
                        return app_history[:-20], 200
                    return app_history[:-number], 200
        
        add_to_history(request)        
        if len(app_history) > 5:
            return app_history[:-5], 200
        
        return app_history, 200
    
    if request.method == "DELETE":
        app_history.clear()
        add_to_history(request)
        return { "status": "History cleared" }, 200


@app.route("/current_age", methods= ["GET"])
def get_birthday():
    args = request.args.to_dict()
    date_str = args.get("date")
    if validate_birthday(date_str):
        date_str_list = date_str.split("-")
        date_str_correct_format = ".".join([date_str_list[2], date_str_list[1], date_str_list[0]])
        current_age = get_current_age(convert_to_datetime(date_str_correct_format).date())
        add_to_history(request)
        return {"current_age": current_age}, 200
    return {"error": "Value for data parameter is invalid."}, 400


if __name__ == "__main__":
    app.run(port=8080, debug=True)
