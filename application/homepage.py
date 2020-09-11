from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def homepage():
  return render_template("homepage.html")
  
@app.route("/aboutus")
def about():
  return render_template("aboutjpak2018.html")
  
if __name__ == "__main__":
  app.run(debug=True)
