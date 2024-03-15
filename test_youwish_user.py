"""YouWish User Model tests."""

# run these tests like:
#
# FLASK_DEBUG=False python -m unittest -v test_youwish_user.py

import os
from unittest import TestCase
from models import db, User, Favorite

os.environ['DATABASE_URL'] = "postgresql:///genie_test"

from app import app

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup(username="u1",
                         email="u1@email.com",
                         password="password",
                         image_url='https://qph.cf2.quoracdn.net/main-qimg-c7fd4a31612d7df200d550ab8f34f3c5',
                         first_name='test_first',
                         last_name='test_last')
        db.session.flush()

        db.session.commit()

        self.u1_id = u1.id

    def tearDown(self):
        db.session.rollback()


    def test_user_model(self):
        """Tests that user created has no favorites."""
        u1 = User.query.get(self.u1_id)

        self.assertEqual(len(u1.favorites), 0)


    def test_user_favorite(self):
        """Tests that user has favorited a video."""
        u1 = User.query.get(self.u1_id)
        f1 = Favorite(user_id=u1.id, video_id='i1jcU42HQTQ')

        u1.favorites.append(f1)
        db.session.commit()

        self.assertIn(f1, u1.favorites)
        self.assertEqual(len(u1.favorites), 1)


    def test_user_signup_on_valid(self):
        """Tests that a new user is allowed to sign up."""
        u2 = User.signup(username="u2",
                         email="u2@email.com",
                         password="password",
                         image_url='https://qph.cf2.quoracdn.net/main-qimg-c7fd4a31612d7df200d550ab8f34f3c5',
                         first_name='test_first2',
                         last_name='test_last2')
        db.session.flush()

        test_found_user = User.query.filter_by(username = 'u2').first()

        self.assertTrue(u2 == test_found_user)


    def test_user_authenticate(self):
        """Tests authentication of existing user with credentials provided."""
        u1 = User.query.get(self.u1_id)
        test_user = User.authenticate(u1.username, 'password')
        self.assertTrue(test_user == u1)


    def test_user_username_fail_authenticate(self):
        """Tests that user does not authenticate when wrong username is provided."""
        u1 = User.query.get(self.u1_id)
        test_user = User.authenticate('failed', 'password')
        self.assertFalse(test_user == u1)

