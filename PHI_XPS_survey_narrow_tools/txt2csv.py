# -------------------------------------------------
# txt2csv.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
# -------------------------------------------------
# coding: utf-8

__package__ = "M-DaC_XPS/PHI_XPS_survey_narrow_tools"
__version__ = "1.0.1"

import argparse
import csv
import itertools
import io
import os.path
import codecs

parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="input file")
parser.add_argument("--encoding", default="utf_8")
options = parser.parse_args()
readfile = options.file_path
encoding_option = options.encoding
basename = os.path.basename(readfile)
dirname = os.path.dirname(readfile)
name, ext = os.path.splitext(basename)

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
description_line = 0
templine = 0
acqdate = ''
filetype = ''
element = ['#legend']
collection_time = ['#acq_time']
checkline = "Area Comment,RegionNo,AtomicName,Area No,XLabel,YLabel,DataCount"
with codecs.open(readfile, 'r', encoding_option, 'ignore') as f:
    for line in f:
        line = line.strip()
        if flag == 0:
            if line.find(checkline) > -1:
                templine = 1
                flag = 1
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
                    collection_time.append(float(spectral_reg[10]))
                if line.find('FileType') > -1:
                    value = line.split(':')
                    filetype = value[-1].strip()
                    print(filetype)
                if line.find('SpatialAreaDesc') > -1:
                    value = line.split(':')
                    description = value[-1].split()
                    description = value[1].lstrip(description[0] + ' ')
        else:
            if line == '' and description_line != 1:
                flag = 0
                allData.insert(column, arr)
                column += 1
                description_line = 0
                templine += 1
            else:
                templine += 1
                line = line.rstrip()
                temp = []
                if column == 0 and count == 1:
                    title = name
                    meta = ['#title', title]
                    header.append(meta)
                    meta = ['#dimension', 'x', 'y']
                    header.append(meta)
                elif count == 5 and column == 0:
                    itemList = line.split(',')
                    for i, j in enumerate(itemList):
                        temp.insert(i, j)
                    xlabel = itemList[0].split('(')
                    xlabelname = xlabel[0]
                    xlabelunit = xlabel[1].replace(')', '')
                    if len(itemList) > 1:
                        xoption = itemList[1]
                    xlabelList = itemList
                elif count == 6 and column == 0:
                    itemList = line.split(',')
                    for i, j in enumerate(itemList):
                        temp.insert(i, j)
                    ylabel = itemList[0].split('(')
                    ylabelname = ylabel[0]
                    ylabelunit = ylabel[1].replace(')', '')
                    if (ylabelunit == 'c/s'):
                        ylabelunit = 'cps'
                    if len(xlabelList) > 1:
                        meta = ['#x', xlabelname, xlabelunit, xoption]
                    else:
                        meta = ['#x', xlabelname, xlabelunit]
                    header.append(meta)
                    meta = ['#y', ylabelname, ylabelunit]
                    header.append(meta)
                    meta = element
                    header.append(meta)
                    meta = ['##acq_date', acqdate]
                    header.append(meta)
                    meta = ['##tool_package', __package__]
                    header.append(meta)
                    meta = ['##tool_filename', os.path.basename(__file__)]
                    header.append(meta)
                    meta = ['##tool_version', __version__]
                    header.append(meta)
                    meta = ['##comment', filetype]
                    header.append(meta)
                elif 7 < count:
                    if ',' in line:
                        itemList = line.split(',')
                    else:
                        itemList = line.split('\t')
                    for i, j in enumerate(itemList):
                        temp.insert(i, j)
                    arr.insert(count-8, temp)
                    if maxlen < count-7:
                        maxlen = count-7
                count += 1
                description_line += 1

allData.insert(column, arr)
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
