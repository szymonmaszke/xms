__all__ = ['menu', 'receive_data']

import os
import base64
import pathlib

from getpass import getpass

def find_keyword(cursor, keyword):
    id = 0
    while True:
        cursor.callproc('find_node', [keyword, id])

        for results in cursor.stored_results():
            # [1:] So it won't fetch root
            result = results.fetchall()[1:]
            if not result:
                print('No results found\n')
                return
            for indent, branch in enumerate(result):
                print(' '*indent + '%s' %branch)

        decision = input('\nShow next result?\n [Y] yes [ANY] quit\n')
        if decision.lower() != 'y':
            return
        print()
        id += 1
    return

def receive_data(
        directory,filename,
        error_message, not_found_message,
        first_prompt_message, second_prompt_message
        ):

    secret = pathlib.Path(os.path.expanduser(directory + filename))
    if secret:
        try:
            with open(os.path.expanduser(directory + filename), 'r') as f:
               return [(base64.b64decode(data)).decode('utf-8') for data in f.read().splitlines()]
        except Exception as e:
            print(error_message)
            data1 = input(first_prompt_message)
            data2 = getpass(second_prompt_message)
            return [data1, data2]
    else:
        print(not_found_message)
        data1 = input(first_prompt_message)
        data2 = getpass(second_prompt_message)
        return [data1, data2]
