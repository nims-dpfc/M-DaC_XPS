#-------------------------------------------------
# batch_exe_XPS_jupyter.py
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
parser.add_argument("--jupytermode", help="for jupyter mode", action="store_true")
options = parser.parse_args()
readfile = options.file_path
jupytermode = options.jupytermode
basename = os.path.basename(readfile)
dirname = os.path.dirname(readfile)
name, ext = os.path.splitext(basename)
currentdir = os.getcwd()

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
subprocess.run(["python", "../" + tooldir + "csv2graph.py", name+".csv"])
subprocess.run(["python", "../" + tooldir + "txt2raw_XPS_survey.py", name+".txt", "../" + tooldir + "xps_raw_template.xml", "raw.xml"])
subprocess.run(["python", "../" + tooldir + "raw2primary_XPS_survey.py", "raw.xml", "../" + tooldir + "xps_primary_template.xml", "primary.xml"])
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
