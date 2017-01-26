import mysql.connector

__all__ = ['setup_database']

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
