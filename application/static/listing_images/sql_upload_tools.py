
def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo

import mysql.connector
from mysql.connector import Error

def update_blob(list_id, filename):
    # read file
    data = read_file(filename)

    # prepare update query and data
    query = "UPDATE Listing " \
            "SET image = %s " \
            "WHERE list_id  = %s"

    args = (data, list_id)


    try:
        conn =  mysql.connector.connect(host='trademart.c9x2rihy8ycd.us-west-1.rds.amazonaws.com',
                database='Trademart',
                user='root',
                password='trademartadmin')
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def main():
    update_blob(19273, "/home/ubuntu/dbtest/images/textbook3.jpg")

if __name__ == '__main__':
    main()
