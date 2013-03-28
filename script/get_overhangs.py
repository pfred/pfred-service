#!/usr/bin/env python

import string
import sys

mRNA_in = open(sys.argv[1], "r") 
oligos_in = open(sys.argv[3], "r") 
parser = sys.argv[2]
seq = ""
if parser == "FASTA" or parser == "fasta" or parser == "Fasta":
	header = string.split(string.strip(mRNA_in.readline()))
	for line in mRNA_in.readlines():
		nline = string.strip(line)
		seq += nline
elif parser == "text" or parser == "TEXT" or parser == "Text" or parser == "txt" or parser:
	for line in mRNA_in.readlines():
		nline = string.strip(line)
		seq += nline

RNA_seq = "" 
for nt in seq:
	if nt == "T":
		RNA_seq += "U"
	else:
		RNA_seq += nt
		
oLiGoS = {}
header_oligos = string.strip(oligos_in.readline()).split(",")
nameOligo_col_index = header_oligos.index("name")
target_col_id = header_oligos.index("target_name")
sense_col_id = header_oligos.index("parent_sense_oligo")
antisense_col_id = header_oligos.index("parent_antisense_oligo")
start_col_id = header_oligos.index("start")
end_col_id = header_oligos.index("end")

for line in oligos_in.readlines():
	nline = string.strip(line)
	tokens = nline.split(",")
	aso__5_3 = tokens[antisense_col_id] 
	so__5_3 = tokens[sense_col_id] 
	oLiGoS[tokens[nameOligo_col_index]] = aso__5_3,so__5_3, tokens[start_col_id], tokens[end_col_id] 

oLiGoS_OH = {} 
for seq_name in oLiGoS.keys():
	sense_5p_3p = oLiGoS[seq_name][1]
	start_id = oLiGoS[seq_name][2]
	end_id = oLiGoS[seq_name][3]
	nt_id = int(start_id) -1
	
	if nt_id > 1 and nt_id < (len(RNA_seq)-20):
		oh_sense = RNA_seq[nt_id-2]+RNA_seq[nt_id-1]+sense_5p_3p
		sense_oh = sense_5p_3p+RNA_seq[nt_id+1+18]+RNA_seq[nt_id+2+18]
		
		oh_antisense__3_5 = "" 
		for ntd in oh_sense:
			if ntd == "A":
				oh_antisense__3_5 += "U"
			elif ntd == "C":
				oh_antisense__3_5 += "G"
			elif ntd == "G":
				oh_antisense__3_5 += "C"
			elif ntd == "U":
				oh_antisense__3_5 += "A"

		oh_antisense__5_3 = "" 
		for ntd_idt in range(len(oh_antisense__3_5),0,-1):
			oh_antisense__5_3 += oh_antisense__3_5[ntd_idt-1]
		oLiGoS_OH[seq_name] = sense_oh, oh_antisense__3_5, oh_antisense__5_3
	

oligo2predict = open("oligo2predict.csv", "w")
oligo2predict.write("%s,%s\n" % ("Guide_strand","NAS_ID"))					
for seq_name in oLiGoS_OH.keys():
	oligo2predict.write("%s,%s\n" % (oLiGoS_OH[seq_name][2],seq_name))	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
