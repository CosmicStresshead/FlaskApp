# Imports

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from data import article_data


# Classes

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('email', [validators.Length(min=6, max=50)])	
	password = PasswordField('Password', [
				validators.DataRequired(),
				validators.EqualTo('confirm', message="Passwords do not match")
			   ])
	confirm = PasswordField('Confirm Password')


# Create app object and grab data

app = Flask(__name__)
articles_data = article_data()


# Configure MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# Initialise MySQL

mysql = MySQL(app)





# Routes

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/articles")
def articles():    
    return render_template("articles.html", articles = articles_data)

@app.route("/article/<string:id>/")
def article(id):    
    return render_template("article.html", id=id)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.username.data))
		
		# submit fields to db
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, email, username, password), VALUES(%s, %s, %s, %s)", (name, email, username, password))
		mysql.connection.commit()
		cur.close()

		flash("You are now registered and can log in", "success")

		redirect(url_for('home'))


	return render_template("register.html", form=form)


# Main
if __name__ == "__main__":
    app.run(debug=True)