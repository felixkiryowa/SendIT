# from api import create_app

# from flask import Flask
from api import app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)