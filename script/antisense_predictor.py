#!/usr/bin/env python
#
from antisense_descriptors import *
from antisense_load_dataset import *
from antisense_stats import *

	 ###############
#------->#  FUNCTIONS  #<-------#
	 ###############
#-----------------------------------------------------------------------> WRITING R FILES <---------------------------------------------------------------
#-------------------------------------------------------------------------> REGRESSION <------------------------------------------------------------------
def write_R_train():
	train_out = open("train_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		#print "var.%d," % (var+1),
		train_out.write("var.%d," % (var+1))
	#print "%s" % "activity"
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
		elif 'c_a_thermo' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]			
		#print "%s," % key,
		train_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			train_out.write("%f," % merged[var_i])
		#print "%f, %s" % (merged[-1],activity[key])
		train_out.write("%f,%s\n" % (merged[-1],activity[key]))
	

def write_R_test():
	test_out = open("test_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		#print "var.%d," % (var+1),
		test_out.write("var.%d," % (var+1))
	#print "%s" % "activity"
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
		elif 'c_a_thermo' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]	
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		#print "%s," % key,
		test_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			test_out.write("%f," % merged[var_i])
		#print "%f, %s" % (merged[-1],activity[key])
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
		elif 'c_a_thermo' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
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
		#print "var.%d," % (var+1),
		train_out.write("var.%d," % (var+1))
	#print "%s" % "activity"
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
		elif 'c_a_thermo' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]	
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		#print "%s," % key,
		train_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			train_out.write("%f," % merged[var_i])
		#print "%f, %s" % (merged[-1],activity_class[key])
		train_out.write("%f,%s\n" % (merged[-1],activity_class[key]))
	

def write_R_test_class():
	test_out = open("class_test_%svars.csv" % (lenght_descriptors), "w")
	for var in range(lenght_descriptors):
		#print "var.%d," % (var+1),
		test_out.write("var.%d," % (var+1))
	#print "%s" % "activity"
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
		elif 'c_a_thermo' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'p_c_a_nn_thermo' in sys.argv:
			merged = seq_descriptors[key] + nn_descriptors[key] + comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
		elif 'thermo' in sys.argv:
			merged = Thermo_descriptors[key]
		elif 'p_c_thermo' in sys.argv:
			merged = seq_descriptors[key] + comp_descriptors[key] + Thermo_descriptors[key]						
		#print "%s," % key,
		test_out.write("%s," % key)
		for var_i in range(len(merged)-1):
			#print "%f," % merged[var_i],
			test_out.write("%f," % merged[var_i])
		#print "%f, %s" % (merged[-1],activity_class[key])
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
		elif 'c_a_thermo' in sys.argv:
			merged = comp_descriptors[key] + ACC_descriptors[key] + Thermo_descriptors[key]
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
	"""
	Possible Algoritms:
	"                     PLS (Model building and cross-validation) : 1	ok
	"                     PLS   		       (Ext_Prediciton) : 2	ok
	"                     SVM  		      (Tune Parameters) : 3	
	"                     SVM                          (Regression) : 4	ok
	"                     SVM                      (Classification) : 5	ok
	"                      RF                          (Regression) : 6	ok
	"                      RF                      (Classification) : 7	ok
	"""
	if model_type == "regression":
		if 'build' in sys.argv:
			#-->training set
			csv_file = "train_%svars.csv" % (lenght_descriptors)
			#csv_file = sys.argv[1]
			"""the trick is to use header=TRUE and the first row must contains one fewer field than the number of columns, 
   			in this way the first column in the input is used for the row names"""
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
			#Creating X-block(t1_build) file necessary for RF analysis
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
			#-->training set
			csv_file = "train_%svars.csv" % (lenght_descriptors)
			"""the trick is to use header=TRUE and the first row must contains one fewer field than the number of columns, 
   			in this way the first column in the input is used for the row names"""
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
                                                                                                                                                                               
			#-->test set											
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
			#Creating X-block(t1) file necessary for RF analysis
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
			#-->training set
			csv_file = "train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
                                                                                                                                                                               
			#-->test set											
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
			#Creating X-block(t1) file necessary for RF analysis
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
			#-->training set
			csv_file = "class_train_%svars.csv" % (lenght_descriptors)
			#csv_file = sys.argv[1]
			"""the trick is to use header=TRUE and the first row must contains one fewer field than the number of columns, 
   			in this way the first column in the input is used for the row names"""
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
			#Creating X-block(t1_build) file necessary for RF analysis
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
			#-->training set
			csv_file = "class_train_%svars.csv" % (lenght_descriptors)
			"""the trick is to use header=TRUE and the first row must contains one fewer field than the number of columns, 
   			in this way the first column in the input is used for the row names"""
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
                                                                                                                                                                               
			#-->test set											
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
			#Creating X-block(t1) file necessary for RF analysis
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
			#-->training set
			csv_file = "class_train_%svars.csv" % (lenght_descriptors)
			train = with_mode(NO_CONVERSION, r.read_table)(file="%s" % (csv_file), head=r.TRUE, sep=",") 
                                                                                                                                                                               
			#-->test set											
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
			#Creating X-block(t1) file necessary for RF analysis
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
	
						
	#Different algorithm options
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
		pls_regression_varSelection_extValidation__15_21(csv_file_ext)
	
	elif mode == "9":
		pls_regression_varSelection_extValidation__20_20(csv_file_ext)
	
	elif mode == "10":
		pls_regression_varSelection_extValidation_NULL(csv_file_ext)
	
	


	 ##########
#------->#  MAIN  #<-------#
	 ##########

if len(sys.argv) == 1 or sys.argv[1] == 'help' or sys.argv[1] == '-help' or sys.argv[1] == '--help':
	print
	print "Usage:"
	print "         ............................................................."
	print
	print
	print "In general when running the classification models, one should be sure of the"
	print "activity cut-off he wants to use in order to classify antisense in the training set"
	print "The threshold is set in the load_dataset.py file"
	print
	print
	print "################"
	print "#Model building#"
	print "################"
	print "#--->PLS  --> OK (You get the CV results for both Regression and Classification)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo build 1 < input.txt"
	print "#--->SVM  --> OK (regression, you get the pearson for fitting)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo build 4 < input.txt"
	print "#--->SVM  --> OK (classification, you get the confusion matrix for fitting)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo build 5 < input.txt"
	print "#--->RF   --> OK (regression, you get the pearson for fitting)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo build 6 < input.txt"
	print "#--->RF   --> OK (classification, you get the confusion matrix for fitting)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo build 7 < input.txt"
	print 
	print 
	print "#####################"
	print "#External validation# (assume you want to do an external validation on the novartis testset)"
	print "#####################"
	print "#--->PLS  --> OK  (You get both the prediction results for Regression and Classification using the ext test set)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo validate 2 < input.txt"
	print "#--->SVM  --> OK (regression, you get the pearson for the ext prediction)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo validate 4 < input.txt"
	print "#--->SVM  --> OK (classification, you get the confusion matrix for the ext prediction)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo validate 5 < input.txt"
	print "#--->RF  -->  OK (regression, you get the pearson for the ext prediction)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo validate 6 < input.txt"
	print "#--->RF  -->  OK (classification, you get the confusion matrix for the ext prediction)"
	print "./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv p_c_a_thermo validate 7 < input.txt"
	print
	print
	print "#####################"
	print "#External prediction# from FRED (gives back SVMregress+PLSregress)"
	print "#####################"
	print "time ./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv c_a_thermo predict pfred_sequences_plusActivity.csv < input.txt"
	print "time ./antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009.csv c_a_thermo predict pfred_sequences.csv < input.txt"
	print 
	print 
	print "###########"
	print "#Debugging#"
	print "###########"
	print "#./antisense_predictor.py debug AOBase_542seq_cleaned_modelBuilding_Jan2009.csv [fred_sequences.csv] < input.txt "
	print


elif sys.argv[1] == 'AOBase':
	min_len=input("min_len:")
	max_len=input("max_len:")
	min_conc=input("min_conc:")
	max_conc=input("max_conc:")
	max_acc_lag = input("max_acc_lag:")
	
	AOBase_data(sys.argv[2],min_len,max_len,min_conc,max_conc)
	if 'predict' in sys.argv:
		seq2predict(sys.argv[5])
	#------>Calling different functions
	global lenght_descriptors
	if 'p_c_a' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS,max_acc_lag)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition']) + int(lenghts['acc'])
	elif 'p_c' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition'])
	elif 'p_a' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_acc(SeQuEnCeS,max_acc_lag)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['acc'])
	elif 'c_a' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS,max_acc_lag)
		lenght_descriptors = int(lenghts['composition']) + int(lenghts['acc'])
	elif '_p_' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions'])
	elif '_nn_' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_NNpositions(SeQuEnCeS)
		lenght_descriptors = int(lenghts['NNpositions'])	
	elif 'p_nn' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_NNpositions(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['NNpositions'])	
	elif '_c_' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		lenght_descriptors = int(lenghts['composition'])
	elif '_a_' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_acc(SeQuEnCeS,max_acc_lag)
		lenght_descriptors = int(lenghts['acc'])
	elif 'p_c_a_thermo' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS,max_acc_lag)
		thermodynamic_rnadna(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition']) + int(lenghts['acc']) + int(lenghts['thermoDy'])
	elif 'c_a_thermo' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS,max_acc_lag)
		thermodynamic_rnadna(SeQuEnCeS)
		lenght_descriptors = int(lenghts['composition']) + int(lenghts['acc']) + int(lenghts['thermoDy'])
	elif 'p_c_a_nn_thermo' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_NNpositions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		sequence_acc(SeQuEnCeS,max_acc_lag)
		thermodynamic_rnadna(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['NNpositions']) + int(lenghts['composition']) + int(lenghts['acc']) + int(lenghts['thermoDy'])
	elif 'thermo' in sys.argv:
		quality_filter(SeQuEnCeS)
		thermodynamic_rnadna(SeQuEnCeS)
		lenght_descriptors = int(lenghts['thermoDy'])
	elif 'p_c_thermo' in sys.argv:
		quality_filter(SeQuEnCeS)
		sequence_positions(SeQuEnCeS)
		sequence_composition(SeQuEnCeS)
		thermodynamic_rnadna(SeQuEnCeS)
		lenght_descriptors = int(lenghts['positions']) + int(lenghts['composition']) + int(lenghts['thermoDy'])
	#Creating input files for R and then running R
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
		if sys.argv[5] == "2": #PLS
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

	elif 'predict' in sys.argv:
		write_R_train()
		write_R_test_predict()
		write_R_train_class()
		write_R_test_predict_class()
		run_stats("2","regression") 	#PLSr
		run_stats("4","regression")  	#SVMr
		#run_stats("5","classification") #SVMc
		#run_stats("6","regression")	#RFr
		if "_15_21_" in sys.argv[2]:
			run_stats("8","regression")  
		elif "_20_20_" in sys.argv[2]:
			run_stats("9","regression") 
		else:
			run_stats("10","regression") 
		
		if len(activity2predict_TAG) == 1: #the external file of sequences does not contain activity values
			PrEdIcTiOn = open("OuTpUt_ReSuLtS.csv", "w")
			PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("siRNA_id","antisense_strand__5_3","SVMpred","PLSpred","PLSpred_optimized","dG","Tm","G/C","AAAAA","CCCCC","GGGGG","TTTTT","SS1"))
			for key in svm_regression_results.keys():
				PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (key,SeQuEnCeS[key],svm_regression_results[key],pls_regression_results[key],pls_regression_varSelection_results[key],
												Thermo_descriptors[key][2],Thermo_descriptors[key][3],quality_descriptors[key][0],
												quality_descriptors[key][1],quality_descriptors[key][2],quality_descriptors[key][3],quality_descriptors[key][4],quality_descriptors[key][5])) 	
			PrEdIcTiOn.close()
				
		elif len(activity2predict_TAG) == 2: #the external file of sequences contain activity values
			PrEdIcTiOn = open("OuTpUt_ReSuLtS_ExpActivityPlus.csv", "w")
			PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("siRNA_id","antisense_strand__5_3","SVMpred","PLSpred","PLSpred_optimized","exp_activity","dG","Tm","G/C","AAAAA","CCCCC","GGGGG","TTTTT","SS1"))
			for key in svm_regression_results.keys():
				PrEdIcTiOn.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (key,SeQuEnCeS[key],svm_regression_results[key],pls_regression_results[key],pls_regression_varSelection_results[key],activity[key],
												Thermo_descriptors[key][2],Thermo_descriptors[key][3],quality_descriptors[key][0],
												quality_descriptors[key][1],quality_descriptors[key][2],quality_descriptors[key][3],quality_descriptors[key][4],quality_descriptors[key][5]))
			PrEdIcTiOn.close()


elif sys.argv[1] == 'debug':
	min_len=input("min_len:")
	max_len=input("max_len:")
	min_conc=input("min_conc:")
	max_conc=input("max_conc:")
	max_acc_lag = input("max_acc_lag:")
	
	AOBase_data(sys.argv[2],min_len,max_len,min_conc,max_conc)

	if len(sys.argv) > 3:
		seq2predict(sys.argv[3])
	
	######################################
	#-->Testing out different descriptors#
	######################################
	
	sequence_positions(SeQuEnCeS)
	for key in seq_descriptors.keys():
		print key, seq_descriptors[key]
	
	#sequence_NNGpositions(SeQuEnCeS)
	#for key in nnG_descriptors.keys():
	#	merge_out = ""
	#	for j in range(len(nnG_descriptors[key])):
	#		merge_out += str(nnG_descriptors[key][j])
	#	print key,"\t",merge_out	
	
	#sequence_composition(SeQuEnCeS)
	#for key in comp_descriptors.keys():
		#print key, comp_descriptors[key]
	
	#sequence_acc(SeQuEnCeS,max_acc_lag)
	#for key in ACC_descriptors.keys():
		#print key, ACC_descriptors[key]
	
	#thermodynamic_rnadna(SeQuEnCeS)
	#for key in Thermo_descriptors.keys():
	#	print key, SeQuEnCeS[key], Thermo_descriptors[key][3] #Tm
	pass

os.system("rm -f train_*vars.csv test_*vars.csv PredictionTest_*vars.csv class_train_*vars.csv class_test_*vars.csv class_PredictionTest_*vars.csv antisense_stats.pyc antisense_load_dataset.pyc antisense_descriptors.pyc")		
