from api import connection

class DropTables:
    @staticmethod
    def drop_tables_after_running_tests():
        """ drop tables in test database after running tests """
        commands = (
            """
            DROP TABLE users
            """,
            """
            DROP TABLE  orders 
            """
        )
        
        cursor = connection.cursor()
        # create table one by one
        for command in commands:
            cursor.execute(command)
        # commit the changes
        connection.commit()
