from flask import Flask, redirect, url_for, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

# sql config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'trademartadmin'
app.config['MYSQL_DATABASE_DB'] = 'Trademart'
app.config['MYSQL_DATABASE_HOST'] = 'trademart.c9x2rihy8ycd.us-west-1.rds.amazonaws.com'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
# end sql config

# home page
@app.route("/")
def home():
    return render_template("index.html")

# main about page
@app.route("/aboutHome/")
def aboutHome():
    #print("in main home")
    return render_template("/aboutHome/aboutHome.html")

# about page per member
@app.route("/aboutHome/<aboutName>")
def aboutPage(aboutName):
    #print("in separate about page")
    #print(aboutName)
    url = "aboutHome/"+aboutName
    # print(url)
    return render_template(url)

#search page
@app.route('/search', methods=['GET', 'POST'])
@app.route('/*/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        #print("in post")
        searchItem = request.form['item'].lower()
        filterCategory = request.form['category-select'].lower()
        print("item: ", searchItem)
        print("filter: ", filterCategory)
        if filterCategory=="all":   #case where only item provided, will search for item in any category
            cursor.execute("\
                SELECT list_title\
                FROM Listing L \
                WHERE L.list_title LIKE %s", \
                (searchItem))
        else:   #case where item and narrowed category is selected.
            cursor.execute("\
                SELECT list_title \
                FROM Listing L \
                WHERE L.list_category=%s \
                    AND L.list_title LIKE %s \
                    OR L.list_category LIKE %s", \
                    (filterCategory, searchItem, filterCategory))
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 0: # no item provided. lists all items
            cursor.execute("\
                SELECT list_title FROM Listing L")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')

# home page
@app.route("/captchatest")
def captcha():
    return render_template("captchaTest.html")


if __name__ == '__main__':
    app.run(debug = True)