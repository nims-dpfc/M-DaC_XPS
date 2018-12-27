#-------------------------------------------------
# raw2primary_XRD.py
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

def registdf(key, channel, value, metadata, unitlist, template):
    key_unit = 0
    column = key

    tempflag = 1
    if not column in columns:
        tempflag = 0
    if tempflag == 1:
        org_column = column
#        if value != None:
        if 1:
            unitcolumn = template.find('meta[@key="{value}"][@unit]'.format(value=key))
            transition = 0
            if unitcolumn != None:
                if key == "Detector_Pixel_Size":
                    value_unit = unitcolumn.get("unit")
                elif key == "K_alpha_1_Wavelength":
                    value_unit = rawdata.find('meta[@key="HW_XG_WAVE_LENGTH_UNIT"]').text
                elif key == "K_alpha_2_Wavelength":
                    value_unit = rawdata.find('meta[@key="HW_XG_WAVE_LENGTH_UNIT"]').text
                elif key == "K_beta_Wavelength":
                    value_unit = rawdata.find('meta[@key="HW_XG_WAVE_LENGTH_UNIT"]').text
                elif key == "X-ray_Tube_Current":
                    value_unit = rawdata.find('meta[@key="HW_XG_CURRENT_UNIT"]').text
                elif key == "X-ray_Tube_Voltage":
                    value_unit = rawdata.find('meta[@key="HW_XG_VOLTAGE_UNIT"]').text
                elif key == "Scan_Speed":
                    value_unit = rawdata.find('meta[@key="MEAS_SCAN_SPEED_UNIT"]').text
                elif key == "Scan_Starting_Position":
                    value_unit = rawdata.find('meta[@key="MEAS_SCAN_UNIT_X"]').text
                elif key == "Scan_Step_Size":
                    value_unit = rawdata.find('meta[@key="MEAS_SCAN_UNIT_X"]').text
                elif key == "Scan_Ending_Position":
                    value_unit = rawdata.find('meta[@key="MEAS_SCAN_UNIT_X"]').text
            else:
                value_unit=""
                if key == "Year":
                    dt = parse(value)
                    value = dt.year
                elif key == "Month":
                    dt = parse(value)
                    value = "{0:02d}".format(dt.month)
                elif key == "Day":
                    dt = parse(value)
                    value = "{0:02d}".format(dt.day)
                elif key == "Wavelength_Type":
                    wavetype = value
                    if wavetype.find('a'):
                        wavetype = wavetype.replace('a', '_alpha')
                    if wavetype.find('b'):
                        wavetype = wavetype.replace('b', '_beta')
                    value = wavetype
                elif key == "Scan_Axis":
                    xlabelname = value
                    theta_list = ['TwoThetaTheta', '2θ/θ']
                    if xlabelname in theta_list:
                        xlabelname = '2Theta-Theta'
                    value = xlabelname
            if value == None:
                value =""

            subnode = dom.createElement('meta')
            subnode.appendChild(dom.createTextNode(str(value)))
            subnode_attr = dom.createAttribute('key')
            subnode_attr.value = column
            subnode.setAttributeNode(subnode_attr)
            metadata.appendChild(subnode)

            if value_unit != None and len(value_unit) > 0:
                subnode_attr = dom.createAttribute('unit')
                subnode_attr.value = value_unit
                subnode.setAttributeNode(subnode_attr)
                metadata.appendChild(subnode)
                unitlist.append(key)
                
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

            if transition == 1:
                subnode = dom.createElement('meta')
                subnode.appendChild(dom.createTextNode(str(value2)))
                subnode_attr = dom.createAttribute('key')
                subnode_attr.value = "Transitions"
                subnode.setAttributeNode(subnode_attr)
                metadata.appendChild(subnode)

                subnode_attr = dom.createAttribute('type')
                typename = template.find('meta[@key="Transitions"]')
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

                transition = 0

        return metadata

def regist(column, key, rawdata, metadata, channel, value, unitlist, template):
    if column in rawcolumns:
        registdf(key, channel, value, metadata, unitlist, template)
    return metadata


def conv(column, temp_name, rawdata, metadata, channel, unitlist, template):
    if channel == 0:
        metadata = regist(column, temp_name, rawdata, metadata, 0, rawdata.find('meta[@key="{value}"]'.format(value=column)).text, unitlist, template)
    else:
        for node in rawdata.findall('meta[@key="{value}"]'.format(value=column)):
            columnnum = node.attrib.get('column')
            metadata = regist(column, temp_name, rawdata, metadata, columnnum, node.text, unitlist, template)
    return(metadata)

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
rawdata = ET.parse(readfile)
rawcolumns=[]
rawmetas = rawdata.findall('meta')
for meta in rawmetas:
    rawcolumns.append(meta.attrib["key"])
rawcolumns = list(set(rawcolumns))
#print(rawcolumns)
template = ET.parse(templatefile)
columns=[]
metas = template.findall('meta')
for meta in metas:
    columns.append(meta.attrib["key"])
dom = xml.dom.minidom.Document()
metadata = dom.createElement('metadata')
dom.appendChild(metadata)
count = 0;

metalist = {"Year":"MEAS_SCAN_START_TIME",
            "Month":"MEAS_SCAN_START_TIME",
            "Day":"MEAS_SCAN_START_TIME",
            "Operator_identifier":"FILE_OPERATOR",
            "Comment":"FILE_COMMENT",
            "Memo":"FILE_MEMO",
            "Operator":"FILE_OPERATOR",
            "Specimen":"FILE_SAMPLE",
            "Detector_Pixel_Size":"HW_COUNTER_PIXEL_SIZE",
            "Selected_Detector_Name":"HW_COUNTER_SELECT_NAME",
            "X-ray_Target_Material":"HW_XG_TARGET_NAME",
            "K_alpha_1_Wavelength":"HW_XG_WAVE_LENGTH_ALPHA1",
            "K_alpha_2_Wavelength":"HW_XG_WAVE_LENGTH_ALPHA2",
            "K_beta_Wavelength":"HW_XG_WAVE_LENGTH_BETA",
            "Optics_Attribute":"MEAS_COND_OPT_ATTR",
            "X-ray_Tube_Current":"MEAS_COND_XG_CURRENT",
            "X-ray_Tube_Voltage":"MEAS_COND_XG_VOLTAGE",
            "Wavelength_Type":"MEAS_COND_XG_WAVE_TYPE",
            "Data_Point_Number":"MEAS_DATA_COUNT",
            "Scan_Axis":"MEAS_SCAN_AXIS_X",
            "Scan_Ending_Date_Time":"MEAS_SCAN_END_TIME",
            "Scan_Mode":"MEAS_SCAN_MODE",
            "Scan_Speed":"MEAS_SCAN_SPEED",
            "Scan_Starting_Position":"MEAS_SCAN_START",
            "Scan_Starting_Date_Time":"MEAS_SCAN_START_TIME",
            "Scan_Step_Size":"MEAS_SCAN_STEP",
            "Scan_Ending_Position":"MEAS_SCAN_STOP",
            "Scan_Axis_Unit":"MEAS_SCAN_UNIT_X",
            "Intensity_Unit":"MEAS_SCAN_UNIT_Y"}

columns_unique = list(dict.fromkeys(columns))
unitlist=[]
maxcolumn = 0
for k in columns_unique:
    if k in metalist:
        v = metalist[k]
        tempcolumn = len(rawdata.findall('meta[@key="{value}"]'.format(value=v)))-1
        if maxcolumn < tempcolumn + 1:
            maxcolumn = tempcolumn + 1
        metadata = conv(v, k, rawdata, metadata, len(rawdata.findall('meta[@key="{value}"]'.format(value=v)))-1, unitlist, template)

subnode = dom.createElement('column_num')
subnode.appendChild(dom.createTextNode(str(maxcolumn)))
metadata.appendChild(subnode)
column_name = template.find('column_name').text
subnode = dom.createElement('column_name')
subnode.appendChild(dom.createTextNode(column_name))
metadata.appendChild(subnode)
#print(dom.toprettyxml())
file = codecs.open(outputfile,'wb',encoding='utf-8')
dom.writexml(file,'','\t','\n',encoding='utf-8')
file.close()
dom.unlink()