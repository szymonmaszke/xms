#DODAC COMMITE'Y
import xml.etree.ElementTree as xmlET
import mysql.connector
import pexpect

from argparse import ArgumentParser
from zipfile import ZipFile
from time import sleep
from subprocess import run
from getpass import getpass
from os import walk
from copy import deepcopy

from setup_database import setup_database

#RECURSIVE READ OF MIND MAPS

MAP_ID = 1

xmind_namespace = 'urn:xmind:xmap:xmlns:content:2.0'

def recursive_read(root, id):
    if root.tag == ('{' + xmind_namespace + '}' + 'topic'):
        cursor.callproc('add_node',
                (id, root.find('xmind:title',namespaces={'xmind': xmind_namespace}).text))

        global MAP_ID
        print(' '*id + '%s' % (root.find('xmind:title',namespaces={'xmind':xmind_namespace}).text))
        # print('Added branch: ' + str(MAP_ID) , end='\r')
        MAP_ID += 1

        children = root.find('xmind:children', namespaces={'xmind': xmind_namespace})
        if children is not None:
            for elem in children:
                recursive_read(elem, id+1)
    else:
        for elem in root:
            recursive_read(elem, id)


#ARGUMENT PARSING AND MAIN PROGRAM LOGIC

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

parser.add_argument('--no_store_password', '-n', required=False, action='store_true',
    help='''Do not store password in secured file in the database\n
    WARNING! if this argument is specified, xms searcher will ask you\n
    to provide MySQL password each time!
    ''',
    default=True)

parser.add_argument('--experimental', required=False, action='store_true',
    help='''Turns on experimental functions [Mind Maps XSD validation]\n
    IMPORTANT: Slows down the program significantly\n''',
    default=False)

#OBTAIN USER DATA AND OPTIONAL SSH DATA
args = parser.parse_args()
pwd = getpass('MySQL password: ')

#CREATING DATABASE
try:
    database = mysql.connector.connect(
            user = args.user,
            password = pwd,
            host = args.connect,
            autocommit=True
    )

    #SETUP DATABASE
    print("Creating database...")
    cursor = setup_database(database, args)
    print("Database created correctly")

    #SETUP PROCEDURES
    print("Loading procedures...")
    with pexpect.spawn('mysql -u ' + args.user + ' -p') as process:
        process.expect(r'(Enter.*)')
        process.sendline(pwd)
        process.expect(r'(.*)')
        process.sendline('USE ' + args.db)
        process.expect(r'(.*)')
        process.sendline('source ../procedures/setup_procedures.sql')
        #BUDUJEMY NAPIECIE
        sleep(1)
        #ZBUDOWANO NAPIECIE
        process.close()
    print("Procedures loaded correctly\n")

    #SET UP ROOT
    cursor.execute('''INSERT INTO tree (content, lft, rgt) VALUES ('root', 1,
            2) ''')

    for subdir, dirs, files in walk(args.path):
        for file in files:
            if file.endswith('.xmind'):
                archive = ZipFile(subdir + r'/' + file, 'r')

                #EXPERIMENTAL
                if args.experimental:
                    print('Validating file ' + file)
                    run(['xmllint', '--noout', '--schema', '../validations/mind_map.xsd', archive.extract('content.xml')])
                    run(['rm', 'content.xml'])

                #SCANNING MIND MAPS
                with archive.open('content.xml', 'r') as content:
                    print('Adding branches from file ' + file + ' to database')
                    tree = xmlET.parse(content)
                    MAP_ID = 1
                    root = tree.getroot()
                    recursive_read(root, 1)
                    print('Branches from file ' + file + ' added successfully\n')

except Exception as e:
    print(e)
finally:
    cursor.close()
    database.close()
