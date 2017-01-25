#DODAC COMMITE'Y
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
        help='''Name of the database [DEFAULT: mind_maps]''',
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
cursor.callproc('find_node', (args.keyword,))

for result in cursor.stored_results():
    limit = 0
    for branch in result.fetchall():
        if limit % 5 == 0:
            print('%s' % branch)
        else:
            print('%s' % branch, end='->')
        limit += 1
