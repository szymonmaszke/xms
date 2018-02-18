#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Creates hierarchical database from XMind Maps."""

import argparse
import os
from getpass import getpass

import mysql.connector as connector

# IMPORT FUNCTIONS FOR CREATING DATABASE, STORING CREDS ETC.
import create_database_utils
import utils
from parse_mind_maps import parse_mind_maps

parser = argparse.ArgumentParser(description='''
    Scans through given path, makes keywords database from .xmind files\n
    which allows searching through it via xms program.\n
    !!! Run it only once before using xms program !!!\n
    ''')

parser.add_argument(
    '--connect',
    '-c',
    required=False,
    help='''Network placement of created database [DEFAULT: localhost]''',
    default='localhost')

parser.add_argument(
    '--database',
    '-d',
    required=False,
    help='''Name of the database [DEFAULT: xmindmaps]''',
    default='xmindmaps')

parser.add_argument(
    '--char',
    required=False,
    help='''Character set for the database [DEFAULT: utf8mb4]''',
    default='utf8mb4')

parser.add_argument(
    '--collation',
    required=False,
    help='''Collation of the database [DEFAULT: utf8mb4_unicode_ci]''',
    default='utf8mb4_unicode_ci')

parser.add_argument(
    '--engine',
    '-e',
    required=False,
    help='''Engine used for database creation [DEFAULT: InnoDB]''',
    default='InnoDB')

parser.add_argument(
    '--verbose',
    required=False,
    action='store_true',
    help='''If specified messages during mind map parsing will be printed''',
    default=True)

args = parser.parse_args()

print(
    'For custom installation check src/init/init.py\n'
    'For this app to work I need your MySQL credentials.\n'
    'For lookup to work they will be saved onto your system in encrypted form.\n'
    'You may specify otherwise below, but you\'ll have to provide those '
    'informations each time the searcher is ran!\n')

# Obtain user data
store_credentials = input('Store credentials?\n[Y] yes [ANY] no ')

username = input('\nMySQL username: ')
pwd = getpass('MySQL password: ')

# Obtain directory containing mind maps from user
while True:
    path = os.path.expanduser(input('\nPath to your xmind directory: '))
    if os.path.isdir(path):
        break
    print('\nCannot find this directory on your system. Are you sure about the'
          'input?',
          'Please provide correct path (fullpath/local path supported)')

try:
    # SETUP DATABASE
    utils.print_verbose("\nCreating database...", args.verbose)
    connection = connector.connect(
        user=username, password=pwd, host=args.connect, autocommit=True)
    cursor = create_database_utils.setup_database(connection, args)

    # SETUP PROCEDURES
    utils.print_verbose("Loading procedures...", args.verbose)
    create_database_utils.setup_procedures(username, pwd, args.database)
    utils.print_verbose("Procedures loaded correctly\n", args.verbose)

    # SET UP ROOT OF HIERARCHICAL DATABASE
    cursor.execute('''INSERT INTO tree (content, lft, rgt) VALUES ('root', 1,
            2) ''')

    # PARSE MIND MAPS FROM PROVIDED DIRECTORY
    parse_mind_maps(path, cursor, args.verbose)

    # STORE CREDENTIALS FOR EASIER USABILITY OF THE APPLICATION
    if store_credentials.lower() == 'y':
        utils.print_verbose('Saving user credentials for searcher use...',
                            args.verbose)
        utils.store_data(username, pwd, directory='~/.xms/', file='data')
        utils.print_verbose('Successfully saved\n', args.verbose)

    # STORE DATABASE PARAMETERS
    utils.print_verbose('Saving database and connection data for app use...',
                        args.verbose)
    utils.store_data(
        args.database, args.connect, directory='~/.xms/', file='config')
    utils.print_verbose('Successfully saved\n', args.verbose)

finally:
    connection.close()
    cursor.close()
