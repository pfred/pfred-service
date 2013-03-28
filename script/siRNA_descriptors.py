#!/usr/bin/env python

import string
import sys
import math
from rpy import *

lenghts = {} #dictionary storing the lenghts for different arrays of descriptors



####################################
#     Standard Deviation Filter    #
####################################
def stdev_filter(raw_dict,new_dict):
	keys = raw_dict.keys()
	var2remove = []
	for i in range(len(raw_dict[keys[0]])):
		tmp_var_i = []
		for key in raw_dict.keys():
			tmp_var_i.append(raw_dict[key][i])
		if r.sd(tmp_var_i) <= 0:				
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
#     Reynolds score & descriptors      #
#		(19 nucleotides)        #
#########################################
stretches = {} 			
reynolds_descriptors = {} 	
reynolds_score = {} 		
def reynolds_filter(dict_sequences):
	for KeY in dict_sequences.keys():
		seq = dict_sequences[KeY]
		seq_string = [] #		
		AAAAA_count = 0
		CCCCC_count = 0
		GGGGG_count = 0
		UUUUU_count = 0
		if "AAAAA" in seq:
			AAAAA_count += 1
		if "CCCCC" in seq:
			CCCCC_count += 1
		if "GGGGG" in seq:
			GGGGG_count += 1
		if "UUUUU" in seq:
			UUUUU_count += 1			
		stretches[KeY] = AAAAA_count,CCCCC_count,GGGGG_count,UUUUU_count
		
		gc_count = 0
		gc_score = 0
		for i in range(len(seq)):
			if seq[i] == "A" or seq[i] == "a":
				pass
			elif seq[i] == "C" or seq[i] == "c":
				if i < len(seq)-2:
					gc_count += 1
			elif seq[i] == "G" or seq[i] == "g":
				if i < len(seq)-2:
					gc_count += 1
			elif seq[i] == "U" or seq[i] == "u":
				pass
			elif seq[i] == "t":
				pass
		GC_content = (float(gc_count)/19.0)*100
		seq_string.append(GC_content) 
		if GC_content >= 30.0:
			if GC_content <= 52.0:
				gc_score += 1
		
		au_count = 0 
		for i in (0,1,2,3,4):
			if seq[i] == "A" or seq[i] == "a":
				au_count += 1	
			elif seq[i] == "C" or seq[i] == "c":
				pass
			elif seq[i] == "G" or seq[i] == "g":
				pass
			elif seq[i] == "U" or seq[i] == "u":
				au_count += 1
			elif seq[i] == "t":
				pass
		seq_string.append(au_count) 
		
		Tm_score = 0
		seq_string.append(Tm_score)
		
		u_p1 = 0
		if seq[0] == "U" or seq[0] == "u":
			u_p1 += 1
		seq_string.append(u_p1) 
		
		u_p17 = 0
		if seq[16] == "U" or seq[16] == "u":
			u_p17 += 1
		seq_string.append(u_p17) 
		
		a_p10 = 0
		if seq[9] == "A" or seq[9] == "a":
			a_p10 += 1
		seq_string.append(a_p10) 
		
		gc_p1 = 0
		if seq[0] == "C" or seq[0] == "c":
			gc_p1 += 1
		elif seq[0] == "G" or seq[0] == "g":
			gc_p1 += 1	
		seq_string.append(gc_p1) 
		
		gc_p7 = 0
		if seq[6] == "C" or seq[6] == "c":
			gc_p7 += 1	
		seq_string.append(gc_p7)
		
		Rscore = gc_score + Tm_score + u_p1 + u_p17 + a_p10 + au_count - gc_p1 - gc_p7
		reynolds_score[KeY] = Rscore, GC_content, gc_score	
		reynolds_descriptors[KeY] = seq_string
	
		


#################################################
#     Sequence-position based descriptors       #
#		(21 nucleotides)                #
#         Compute also G/C contents             #
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
				if i < len(seq)-2:
					gc_count += 1
			elif seq[i] == "G" or seq[i] == "g":
				seq_string[i+j+2] = 1
				if i < len(seq)-2:
					gc_count += 1
			elif seq[i] == "U" or seq[i] == "u":
				seq_string[i+j+3] = 1
			elif seq[i] == "t":
				seq_string[i+j+3] = 1
			j += 3	
		GC_content = (float(gc_count)/19.0)*100
		seq_string.append(GC_content) #adding GC contents
		seq_descriptors_tmp[KeY] = seq_string
	stdev_filter(seq_descriptors_tmp,seq_descriptors)	
	ki = seq_descriptors.keys()
	seq_lenght = len(seq_descriptors[ki[0]])	
	lenghts['positions'] = seq_lenght	
	
	
#################################################
#     Sequence-position NN based descriptors    #
#		(19 nucleotides)                #
#################################################
nn_descriptors = {}
def sequence_NNpositions(dict_sequences):
	nn_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		seq = dict_sequences[KeY]
		lenght_seq = (len(seq)-2)*4*4*2
		seq_string = [0]*lenght_seq
		j = 0
		first = 1
		for i in range(len(seq)-2):
			if first: #first position
				nn_r = seq[i+1]				
				if seq[i] == "A" or seq[i] == "a":
					start_id = i+j+0
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "U" or nn_r == "u":	
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
					elif nn_r == "U" or nn_r == "u":	
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
					elif nn_r == "U" or nn_r == "u":	
						id_after = start_id + 7				
					seq_string[id_after] = 1
			
				elif seq[i] == "U" or seq[i] == "u":
					start_id = i+j+24
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "U" or nn_r == "u":	
						id_after = start_id + 7				
					seq_string[id_after] = 1
				first = 0
			
			elif i == len(seq)-2: #last position
				nn_l = seq[i-1]				
				if seq[i] == "A" or seq[i] == "a":
					start_id = i+j+0
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "U" or nn_l == "u":	
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
					elif nn_l == "U" or nn_l == "u":	
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
					elif nn_l == "U" or nn_l == "u":	
						id_before = start_id + 3				
					seq_string[id_before] = 1
			
				elif seq[i] == "U" or seq[i] == "u":
					start_id = i+j+24
					if nn_l == "A" or nn_l == "a":
						id_before = start_id + 0
					elif nn_l == "C" or nn_l == "c":	
						id_before = start_id + 1
					elif nn_l == "G" or nn_l == "g":	
						id_before = start_id + 2
					elif nn_l == "U" or nn_l == "u":	
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
					elif nn_l == "U" or nn_l == "u":	
						id_before = start_id + 3
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "U" or nn_r == "u":	
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
					elif nn_l == "U" or nn_l == "u":	
						id_before = start_id + 3
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "U" or nn_r == "u":	
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
					elif nn_l == "U" or nn_l == "u":	
						id_before = start_id + 3			
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "U" or nn_r == "u":	
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
					elif nn_l == "U" or nn_l == "u":	
						id_before = start_id + 3			
					if nn_r == "A" or nn_r == "a":
						id_after = start_id + 4
					elif nn_r == "C" or nn_r == "c":	
						id_after = start_id + 5
					elif nn_r == "G" or nn_r == "g":	
						id_after = start_id + 6
					elif nn_r == "U" or nn_r == "u":	
						id_after = start_id + 7				
					seq_string[id_before] = 1
					seq_string[id_after] = 1
			j += 31	
		nn_descriptors_tmp[KeY] = seq_string
	stdev_filter(nn_descriptors_tmp,nn_descriptors)	
	ki = nn_descriptors.keys()
	nn_lenght = len(nn_descriptors[ki[0]])	
	lenghts['NNpositions'] = nn_lenght	


#############################################################################
#                    Composition based descriptors 			    #
#    (19 nucleotides #### removing the last 2 nucleotides - 3' overhang)    #
#############################################################################
comp_descriptors = {}
def sequence_composition(dict_sequences):
	comp_vars = ["A","C","G","U",
		     "AA","AC","AG","AU","CA","CC","CG","CU","GA","GC","GG","GU","UA","UC","UG","UU",
		     "AAA","AAC","AAG","AAU","ACA","ACC","ACG","ACU","AGA","AGC","AGG","AGU","AUA","AUC","AUG","AUU",
		     "CAA","CAC","CAG","CAU","CCA","CCC","CCG","CCU","CGA","CGC","CGG","CGU","CUA","CUC","CUG","CUU",
		     "GAA","GAC","GAG","GAU","GCA","GCC","GCG","GCU","GGA","GGC","GGG","GGU","GUA","GUC","GUG","GUU",
		     "UAA","UAC","UAG","UAU","UCA","UCC","UCG","UCU","UGA","UGC","UGG","UGU","UUA","UUC","UUG","UUU"]
	comp_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		comp_string = [0]*84
		seq = dict_sequences[KeY]
		test = ["a","c","g","u","t"]		
		if seq[-1] in test:
			seq = seq[:-2] #normally 3'-overhang are lowercase,
				       #so here we just removed the last two nucleotides
		
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
	
	
#######################################################
#               ACC based descriptors 	              #
#    (21 nucleotides  or full-nucleotide sequence)    #
#######################################################
basis_set = {"A" : (-1, -1, +1),"C" : (+1, -1, -1),"G" : (-1, +1, -1),"T" : (+1, +1, +1),"U" : (+1, +1, +1),
             "a" : (-1, -1, +1),"c" : (+1, -1, -1),"g" : (-1, +1, -1),"t" : (+1, +1, +1),"u" : (+1, +1, +1)}
ACC_descriptors = {}
def sequence_acc(dict_sequences):
	ACC_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		ori_seq = dict_sequences[KeY]
		l = len(ori_seq)
		Max_Lag = 13
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
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j] * modify_seq[i+j+3+(3*(d-1))]
				a_11 += tmp_count
			A_11 = float(a_11)/float(l-d)
			TMP_LIST.append(A_11)
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+1] * modify_seq[i+j+3+1+(3*(d-1))]
				a_22 += tmp_count
			A_22 = float(a_22)/float(l-d)
			TMP_LIST.append(A_22)
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+2] * modify_seq[i+j+3+2+(3*(d-1))]
				a_33 += tmp_count
			A_33 = float(a_33)/float(l-d)
			TMP_LIST.append(A_33)
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j] * modify_seq[i+j+3+1+(3*(d-1))]
				c_12 += tmp_count
			C_12 = float(c_12)/float(l-d)
			TMP_LIST.append(C_12)
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j] * modify_seq[i+j+3+2+(3*(d-1))]
				c_13 += tmp_count
			C_13 = float(c_13)/float(l-d)
			TMP_LIST.append(C_13)
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+1] * modify_seq[i+j+3+(3*(d-1))]
				c_21 += tmp_count
			C_21 = float(c_21)/float(l-d)
			TMP_LIST.append(C_21)
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+1] * modify_seq[i+j+3+2+(3*(d-1))]
				c_23 += tmp_count
			C_23 = float(c_23)/float(l-d)
			TMP_LIST.append(C_23)
			for i in range(l-d):
				j = 2 * i
				tmp_count = modify_seq[i+j+2] * modify_seq[i+j+3+(3*(d-1))]
				c_31 += tmp_count
			C_31 = float(c_31)/float(l-d)
			TMP_LIST.append(C_31)
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


	
############################################
#          NN based descriptors            #
############################################
#			
ThermoParameter_set = {"AA":(-6.82,-19.00,-0.93),
		       "AU":(-9.38,-26.70,-1.10),
		       "UA":(-7.69,-20.50,-1.33),
		       "CA":(-10.44,-26.90,-2.11),
		       "CU":(-10.48,-27.10,-2.08),
		       "GA":(-12.44,-32.50,-2.35),
		       "GU":(-11.40,-29.50,-2.24),
		       "CG":(-10.64,-26.70,-2.36),
		       "GC":(-14.88,-36.90,-3.42),
		       "GG":(-13.39,-32.70,-3.26),
		       "UU":(-6.82,-19.00,-0.93),
		       "UG":(-10.44,-26.90,-2.11),
		       "AG":(-10.48,-27.10,-2.08),
		       "UC":(-12.44,-32.50,-2.35),
		       "AC":(-11.40,-29.50,-2.24),
		       "CC":(-13.39,-32.70,-3.26),
		       "terminal_AU":(3.72,10.5,0.45),
		       "Initiation":(3.61,-1.50,4.09),
		       "Symmetry_self":(0.00,-1.40,0.43),
		       "Symmetry_nonSelf":(0.00,0.00,0.00)}

dG_3prime_Dangling_U = {"AU":-0.6,"CU":-1.2,"GU":-0.6,"UU":-0.1}


Tot_strand_concentration_self = 0.0001 #M
Tot_strand_concentration_nonSelf = 0.0002 #M
A_self = -1.4 #eu
A_nonSelf = -2.8 #eu
Thermo_descriptors = {}
def thermodynamic(dict_sequences):
	Thermo_descriptors_tmp = {}
	for KeY in dict_sequences.keys():
		seq = dict_sequences[KeY]
		test = ["a","c","g","u","t"]		
		if seq[-1] in test:
			seq = seq[:-2] #normally 3'-overhang are lowercase,so here we just removed the last two nucleotides
		
		self_simmetry = 0
		test_seq_1 = seq
		test_seq_2 = ""
		for i in range(len(test_seq_1)-1,-1,-1):
			if test_seq_1[i] == "A":
				test_seq_2 += "U"
			elif test_seq_1[i] == "C":
				test_seq_2 += "G"	
			elif test_seq_1[i] == "G":
				test_seq_2 += "C"
			elif test_seq_1[i] == "U":
				test_seq_2 += "A"	
		if test_seq_1 == test_seq_2:
			self_simmetry = 1	
		
		n_AU = 0
		test_AU = 0
		as_AU_test = 0
		ss_AU_test = 0
		if seq[0] == "A" or seq[0] == "U":
			n_AU += 1
			test_AU = 1
			as_AU_test = 1
		if seq[-1] == "A" or seq[-1] == "U":
			n_AU += 1
			test_AU = 1
			ss_AU_test = 1
		Thermo_List = [] #list of thermodynamic descriptors
		D_H = 0
		D_S = 0
		D_G = 0
		tmp_stability = [] #temporary stability profiles
		tmp_dG = [] #temporary free energy profiles
		tmp_dS = [] #temporary entalpy profiles
		tmp_dH = [] #temporary entropy profiles
		
		if self_simmetry == 1:
			for idx in range(len(seq)-1):
				seq2 = seq[idx] + seq[idx+1]
				d_H = ThermoParameter_set[seq2][0]
				d_S = ThermoParameter_set[seq2][1]
				d_G = ThermoParameter_set[seq2][2]
				tmp_dH.append(d_H)
				tmp_dS.append(d_S)
				tmp_dG.append(d_G)
				D_H += d_H
				D_S += d_S
				D_G += d_G
			if test_AU:
				DELTA_H_self = D_H + ThermoParameter_set["Initiation"][0] + ThermoParameter_set["Symmetry_self"][0] + n_AU*ThermoParameter_set["terminal_AU"][0]
				DELTA_S_self = D_S + ThermoParameter_set["Initiation"][1] + ThermoParameter_set["Symmetry_self"][1] + n_AU*ThermoParameter_set["terminal_AU"][1]
				DELTA_G_self = D_G + ThermoParameter_set["Initiation"][2] + ThermoParameter_set["Symmetry_self"][2] + n_AU*ThermoParameter_set["terminal_AU"][2]
				Tm_self = ((DELTA_H_self*1000)/(DELTA_S_self+(1.987*(math.log(Tot_strand_concentration_self)))))-273.15
				Thermo_List.append(DELTA_H_self) 	 #1 descr
				Thermo_List.append(DELTA_S_self) 	 #1 descr
				Thermo_List.append(DELTA_G_self) 	 #1 descr
				Thermo_List.append(Tm_self)     	 #1 descr
			else:
				DELTA_H_self = D_H + ThermoParameter_set["Initiation"][0] + ThermoParameter_set["Symmetry_self"][0]
				DELTA_S_self = D_S + ThermoParameter_set["Initiation"][1] + ThermoParameter_set["Symmetry_self"][1]
				DELTA_G_self = D_G + ThermoParameter_set["Initiation"][2] + ThermoParameter_set["Symmetry_self"][2]	
				Tm_self = ((DELTA_H_self*1000)/(DELTA_S_self+(1.987*(math.log(Tot_strand_concentration_self)))))-273.15
				Thermo_List.append(DELTA_H_self) 	 #1 descr
				Thermo_List.append(DELTA_S_self) 	 #1 descr
				Thermo_List.append(DELTA_G_self) 	 #1 descr
				Thermo_List.append(Tm_self)     	 #1 descr
		else:
			for idx in range(len(seq)-1):
				seq2 = seq[idx] + seq[idx+1]
				d_H = ThermoParameter_set[seq2][0]
				d_S = ThermoParameter_set[seq2][1]
				d_G = ThermoParameter_set[seq2][2]
				tmp_dH.append(d_H)
				tmp_dS.append(d_S)
				tmp_dG.append(d_G)
				D_H += d_H
				D_S += d_S
				D_G += d_G
			if test_AU:
				DELTA_H_nonSelf = D_H + ThermoParameter_set["Initiation"][0] + ThermoParameter_set["Symmetry_nonSelf"][0] + n_AU*ThermoParameter_set["terminal_AU"][0]
				DELTA_S_nonSelf = D_S + ThermoParameter_set["Initiation"][1] + ThermoParameter_set["Symmetry_nonSelf"][1] + n_AU*ThermoParameter_set["terminal_AU"][1]
				DELTA_G_nonSelf = D_G + ThermoParameter_set["Initiation"][2] + ThermoParameter_set["Symmetry_nonSelf"][2] + n_AU*ThermoParameter_set["terminal_AU"][2]
				Tm_nonSelf = ((DELTA_H_nonSelf*1000)/(DELTA_S_nonSelf+(1.987*(math.log(Tot_strand_concentration_nonSelf/4.0)))))-273.15
				Thermo_List.append(DELTA_H_nonSelf) 	 #1 descr
				Thermo_List.append(DELTA_S_nonSelf) 	 #1 descr
				Thermo_List.append(DELTA_G_nonSelf) 	 #1 descr
				Thermo_List.append(Tm_nonSelf)     	 #1 descr			
			else:
				DELTA_H_nonSelf = D_H + ThermoParameter_set["Initiation"][0] + ThermoParameter_set["Symmetry_nonSelf"][0]
				DELTA_S_nonSelf = D_S + ThermoParameter_set["Initiation"][1] + ThermoParameter_set["Symmetry_nonSelf"][1]
				DELTA_G_nonSelf = D_G + ThermoParameter_set["Initiation"][2] + ThermoParameter_set["Symmetry_nonSelf"][2]
				Tm_nonSelf = ((DELTA_H_nonSelf*1000)/(DELTA_S_nonSelf+(1.987*(math.log(Tot_strand_concentration_nonSelf/4.0)))))-273.15
				Thermo_List.append(DELTA_H_nonSelf) 	 #1 descr
				Thermo_List.append(DELTA_S_nonSelf) 	 #1 descr
				Thermo_List.append(DELTA_G_nonSelf) 	 #1 descr
				Thermo_List.append(Tm_nonSelf)     	 #1 descr
		
		Thermo_List.append((float(tmp_dG[-1])-float(tmp_dG[0])))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-float(tmp_dG[1])))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-float(tmp_dG[2])))  #1 descr
		Thermo_List.append((float(tmp_dG[-2])-float(tmp_dG[0])))  #1 descr
		Thermo_List.append((float(tmp_dG[-2])-float(tmp_dG[1])))  #1 descr
		Thermo_List.append((float(tmp_dG[-2])-float(tmp_dG[2])))  #1 descr
		Thermo_List.append((float(tmp_dG[-3])-float(tmp_dG[0])))  #1 descr
		Thermo_List.append((float(tmp_dG[-3])-float(tmp_dG[1])))  #1 descr
		Thermo_List.append((float(tmp_dG[-3])-float(tmp_dG[2])))  #1 descr
		Thermo_List.append(((float(tmp_dG[-1])+float(tmp_dG[-2]))-(float(tmp_dG[0])+float(tmp_dG[1]))))  #1 descr
		Thermo_List.append(((float(tmp_dG[-1])+float(tmp_dG[-2])+float(tmp_dG[-3]))-(float(tmp_dG[0])+float(tmp_dG[1])+float(tmp_dG[2]))))  #1 descr
		Thermo_List.append((float(tmp_dG[-1])-float(tmp_dG[9])))  #1 descr
		Thermo_List.append((float(tmp_dG[0])-float(tmp_dG[12])))  #1 descr
		for dg in tmp_dG:                	 	#18 descr (34th descriptor)
			Thermo_List.append(dg)				
	
		LS1 = ThermoParameter_set[seq[0]+seq[1]][2] + ThermoParameter_set[seq[1]+seq[2]][2] + ThermoParameter_set[seq[2]+seq[3]][2] + ThermoParameter_set[seq[3]+seq[4]][2]
		if as_AU_test == 1:
			LS1 += ThermoParameter_set["terminal_AU"][2]
		if seq[0] == "A":
			dG_dangling = dG_3prime_Dangling_U["UU"]
			LS1 += dG_dangling
		elif seq[0] == "C":
			dG_dangling = dG_3prime_Dangling_U["GU"]
			LS1 += dG_dangling
		elif seq[0] == "G":
			dG_dangling = dG_3prime_Dangling_U["CU"]
			LS1 += dG_dangling
		elif seq[0] == "U":
			dG_dangling = dG_3prime_Dangling_U["AU"]
			LS1 += dG_dangling
		LS2 = ThermoParameter_set[seq[1]+seq[2]][2] + ThermoParameter_set[seq[2]+seq[3]][2] + ThermoParameter_set[seq[3]+seq[4]][2] + ThermoParameter_set[seq[4]+seq[5]][2]
		LS3 = ThermoParameter_set[seq[2]+seq[3]][2] + ThermoParameter_set[seq[3]+seq[4]][2] + ThermoParameter_set[seq[4]+seq[5]][2] + ThermoParameter_set[seq[5]+seq[6]][2]
		LS4 = ThermoParameter_set[seq[3]+seq[4]][2] + ThermoParameter_set[seq[4]+seq[5]][2] + ThermoParameter_set[seq[5]+seq[6]][2] + ThermoParameter_set[seq[6]+seq[7]][2]
		LS5 = ThermoParameter_set[seq[4]+seq[5]][2] + ThermoParameter_set[seq[5]+seq[6]][2] + ThermoParameter_set[seq[6]+seq[7]][2] + ThermoParameter_set[seq[7]+seq[8]][2]
		LS6 = ThermoParameter_set[seq[5]+seq[6]][2] + ThermoParameter_set[seq[6]+seq[7]][2] + ThermoParameter_set[seq[7]+seq[8]][2] + ThermoParameter_set[seq[8]+seq[9]][2]
		LS7 = ThermoParameter_set[seq[6]+seq[7]][2] + ThermoParameter_set[seq[7]+seq[8]][2] + ThermoParameter_set[seq[8]+seq[9]][2] + ThermoParameter_set[seq[9]+seq[10]][2]
		LS8 = ThermoParameter_set[seq[7]+seq[8]][2] + ThermoParameter_set[seq[8]+seq[9]][2] + ThermoParameter_set[seq[9]+seq[10]][2] + ThermoParameter_set[seq[10]+seq[11]][2]
		LS9 = ThermoParameter_set[seq[8]+seq[9]][2] + ThermoParameter_set[seq[9]+seq[10]][2] + ThermoParameter_set[seq[10]+seq[11]][2] + ThermoParameter_set[seq[11]+seq[12]][2]
		LS10 = ThermoParameter_set[seq[9]+seq[10]][2] + ThermoParameter_set[seq[10]+seq[11]][2] + ThermoParameter_set[seq[11]+seq[12]][2] + ThermoParameter_set[seq[12]+seq[13]][2]
		LS11 = ThermoParameter_set[seq[10]+seq[11]][2] + ThermoParameter_set[seq[11]+seq[12]][2] + ThermoParameter_set[seq[12]+seq[13]][2] + ThermoParameter_set[seq[13]+seq[14]][2]
		LS12 = ThermoParameter_set[seq[11]+seq[12]][2] + ThermoParameter_set[seq[12]+seq[13]][2] + ThermoParameter_set[seq[13]+seq[14]][2] + ThermoParameter_set[seq[14]+seq[15]][2]
		LS13 = ThermoParameter_set[seq[12]+seq[13]][2] + ThermoParameter_set[seq[13]+seq[14]][2] + ThermoParameter_set[seq[14]+seq[15]][2] + ThermoParameter_set[seq[15]+seq[16]][2]
		LS14 = ThermoParameter_set[seq[13]+seq[14]][2] + ThermoParameter_set[seq[14]+seq[15]][2] + ThermoParameter_set[seq[15]+seq[16]][2] + ThermoParameter_set[seq[16]+seq[17]][2]
		LS15 = ThermoParameter_set[seq[14]+seq[15]][2] + ThermoParameter_set[seq[15]+seq[16]][2] + ThermoParameter_set[seq[16]+seq[17]][2] + ThermoParameter_set[seq[17]+seq[18]][2]
		LS16 = ThermoParameter_set[seq[11]+seq[12]][2] + ThermoParameter_set[seq[12]+seq[13]][2] + ThermoParameter_set[seq[13]+seq[14]][2] + ThermoParameter_set[seq[14]+seq[15]][2]
		LS17 = ThermoParameter_set[seq[12]+seq[13]][2] + ThermoParameter_set[seq[13]+seq[14]][2] + ThermoParameter_set[seq[14]+seq[15]][2] + ThermoParameter_set[seq[15]+seq[16]][2]
		LS18 = ThermoParameter_set[seq[13]+seq[14]][2] + ThermoParameter_set[seq[14]+seq[15]][2] + ThermoParameter_set[seq[15]+seq[16]][2] + ThermoParameter_set[seq[16]+seq[17]][2]
		LS19 = ThermoParameter_set[seq[14]+seq[15]][2] + ThermoParameter_set[seq[15]+seq[16]][2] + ThermoParameter_set[seq[16]+seq[17]][2] + ThermoParameter_set[seq[17]+seq[18]][2]
		if ss_AU_test == 1:
			LS19 += ThermoParameter_set["terminal_AU"][2]
		if seq[-1] == "A":
			dG_dangling = dG_3prime_Dangling_U["AU"]
			LS19 += dG_dangling
		elif seq[-1] == "C":
			dG_dangling = dG_3prime_Dangling_U["CU"]
			LS19 += dG_dangling
		elif seq[-1] == "G":
			dG_dangling = dG_3prime_Dangling_U["GU"]
			LS19 += dG_dangling
		elif seq[-1] == "U":
			dG_dangling = dG_3prime_Dangling_U["UU"]
			LS19 += dG_dangling
		tmp_stability.append(LS1)
		tmp_stability.append(LS2)
		tmp_stability.append(LS3)
		tmp_stability.append(LS4)
		tmp_stability.append(LS5)
		tmp_stability.append(LS6)
		tmp_stability.append(LS7)
		tmp_stability.append(LS8)
		tmp_stability.append(LS9)
		tmp_stability.append(LS10)
		tmp_stability.append(LS11)
		tmp_stability.append(LS12)
		tmp_stability.append(LS13)
		tmp_stability.append(LS14)
		tmp_stability.append(LS15)
		tmp_stability.append(LS16)
		tmp_stability.append(LS17)
		tmp_stability.append(LS18)
		tmp_stability.append(LS19)	
		Thermo_List.append((LS9+LS10+LS11+LS12+LS13+LS14)/6.0)    
	
		Thermo_descriptors[KeY] = Thermo_List
	ki = Thermo_descriptors.keys()
	thermo_lenght = len(Thermo_descriptors[ki[0]])
	lenghts['thermoDy'] = thermo_lenght
	


