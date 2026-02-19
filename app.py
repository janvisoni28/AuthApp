from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # 🔹 Validation Checks
        if not name:
            flash("Name is required!")
            return redirect(url_for('register'))

        if not email:
            flash("Email is required!")
            return redirect(url_for('register'))

        if not password:
            flash("Password is required!")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters!")
            return redirect(url_for('register'))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for('register'))

        # Save user
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!")
        return redirect(url_for('register'))

    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)
@app.route("/")
def home():
    return "AuthApp is running successfully 🚀"
