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
	model = r("activity ~ .")
	PLSfit = with_mode(NO_CONVERSION, r.plsr)(model,20,data=TRAINpls, scale=r.TRUE)
	
	PLSval = with_mode(NO_CONVERSION, r.plsr)(model,20,data=TRAINpls,validation="CV", scale=r.TRUE)
	r.summary(PLSval)
	r.png("PLS_cv.png", width=400, height=350)
	r.plot(PLSval, "val")
	r.dev_off()
	

pls_regression_results = {}	
def pls_regression_ext_validation(TRAINpls,TESTpls,activity_dict,NAMES,output_type):	
	model = r("activity ~ .")
	PLSfit = with_mode(NO_CONVERSION, r.plsr)(model,10,data=TRAINpls, scale=r.TRUE)
	PLSpred = r.predict(PLSfit,TESTpls) #numpy_array
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
		print "LV1", r.cor(pls_exp,pls_pred_1)
		print "LV2", r.cor(pls_exp,pls_pred_2)
		print "LV3", r.cor(pls_exp,pls_pred_3)
		print "LV4", r.cor(pls_exp,pls_pred_4) # or one can use the R function -->  r.cor(pls_exp,pls_pred_4)
		print "LV5", r.cor(pls_exp,pls_pred_5)
		print "LV6", r.cor(pls_exp,pls_pred_6)
		print "LV7", r.cor(pls_exp,pls_pred_7)
		print "LV8", r.cor(pls_exp,pls_pred_8)
		print "LV9", r.cor(pls_exp,pls_pred_9)
		print "LV10", r.cor(pls_exp,pls_pred_10)
		r.png("PLS_ext_pred.png", width=400, height=350)
		r.plot(pls_exp,pls_pred_4)
		r.dev_off()
	elif output_type == "predict":
		for key in pls_ext_pred_6.keys():
			pls_regression_results[key] = pls_ext_pred_6[key]
	
	
	

svm_regression_results = {}		
def svm_regression(TRAINsvm,TESTsvm,activity_dict,output_type):
	formula = r("activity ~ .")
	SVMfit = with_mode(NO_CONVERSION, r.svm)(formula,data=TRAINsvm, scale=r.TRUE)
	SVMself = with_mode(NO_CONVERSION, r.predict)(SVMfit,TRAINsvm)
	SVMpred = with_mode(NO_CONVERSION, r.predict)(SVMfit,TESTsvm)
	#for obj in SVMfit:
	if output_type == "build":
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
	else:
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
			print
			

	
			
rf_regression_results = {}
def rf_regression(TRAINrf,TESTrf,activity_dict,output_type):
	model = r("activity ~ .")
	RFmod = r.randomForest(model,data=TRAINrf,xtest=TESTrf,scale=r.TRUE,ntree=1000) #5000 is more reliable but it takes longer
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
	RFmod = r.randomForest(model,data=TRAINrf,xtest=TESTrf,scale=r.TRUE,ntree=1000) #5000 is more reliable but it takes longer
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
		print	
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
		print	
				
	elif output_type == "predict":
		external_pred = RFmod['test']['predicted']
		for key in external_pred.keys():
			rf_classification_results[key] = external_pred[key]
			

pls_regression_varSelection_results = {}	
def pls_regression_varSelection_extValidation(TESTpls):	
	#first value is the intercept, remaining values are the 313 descriptor's coefficients
	LV3_coefficients = (63.63,0.5271,-5.398,-3.395,0,1.884,-0.3211,-0.6358,-1.15,2.34,0.5226,-1.227,-1.556,1.61,-1.489,1.421,-2.157,0,2.468,0,-1.727,0,-3.201,-0.3761,2.883,-1.702,-1.356,0,2.215,0,-1.814,0,1.442,-2.619,3.076,1.603,-2.082,2.797,-2.666,-1.023,0,0,0.2344,2.781,-2.123,-1.777,-1.106,0.05582,2.422,0,0,1.354,-1.196,3.741,-4.291,0,0.1678,-3.848,3.794,0.7811,0,1.322,0,-0.629,0.729,0,0,-1.015,0,-0.8461,2.267,-1.624,-0.6412,-5.065,2.074,-4.133,4.747,1.032,4.006,-3.841,-0.9858,0,0,0,2.823,-0.05147,0.1729,-0.11,-0.09794,0.055,-0.0421,0.5175,0.7696,0.0006497,-0.2065,-0.8756,0.1386,0.1913,0.5242,-0.6247,-0.224,0.5665,0.3697,0.5626,-0.764,-0.4865,-0.03976,-0.6843,1.539,-0.7842,-1.046,-3.407,3.421,3.687,0,1.745,1.621,1.06,0.2596,0.7939,0.1448,-1.677,-0.1947,0.2598,-0.6906,-0.1139,-1.01,-0.7949,-1.058,-1.857,2.827,-0.5307,-0.8922,0.4929,-2.242,-0.00786,0,-0.2106,0.8451,0,0.4082,2.496,0.4999,2.34,-6.114,-1.656,1.83,-3.881,0,0.8127,0.2629,-1.072,-0.7517,2.689,-1.409,7.272,0.746,-1.708,1.223,-1.321,2.664,-0.2414,0.3553,-1.39,-1.663,0,-0.3207,1.381,-1.548,-1.383,0,-2.447,-7.108,-0.8358,-0.2735,3.246,4.215,1.234,-2.646,0.01932,-6.069,0,-7.22,-2.693,0.5493,3.189,-0.9048,0,10.36,0,-1.943,0,-1.527,0,0,0,0,5.497,0,-1.088,-0.9825,-3.075,0,-2.899,0,-1.098,0,2.483,-3.626,5.56,3.85,-3.892,3.094,0,-0.9136,5.246,2.571,0.9065,1.093,2.135,1.349,1.75,0,1.715,2.617,1.637,0,4.374,4.793,0,0,3.571,0,-2.331,3.625,-2.996,0,0,-2.871,3.572,2.604,0,0,-5.943,3.314,-1.887,-1.518,-2.124,0,-3.589,-2.524,-1.006,0,0,-4.316,-5.065,0,4.195,0,0,0.9646,2.063,2.803,0,-1.421,0,0,4.286,0,2.854,0,-0.8618,1.569,-0.8474,0,0,0,0,0.01875,0.006392,0.08018,-0.04263,-0.4131,-0.1849,-0.364,-0.5908,-0.3863,-0.5638,0.2958,0.4941,0.3497,-0.2772,-0.09434,-0.08914,-0.6914,0.7254,0.2053,0.585,-1.34,0.7788,1.825,0.6545,-1.79,-0.7297,-0.003391,-0.7586,0.84,1.81,-0.3274,-0.8272,1.146,-0.5551,-0.1966,0.2549)
	test_set_file = open(TESTpls,"r")
	test_set_file.readline()
	for line in test_set_file.readlines():
		tokens = string.strip(line).split(",")
		name = tokens[0]
		y_pred = LV3_coefficients[0]
		for i in range(1,len(tokens)-1):
			y_pred += (float(tokens[i])*LV3_coefficients[i])
		pls_regression_varSelection_results[name] = y_pred


