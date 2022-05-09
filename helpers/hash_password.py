import bcrypt


def generateHash(password):
    hashed = bcrypt.hashpw(password.encode('ASCII'), bcrypt.gensalt())
    return hashed


def validateHash(password, hashPassword):
    b_password = password.encode('ASCII')
    if bcrypt.checkpw(b_password, hashPassword.encode('ASCII')):
        return True

    return False


# res = generateHash('helloworld')
# s_res = res.decode('ASCII')
# print(validateHash('helloworlds', s_res))

# password -> hash algo -> new hashed password
# one way
# hashpw -
# gensalt - generates a random string to make password hard to hack
