from flask import Flask, redirect, url_for, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

# mysql = MySQL()
# mysql.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutHome")
def aboutHome():
    return render_template("/aboutHome/aboutHome.html")

@app.route("/aboutHome/<aboutName>")
def aboutPage(aboutName):
    print(aboutName)
    url = "/aboutHome/"+aboutName
    print(url)
    return render_template({url})

@app.route('/search', methods=['GET', 'POST'])
def search():
    # if request.method == "POST":
        # book = request.form['book']
        # # search by author or book
        # cursor.execute("SELECT name, author from Book WHERE name LIKE %s OR author LIKE %s", (book, book))
        # conn.commit()
        # data = cursor.fetchall()
        # # all in the search box will return all the tuples
        # if len(data) == 0 and book == 'all': 
        #     cursor.execute("SELECT name, author from Book")
        #     conn.commit()
        #     data = cursor.fetchall()
        # return render_template('search.html', data=data)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug = True)