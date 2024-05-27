import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Favorite
from googleapiclient.discovery import build
from wordfinder import WordFinder
from random import choice
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from forms import CSRFProtectForm, LoginForm, UserAddForm, ForgotPasswordForm, NewPasswordForm
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

toolbar = DebugToolbarExtension(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'livescreamrules@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD_GMAIL']
app.config['MAIL_DEFAULT_SENDER'] = 'livescreamrules@gmail.com'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

mail = Mail(app)

connect_db(app)

YOUTUBE_API = os.environ['YOUTUBE_API']
YOUTUBE_API_2 = os.environ['YOUTUBE_API_2']
YOUTUBE_API_3 = os.environ['YOUTUBE_API_3']
YOUTUBE_API_4 = os.environ['YOUTUBE_API_4']
YOUTUBE_API_5 = os.environ['YOUTUBE_API_5']
YOUTUBE_API_6 = os.environ['YOUTUBE_API_6']
YOUTUBE_API_7 = os.environ['YOUTUBE_API_7']

CURR_USER_KEY = "curr_user"
VIDEO_LIMIT = 3

##############################################################################


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_to_g():
    """Add CSRF token to Flask global"""
    g.csrf_form = CSRFProtectForm()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# Main Routes
##############################################################################


@app.get('/')
def display_homepage():
    """Displays the index/home page. Options for signup and login."""

    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        flash("You're already a user")
        return redirect('/')

    do_logout()

    form = UserAddForm()

    if form.validate_on_submit():
        if User.query.filter(form.email.data == User.email).one_or_none():
            form.email.errors = ["Email already exists"]
            return render_template('signup.html', form=form)

        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data,
                last_name=form.last_name.data,
                first_name=form.first_name.data,
            )

            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/wish")

    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    form = LoginForm()

    if CURR_USER_KEY in session:
        return redirect("/wish")

    do_logout()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data,
        )

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/wish")

        flash("Invalid credentials", 'danger')

    return render_template('login.html', form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")

    if g.csrf_form.validate_on_submit():
        do_logout()
        flash(f"You've been logged out")
        return redirect('/')
    else:
        flash(f"You don't have access")
        raise Unauthorized()

# Favorite/Unfavorite Video & Show Savorites
##############################################################################


@app.post('/favorite_video/<video_id>/')
def favorite_and_unfavorite_video(video_id):
    """Adds video to user's favorites list."""

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")

    # if  g.csrf_form.validate_on_submit():
    if request.method == 'POST':
        unfavorite = Favorite.query.filter_by(user_id=g.user.id,
                                              video_id=video_id).first()

        if unfavorite:
            db.session.delete(unfavorite)
            db.session.commit()
            flash('Removed video')
            return redirect(f"/favorite/{g.user.id}")

        else:
            favorite = Favorite(user_id=g.user.id, video_id=video_id)
            g.user.favorites.append(favorite)
            db.session.commit()
            favorited = {
                'data': 'Success! Video Favorited',
            }
            return (jsonify(favorited), 201)

    flash("Access unauthorized", "danger")
    return redirect("/")


@app.get('/favorite/<int:user_id>')
def show_user_favorites(user_id):
    """Render page to show current user's favorited videos."""

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")

    if g.user.blocked:
        flash("You're blocked until midnight...")
        return redirect('/')

    if g.user.id != user_id:
        return redirect(f"/favorite/{g.user.id}")

    user = User.query.get_or_404(user_id)
    return render_template('favorites.html', user=user)

# Edit User Profile
################################################################################


@app.route('/edit', methods=["GET", "POST"])
def edit_user_profile():
    """Page to edit user profile."""

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")

    if g.user.blocked:
        flash("You're blocked until midnight...")
        return redirect('/')

    form = UserAddForm(obj=g.user)

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data,
        )

        if user:
            g.user.image_url = form.image_url.data
            g.user.first_name = form.first_name.data
            g.user.last_name = form.last_name.data
            g.user.email = form.email.data

            db.session.commit()
            flash('Profile updated')
            return redirect('/wish')

        else:
            flash('Wrong password')

    return render_template('edit-user.html', form=form)


# Youtube API / Wish Page
##############################################################################

@app.route('/wish', methods=['GET', 'POST'])
def youtube_search():
    """Renders page where videos will display. If a POST request is made
    to this endpoint it will return JSON data to the client from the YouTube
    API. This endpoint also keeps count of how many videos the user has currently
    watched-- if they exceed 3 videos (max number), they will be redirected
    to an alternate page. JSON data will look like:
    JSON{
            "video_data":
                'id': random_video_choice['id'],
                'views': random_video_choice['statistics']['viewCount'],
                'userId': user_id
        }
    }
    """

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")

    if g.user.blocked:
        flash("You're blocked until midnight...")
        return redirect('/')

    if request.method == 'POST':

        if 'video_limit' not in session:
            session['video_limit'] = 0

        if session['video_limit'] >= VIDEO_LIMIT:
            flash('Wishes expired for 24 hours... Please come back later.')
            return redirect('/genie', code=403)

        # Reads words from txt file, and selects a random word to input
        # into query for YouTube API.
        word_find = WordFinder('words.txt')
        random_word = word_find.random()

        query = f"{random_word}"
        # change max result to 20
        max_results = 50
        order = 'date'
        view_count_min = 200
        view_count_max = 1200
        video_cat_ids = [1, 2, 10, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                         31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
        random_video_cat_id = choice(video_cat_ids)

        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_2)

        # Call Youtube API and retrieve videos with input from random word
        # and random category. Cannot pull video stats with this call,
        # secondary call is needed.
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            videoEmbeddable='true',
            maxResults=max_results,
            order=order,
            videoDuration='short',
            videoCategoryId=f"{random_video_cat_id}"
        ).execute()

        video_ids = [item['id']['videoId']
                     for item in search_response['items']]
        videos = []

        # For every video retrieved, make another call to the YouTube API to
        # retrieve stats. Used for tracking view count to see if it matches
        # our criteria between min & max views.
        for video_id in video_ids:
            video_response = youtube.videos().list(
                id=video_id,
                part='snippet,statistics',
            ).execute()

            for video in video_response['items']:
                view_count = int(video['statistics']['viewCount'])
                if (view_count >= view_count_min) and (view_count <= view_count_max):
                    videos.append(video)

        if videos:
            session['video_limit'] += 1
            # Selects a single random video in a list that is
            # between min-max view count.
            random_video_choice = choice(videos)
            user_id = session[CURR_USER_KEY]

            # JSON response to send the client.
            video_data = {
                'id': random_video_choice['id'],
                'views': random_video_choice['statistics']['viewCount'],
                'userId': user_id
            }
            print('''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣷⡀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡟⢿⣿⣿⠃⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣶⡄⠀⠀⠀⠹⢿⣷⣦⣍⡁⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣅⡀⠀⠀⠀⠀⠈⠙⠻⣿⣦⠀
                    ⠀⣴⠿⠿⢷⡄⠀⠀⠴⠿⠿⠿⠿⠿⠿⠆⠀⠀⠀⠀⣀⣤⣴⣿⣿⡿⠟
                    ⠘⣿⡀⠀⠈⣿⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⠿⠋⠀⠀
                    ⠀⠙⢷⣤⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
                    ⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠛⠋⠉⠻⠿⣿⣿⣿⣿⣿⣿⠿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣼⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀''')
            return (jsonify(video_data), 201)

    top_users = check_blocked_total()
    return render_template('display.html', video=None, top_users=top_users)


# Page for Genie to appear
################################################################################

@app.get('/genie')
def show_genie():
    """Displays genie, and shows timer for when the user can return."""

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")

    if 'video_limit' not in session:
        flash('Access blocked')
        return redirect('/')

    if session['video_limit'] < 3:
        flash('Access blocked')
        return redirect('/')

    if g.user.blocked:
        flash("You're blocked until midnight...")
        return redirect('/')

    g.user.blocked = True

    if g.user.blocked_total is None:
        g.user.blocked_total = 1
    else:
        g.user.blocked_total += 1

    db.session.commit()
    print('''
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⢿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠹⠿⠛⣁⣤⣤⣈⠛⠿⠏⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣀⣤⣴⣶⣤⣈⠙⠻⠟⠋⣁⣤⣶⣦⣤⣀⠀⠀⠀⠀
    ⠀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣷⣤⠀
    ⣾⣿⣿⣿⣿⣿⣧⣀⣀⣀⣀⣀⡀⠀⢀⣀⣠⣿⣿⣿⣿⣿⣿⣷
    ⠙⠿⣿⣿⣿⣿⣿⣿⠿⠿⠋⠁⠀⠶⢿⣿⣿⣿⣿⣿⣿⠿⠿⠋
    ⠀⠀⠀⠀⠀⣀⣀⣤⣤⣶⣾⣿⣷⣶⣤⣤⣀⣀⣀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⠿⠟⠛⢉⣄⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢤⣤⣶⣾⣿⣿⣿⣶⣶⣶⠶⠒⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠙⠛⠉⠉⠉⠀⠀⠀⠀
    ''')
    return render_template('genie-timer.html')


# Forgot Password & New Password entry
################################################################################

@app.route('/forgot', methods=['GET', 'POST'])
def get_user_password():
    """Sends email to user with forgotten password, includes token to use for
    new password."""

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            token = serializer.dumps(form.email.data)
            reset_url = f"http://localhost:5001/reset/{token}"
            send_password(form.email.data, reset_url)
            flash('Password reset information sent to email')
            return redirect('/login')
        else:
            flash('No email address found on record')
            return redirect('/forgot')

    return render_template('forgot.html', form=form)


def send_password(email, reset_url):
    subject = 'Password Reset Request'
    body = f"Click the link to reset your password for your YouWish account: {reset_url}"
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Resets user password."""

    form = NewPasswordForm()

    if form.validate_on_submit():
        email = serializer.loads(token)
        new_password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user:
            hashed_pwd = bcrypt.generate_password_hash(
                new_password).decode('UTF-8')
            user.password = hashed_pwd
            db.session.commit()
            flash('Success!')
            return redirect('/login')
        else:
            return redirect('/')

    return render_template('reset.html', token=token, form=form)


# Clear blocked users (for use w/ cron)
################################################################################


def clear_blocked_users():
    """Checks for any blocked users in databse and turns them to false."""
    blocked_users = User.query.filter(User.blocked == True).all()

    for user in blocked_users:
        user.blocked = False

    db.session.commit()
    print('cleared user')
    print("""
⠀⠀⠀⠀⣀⠤⠔⠒⠒⠒⠒⠒⠒⠒⠦⢄⣀⠀⠀⠀⠀
⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢄⠀⠀
⢀⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⠀
⢸⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢢⠈⡇
⢸⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⡇
⠘⡆⢸⠀⢀⣀⣤⣄⡀⠀⠀⠀⢀⣤⣤⣄⡀⠀⡇⡸⠀
⠀⠘⣾⠀⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⣿⣿⣿⠀⡗⠁⠀
⠀⠀⣿⠀⠙⢿⣿⠿⠃⢠⢠⡀⠙⠿⣿⠿⠃⠀⡇⠀⠀
⠀⠀⠘⣄⡀⠀⠀⠀⢠⣿⢸⣿⠀⠀⠀⠀⠀⣠⠇⠀⠀
⠀⠀⠀⠀⡏⢷⡄⠀⠘⠟⠈⠿⠁⠀⢠⡞⡹⠁⠀⠀⠀
⠀⠀⠀⠀⢹⠸⠘⢢⢠⠤⠤⡤⡄⢰⢡⠁⡇⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠣⣹⢸⠒⠒⡗⡇⣩⠌⢀⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠈⢧⡀⠀⠉⠉⠉⠉⠁⠀⣀⠜⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠉⠓⠢⠤⠤⠤⠔⠊⠁⠀⠀⠀⠀
""")


def check_blocked_total():
    """Checks the blocked users total and stores top three users in a list."""
    top_blocked_users = User.query.filter(User.blocked_total >= 1).order_by(
        User.blocked_total.desc()).limit(3).all()

    return top_blocked_users
