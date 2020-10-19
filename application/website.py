from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutHome")
def aboutHome():
    return render_template("aboutHome.html")

@app.route("/<aboutName>")
def aboutPage(aboutName):
    return render_template({aboutName})

if __name__ == '__main__':
    app.run(debug = True)