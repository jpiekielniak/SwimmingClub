import os
import sys
from flask import Flask, session, render_template, request

# Ensure the project root is in sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import data_tools
import conversion_tools


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "change_this_secret")

    @app.route("/", methods=["GET"])
    def index():
        return render_template(
            "index.html",
            title="Welcome to the Swimming Club Website",
        )

    @app.route("/sessions", methods=["GET"])
    def show_sessions():
        sessions = data_tools.get_sessions()
        dates = [row[0].split(" ")[0] for row in sessions]
        return render_template(
            "select.html",
            title="Select a training session date",
            url="/swimmers",
            select_id="chosen_date",
            select_text="training session date",
            data=dates,
        )

    @app.route("/swimmers", methods=["POST"])
    def show_swimmers():
        session["chosen_date"] = request.form["chosen_date"]
        swimmers = data_tools.get_swimmers_by_session(session["chosen_date"])
        swimmer_list = [f"{swimmer[0]}-{swimmer[1]}" for swimmer in swimmers]
        return render_template(
            "select.html",
            title="Select a swimmer",
            url="/events",
            select_id="swimmer",
            select_text="swimmer",
            data=sorted(swimmer_list),
        )

    @app.route("/events", methods=["POST"])
    def show_events():
        session["swimmer"], session["age"] = request.form["swimmer"].split("-")
        events = data_tools.get_events_for_swimmer(
            session["swimmer"], session["age"], session["chosen_date"]
        )
        event_list = [f"{event[0]} {event[1]}" for event in events]
        return render_template(
            "select.html",
            title="Select an event",
            url="/chart",
            select_id="event",
            select_text="event",
            data=event_list,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
