# from api import create_app

# from flask import Flask
from api.model.users import AuthUser
from api.model.orders import Orders
from api import app


if __name__ == '__main__':
    app.run(use_reloader=False)
    AuthUser().create_table_users()
    Orders().create_orders_table()