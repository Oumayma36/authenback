from daos.login_dao import LoginDAO
from utils.password_hasher import PasswordHasher
from utils.session_manager import SessionManager

class LoginService:
    def __init__(self, app):
        self.login_dao = LoginDAO()
        self.password_hasher = PasswordHasher()
        self.session_manager = SessionManager(app)

    def is_logged_in(self):
        return self.session_manager.is_logged_in()

    def authenticate(self, login_data):
        try:
            email = login_data["email"]
            password = login_data["password"]
            user = self.login_dao.find_by_email(email)

            if user is None:
                return {
                    "msg": "Invalid login credentials"
                }

            if not self.password_hasher.check_password(password, user.password):
                return {
                    "msg": "Invalid login credentials"
                }
            
            session_data = self.login_dao.find_session_by_email(email)
            
            new_session = self.session_manager.startSession(session_data)
            return new_session
    
        except Exception as ex:
            print(ex)
            return {
                "msg": "cannot login",
                "errorMsg": "exception"
            }
        

    def signout(self, session_cookie):
        return self.session_manager.destroy_session(session_cookie)
    

    def signup_user(self, signup_data, session_data):
        email = signup_data["email"]
        password = signup_data["password"]
        hashed_password = self.password_hasher.hash_password(password)
        signup_data["password"] = hashed_password

        if self.login_dao.find_by_email(email) is not None:
            return {"msg": "Email address already in use"}

        self.login_dao.save(signup_data)

        new_session = self.session_manager.startSession(session_data)
        return new_session
    

    def send_confirmation_code(self, email):
        try:
            if not email:
                return{'error': 'Email is required'}
            session_data = self.login_dao.find_session_by_email(email)
            if session_data is None:
                raise ValueError("Email not found in database")
            subject = "Action Required: Confirm your email"
            body = "We created an account for you. Please confirm your email address."
            self.session_manager.send_code([email], subject, body)
            return {
                "msg": "check your email!",
                "current_user": session_data,
                "logged_in": False
            }
        except ValueError as ex:
            print("Exception: "+ str(ex))
            return {
                "msg": "cannot send message",
                "errorMsg": str(ex)
            }
        except Exception as ex:
            print("Exception: "+ str(ex))
            return {
                "msg": "cannot send message",
                "errorMsg": "exception"
            }
    
    
    def verify_email(self, requestCode):
        try:
            session_data = self.session_manager.verify_confirmation_code(requestCode)
            if session_data is not None:
                email = session_data['email']
                update_data = {"isVerified": True}
                if (self.login_dao.update(email,update_data)):
                    session_data["isVerified"]=True
                    new_session = self.session_manager.startSession(session_data)
                    return new_session
                else:
                    {
                        "msg": "verification failed"
                    }
            else:
                return {
                "msg": "not equal"
                }
        except Exception as ex:
            print(ex)
            return {
                "msg": "cannot verify",
                "errorMsg": "exception"
            }
        
    def get_session_info(self):
        sessionInfo = self.session_manager.get_session_info()
        return sessionInfo
    
    def reset_password_step1(self, email):
        try:
            if self.login_dao.find_by_email(email) is not None:
                subject = "Password Reset"
                body = "We received a request to change your password."
                self.session_manager.start_reset_password_session(email)
                self.session_manager.send_code([email],subject=subject,body=body)
                return {"msg": "check your email for confirmation code"}
            else:
                return {"msg": "there is no account with this email"}
        except Exception as ex:
            print("Exception: ",str(ex))
            return {"msg": "cannot reset password", "errorMsg": "exception"}
        
    def reset_password_step2(self, requestCode):
        try:
            session_data = self.session_manager.verify_confirmation_code(requestCode)
            if session_data is not None:
                email=session_data["email"]
                self.session_manager.start_reset_password_session(email,True)
                return {"msg": "code verified"}
            else: 
                return {"msg": "code not matched"}
        except Exception as ex:
            print("Exception: ",str(ex))
            return {"msg": "cannot reset password", "errorMsg": "exception"}
    
    def reset_password_step3(self, password, session_cookie):
        try:
            session_data = self.get_session_info()["current_user"]
            email = session_data['email']
            hashed_password = self.password_hasher.hash_password(password)
            update_data = {"password": hashed_password}
            session_is_verified = self.session_manager.verify_session(session_cookie)
            
            if session_data["code_verified"] and session_is_verified:
                self.login_dao.update(email,update_data)
                self.signout(session_cookie)
                return {"msg": "password changed successfully"}
            else:
                return {"msg": "Code not verified, Try Later"}
            
        except Exception as ex:
            return {"msg": "Internal error, Try Later", "errorMsg": "exception"} 
