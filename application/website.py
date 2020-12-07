# 
# website.py
# Description:
# This file handles the routing of each page endpoint and takes care of the queries
# 
# Contents:
# -endpoints
# -function to convert blobs to images
# 

# TODO implement rest of the endpoints with sessions

# imports
import pathlib
import re
import subprocess
import sys
import random

from PIL import Image
from flask import Flask, redirect, url_for, render_template, request, session
from flaskext.mysql import MySQL
from db_tools.hashing_test import hash_password, verify_password
# end imports

app = Flask(__name__)
app.secret_key = 'csc648sfsutrademart' # key for session purposes

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
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    popUp = ''
    message = ''
    if 'loggedIn' in session: # checks if user is logged in
        # print('logged in')
        username = session['username'] # sets appropriate login name
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    # print('request')
    # print(request.args)
    if request.args: #checks if arguments were provided (account creation success)
        if request.args['message']:
            message = request.args['message']
        if request.args['popUp']:
            popUp = request.args['popUp']

    limit = 3   # you can specify how many listings will be shown with this variable
    cursor.execute('SELECT list_title, suggest_price, image, list_id \
                FROM Trademart.Listing \
                WHERE approval_status=1\
                order by list_date desc \
                limit %s', limit)   #The query to be run to grab the appropriate info
    conn.commit()
    data = cursor.fetchall() # gets all the query contents
    # goes through each listing to create an image
    for listing in data:
        blob2Img(listing)
    pathPrefix = 'static/listing_images/'  # path provided
    return render_template('index.html', data=data, pathPrefix=pathPrefix, limit=limit, username=username, popUp=popUp, message=message) #loads the home page

# main about page
@app.route('/aboutHome/')
def aboutHome():
    if 'loggedIn' in session: # checks if user is logged in
        # print('logged in')
        username = session['username'] # sets appropriate login name
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    #print('in main home')
    return render_template('/aboutHome/aboutHome.html', username=username) # loads about page

# class resource page
@app.route('/classResource/')
def classResource():
    #print('in main home')
    return render_template('/classResource.html') #loads class resource page

# dashboard page
@app.route('/dashboard/')
def dashboard():
    if 'loggedIn' in session: # checks if user is logged in
        # print('logged in')
        username = session['username'] # sets appropriate login name
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    #print('in main home')
    return render_template('/dashboard.html', username=username) #loads dashboard page

# about page per member
@app.route('/aboutHome/<aboutName>')
def aboutPage(aboutName):
    if 'loggedIn' in session: # checks if user is logged in
        # print('logged in')
        username = session['username'] # sets appropriate login name
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    #print('in separate about page')
    #print(aboutName)
    url = 'aboutHome/'+aboutName #creates the appropriate url for each member
    # print(url)
    return render_template(url, username=username) #loads the member's page

# TODO make sure to refine search for no results
#search page
@app.route('/search', methods=['GET', 'POST'])
@app.route('/*/search', methods=['GET', 'POST'])
def search():
    if 'loggedIn' in session: # checks if user is logged in
        # print('logged in')
        username = session['username'] # sets appropriate login name
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    if request.method == 'POST': #for getting info sent
        #print('in post')
        searchItem = request.form['item'].lower() #converts search item to lower
        filterCategory = request.form['category-select'].lower()  #converts category to lower
        # print('item: ', searchItem)
        # print('filter: ', filterCategory)
        if filterCategory == 'all':  #case where only item provided, will search for item in any category
            # print('only item')
            cursor.execute('SELECT list_title, suggest_price, image, list_id\
                FROM Listing L\
                WHERE approval_status=1 \
                    AND L.list_title LIKE %s\
                    OR L.list_category LIKE %s\
                    OR L.list_desc LIKE %s', \
                    (('%' + searchItem + '%'), ('%' + searchItem + '%'), ('%' + searchItem + '%')))  # query to grab data
            # print('query done item only')
        elif searchItem == '' or not searchItem:        #empty search item but category selected
            # print('category only')
            cursor.execute('SELECT list_title, suggest_price, image, list_id\
                        FROM Listing L\
                        WHERE approval_status=1\
                        AND L.list_category LIKE %s\
                        OR L.list_title LIKE %s\
                        OR L.list_desc LIKE %s', \
                        ((filterCategory, filterCategory, filterCategory)))  # query to grab data
            # print('query done category only')
        else:  #category and item selected
            # print('category and item')
            cursor.execute('SELECT list_title, suggest_price, image, list_id\
                            FROM Listing L\
                            WHERE approval_status=1\
                            AND L.list_category=%s\
                            AND L.list_title LIKE %s\
                            OR L.list_desc LIKE %s', \
                            (filterCategory, ('%' + searchItem + '%'), ('%' + searchItem + '%')))  # query to grab data
            # print('query done category and item')
        conn.commit()
        data = cursor.fetchall() # gets all data from query
        # creates images for each listing
        for listing in data:
            blob2Img(listing)
        if len(data) == 0:  # no results from query. lists all items
            #print('no results')
            cursor.execute('SELECT list_title, suggest_price, image, list_id FROM Trademart.Listing WHERE approval_status=1') #query to grab data
            conn.commit()
            data = cursor.fetchall() # gets all data from query
            # creates image for each listing
            for listing in data:
                blob2Img(listing)
        # for item in data:
        #     print(item[0])
        return render_template('search.html', data=data, searchItem=request.form['item'], filter=request.form['category-select'], username=username) # loads search result page
    return render_template('search.html')

# register
@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'loggedIn' in session:  # checks if user is logged in
        username = session['username']  # sets appropriate login name
        return redirect(url_for('home'))
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    message = '' # message to print
    if (request.method == 'POST'):
        # gets user data to input into database from provided fields
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        username = request.form['userName']
        email = request.form['emailAddress']
        passwordInit = request.form['passInit']
        passwordConfirm = request.form['passConfirm']

        if (not firstname
            or not lastname
            or not username
            or not email
            or not passwordInit
            or not passwordConfirm): # server checks if all fields were submitted
                message = 'Please fill out all required fields'
                return render_template('register.html', popUp='True', message=message)
        
        # print('firstname: ' + firstname
        #     + ' lastname: ' + lastname
        #     + ' username: ' + username
        #     + ' email: ' + email
        #     + ' pass: ' + passwordConfirm)

        # username verification
        cursor.execute('SELECT user_name\
            FROM Trademart.User\
            WHERE user_name= % s ', username)
        conn.commit()
        userCheck=cursor.fetchone()
        if userCheck:
            # print('username exists')
            message = 'Username already exists.'
            return render_template('register.html', message=message, popUp='True')

        # email check
        if (email.endswith('@sfsu.edu')
            or email.endswith('@mail.sfsu.edu')): # Checks that the correct sfsu suffix is there
                cursor.execute('SELECT user_email\
                    FROM Trademart.User\
                    WHERE user_email= % s ', email)
                conn.commit()
                emailCheck=cursor.fetchone()
                if emailCheck:
                    # print('email exists')
                    message = 'Email aready has an account.'
                    return render_template('register.html', message=message, popUp='True')
        else:
            # print('not sfsu')
            message = 'Please input a SFSU email'
            return render_template('register.html', message=message, popUp='True')
        
        #password check
        if passwordInit != passwordConfirm:
            message = 'Passwords do not match'
            return render_template('register.html', message=message, popUp='True')

        #TODO: make sure to default rest of the acc info(if needed)
        idExists = True  # check if user id exists
        userId = random.randint(100000000, 999999998) # generate id
        while idExists: # loop for id generation will quit if id does not exist
            returnId = cursor.execute('SELECT user_id\
                                        FROM Trademart.User\
                                        WHERE user_id= % s ', userId)
            conn.commit()
            # print(returnId)
            if returnId: # id exists so randomize another
                userId = random.randint(100000000, 999999998)
                # print(userId)
            else: # id doesn't exist so it will quit loop with appropriate id
                idExists = False
                # print('id can be created')
        # print(userId)

        # at this point all user data is verified (no repeating username or email address)
        hashedPass = hash_password(userId, passwordConfirm)
        #print(hashedPass)
        accCreated = cursor.execute('INSERT INTO Trademart.User\
            (user_id, user_email, fname, lname, user_name, user_pass, reg_status)\
            VALUES(%s, %s, %s, %s, %s, %s, %s) ', (userId, email, firstname, lastname, username, hashedPass, '0'))
        conn.commit()
        if accCreated:
            message = 'Account successfully created!'
            return redirect(url_for('home', message=message, popUp='True', username=username))
    return render_template('register.html') # loads register page

# sign in
@app.route('/signIn', methods=['POST', 'GET'])
def signIn():
    if 'loggedIn' in session: # checks if user is logged in
        return redirect(url_for('home'))

    message = '' # message for popup
    if (request.method == 'POST'
    and 'loginEmail' in request.form
    and 'password' in request.form): # checks if there is an email abd password provided 
        loginEmail = request.form['loginEmail'] # gets email
        password = request.form['password'] # gets password
        print('email: ' + loginEmail + ' password: ' + password)
        
        cursor.execute('SELECT user_pass\
                        FROM Trademart.User\
                        WHERE user_email= % s\
                            AND reg_status=1 ', loginEmail) # query to get account info
        conn.commit() # commits query
        hashPassResult=cursor.fetchone()  # grabs query result
        # print(hashPassResult)
        if hashPassResult: # ensures data was returned from db
            hashedPass = hashPassResult[0] # gets pass from db query value
            # print(hashedPass)
            passVerify = verify_password(password, hashedPass) # verifies password
            if passVerify: # if the password is correct
                cursor.execute('SELECT *\
                            FROM Trademart.User\
                            WHERE user_email= % s\
                                AND reg_status= 1', loginEmail) # query to get account info
                conn.commit() # commits query
                account=cursor.fetchone()  # grabs query result
                # print(account)
            
                if account: # if the account exists
                    # print('account found')
                    session['loggedIn'] = True # variable for user logged in
                    session['id'] = account[0] # user id linked to session
                    session['username'] = account[5]  # username for session
                    return redirect(url_for('home'))  # redirects home
            else: # passwords dont match
                message = 'Incorrect email/password!'
                return render_template('signIn.html', message=message, popUp='True') # loads sign in page with error
        else: # one field empty or incorrect email and/or password
            message = 'Incorrect email/password!'
            return render_template('signIn.html', message=message, popUp='True') # loads sign in page with error
    return render_template('signIn.html') # loads sign in page

# log out route
@app.route('/logOut')
def logOut():
    session.pop('loggedIn', None) # lets server know current client is logging out
    session.pop('id', None) # removes signed in user from list
    session.pop('username', None) # removes username from list
    return redirect(url_for('home')) # redirect home

# item page
@app.route('/itempage')
def itempage():
    return render_template('itempage.html') # loads item page

# contact listing owner
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        listingId = request.form['listingId'] # gets listing id provided
        cursor.execute('SELECT list_id, list_desc, image, list_title, \
                condition, pref_location, suggest_price, offer_type \
                FROM Trademart.Listing \
                WHERE approval_status=1 \
                AND list_id=%s\
                order by list_date desc', listingId) # query to get data
        conn.commit()
        data = cursor.fetchall() # gets all data from query
        return render_template('contact.html', data=data) # loads contact owner page
    return render_template('contact.html') # laods contact owner page

# create a listing
@app.route('/createListing')
def createListing():
    if 'loggedIn' in session: # checks if user is logged in
        # print('logged in')
        username = session['username'] # sets appropriate login name
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    return render_template('createListing.html', username=username) # loads creating a listing page

# listing
@app.route('/listing', methods=['POST', 'GET'])
def listing():
    if 'loggedIn' in session: # checks if user is logged in
        # print('logged in')
        username = session['username'] # sets appropriate login name
    else: # user isnt logged in
        # print('not logged in')
        username = ''

    if request.method == 'POST':
        listingId = request.form['listingId'] # gets listing id
        # print(listingId)
        cursor.execute('SELECT list_title, suggest_price, image, list_id \
                FROM Trademart.Listing \
                WHERE approval_status=1\
                AND list_id=%s\
                order by list_date desc', listingId) #query to get data
        conn.commit()
        data = cursor.fetchall() # gets data from query
        return render_template('itempage.html', data=data, username=username) # load listing page
    return render_template('itempage.html') # load listing page

# this function converts a blob to an image of type jpg
def blob2Img(listing):
    fileName = str(listing[3]) + '.jpg' # the file name using listing id
    path = '/home/dasfiter/CSC648/application/static/listing_images/'+fileName # path to image
    # path = 'static/listing_images/'+fileName # path to image
    #print(path)
    # size = sys.getsizeof(listing[11])
    # print(size)
    #print(listing[2])
    sizes = [(4, 'quarter'), (2, 'half')] # resize values
    if listing[2]:  #checks if pulled image from DB isn't empty
        test_path = pathlib.Path(path) # gets path
        if not test_path.exists(): # if path doesnt exist
        #print('exists')
            with open(path, 'wb') as file: # open the file
                file.write(listing[2]) # convert blob to image
                file.close()
            # loop to create thumbnails
            for size, name in sizes:
                im = Image.open('/home/dasfiter/CSC648/application/static/listing_images/%s' % fileName) # opens image
                # im = Image.open('static/listing_images/%s' % fileName) # opens image
                im.thumbnail((im.width//size, im.height//size)) # creates thumbnail
                im.save('/home/dasfiter/CSC648/application/static/listing_images/thumbnail_%s_%s_size.jpg' % (fileName[:-4], name)) #saves image
                # im.save('static/listing_images/thumbnail_%s_%s_size.jpg' % (fileName[:-4], name)) #saves image
        

if __name__ == '__main__':
    app.run(debug = True)
