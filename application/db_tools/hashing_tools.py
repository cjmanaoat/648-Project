from passlib.hash import sha256_crypt


##### HASHES USER'S EMAIL AND STORES HASHED VERSION IN DB #####
def hash_email(user_id, email):
    hashed_email = sha256_crypt.hash(email) # one-way hash

    return hashed_email                     # returns hashed version of the email

##### HASHES USER'S ADDRESS AND STORES HASHED VERSION IN DB #####
def hash_addr(user_id, addr):
    hashed_addr = sha256_crypt.hash(addr)   # one-way hash

    return hashed_addr                      # returns hashed version of the address

##### HASHES USER'S PASSWORD AND STORES HASHED VERSION IN DB #####
def hash_password(user_id, password):
    hashed_password = sha256_crypt.hash(password)   # one-way hash

    return hashed_password                          # returns hashed version of the password

##### compare plain text to hashed info in database #####
def verify_hashed_info(entered_info, hashed_info):
    return sha256_crypt.verify(entered_info, hashed_info) # returns true if plaint text = hashed version in db
