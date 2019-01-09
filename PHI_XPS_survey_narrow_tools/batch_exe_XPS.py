#-------------------------------------------------
# batch_exe_XPS.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
#-------------------------------------------------
# coding: utf-8

import argparse
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import shutil
import subprocess
import glob
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
from dateutil.parser import parse
import xml.dom.minidom
import re
import xml.etree.ElementTree as ET
import codecs

def getKey(key, row):
    if row[0] == key:
        return row[1]
    else:
        return 0

def plotlygraph(xrevFlag, yrevFlag, title, data, fig):
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
    iplot(fig, show_link=False, filename=title, validate=False, config={"displaylogo":False, "modeBarButtonsToRemove":["sendDataToCloud"]})

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
                elif key == "Analyser_work_function":
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
                                
                elif key == "Number_of_scans":
                    SurvNumCycles = rawdata.find('meta[@key="SurvNumCycles"]').text
                    if SurvNumCycles == None:
                        SurvNumCycles = 1
                    value = int(SurvNumCycles) * int(arrayvalue[2])
                    
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
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
parser.add_argument("--jupytermode", help="for jupyter mode", action="store_true")
options = parser.parse_args()
readfile = options.file_path
jupytermode = options.jupytermode
basename = os.path.basename(readfile)
dirname = os.path.dirname(readfile)
name, ext = os.path.splitext(basename)
currentdir = os.getcwd()

if jupytermode == True:
    init_notebook_mode(connected=True)

sourcedir = dirname
resultdir = "../result/"
tooldir = "./"

if os.path.isdir("temp"):
    shutil.rmtree("./temp")
os.mkdir("temp")
shutil.copy2(readfile, "temp/" + basename)
os.chdir("temp")
subprocess.run(["../"+tooldir + "MPExport.exe", "-Filename:"+basename, "-TSV"])
subprocess.run(["python", "../" + tooldir + "txt2csv.py", name+".txt"])

#------- csv2graph.py begin ---------
scale_option = ""
unit_option = ""
scalename_option = ""
xrange_option = ""
yrange_option = ""
axis = []
readfile2 = name + ".csv"
with open(readfile2, 'r') as f:
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
                    xaxis = xaxis + " " + xunit
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
                    yaxis = yaxis + " " + yunit
                    if len(row) > 3:
                        if row[3] == 'reverse':
                            yrevFlag = True
            key = getKey('#legend', row)
            if (key != 0):
                row.pop(0)
                legends = row[:]
        else:
            break
df = pd.read_csv(readfile2, skiprows=line, header=None)
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
        plt.plot(x,y,lw=1)
        if jupytermode == True:
            trace = dict(
                name = col,
                x = x, y = y,
                type = "lines",
                mode = 'lines')
            data.append( trace )
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
plt.close()

if len(legends) > 1:
    num = 1
    for col in df.columns:
        plt.figure()
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
            plt.close()
        num += 1

if jupytermode == True:
    plotlygraph(xrevFlag, yrevFlag, title, data, fig)

#------- csv2graph.py end ---------

subprocess.run(["python", "../" + tooldir + "txt2raw_XPS_survey.py", name+".txt", "../" + tooldir + "xps_raw_template.xml", "raw.xml"])

#------- raw2primary_XPS_survey.py begin ---------

readfile3 = "raw.xml"
templatefile = "../" + tooldir + "xps_primary_template.xml"
outputfile = "primary.xml"
rawdata = ET.parse(readfile3)
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
            "Flood_gun_Voltage":"NeutralizerEnergy",
            "Flood_gun_Emission_current":"NeutralizerCurrent",
            "Sputtering_interval_time":"ProfSputterDelay",
            "Sputtering_cycle":"ProfSputterDelay",
            "Species_label":"SpectralRegDef",
            "Abscissa_increment":"SpectralRegDef",
            "Abscissa_start":"SpectralRegDef",
            "Abscissa_end":"SpectralRegDef",
            "Collection_time":"SpectralRegDef",
            "Analyser_Pass_energy":"SpectralRegDef",
            "Number_of_scans":"SpectralRegDef2",
            "Ion_gun_Voltage":"FloatVolt",
            "Analyser_axis_take_off_polar_angle":"SourceAnalyserAngle",
            "Analyser_acceptance_solid_angle":"AnalyserSolidAngle",
            "Analysis_source_beam_diameter":"XrayBeamDiameter",
            "Analysis_source_strength":"XRayHighPower",
            "Comment":"SpatialAreaDesc",
            "Analysis_width_x":"ImageSizeXY",
            "Analysis_width_y":"ImageSizeXY",
            "Analysis_region":"ImageSizeXY"}

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
if jupytermode == True:
    print(dom.toprettyxml())
file = codecs.open(outputfile,'wb',encoding='utf-8')
dom.writexml(file,'','\t','\n',encoding='utf-8')
file.close()
dom.unlink()

#------- raw2primary_XPS_survey.py end ---------

os.remove(basename)
os.chdir("../")
if not(os.path.isdir(resultdir)):
    os.mkdir(resultdir)
os.chdir(resultdir)
if os.path.isdir(name):
    shutil.rmtree(name)
os.mkdir(name)
os.chdir(currentdir)
for file in glob.glob(r'temp/*'):
    shutil.move(file, resultdir + name)
shutil.rmtree("temp")
