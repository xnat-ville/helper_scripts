#!/bin/sh

REGRESSION_BASE=`dirname $0`
BASE=$REGRESSION_BASE/..

# Required arguments are:
#    File/folder to store
#    Scanner Label: BAY1 BAY2 BAY3 NRB1
#    Project Label
#    Subject Label
#    Session Label
# We add these optional arguments
#    [Alternate Target AE title] (repeat the default)
#    [Alternate Target Host]     (default host is cnda-shadow03.nrg.wustl.edu)
#    [Alternate Target Port]     (default port is 8104)
#    

$BASE/scripts/mrf_storescu_delegate.sh	\
	$REGRESSION_BASE/datasets/501_1-1.dcm BAY1 STORE_TEST SUBJECT_1 SESSION_1_x CNDA_BAY1 localhost 8104

