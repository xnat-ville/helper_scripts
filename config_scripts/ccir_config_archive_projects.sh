#!/bin/sh

# Add configuration information for CCIR Archive Projects such as CCIR_BIOPMR_2024
# This should only be used in a test environment as it hard codes the id of a row
# in the xhbm_configuration_data table.
# There is probably a better way to do this.  In the mean time, ....
# This script assumes you are on the system with the XNAT database.

DB=xnat

psql -U xnat -c "delete from xhbm_configuration      where config_data=100000" $DB
psql -U xnat -c "delete from xhbm_configuration_data where id=100000" $DB

psql -U xnat -c "insert into xhbm_configuration_data 
(id,created,disabled,enabled,timestamp, contents) VALUES 
(100000, '2024-04-20', '2024-04-21', 't', '2024-04-22',
'{"contents": "CCIRWP-MR30A=CCIR_PRISMA_20\nCCIRWP-CTDSA=CCIR_SOMATOM\nCCIRWP-PETMR=CCIR_BIOPMR_20\nCCIRWP-PETCTA=CCIR_BIOPCT_20\nCCIRWP-MR15A=CCIR_AVANTO\nCCIR_ARC_TEST=CCIR_ARC_TEST\nWP-MR15A=CCIR_AVANTO\nWP-MR30A=CCIR_PRISMA_20\nWP-PETCTA=CCIR_BIOPCT_20\nWP-PETMRA=CCIR_BIOPMR_20\n","project":"","unversioned":"false","create_date":"2014-03-10","user":"admin","version":"3","tool":"CCIR","status":"enabled"}')" \
$DB


psql -U xnat -c "insert into xhbm_configuration
(created,disabled,enabled,timestamp, status, tool, path,version,xnat_user,config_data,scope) VALUES 
('2024-04-20', '2024-04-21', 't', '2024-04-22', 'enabled', 'CCIR', 'projectMapConfig', 1, 'admin', 100000, 0)" $DB
