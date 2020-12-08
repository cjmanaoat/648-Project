from cryptography.fernet import Fernet

# writes a key to a file called key.key, call once in entire code to generate
def write_key():
    key = Fernet.generate_key() * 675
    print(key)
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# call everytime you need to get the key
def load_key():
    return open("/home/dasfiter/CSC648/credentials/key.key", "rb").read
    # return open("../credentials/key.key", "rb").read()
