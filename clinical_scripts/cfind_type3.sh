#!/bin/sh

rm -rf /tmp/type3/*
mkdir -p /tmp/type3

findscu -od /tmp/type3 -X -S -k QueryRetrieveLevel="STUDY" -k PatientName="$1" -k StudyDate="$2" -k PatientBirthDate="$3" -k Modality="$4" -k PatientID="" -k StudyInstanceUID="" --aetitle CLINICAL1 --call BJC_DR_ARCHIVE 10.50.141.8 12000

ls /tmp/type3
