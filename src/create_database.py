from argparse import ArgumentParser
from zipfile import ZipFile
from re import compile
import xml.etree.ElementTree as xmlET
import os
import mysql.connector
from argparse import ArgumentParser
from getpass import getpass

def recursive_read(root, indent):
    pass
    #print(' '*indent + '%s' % root)
    #if root.text is not None:
    #    print(' '*indent + '%s' % (root.text))
    #for elem in root.getchildren():
    #    recursive_read(elem, indent+1)

#REFAKTORYZACJA
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
        help='''Name of the database''',
        default='temp' #ZMIENIC NAZWE
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

cursor = database.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS ' + args.db)

#SCRAPPING DATA

pattern = compile(r'.*\.xmind')

for subdir, dirs, files in os.walk(args.path):
    for file in files:
        if pattern.fullmatch(file):
            print(subdir + file)
            archive = ZipFile(subdir + r'/' + file, 'r')
            tree = xmlET.parse(archive.open('content.xml', 'r'))
            recursive_read(tree.getroot(), 0)
