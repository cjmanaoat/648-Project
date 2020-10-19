from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # message = '''<center> Software Engineering class SFSU <br>
    #             Fall 2020 <br>
    #             Section 3 <br>
    #             Team 7 <br>
    #             </center>'''
    #return message
    return render_template("index.html")

@app.route("/test")
def test():
    # message = '''<center> Software Engineering class SFSU <br>
    #             Fall 2020 <br>
    #             Section 3 <br>
    #             Team 7 <br>
    #             </center>'''
    #return message
    return render_template("new.html")

if __name__ == '__main__':
    app.run(debug = True)
