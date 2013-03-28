#!/usr/bin/env python
#
from siRNA_descriptors import *
from load_dataset import *
from siRNA_stats import *
def write_R_train():
	train_out = open("train_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		#print "var.%d," % (var+1),
		train_out.write("var.%d," % (var+1))
	train_out.write("%s\n" % "activity")
	for key in Training_All.keys():
		if 'p_c_a' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key]
		elif 'p_c' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key]
		elif 'p_a' in sys.argv:
			merged = seq_descriptors[key] + ACC_descriptors[key]
		elif 'c_a' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key]
		elif '_p_' in sys.argv:
			merged = seq_descriptors[key]
		elif '_nn_' in sys.argv:
			merged = nn_descriptors[key]
		elif 'p_nn' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key]		
		elif '_c_' in sys.argv:
			merged = comp_descriptors[key]
		elif '_a_' in sys.argv:	
			merged = ACC_descriptors[key]
		elif 'p_c_a_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]			
		train_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			train_out.write("%f," % merged[var_i])
		train_out.write("%f,%s\n" % (merged[-1],activity[key]))
	
def write_R_test():
	test_out = open("test_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		test_out.write("var.%d," % (var+1))
	test_out.write("%s\n" % "activity")
	for key in Testing_All.keys():
		if 'p_c_a' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key]
		elif 'p_c' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key]
		elif 'p_a' in sys.argv:
			merged = seq_descriptors[key] + ACC_descriptors[key]
		elif 'c_a' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key]
		elif '_p_' in sys.argv:
			merged = seq_descriptors[key]
		elif '_nn_' in sys.argv:
			merged = nn_descriptors[key]
		elif 'p_nn' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key]		
		elif '_c_' in sys.argv:
			merged = comp_descriptors[key]
		elif '_a_' in sys.argv:		
			merged = ACC_descriptors[key]
		elif 'p_c_a_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]	
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		test_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			test_out.write("%f," % merged[var_i])
		test_out.write("%f,%s\n" % (merged[-1],activity[key]))

def write_R_test_predict():
	test_out = open("PredictionTest_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		test_out.write("var.%d," % (var+1))
	test_out.write("%s\n" % "activity")
	for key in pfred_seq2pred_name:
		if 'p_c_a' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key]
		elif 'p_c' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key]
		elif 'p_a' in sys.argv:
			merged = seq_descriptors[key] + ACC_descriptors[key]
		elif 'c_a' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key]
		elif '_p_' in sys.argv:
			merged = seq_descriptors[key]
		elif '_c_' in sys.argv:
			merged = comp_descriptors[key]
		elif '_nn_' in sys.argv:
			merged = nn_descriptors[key]	
		elif 'p_nn' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key]				
		elif '_a_' in sys.argv:		
			merged = ACC_descriptors[key]
		elif 'p_c_a_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		test_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			test_out.write("%f," % merged[var_i])
		test_out.write("%f,%s\n" % (merged[-1],activity[key]))

#-------------------------------------------------------------------------> CLASSIFICATION <------------------------------------------------------------------
def write_R_train_class():
	train_out = open("class_train_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		train_out.write("var.%d," % (var+1))
	train_out.write("%s\n" % "activity")
	for key in Training_All.keys():
		if 'p_c_a' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key]
		elif 'p_c' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key]
		elif 'p_a' in sys.argv:
			merged = seq_descriptors[key] + ACC_descriptors[key]
		elif 'c_a' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key]
		elif '_p_' in sys.argv:
			merged = seq_descriptors[key]
		elif '_nn_' in sys.argv:
			merged = nn_descriptors[key]
		elif 'p_nn' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key]					
		elif '_c_' in sys.argv:
			merged = comp_descriptors[key]
		elif '_a_' in sys.argv:	
			merged = ACC_descriptors[key]
		elif 'p_c_a_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]	
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		train_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			train_out.write("%f," % merged[var_i])
		train_out.write("%f,%s\n" % (merged[-1],activity_class[key]))
	

def write_R_test_class():
	test_out = open("class_test_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		#print "var.%d," % (var+1),
		test_out.write("var.%d," % (var+1))
	test_out.write("%s\n" % "activity")
	for key in Testing_All.keys():
		if 'p_c_a' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key]
		elif 'p_c' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key]
		elif 'p_a' in sys.argv:
			merged = seq_descriptors[key] + ACC_descriptors[key]
		elif 'c_a' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key]
		elif '_p_' in sys.argv:
			merged = seq_descriptors[key]
		elif '_nn_' in sys.argv:
			merged = nn_descriptors[key]
		elif 'p_nn' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key]					
		elif '_c_' in sys.argv:
			merged = comp_descriptors[key]
		elif '_a_' in sys.argv:		
			merged = ACC_descriptors[key]
		elif 'p_c_a_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		test_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			test_out.write("%f," % merged[var_i])
		test_out.write("%f,%s\n" % (merged[-1],activity_class[key]))

def write_R_test_predict_class():
	test_out = open("class_PredictionTest_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		test_out.write("var.%d," % (var+1))
	test_out.write("%s\n" % "activity")
	for key in pfred_seq2pred_name:
		if 'p_c_a' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key]
		elif 'p_c' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key]
		elif 'p_a' in sys.argv:
			merged = seq_descriptors[key] + ACC_descriptors[key]
		elif 'c_a' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key]
		elif '_p_' in sys.argv:
			merged = seq_descriptors[key]
		elif '_nn_' in sys.argv:
			merged = nn_descriptors[key]
		elif 'p_nn' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key]
		elif '_c_' in sys.argv:
			merged = comp_descriptors[key]
		elif '_a_' in sys.argv:		
			merged = ACC_descriptors[key]
		elif 'p_c_a_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		test_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			test_out.write("%f," % merged[var_i])
		test_out.write("%f,%s\n" % (merged[-1],activity_class[key]))
	
		
		

#-----------------------------------------------------------> RUNNING R  <------------------------------------------------------------------------
def run_stats(mode,model_type):
	if model_type == "regression":
		if 'build' in sys.argv:
			csv_file = "train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",")
			f_in = open(csv_file,"r")
			raw_header = string.strip(f_in.readline())
			header = raw_header.split(",")
			names = []
			act = {}
			descriptors = {}
			for line in f_in.readlines():
				nline = string.strip(line)
				tokens = nline.split(",")
				names.append(tokens[0])
				act[tokens[0]] = tokens[-1]
				tmp_list = tokens[1:-1]
				descriptors[tokens[0]] = tmp_list
			t1_build = open("t1_build.txt","w")
			for label in range(len(header)-2):
				t1_build.write("%s," % header[label])
			t1_build.write("%s\n" % header[-2])
			for key in names:
				tmp_list = descriptors[key]
				t1_build.write("%s," % key)
				for idx in range(len(tmp_list)-1):
					t1_build.write("%s," % tmp_list[idx])
				t1_build.write("%s\n" % tmp_list[-1])
			t1_build.close()
			t1_build_in = "t1_build.txt"
			t1_build_table = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (t1_build_in), head=r.TRUE, sep=",")
			os.system("rm t1_build.txt")	
			
	
		elif 'validate' in sys.argv:
			csv_file = "train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
			csv_file_ext = "test_%svars.csv" % (lenght_descriptors)
			ext_pred_file = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file_ext), head=r.TRUE, sep=",") 
			f_in = open(csv_file_ext,"r")
			raw_header = string.strip(f_in.readline())
			header = raw_header.split(",")
			names = []
			descriptors = {}
			act = {}
			for line in f_in.readlines():
				nline = string.strip(line)
				tokens = nline.split(",")
				names.append(tokens[0])
				act[tokens[0]] = tokens[-1]
				tmp_list = tokens[1:-1]
				descriptors[tokens[0]] = tmp_list
			t1 = open("t1.txt","w")
			for label in range(len(header)-2):
				t1.write("%s," % header[label])
			t1.write("%s\n" % header[-2])
			for key in names:
				tmp_list = descriptors[key]
				t1.write("%s," % key)
				for idx in range(len(tmp_list)-1):
					t1.write("%s," % tmp_list[idx])
				t1.write("%s\n" % tmp_list[-1])
			t1.close()
			t1_in = "t1.txt"
			t1_table = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (t1_in), head=r.TRUE, sep=",")
			os.system("rm t1.txt")
		elif 'predict' in sys.argv:
			csv_file = "train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
			csv_file_ext = "PredictionTest_%svars.csv" % (lenght_descriptors)
			ext_pred_file = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file_ext), head=r.TRUE, sep=",") 
			f_in = open(csv_file_ext,"r")
			raw_header = string.strip(f_in.readline())
			header = raw_header.split(",")
			names = []
			descriptors = {}
			act = {}
			for line in f_in.readlines():
				nline = string.strip(line)
				tokens = nline.split(",")
				names.append(tokens[0])
				act[tokens[0]] = "0.00" #exp value is not known
				tmp_list = tokens[1:-1]
				descriptors[tokens[0]] = tmp_list
			t1 = open("t1.txt","w")
			for label in range(len(header)-2):
				t1.write("%s," % header[label])
			t1.write("%s\n" % header[-2])
			for key in names:
				tmp_list = descriptors[key]
				t1.write("%s," % key)
				for idx in range(len(tmp_list)-1):
					t1.write("%s," % tmp_list[idx])
				t1.write("%s\n" % tmp_list[-1])
			t1.close()
			t1_in = "t1.txt"
			t1_table = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (t1_in), head=r.TRUE, sep=",")
			os.system("rm t1.txt")

	if model_type == "classification":
		if 'build' in sys.argv:
			csv_file = "class_train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",")
			f_in = open(csv_file,"r")
			raw_header = string.strip(f_in.readline())
			header = raw_header.split(",")
			names = []
			act = {}
			descriptors = {}
			for line in f_in.readlines():
				nline = string.strip(line)
				tokens = nline.split(",")
				names.append(tokens[0])
				act[tokens[0]] = tokens[-1]
				tmp_list = tokens[1:-1]
				descriptors[tokens[0]] = tmp_list
			t1_build = open("t1_build.txt","w")
			for label in range(len(header)-2):
				t1_build.write("%s," % header[label])
			t1_build.write("%s\n" % header[-2])
			for key in names:
				tmp_list = descriptors[key]
				t1_build.write("%s," % key)
				for idx in range(len(tmp_list)-1):
					t1_build.write("%s," % tmp_list[idx])
				t1_build.write("%s\n" % tmp_list[-1])
			t1_build.close()
			t1_build_in = "t1_build.txt"
			t1_build_table = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (t1_build_in), head=r.TRUE, sep=",")
			os.system("rm t1_build.txt")	
			
	
		elif 'validate' in sys.argv:
			csv_file = "class_train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
			csv_file_ext = "class_test_%svars.csv" % (lenght_descriptors)
			ext_pred_file = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file_ext), head=r.TRUE, sep=",") 
			f_in = open(csv_file_ext,"r")
			raw_header = string.strip(f_in.readline())
			header = raw_header.split(",")
			names = []
			descriptors = {}
			act = {}
			for line in f_in.readlines():
				nline = string.strip(line)
				tokens = nline.split(",")
				names.append(tokens[0])
				act[tokens[0]] = tokens[-1]
				tmp_list = tokens[1:-1]
				descriptors[tokens[0]] = tmp_list
			t1 = open("t1.txt","w")
			for label in range(len(header)-2):
				t1.write("%s," % header[label])
			t1.write("%s\n" % header[-2])
			for key in names:
				tmp_list = descriptors[key]
				t1.write("%s," % key)
				for idx in range(len(tmp_list)-1):
					t1.write("%s," % tmp_list[idx])
				t1.write("%s\n" % tmp_list[-1])
			t1.close()
			t1_in = "t1.txt"
			t1_table = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (t1_in), head=r.TRUE, sep=",")
			os.system("rm t1.txt")
		elif 'predict' in sys.argv:
			csv_file = "class_train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
			csv_file_ext = "class_PredictionTest_%svars.csv" % (lenght_descriptors)
			ext_pred_file = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file_ext), head=r.TRUE, sep=",") 
			f_in = open(csv_file_ext,"r")
			raw_header = string.strip(f_in.readline())
			header = raw_header.split(",")
			names = []
			descriptors = {}
			act = {}
			for line in f_in.readlines():
				nline = string.strip(line)
				tokens = nline.split(",")
				names.append(tokens[0])
				act[tokens[0]] = "0.00" #exp value is not known
				tmp_list = tokens[1:-1]
				descriptors[tokens[0]] = tmp_list
			t1 = open("t1.txt","w")
			for label in range(len(header)-2):
				t1.write("%s," % header[label])
			t1.write("%s\n" % header[-2])
			for key in names:
				tmp_list = descriptors[key]
				t1.write("%s," % key)
				for idx in range(len(tmp_list)-1):
					t1.write("%s," % tmp_list[idx])
				t1.write("%s\n" % tmp_list[-1])
			t1.close()
			t1_in = "t1.txt"
			t1_table = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (t1_in), head=r.TRUE, sep=",")
			os.system("rm t1.txt")	
	
						
	if mode == "1":	
		pls_regression_cross_validation(train) #correspond to "build" option for PLS
	
	elif mode == "2":
		if 'validate' in sys.argv:
			pls_regression_ext_validation(train,ext_pred_file,act,names,"validate")
		elif 'predict' in sys.argv:
			pls_regression_ext_validation(train,ext_pred_file,act,names,"predict")
	
	elif mode == "3":
		svm_tune_parameters()
	
	elif mode == "4":
		if 'validate' in sys.argv:
			svm_regression(train,ext_pred_file,act,"validate")
		elif 'predict' in sys.argv:
			svm_regression(train,ext_pred_file,act,"predict")
		elif 'build' in sys.argv:
			svm_regression(train,train,act,"build") #self-consistency validation (fitting)
	
	elif mode == "5":
		if 'validate' in sys.argv:
			svm_classification(train,ext_pred_file,act,"validate")
		elif 'predict' in sys.argv:
			svm_classification(train,ext_pred_file,act,"predict")
		elif 'build' in sys.argv:
			svm_classification(train,train,act,"build") #self-consistency validation (fitting)
	
	elif mode == "6": 
		if 'validate' in sys.argv:
			rf_regression(train,t1_table,act,"validate")
		elif 'predict' in sys.argv:
			rf_regression(train,t1_table,act,"predict")
		elif 'build' in sys.argv:
			rf_regression(train,t1_build_table,act,"build") #self-consistency validation (fitting)

	elif mode == "7":
		if 'validate' in sys.argv:
			rf_classification(train,t1_table,act,"validate")
		elif 'predict' in sys.argv:
			rf_classification(train,t1_table,act,"predict")
		elif 'build' in sys.argv:
			rf_classification(train,t1_build_table,act,"build") #self-consistency validation (fitting)
	
	elif mode == "8":
		pls_regression_varSelection_extValidation(csv_file_ext)
	
	elif mode == "9":
		pls_regression_varSelection_extValidation_NULL(csv_file_ext)
	
	
	 ##########
#------->#  MAIN  #<-------#
	 ##########

if sys.argv[1] == 'help' or sys.argv[1] == '-help' or sys.argv[1] == '--help' or sys.argv[1] == '':
	pass

elif sys.argv[1] == 'novartis':
	novartis_data(sys.argv[2])
	if 'predict' in sys.argv:
		seq2predict(sys.argv[5])
	global lenght_descriptors
	if 'p_c_a' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition']) + int(lenghts['acc'])
	elif 'p_c' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition'])
	elif 'p_a' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_acc(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['acc'])
	elif 'c_a' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS)
		lenght_descriptors = int(lenghts['composition']) + int(lenghts['acc'])
	elif '_p_' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions'])
	elif '_nn_' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_NNpositions(SeQuEnCeS)
		lenght_descriptors = int(lenghts['NNpositions'])	
	elif 'p_nn' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_NNpositions(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['NNpositions'])	
	elif '_c_' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		lenght_descriptors = int(lenghts['composition'])
	elif '_a_' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_acc(SeQuEnCeS)
		lenght_descriptors = int(lenghts['acc'])
	elif 'p_c_a_thermo' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS)
		thermodynamic(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition']) + int(lenghts['acc']) + int(lenghts['thermoDy'])
	elif 'p_c_a_nn_thermo' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_NNpositions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS)
		thermodynamic(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['NNpositions']) + int(lenghts['composition']) + int(lenghts['acc']) + int(lenghts['thermoDy'])
	elif 'thermo' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		thermodynamic(SeQuEnCeS)
		lenght_descriptors = int(lenghts['thermoDy'])
	elif 'p_c_thermo' in sys.argv:
		reynolds_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		thermodynamic(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition']) + int(lenghts['thermoDy'])
	if 'build' in sys.argv:
		write_R_train()
		write_R_train_class()
		if sys.argv[5] == "1": #PLS
			print "\n\n###  PLS REGRESSION ###"
			run_stats(sys.argv[5],"regression")
			print "\n\n###  PLS CLASSIFICATION ###"
			run_stats(sys.argv[5],"classification")
		elif sys.argv[5] == "4": #SVM regression
			run_stats(sys.argv[5],"regression")
		elif sys.argv[5] == "5": #SVM classification
			run_stats(sys.argv[5],"classification")
		elif sys.argv[5] == "6": #RF regression
			run_stats(sys.argv[5],"regression")
		elif sys.argv[5] == "7": #RF classification
			run_stats(sys.argv[5],"classification")

	elif 'validate' in sys.argv:
		write_R_train()
		write_R_test()
		write_R_train_class()
		write_R_test_class()
		if sys.argv[5] == "2": 
			print "\n\n###  PLS REGRESSION ###"
			run_stats(sys.argv[5],"regression")
			print "\n\n###  PLS CLASSIFICATION ###"
			run_stats(sys.argv[5],"classification")
		elif sys.argv[5] == "4": 
			run_stats(sys.argv[5],"regression")
		elif sys.argv[5] == "5": 
			run_stats(sys.argv[5],"classification")
		elif sys.argv[5] == "6": 
			run_stats(sys.argv[5],"regression")
		elif sys.argv[5] == "7": 
			run_stats(sys.argv[5],"classification")

	elif 'predict' in sys.argv:
		write_R_train()
		write_R_test_predict()
		write_R_train_class()
		write_R_test_predict_class()
		#run_stats("2","regression")	
		run_stats("4","regression")	
		#run_stats("5","classification")
		#run_stats("6","regression")	
		run_stats("8","regression")	



		
		if len(activity2predict_TAG) == 1: #the external file of sequences does not contain activity values
			PrEdIcTiOn = open("OuTpUt_ReSuLtS.csv", "w")
			PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("siRNA_id","guide_strand_seq",
							"SVMpred","PLS_InHouse",
							"AAAAA","CCCCC","GGGGG","UUUUU","G:C_content",
							"Reynolds_rule1","Reynolds_rule2","Reynolds_rule3","Reynolds_rule4","Reynolds_rule5","Reynolds_rule6","Reynolds_rule7","Reynolds_rule8","ReynoldsScore",
							"dH","dS","dG","Tm",
							#"dES",
							"AIS",
							"ddG_18_1","ddG_18_10","ddG_1_13",
							"dG1","dG2","dG3","dG4","dG5","dG6","dG7","dG8","dG9","dG10","dG11","dG12","dG13","dG14","dG15","dG16","dG17","dG18"))
			for key in svm_regression_results.keys():
				PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (key,SeQuEnCeS[key],#name
							svm_regression_results[key],pls_regression_varSelection_results[key],						
							stretches[key][0],stretches[key][1],stretches[key][2],stretches[key][3],reynolds_score[key][1],                     #AAAAAstretch, CCCCCstretch, GGGGGstretch, UUUUUstretch, G/C content
							reynolds_score[key][2],reynolds_descriptors[key][1],reynolds_descriptors[key][2],reynolds_descriptors[key][3],reynolds_descriptors[key][4],reynolds_descriptors[key][5],reynolds_descriptors[key][6],reynolds_descriptors[key][7],
							reynolds_score[key][0],
							Thermo_descriptors[key][0],Thermo_descriptors[key][1],Thermo_descriptors[key][2],Thermo_descriptors[key][3],#DeltaH, DeltaS, DeltaG, Tm, 
							Thermo_descriptors[key][35], #AverageInternalStability
							Thermo_descriptors[key][4],Thermo_descriptors[key][15],Thermo_descriptors[key][16],	#dDG(18-1),dDG(18-10),dDG(1-13)
							Thermo_descriptors[key][17],Thermo_descriptors[key][18],Thermo_descriptors[key][19],Thermo_descriptors[key][20],Thermo_descriptors[key][21], #DG profile
							Thermo_descriptors[key][22],Thermo_descriptors[key][23],Thermo_descriptors[key][24],Thermo_descriptors[key][25],Thermo_descriptors[key][26], #DG profile
							Thermo_descriptors[key][27],Thermo_descriptors[key][28],Thermo_descriptors[key][29],Thermo_descriptors[key][30],Thermo_descriptors[key][31], #DG profile
							Thermo_descriptors[key][32],Thermo_descriptors[key][33],Thermo_descriptors[key][34])) 							     #DG profile
			PrEdIcTiOn.close()
		elif len(activity2predict_TAG) == 2: #the external file of sequences contain activity values
			PrEdIcTiOn = open("OuTpUt_ReSuLtS_ExpActivityPlus.csv", "w")
			PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("siRNA_id","exp_activity",
							"SVMpred","PLS_InHouse",
							"AAAAA","CCCCC","GGGGG","UUUUU","G:C_content",
							"Reynolds_rule1","Reynolds_rule2","Reynolds_rule3","Reynolds_rule4","Reynolds_rule5","Reynolds_rule6","Reynolds_rule7","Reynolds_rule8","ReynoldsScore",
							"dH","dS","dG","Tm",
							#"dES",
							"AIS",
							"ddG_18_1","ddG_18_10","ddG_1_13",
							"dG1","dG2","dG3","dG4","dG5","dG6","dG7","dG8","dG9","dG10","dG11","dG12","dG13","dG14","dG15","dG16","dG17","dG18"))
			for key in svm_regression_results.keys():
				PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (key,activity[key],#name,exp_activity
							svm_regression_results[key],pls_regression_varSelection_results[key],
							stretches[key][0],stretches[key][1],stretches[key][2],stretches[key][3],reynolds_score[key][1], 	#AAAAAstretch, CCCCCstretch, GGGGGstretch, UUUUUstretch, G/C content
							reynolds_score[key][2],reynolds_descriptors[key][1],reynolds_descriptors[key][2],reynolds_descriptors[key][3],reynolds_descriptors[key][4],reynolds_descriptors[key][5],reynolds_descriptors[key][6],reynolds_descriptors[key][7],
							reynolds_score[key][0],
							Thermo_descriptors[key][0],Thermo_descriptors[key][1],Thermo_descriptors[key][2],Thermo_descriptors[key][3],#DeltaH, DeltaS, DeltaG, Tm, 
							Thermo_descriptors[key][35], #AverageInternalStability
							Thermo_descriptors[key][4],Thermo_descriptors[key][15],Thermo_descriptors[key][16],	#dDG(18-1),dDG(18-10),dDG(1-13)
							Thermo_descriptors[key][17],Thermo_descriptors[key][18],Thermo_descriptors[key][19],Thermo_descriptors[key][20],Thermo_descriptors[key][21], #DG profile
							Thermo_descriptors[key][22],Thermo_descriptors[key][23],Thermo_descriptors[key][24],Thermo_descriptors[key][25],Thermo_descriptors[key][26], #DG profile
							Thermo_descriptors[key][27],Thermo_descriptors[key][28],Thermo_descriptors[key][29],Thermo_descriptors[key][30],Thermo_descriptors[key][31], #DG profile
							Thermo_descriptors[key][32],Thermo_descriptors[key][33],Thermo_descriptors[key][34])) 							     #DG profile
			PrEdIcTiOn.close()
		


		
os.system("rm -f train_*vars.csv test_*vars.csv PredictionTest_*vars.csv class_train_*vars.csv class_test_*vars.csv class_PredictionTest_*vars.csv")		
					
