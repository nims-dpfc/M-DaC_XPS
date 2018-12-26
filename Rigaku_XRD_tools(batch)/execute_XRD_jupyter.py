#-------------------------------------------------
# execute_XRD_jupyter.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
#-------------------------------------------------
# coding: utf-8

import argparse
import os
import shutil
import subprocess
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from dateutil.parser import parse
import xml.dom.minidom
import re
import xml.etree.ElementTree as ET
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import codecs
import glob

init_notebook_mode(connected=True)

def getKey(key, row):
    if row[0] == key:
        return row[1]
    else:
        return 0

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
parser.add_argument("--scale", nargs=2, type=float)
parser.add_argument("--unit", nargs=2)
parser.add_argument("--scalename", nargs=2)
parser.add_argument("--xrange", choices=['reverse'])
parser.add_argument("--yrange", choices=['reverse'])
options = parser.parse_args()
readfile = options.file_path
scale_option = options.scale
unit_option = options.unit
scalename_option = options.scalename
xrange_option = options.xrange
yrange_option = options.yrange

basename = os.path.basename(readfile)
dirname = os.path.dirname(readfile)
name, ext = os.path.splitext(basename)
org_name = name
axis = []

sourcedir = dirname
resultdir = "../"
tooldir = "./"

if os.path.isdir("temp"):
    shutil.rmtree("./temp")
os.mkdir("temp")
shutil.copy2(readfile, "temp/" + basename)
os.chdir("temp")
subprocess.run(["python", "../" + tooldir + "ras2csv.py", "--encoding", "sjis", basename])

#os.mkdir(resultdir + name)
#shutil.copy2(readfile, resultdir + name+"/.")
#subprocess.run(["python", tooldir + "ras2csv.py", "--encoding", "sjis", resultdir + name+"/"+basename])

readfile_csv = name+".csv"
with open(readfile_csv, 'r') as f:
    reader = csv.reader(f)
    line = 1
    if xrange_option == 'reverse':
        xrevFlag = True
    else:
        xrevFlag = False
    if yrange_option == 'reverse':
        yrevFlag = True
    else:
        yrevFlag = False
    for row in reader:
        if len(row) != 0:
            line += 1
            key = getKey('#title', row)
            if (key != 0):
                title = key
            key = getKey('#dimension', row)
            if (key != 0):
                axis = row[:]
                axis.pop(0)
                dimension = len(axis)
            key = getKey('#dim_axis', row)
            if (key != 0):
                dim_option = row[:]
                dim_option.pop(0)
            if len(axis) > 0:
                key = getKey('#'+axis[0], row)
                if key != 0:
                    xaxis = row[1]
                    xunit = ''
                    if len(row) > 2:
                        xunit = "(" + row[2] + ")"
                    if isinstance(unit_option, list):
                        xunit = "(" + unit_option[0] + ")"
                    if isinstance(scalename_option, list):
                        xaxis = scalename_option[0]
                    xaxis = xaxis +' '+ xunit
                    if len(row) > 3:
                        if row[3] == 'reverse':
                            xrevFlag = True
                key = getKey('#'+axis[1], row)
                if key != 0:
                    yaxis = row[1]
                    yunit = ''
                    if len(row) > 2:
                        yunit = "(" + row[2] + ")"
                    if isinstance(unit_option, list):
                        yunit = "(" + unit_option[1] + ")"
                    if isinstance(scalename_option, list):
                        yaxis = scalename_option[1]
                    yaxis = yaxis +' '+ yunit
                    if len(row) > 3:
                        if row[3] == 'reverse':
                            yrevFlag = True
            key = getKey('#legend', row)
            if (key != 0):
                row.pop(0)
                legends = row[:]
        else:
            break

df = pd.read_csv(readfile_csv, skiprows=line, header=None)
num_columns = len(df.columns)
if (len(legends) * len(axis) == num_columns):
    num = 0
    column = [];
    for col in legends:
        for i in range(len(axis)-1):
            column.append(col + '_' + str(i))
        column.append(col)
        num += len(axis)

df.columns=column
plt.rcParams['font.size'] = 12
fig, ax = plt.subplots()
formatter = ScalarFormatter(useMathText=True)
ax.yaxis.set_major_formatter(formatter)
if xrevFlag:
    plt.gca().invert_xaxis()
if yrevFlag:
    plt.gca().invert_yaxis()
plt.xlabel(xaxis)
plt.ylabel(yaxis)
plt.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
plt.grid(True)
plt.subplots_adjust(left=0.155, bottom=0.155, right=0.95, top=0.9, wspace=None, hspace=None)

num = 1
for col in df.columns:
    if num % dimension != 0:
        if isinstance(scale_option, list):
            x=df[col] * scale_option[0]
        else:
            x=df[col]
    else:
        if isinstance(scale_option, list):
            y=df[col] * scale_option[1]
        else:
            y=df[col]
        plt.plot(x,y,lw=1)
    num += 1
length = 35
if len(title) > length:
    string = title[:length] + '...'
else:
    string = title
    
plt.title(string)

plt.rcParams['font.family'] ='sans-serif'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0

plt.rcParams['axes.linewidth'] = 1.0

plt.legend()
writefile = name + '.png'
plt.savefig(writefile)
#plt.show()
plt.close()

if len(legends) > 1:
    num = 1
    for col in df.columns:
#        plt.figure()
        if num % dimension != 0:
            x=df[col]
        else:
            y=df[col]
            plt.rcParams['font.size'] = 12
            fig, ax = plt.subplots()
            formatter = ScalarFormatter(useMathText=True)
            ax.yaxis.set_major_formatter(formatter)
            if xrevFlag:
                plt.gca().invert_xaxis()
            if yrevFlag:
                plt.gca().invert_yaxis()
            plt.xlabel(xaxis)
            plt.ylabel(yaxis)
            plt.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
            plt.grid(True)
            plt.subplots_adjust(left=0.155, bottom=0.155, right=0.95, top=0.9, wspace=None, hspace=None)
            plt.plot(x,y,lw=1,label=col)
            plt.title(title + '_' + col)
            plt.rcParams['font.family'] ='sans-serif'
            plt.rcParams['xtick.direction'] = 'in'
            plt.rcParams['ytick.direction'] = 'in'
            plt.rcParams['xtick.major.width'] = 1.0
            plt.rcParams['ytick.major.width'] = 1.0
            plt.rcParams['axes.linewidth'] = 1.0
            plt.legend()
            writefile = name + '_' + col + '.png'
            plt.savefig(writefile)
#            plt.show()
            plt.close()
        num += 1

num = 1
data = []
for col in df.columns:
    if num % dimension != 0:
        if isinstance(scale_option, list):
            x=df[col] * scale_option[0]
        else:
            x=df[col]
    else:
        if isinstance(scale_option, list):
            y=df[col] * scale_option[1]
        else:
            y=df[col]
        trace = dict(
            name = col,
            x = x, y = y,
            type = "lines",
            mode = 'lines')
        data.append( trace )
    num += 1
length = 35

x_axis = 'false'
y_axis = 'false'
if xrevFlag:
    x_axis = 'reversed'
if yrevFlag:
    y_axis = 'reversed'
    
layout = dict(
    width=800,
    height=700,
    autosize=False,
    title=title,
    xaxis=dict(title=xaxis, autorange=x_axis),
    yaxis=dict(title=yaxis, autorange=y_axis),
    showlegend=True
)


fig = dict(data=data, layout=layout)
iplot(fig, filename=title, validate=False, show_link=False, config={"displaylogo":False, "modeBarButtonsToRemove":["sendDataToCloud"]})
#iplot(fig, filename=title, validate=False)

#subprocess.run(["python", "../Rigaku_XRD_tools/csv2graph_jupyter.py", "../"+name+"/"+name+".csv"])
#subprocess.check_call(["python", "../Rigaku_XRD_tools/ras2raw_XRD.py", "../"+name+"/"+readfile, "--encoding", "sjis", "../Rigaku_XRD_tools/xrd_raw_template.xml", "../"+name+"/raw.xml"])
subprocess.check_call(["python", "../" + tooldir + "ras2raw_XRD.py", basename, "--encoding", "sjis", "../" + tooldir + "xrd_raw_template.xml", "raw.xml"])

readfile_raw = "raw.xml"
templatefile = "../" + tooldir + "xrd_primary_template.xml"
outputfile = "primary.xml"
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
channel = 0
rawdata = ET.parse(readfile_raw)
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
print(dom.toprettyxml())
file = codecs.open(outputfile,'wb',encoding='utf-8')
dom.writexml(file,'','\t','\n',encoding='utf-8')
file.close()
dom.unlink()
os.remove(basename)
os.chdir("../")
if os.path.isdir(resultdir + name):
    shutil.rmtree(resultdir + name)
os.mkdir(resultdir + name)
for file in glob.glob(r'temp/*'):
    shutil.move(file, resultdir + name)
shutil.rmtree("temp")
