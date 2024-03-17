"""YouWish User views tests."""

# run these tests like:
#
# FLASK_DEBUG=False python -m unittest -v test_youwish_views.py

import os
from unittest import TestCase
from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///genie_test"

from app import app, CURR_USER_KEY, VIDEO_LIMIT

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup(username="u1",
                         email="u1@email.com",
                         password="password",
                         image_url='https://qph.cf2.quoracdn.net/main-qimg-c7fd4a31612d7df200d550ab8f34f3c5',
                         first_name='test_first',
                         last_name='test_last')
        db.session.flush()

        self.u1_id = u1.id


    def tearDown(self):
        db.session.rollback()


    def test_log_in(self):
        """Tests the login route."""

        with app.test_client() as c:

            resp = c.get("/login")
            html = resp.get_data(as_text=True)

            self.assertIn('Welcome back', html)
            self.assertEqual(resp.status_code, 200)


    def test_log_in_session(self):
        """Tests the route for processing after login--> lands on the Wish page."""

        with app.test_client() as c:

            resp = c.post("/login", data={"username": "u1",
                                          "password": "password"},
                                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('<!-- wish page -->', html)
            self.assertEqual(resp.status_code, 200)


    def test_log_out(self):
        """Tests that on logout, user is redirected back to homepage."""

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.post("/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Signup", html)
            self.assertEqual(resp.status_code, 200)


    def test_invalid_user_accessing_wish_page(self):
        """Tests that if an entity is not signed in, they cannot access
        the wish page and get redirected to home."""

        with app.test_client() as c:

            resp = c.get("/wish", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Signup", html)
            self.assertEqual(resp.status_code, 200)


    def test_invalid_user_accessing_genie(self):
        """Tests that if an entity is not signed in, they cannot access
        the genie, and get redirected to home."""

        with app.test_client() as c:

            resp = c.get("/genie", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Signup", html)
            self.assertEqual(resp.status_code, 200)


    def test_video_limit_not_met_user_accessing_genie(self):
        """Tests that if a user is signed in, but they have not reached max video
        limit, they cannot access the genie, and get redirected to home."""

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
                sess['video_limit'] = 2

            resp = c.get("/genie", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Signup", html)
            self.assertEqual(resp.status_code, 200)


    def test_video_limit_met_user_accessing_genie(self):
        """Tests that if a user is signed in, and have reached max video
        limit, they can access the genie."""

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
                sess['video_limit'] = 3

            resp = c.get("/genie", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("<!-- genie page -->", html)
            self.assertEqual(resp.status_code, 200)


    def test_user_wish(self):
        """Tests that if a user is signed in, they have access to the lamp and
        can make a wish. Important note: this may take two attempts if YouTube
        API does not return video(s) that match criteria on search + views."""

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.post("/wish")

            self.assertEqual(resp.status_code, 201)


    def test_user_max_video_limit(self):
        """Tests that if a user is signed in and have reached their max video
        limit(3), they cannot make a wish, and get a 403 resp."""

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
                sess['video_limit'] = VIDEO_LIMIT

            resp = c.post("/wish")

            self.assertEqual(resp.status_code, 403)


    def test_user_blocked(self):
        """Tests if user is blocked, they cannot access the site."""
        test_user = User.query.get_or_404(self.u1_id)
        test_user.blocked=True
        db.session.commit()

        with app.test_client() as c:

            resp = c.get("/wish", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<!-- homepage -->', html)





