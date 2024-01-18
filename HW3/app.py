from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

from forms import RegisterForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = b'c260bd38ddcd0dad747a816dd21c0aff162c88000d2016d11f42cf9c34c08295'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(first_name=form.name.data, last_name=form.surname.data, email=form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return 'New user has been added to database!'
    return render_template('register.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
