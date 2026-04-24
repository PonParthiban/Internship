from flask import Flask, request, render_template,url_for,redirect,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'#here the users is the table name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
   return render_template("view.html", values = users.query.all())
@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
      session.permanent = True 
      user =  request.form["nm"]
      session["user"] = user
      '''found_user = users.query.filter_by(name=user).delete() => to delete 
      for users in found user:
          users.delete()  => multiple user 
      '''
      found_user = users.query.filter_by(name=user).first()
      if found_user:
         session["email"] = found_user.email
      else:
         usr = users(user,"")
         db.session.add(usr)
         db.session.commit()

      flash("login sucessful!")
      return redirect(url_for("user"))
    else:
      if "user" in session:
         flash("Already logged in!")
         return redirect(url_for("user"))
      return render_template("login.html")
@app.route("/user", methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
       user = session["user"]
       if request.method == "POST":
          email = request.form["email"]
          session["email"] = email
          found_user = users.query.filter_by(name=user).first()
          found_user.email = email
          db.session.commit()
          flash("Email was saved")
       else:
          if "email" in session:
           email = session["email"]
       return render_template("user.html", email = email)
    else:
       if "user" in session:
          user = session["user"]
          return f"<h1>{user}<h1/>"
       else:
          flash("you are not logged in")
          return redirect (url_for("login"))
    
@app.route("/logout")
def logout():
   flash(f"You have been logged out!", "info")
   session.pop("user", None)
   session.pop("email",None)
   return redirect (url_for("login"))

if __name__ == '__main__':
    with app.app_context():
     db.create_all()#create if db not created
    app.run(debug=True) 