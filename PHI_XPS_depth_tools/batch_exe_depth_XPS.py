#-------------------------------------------------
# execute_XPS.py
#
# Copyright (c) 2018, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
#-------------------------------------------------
# coding: utf-8

import argparse
import os.path
import subprocess

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
resultdir = "../"
tooldir = "./"

print(resultdir + name)
subprocess.run(["mkdir", resultdir + name])
subprocess.run(["cp", readfile, resultdir + name+"/."])
subprocess.run(["cd", resultdir + name])
subprocess.run(["python", tooldir + "MPExport.exe", "-Filename:"+ basename, "-TSV"])
#subprocess.run(["python", tooldir + "txt2csv.py", resultdir + name+"/"+name+".txt"])
#subprocess.run(["python", tooldir + "csv2graph.py", resultdir + name+"/"+name+".csv"])
#subprocess.run(["python", tooldir + "txt2raw_XPS_survey.py", resultdir + name+"/"+basename, tooldir + "xps_raw_template.xml", resultdir + name+"/raw.xml"])
#subprocess.run(["python", tooldir + "raw2primary_XRD.py", resultdir + name+"/raw.xml", tooldir + "xps_primary_template.xml", resultdir + name+"/primary.xml"])
#subprocess.run(["rm", resultdir + name+"/"+basename])