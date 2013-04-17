#!/usr/bin/env python

import string
import sys
import os

#Needed for running CCT protocol
#name,antisense_oligo,sense_oligo,dna_oligo,target_name,start,end
#name,start,end,length,parent_dna_oligo,parent_sense_oligo,parent_antisense_oligo,target_name
#name,start,end,length,parent_dna_oligo,parent_sense_oligo,parent_antisense_oligo,target_name

file_in = open(sys.argv[1], "r")
header = string.strip(file_in.readline()).split(",")
nameID = header.index("name")
ASOseqID = header.index("parent_antisense_oligo")

file_out = open("EnumerationResult_clean.csv", "w")
file_out.write("%s,%s\n" % (header[ASOseqID],header[nameID]))
for line in file_in.readlines():
	tokens = string.strip(line).split(",")
	odn_seq = string.replace(tokens[ASOseqID],"U","T")
	file_out.write("%s,%s\n" % (odn_seq, tokens[nameID]))
file_out.close()

