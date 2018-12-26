#-------------------------------------------------
# ras2csv.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
#-------------------------------------------------
# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals
import argparse
import csv
import itertools
import io
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
options = parser.parse_args()
readfile = options.file_path
encoding_option = options.encoding

basename = os.path.basename(readfile)
dirname = os.path.dirname(readfile)
name, ext = os.path.splitext(basename)
org_name = name

flag = 0
count = 0
column = 0
area_comment = []
atomName_array = []
allData = []
header = []
maxlen = 0
arr = []
description = 'No title'
acqdate = ''
filetype = ''
element = ['#legend']
collection_time = ['#acq_time']
xlabelname = ''
ylabelname = ''
target = ''
wavetype = ''
with open(readfile, 'r', encoding=encoding_option) as f:
    for line in f:
        line = line.strip()
        if flag == 0:
            if line.find('RAS_INT_START') > -1:
                flag = 1
                count = 1
                arr = []
                dimension = 2
                if len(header) == 0:
                    meta = ['#title', name+ext]
                    header.append(meta)
                    meta = ['#dimension', 'x', 'y']
                    header.append(meta)
                    meta = ['#x', xlabelname, xlabelunit]
                    header.append(meta)
                    meta = ['#y', ylabelname, ylabelunit]
                    header.append(meta)
                    element.append(target+' '+wavetype)
                    meta = element
                    header.append(meta)
                    meta = ['##acq_date', acqdate]
                    header.append(meta)
                    if filememo != "":
                        meta = ['##comment', filememo]
                        header.append(meta)
                else:
                    header[4].append(target+' '+wavetype+'_2')
            else:
                if line.find('HW_XG_TARGET_NAME') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    target = value[1]
                if line.find('MEAS_COND_XG_WAVE_TYPE') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    wavetype = value[1]
                    if wavetype.find('a'):
                        wavetype = wavetype.replace('a', '_alpha')
                    if wavetype.find('b'):
                        wavetype = wavetype.replace('b', '_beta')
                if line.find('MEAS_SCAN_AXIS_X ') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    xlabelname = value[1]
                    theta_list = ['TwoThetaTheta', '2θ/θ']
                    if xlabelname in theta_list:
                        xlabelname = '2Theta-Theta'
                if line.find('MEAS_SCAN_END_TIME') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    acqdate = value[1]
                if line.find('FILE_COMMENT') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    if value[1] != "":
                        description = value[1]
                if line.find('MEAS_SCAN_UNIT_X') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    xlabelunit = value[1]
                if line.find('MEAS_SCAN_UNIT_Y') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    ylabelname = 'Intensity'
                    ylabelunit = value[1]
                if line.find('FILE_MEMO') > -1:
                    value = line.split(" ", 1)
                    tempvalue = value[1]
                    value[1] = tempvalue[1:-1]
                    if value[1] != "":
                        filememo = value[1]
                        if filememo == " ":
                            filememo = ""
                    else:
                        filememo = ""
        else:
            if line.find('RAS_DATA_END') > -1:
                break
            else:
                if line.find('RAS_INT_END') > -1:
                    flag = 0
                    allData.insert(column, arr)
                    mylen = len(arr)
                    if maxlen < mylen:
                        maxlen = mylen
                    column += 1
                else:
                    line = line.rstrip()
                    temp = []
                    if ',' in line:
                        itemList = line.split(',')
                    else:
                        itemList = line.split()
                    for i, j in enumerate(itemList):
                        if i == 0:
                            temp.insert(i, j)
                        elif i == 1:
                            value = float(itemList[i])
                        elif i == 2:
                            value = f"{float(itemList[i]) * value:.4f}"
                            temp.insert(i, value)
                    arr.insert(count, temp)
                count += 1
column = column - 1
elements = element[:]
elements.pop(0)
atomName_array = []
for col in elements:
    atomName_array.append(col + '_x')
    atomName_array.append(col)

header.append('')
lst = [[[''] * 2 for i in range(maxlen)] for j in range(column+1)]
for i, j in enumerate(allData):
    lst[i][0:len(j)] = j
list2 = list(map(list, zip(*lst)))
for i, j in enumerate(list2):
    temp = list2[i]
    csvout = [x for l in temp for x in l]
writefile = name + '.csv'
with open(writefile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(header)
    for i, j in enumerate(list2):
        temp = list2[i]
        csvout = [x for l in temp for x in l]
        writer.writerow(csvout)
