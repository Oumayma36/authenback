class LoginDTO:
    def __init__(self, data):
        if "firstName" in data and "firstName" in data:
            self.name = data.get('firstName') + " " + data.get('lastName')
            self.email = data.get('email')
            self.password = data.get('password')
            self.address = data.get('address')
            self.phone = data.get('phone')
            self.isVerified = data.get('isVerified', False)
            self.role = data.get('role', 'admin')
        else:
            self.name = data.get('name')
            self.email = data.get('email')
            self.password = data.get('password')
            self.address = data.get('address')
            self.phone = data.get('phone')
            self.isVerified = data.get('isVerified', False)
            self.role = data.get('role', 'admin')
        

    def get_signin_data(self):
        return {
            "email": self.email,
            "password": self.password
        }
    
    def get_signup_data(self):
        import uuid
        return {
            "_id": uuid.uuid4().hex,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "phone": self.phone,
            "isVerified": self.isVerified,
            "role": self.role
        }
    
    def get_session_data(self):
        import uuid
        return {
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "isVerified": self.isVerified,
            "role": self.role
        }
    
    @staticmethod
    def from_user(user):
        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "address": user.address,
            "phone": user.phone,
            "isVerified": user.isVerified,
            "role": user.role
        }
        return LoginDTO(data)