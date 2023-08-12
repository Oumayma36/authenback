import bcrypt

class PasswordHasher:
    def __init__(self):
        self.salt = bcrypt.gensalt()

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        return hashed_password.decode('utf-8')

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))