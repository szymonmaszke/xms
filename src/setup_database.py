import mysql.connector

__all__ = ['setup_database']

def setup_database(database):
    #CREATING DATABASE
    cursor = database.cursor()

    cursor.execute('CREATE DATABASE IF NOT EXISTS ' + args.db
            + ' CHARACTER SET ' + args.char + ' COLLATE ' + args.collation
            )

    cursor.execute('USE ' + args.db)

    cursor.execute('DROP TABLE IF EXISTS ' + args.table)

    #MAXIMUM SIZE OF TABLE = 64 TERRABYTES, SHOULD BE ENOUGH...
    cursor.execute('CREATE TABLE ' + args.table + ''' (
                        content_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        content TEXT NOT NULL,
                        lft BIGINT NOT NULL,
                        rgt BIGINT NOT NULL
                    )ENGINE=InnoDB'''
                  )
    return cursor;
