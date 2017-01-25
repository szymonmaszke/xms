#DODAC COMMITE'Y
from argparse import ArgumentParser
from zipfile import ZipFile
import xml.etree.ElementTree as xmlET
import os
import mysql.connector
from getpass import getpass
from subprocess import run

from setup_database import setup_database
from setup_procedures import setup_procedures

def recursive_read(root, indent):
    if root.text is not None:
        print(' '*indent + '%s' % (root.text))
    for elem in root.getchildren():
        recursive_read(elem, indent+1)

#def recursive_read(root, cursor):
#    if root.text is not None:
#        cursor.callproc('add_node', root) #TBD
#    for elem in root.getchildren():
#        recursive_read(elem, indent+1)

parser = ArgumentParser(
        description='''
        Scans through given path, makes keywords database of .xmind files\n
        which allows searching through it via xms program.\n
        !!! Run it only once before using xms program !!!\n
        ''')

parser.add_argument('--format', '-f',
        help='''Format of repositories containg XMind notes, matching to regex *format*\n
        [DEFAULT: All user repositories will be cloned]\n''',
        default='.*')
parser.add_argument('--path', '-p', required=True,
        help='''Directory where XMind notes are located''')

parser.add_argument('--user', '-u', required=True,
        help='''MySQL user''')

parser.add_argument('--connect', '-c', required=False,
        help='''Placement of created database [DEFAULT: localhost]''',
        default='localhost'
        )

parser.add_argument('--db', '-d', required=False,
        help='''Name of the database [DEFAULT: mind_maps]''',
        default='mind_maps')

parser.add_argument('--table', '-t', required=False,
        help='''Name of the table [DEFAULT: mind_maps_tree]''',
        default='mind_maps_tree'
        )

parser.add_argument('--char', required=False,
        help='''Character set for the database [DEFAULT: utf-8]''',
        default='utf_8'
        )

parser.add_argument('--collation', required=False,
        help='''Character set for the database [DEFAULT: utf8_unicode_ci]''',
        default='utf8mb4_unicode_ci'
        )


#OBTAING USER DATA AND OPTIONAL SSH DATA
args = parser.parse_args()
pwd = getpass('MySQL password: ')

#CREATING DATABASE
database = mysql.connector.connect(
        user = args.user,
        password = pwd,
        host = args.connect
)

cursor = setup_database(database)
setup_procedures(cursor)

#CREATE TREE ROOT
cursor.execute('INSERT INTO ' + args.table + ''' (content, lft, rgt) VALUES ('root', 1, 2) ''')

#SCRAPPING DATA

for subdir, dirs, files in os.walk(args.path):
    for file in files:
        if file.endswith('.xmind'):
            archive = ZipFile(subdir + r'/' + file, 'r')
            tree = xmlET.parse(archive.open('content.xml', 'r'))
            #if run(['xmllint', '--noout', '--schema', tree]).returncode == 1:
            #    print(subdir + file)
            recursive_read(tree.getroot(), 0)
