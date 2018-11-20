import os
import psycopg2
import pprint
from api.config import app_config


# test_connection = psycopg2.connect(database="test_db",user="francis",password="atagenda1@",host="localhost",port="5432")
# conn = psycopg2.connect(database="SendIT")

class DatabaseConnection:

    def DB(self):
        try:
            # if app_config['testing']:
            #     self.conn = psycopg2.connect("dbname = 'test_sendit' user ='postgres' host = 'localhost' password = 'postgres' port = '5432'")
            #     self.cursor = self.conn.cursor()
            #     return self.cursor
            if app_config['testing']:
                self.conn = psycopg2.connect(database="test_db",user="postgres",password="atagenda1@",host="localhost",port="5432")
                self.cur = self.conn.cursor()
                self.cur_list = [self.conn, self.cur]
                return self.cur_list
            # elif app_config['production']:
            #     self.conn = psycopg2.connect("dbname = 'd6g1ajbujg1285', user = 'lczfiodmgblubu' host = 'ec2-54-235-193-0.compute-1.amazonaws.com' password = '76487fa95068a43af7da7deab9bd4783e1bc97659503032e4b37a6ee5199769c' port = '5432'")
            #     self.cursor = self.conn.cursor()
            #     return self.cursor
            elif app_config['development']:
                self.conn = psycopg2.connect(database="SendIT",user="postgres",password="atagenda1@",host="localhost",port="5432")
                self.cursor = self.conn.cursor()
                self.cur_list = [self.conn, self.cur]
                return self.cur_list
        except (Exception, psycopg2.DatabaseError) as error:
            pprint(error)
    





