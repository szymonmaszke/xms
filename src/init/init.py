import mysql.connector as db
import argparse
import subprocess
import os

from getpass import getpass

#IMPORT FUNCTIONS FOR CREATING DATABASE, STORING CREDS ETC.
import init_utilities
from parse_mind_maps import parse_mind_maps

parser = argparse.ArgumentParser(
    description='''
    Scans through given path, makes keywords database of .xmind files\n
    which allows searching through it via xms program.\n
    !!! Run it only once before using xms program !!!\n
    ''')

parser.add_argument('--user', '-u', required=True,
    help='''MySQL user''')

parser.add_argument('--path', '-p', required=True,
    help='''Directory where XMind notes are located''')

parser.add_argument('--connect', '-c', required=False,
    help='''Placement of created database [DEFAULT: localhost]''',
    default='localhost')

parser.add_argument('--db', '-d', required=False,
    help='''Name of the database [DEFAULT: xmindmaps]''',
    default='xmindmaps')

parser.add_argument('--char', required=False,
    help='''Character set for the database [DEFAULT: utf8mb4]''',
    default='utf8mb4')

parser.add_argument('--collation', required=False,
    help='''Character set for the database [DEFAULT: utf8mb4_unicode_ci]''',
    default='utf8mb4_unicode_ci')

parser.add_argument('--engine', '-e', required=False,
    help='''Engine used for database creation [DEFAULT: InnoDB]''',
    default='InnoDB')

parser.add_argument('--store_credentials', '-s', required=False, action='store_true',
    help='''Do not store username and password in secured file in $HOME/.xms/config\n
    WARNING! if this argument is specified as False, xms searcher will ask you\n
    to provide MySQL credentials each time it's run!
    ''',
    default=True)

parser.add_argument('--experimental', required=False, action='store_true',
    help='''Turns on experimental functions [Mind Maps XSD validation]\n
    IMPORTANT: Slows down the program significantly\n''',
    default=False)

#OBTAIN USER DATA
args = parser.parse_args()
pwd = getpass('MySQL password: ')
if args.store_credentials:
    print('\nSaving user credentials for app use...')
    init_utilities.store_data(args.user, pwd, directory='~/.xms/', file='data')
    print('Successfully saved')
print('\nSaving database and connection data for app use...')
init_utilities.store_data(args.db, args.connect, directory='~/.xms/', file='config')
print('Successfully saved\n')

#CREATING DATABASE
try:
    database = db.connect(
            user = args.user,
            password = pwd,
            host = args.connect,
            autocommit=True
    )

    #SETUP DATABASE
    print("Creating database...")
    cursor = init_utilities.setup_database(database, args)
    print("Database created correctly")

    #SETUP PROCEDURES
    print("Loading procedures...")
    init_utilities.setup_procedures(args.user, pwd, args.db)
    print("Procedures loaded correctly\n")

    #SET UP ROOT
    cursor.execute('''INSERT INTO tree (content, lft, rgt) VALUES ('root', 1,
            2) ''')

    #PARSE MIND MAPS FROM GIVEN DIRECTORY
    parse_mind_maps(args.path, cursor, experimental=args.experimental)

    #STORE CREDENTIALS
    # if args.store_credentials:
    #     print('Saving user configuration for app use...')
    #     store_data(args.user, pwd, args.db, args.connect, directory='~/.xms', file='config')
    #     print('Successfully saved')

except Exception as e:
    print(e)
finally:
    cursor.close()
    database.close()
