#!/bin/sh

# Args:
#        Project Folder
report_project() {
  session_count=0
  most_recent="NA"
  if [ -e $1/arc001 ] ; then
   session_count=`ls $1/arc001 | wc -l`
   xy=`ls -ltd $1/arc001/* | head -1`
   date_string=`echo $xy | sed -e 's/  */ /g' | cut -d ' ' -f 6,7,8`
  fi
  echo "$1$TAB$session_count$TAB$date_string"
}

pushd /data/CNDA/archive > /dev/null

TAB=" "

for project in *; do
 report_project $project
done

