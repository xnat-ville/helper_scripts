#!/bin/sh

rm -rf /tmp/patient/*
mkdir -p /tmp/patient

findscu -od /tmp/patient -X -S -k QueryRetrieveLevel="STUDY" -k PatientName="" -k StudyDate="" -k ModalitiesInStudy="" -k AccessionNumber="" -k PatientID="$1" -k StudyInstanceUID="" --aetitle CLINICAL1 --call BJC_DR_ARCHIVE 10.50.141.8 12000
ls /tmp/patient
