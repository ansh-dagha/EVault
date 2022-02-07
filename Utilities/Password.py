import random

Lalphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Ualphabets = 'abcdefghijklmnopqrstuvwxyz'
numerics = '0123456789'
specials = '!@#$%^&*'

minLen = 8
maxLen = 15
        
def generatePass():

    passLength = random.randint(minLen, maxLen)

    password = random.choice(Lalphabets) +\
                    random.choice(Ualphabets) +\
                    random.choice(numerics) +\
                    random.choice(specials)
    passLength -= 4

    #randomly select remaining characters
    for _ in range(passLength):
        character_set = random.choice([Lalphabets, Ualphabets, numerics, specials])
        password += random.choice(character_set)
    #shuffle string
    password = ''.join(random.sample(list(password), len(password)))
    return password

def isValid(p):

    if len(p)<8 or len(p)>15: 
        return False, "Invalid password length"

    fl=fu=fd=fs=False
    for c in p:
        if c.isdigit():
            fd=True
        elif c.islower():
            fl = True
        elif c.isupper():
            fu = True
        elif c in specials:
            fs = True
        else:
            return False, f"Invalid character '{c}'"

    if not fl:
        return False, 'Minimum 1 lowercase alphebet is required'
    if not fu:
        return False, 'Minimum 1 uppercase alphebet is required'
    if not fd:
        return False, 'Minimum 1 numeric digit is required'
    if not fs:
        return False, 'Minimum 1 special character is required'

    return fl and fu and fd and fs, None