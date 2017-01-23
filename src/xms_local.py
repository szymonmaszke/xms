from argparse import ArgumentParser
from re import compile
import os

from create_database import create_database

parser = ArgumentParser(
        description='''
        Scans through given path, makes keywords database of .xmind files\n
        and allows searching through it via xms program.\n
        !!! Run it only once before using xms program !!!\n
        ''')

parser.add_argument('--format', '-f',
        help='''Format of repositories containg XMind notes, matching to regex *format*\n
        [DEFAULT: All user repositories will be cloned]\n''',
        default='.*')
parser.add_argument('--path', '-p', required=True,
        help='''Directory where to place notes folder including XMind notes''')


#OBTAING USER DATA AND OPTIONAL SSH DATA
args = parser.parse_args()

#SETTING UP NOTES FORMAT IN REPOSITORIES
notes_pattern = compile(r'/.*/' + r'(.*' + args.format + r'.*)')

#SETTING UP FOLDERS INCLUDING NOTES
create_database(args.path)
