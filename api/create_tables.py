import psycopg2
from api import conn


class CreateTables:

    @staticmethod
    def create_tables():
        
        """ create tables in the PostgreSQL database"""
        commands = (
              """
            CREATE TABLE IF NOT EXISTS users  (
                user_id SERIAL PRIMARY KEY,
                first_name VARCHAR(200) NOT NULL,
                last_name VARCHAR(200) NOT NULL,
                email VARCHAR(200) NOT NULL,
                phone_contact VARCHAR(200) NULL,
                username VARCHAR(255) NOT NULL UNIQUE, 
                user_password VARCHAR(255) NOT NULL,
                user_type VARCHAR(200) NOT NULL
            )
            """
            ,
           """
            CREATE TABLE IF NOT EXISTS orders (
                parcel_order_id SERIAL PRIMARY KEY,
                senders_user_id INTEGER NOT NULL,
                order_name VARCHAR(100) NOT NULL,
                parcel_weight INTEGER NOT NULL,
                price BIGINT NOT NULL,
                parcel_pickup_address VARCHAR(100) NOT NULL,
                parcel_destination_address VARCHAR(100) NOT NULL,
                order_status VARCHAR(100)  DEFAULT 'pending',
                receivers_names VARCHAR(100) NOT NULL,
                receivers_contact VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                ordering_time TIME DEFAULT NOW(),
                location VARCHAR(100) NOT NULL,
                FOREIGN KEY (senders_user_id)
                    REFERENCES users(user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
            """
        )

        cursor = conn.cursor()
        # create table one by one
        for command in commands:
            cursor.execute(command)
        # close communication with the PostgreSQL database server
        cursor.close()
        # commit the changes
        conn.commit()
        

    if __name__ ==  '__main__':
        create_tables()