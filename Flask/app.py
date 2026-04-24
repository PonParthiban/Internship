from flask import Flask, request, render_template,url_for,redirect,session,flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
      session.permanent = True 
      user =  request.form["nm"]
      session["user"] = user
      flash("login sucessful!")
      return redirect(url_for("user"))
    else:
      if "user" in session:
         flash("Already logged in!")
         return redirect(url_for("user"))
      return render_template("login.html")
@app.route("/user")
def user():
    if "user" in session:
       user = session["user"]
       return render_template("user.html", user=user)
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
   return redirect (url_for("login"))

if __name__ == '__main__':
    app.run(debug=True) 