__all__ = ['create_database']

from zipfile import ZipFile
from re import compile
import xml.etree.ElementTree as xmlET
import os

def recursive_read(root, indent):
    if root.text is not None:
        print(' '*indent + '%s' % (root.text))
    for elem in root.getchildren():
        recursive_read(elem, indent+2)


def create_database(path):
    pattern = compile(r'.*\.xmind')
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if pattern.fullmatch(file):
                archive = ZipFile(subdir + r'/' + file, 'r')
                tree = xmlET.parse(archive.open('content.xml', 'r'))
                recursive_read(tree.getroot(), 0)
