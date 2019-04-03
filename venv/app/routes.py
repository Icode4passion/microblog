from flask import render_template,flash,redirect,url_for
from app import app , db
from flask_login import current_user, login_user , logout_user , login_required
from app.forms import LoginForm , Registration
from app.models import User

@app.route("/")

@app.route("/index")
@login_required
def index():
	user = {'username': 'Mahesh'}
	posts = [
	{'author':{'username':'JOhn'},'body':'Beautiful Day'},
	{'author':{'username':'Bon'},'body':'Beautiful Day it is'}
	]
	return render_template('index.html', title='Home', posts=posts )
	
	

@app.route('/login', methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash ('Invalid user or password ')
			return redirect(url_for('login'))
		login_user(user,remember=form.remember_me.data)
		next_page = request.args.get(next)
		if not next_page or url_parser(next).netloc != '':
			next_page = url_for('index')
			return redirect(url_for('next_page'))
		return redirect(url_for('next_page'))
	return render_template('login.html',title = 'Sign-In', form = form)


@app.route('/register'  ,methods = ["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	form = Registration()
	if form.validate_on_submit():
		user = User(username= form.username.data , email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Successful Registered...")
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register' , form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))