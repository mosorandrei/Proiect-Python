import cx_Oracle
import mysql.connector

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
conn = cx_Oracle.connect(user=r'STUDENT', password='STUDENT', dsn=dsn_tns)

c = conn.cursor()
c.execute('DROP TABLE filedatabase')

c = conn.cursor()
c.execute('CREATE TABLE filedatabase('
          + 'file_id number(10) NOT NULL,'
          + 'file_name varchar2(255) NOT NULL,'
          + 'file_type varchar2(255) NOT NULL,'
          + 'file_size varchar2(255) NOT NULL,'
          + 'file_created varchar2(255) NOT NULL,'
          + 'file_modified varchar2(255) NOT NULL,'
          + 'file_accessed varchar2(255) NOT NULL,'
          + 'public_key varchar2(255) NOT NULL,'
          + 'product_prime varchar2(255) NOT NULL'
          + ')')

c = conn.cursor()
c.execute('select * from filedatabase')

for row in c:
    print(row)

c.close()
conn.close()

connection = mysql.connector.connect(host='localhost',
                                     database='Mysql',
                                     user='root',
                                     password='STUDENT')

cursor = connection.cursor()
cursor.execute("Drop table filedatabase")

cursor = connection.cursor()
result = cursor.execute('CREATE TABLE filedatabase('
                        + 'file_id int(10) NOT NULL,'
                        + 'file_name varchar(255) NOT NULL,'
                        + 'file_type varchar(255) NOT NULL,'
                        + 'file_size varchar(255) NOT NULL,'
                        + 'file_created varchar(255) NOT NULL,'
                        + 'file_modified varchar(255) NOT NULL,'
                        + 'file_accessed varchar(255) NOT NULL,'
                        + 'public_key varchar(255) NOT NULL,'
                        + 'product_prime varchar(255) NOT NULL'
                        + ')')


cursor = connection.cursor()
result2 = cursor.execute("select * from filedatabase")

for r in cursor:
    print(r)
