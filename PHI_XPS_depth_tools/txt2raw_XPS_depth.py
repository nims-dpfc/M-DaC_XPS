#-------------------------------------------------
# txt2raw_XPS_depth.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
#-------------------------------------------------
# coding: utf-8

__package__ = "M-DaC_XPS/PHI_XPS_depth_tools"
__version__ = "1.0.0"

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
depth = 1
spectral = 1
maxcolumn = 1
with codecs.open(readfile, 'r', 'utf-8', 'ignore') as f:
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
            if key == "NoDepthReg":
                depth = int(value) - 1
            if key == "NoSpectralReg":
                spectral = int(value) - 1
            if key == "DepthCalDef":
                values = value.split()
                channel = int(values[0])
            if key == "SpectralRegDef":
                values = value.split()
                channel = int(values[0])
                temp = (depth + 1) * channel
                if maxcolumn < temp:
                    maxcolumn = temp
            if key == "NoSpectralReg":
                channel = 0
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
                subnode_attr.value = str(channel)
                subnode.setAttributeNode(subnode_attr)
                metadata.appendChild(subnode)

depth_count = 0
spectral_count = 0
metas = dom.getElementsByTagName("meta")
for element in metas:
    if element.getAttribute("key") == "DepthCalDef":
        original = element.attributes["column"].value
        new_depth = int(original) + (depth_count * spectral)
        element.attributes["column"].value = str(new_depth)
        for i in range(spectral):
            element2 = element.cloneNode(element)
            temp = new_depth + i + 1
            element2.attributes["column"].value = str(temp)
            metadata.appendChild(element2)
        depth_count = depth_count + 1

    if "SpectralRegDef" in element.getAttribute("key"):
        original = element.attributes["column"].value
        for i in range(depth):
            element2 = element.cloneNode(element)
            temp = int(original) + (i + 1) * depth
            element2.attributes["column"].value = str(temp)
            metadata.appendChild(element2)
        if element.getAttribute("key") == "SpectralRegDef2":
            spectral_count = spectral_count + 1

subnode = dom.createElement('column_num')
subnode.appendChild(dom.createTextNode(str(maxcolumn)))
metadata.appendChild(subnode)
column_name = template.find('column_name').text
subnode = dom.createElement('column_name')
subnode.appendChild(dom.createTextNode(column_name))
metadata.appendChild(subnode)
tool_package = __package__
subnode = dom.createElement('tool_package')
subnode.appendChild(dom.createTextNode(tool_package))
metadata.appendChild(subnode)
tool_filename = os.path.basename(__file__)
subnode = dom.createElement('tool_filename')
subnode.appendChild(dom.createTextNode(tool_filename))
metadata.appendChild(subnode)
tool_version = __version__
subnode = dom.createElement('tool_version')
subnode.appendChild(dom.createTextNode(tool_version))
metadata.appendChild(subnode)

template_package = template.getroot().attrib['package']
subnode = dom.createElement('template_package')
subnode.appendChild(dom.createTextNode(template_package))
metadata.appendChild(subnode)
template_filename = os.path.basename(templatefile)
subnode = dom.createElement('template_filename')
subnode.appendChild(dom.createTextNode(template_filename))
metadata.appendChild(subnode)
template_version = template.getroot().attrib['version']
subnode = dom.createElement('template_version')
subnode.appendChild(dom.createTextNode(template_version))
metadata.appendChild(subnode)
if print_option == True:
    print(dom.toprettyxml())
file = codecs.open(outputfile,'wb',encoding='utf-8')

dom.writexml(file,'','\t','\n',encoding='utf-8')

file.close()
dom.unlink()
