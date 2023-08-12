from daos import db
from dto.login_dto import LoginDTO
from models.user import User

class LoginDAO:
    def __init__(self):
        self.users = db['users']

    def find_by_email(self, email):
        user_doc = self.users.find_one({'email': email})
        if user_doc is None:
            return None
        user_id = str(user_doc['_id'])
        return User( user_doc['name'], user_doc['email'], \
                     user_doc['password'], user_doc['address'],user_doc["address"], \
                     user_id ,user_doc['isVerified'], user_doc['role'])

    def save(self, signup_data):
        self.users.insert_one(signup_data)
        return User(signup_data["name"], signup_data["email"], \
                    signup_data["password"], signup_data["address"],signup_data["phone"], signup_data["_id"])
    
    def find_session_by_email(self, email):
        user_doc = self.find_by_email(email)
        if user_doc is None:
            return None
        user_data = LoginDTO.from_user(user_doc)
        session_data = user_data.get_session_data()
        return session_data
    
    def update(self, email, update_data):
        user_doc = self.users.find_one({'email': email})
        if user_doc is None:
            return None
        self.users.update_one({'email': email}, {'$set': update_data})
        updated_user_doc = self.users.find_one({'email': email})
        user_id = str(updated_user_doc['_id'])
        return User(updated_user_doc['name'], updated_user_doc['email'], \
                    updated_user_doc['password'], updated_user_doc['address'],updated_user_doc["phone"], \
                    user_id, updated_user_doc['isVerified'], updated_user_doc['role'])