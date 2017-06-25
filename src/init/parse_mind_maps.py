__all__ = ['parse_mind_maps']

import xml.etree.ElementTree as ET
import subprocess
import os
from zipfile import ZipFile

#PARSE AND ADD MIND MAP TO DATABASE
xmind_namespace = 'urn:xmind:xmap:xmlns:content:2.0'
MAP_ID = 1

def recursive_read(root, cursor, id):
    if root.tag == ('{' + xmind_namespace + '}' + 'topic'):
        inserted_id = cursor.callproc(
                'add_node',
                (id, root.find('xmind:title',namespaces={'xmind':xmind_namespace}).text,
                0 #PLACEHOLDER FOR INSERTED_ID
                ))[2]

        global MAP_ID
        print('Added branch: ' + str(MAP_ID) , end='\r')
        MAP_ID += 1

        children = root.find('xmind:children', namespaces={'xmind': xmind_namespace})
        if children is not None:
            for elem in children:
                recursive_read(elem, cursor, inserted_id)
    else:
        for elem in root:
            recursive_read(elem, cursor, id)

def parse_mind_maps(path, cursor, experimental):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xmind'):
                archive = ZipFile(subdir + r'/' + file, 'r')

                #EXPERIMENTAL VALIDATION OF MIND MAP WITH XSD FILE
                if experimental:
                    print('Validating file ' + file)
                    subprocess.run(['xmllint', '--noout', '--schema', '../validations/mind_map.xsd', archive.extract('content.xml')])
                    subprocess.run(['rm', 'content.xml'])

                #SCANNING MIND MAPS
                with archive.open('content.xml', 'r') as content:
                    print('Adding branches from file ' + file + ' to database')
                    tree = ET.parse(content)
                    root = tree.getroot()
                    global MAP_ID
                    MAP_ID = 1
                    recursive_read(root, cursor, 1)
                    print('Successfully added ' + str(MAP_ID) + ' branches from file ' + file + '\n')
