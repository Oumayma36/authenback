Flask Web Application:
This is a Flask web application that provides user authentication and registration functionality. The application uses a LoginController object to handle the actual authentication and registration logic, while the Flask routes simply call the appropriate methods of the LoginController object.

Installation:
To install the application, you will need to have Python 3 and pip installed on your system. Once you have these dependencies installed, you can install the required Python packages by running the following command:

pip install -r requirements.txt

Usage:
To run the application, you can execute the following command:

python routes.py

This will start the Flask development server, which you can access by navigating to http://localhost:5000 in your web browser.

The application provides the following routes:

/user/login: A POST route that handles user authentication.
/user/logout: A POST route that handles user logout.
/user/register: A POST route that handles user registration.
/test: A GET route that returns a simple string indicating that the route is a test route.