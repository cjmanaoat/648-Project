from flask import Flask, redirect, url_for, render_template, request
from flaskext.mysql import MySQL
<<<<<<< HEAD
import sys

app = Flask(__name__)

<<<<<<< HEAD
=======
# sql config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'trademartadmin'
app.config['MYSQL_DATABASE_DB'] = 'Trademart'
app.config['MYSQL_DATABASE_HOST'] = 'trademart.c9x2rihy8ycd.us-west-1.rds.amazonaws.com'
>>>>>>> 7e3875210a4bfcfbc9a752f88568b0acf71c97c4

=======

app = Flask(__name__)

>>>>>>> 55be20a9250692053c1de82f8301288ec25aef25
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
<<<<<<< HEAD
# end sql config

<<<<<<< HEAD

=======
# home page
>>>>>>> 7e3875210a4bfcfbc9a752f88568b0acf71c97c4
@app.route("/")
def home():
    cursor.execute("SELECT list_title, suggest_price, image, list_id \
                FROM Trademart.Listing \
                WHERE approval_status=1\
                order by list_date desc \
                limit 3")
    conn.commit()
    data = cursor.fetchall()
    for listing in data:
        blob2Img(listing)
    pathPrefix = "static/listing_images/"
    return render_template("index.html", data=data, pathPrefix=pathPrefix)

# main about page
=======


@app.route("/")
def home():
    return render_template("index.html")

>>>>>>> 55be20a9250692053c1de82f8301288ec25aef25
@app.route("/aboutHome/")
def aboutHome():
    #print("in main home")
    return render_template("/aboutHome/aboutHome.html")

<<<<<<< HEAD
# about page per member
=======
>>>>>>> 55be20a9250692053c1de82f8301288ec25aef25
@app.route("/aboutHome/<aboutName>")
def aboutPage(aboutName):
    #print("in separate about page")
    #print(aboutName)
    url = "aboutHome/"+aboutName
    # print(url)
    return render_template(url)

<<<<<<< HEAD
#search page
=======
>>>>>>> 55be20a9250692053c1de82f8301288ec25aef25
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 55be20a9250692053c1de82f8301288ec25aef25
            cursor.execute("\
                SELECT list_title,image, list_id, suggest_price\
                FROM Trademart.Listing \
                WHERE list_title LIKE %s", \
                (searchItem))
        else:   #case where item and narrowed category is selected.
            cursor.execute("\
                SELECT list_title,image, list_id, suggest_price\
                FROM Trademart.Listing \
                WHERE list_category=%s \
                    AND list_title LIKE %s \
                    OR list_category LIKE %s", \
                    (filterCategory, searchItem, filterCategory))
        conn.commit()
        data = cursor.fetchall()
        for listing in data:
            fileName = str(listing[2]) + ".jpg"
            path = "static/listing_images"+fileName
            print(path)
            with open(path, "wb") as file:
                file.write(listing[1])
        if len(data) == 0: # no item provided. lists all items
            cursor.execute("\
                SELECT list_title,image, list_id, suggest_price FROM Trademart.Listing")
<<<<<<< HEAD
=======
            cursor.execute("SELECT *\
                FROM Listing L \
                WHERE L.list_title LIKE %s\
                OR L.list_category LIKE %s\
                OR L.list_desc LIKE %s", \
                (("%" + searchItem + "%"), ("%" + searchItem + "%"), ("%" + searchItem + "%")))
        else:   #case where item and narrowed category is selected.
            cursor.execute("SELECT * \
                FROM Listing L \
                WHERE L.list_category=%s \
                    AND L.list_title LIKE %s \
                    OR L.list_category LIKE %s", \
                    (filterCategory, ('%' + searchItem + '%'), filterCategory))
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 0: # no item provided. lists all items
            cursor.execute("SELECT * \
                FROM Listing L")
>>>>>>> 7e3875210a4bfcfbc9a752f88568b0acf71c97c4
=======
>>>>>>> 55be20a9250692053c1de82f8301288ec25aef25
            conn.commit()
            data = cursor.fetchall()
            for listing in data:
                fileName = str(listing[2]) + ".jpg"
                path = "static/listing_images"+fileName
                print(path)
                with open(path, "wb") as file:
                    file.write(listing[1])
        return render_template('search.html', data=data)
    return render_template('search.html')

<<<<<<< HEAD
# home page
@app.route("/captchatest")
def captcha():
    return render_template("captchaTest.html")


def blob2Img(listing):
    fileName = str(listing[3]) + ".jpg"
    path = "static/listing_images/"+fileName
    # print(path)
    # size = sys.getsizeof(listing[11])
    # print(size)
    with open(path, "wb") as file:
        file.write(listing[2])

=======
>>>>>>> 55be20a9250692053c1de82f8301288ec25aef25

if __name__ == '__main__':
    app.run(debug = True)
