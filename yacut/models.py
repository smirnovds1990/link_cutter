from datetime import datetime

from . import db
from .constants import MAX_CUSTOM_ID_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(
        db.String(MAX_CUSTOM_ID_LENGTH), unique=True, nullable=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
