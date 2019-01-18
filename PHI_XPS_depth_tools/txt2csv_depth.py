#-------------------------------------------------
# txt2csv_depth.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
#-------------------------------------------------
# coding: utf-8

__package__ = "M-DaC_XPS/PHI_XPS_depth_tools"
__version__ = "1.0.0"

import argparse
import csv
import itertools
import io
import os.path
import numpy as np
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
options = parser.parse_args()
readfile = options.file_path
encoding_option = options.encoding
basename = os.path.basename(readfile)
dirname = os.path.dirname(readfile)
name, ext = os.path.splitext(basename)

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
with codecs.open(readfile, 'r', encoding_option, 'ignore') as f:
    for line in f:
        line = line.strip()
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
                    element2.append(cycle)
                    cyclearray.append(element2)
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
                    allData.insert(column, arr)
                else:
                    if column == len(allData):
                        allData_depth_np = np.array(arr)
                    else:
                        arr_np = np.array(arr)
                        arr_np = arr_np[:,1:]
                        allData_depth_np = np.append(allData_depth_np, arr_np, axis=1)
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
                elif count == headm2 and column == 0:
                    itemList = line.split(',')
                    for i, j in enumerate(itemList):
                        temp.insert(i, j)
                    xlabel = itemList[0].split('(')
                    xlabelname = xlabel[0]
                    xlabelunit = xlabel[1].replace(')', '')
                    if len(itemList) > 1:
                        xoption = itemList[1]
                    xlabelList = itemList
                elif count == headm1 and column == 0:
                    meta = ['##tool_package', __package__]
                    header.append(meta)
                    meta = ['##tool_filename', os.path.basename(__file__)]
                    header.append(meta)
                    meta = ['##tool_version', __version__]
                    header.append(meta)
                    meta = ['##Spectra in depth profile']
                    header.append(meta)
                    meta = ['##Intensity in depth profile']
                    header_depth.append(meta)
                    meta = ['#title', name]
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
                    header_depth.append(element_org)
                    meta = element
                    header.append(meta)
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
                        if depthflag == 1 and column == zcolumn and i == 0:
                            zaxis.append(j)
                    arr.insert(count-header_num+1, temp)
                    if maxlen < count-header_num:
                        maxlen = count-header_num
                count += 1
                description_line += 1
header.append('')
header_depth.append('')
allData_depth = list(allData_depth_np)
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
