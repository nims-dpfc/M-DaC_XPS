#-------------------------------------------------
# raw2primary_XPS_depth.py
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
        if value != None:
            arrayvalue = value.split()
            unitcolumn = template.find('meta[@key="{value}"][@unit]'.format(value=key))
            transition = 0
            if unitcolumn != None:
                if len(arrayvalue) > 1:
                    value_unit = arrayvalue[1]
                value = arrayvalue[0] 
                if key == "Analyser_axis_take_off_polar_angle":
                    value_unit = unitcolumn.get("unit")
                elif key == "Analyser_Pass_energy":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[11]
                elif key == "Analysis_width_x":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[0]
                elif key == "Analysis_width_y":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[1]
                elif key == "Ion_gun_Voltage":
                    value_unit = unitcolumn.get("unit")
                    floatvolt = int(float(arrayvalue[0]))
                    temp = rawdata.find('meta[@key="SputterEnergy"]').text
                    temp = temp.split()
                    if temp[1] == "kV":
                        sputterEnergy = int(float(temp[0]) * 1000)
                    else:
                        sputterEnergy = int(float(temp[0]))
                    value = floatvolt + sputterEnergy
                elif key == "Abscissa_start":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[6]
                elif key == "Abscissa_end":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[7]
                elif key == "Abscissa_increment":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[5]
                elif key == "Collection_time":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[10]
                elif key == "Analyser_work_function":
                    value_unit = arrayvalue[1]
                    value = arrayvalue[0]
                elif key == "Sputtering_interval_time":
                    value = arrayvalue[7]
                    value_unit = unitcolumn.get("unit")
                elif key == "Sputtering_to_measurement_time":
                    value = arrayvalue[0]
                    value_unit = unitcolumn.get("unit")
                elif key == "Sputtering_Ion_Energy":
                    value_unit = arrayvalue[1]
                    value = arrayvalue[0]
                elif key == "Sputtering_Raster_Area":
                    value_unit = arrayvalue[2]
                    value = arrayvalue[0] + 'x' + arrayvalue[1]

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
                elif key == "Analysis_source_strength":
                    arrayvalue = rawdata.find('meta[@key="XrayPower"]').text
                    arrayvalue = arrayvalue.split()
                    itemarray = ""
                    for item in arrayvalue:
                        itemarray += item
                    if value == "yes":
                        value = itemarray + "_HP"
                    else:
                        value = itemarray
                elif key == "Analysis_source_beam_diameter":
                    value_unit = arrayvalue[1]
                    value = arrayvalue[0]
                elif key == "Analysis_region":
                    value = arrayvalue[2]
                elif key == "Species_label":
                    transition = 1
                    peak = re.findall(r'(\d+|\D+)', arrayvalue[2])
                    if peak[0] == "Su":
                        value = "Survey"
                        value2= ""
                    elif peak[0] == "Va":
                        value = "Valence"
                        value2= ""
                    elif "_" in peak[0]:
                        peak2 = peak[0].split("_", 1)
                        value = peak2[0]
                        value2 = peak2[1]
                    else:
                        value = peak[0]
                        value2 = ""
                        for i, x in enumerate(peak):
                            if 0 < i:
                                value2 = value2 + x

                elif key == "Measurement_Acquisition_Number":
                    value = 1
                elif key == "Peak_Sweep_Number":
                    value = int(arrayvalue[2])
                elif key == "Software_Preset_Sputtering_Layer_Name":
                    value = arrayvalue[1]
                elif key == "Total_Cycle_Number":
                    value = "***"
                elif key == "Cycle_Control":
                    value = "***"
                elif key == "Number_of_scans":
                    if rawdata.find('meta[@key="SurvNumCycles"]') != None:
                        SurvNumCycles = rawdata.find('meta[@key="SurvNumCycles"]').text
                    else:
                        SurvNumCycles = 1
                    value = int(SurvNumCycles) * int(arrayvalue[2])
                elif key == "Sputtering_cycle":
                    value = arrayvalue[8]
                    
            subnode = dom.createElement('meta')
            subnode.appendChild(dom.createTextNode(str(value)))
            subnode_attr = dom.createAttribute('key')
            subnode_attr.value = column
            subnode.setAttributeNode(subnode_attr)
            metadata.appendChild(subnode)

            if len(value_unit) > 0:
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
rawdata = ET.parse(readfile)
rawcolumns=[]
rawmetas = rawdata.findall('meta')
for meta in rawmetas:
    rawcolumns.append(meta.attrib["key"])
rawcolumns = list(set(rawcolumns))
template = ET.parse(templatefile)
columns=[]
metas = template.findall('meta')
for meta in metas:
    columns.append(meta.attrib["key"])
dom = xml.dom.minidom.Document()
metadata = dom.createElement('metadata')
dom.appendChild(metadata)
count = 0;

metalist = {"Technique":"Technique",
            "Year":"AcqFileDate",
            "Month":"AcqFileDate",
            "Day":"AcqFileDate",
            "Instrument_model_identifier":"InstrumentModel",
            "Operator_identifier":"Operator",
            "Institution_idendfier":"Institution",
            "Experiment_Identifier":"ExperimentID",
            "Experiment_mode":"FileType",
            "Analyser_mode":"AnalyserMode",
            "Analyser_work_function":"AnalyserWorkFcn",
            "Sputtering_to_measurement_time":"ProfSputterDelay",
            "Sputtering_interval_time":"DepthCalDef",
            "Sputtering_cycle":"DepthCalDef",
            "Species_label":"SpectralRegDef",
            "Abscissa_increment":"SpectralRegDef",
            "Abscissa_start":"SpectralRegDef",
            "Abscissa_end":"SpectralRegDef",
            "Collection_time":"SpectralRegDef",
            "Measurement_Acquisition_Number":"Technique",
            "Peak_Sweep_Number":"SpectralRegDef2",
            "Analyser_Pass_energy":"SpectralRegDef",
            "Number_of_scans":"SpectralRegDef2",
            "Analyser_axis_take_off_polar_angle":"SourceAnalyserAngle",
            "Analyser_acceptance_solid_angle":"AnalyserSolidAngle",
            "Analysis_source_beam_diameter":"XrayBeamDiameter",
            "Analysis_source_strength":"XRayHighPower",
            "Comment":"SpatialAreaDesc",
            "Sputtering_Ion_Energy":"SputterEnergy",
            "Sputtering_Raster_Area":"SputterRaster",
            "Specimen_Stage_Rotation_Setting_During_Sputtering":"SampleRotation",
            "Depth_Profiling_Preset_Layer_Number":"NoDepthReg",
            "Total_Cycle_Number":"DepthCalDef",
            "Cycle_Control":"DepthCalDef",
            "Software_Preset_Sputtering_Layer_Name":"DepthCalDef",
            "Analysis_width_x":"ImageSizeXY",
            "Analysis_width_y":"ImageSizeXY",
            "Analysis_region":"ImageSizeXY"}

columns_unique = list(dict.fromkeys(columns))
unitlist=[]
maxcolumn = 0
depthcolumn = rawdata.find('meta[@key="NoDepthReg"]').text
spectralcolumn = rawdata.find('meta[@key="NoSpectralReg"]').text
for k in columns_unique:
    if k in metalist:
        v = metalist[k]
        column_num = len(rawdata.findall('meta[@key="{value}"]'.format(value=v)))
        if maxcolumn < column_num:
            maxcolumn = column_num
        metadata = conv(v, k, rawdata, metadata, column_num - 1, unitlist, template)

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
