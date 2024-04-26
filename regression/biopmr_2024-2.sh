#!/bin/sh

REGRESSION_BASE=`dirname $0`
BASE=$REGRESSION_BASE/..

source ./$BASE/scripts/dcm4che_storescu.sh

echo $DCM4CHE_STORESCU

echo $DCM4CHE_STORESCU	\
	-s \"00081010=XXWP-PETMRA\"			\
	-s \"00081030=CCIR-01400\^CCIR-1414 Vlassenko\"	\
	-s \"00081040=WUSTL-TEST\"			\
	-s \"00081090=Biograph_mMR\"			\
	-s \"00100010=WSCT4509_02\"			\
	-s \"00100020=WSCT4509_FDG2_20240419\"		\
	-b CCIR-CTP -c CNDA_CCIR@localhost:8104 $REGRESSION_BASE/datasets/501_1-1.dcm

     $DCM4CHE_STORESCU	\
	-s \"00081010=XXWP-PETMRA\"			\
	-s \"00081030='CCIR-01400^CCIR-1414 Vlassenko'\"\
	-s \"00081040=WUSTL-TEST\"			\
	-s \"00081090=Biograph_mMR\"			\
	-s \"00100010=WSCT4509_02\"			\
	-s \"00100020=WSCT4509_FDG2_20240419\"		\
	-b CCIR-CTP -c CNDA_CCIR@localhost:8104 $REGRESSION_BASE/datasets/501_1-1.dcm
