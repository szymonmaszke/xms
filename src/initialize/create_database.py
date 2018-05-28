#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create hierarchical database from XMind Maps."""

import argparse
import os
from getpass import getpass

# IMPORT FUNCTIONS FOR CREATING DATABASE, STORING CREDS ETC.
from create_database_utils import setup_database, setup_procedures
from parse_mind_maps import parse_mind_maps
from store_data import store_connection, store_credentials


def parse_arguments():
    """Parse user provided arguments."""
    parser = argparse.ArgumentParser(
        description="""
        Scans through given path, makes keywords database from .xmind files\n
        which allows searching through it via xms program.\n
        !!! Run it only once before using xms program !!!\n
        """
    )

    parser.add_argument(
        "--connect",
        "-c",
        required=False,
        help="""Network placement of created database [DEFAULT: localhost]""",
        default="localhost",
    )

    parser.add_argument(
        "--database",
        "-d",
        required=False,
        help="""Name of the database [DEFAULT: xmindmaps]""",
        default="xmindmaps",
    )

    parser.add_argument(
        "--char",
        required=False,
        help="""Character set for the database [DEFAULT: utf8mb4]""",
        default="utf8mb4",
    )

    parser.add_argument(
        "--collation",
        required=False,
        help="""Collation of the database [DEFAULT: utf8mb4_unicode_ci]""",
        default="utf8mb4_unicode_ci",
    )

    parser.add_argument(
        "--engine",
        "-e",
        required=False,
        help="""Engine used for database creation [DEFAULT: InnoDB]""",
        default="InnoDB",
    )

    parser.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="""If specified messages during mind map parsing will be printed""",
        default=True,
    )

    return parser.parse_args()


def get_user_data():
    """Get data from user (username, password and whether to store credentials)."""
    credentials_storing = input("Store credentials?\n[Y] yes [ANY] no ")

    username = input("\nMySQL username: ")
    pwd = getpass("MySQL password: ")

    # Obtain directory containing mind maps from user
    while True:
        path = os.path.expanduser(input("\nPath to your xmind directory: "))
        if os.path.isdir(path):
            break
        print(
            "\nCannot find this directory on your system. Are you sure about the"
            "input?",
            "Please provide correct path (fullpath/local path supported)",
        )

    return credentials_storing, username, pwd, path


def create_database(
    args, credentials_storing: bool, username: str, password: str, path: str
):
    """Create database from XMind Mind maps.

    Parameters
    ----------
    args : type
            <argument description>
    {{_indent}}credentials_storing:{{_indent}} : type
            <argument description>
    {{_indent}}username:{{_indent}} : type
            <argument description>
    {{_indent}}password:{{_indent}} : type
            <argument description>
    {{_indent}}path:{{_indent}} : type
            <argument description>

    Returns
    -------
    type
            <return description>

    """
    with setup_database(args) as cursor:

        setup_procedures(args.username, args.pwd, args.database)

        # SET UP ROOT OF HIERARCHICAL DATABASE
        cursor.execute(
            """INSERT INTO tree (content, lft, rgt) VALUES ('root', 1,
                2) """
        )

        # PARSE MIND MAPS FROM PROVIDED DIRECTORY
        parse_mind_maps(path, cursor, args.verbose)

        if credentials_storing.lower() == "y":
            store_credentials(username, password, directory="~/.xms/", file="data")
        store_connection(
            args.database, args.connect, directory="~/.xms/", file="config"
        )


if __name__ == "__main__":
    args = parse_arguments()
    print(
        "For custom installation check src/init/init.py\n"
        "For this app to work I need your MySQL credentials.\n"
        "For lookup to work they will be saved onto your system in encrypted form.\n"
        "You may specify otherwise below, but you'll have to provide those "
        "informations each time the searcher is ran!\n"
    )
    user_data = get_user_data()
    create_database(args, *user_data)
