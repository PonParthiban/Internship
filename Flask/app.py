from flask import Flask, request, render_template,url_for,redirect
app = Flask(__name__)

@app.route("/")
def home():
    return "hello this is home page \n <h2>hello</h2>"

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)