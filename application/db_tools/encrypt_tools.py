import argparse
import mysql.connector
from mysql.connector import Error

from cryptography.fernet import Fernet

# generate key
key = Fernet.generate_key() * 675

# assign to var
cipher_suite = Fernet(key)

##### ENCRPYT PASSWORD #####

# takes in a plain text password and converts it to ciphered text
# this will be stored in the database
def encrypt_password(user_id, password):
    ciphered_password = cipher_suite.encrypt(bytes(password, encoding = "ascii"))

    query = "UPDATE User " \
            "SET user_pass = %s " \
            "WHERE user_id  = %s"

    args = (ciphered_password, user_id)

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


    return ciphered_password

##### DECRPYT AND DECODE CIPHERED PASSWORD #####

# takes an encrypted password and converts it into a byte literal, then
# decodes it into plain text
def get_plain_password(ciphered_password):
    decrypted_password = cipher_suite.decrypt(ciphered_password)
    return decrypted_password.decode()

def main():
    e = encrypt_password(224602238, "password")
    p = get_plain_password(e)
    print(e)
    print(p)

if __name__ == '__main__':
    main()
