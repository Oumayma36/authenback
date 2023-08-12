from flask import request, jsonify
from services.login_service import LoginService
from dto.login_dto import LoginDTO

class LoginController:
    def __init__(self,app):
        self.login_service = LoginService(app)

    
    def decorated_function(self, f):
        def decorated_function(*args, **kwargs):
            if not self.login_service.is_logged_in():
                return jsonify(msg="You must be logged in to perform this action"), 401
            return f(*args, **kwargs)
        return decorated_function
    
    def decorated_function_signout(self, f):
        def decorated_function_signout(*args, **kwargs):
            if self.login_service.is_logged_in():
                return jsonify(msg="You must be logged out to perform this action"), 401
            return f(*args, **kwargs)
        return decorated_function_signout


    def login(self):
        login_data = LoginDTO(request.json).get_signin_data()
        response = self.login_service.authenticate(login_data)
        return jsonify(response)
    

    def signout(self):
        session_cookie = request.cookies.get('session')
        response = self.login_service.signout(session_cookie)
        return jsonify(response)
    

    def signup(self):
        signup_data = LoginDTO(request.json).get_signup_data()
        session_data = LoginDTO(request.json).get_session_data()
        response = self.login_service.signup_user(signup_data,session_data)
        return jsonify(response)
    

    def sendConfirmationCode(self):
        email = request.json.get('email')
        response = self.login_service.send_confirmation_code(email)
        return jsonify(response)
    

    def verifyEmail(self):
        requestCode = int(request.json.get('verificationCode'))
        response = self.login_service.verify_email(requestCode)
        return jsonify(response)
    
    
    def getSessionInfo(self):
        response = self.login_service.get_session_info()
        return jsonify(response)
    

    def resetPasswordStep1(self):
        email = request.json.get("email")
        response = self.login_service.reset_password_step1(email)
        return jsonify(response)
    
    def resetPasswordStep2(self):
        requestCode = int(request.json.get('verificationCode'))
        response = self.login_service.reset_password_step2(requestCode)
        return jsonify(response)
    
    def resetPasswordStep3(self):
        password = request.json.get("password")
        session_cookie = request.cookies.get('session')
        response = self.login_service.reset_password_step3(password, session_cookie)
        return jsonify(response)