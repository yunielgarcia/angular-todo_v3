from flask import g
from flask_httpauth import HTTPBasicAuth

import models

basic_auth = HTTPBasicAuth()
auth = basic_auth


@basic_auth.verify_password
def verify_password(email_or_username, psw):
    try:
        user = models.User.get(
            (models.User.email == email_or_username) |
            (models.User.username == email_or_username)
        )
        if not user.verify_password(psw):
            return False
    except models.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True
