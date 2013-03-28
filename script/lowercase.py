#!/usr/bin/env python

import string
import sys

lowercase = ["a","t","c","g","u"]
uppercase = ["A","T","C","G","U"]

file_in = open(sys.argv[1],"r")
file_out = open("oligo2predict_clean.csv","w")
header = string.strip(file_in.readline())
file_out.write("%s\n" % header)
for line in file_in.readlines():
	nline = string.strip(line)
	tokens = nline.split(",")
	sirna1 = tokens[0][:19]
	sirna2 = tokens[0][-2:]
	if sirna2[0] in lowercase:
		new_sirna = sirna1+sirna2
		file_out.write("%s,%s\n" % (new_sirna, tokens[1]))
	else:
		new_sirna = sirna1+string.lower(sirna2)
		file_out.write("%s,%s\n" % (new_sirna, tokens[1]))
	
file_out.close()	
