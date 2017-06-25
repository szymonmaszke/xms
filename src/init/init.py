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

parser.add_argument('--experimental', required=False, action='store_true',
    help='''Turns on experimental functions [Mind Maps XSD validation]\n
    IMPORTANT: Slows down the program significantly\n''',
    default=False)

parser.add_argument('--docker', required=False, action='store_true',
    help='''Shows information about dependencies if app is not run from docker
    container''',
    default=False)

#OBTAIN USER DATA
args = parser.parse_args()

if not args.docker:
    print('IMPORTANT: This software needs three specified dependencies (listed in dependencies.txt). Make sure you have them!')
    print('IMPORTANT: You should follow system-specific installation instructions for each of them.\n')

print('For custom installation check src/init/init.py\n')

print('For this app to work I need your MySQL credentials.')
print('For lookup to work they have to be saved onto your system in encrypted form.')
print("You may specify otherwise below, but you'll have to provide those informations each time the searcher is ran!\n")

store_credentials = input('Store credentials?\n[Y] yes [ANY] no ')

username = input('\nMySQL username: ')
pwd = getpass('MySQL password: ')
#ADD BETTER DATA VALIDATION
while(True):
    path = os.path.expanduser(input('\nPath to your xmind directory (specify fullpath): '))
    if os.path.isdir(path):
        break;
    print('\nCannot find this directory on your system. Are you sure about the input?')
    print('Please provide correct path (fullpath/localpaths supported)')

#CREATING DATABASE
try:
    database = db.connect(
            user = username,
            password = pwd,
            host = args.connect,
            autocommit=True
    )

    #SETUP DATABASE
    print("\nCreating database...")
    cursor = init_utilities.setup_database(database, args)
    print("Database created correctly")

    #SETUP PROCEDURES
    print("Loading procedures...")
    init_utilities.setup_procedures(username, pwd, args.db)
    print("Procedures loaded correctly\n")

    #SET UP ROOT
    cursor.execute('''INSERT INTO tree (content, lft, rgt) VALUES ('root', 1,
            2) ''')

    #PARSE MIND MAPS FROM GIVEN DIRECTORY
    parse_mind_maps(path, cursor, experimental=args.experimental)

    if store_credentials.lower() == 'y':
        print('Saving user credentials for searcher use...')
        init_utilities.store_data(username, pwd, directory='~/.xms/', file='data')
        print('Successfully saved\n')

    print('Saving database and connection data for app use...')
    init_utilities.store_data(args.db, args.connect, directory='~/.xms/', file='config')
    print('Successfully saved\n')

except Exception as e:
    print(e)
finally:
    cursor.close()
    database.close()
