from argparse import ArgumentParser
from github3 import login
from getpass import getpass
from re import compile
from subprocess import run
import pexpect
import os

from create_database import create_database

parser = ArgumentParser(
        description='''
        Scans through folders/GitHub repositories, makes database of keywords\n
        and allows searching through it via xms program.\n
        !!! Run it only once before using xms program !!!\n
        ''')

parser.add_argument('--user', '-u', required=True, help='Your GitHub username')
parser.add_argument('--nickname', '-n',
        help='''Nick of user whos repository you want to obtain\n
        [DEFAULT EQUAL TO USER]\n''')
parser.add_argument('--format', '-f',
        help='''Format of repositories containg XMind notes, matching to regex *format*\n
        [DEFAULT: All user repositories will be cloned]\n''',
        default='.*')
parser.add_argument('--ssh', '-s', action='store_true',
        help='''Clones repositories via SSH if provided\n''')
parser.add_argument('--path', '-p', required=True,
        help='''Directory where to place notes folder including XMind notes''')


#OBTAING USER DATA AND OPTIONAL SSH DATA
args = parser.parse_args()
password = getpass('GitHub password:')
ssh_password = ''
if args.ssh:
    ssh_password = getpass('SSH Github password: ')

g = login(args.user, password)

#OBTAINING GITHUB USER FROM WHICH WE'LL CLONE REPOSITORIES
user = args.nickname
if args.nickname is None:
    user = args.user

#SETTING UP NOTES FORMAT IN REPOSITORIES
notes_pattern = compile(r'/.*/' + r'(.*' + args.format + r'.*)')

#SETTING UP FOLDERS INCLUDING NOTES
current_path = os.getcwd()
if not os.path.exists(args.path):
    os.makedirs(args.path)

os.chdir(args.path)


#DOWNLOADING REPOSITORIES VIA HTTPS/SSH MATCHING THE PATTERN
for repo in g.iter_user_repos(user, type='user'):
    repo_name = notes_pattern.findall(repo.clone_url)
    if repo_name:
        if args.ssh:
            login = pexpect.spawn('git clone git@github.com:' + user + '/' + repo_name[0])
            login.expect(r'(Enter.*)')
            login.sendline(ssh_password)
            print(login.before)
            login.interact()
        else:
            run(['git', 'clone', 'https://github.com/' + user + '/' + repo_name[0]])

os.chdir(current_path)

create_database(args.path)
