import argparse
import os
import mysql.connector
from mysql.connector import Error

# parser = argparse.ArgumentParser(description="Parser for updating blob images")
# parser.add_argument("user", help="Username for logging into the DB", type=str)
# parser.add_argument("password", help="DB Password", type=str)
# parser.add_argument("list_id", help="Listing ID that needs picture", type=int)
# parser.add_argument("path", help='Path to image', type=str)
# p_args = parser.parse_args()

def read_file(filename):
    with open(filename, 'rb') as file:
        image = file.read()
    return image

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def update_blob(list_id, filename):
    # read file
    data = read_file(filename)

    # prepare update query and data
    query = "UPDATE Listing " \
            "SET image = %s " \
            "WHERE list_id  = %s"

    args = (data, list_id)


    try:
        conn =  mysql.connector.connect(host=os.getenv("MYSQL_DATABASE_HOST"),
                database=os.getenv("MYSQL_DATABASE_DB"),
                user=os.getenv("MYSQL_DATABASE_USER"),
                password=os.getenv("MYSQL_DATABASE_PASSWORD"))
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)

# read blob data to a file so we can actually use the image
def read_blob(list_id, path):
    query = "SELECT image FROM Listing WHERE id = %s"

    db_config = read_db_config()

    try:
        # get blob data from listing
        conn =  mysql.connector.connect(host='trademart.c9x2rihy8ycd.us-west-1.rds.amazonaws.com',
                database='Trademart',
                user='root',
                password='trademartadmin')
        cursor = conn.cursor()
        cursor.execute(query, (list_id))
        image = cursor.fetchone()[0]

        #write blob data into a file
        write_file(image, filename)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def main():
    # update_blob(p_args.list_id, p_args.path)

   #read_blob(19273, "converted_images\imagename.jpg")

    if __name__ == '__main__':
        main()
