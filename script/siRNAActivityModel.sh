cp EnumerationResult.csv oligo2predict_noOverhangs.csv
get_overhangs.py target.txt txt oligo2predict_noOverhangs.csv
lowercase.py oligo2predict.csv
siRNA_predictor.py novartis siRNA_2431seq_modelBuilding.csv p_c_a_thermo predict oligo2predict_clean.csv

if [ -f siRNAOffTargetSearchResult.csv ]; then
    cp siRNAOffTargetSearchResult.csv outputSummaryBeforeMerge.csv
else
    cp EnumerationResult.csv outputSummaryBeforeMerge.csv
fi
 
cat OuTpUt_ReSuLtS.csv|cut -f 1-3,5-9,18,22-24 -d ',' |sed 's/siRNA_id,/name,/'|sed 's/G:C_content/GC_content/'|tr ',' '\t' >svm_out.txt
cat outputSummaryBeforeMerge.csv|tr ',' '\t' |mergeEx.pl 1 1 svm_out.txt keepAll 1|tr '\t' ','>siRNAActivityModelResult.csv

rm siRNA_descriptors.pyc load_dataset.pyc siRNA_stats.pyc

