#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = []
    for event in Event.query.all():
        body = {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        events.append(body)
    return jsonify(events), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    sessions = []
    for session in Session.query.filter_by(event_id=id).all():
        body = {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat() if session.start_time else None
        }
        sessions.append(body)
    if not sessions:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(sessions), 200
    

@app.route('/speakers')
def get_speakers():
    speakers = []
    for speaker in Speaker.query.all():
        body = {
            "id": speaker.id,
            "name": speaker.name
        }
        speakers.append(body)
    return jsonify(speakers), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = db.session.get(Speaker, id)
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    body = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
    }
    return jsonify(body), 200


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    speakers = []
    for speaker in Speaker.query.join(Session.speakers).filter(Session.id == id).all():
        body = {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
        }
        speakers.append(body)
    if not speakers:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(speakers), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)