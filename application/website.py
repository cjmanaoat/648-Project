from flask import Flask, redirect, url_for, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)


mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutHome/")
def aboutHome():
    #print("in main home")
    return render_template("/aboutHome/aboutHome.html")

@app.route("/aboutHome/<aboutName>")
def aboutPage(aboutName):
    #print("in separate about page")
    #print(aboutName)
    url = "aboutHome/"+aboutName
    # print(url)
    return render_template(url)

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


if __name__ == '__main__':
    app.run(debug = True)
