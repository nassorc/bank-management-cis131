import bcrypt


def generateHash(password):
    hashed = bcrypt.hashpw(password.encode('ASCII'), bcrypt.gensalt())
    return hashed


def validateHash(password, hashPassword):
    b_password = password.encode('ASCII')
    if bcrypt.checkpw(b_password, hashPassword):
        print('correct')
    else:
        print('wrong')


def test():
    print('working')


# res = generateHash('helloworld')
# print(validateHash('helloworld', res))

# password -> hash algo -> new hashed password
# one way
# hashpw -
# gensalt - generates a random string to make password hard to hack
