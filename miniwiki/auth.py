import hmac

from bcrypt import hashpw
from flask import abort, redirect, render_template, request, session


class AnonymousAuthBackend(object):
    get_login = False
    post_login = False
    get_logout = False

    def __init__(self, config):
        pass

    def is_logged_in(self):
        return True


class SimpleAuthBackend(AnonymousAuthBackend):
    '''
    A simple hard-coded username : password auth backend. Passwords hashed using bcrpyt, to create
    a new user, generate the password by:

        hashpw(b'PASSWORD', gensalt(N_BCRYPT_ROUNDS))
    '''

    def __init__(self, config):
        auth_settings = config['auth_backend_settings']

        self.users = auth_settings.get('users')

        if not self.users:
            raise ValueError(
                'Must provide `config.auth_backend_settings.users` with `SimpleAuthBackend`!',
            )

    def is_logged_in(self):
        return session.get('logged_in')

    def get_login(self):
        return render_template('simple_login.html')

    def post_login(self):
        username = request.form['username']

        if username not in self.users:
            abort(401, 'Invalid username or password')

        password = request.form['password'].encode()
        hashed = self.users[username]
        if isinstance(hashed, str):
            hashed = hashed.encode()

        if not hmac.compare_digest(
            hashpw(password, hashed),
            hashed,
        ):
            abort(401, 'Invalid username or password')

        session['logged_in'] = True
        session['logged_in_username'] = username
        return redirect('/')

    def get_logout(self):
        session.pop('logged_in', None)
        session.pop('logged_in_username', None)
        return redirect('/')
