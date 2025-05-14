from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, User, Bet
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' in session:
        bets = Bet.query.order_by(Bet.id.desc()).all()
        return render_template('dashboard.html', bets=bets)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
        flash('Credenziali non valide')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'], method='sha256')
        new_user = User(email=request.form['email'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione completata. Accedi ora.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        new_bet = Bet(type=request.form['type'], description=request.form['description'])
        db.session.add(new_bet)
        db.session.commit()
        flash('Giocata aggiunta!')
    bets = Bet.query.order_by(Bet.id.desc()).all()
    return render_template('admin.html', bets=bets)

if __name__ == '__main__':
    app.run(debug=True)
