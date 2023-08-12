from functools import wraps
from controllers.login_controller import LoginController
from flask import Flask

app = Flask(__name__)
login_controller = LoginController(app)

def loginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return login_controller.decorated_function(f)(*args, **kwargs)
    return decorated_function

def signoutRequired(f):
    @wraps(f)
    def decorated_function_signout(*args, **kwargs):
        return login_controller.decorated_function_signout(f)(*args, **kwargs)
    return decorated_function_signout

@app.route('/protected_signout', methods=['GET'])
@signoutRequired
def protected_signout():
    return 'This is a protected signout-required route!'




@app.route('/protected', methods=['GET'])
@loginRequired
def protected():
    return 'This is a protected route!'


@app.route('/test', methods=['GET'])
def test():
    return 'This is a test route!'

@app.route('/user/login', methods=['POST'])
def login():
    return login_controller.login()

@app.route('/user/signout', methods=['GET'])
def logout():
    return login_controller.signout()

@app.route('/user/signup', methods=['POST'])
def register():
    return login_controller.signup()

@app.route("/user/sendConfirmationCode", methods=['POST'])
def sendConfirmationCode():
    return login_controller.sendConfirmationCode()

@app.route('/user/verifyEmail', methods=['POST'])
def verifyEmail():
    return login_controller.verifyEmail()

@app.route('/@me', methods=['GET'])
def getSessionInfo():
    return login_controller.getSessionInfo()

@app.route('/resetPasswordStep1', methods=['POST'])
def resetPasswordStep1():
    return login_controller.resetPasswordStep1()

@app.route('/resetPasswordStep2', methods=['POST'])
def resetPasswordStep2():
    return login_controller.resetPasswordStep2()

@app.route('/resetPasswordStep3', methods=['POST'])
def resetPasswordStep3():
    return login_controller.resetPasswordStep3()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)