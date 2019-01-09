#-------------------------------------------------
# txt2raw_XPS_survey.py
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
import sys
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="input file")
parser.add_argument("template_file", help="template file")
parser.add_argument("out_file", help="output file")
parser.add_argument("--stdout", help="show meta information", action="store_true")
options = parser.parse_args()
readfile = options.file_path
templatefile = options.template_file
outputfile = options.out_file
print_option = options.stdout
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
with open(readfile, 'r', encoding="utf8") as f:
    for line in f:
        line = line.strip()
        comment = line[0:2]
        if line == '':
            break
        elif comment.find("//") != 0:
            lines = line.split(":")
            lines = [item.strip() for item in lines]
            key = lines[0]
            value = lines[1]
            if 2 < len(lines):
                for index,item in enumerate(lines):
                    if index > 1:
                        value = value + ':' + item
            if key == "NoSpectralReg" and 1 < int(value):
                wide = 0
            if wide == 0 and key == "SpectralRegDef":
                values = value.split()
                channel = values[0]
                if maxcolumn < int(channel):
                    maxcolumn = int(channel)
            if key == "NoSpatialArea":
                channel = 0
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
if print_option == True:
    print(dom.toprettyxml())
file = codecs.open(outputfile,'wb',encoding='utf-8')

dom.writexml(file,'','\t','\n',encoding='utf-8')

file.close()
dom.unlink()
