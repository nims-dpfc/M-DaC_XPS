#-------------------------------------------------
# execute_XRD.py
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
import glob

def getKey(key, row):
    if row[0] == key:
        return row[1]
    else:
        return 0

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
options = parser.parse_args()
readfile = options.file_path
basename = os.path.basename(readfile)
dirname = os.path.dirname(readfile)
name, ext = os.path.splitext(basename)

sourcedir = dirname
resultdir = "../result/"
tooldir = "./"

if os.path.isdir("temp"):
    shutil.rmtree("./temp")
os.mkdir("temp")
shutil.copy2(readfile, "temp/" + basename)
os.chdir("temp")
subprocess.run(["python", "../" + tooldir + "ras2csv.py", "--encoding", "sjis", basename])
subprocess.run(["python", "../" + tooldir + "csv2graph.py", name+".csv"])
subprocess.run(["python", "../" + tooldir + "ras2raw_XRD.py", basename, "--encoding", "sjis", "../" + tooldir + "xrd_raw_template.xml", "raw.xml"])
subprocess.run(["python", "../" + tooldir + "raw2primary_XRD.py", "raw.xml", "../" + tooldir + "xrd_primary_template.xml", "primary.xml"])
os.remove(basename)
os.chdir("../")
if not(os.path.isdir(resultdir)):
    os.mkdir(resultdir)
os.chdir(resultdir)
if os.path.isdir(name):
    shutil.rmtree(name)
os.mkdir(name)
os.chdir("../Rigaku_XRD_tools(batch)/")
for file in glob.glob(r'temp/*'):
    shutil.move(file, resultdir + name)
shutil.rmtree("temp")
