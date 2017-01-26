#!/usr/bin/env python

from argparse import ArgumentParser
import mysql.connector
from getpass import getpass

parser = ArgumentParser(
        description='''
        Scans through xmind notes and returns path and exact branch to your query\n\n
        [IMPORTANT]\n\n
        Before running this program you need to initialize database, check README.txt\n
        ''')

parser.add_argument('keyword',
        help='Keyword to be searched for')
parser.add_argument('--user', '-u', required=True,
        help='''MySQL user''')

parser.add_argument('--connect', '-c', required=False,
        help='''Placement of created database [DEFAULT: localhost]''',
        default='localhost'
        )

parser.add_argument('--database', '-d', required=False,
        help='''Name of the database [DEFAULT: xmindmaps]''',
        default='xmindmaps')


#OBTAING USER DATA AND OPTIONAL SSH DATA
args = parser.parse_args()
pwd = getpass('MySQL password: ')

#CONECTING TO DATABASE
database = mysql.connector.connect(
        user = args.user,
        password = pwd,
        host = args.connect,
        database = args.database
)

cursor = database.cursor()

id = 0
while True:
    print()
    cursor.callproc('find_node', [args.keyword, id])

    for result in cursor.stored_results():
        for indent, branch in enumerate(result.fetchall()[1:]):
            print(' '*indent + '%s' %branch)
    decision = input('\nShow next result?\n [Y] yes [OTHER] no ')
    if decision.lower() != 'y':
        break
    id += 1
