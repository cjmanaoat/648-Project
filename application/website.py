import pathlib
import re
import subprocess
import sys

from PIL import Image
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
    limit = 3
    cursor.execute("SELECT list_title, suggest_price, image, list_id \
                FROM Trademart.Listing \
                WHERE approval_status=1\
                order by list_date desc \
                limit %s", limit)
    conn.commit()
    data = cursor.fetchall()
    for listing in data:
        blob2Img(listing)
    pathPrefix = "static/listing_images/"
    return render_template("index.html", data=data, pathPrefix=pathPrefix, limit=limit)

# main about page
@app.route("/aboutHome/")
def aboutHome():
    #print("in main home")
    return render_template("/aboutHome/aboutHome.html")

# class resource page
@app.route("/classResource/")
def classResource():
    #print("in main home")
    return render_template("/classResource.html")

# dashboard page
@app.route("/dashboard/")
def dashboard():
    #print("in main home")
    return render_template("/dashboard.html")

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
            cursor.execute("SELECT list_title, suggest_price, image, list_id\
                FROM Listing L\
                WHERE approval_status=1 \
                    AND L.list_title LIKE %s\
                    OR L.list_category LIKE %s\
                    OR L.list_desc LIKE %s", \
                    (("%" + searchItem + "%"), ("%" + searchItem + "%"), ("%" + searchItem + "%")))
        else:   #case where category is selected.
            if searchItem == "":        #empty search item but category selected
                cursor.execute("SELECT list_title, suggest_price, image, list_id\
                FROM Listing L\
                WHERE approval_status=1\
                    AND L.list_category=%s", \
                    (filterCategory))
             else:    #category and item selected
                cursor.execute("SELECT list_title, suggest_price, image, list_id\
                    FROM Listing L\
                    WHERE approval_status=1\
                        AND L.list_category=%s\
                        AND L.list_title LIKE %s\
                        OR L.list_desc LIKE %s", \
                        (filterCategory, ('%' + searchItem + '%'), ('%' + searchItem + '%')))
        conn.commit()
        data = cursor.fetchall()
        for listing in data:
            blob2Img(listing)
        if len(data) == 0: # no item provided. lists all items
            cursor.execute("SELECT list_title, suggest_price, image, list_id FROM Trademart.Listing WHERE approval_status=1")
            conn.commit()
            data = cursor.fetchall()
            for listing in data:
                blob2Img(listing)
         return render_template('search.html', data=data, searchItem=searchItem)
    return render_template('search.html') 
# home page
@app.route("/captchatest")
def captcha():
    return render_template("captchaTest.html")

# register
@app.route("/register")
def register():
    return render_template("register.html")

# sign in
@app.route("/signIn")
def signIn():
    return render_template("signIn.html")

# item page
@app.route("/itempage")
def itempage():
    return render_template("itempage.html")

# contact listing owner
@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        listingId = request.form['listingId']
        cursor.execute("SELECT list_id, list_desc, image, list_title, \
                condition, pref_location, suggest_price, offer_type \
                FROM Trademart.Listing \
                WHERE approval_status=1 \
                AND list_id=%s\
                order by list_date desc", listingId)
        conn.commit()
        data = cursor.fetchall()
        return render_template('contact.html', data=data)
    return render_template('contact.html')

@app.route("/createListing")
def createListing():
    return render_template("createListing.html")

@app.route("/listing", methods=["POST", "GET"])
def listing():
    if request.method == "POST":
        listingId = request.form['listingId']
        print(listingId)
        cursor.execute("SELECT list_title, suggest_price, image, list_id \
                FROM Trademart.Listing \
                WHERE approval_status=1\
                AND list_id=%s\
                order by list_date desc", listingId)
        conn.commit()
        data = cursor.fetchall()
        return render_template('listing.html', data=data)
    return render_template("listing.html")

def blob2Img(listing):
    fileName = str(listing[3]) + ".jpg"
    path = "/home/dasfiter/CSC648/application/static/listing_images/"+fileName
    #print(path)
    # size = sys.getsizeof(listing[11])
    # print(size)
    #print(listing[2])
    sizes = [(4, "quarter"), (2, "half")]
    if listing[2]:  #checks if pulled image from DB isn't empty
        test_path = pathlib.Path(path)
        if not test_path.exists():
        #print("exists")
            with open(path, "wb") as file:
                file.write(listing[2])
                file.close()
            for size, name in sizes:
                im = Image.open("/home/dasfiter/CSC648/application/static/listing_images/%s" % fileName)
                im.thumbnail((im.width//size, im.height//size))
                im.save("/home/dasfiter/CSC648/application/static/listing_images/thumbnail_%s_%s_size.jpg" % (fileName[:-4], name))
        

if __name__ == '__main__':
    app.run(debug = True)
