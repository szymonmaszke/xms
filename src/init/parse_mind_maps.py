#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""parse_mind_maps."""

__all__ = ['parse_mind_maps']

import os
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import utils

XMIND_NAMESPACE = 'urn:xmind:xmap:xmlns:content:2.0'
# Id used to display branch number to user during db creation
BRANCH_ID = 1


def _recursive_parse(root, cursor, parent_id: int):
    """Parse XML ETree root recursively and add it to hierarchical database.

    If root's tag consists of 'topic' we have found branch containing text.
    In such case call MySQL procedure adding node to parent (specified by
    parent_id), print information and proceed to parse children of current root
    (if exist).


    Parameters
    ----------
    root : class xml.etree.ElementTree.Element
           Current root to be parsed
    cursor : MySQL connector cursor
           Cursor for MySQL queries execution
    parent_id : int
           Id of parent branch

    """
    # TEXTUAL XML BRANCH, PROCESS IT
    if root.tag == ('{' + XMIND_NAMESPACE + '}' + 'topic'):
        root_text = root.find(
            'xmind:title', namespaces={
                'xmind': XMIND_NAMESPACE
            }).text

        inserted_id = cursor.callproc(
            'add_node',  # name of procedure to be called
            (
                parent_id,  # parent branch id
                root_text,  # text in branch to be inserted
                0,  # placeholder value for inserted_id variable
            ))[2]

        global BRANCH_ID
        print('Added branch: ' + str(BRANCH_ID), end='\r')
        BRANCH_ID += 1

        # PARSE CHILDREN

        children = root.find(
            'xmind:children', namespaces={'xmind': XMIND_NAMESPACE})
        if children is not None:
            for elem in children:
                _recursive_parse(elem, cursor, inserted_id)

    # BRANCH WITHOUT TEXTUAL INFORMATIONS, PROCESS TO NEXT ELEMENTS
    else:
        for elem in root:
            _recursive_parse(elem, cursor, parent_id)


def parse_mind_maps(path: str, cursor, verbose: bool):
    """Adds mind maps to database using cursor and recursive XML parsing.

    Parameters
    ----------
    path : str
           Path containing every mind map
    cursor : MySQL connector cursor
           Cursor for MySQL queries execution
    verbose : bool
           <argument description>

    """
    for subdir, _, files in os.walk(path):
        for file in files:
            # XMind mind map's are .zip files with various files, open them as
            # zip
            if file.endswith('.xmind'):
                archive = ZipFile(subdir + r'/' + file, 'r')

                # Open textual content of mind map .zip archive
                with archive.open('content.xml', 'r') as content:
                    utils.print_verbose(
                        'Adding branches from {} to database'.format(file),
                        verbose,
                    )

                    global BRANCH_ID
                    BRANCH_ID = 1

                    root = ET.parse(content).getroot()
                    _recursive_parse(root, cursor, 1)

                    utils.print_verbose(
                        'Successfully added {} branches from file {} \n'
                        .format(str(BRANCH_ID), file),
                        verbose,
                    )
