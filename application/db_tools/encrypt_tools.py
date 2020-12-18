import argparse
import mysql.connector
import os
from mysql.connector import Error

from cryptography.fernet import Fernet
from .key import *

##### ENCRPYT PASSWORD #####

# takes in a plain text password and converts it to ciphered text
# this will be stored in the database
def encrypt_email(user_id, email, f):
    emailBytes = bytes(email, 'utf-8') # convert email to bytes first
    ciphered_email = f.encrypt(emailBytes) # encrypt email

    query = "UPDATE User " \
            "SET user_email = %s " \
            "WHERE user_id  = %s"

    args = (ciphered_email, user_id)

    try:
        conn =  mysql.connector.connect(host=os.getenv("MYSQL_DATABASE_HOST"),
                database=os.getenv("MYSQL_DATABASE_DB"),
                user=os.getenv("MYSQL_DATABASE_USER"),
                password=os.getenv("MYSQL_DATABASE_PASSWORD"))
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as e:
        print(e)


    return ciphered_email

##### DECRPYT AND DECODE CIPHERED PASSWORD #####

# takes an encrypted password and converts it into a byte literal, then
# decodes it into plain text
def get_plain_email(ciphered_email, f):
    decipher = f.decrypt(ciphered_email) # decipher email
    plain_text = bytes(decipher).decode('utf-8') # turn email back to readable string
    return plain_text

def main():
    # CHANGE: call load_key() to get the key instead of generating a new one
    key = load_key()
    print(key)
    f = Fernet(key) # use to encrypt and decrypt
    # CHANGE: pass in f (previously ciphered_suite for these functions)
    e = encrypt_email(194724822, "kahleed@mail.sfsu.edu", f)
    # p = get_plain_email(e, f)
    #print(e)
    print(p)

if __name__ == '__main__':
    main()
