#!/usr/bin/env python
#
# Statistical Python Library
#
import string
import sys
from rpy import *
import numpy
r.library("randomForest") #import randomForest library in R
r.library("pls") #import pca library in R
r.library("e1071") #import pca library in R



def pls_regression_cross_validation(TRAINpls):
	#PLS MODEL BUILDING AND CROSS-VALIDATION
	model = r("activity ~ .")
	PLSfit = with_mode(NO_CONVERSION, r.plsr)(model,20,data=TRAINpls, scale=r.TRUE)
	#Add a plot for R2
	
	PLSval = with_mode(NO_CONVERSION, r.plsr)(model,20,data=TRAINpls,validation="CV", scale=r.TRUE)
	#---plot
	r.summary(PLSval)
	r.png("PLS_cv.png", width=400, height=350)
	r.plot(PLSval, "val")
	r.dev_off()
	#Add a plot for cross-validated R2

pls_regression_results = {}	
def pls_regression_ext_validation(TRAINpls,TESTpls,activity_dict,NAMES,output_type):	
	model = r("activity ~ .")
	#PLSfit = with_mode(NO_CONVERSION, r.plsr)(model,10,data=TRAINpls)
	PLSfit = with_mode(NO_CONVERSION, r.plsr)(model,10,data=TRAINpls, scale=r.TRUE)
	PLSpred = r.predict(PLSfit,TESTpls) #numpy_array
	#results
	pls_ext_pred_1 = {}
	pls_ext_pred_2 = {}
	pls_ext_pred_3 = {}
	pls_ext_pred_4 = {}
	pls_ext_pred_5 = {}
	pls_ext_pred_6 = {}
	pls_ext_pred_7 = {}
	pls_ext_pred_8 = {}
	pls_ext_pred_9 = {}
	pls_ext_pred_10 = {}
	for compd_id in range(len(PLSpred)):
		compd_i = PLSpred[compd_id,0,:] 
		pls_ext_pred_1[NAMES[compd_id]] = compd_i[0]#printing Pred_PC1,names
		pls_ext_pred_2[NAMES[compd_id]] = compd_i[1]#printing Pred_PC2,names
		pls_ext_pred_3[NAMES[compd_id]] = compd_i[2]#printing Pred_PC3,names
		pls_ext_pred_4[NAMES[compd_id]] = compd_i[3]#printing Pred_PC4,names
		pls_ext_pred_5[NAMES[compd_id]] = compd_i[4]#printing Pred_PC5,names
		pls_ext_pred_6[NAMES[compd_id]] = compd_i[5]#printing Pred_PC6,names
		pls_ext_pred_7[NAMES[compd_id]] = compd_i[6]#printing Pred_PC7,names
		pls_ext_pred_8[NAMES[compd_id]] = compd_i[7]#printing Pred_PC8,names
		pls_ext_pred_9[NAMES[compd_id]] = compd_i[8]#printing Pred_PC9,names
		pls_ext_pred_10[NAMES[compd_id]] = compd_i[9]#printing Pred_PC10,names
	name_objs = []
	pls_exp = []
	pls_pred_1 = []
	pls_pred_2 = []
	pls_pred_3 = []
	pls_pred_4 = []
	pls_pred_5 = []
	pls_pred_6 = []
	pls_pred_7 = []
	pls_pred_8 = []
	pls_pred_9 = []
	pls_pred_10 = []
	for key in activity_dict.keys():
		name_objs.append(key)
		pls_exp.append(activity_dict[key])
		pls_pred_1.append(pls_ext_pred_1[key])
		pls_pred_2.append(pls_ext_pred_2[key])
		pls_pred_3.append(pls_ext_pred_3[key])
		pls_pred_4.append(pls_ext_pred_4[key])
		pls_pred_5.append(pls_ext_pred_5[key])
		pls_pred_6.append(pls_ext_pred_6[key])
		pls_pred_7.append(pls_ext_pred_7[key])
		pls_pred_8.append(pls_ext_pred_8[key])
		pls_pred_9.append(pls_ext_pred_9[key])
		pls_pred_10.append(pls_ext_pred_10[key])
	if output_type == "validate":
		print pls_exp
		print "LV1", r.cor(pls_exp,pls_pred_1)
		print "LV2", r.cor(pls_exp,pls_pred_2)
		print "LV3", r.cor(pls_exp,pls_pred_3)
		print "LV4", r.cor(pls_exp,pls_pred_4)
		print "LV5", r.cor(pls_exp,pls_pred_5)
		print "LV6", r.cor(pls_exp,pls_pred_6)
		#print "LV7", r.cor(pls_exp,pls_pred_7)
		#print "LV8", r.cor(pls_exp,pls_pred_8)
		#print "LV9", r.cor(pls_exp,pls_pred_9)
		#print "LV10", r.cor(pls_exp,pls_pred_10)
		
		#-->print out the exp vs. pred for LV6
		print
		print "Exp vs Pred"
		for i in range(len(pls_exp)):
			print name_objs[i],"exp=",pls_exp[i],"pred_pc3=",pls_pred_3[i],"pred_pc4=",pls_pred_4[i],"pred_pc5=",pls_pred_5[i],"pred_pc6=",pls_pred_6[i]
		print
		
		#-->plot
		#r.png("PLS_ext_pred.png", width=400, height=350)
		#r.plot(pls_exp,pls_pred_6)
		#r.dev_off()
	elif output_type == "predict":
		#save in "pls_regression_results"  only predicition for the best component(LV6 using p_c_a_thermo)
		for key in pls_ext_pred_4.keys():
			pls_regression_results[key] = pls_ext_pred_4[key]
	
	
def svm_tune_parameters():
	"""
	formula = r("activity ~ .")
	SVMtune = with_mode(NO_CONVERSION, r.tune_svm)(formula,data=train, scale=r.TRUE, gamma = r.seq(0.5,4,by=0.5), cost = r.seq(4,100,by=5))
	print r.summary(SVMtune)
	"""
	pass
	

svm_regression_results = {}		
def svm_regression(TRAINsvm,TESTsvm,activity_dict,output_type):
	"""
	Important step in SVM to improve accuracy
	#
	# --> 1) Conduct simple scaling on the data
	# --> 2) Consider RBF kernel (Radial Basis Function) K(x,y) = e(-y||x-y||)2
	# --> 3) Use cross-validation to find the best parameter C and y(gamma)
	# --> 4) Use the best C and gamma to train the whole training set
	# --> 5) Test
	"""
	formula = r("activity ~ .")
	if output_type == "build":
		SVMfit = with_mode(NO_CONVERSION, r.svm)(formula,data=TRAINsvm, scale=r.TRUE)
		SVMself = with_mode(NO_CONVERSION, r.predict)(SVMfit,TRAINsvm)
		#SVMcv = with_mode(NO_CONVERSION, r.svm)(formula,data=TRAINsvm, scale=r.TRUE, cross=10)
		#Fitting
		calc_svm_act = []
		exp_svm_act = []
		for obj in SVMself:
			calc_svm_act.append(obj[obj.keys()[0]])
			exp_svm_act.append(activity_dict[obj.keys()[0]])
			print obj.keys()[0],"exp=",activity_dict[obj.keys()[0]],"pred=",obj[obj.keys()[0]]
		print
		print 
		print "SVM_pearson =", r.cor(exp_svm_act,calc_svm_act)		
		r.png("svm_model.png", width=400, height=350)
		r.plot(exp_svm_act,calc_svm_act)
		r.dev_off()
		#Cross-Validation
		#for obj in SVMfit:
			#print obj
		
	else:
		SVMfit = with_mode(NO_CONVERSION, r.svm)(formula,data=TRAINsvm, scale=r.TRUE)
		SVMpred = with_mode(NO_CONVERSION, r.predict)(SVMfit,TESTsvm)
		pred_svm_act = []
		exp_svm_act = []
		validate_test = 0
		for obj in SVMpred:
			pred_svm_act.append(obj[obj.keys()[0]])
			exp_svm_act.append(activity_dict[obj.keys()[0]])
			if output_type == "validate":
				svm_regression_results[obj.keys()[0]] = obj[obj.keys()[0]], activity_dict[obj.keys()[0]]
				print obj.keys()[0], "exp=", activity_dict[obj.keys()[0]], "pred=",obj[obj.keys()[0]]
				validate_test = 1
			elif output_type == "predict":
				svm_regression_results[obj.keys()[0]] = obj[obj.keys()[0]]
				#print obj.keys()[0], obj[obj.keys()[0]]
		if validate_test:
			print
			print "SVM_pearson =", r.cor(exp_svm_act,pred_svm_act)	
			print
			r.png("svm_ext_pred.png", width=400, height=350)
			r.plot(exp_svm_act,pred_svm_act)
			r.dev_off()
	
		

svm_classification_results = {}			
def svm_classification(TRAINsvm,TESTsvm,activity_dict,output_type):
	formula = r("factor(activity) ~ .")
	SVMfit = with_mode(NO_CONVERSION, r.svm)(formula,data=TRAINsvm, scale=r.TRUE)
	SVMself = with_mode(NO_CONVERSION, r.predict)(SVMfit,TRAINsvm)
	SVMpred = with_mode(NO_CONVERSION, r.predict)(SVMfit,TESTsvm)
	if output_type == "build":
		calc_svm_act = []
		exp_svm_act = []
		for obj in SVMself:
			calc_svm_act.append(obj[obj.keys()[0]])
			exp_svm_act.append(activity_dict[obj.keys()[0]])
			print obj.keys()[0],"exp=",activity_dict[obj.keys()[0]],"pred=",obj[obj.keys()[0]]
		print
		print "SVM_confusion =", r.table(exp_svm_act,calc_svm_act)		
		table_svm = r.table(exp_svm_act,calc_svm_act)
		print "SVM_kappa =", r.classAgreement(table_svm)
		print
	else:
		pred_svm_act = []
		exp_svm_act = []
		validate_test = 0
		for obj in SVMpred:
			pred_svm_act.append(obj[obj.keys()[0]])
			exp_svm_act.append(activity_dict[obj.keys()[0]])
			if output_type == "validate":
				svm_classification_results[obj.keys()[0]] = obj[obj.keys()[0]], activity_dict[obj.keys()[0]]
				print obj.keys()[0], "exp=", activity_dict[obj.keys()[0]], "pred=",obj[obj.keys()[0]]
				validate_test = 1
			elif output_type == "predict":
				svm_classification_results[obj.keys()[0]] = obj[obj.keys()[0]]
				#print obj.keys()[0], obj[obj.keys()[0]]
		if validate_test:
			print
			print "SVM_confusion =", r.table(exp_svm_act,pred_svm_act)
			table_svm = r.table(exp_svm_act,pred_svm_act)
			print "SVM_kappa =", r.classAgreement(table_svm)
			print
			

	
			
rf_regression_results = {}
def rf_regression(TRAINrf,TESTrf,activity_dict,output_type):
	model = r("activity ~ .")
	RFmod = r.randomForest(model,data=TRAINrf,xtest=TESTrf,scale=r.TRUE,ntree=5000) #5000 is more reliable but it takes longer
	#RF_MODEL_RESULTS
	if output_type == "build":
		internal_pred = RFmod['predicted']
		MSE = numpy.array(RFmod['mse'])
		RMSE = numpy.sqrt(MSE)
		Rsq = RFmod['rsq']	
		#print "MSE=", MSE
		#print "RMSE=",RMSE
		#print "Rsq", Rsq
		calc_rf_act = []
		exp_rf_act = []
		for key in internal_pred.keys():
			print key, "exp=", activity_dict[key], "pred=", internal_pred[key]
			calc_rf_act.append(internal_pred[key])
			exp_rf_act.append(activity_dict[key])
		print
		print "RF_pearson =", r.cor(exp_rf_act,calc_rf_act)	
		print
		r.png("rf_model.png", width=400, height=350)
		r.plot(exp_rf_act,calc_rf_act)
		r.dev_off()	
	#RF_EXT_PREDICTIONS	
	elif output_type == "validate":
		external_pred = RFmod['test']['predicted']
		pred_rfr_act = []
		exp_rfr_act = []
		for key in external_pred.keys():
			print key, activity_dict[key], external_pred[key]
			pred_rfr_act.append(external_pred[key])
			exp_rfr_act.append(activity_dict[key])
		print
		print "RF_regression_pearson =", r.cor(exp_rfr_act,pred_rfr_act)	
		print
		r.png("RF_ext_pred.png", width=400, height=350)
		r.plot(exp_rfr_act,pred_rfr_act)
		r.dev_off()
	elif output_type == "predict":
		external_pred = RFmod['test']['predicted']
		for key in external_pred.keys():
			rf_regression_results[key] = external_pred[key]
		

rf_classification_results = {}
def rf_classification(TRAINrf,TESTrf,activity_dict,output_type):
	model = r("factor(activity) ~ .")
	RFmod = r.randomForest(model,data=TRAINrf,xtest=TESTrf,scale=r.TRUE,ntree=5000) #5000 is more reliable but it takes longer
	#RF_MODEL_RESULTS
	if output_type == "build":
		internal_pred = RFmod['predicted']
		calc_rf_act = []
		exp_rf_act = []
		for key in internal_pred.keys():
			print key, "exp=", activity_dict[key], "pred=", internal_pred[key]
			calc_rf_act.append(internal_pred[key])
			exp_rf_act.append(activity_dict[key])
		print
		print "RF_confusion =", r.table(exp_rf_act,calc_rf_act)
		table_rf = r.table(exp_rf_act,calc_rf_act)
		print "RF_kappa =", r.classAgreement(table_rf)
		print	
	#RF_EXT_PREDICTIONS	
	elif output_type == "validate":
		external_pred = RFmod['test']['predicted']
		pred_rfr_act = []
		exp_rfr_act = []
		for key in external_pred.keys():
			print key, "exp=",activity_dict[key], "pred=",external_pred[key]
			pred_rfr_act.append(external_pred[key])
			exp_rfr_act.append(activity_dict[key])
		print
		print "RF_confusion =", r.table(exp_rfr_act,pred_rfr_act)
		table_rf = r.table(exp_rfr_act,pred_rfr_act)
		print "RF_kappa =", r.classAgreement(table_rf)
		print	
				
	elif output_type == "predict":
		external_pred = RFmod['test']['predicted']
		for key in external_pred.keys():
			rf_classification_results[key] = external_pred[key]
			


pls_regression_varSelection_results = {}	
def pls_regression_varSelection_extValidation__15_21(TESTpls):	
	#first value is the intercept, remaining values are the 208 descriptor's coefficients
	LV4_coefficients = (0.7735,0,0.004379,-0.00481,0.0006733,0,0.003745,0,-0.007869,0.005891,0.006537,0.002596,-0.004105,-0.0002237,0,-0.009596,0.006735,-0.02051,0.002801,0.0008511,0.003731,0,0,-0.02013,0,0,0,0,0.01552,0.02533,-0.02749,0,0,0,0,-0.02233,0,-0.04415,0,0,0.01261,0.04161,0,-0.03633,-0.006835,0.03508,0.01167,0,-0.04047,0,0,0,0.000188,0.01664,0,0.009901,-0.02576,0,-0.006481,0,0.02209,0,0.02103,-0.03058,0,0.00598,0,0,0,-0.03634,0,-0.03628,-0.0433,0,0.01328,0.05725,-0.02512,-0.0273,0,-0.02389,0.03251,-0.05052,-0.002221,0.02903,0,0,0.04214,0,0.02283,-0.02781,0.02939,0,0.02888,0,0.03904,0,0,-0.03222,-0.05856,0.06352,0,0,0.07207,0,-0.1187,-0.09396,-0.06222,-0.05678,-0.06905,-0.0738,-0.1032,0,0,0.04851,0,0,0,-0.1093,0.08248,0,0.1504,0,0,-0.04357,0,-0.03681,0,0,0,-0.04913,0,0,0,-0.04461,0.07535,-0.03673,-0.1615,0,0,0.03784,-0.05185,0,0,-0.07313,-0.03091,0,-0.05664,0,0,0,-0.01888,-0.04317,0,0,-0.1057,-0.065,0,-0.06388,0,-0.08731,0.07891,0.06028,0,0.04852,0.06057,0,0,0,0.02499,0.04236,-0.1097,-0.04415,0,0,0,0.06091,0.02327,-0.04656,0,0,0,0,0,0,0.0003338,0.0001883,-0.001173,0.001085,0.006852,0.002606,-0.01243,0.006503,0,-0.01421,0,0,-0.01712,0.003811,-0.001945,-0.0002187,-0.0002187,-0.0002187,-0.0002187,-0.0002187,0.004827,0.004827,0.004827,0.004827,0.004827)
	test_set_file = open(TESTpls,"r")
	test_set_file.readline()
	for line in test_set_file.readlines():
		tokens = string.strip(line).split(",")
		name = tokens[0]
		y_pred = LV4_coefficients[0]
		for i in range(1,len(tokens)-1):
			y_pred += (float(tokens[i])*LV4_coefficients[i])
		pls_regression_varSelection_results[name] = y_pred
	
def pls_regression_varSelection_extValidation__20_20(TESTpls):	
	#first value is the intercept, remaining values are the 208 descriptor's coefficients
	LV4_coefficients = (0.7557,-0.001058,0.00361,-0.001695,-0.001902,-0.008563,0,0,-0.003166,0,0.007575,-0.003855,-0.005526,0.0008996,0.002364,-0.005692,0.007591,-0.005725,0.002997,0,-0.005318,-0.03727,0,0.004521,0,0,0.01519,0,0,0.0148,0,0.03041,0,-0.01533,0,-0.009895,0.0134,-0.03508,0,0,0,0.0311,0.02359,-0.02256,-0.008678,0,0.0117,0,-0.04636,0,0.01193,-0.03537,0,0.02587,0,0,-0.03914,0,-0.01695,-0.02217,0.02586,0,0.01495,-0.02155,0.002396,0,0.03985,0.01572,-0.001543,-0.0168,0.04709,0,0,0,0.008142,0.03513,-0.01359,-0.01088,0,0,0,-0.02011,-0.02866,0.02489,-0.02666,-0.02563,0,-0.04631,-0.0818,-0.02779,0.01488,0.02456,0,0,0.01425,-0.02695,0,-0.07636,-0.0688,0,0,-0.05296,0.1474,-0.05371,-0.099,-0.1407,0,0,0,-0.08539,-0.07831,0,-0.04679,0,0,0.04379,-0.02873,-0.156,0.1063,-0.06901,0.1232,0,0,0,0,-0.0304,0,0,0,0.06625,0,-0.06827,-0.02671,0,0.103,0,-0.1127,0,0,0.07858,-0.06582,0,0,-0.1015,0.04342,0,0,-0.03649,0,0,0,0,0,0,-0.09337,-0.03322,-0.04095,0,0,-0.07249,0.06486,0.03352,0,0,0.1033,0,0,0.03306,0.06073,0,-0.05355,-0.0771,0,0,0,0.04015,0,0,0.07494,0.0525,0,0,-0.06571,0,-0.00006273,0.0001326,-0.00222,0.00138,-0.005992,0.008417,-0.02021,0,0.02155,-0.008776,0,0,-0.02236,0.00577,-0.001623,-0.002328,-0.002328,-0.002328,-0.002328,-0.002328,0.009689,0.009689,0.009689,0.009689,0.009689)
	test_set_file = open(TESTpls,"r")
	test_set_file.readline()
	for line in test_set_file.readlines():
		tokens = string.strip(line).split(",")
		name = tokens[0]
		y_pred = LV4_coefficients[0]
		for i in range(1,len(tokens)-1):
			y_pred += (float(tokens[i])*LV4_coefficients[i])
		pls_regression_varSelection_results[name] = y_pred
	
def pls_regression_varSelection_extValidation_NULL(TESTpls):	
	test_set_file = open(TESTpls,"r")
	test_set_file.readline()
	for line in test_set_file.readlines():
		tokens = string.strip(line).split(",")
		name = tokens[0]
		y_pred = -999.999	
		pls_regression_varSelection_results[name] = y_pred
	
	
	
