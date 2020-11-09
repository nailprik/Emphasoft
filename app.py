from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from oauth1 import OAuthSignIn
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = '1234'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['OAUTH_CREDENTIALS'] = {
    'google': {
        'id': '483369488098-bolg2ajue9pb71dqo9cdion87avpdu09.apps.googleusercontent.com',
        'secret': 'tSGMt4t1u2t9TJQ7v23_7Lg1'
    },
    'github': {
        'id': '',
        'secret': ''
    }
}
UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    # Класс пользователя
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20))
    l_name = db.Column(db.String(20))
    m_name = db.Column(db.String(20))
    email = db.Column(db.String(64), nullable=False)
    about = db.Column(db.String(300))
    avatar = db.Column(db.String(300))


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/')
def index():
    if current_user.is_anonymous:
        return redirect('/auth')
    return redirect('/users')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/users')
def users():
    if current_user.f_name and current_user.l_name and current_user.m_name:
        users = User.query.order_by(User.id).all()
        return render_template('users.html', current_user=current_user, users=users)
    else:
        return redirect(url_for('edit',id = current_user.id))


@app.route('/users/<int:id>')
def user_info(id):
    if current_user.f_name and current_user.l_name and current_user.m_name:
        user = User.query.get(id)
        return render_template('user_info.html', current_user=current_user, user=user)
    else:
        return redirect(url_for('edit',id = current_user.id))

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if current_user.is_anonymous or current_user.id != id:
        return redirect('/')
    user = User.query.get(id)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], user.email + filename))
            if user.avatar:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.avatar))
            user = User.query.get(current_user.id)
            user.avatar = user.email + filename
        user.f_name = request.form['f_name']
        user.l_name = request.form['l_name']
        user.m_name = request.form['m_name']
        user.about = request.form['about']

        db.session.commit()
        return redirect('/users/' + str(id))

    else:
        return render_template('edit.html', current_user=current_user, user=user)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect('/')
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect('/')
    oauth = OAuthSignIn.get_provider(provider)
    email = oauth.callback()
    if email is None:
        return redirect('/')
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
        return redirect('/users/' + str(user.id) + '/edit')
    login_user(user, True)
    return redirect('/users/' + str(user.id))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/images/<filename>')
def images(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)
