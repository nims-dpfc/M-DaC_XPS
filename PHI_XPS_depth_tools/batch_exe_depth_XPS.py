#-------------------------------------------------
# batch_exe_depth_XPS.py
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
import subprocess
import shutil
import glob
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import ScalarFormatter
import numpy as np
from scipy import integrate
from mpl_toolkits.mplot3d import Axes3D
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
from dateutil.parser import parse
import xml.dom.minidom
import re
import xml.etree.ElementTree as ET
import codecs
import unicodedata

def getKey(key, row):
    if row[0] == key:
        return row[1]
    else:
        return 0

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
                    items = rawdata.findall('meta[@key="DepthCalDef"]')
                    itemlist = []
                    cyclenum = 0
                    for item in items:
                        if item.text not in itemlist:
                            itemlist.append(item.text)
                            myitem = item.text
                            myitems = myitem.split()
                            cyclenum = cyclenum + int(myitems[8])
                    value = cyclenum
                elif key == "Cycle_Control":
                    items = rawdata.findall('meta[@key="DepthCalDef"]')
                    itemlist = []
                    cyclecontrol = ""
                    for item in items:
                        if item.text not in itemlist:
                            itemlist.append(item.text)
                            myitem = item.text
                            myitems = myitem.split()
                            cont_value = myitems[7] + "min " + myitems[8] + "cyc, "
                            cyclecontrol = cyclecontrol + cont_value
                    value = cyclecontrol[0:len(cyclecontrol)-2]
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
        if key == "Measurement_Acquisition_Number":
            value = template.find('meta[@key="Measurement_Acquisition_Number"]').text
        registdf(key, channel, value, metadata, unitlist, template)
    return metadata


def conv(column, temp_name, rawdata, metadata, channel, unitlist, template):
    if channel == 0:
        metadata = regist(column, temp_name, rawdata, metadata, 0, rawdata.find('meta[@key="{value}"]'.format(value=column)).text, unitlist, template)
    elif channel == -1 and temp_name == "Measurement_Acquisition_Number":
        metadata = regist(column, temp_name, rawdata, metadata, 0, 1, unitlist, template)
    else:
        for node in rawdata.findall('meta[@key="{value}"]'.format(value=column)):
            columnnum = node.attrib.get('column')
            metadata = regist(column, temp_name, rawdata, metadata, columnnum, node.text, unitlist, template)
    return(metadata)

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

def plotlygraph3D(xrevFlag, yrevFlag, zrevFlag, title, data, fig):
    x_axis = 'false'
    y_axis = 'false'
    z_axis = 'false'
    if xrevFlag:
        x_axis = 'reversed'
    if yrevFlag:
        y_axis = 'reversed'
    if zrevFlag:
        z_axis = 'reversed'

    layout = dict(
            width=800,
            height=700,
            autosize=False,
            title=title,
            scene = dict(
                    xaxis = dict(
                        title=df_head.loc['z','spectra'],
                        autorange=x_axis),
                    yaxis = dict(
                        title=df_head.loc['x','spectra'],
                        autorange=y_axis),
                    zaxis = dict(
                        title=df_head.loc['y','spectra'],
                        autorange=z_axis),
                    camera = dict(
                        up=dict(x=0, y=0, z=1),
                        center=dict(x=0, y=0, z=0),
                        eye=dict(x=2.5, y=0.1, z=0.1)
                    ),
            ),  
    )

    fig = dict(data=data, layout=layout)
    iplot(fig, show_link=False, filename=title, validate=False, config={"displaylogo":False, "modeBarButtonsToRemove":["sendDataToCloud"]})

def is_japanese(titlestring):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return(True)
    return(False)

fp = FontProperties(fname=r'C:\WINDOWS\Fonts\meiryo.ttc', size=14)

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
subprocess.run(["../"+tooldir + "MPExport.exe", "-ExportProfile", "-Filename:"+basename])
subprocess.run(["python", "../" + tooldir + "txt2csv_depth.py", name+".txt"])

#------- csv2graph_depth.py begin ---------
axis = []
headernum = []
xrange_option = ''
yrange_option = ''
zrange_option = ''
unit_option = ''
scalename_option = ''
lastline = 'empty'
legends = []
section = 0
block = 0
start = []
end = []
start_d = []
end_d = []
scatterTime = []
spectrablock = 0
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
    if zrange_option == 'reverse':
        zrevFlag = True
    else:
        zrevFlag = False
    df_head = pd.DataFrame(index=['title', 'dimension', 'x', 'y', 'z', 'legend','start', 'stop'], columns=['spectra', 'intensity'])
    for row in reader:
        if len(row) == 0:
            lastline2 = lastline
            lastline = 'empty'
            if section == 0 and spectrablock == 0:
                df_head.at['title','spectra'] = title
                df_head.at['dimension','spectra'] = dimension
                df_head.at['x','spectra'] = xaxis
                df_head.at['y','spectra'] = yaxis
                df_head.at['z','spectra'] = zaxis
                df_head.at['legend','spectra'] = legends
                df_head.at['xrevFlag','spectra'] = xrevFlag
                df_head.at['yrevFlag','spectra'] = yrevFlag
                df_head.at['zrevFlag','spectra'] = zrevFlag
                xrevFlag = False
                yrevFlag = False
                zrevFlag = False
            if section == 1 and spectrablock == 0:
                df_head.at['title','intensity'] = title
                df_head.at['dimension','intensity'] = dimension
                df_head.at['x','intensity'] = xaxis
                df_head.at['y','intensity'] = yaxis
                df_head.at['legend','intensity'] = legends
                df_head.at['xrevFlag','intensity'] = xrevFlag
                df_head.at['yrevFlag','intensity'] = yrevFlag
            if spectrablock == 1 and lastline2 != 'empty':
                end.append(line - 1)
                df_head.at['stop','spectra'] = end
            if spectrablock == 2:
                end_d.append(line - 1)
                df_head.at['stop','intensity'] = end_d
            if spectrablock == 1 and lastline2 == 'empty':
                    spectrablock = 2
                    section = -1
            section = section + 1
        else:
            lastline2 = lastline
            if row[0][0:1] == '#':
                lastline = 'comment'
            else:
                lastline = 'num'
            if lastline2 == 'empty' and lastline == 'num':
                if spectrablock == 0:
                    spectrablock = 1
                    section = 0
                if spectrablock == 1:
                    start.append(line + 1)
                    df_head.at['start','spectra'] = start
                    scatterTime = row
            if lastline2 == 'comment' and spectrablock == 2:
                start_d.append(line)
                df_head.at['start','intensity'] = start_d
            if lastline2 == 'empty' and spectrablock == 2 and lastline != 'comment':
                start_d.append(line)
                df_head.at['start','intensity'] = start_d
            if row[0][0:2] != '##':
                key = getKey('#title', row)
                if (key != 0):
                    title = key
                else:
                    key = getKey('#dimension', row)
                    if (key != 0):
                        axis = row[:]
                        axis.pop(0)
                        dimension = len(axis)
                    else:
                        if len(axis) > 0:
                            key = getKey('#'+axis[0], row)
                            key2 = getKey('#'+axis[1], row)
                            if len(axis) > 2:
                                key3 = getKey('#'+axis[2], row)
                            else:
                                key3 = 0
                            if key != 0:
                                xaxis = row[1]
                                xunit = ''
                                if len(row) > 2:
                                    xunit = "(" + row[2] + ")"
                                    xaxis = xaxis + " " + xunit
                                if len(row) > 3:
                                    if row[3] == 'reverse':
                                        xrevFlag = True
                            elif key2 != 0:
                                yaxis = row[1]
                                yunit = ''
                                if len(row) > 2:
                                    yunit = "(" + row[2] + ")"
                                yaxis = yaxis + " " + yunit
                                if len(row) > 3:
                                    if row[3] == 'reverse':
                                        yrevFlag = True
                            elif key3 != 0:
                                zaxis = row[1]
                                zunit = ''
                                if len(row) > 2:
                                    zunit = "(" + row[2] + ")"
                                zaxis = zaxis + " " + zunit
                                if len(row) > 3:
                                    if row[3] == 'reverse':
                                        zrevFlag = True
                            else:
                                key = getKey('#legend', row)
                                if (key != 0):
                                    row.pop(0)
                                    legends = row[:]
                                else:
                                    lastline = 'unknownKey'
        line += 1
end_d.append(line - 1)
df_head.at['stop','intensity'] = end_d
startline = df_head.loc['start','spectra']
endline = df_head.loc['stop','spectra']
offset = startline[0]
with codecs.open(readfile2, 'r', 'utf-8', 'ignore') as f:
    df = pd.read_csv(f, skiprows=offset-1, header=None)
maxColumn = len(df.columns)
title = df_head.loc['title','spectra']
length = 35
if len(title) > length:
    string = title[:length] + '...'
else:
    string = title
maxValue = 0
formatter = ScalarFormatter(useMathText=True)
xrev = df_head.loc['xrevFlag','spectra']
dfcum = []
titleList = df_head.loc['legend','spectra']
data_frame = pd.DataFrame(index=[])
index = 0
emptyoffset = 0
scatterTime.pop(0)
scatterTime = list(map(float, scatterTime))
data = []
for atom in titleList:
    s_col = startline[index] - offset - emptyoffset
    e_col = endline[index] - offset + 1 - emptyoffset
    emptyoffset = emptyoffset + 1
    df3 = df.iloc[s_col:e_col,0:maxColumn]
    df3 = df3.astype(float)
    minValue = df3[0].min()
    maxValue = df3[0].max()
    if index == 0:
        allmin = minValue
        allmax = maxValue
    else:
        if minValue < allmin:
            allmin = minValue
        if allmax < maxValue:
            allmax = maxValue
    writefile = name + '_' + atom + '.png'
    index += 1
    if xrev == True:
        ax = df3.plot(x=0, legend=False, title=string + '_' + atom, grid=True, xlim=[maxValue,minValue])
    else:
        ax = df3.plot(x=0, legend=False, title=string + '_' + atom, grid=True, xlim=[minValue, maxValue])
    if xrev == True:
        ax.invert_xaxis()
        plt.gca().invert_xaxis();
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel(df_head.loc['x','spectra'])
    ax.set_ylabel(df_head.loc['y','spectra'])
    ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    plt.savefig(writefile)

    fig = plt.figure()
    ax3 = fig.gca(projection='3d')
    writefile = name + '_' + atom + '_3d.png'
    x = df3[0].values
    timecount = -1
    min_temp = df3[1].min()
    max_temp = df3[1].max()
    lastindex = len(scatterTime)
    for time in scatterTime:
        lasttime = scatterTime[lastindex-1]
        y = df3[lastindex].values
        if df3[lastindex].min() < min_temp:
            min_temp = df3[lastindex].min()
        if  max_temp < df3[lastindex].max():
            max_temp = df3[lastindex].max()
        lastindex = lastindex - 1
        ax3.plot(x, y, zs=lasttime, zdir='y')
    if xrev:
        ax3.set_xlim(df3[0].max(), df3[0].min())
    else:
        ax3.set_xlim(df3[0].min(), df3[0].max())
    ax3.set_title(string + '_' + atom)
    ax3.set_ylim(min(scatterTime), max(scatterTime))
    ax3.set_zlim(min_temp, max_temp)
    ax3.zaxis.set_major_formatter(formatter)
    ax3.set_xlabel(df_head.loc['x','spectra'])
    ax3.set_zlabel(df_head.loc['y','spectra'])
    ax3.set_ylabel(df_head.loc['z','spectra'])
    ax3.ticklabel_format(style="sci",  axis="z",scilimits=(0,0))
    if xrev:
        ax3.invert_xaxis()
        plt.gca().invert_xaxis();
    fig = ax3.get_figure()
    fig.savefig(writefile)

index = 0
emptyoffset = 0
for atom in titleList:
    s_col = startline[index] - offset - emptyoffset
    e_col = endline[index] - offset + 1 - emptyoffset
    emptyoffset = emptyoffset + 1
    df3 = df.iloc[s_col:e_col,0:maxColumn]
    df3 = df3.astype(float)
    maxtemp = ((int)(max(df3[0])/100) + 1) * 100
    if maxValue < maxtemp:
        maxValue = maxtemp
    if index == 0:
        if xrev == True:
            ax1 = df3.plot(x=0, legend=False, title=False, grid=True, xlim=[allmax,allmin])
        else:
            ax1 = df3.plot(x=0, legend=False, title=False, grid=True, xlim=[allmin, allmax])
    else:
        if xrev == True:
            ax1 = df3.plot(x=0, legend=False, title=False, grid=True, ax=ax1, xlim=[allmax,allmin])
        else:
            ax1 = df3.plot(x=0, legend=False, title=False, grid=True, ax=ax1, xlim=[allmin, allmax])
    index += 1
if xrev:
    ax1.invert_xaxis()
    plt.gca().invert_xaxis();
plt.title(string + '_spectraAll')
ax1.yaxis.set_major_formatter(formatter)
ax1.set_xlabel(df_head.loc['x','spectra'])
ax1.set_ylabel(df_head.loc['y','spectra'])
ax1.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
ax1.axis('tight')
writefile = name + '_speall' + '.png'
plt.savefig(writefile)

#for 3D
index = 0
emptyoffset = 0
fig = plt.figure()
ax3all = fig.gca(projection='3d')
writefile = name + '_speall_3d.png'
data2 = []
for atom in titleList:
    s_col = startline[index] - offset - emptyoffset
    e_col = endline[index] - offset + 1 - emptyoffset
    emptyoffset = emptyoffset + 1
    df3 = df.iloc[s_col:e_col,0:maxColumn]
    df3 = df3.astype(float)
    x = df3[0].values
    x_d = df3[0]
    timecount = -1
    lastindex = len(scatterTime)
    for time in scatterTime:
        lasttime = scatterTime[lastindex-1]
        y = df3[lastindex].values
        y_d = df3[lastindex]
        if df3[lastindex].min() < min_temp:
            min_temp = df3[lastindex].min()
        if  max_temp < df3[lastindex].max():
            max_temp = df3[lastindex].max()
        lastindex = lastindex - 1
        ax3all.plot(x, y, zs=lasttime, zdir='y')
        lst = [lasttime] * len(x)
        z_d = pd.Series(lst)
        trace = dict(
            name = atom,
            x = z_d, y = x_d, z = y_d,
            type = "scatter3d",    
            mode = 'lines')
        data2.append( trace )
    index += 1
if xrev:
    ax3all.invert_xaxis()
    ax3all.set_xlim(allmax,allmin)
else:
    ax3all.set_xlim(allmin,allmax)
plt.title(string + '_spectraAll')
ax3all.set_ylim(min(scatterTime), max(scatterTime))
ax3all.set_zlim(min_temp, max_temp)
ax3all.zaxis.set_major_formatter(formatter)
ax3all.set_xlabel(df_head.loc['x','spectra'])
ax3all.set_zlabel(df_head.loc['y','spectra'])
ax3all.set_ylabel(df_head.loc['z','spectra'])
ax3all.ticklabel_format(style="sci",  axis="z",scilimits=(0,0))
plt.savefig(writefile)

#plt.figure()
index = 0
titleList = df_head.loc['legend','intensity']
index = 0
startline = df_head.loc['start','intensity']
endline = df_head.loc['stop','intensity']
s_col = startline[index] - offset + 1 - emptyoffset - 2
e_col = endline[index] - offset + 1 - emptyoffset - 2 + 1
df3 = df.iloc[s_col:e_col,0:len(titleList)+1]
titleList.insert(0, 'Sputter Time')
df3.columns = titleList
df3 = df3.astype(float)
ax1 = df3.plot(x=0, legend=False, title=string, grid=True)
ax1.set_xlabel(df_head.loc['x','intensity'])
ax1.set_ylabel(df_head.loc['y','intensity'])
ax1.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
ax1.yaxis.set_major_formatter(formatter)
writefile = name + '.png'
plt.legend()
#df3.plot()
plt.savefig(writefile)
num = 1
data = []
if jupytermode == True:
    for col in df3.columns:
        trace = dict(
            name = col,
            x = df3['Sputter Time'], y = df3[col],
            type = "lines",
            mode = 'lines')
        if num > 1:
            data.append( trace )
        num += 1
plt.close()
if jupytermode == True:
    plotlygraph("", "", title, data, fig)
if jupytermode == True:
    if xrev:
        plotlygraph3D(True, True, "", title, data2, fig)
    else:
        plotlygraph3D(True, False, "", title, data2, fig)

#------- csv2graph_depth.py end ---------

subprocess.run(["python", "../" + tooldir + "txt2raw_XPS_depth.py", name+".txt", "../" + tooldir + "xps_raw_depth_template.xml", "raw.xml"])

#------- raw2primary_XPS_depth.py begin ---------
readfile3 = "raw.xml"
templatefile = "../" + tooldir + "xps_primary_depth_template.xml"
outputfile = "primary.xml"
channel = 0
rawdata = ET.parse(readfile3)
rawcolumns=[]
rawmetas = rawdata.findall('meta')
for meta in rawmetas:
    rawcolumns.append(meta.attrib["key"])
rawcolumns.append("SurvNumCycles")
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
            "Measurement_Acquisition_Number":"SurvNumCycles",
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
        if k == "Total_Cycle_Number" or k == "Cycle_Control":
            column_num = 1
        else:
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
if jupytermode == True:
    print(dom.toprettyxml())
file = codecs.open(outputfile,'wb',encoding='utf-8')
dom.writexml(file,'','\t','\n',encoding='utf-8')
file.close()
dom.unlink()

#------- raw2primary_XPS_depth.py end ---------

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
