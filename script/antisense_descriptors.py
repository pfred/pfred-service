#!/usr/bin/env python

import string
import sys
import math
from rpy import *

#./antisense.py antisense_seq.csv
#
#./antisense.py thermo_py.seq.txt
#
#
# 2) The antisense sequence can be given with or without overhangs and with different lenghts 
#
# 3) The rna and dna antisense can be written in both uppercase or lowercase letters
#

lenghts = {} #dictionary storing the lenghts for different arrays of descriptors

####################################
#     Standard Deviation Filter    #
####################################
def stdev_filter(raw_dict,new_dict):	
	keys = raw_dict.keys()
	var2remove = []
	for i in range(len(raw_dict[keys[0]])):
		tmp_dict_ii = {}
		tmp_var_i = []
		for key in raw_dict.keys():
			tmp_var_i.append(raw_dict[key][i])
		#-->Filter based on SD - sometime fails in LOO because of this cases (0,0,0,0,0,0,0,0,0,1)
		#-->The variance could be fine for the all set, however in loo, when you remove 1, then you have all 0s.
		#sdev = r.sd(tmp_var_i)
		#if sdev*sdev <= 0.05:				#SD threshold: to be decided yet
		#	var2remove.append(i)
		count_1s = 0
		for value in tmp_var_i:
			tmp_dict_ii[value] = "varianceTest"
			if value == 1:
				count_1s += 1
		if len(tmp_dict_ii.keys()) > 2:
			pass		
		elif len(tmp_dict_ii.keys()) == 2 and count_1s > 1:
			pass
		else:
			var2remove.append(i)	
	
	#build new_dict
	for KeY in raw_dict.keys():
		old_array = raw_dict[KeY]
		new_array = []	
		for j in range(len(old_array)):
			if j in var2remove:
				pass
			else:
				new_array.append(old_array[j])
		new_dict[KeY] = new_array		
			


#########################################
#     Quality control  descriptors      #
#########################################
quality_descriptors = {} 	 # {key : (AAAAA_count,CCCCC_count,GGGGG_count,TTTTT_count, sec_struct_index)}
def quality_filter(dict_sequences):
	for KeY in dict_sequences.keys():
		seq = dict_sequences[KeY]
		#---------------------> Nucleotide Stretches 
		AAAAA_count = 0
		CCCCC_count = 0
		GGGGG_count = 0
		TTTTT_count = 0
		if "aaaaa" in seq or "AAAAA" in seq:
			AAAAA_count += 1
		elif "ccccc" in seq or "CCCCC" in seq:
			CCCCC_count += 1
		elif "ggggg" in seq or "GGGGG" in seq:
			GGGGG_count += 1
		elif "uuuuu" in seq or "TTTTT" in seq or "ttttt" in seq:
			TTTTT_count += 1						
		
		#---------------------> GC counts
		gc_count = 0
		for i in range(len(seq)):
			if seq[i] == "C" or seq[i] == "c":
				gc_count += 1
			elif seq[i] == "G" or seq[i] == "g":
				gc_count += 1
		GC_content = (float(gc_count)/len(seq))*100
		
		
		#---------------------> Add Unafold prediction of secondary structure of antisense strand
		sec_struct_index = 0
		#
		
		quality_descriptors[KeY] = GC_content,AAAAA_count,CCCCC_count,GGGGG_count,TTTTT_count,sec_struct_index
	

#################################################
#     Sequence-position based descriptors       #
#		(21 nucleotides)                #
#         Compute also G/C contents             # ->lenght must be fixed
#################################################
seq_descriptors = {}
def sequence_positions(dict_sequences):
	seq_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		seq = dict_sequences[KeY]
		lenght_seq = len(seq)*4
		seq_string = [0]*lenght_seq
		gc_count = 0
		j = 0
		for i in range(len(seq)):
			if seq[i] == "A" or seq[i] == "a":
				seq_string[i+j+0] = 1
			elif seq[i] == "C" or seq[i] == "c":
				seq_string[i+j+1] = 1
				gc_count += 1
			elif seq[i] == "G" or seq[i] == "g":
				seq_string[i+j+2] = 1
				gc_count += 1
			elif seq[i] == "U" or seq[i] == "u":
				seq_string[i+j+3] = 1
			elif seq[i] == "t":
				seq_string[i+j+3] = 1
			j += 3	
		GC_content = (float(gc_count)/len(seq))*100
		seq_string.append(GC_content) #adding GC contents
		seq_descriptors_tmp[KeY] = seq_string
	stdev_filter(seq_descriptors_tmp,seq_descriptors)	
	ki = seq_descriptors.keys()
	seq_lenght = len(seq_descriptors[ki[0]])	
	lenghts['positions'] = seq_lenght
	print "position_descriptors =",seq_lenght
	
#################################################
#     Sequence-position NN based descriptors    #
#		(lenght must be fixed)          #
#################################################
nn_descriptors = {}
def sequence_NNpositions(dict_sequences):
	nn_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		seq = dict_sequences[KeY]
		lenght_seq = (len(seq))*4*4*2
		seq_string = [0]*lenght_seq
		j = 0
		first = 1
		for i in range(len(seq)):
			if first: #first position
				nn_r = seq[i+1]				#nn_r: neighbour on the right side
				if seq[i] == "A" or seq[i] == "a":
					start_id = i+j+0
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7
					seq_string[id_after] = 1
			
				elif seq[i] == "C" or seq[i] == "c":
					start_id = i+j+8
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7
					seq_string[id_after] = 1
			
				elif seq[i] == "G" or seq[i] == "g":
					start_id = i+j+16
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7				
					seq_string[id_after] = 1
			
				elif seq[i] == "T" or seq[i] == "t":
					start_id = i+j+24
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7				
					seq_string[id_after] = 1
				first = 0
			
			elif i == len(seq)-1: #last position
				nn_l = seq[i-1]				#nn_l: neighbour on the right side
				if seq[i] == "A" or seq[i] == "a":
					start_id = i+j+0
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3
					seq_string[id_before] = 1
			
				elif seq[i] == "C" or seq[i] == "c":
					start_id = i+j+8
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3
					seq_string[id_before] = 1
			
				elif seq[i] == "G" or seq[i] == "g":
					start_id = i+j+16
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3				
					seq_string[id_before] = 1
			
				elif seq[i] == "T" or seq[i] == "t":
					start_id = i+j+24
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3				
					seq_string[id_before] = 1
			
			else:	
				nn_l = seq[i-1]
				nn_r = seq[i+1]
				if seq[i] == "A" or seq[i] == "a":
					start_id = i+j+0
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7
					seq_string[id_before] = 1
					seq_string[id_after] = 1
				elif seq[i] == "C" or seq[i] == "c":
					start_id = i+j+8
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7
					seq_string[id_before] = 1
					seq_string[id_after] = 1
				elif seq[i] == "G" or seq[i] == "g":
					start_id = i+j+16
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3			
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7				
					seq_string[id_before] = 1
					seq_string[id_after] = 1
				elif seq[i] == "U" or seq[i] == "u":
					start_id = i+j+24
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "T" or nn_l == "t":	
						id_before = start_id + 3			
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "T" or nn_r == "t":	
						id_after = start_id + 7				
					seq_string[id_before] = 1
					seq_string[id_after] = 1
			j += 31	
		nn_descriptors_tmp[KeY] = seq_string
	stdev_filter(nn_descriptors_tmp,nn_descriptors)	
	ki = nn_descriptors.keys()
	nn_lenght = len(nn_descriptors[ki[0]])	
	lenghts['NNpositions'] = nn_lenght
	print "NNposition_descriptors =",nn_lenght


#############################################################################
#                    Composition based descriptors 			    #
#############################################################################
comp_descriptors = {}

def sequence_composition(dict_sequences):
	comp_vars = ["A","C","G","T",
		     "AA","AC","AG","AT","CA","CC","CG","CT","GA","GC","GG","GT","TA","TC","TG","TT",
		     "AAA","AAC","AAG","AAT","ACA","ACC","ACG","ACT","AGA","AGC","AGG","AGT","ATA","ATC","ATG","ATT",
		     "CAA","CAC","CAG","CAT","CCA","CCC","CCG","CCT","CGA","CGC","CGG","CGT","CTA","CTC","CTG","CTT",
		     "GAA","GAC","GAG","GAT","GCA","GCC","GCG","GCT","GGA","GGC","GGG","GGT","GTA","GTC","GTG","GTT",
		     "TAA","TAC","TAG","TAT","TCA","TCC","TCG","TCT","TGA","TGC","TGG","TGT","TTA","TTC","TTG","TTT"]

	comp_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		comp_string = [0]*84

		dna_seq = dict_sequences[KeY] #5'->3' dna antisense sequence
		seq = string.upper(dna_seq)
		
		for ni in range(len(seq)): #single
			Ni = seq[ni]
			Pi = comp_vars.index(Ni)
			comp_string[Pi] += 1
		for ni in range(len(seq)-1): #duplets
			Nij = seq[ni:ni+2]
			Pij = comp_vars.index(Nij)
			comp_string[Pij] += 1
		for ni in range(len(seq)-2): #triplets
			Nijk = seq[ni:ni+3]
			Pijk = comp_vars.index(Nijk)
			comp_string[Pijk] += 1
		comp_descriptors_tmp[KeY] = comp_string
	stdev_filter(comp_descriptors_tmp,comp_descriptors)	
	ki = comp_descriptors.keys()
	comp_lenght = len(comp_descriptors[ki[0]])	
	lenghts['composition'] = comp_lenght
	print "composition_descriptors =", comp_lenght
	
	
#######################################################
#               ACC based descriptors 	              #
#    (21 nucleotides  or full-nucleotide sequence)    #
#######################################################
basis_set = {"A" : (-1, -1, +1),"C" : (+1, -1, -1),"G" : (-1, +1, -1),"T" : (+1, +1, +1),"U" : (+1, +1, +1),
             "a" : (-1, -1, +1),"c" : (+1, -1, -1),"g" : (-1, +1, -1),"t" : (+1, +1, +1),"u" : (+1, +1, +1)}
ACC_descriptors = {}
def sequence_acc(dict_sequences,acc_max_lag):
	ACC_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		ori_seq = dict_sequences[KeY]
		l = len(ori_seq)
		Max_Lag = acc_max_lag
		modify_seq = []
		for i in ori_seq:
			modify_seq.append(basis_set[i][0])
			modify_seq.append(basis_set[i][1])
			modify_seq.append(basis_set[i][2])
		TMP_LIST = []
		for d in range(1,Max_Lag):
			a_11 = 0
			a_22 = 0
			a_33 = 0
			c_12 = 0
			c_13 = 0
			c_21 = 0
			c_23 = 0
			c_31 = 0
			c_32 = 0
		#---a_11
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j] * modify_seq[i+j+3+(3*(d-1))]
				a_11 += tmp_count
			A_11 = float(a_11)/float(l-d)
			#print a_11, l, d, l-d, A_11
			TMP_LIST.append(A_11)
		#---a_22
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+1] * modify_seq[i+j+3+1+(3*(d-1))]
				a_22 += tmp_count
			A_22 = float(a_22)/float(l-d)
			TMP_LIST.append(A_22)
		#---a_33
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+2] * modify_seq[i+j+3+2+(3*(d-1))]
				a_33 += tmp_count
			A_33 = float(a_33)/float(l-d)
			TMP_LIST.append(A_33)
		#---c_12
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j] * modify_seq[i+j+3+1+(3*(d-1))]
				c_12 += tmp_count
			C_12 = float(c_12)/float(l-d)
			TMP_LIST.append(C_12)
		#---c_13
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j] * modify_seq[i+j+3+2+(3*(d-1))]
				c_13 += tmp_count
			C_13 = float(c_13)/float(l-d)
			TMP_LIST.append(C_13)
		#---c_21
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+1] * modify_seq[i+j+3+(3*(d-1))]
				c_21 += tmp_count
			C_21 = float(c_21)/float(l-d)
			TMP_LIST.append(C_21)
		#---c_23
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+1] * modify_seq[i+j+3+2+(3*(d-1))]
				c_23 += tmp_count
			C_23 = float(c_23)/float(l-d)
			TMP_LIST.append(C_23)
		#---c_31
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+2] * modify_seq[i+j+3+(3*(d-1))]
				c_31 += tmp_count
			C_31 = float(c_31)/float(l-d)
			TMP_LIST.append(C_31)
		#---c_32
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+2] * modify_seq[i+j+3+1+(3*(d-1))]
				c_32 += tmp_count
			C_32 = float(c_32)/float(l-d)
			TMP_LIST.append(C_32)
		ACC_descriptors_tmp[KeY] = TMP_LIST	
	stdev_filter(ACC_descriptors_tmp,ACC_descriptors)	
	ki = ACC_descriptors.keys()
	ACC_lenght = len(ACC_descriptors[ki[0]])	
	lenghts['acc'] = ACC_lenght
	print "acc_descriptors =", ACC_lenght




                                                                    ###########################################
#-------------------------------------------------------------------#      NN based descriptors   (rna/dna)   #-------------------------------------------------------------------
#                                                                   ###########################################
#			
#Sugimoto NN model (Biochemistry 1995, v34, n35, 11211-11216)    
#dictionary structure ==> {"XY":(dH,dS,dG)}......dH(kcal/mol), dS(eu), dG(kcal/mol)
ThermoParameter_rnadna = {"AA":(-7.8,-21.9,-1.0,"rAA_dTT"),
		          "AC":(-5.9,-12.3,-2.1,"rAC_dTG"),
		          "AG":(-9.1,-23.5,-1.8,"rAG_dTC"),
		          "AU":(-8.3,-23.9,-0.9,"rAU_dTA"),
		          "CA":(-9.0,-26.1,-0.9,"rCA_dGT"),
		          "CC":(-9.3,-23.2,-2.1,"rCC_dGG"),
		          "CG":(-16.3,-47.1,-1.7,"rCG_dGC"),
		          "CU":(-7.0,-19.7,-0.9,"rCU_dGA"),
		          "GA":(-5.5,-13.5,-1.3,"rGA_dCT"),
		          "GC":(-8.0,-17.1,-2.7,"rGC_dCG"),
		          "GG":(-12.8,-31.9,-2.9,"rGG_dCC"),
		          "GU":(-7.8,-21.6,-1.1,"rGU_dCA"),
		          "UA":(-7.8,-23.2,-0.6,"rUA_dAT"),
		          "UC":(-8.6,-22.9,-1.5,"rUC_dAG"),
		          "UG":(-10.4,-28.4,-1.6,"rUG_dAC"),
		          "UU":(-11.5,-36.4,-0.2,"rUU_dAA"),
			  "Initiation":(1.9,-3.9,3.1,),
			  "Symmetry_nonSelf":(0.00,0.00,0.00)}


Tot_strand_concentration_nonSelf = 0.0002 #M
Thermo_descriptors = {}
def thermodynamic_rnadna(dict_sequences):
	Thermo_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		dna_seq = dict_sequences[KeY] #5'->3' dna antisense sequence
		
		#Defining the RNA reverse complement of the DNA antisense sequence 
		#Antisense
		aso__3_5 = ""
		for ntd in dna_seq:
			if ntd == "A" or ntd == "a":
				aso__3_5 += "U"
			elif ntd == "C" or ntd == "c":
				aso__3_5 += "G"
			elif ntd == "G" or ntd == "g":
				aso__3_5 += "C"
			elif ntd == "T" or ntd == "t":
				aso__3_5 += "A"
		aso__5_3 = ""
		for ntd_id in range(len(aso__3_5),0,-1):
			aso__5_3 += aso__3_5[ntd_id-1]
		seq = aso__5_3
		
		#Initializing lists and counters
		Thermo_List = [] #list of thermodynamic descriptors
		D_H = 0
		D_S = 0
		D_G = 0
		tmp_dG = [] #temporary free energy profiles
		tmp_dS = [] #temporary entalpy profiles
		tmp_dH = [] #temporary entropy profiles
		
		for idx in range(len(seq)-1):
			seq2 = seq[idx] + seq[idx+1]
			d_H = ThermoParameter_rnadna[seq2][0]
			d_S = ThermoParameter_rnadna[seq2][1]
			d_G = ThermoParameter_rnadna[seq2][2]
			tmp_dH.append(d_H)
			tmp_dS.append(d_S)
			tmp_dG.append(d_G)
			D_H += d_H
			D_S += d_S
			D_G += d_G
			
		
		DELTA_H_nonSelf = D_H + ThermoParameter_rnadna["Initiation"][0] + ThermoParameter_rnadna["Symmetry_nonSelf"][0]
		DELTA_S_nonSelf = D_S + ThermoParameter_rnadna["Initiation"][1] + ThermoParameter_rnadna["Symmetry_nonSelf"][1]
		DELTA_G_nonSelf = D_G + ThermoParameter_rnadna["Initiation"][2] + ThermoParameter_rnadna["Symmetry_nonSelf"][2]
		Tm_nonSelf = ((DELTA_H_nonSelf*1000)/(DELTA_S_nonSelf+(1.987*(math.log(Tot_strand_concentration_nonSelf/4.0)))))-273.15
		Thermo_List.append(DELTA_H_nonSelf) 	 #1 descr
		Thermo_List.append(DELTA_S_nonSelf) 	 #1 descr
		Thermo_List.append(DELTA_G_nonSelf) 	 #1 descr
		Thermo_List.append(Tm_nonSelf)     	 #1 descr
		
		
		#---->Differential free-energy descriptors type1
		Thermo_List.append((float(tmp_dG[-1])-float(tmp_dG[0])))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-float(tmp_dG[1])))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-float(tmp_dG[2])))  #1 descr
		Thermo_List.append((float(tmp_dG[-2])-float(tmp_dG[0])))  #1 descr
		Thermo_List.append((float(tmp_dG[-2])-float(tmp_dG[1])))  #1 descr
		Thermo_List.append((float(tmp_dG[-2])-float(tmp_dG[2])))  #1 descr
		Thermo_List.append((float(tmp_dG[-3])-float(tmp_dG[0])))  #1 descr
		Thermo_List.append((float(tmp_dG[-3])-float(tmp_dG[1])))  #1 descr
		Thermo_List.append((float(tmp_dG[-3])-float(tmp_dG[2])))  #1 descr
		
		#---->Differential free-energy descriptors type2
		Thermo_List.append(((float(tmp_dG[-1])+float(tmp_dG[-2]))-(float(tmp_dG[0])+float(tmp_dG[1]))))  #1 descr
		Thermo_List.append(((float(tmp_dG[-1])+float(tmp_dG[-2])+float(tmp_dG[-3]))-(float(tmp_dG[0])+float(tmp_dG[1])+float(tmp_dG[2]))))  #1 descr
		
		#---->Differential free-energy descriptors type3
		Thermo_List.append((float(tmp_dG[-1])-math.ceil(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-math.ceil(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-math.ceil(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-math.ceil(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-math.ceil(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[0])-math.floor(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[0])-math.floor(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[0])-math.floor(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[0])-math.floor(len(seq)/2.0)))  #1 descr
		Thermo_List.append((float(tmp_dG[0])-math.floor(len(seq)/2.0)))  #1 descr
		
		#---->dH profile
		#for dh in tmp_dH:			 	#dH profile descr
			#Thermo_List.append(dh)  	
		
		#---->dS profile
		#for ds in tmp_dS:                	 	#dS descr
			#Thermo_List.append(ds)
		
		#---->dG profile
		#for dg in tmp_dG:                	 	#dG descr 
			#Thermo_List.append(dg)				
		
		Thermo_descriptors[KeY] = Thermo_List
	ki = Thermo_descriptors.keys()
	thermo_lenght = len(Thermo_descriptors[ki[0]])
	lenghts['thermoDy'] = thermo_lenght
	print "thermo_descriptors",thermo_lenght




##################################################################################################################################################
#                                                                   ##########									 #
#-------------------------------------------------------------------#  MAIN  #-------------------------------------------------------------------#
#                                                                   ##########									 #
##################################################################################################################################################
#For testing this module alone:
"""
SeQuEnCeS = {"0001":"actggcccctttttaaa","0002":"gctggcaccttgtgact"} #rnadna test

thermodynamic_rnadna(SeQuEnCeS)
#print "thermodynamic_rnadna DONE!!"
#print Thermo_descriptors

sequence_acc(SeQuEnCeS,5)
#print "sequence_acc DONE!!"
#print ACC_descriptors

sequence_composition(SeQuEnCeS)
#print "sequence_composition DONE!!"
#print comp_descriptors

sequence_NNpositions(SeQuEnCeS)
#print "sequence_NNpositions DONE!!"
#print nn_descriptors

sequence_positions(SeQuEnCeS)
#print "sequence_positions DONE!!"
#print seq_descriptors

quality_filter(SeQuEnCeS)
#print "quality_filter DONE!!"
#print quality
"""

