#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities used during database creation."""

import time

import mysql.connector as connector
import pexpect

from utilities import verbose


@verbose(in_progress="Creating database...", success="Database created successfully")
def setup_database(args):
    """Create connection and setup database.

    If database of this name already exists drop it (if possible).

    Parameters
    ----------
    args : Object returned from ArgumentParser.parse_args()
           Container with arguments specified in :see create_database_utils.py
           Here, database (name of database), it's character set and collation
           (args.char and args.collation) and engine (args.engine) are used.

    Returns
    -------
    cursor
         Cursor created from connection

    """

    connection = connector.connect(
        user=args.username, password=args.pwd, host=args.connect, autocommit=True
    )

    cursor = connection.cursor()

    cursor.execute("DROP DATABASE IF EXISTS " + args.database)

    cursor.execute(
        "CREATE DATABASE {} CHARACTER SET {} COLLATE {}".format(
            args.database, args.char, args.collation
        )
    )

    cursor.execute("USE {}".format(args.database))

    cursor.execute(
        """CREATE TABLE tree (
                        content_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        content TEXT,
                        lft BIGINT NOT NULL,
                        rgt BIGINT NOT NULL,
                        FULLTEXT(content)
                    )ENGINE={}""".format(
            args.engine
        )
    )
    return cursor


@verbose(in_progress="Loading procedures...", success="Procedures loaded successfully")
def setup_procedures(user: str, password: str, connection):
    """Sources procedures through MySQL connection created as separate process.

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
    with pexpect.spawn("mysql -u {} -p".format(user)) as process:
        process.expect(r"(Enter.*)")
        process.sendline(password)
        process.expect(r"(.*)")
        process.sendline("USE {}".format(connection))
        process.expect(r"(.*)")
        process.sendline("source ./src/procedures/setup_procedures.sql")
        # WORKAROUND, ALLOWS MYSQL TO LOAD PROCEDURES
        time.sleep(2)
