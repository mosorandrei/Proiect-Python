import cx_Oracle

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
conn = cx_Oracle.connect(user=r'STUDENT', password='STUDENT', dsn=dsn_tns)

c = conn.cursor()
c.execute('DROP TABLE filedatabase')

c = conn.cursor()
c.execute('CREATE TABLE filedatabase('
          + 'file_id number(10) NOT NULL,'
          + 'file_name varchar2(50) NOT NULL,'
          + 'file_type varchar2(50) NOT NULL,'
          + 'file_size varchar2(50) NOT NULL,'
          + 'file_created varchar2(50) NOT NULL,'
          + 'file_modified varchar2(50) NOT NULL,'
          + 'file_accessed varchar2(50) NOT NULL,'
          + 'public_key varchar2(50) NOT NULL,'
          + 'product_prime varchar2(800) NOT NULL'
          + ')')

c = conn.cursor()
c.execute('select * from filedatabase')

for row in c:
    print(row)

c.close()
conn.close()
