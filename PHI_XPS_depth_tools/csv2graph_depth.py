#-------------------------------------------------
# csv2graph_depth.py
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
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import numpy as np
from scipy import integrate
from mpl_toolkits.mplot3d import Axes3D   
import codecs
import unicodedata
import matplotlib.ticker as ticker

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

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
parser.add_argument("--jupytermode", help="for jupyter mode", action="store_true")
options = parser.parse_args()
readfile = options.file_path
jupytermode = options.jupytermode
name, ext = os.path.splitext(readfile)
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

if jupytermode == True:
    init_notebook_mode(connected=True)
    
with open(readfile, 'r') as f:
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
with codecs.open(readfile, 'r', 'utf-8', 'ignore') as f:
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
