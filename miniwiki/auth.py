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
    def __init__(self, config):
        self.users = config['auth_backend_settings'].get('users')
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
        password = request.form['password']

        if (username, password) not in self.users:
            abort(401, 'Invalid username or password')

        session['logged_in'] = True
        return redirect('/')

    def get_logout(self):
        session.pop('logged_in', None)
        return redirect('/')
