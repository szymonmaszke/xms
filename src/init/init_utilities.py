__all__ = ['setup_database', 'setup_procedures', 'store_data']

import mysql.connector
import pexpect
import time
import os
import base64

def setup_database(database, args):
    #CREATING DATABASE
    cursor = database.cursor()

    cursor.execute('DROP DATABASE IF EXISTS ' + args.db)

    cursor.execute('CREATE DATABASE ' + args.db
            + ' CHARACTER SET ' + args.char + ' COLLATE ' + args.collation
            )

    cursor.execute('USE ' + args.db)

    #MAXIMUM SIZE OF TABLE = 64 TERRABYTES, SHOULD BE ENOUGH...
    cursor.execute('''CREATE TABLE tree (
                        content_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        content TEXT NOT NULL,
                        lft BIGINT NOT NULL,
                        rgt BIGINT NOT NULL,
                        FULLTEXT(content)
                    )ENGINE=''' + args.engine
                  )
    return cursor;

def setup_procedures(user, password, database):
    with pexpect.spawn('mysql -u ' + user + ' -p') as process:
        process.expect(r'(Enter.*)')
        process.sendline(password)
        process.expect(r'(.*)')
        process.sendline('USE ' + database)
        process.expect(r'(.*)')
        process.sendline('source ../procedures/setup_procedures.sql')
        #WORKAROUND, ALLOWS MYSQL TO LOAD
        time.sleep(1)
        process.close()

def store_data(data1, data2, directory, file):
    if not os.path.exists(os.path.expanduser(directory)):
        try:
            os.makedirs(os.path.expanduser(directory))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    with open(os.path.expanduser(directory + file), 'w') as f:
        f.writelines(
                  (base64.b64encode(data1.encode('utf-8'))).decode('utf-8')
                + '\n'
                + (base64.b64encode(data2.encode('utf-8'))).decode('utf-8')
                )
