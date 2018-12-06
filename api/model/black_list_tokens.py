"""This is users class defining the used tokens model constructor """
from  api import connection
from flask import jsonify

cursor = connection.cursor()

class BlackListTokens:

    cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tokensblacklisted  (
                token_id SERIAL PRIMARY KEY,
                used_token VARCHAR(500) NOT NULL
            )
            """
    )

    def __init__(self, *args):
        """This is AuthUsers class constructor"""
        self.token = args[0]

    
    def execute_save_used_token_query(self):
        """ insert a used token into the tokensblacklisted table """
        sql = """INSERT INTO tokensblacklisted(used_token)
        VALUES(%s) RETURNING token_id;"""
        # create a new cursorsor
        cursor = connection.cursor()
        cursor.execute(sql, (self.token, ))
        # commit the changes to the database
        connection.commit()
        return jsonify({'message':'success'})
    
    

