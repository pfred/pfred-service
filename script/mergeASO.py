#!/usr/bin/env python

import string
import sys

#./mergeASO.py EnumerationResult.csv OuTpUt_ReSuLtS.csv

f1 = open(sys.argv[1],"r")
f1Head = string.strip(f1.readline())

f2 = open(sys.argv[2],"r")
f2Head = string.strip(f2.readline())
f2Head = (f2Head.replace("siRNA_id","")).split(",")

asoPred = {}
for line in f2.readlines():
	tokens = (string.strip(line)).split(",")
	# ['siRNA_id'] : {'antisense_strand__5_3', 'SVMpred', 'PLSpred', 'PLSpred_optimized', 'dG', 'Tm', 'G/C'}
	asoPred[tokens[0]] = tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6],tokens[7]
	
f3 = open("ASOActivityModelResult.csv", "w")
f3.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (f1Head,f2Head[1],f2Head[2],f2Head[3],f2Head[4],f2Head[5],f2Head[6],f2Head[7]))

for line in f1.readlines():
	tokens = (string.strip(line)).split(",")
	nline1 = string.strip(line)
	asoProps = asoPred[tokens[0]]
	nline2 = ",%s,%s,%s,%s,%s,%s,%s\n" % (asoProps[0],asoProps[1],asoProps[2],asoProps[3],asoProps[4],asoProps[5],asoProps[6])
	nline = nline1+nline2
	f3.write("%s" % nline)
	
	
	
	
