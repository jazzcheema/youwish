"""Clears blocked users and gives them access to YouWish."""


from app import app
from models import db, User


def clear_blocked_users():
    with app.app_context():
        blocked_users = User.query.filter(User.blocked).all()

        for user in blocked_users:
            user.blocked = False

        db.session.commit()
        print('''
                      ______
                    .-"      "-.
                   /            \\
       _          |              |          _
      ( \\         |,  .-.  .-.  ,|         / )
       > "=._     | )(__/  \\__)( |     _.=" <
      (_/"=._"=._ |/     /\\     \\| _.="_.="\\_)
             "=._ (_     ^^     _)"_.="
                 "=\__|IIIIII|__/="
                _.="| \\IIIIII/ |"=._
      _     _.="_.="\\          /"=._"=._     _
     ( \\_.="_.="     `--------`     "=._"=._/ )
      > _.="                            "=._ <
     (_/                                    \\_)
''')
