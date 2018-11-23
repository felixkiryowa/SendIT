# from api import create_app

# from flask import Flask
from api import app
from api.model.users import AuthUser
if __name__ == '__main__':
    AuthUser.create_default_admin_user()
    app.run(debug=True, use_reloader=False)