"""SQLAlchemy models for Genie."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


DEFAULT_IMAGE_URL = ("/static/screamhead3.png")

class Favorite(db.Model):
    """Connection of a user <-> favorite."""

    __tablename__ = 'favorites'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        nullable=False,
    )

    video_id = db.Column(
        db.String(200),
        nullable=False,
    )



class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(50),
        nullable=False,
    )

    last_name = db.Column(
        db.String(50),
        nullable=False,
    )

    image_url = db.Column(
        db.String(255),
        nullable=False,
        default=DEFAULT_IMAGE_URL,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    favorites = db.relationship('Favorite', backref="user")


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, username, email, password, first_name, last_name, image_url=DEFAULT_IMAGE_URL):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        return user



    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)