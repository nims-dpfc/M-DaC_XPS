#-------------------------------------------------
# execute.py
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

subprocess.run(["mkdir", resultdir + name])
subprocess.run(["cp", readfile, resultdir + name+"/."])
subprocess.run(["python", tooldir + "ras2csv.py", "--encoding", "sjis", resultdir + name+"/"+basename])
subprocess.run(["python", tooldir + "csv2graph.py", resultdir + name+"/"+name+".csv"])
subprocess.run(["python", tooldir + "ras2raw_XRD.py", resultdir + name+"/"+basename, "--encoding", "sjis", tooldir + "xrd_raw_template.xml", resultdir + name+"/raw.xml"])
subprocess.run(["python", tooldir + "raw2primary_XRD.py", resultdir + name+"/raw.xml", tooldir + "xrd_primary_template.xml", resultdir + name+"/primary.xml"])
subprocess.run(["rm", resultdir + name+"/"+basename])