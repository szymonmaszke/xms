#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Store user and database credentials."""

from utilities import verbose


@verbose(
    in_progress="Saving user credentials...",
    success="Saved user credentials successfully",
)
def store_credentials(username: str, password: str, directory: str, file: str):
    """Store user credentials (username and password) in directory/file.

    See _store_data internal for implementation.

    Parameters
    ----------
    username: str
            Name of user creating database
    password: str
            Password of user creating database
    directory: str
            Directory where credentials will be stored
    file: str
            Filename where credentials will be stored

    """
    _store_data(username, password, directory, file)


@verbose(
    in_progress="Saving database info...", success="Database info saved successfully"
)
def store_connection(database: str, connection: str, directory: str, file: str):
    """Store database connection informations in directory/file.

    See _store_data internal for implementation.

    Parameters
    ----------
    database: str
            Name of created database
    connection: str
            Name of created connection
    directory: str
            Directory where credentials will be stored
    file: str
            Filename where credentials will be stored

    """
    _store_data(database, connection, directory, file)


def _store_data(data1: str, data2: str, directory: str, file: str):
    """Store specified data in directory/file


    Parameters
    ----------
    data1: str
            First string to be stored (top of the file)
    data2: str
            Second string to be stored (bottom of the file)
    directory: str
            Directory where credentials will be stored
    file: str
            Filename where credentials will be stored

    """
    if not os.path.exists(os.path.expanduser(directory)):
        os.makedirs(os.path.expanduser(directory))

    with open(os.path.expanduser(directory + file), "w") as f:
        f.writelines(
            (base64.b64encode(data1.encode("utf-8"))).decode("utf-8")
            + "\n"
            + (base64.b64encode(data2.encode("utf-8"))).decode("utf-8")
        )
