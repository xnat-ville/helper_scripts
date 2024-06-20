#!/bin/sh

rm -rf /tmp/type2/*
mkdir -p /tmp/type2

findscu -od /tmp/type2 -X -S -k QueryRetrieveLevel="STUDY" -k PatientName="" -k AccessionNumber="$2" -k PatientID="$1" -k StudyInstanceUID="" --aetitle CLINICAL1 --call BJC_DR_ARCHIVE 10.50.141.8 12000
ls /tmp/type2
