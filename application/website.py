from flask import Flask, redirect, url_for, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'trademartadmin'
app.config['MYSQL_DATABASE_DB'] = 'Trademart'
app.config['MYSQL_DATABASE_HOST'] = 'trademart.c9x2rihy8ycd.us-west-1.rds.amazonaws.com'


mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutHome")
def aboutHome():
    return render_template("/aboutHome/aboutHome.html")

@app.route("/aboutHome/<aboutName>")
def aboutPage(aboutName):
    # print(aboutName)
    url = "/aboutHome/"+aboutName
    # print(url)
    return render_template({url})

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        print("inpost")
        searchItem = request.form['item']
        filter1 = request.form['category-select']
        print("item: ", searchItem)
        print("filter: ", filter1)
        cursor.execute("SELECT * FROM Category")
        conn.commit()
        data = cursor.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0: 
            cursor.execute("SELECT * FROM Category")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug = True)