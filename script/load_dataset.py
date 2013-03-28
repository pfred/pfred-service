#!/usr/bin/env python

import string
import sys

activity = {}		
activity_class = {}	
SeQuEnCeS = {}		
Training_All ={} 	
Training_All_Human ={} 	
Training_Human_E2s ={} 	
Training_Rodent ={} 	
Training_Random_1 ={} 	
Training_Random_2 ={} 	
Training_Random_3 ={} 	
Training_Random_4 ={} 	
Testing_All ={} 	
Testing_All_Human ={} 	
Testing_Human_E2s ={} 	
Testing_Rodent ={} 	
def novartis_data(input_data_file):
	load_seq = open(input_data_file, "r")
	header = load_seq.readline().split(",")
	for line in load_seq.readlines():
		nline = string.strip(line)
		tokens = nline.split(",")
		SeQuEnCeS[tokens[0]] = tokens[1]
		activity[tokens[0]] = tokens[14]
		if float(tokens[14]) >= 0.7:		
			activity_class[tokens[0]] = "1"
		else:
			activity_class[tokens[0]] = "0"
		X_list = []
		for idx in range(2,len(tokens)-1):
			if tokens[idx] == "X":
				X_list.append(idx)
		for x in X_list:
			if x == 2:
				Training_All[tokens[0]] = tokens[14]
			elif x == 3:
				Training_All_Human[tokens[0]] = tokens[14]
			elif x == 4:
				Training_Human_E2s[tokens[0]] = tokens[14]
			elif x == 5:
				Training_Rodent[tokens[0]] = tokens[14]
			elif x == 6:
				Training_Random_1[tokens[0]] = tokens[14]
			elif x == 7:
				Training_Random_2[tokens[0]] = tokens[14]
			elif x == 8:
				Training_Random_3[tokens[0]] = tokens[14]
			elif x == 9:
				Training_Random_4[tokens[0]] = tokens[14]
			elif x == 10:
				Testing_All[tokens[0]] = tokens[14]
			elif x == 11:
				Testing_All_Human[tokens[0]] = tokens[14]
			elif x == 12:
				Testing_Human_E2s[tokens[0]] = tokens[14]
			elif x == 13:
				Testing_Rodent[tokens[0]] = tokens[14]


pfred_seq2pred_name = []
activity2predict_TAG = ["0"]
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
			activity_class[tokens[1]] = tokens[2]
			
	else:	
		for line in load_seq2predict.readlines():
			nline = string.strip(line)
			tokens = nline.split(",")
			SeQuEnCeS[tokens[1]] = tokens[0]
			pfred_seq2pred_name.append(tokens[1])
			activity[tokens[1]] = "0.000"
			activity_class[tokens[1]] = "0.000"













	
