#!/usr/bin/env python

import string
import sys

#########################################
# Loading AOBase data into a dictionary #
#########################################
activity = {}	
activity_class = {}
SeQuEnCeS = {}	
Training_All = {} 
Testing_All = {} 
lenght = {}
genebank = {}
modification = {}
concentration = {}
assay = {}
readout = {}
readout_assay = {}
UnIqUe = {}


def AOBase_data(input_data_file,min_len,max_len,min_conc,max_conc):
	load_seq = open(input_data_file, "r")
	header = load_seq.readline().split(",")
	for line in load_seq.readlines():
		nline = string.strip(line)
		tokens = nline.split(",")
		
		lenght[tokens[0]] = int(tokens[6])
		genebank[tokens[0]] = tokens[2]
		modification[tokens[0]] = tokens[9]
		concentration[tokens[0]] = float(tokens[12]) #-->nM
		assay[tokens[0]] = tokens[14]
		readout[tokens[0]] = tokens[15]
		readout_assay[tokens[0]] = tokens[16]
		
		#filtering the dataset based only on lenght and concentration
		
		if int(tokens[6]) >= min_len and int(tokens[6]) <= max_len:
			if float(tokens[12]) >= min_conc and float(tokens[12]) <= max_conc:
				SeQuEnCeS[tokens[0]] = tokens[3]
				UnIqUe[tokens[3]] = tokens[0]
				activity[tokens[0]] = tokens[11]
				if float(tokens[11]) >= 0.65:		
					activity_class[tokens[0]] = "+1"
				else:
					activity_class[tokens[0]] = "-1"
				if len(tokens) == 18:
					if tokens[17] == "TRAIN":
						Training_All[tokens[0]] = tokens[3]
					elif tokens[17] == "TEST":
						Testing_All[tokens[0]] = tokens[3]
				else:
					Training_All[tokens[0]] = tokens[3]			
					Testing_All[tokens[0]] = tokens[3]
	print "Sequences after filtering =>",len(SeQuEnCeS.keys())
	#for key in Training_All.keys():
	#	print "%s,%s,%s" % (Training_All[key],key,activity[key])


pfred_seq2pred_name = []
activity2predict_TAG = ["0"]
#column in the input file data must be in this order --> sequence, name, activity(optional)
def seq2predict(sequence_data):
	load_seq2predict = open(sequence_data, "r")
	header = load_seq2predict.readline().split(",")
	if len(header) > 2:
		activity2predict_TAG.append("1")
		for line in load_seq2predict.readlines():
			nline = string.strip(line)
			tokens = nline.split(",")
			SeQuEnCeS[tokens[1]] = tokens[0]
			pfred_seq2pred_name.append(tokens[1])
			activity[tokens[1]] = tokens[2]
			if float(tokens[2]) >= 0.65:	
				activity_class[tokens[1]] = "+1"
			else:
				activity_class[tokens[1]] = "-1"
			
			
	else:	
		for line in load_seq2predict.readlines():
			nline = string.strip(line)
			tokens = nline.split(",")
			SeQuEnCeS[tokens[1]] = tokens[0]
			pfred_seq2pred_name.append(tokens[1])
			activity[tokens[1]] = "0.000"
			activity_class[tokens[1]] = "0"

