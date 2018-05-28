#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Perform search through hierarchical database of mind maps."""

import argparse
import os

import mysql.connector

# IMPORT MENU, READING CREDENTIALS, DATABASE DATA
from xms_utilities import find_keyword, receive_data


def parse_arguments():
    """parse_arguments (short summary)."""
    parser = argparse.ArgumentParser(
        description="""
            Scans through xmind notes and returns path and exact branch regarding your query\n\n
            [IMPORTANT]\n\n
            Before running this program you need to initialize database, check README.txt\n
            """
    )

    parser.add_argument("keyword", help="keyword to search for")
    parser.add_argument(
        "--color",
        "-c",
        required=False,
        action="store_true",
        help="""colorize the output? [DEFAULT: false]""",
        default=False,
    )

    parser.add_argument(
        "--secret",
        "-s",
        required=False,
        help="""directory containing secret data [DEFAULT: ~/.xms]""",
        default="~/.xms",
    )

    parser.add_argument(
        "--keep",
        "-k",
        required=False,
        action="store_true",
        help="Keep all output on screen instead of clearing terminal? [DEFAULT:"
        "false]",
        default=False,
    )

    return parser.parse_args()


def start_searcher(args):
    """<short summary>.

    <extended summary>

    Parameters
    ----------
    args : type
            <argument description>

    Returns
    -------
    type
            <return description>

    """
    # OBTAIN USER DATA
    username, password = receive_data(
        path=os.path.join(args.secret, "data"),
        error_message="Error occured when reading file, requesting credentials...",
        not_found_message="File not found, requesting credentials...",
        first_prompt_message="MySQL username: ",
        second_prompt_message="Password: ",
    )

    # OBTAIN DATABASE DATA
    database, connection = receive_data(
        path=os.path.join(args.secret, "config"),
        error_message="Error occured when reading file,"
        "requesting database and connection information...",
        not_found_message="File not found, "
        "requesting database and connection information...",
        first_prompt_message="Name of database: ",
        second_prompt_message="IP of database [e.g. localhost]: ",
    )

    # CONNECT TO DATABASE

    connection = mysql.connector.connect(
        user=username, password=password, host=connection, database=database
    )

    cursor = connection.cursor()

    # FIND KEYWORD
    find_keyword(cursor, args.keyword, args.color, args.keep)


if __name__ == "__main__":
    args = parse_arguments()
    start_searcher(args)
