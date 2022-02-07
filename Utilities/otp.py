import random

def generateOTP():
    characters = "0123456789"
    otp=''
    for _ in range(6):
        otp += random.choice(characters)
    return otp