from src.server.flask_server import db
from sqlalchemy import LargeBinary


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(1000))
    created = db.Column(db.DATETIME)
    image = db.Column(db.Text, nullable=True)
    resume = db.Column(db.Text, nullable=True)
    git = db.Column(db.String(100))
    projects = db.Column(db.String(100000))
    about_me = db.Column(db.String(), nullable=True)
    profile = db.Column(db.Text, nullable=True)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
