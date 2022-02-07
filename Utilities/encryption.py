from cryptography.fernet import Fernet

def generate_key():
    key  = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    if checkKeyExist():
        return (open("secret.key", "rb").read())
    else:
        return generate_key()

def checkKeyExist():
    try:
        if(open("secret.key", "rb").read()):
            return True
    except:
        return False

def encrypt(message):
    key = load_key()
    message = message.encode()
    f = Fernet(key)
    message = f.encrypt(message)
    return message

def decrypt(message):
    key = load_key()
    f = Fernet(key)
    message = f.decrypt(message)
    message = message.decode()
    return message