import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app_.config.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(240), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_employee = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, password):
        password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self,password, password)
