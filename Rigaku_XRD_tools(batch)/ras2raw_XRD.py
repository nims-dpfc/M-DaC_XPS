#-------------------------------------------------
# ras2raw.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
#-------------------------------------------------
# coding: utf-8

import argparse
import os.path
import csv
import pandas as pd
from dateutil.parser import parse
import xml.dom.minidom
import re
import xml.etree.ElementTree as ET
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
parser.add_argument("template_file")
parser.add_argument("out_file")
options = parser.parse_args()
readfile = options.file_path
encoding_option = options.encoding
templatefile = options.template_file
outputfile = options.out_file
channel = 0

template = ET.parse(templatefile)
columns=[]
metas = template.findall('meta')
for meta in metas:
    columns.append(meta.attrib["key"])
dom = xml.dom.minidom.Document()
metadata = dom.createElement('metadata')
dom.appendChild(metadata)
count = 0
wide = 1
maxcolumn = 1
df = pd.DataFrame(index=['value'])
with open(readfile, 'r', encoding=encoding_option) as f:
    for line in f:
        line = line.strip()
        line = line[1:]
        if line == 'RAS_HEADER_END':
            break
        elif not(line == 'RAS_DATA_START' or line == 'RAS_HEADER_START'):
            lines = line.split(" ", 1)
            key = lines[0]
            tempvalue = lines[1]
            value = tempvalue[1:-1]
            temp = template.find('meta[@key="{value}"]'.format(value=key))            
            if temp != None:
                df[key] = value

for meta in metas:
    key = meta.attrib["key"]
    if key in df.columns:
        value = df.loc['value', key]
    else:
        value = ""
    subnode = dom.createElement('meta')
    subnode.appendChild(dom.createTextNode(value))
    subnode_attr = dom.createAttribute('key')
    subnode_attr.value = key
    subnode.setAttributeNode(subnode_attr)
    metadata.appendChild(subnode)

    subnode_attr = dom.createAttribute('type')
    typename = template.find('meta[@key="{value}"]'.format(value=key))
    if typename.get("type") != None:
        subnode_attr.value = typename.get("type")
    else:
        subnode_attr.value = "String"
    subnode.setAttributeNode(subnode_attr)
    metadata.appendChild(subnode)

    if channel != 0:
        subnode_attr = dom.createAttribute('column')
        subnode_attr.value = channel
        subnode.setAttributeNode(subnode_attr)
        metadata.appendChild(subnode)
subnode = dom.createElement('column_num')
subnode.appendChild(dom.createTextNode(str(maxcolumn)))
metadata.appendChild(subnode)
column_name = template.find('column_name').text
subnode = dom.createElement('column_name')
subnode.appendChild(dom.createTextNode(column_name))
metadata.appendChild(subnode)
file = codecs.open(outputfile,'wb',encoding='utf-8')

dom.writexml(file,'','\t','\n',encoding='utf-8')

#print(dom.toprettyxml())
file.close()
dom.unlink()