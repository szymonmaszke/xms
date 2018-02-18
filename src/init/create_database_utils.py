#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_database_utils."""

__all__ = ['setup_database', 'setup_procedures']

import time

import pexpect


def setup_database(connection, args):
    """Creates connection with specified arguments, drops if already exists.

    Parameters
    ----------
    connection : MYSQL connection object
           Object describing connection with database
    args : Object returned from ArgumentParser.parse_args()
           Container with arguments specified in :see create_database_utils.py
           Here, database (name of database), it's character set and collation
           (args.char and args.collation) and engine (args.engine) are used.

    Returns
    -------
    cursor
         Cursor created from connection

    """
    cursor = connection.cursor()

    cursor.execute('DROP DATABASE IF EXISTS ' + args.database)

    cursor.execute('CREATE DATABASE ' + args.database + ' CHARACTER SET ' +
                   args.char + ' COLLATE ' + args.collation)

    cursor.execute('USE ' + args.database)

    cursor.execute('''CREATE TABLE tree (
                        content_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        content TEXT,
                        lft BIGINT NOT NULL,
                        rgt BIGINT NOT NULL,
                        FULLTEXT(content)
                    )ENGINE=''' + args.engine)
    return cursor


def setup_procedures(user: str, password: str, connection):
    """Sources procedures through MySQL connection created as seperate process.

    IMPORTANT:
    Workaround function, python mysql-connector fails to process procedure loading
    using standard cursor operations.

    Parameters
    ----------
    user : str
           Name of the user creating the database.
    password : str
           Password used for login for said user.
    connection : MYSQL connector object
           Object describing connection with database

    """
    # connect to mysql via separate process (python's mysql-connector not
    # parsing procedures sourcing correctly... :( )
    with pexpect.spawn('mysql -u ' + user + ' -p') as process:
        process.expect(r'(Enter.*)')
        process.sendline(password)
        process.expect(r'(.*)')
        process.sendline('USE ' + connection)
        process.expect(r'(.*)')
        process.sendline('source ./src/procedures/setup_procedures.sql')
        # WORKAROUND, ALLOWS MYSQL TO LOAD PROCEDURES
        time.sleep(2)
        process.close()
