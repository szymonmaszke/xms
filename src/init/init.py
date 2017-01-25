#DODAC COMMITE'Y
from argparse import ArgumentParser
from zipfile import ZipFile
import xml.etree.ElementTree as xmlET
import os
import mysql.connector
from getpass import getpass
from subprocess import run, Popen, PIPE
import sys

from setup_database import setup_database
sys.path.append('../procedures')
from setup_procedures import setup_procedures

id = 1
def recursive_read(root, cursor, database):
    global id
    if root.text is not None:
        cursor.callproc('add_node', (id, root.text))
        database.commit()
        print('Gathering data...')
        id += 1
    for elem in root.getchildren():
        recursive_read(elem, cursor, database)

def func():
    parser = ArgumentParser(
            description='''
            Scans through given path, makes keywords database of .xmind files\n
            which allows searching through it via xms program.\n
            !!! Run it only once before using xms program !!!\n
            ''')

    parser.add_argument('--user', '-u', required=True,
            help='''MySQL user''')

    parser.add_argument('--path', '-p', required=True,
            help='''Directory where XMind notes are located''')

    parser.add_argument('--format', '-f', required=False,
            help='''Format of repositories containg XMind notes, matching to regex *format*\n
            [DEFAULT: All user repositories will be cloned]\n''',
            default='.*')

    parser.add_argument('--connect', '-c', required=False,
            help='''Placement of created database [DEFAULT: localhost]''',
            default='localhost'
            )

    parser.add_argument('--db', '-d', required=False,
            help='''Name of the database [DEFAULT: mind_maps]''',
            default='xmindmaps')

    parser.add_argument('--table', '-t', required=False,
            help='''Name of the table [DEFAULT: tree]''',
            default='tree'
            )

    parser.add_argument('--char', required=False,
            help='''Character set for the database [DEFAULT: utf8mb4]''',
            default='utf8mb4'
            )

    parser.add_argument('--collation', required=False,
            help='''Character set for the database [DEFAULT: utf8mb4_unicode_ci]''',
            default='utf8mb4_unicode_ci'
            )

    parser.add_argument('--experimental', '-e', required=False, action='store_true',
            help='''Turns on experimental functions [Mind Maps XSD validation]\n
            IMPORTANT: Slows down the program significantly\n''',
            default=False
            )


    #OBTAING USER DATA AND OPTIONAL SSH DATA
    args = parser.parse_args()
    pwd = getpass('MySQL password: ')

    #CREATING DATABASE
    try:
        database = mysql.connector.connect(
                user = args.user,
                password = pwd,
                host = args.connect
        )

        #SETUP DATABASE
        cursor = setup_database(database, args)

        #SET UP ROOT
        cursor.execute('INSERT INTO ' + args.table + ''' (content, lft, rgt) VALUES ('root', 1, 2) ''')

        #SET UP PROCEDURES
        #setup_procedures(cursor, args.db, args.table, database)
        #process = Popen(['mysql', args.db, '-u', args.user, '-p', pwd], stdout=PIPE, stdin=PIPE)
        #output = process.communicate(b'source ' + b'setup_procedures.sql')[0]
        database.commit()

        #SCRAPPING DATA

        for subdir, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith('.xmind'):
                    archive = ZipFile(subdir + r'/' + file, 'r')
                    if args.experimental:
                        run(['xmllint', '--noout', '--schema', './mind_map.xsd', archive.extract('content.xml')])
                    with archive.open('content.xml', 'r') as content:
                        tree = xmlET.parse(content)
                        recursive_read(tree.getroot(), cursor, database)
    finally:
        cursor.close()
        database.close()

if __name__ == '__main__':
    func()
