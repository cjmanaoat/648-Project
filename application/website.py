# 
# website.py
# Description:
# This file handles the routing of each page endpoint and takes care of the queries
# 
# Contents:
# -endpoints
# -function to convert blobs to images
# 

# imports
import pathlib
import re
import subprocess
import sys

from PIL import Image
from flask import Flask, redirect, url_for, render_template, request
from flaskext.mysql import MySQL
# end imports

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

# route for favicon
@app.route('/favicon/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

# home page
@app.route("/")
def home():
    limit = 3   # you can specify how many listings will be shown with this variable
    cursor.execute("SELECT list_title, suggest_price, image, list_id \
                FROM Trademart.Listing \
                WHERE approval_status=1\
                order by list_date desc \
                limit %s", limit)   #The query to be run to grab the appropriate info
    conn.commit()
    data = cursor.fetchall() # gets all the query contents
    # goes through each listing to create an image
    for listing in data:
        blob2Img(listing)
    pathPrefix = "static/listing_images/" # path provided
    return render_template("index.html", data=data, pathPrefix=pathPrefix, limit=limit) #loads the home page

# main about page
@app.route("/aboutHome/")
def aboutHome():
    #print("in main home")
    return render_template("/aboutHome/aboutHome.html") # loads about page

# class resource page
@app.route("/classResource/")
def classResource():
    #print("in main home")
    return render_template("/classResource.html") #loads class resource page

# dashboard page
@app.route("/dashboard/")
def dashboard():
    #print("in main home")
    return render_template("/dashboard.html") #loads dashboard page

# about page per member
@app.route("/aboutHome/<aboutName>")
def aboutPage(aboutName):
    #print("in separate about page")
    #print(aboutName)
    url = "aboutHome/"+aboutName #creates the appropriate url for each member
    # print(url)
    return render_template(url) #loads the member's page

#search page
@app.route('/search', methods=['GET', 'POST'])
@app.route('/*/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST": #for getting info sent
        #print("in post")
        searchItem = request.form['item'].lower() #converts search item to lower
        filterCategory = request.form['category-select'].lower() #converts category to lower
        print("item: ", searchItem)
        print("filter: ", filterCategory)
        if filterCategory=="all":   #case where only item provided, will search for item in any category
            cursor.execute("SELECT list_title, suggest_price, image, list_id\
                FROM Listing L\
                WHERE approval_status=1 \
                    AND L.list_title LIKE %s\
                    OR L.list_category LIKE %s\
                    OR L.list_desc LIKE %s", \
                    (("%" + searchItem + "%"), ("%" + searchItem + "%"), ("%" + searchItem + "%"))) # query to grab data
        else:   #case where category is selected.
            if searchItem == "":        #empty search item but category selected
                cursor.execute("SELECT list_title, suggest_price, image, list_id\
                FROM Listing L\
                WHERE approval_status=1\
                    AND L.list_category=%s", \
                    (filterCategory)) # query to grab data
            else:    #category and item selected
                cursor.execute("SELECT list_title, suggest_price, image, list_id\
                    FROM Listing L\
                    WHERE approval_status=1\
                        AND L.list_category=%s\
                        AND L.list_title LIKE %s\
                        OR L.list_desc LIKE %s", \
                        (filterCategory, ('%' + searchItem + '%'), ('%' + searchItem + '%'))) # query to grab data
        conn.commit()
        data = cursor.fetchall() # gets all data from query
        # creates images for each listing
        for listing in data:
            blob2Img(listing)
        if len(data) == 0: # no item provided. lists all items
            cursor.execute("SELECT list_title, suggest_price, image, list_id FROM Trademart.Listing WHERE approval_status=1") #query to grab data
            conn.commit()
            data = cursor.fetchall() # gets all data from query
            # creates image for each listing
            for listing in data:
                blob2Img(listing)
        return render_template('search.html', data=data, searchItem=request.form['item']) # loads search result page
    return render_template('search.html')

# register
@app.route("/register")
def register():
    return render_template("register.html") # loads register page

# sign in
@app.route("/signIn")
def signIn():
    return render_template("signIn.html") # loads sign in page

# item page
@app.route("/itempage")
def itempage():
    return render_template("itempage.html") # loads item page

# contact listing owner
@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        listingId = request.form['listingId'] # gets listing id provided
        cursor.execute("SELECT list_id, list_desc, image, list_title, \
                condition, pref_location, suggest_price, offer_type \
                FROM Trademart.Listing \
                WHERE approval_status=1 \
                AND list_id=%s\
                order by list_date desc", listingId) # query to get data
        conn.commit()
        data = cursor.fetchall() # gets all data from query
        return render_template('contact.html', data=data) # loads contact owner page
    return render_template('contact.html') # laods contact owner page

# create a listing
@app.route("/createListing")
def createListing():
    return render_template("createListing.html") # loads creating a listing page

# listing
@app.route("/listing", methods=["POST", "GET"])
def listing():
    if request.method == "POST":
        listingId = request.form['listingId'] # gets listing id
        print(listingId)
        cursor.execute("SELECT list_title, suggest_price, image, list_id \
                FROM Trademart.Listing \
                WHERE approval_status=1\
                AND list_id=%s\
                order by list_date desc", listingId) #query to get data
        conn.commit()
        data = cursor.fetchall() # gets data from query
        return render_template('listing.html', data=data) # load listing page
    return render_template("listing.html") # load listing page

# this function converts a blob to an image of type jpg
def blob2Img(listing):
    fileName = str(listing[3]) + ".jpg" # the file name using listing id
    path = "/home/dasfiter/CSC648/application/static/listing_images/"+fileName # path to image
    # path = "static/listing_images/"+fileName # path to image
    #print(path)
    # size = sys.getsizeof(listing[11])
    # print(size)
    #print(listing[2])
    sizes = [(4, "quarter"), (2, "half")] # resize values
    if listing[2]:  #checks if pulled image from DB isn't empty
        test_path = pathlib.Path(path) # gets path
        if not test_path.exists(): # if path doesnt exist
        #print("exists")
            with open(path, "wb") as file: # open the file
                file.write(listing[2]) # convert blob to image
                file.close()
            # loop to create thumbnails
            for size, name in sizes:
                im = Image.open("/home/dasfiter/CSC648/application/static/listing_images/%s" % fileName) # opens image
                # im = Image.open("static/listing_images/%s" % fileName) # opens image
                im.thumbnail((im.width//size, im.height//size)) # creates thumbnail
                im.save("/home/dasfiter/CSC648/application/static/listing_images/thumbnail_%s_%s_size.jpg" % (fileName[:-4], name)) #saves image
                # im.save("static/listing_images/thumbnail_%s_%s_size.jpg" % (fileName[:-4], name)) #saves image
        

if __name__ == '__main__':
    app.run(debug = True)
