runAntisenseDesign.py EnumerationResult.csv
antisense_predictor.py AOBase AOBase_542seq_cleaned_modelBuilding_Jan2009_15_21_noOutliers.csv c_a_thermo predict EnumerationResult_clean.csv < input_15_21_100_1000_12.txt
rm EnumerationResult_clean.csv

if [ -f ASOOffTargetSearchResult.csv ]; then
	mergeASO.py ASOOffTargetSearchResult.csv OuTpUt_ReSuLtS.csv
else
	mergeASO.py EnumerationResult.csv OuTpUt_ReSuLtS.csv
fi

rm antisense_descriptors.pyc antisense_load_dataset.pyc antisense_stats.pyc



