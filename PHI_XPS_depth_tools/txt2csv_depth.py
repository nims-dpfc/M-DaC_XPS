# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
# coding: utf-8
#
#__author__ = "nagao"
#__date__ = "$2017/03/09 17:18:43$"

from __future__ import print_function
from __future__ import unicode_literals
import argparse
import csv
import itertools
import io
import os.path
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
options = parser.parse_args()
readfile = options.file_path
encoding_option = options.encoding
#readfile = 'SNP159.113.txt'
name, ext = os.path.splitext(readfile)
flag = 0
depthflag = 0
count = 0
column = 0
header_num = 0
headm2 = 0
headm1 = 0
area_comment = []
atomName_array = []
allData = []
allData_depth = []
header = []
header_depth = []
maxlen = 0
zcolumn = 0
arr = []
arr_depth = []
description = 'No title'
description_line = 0
templine = 0
acqdate = ''
filetype = ''
zaxis = ['']
element = ['#legend']
element2 = ['##Sputter Time']
cyclearray = []
collection_time = ['#acq_time']
with open(readfile, 'r', encoding=encoding_option) as f:
    for line in f:
        line = line.strip()
#        print('flag=',flag,'depthflag=',depthflag,' column=',column,' count=',count,' line=',line)
        if flag == 0:
            if line.find('Area Comment,RegionNo,AtomicName,Cycle,XLabel,YLabel,DataCount') > -1:
                array = line.lstrip('//')
                array = array.split(',')
                header_num = len(array)
                templine  = 1
                flag = 1
                count = 1
                arr = []
                dimension = 2
                description_line = 1
            elif line.find('Area Comment,AtomicName,XLabel,YLabel,DataCount') > -1:
                if depthflag == 0:
                    zcolumn = column
                array = line.lstrip('//')
                array = array.split(',')
                header_num = len(array)
                templine  = 1
                flag = 1
                depthflag = 1
                count = 1
                arr = []
                dimension = 2
                description_line = 1
            else:
#                print('line=',line)
                if line.find('AcqFileDate') > -1:
                    value = line.split(':')
                    date = value[-1].split()
                    mm = date[1].zfill(2)
                    dd = date[2].zfill(2)
                    acqdate = date[0] + mm + dd
                if line.find('SpectralRegDef:') > -1:
                    value = line.split(':')
                    spectral_reg = value[-1].split()
                    if spectral_reg[2] == 'Su1s':
                        spectral_reg[2] = 'Survey'
                    element.append(spectral_reg[2])
                    element_org = element[:]
                    collection_time.append(float(spectral_reg[10]))
                if line.find('FileType') > -1:
                    value = line.split(':')
                    filetype = value[-1].strip()
                    print(filetype)
                if line.find('NoDPDataCyc') > -1:
                    value = line.split(':')
                    cycle = value[-1].strip()
#                    print('cycle=',cycle)
                    element2.append(cycle)
                    cyclearray.append(element2)
#                    print(cyclearray)
                if line.find('DepthCalDef:') > -1:
                    value = line.split(':')
                    depthcal_reg = value[-1].split()
                    if len(depthcal_reg) > 9:
                        temp = ['##'+depthcal_reg[1], depthcal_reg[7]+'(min)', depthcal_reg[8]+'(cycle)']
                        cyclearray.append(temp)
                if line.find('SpatialAreaDesc') > -1:
                    value = line.split(':')
                    description = value[-1].split()
                    description = value[1].lstrip(description[0] + ' ')
        else:
            if line == '' and description_line != 1:
                flag = 0
                if depthflag == 0:
#                    print('arr=',arr)
                    allData.insert(column, arr)
#                    print('depthflag=',depthflag, 'column=',column,'allData=',allData)
                else:
#                    print(len(allData))
#                    allData_depth.insert(column, arr)
                    if column == len(allData):
#                        print('column=',column)
                        allData_depth_np = np.array(arr)
#                        allData_depth = arr
#                        print(allData_depth_np)
#                        allData_depth.insert(column, arr)
                    else:
                        arr_np = np.array(arr)
                        arr_np = arr_np[:,1:]
#                        print('arr_np=',arr_np)
                        allData_depth_np = np.append(allData_depth_np, arr_np, axis=1)
#                        print('depthflag=',depthflag, 'column=',column,'allData_depthnp=',allData_depth_np)
#                    print('column=',column, 'allData_depth=',allData_depth)
                column += 1
                description_line = 0
                templine += 1
            else:
                templine += 1
                line = line.rstrip()
                temp = []
                headm2 = header_num - 2
                headm1 = header_num - 1
                if column == 0 and count == 1:
                    print("")
#                    meta = ['#title', description]
#                    header.append(meta)
#                    header_depth.append(meta)
#                    dimension = ['#dimension', 'x', 'y', 'z']
#                    dimension_depth = ['#dimension', 'x', 'y']
#                    header.append(dimension)
#                    header_depth.append(dimension_depth)
                elif count == headm2 and column == 0:
#                    print('count5=',line)
                    itemList = line.split(',')
                    for i, j in enumerate(itemList):
                        temp.insert(i, j)
                    xlabel = itemList[0].split('(')
                    xlabelname = xlabel[0]
                    xlabelunit = xlabel[1].replace(')', '')
                    if len(itemList) > 1:
                        xoption = itemList[1]
#                        print(xoption)
#                    print(xlabelunit)
                    xlabelList = itemList
                elif count == headm1 and column == 0:
                    meta = ['##Spectra in depth profile']
                    header.append(meta)
                    meta = ['##Intensity in depth profile']
                    header_depth.append(meta)
                    meta = ['#title', description]
                    header.append(meta)
                    header_depth.append(meta)
                    dimension = ['#dimension', 'x', 'y', 'z']
                    dimension_depth = ['#dimension', 'x', 'y']
                    header.append(dimension)
                    header_depth.append(dimension_depth)

                    itemList = line.split(',')
                    for i, j in enumerate(itemList):
                        temp.insert(i, j)
                    ylabel = itemList[0].split('(')
                    ylabelname = ylabel[0]
                    if len(ylabel) > 1:
                        ylabelunit = ylabel[1].replace(')', '')
                        if (ylabelunit == 'c/s'):
                            ylabelunit = 'cps'
                    if len(xlabelList) > 1:
                        meta = ['#x', xlabelname, xlabelunit, xoption]
                    else:
                        meta = ['#x', xlabelname, xlabelunit]
                    header.append(meta)
                    meta = ['#x', 'Sputter Time', 'min']
                    header_depth.append(meta)
                    meta = ['#y', ylabelname, ylabelunit]
                    header.append(meta)
                    meta = ['#z', 'Sputter Time', 'min']
                    header.append(meta)
                    meta = ['#y', 'Intensity', 'arb.units']
                    header_depth.append(meta)
#                    print("element=",element)
                    header_depth.append(element_org)
#                    element.append('%Cycle')
                    meta = element
                    header.append(meta)
#                    meta = element2
#                    header.append(meta)
#                    element2.insert(0, 'Sputter Time')
                    for x in cyclearray:
                        header.append(x)
                    meta = ['##block', 'depth_intensity']
                    header_depth.append(meta)
                    meta = ['##acq_date', acqdate]
                    header.append(meta)
                    header_depth.append(meta)
                    meta = ['##comment', filetype]
                    header.append(meta)
                    header_depth.append(meta)
                elif header_num < count:
                    if ',' in line:
                        itemList = line.split(',')
                    else:
                        itemList = line.split('\t')
                    for i, j in enumerate(itemList):
                        temp.insert(i, j)
##                        print('column=',column, 'depthflag=',depthflag,'j=',j)
                        if depthflag == 1 and column == zcolumn and i == 0:
                            zaxis.append(j)
                    arr.insert(count-header_num+1, temp)
                    if maxlen < count-header_num:
                        maxlen = count-header_num
                count += 1
                description_line += 1
#print('header=',header)
#print(zcolumn)
header.append('')
header_depth.append('')
allData_depth = list(allData_depth_np)
#print(allData_depth_np)
#print('zaxis=',zaxis)
writefile = name + '.csv'
with open(writefile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(header)
    writer.writerows(header_depth)    
    for i, j in enumerate(allData):
        writer.writerow(zaxis)
        writer.writerows(j)
        writer.writerow('')
    writer.writerow('')
    temp = []
    temp.append('##depth_intensity')
    writer.writerow(temp)
    for i, j in enumerate(allData_depth):
        writer.writerow(j)
#        print(i)
#        print(len(allData_depth))
#        if i < len(allData_depth)-1:
#            writer.writerow('')
